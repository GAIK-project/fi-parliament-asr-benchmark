"""
Finnish Parliament ASR Benchmark
Backends: Azure Whisper, Azure gpt-4o-transcribe, Local WhisperX
Metrics: WER, CER, latency, RTF (deterministic scoring only)
"""

import argparse
import csv
import json
import os
import random
import re
import time
import unicodedata
from datetime import datetime
from pathlib import Path

import requests
import soundfile as sf
from dotenv import load_dotenv
from jiwer import wer, cer
from openai import AzureOpenAI
from tqdm import tqdm

load_dotenv()

# ---------------------------------------------------------------------------
# Paths and splits
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).parent / "fi-parliament-asr"

SPLITS = {
    "2016-dev-seen":    BASE_DIR / "2016-dev" / "seen",
    "2016-dev-unseen":  BASE_DIR / "2016-dev" / "unseen",
    "2016-test-seen":   BASE_DIR / "2016-test" / "seen",
    "2016-test-unseen": BASE_DIR / "2016-test" / "unseen",
    "2020-test":        BASE_DIR / "2020-test",
}

# ---------------------------------------------------------------------------
# Benchmark configurations
# ---------------------------------------------------------------------------
CORE_CONFIGS = [
    {"name": "azure_whisper_fi",             "backend": "azure_whisper",    "language": "fi"},
    {"name": "azure_whisper_auto",           "backend": "azure_whisper",    "language": "auto"},
    {"name": "azure_gpt4o_transcribe_fi",    "backend": "azure_gpt4o",     "language": "fi"},
    {"name": "azure_gpt4o_transcribe_auto",  "backend": "azure_gpt4o",     "language": "auto"},
    {"name": "local_whisper_fi",             "backend": "local_whisper",    "language": "fi"},
    {"name": "local_whisper_auto",           "backend": "local_whisper",    "language": "auto"},
]

OPTIONAL_CONFIGS = [
    {
        "name": "local_whisper_fi_with_prompt",
        "backend": "local_whisper",
        "language": "fi",
        "initial_prompt": "Eduskunnan täysistunto. Suomalainen parlamenttipuhe.",
    },
]

# ---------------------------------------------------------------------------
# Text normalization
# ---------------------------------------------------------------------------
def normalize_finnish(text: str) -> str:
    """Normalize text for fair WER/CER comparison on Finnish."""
    text = unicodedata.normalize("NFC", text)
    text = text.lower()
    # Keep only letters (including äöå), digits, and whitespace
    text = re.sub(r"[^a-zäöå0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# ---------------------------------------------------------------------------
# Dataset loader
# ---------------------------------------------------------------------------
def load_samples(
    split_dir: Path,
    limit: int | None = None,
    seed: int = 42,
) -> list[dict]:
    """Discover .wav + .trn pairs and return sample dicts."""
    wavs = sorted(split_dir.rglob("*.wav"))
    if limit:
        random.seed(seed)
        wavs = random.sample(wavs, min(limit, len(wavs)))

    samples = []
    for wav in wavs:
        trn = wav.with_suffix(".trn")
        if not trn.exists():
            continue
        ref = trn.read_text(encoding="utf-8").strip()
        try:
            info = sf.info(str(wav))
            duration = info.duration
        except Exception:
            duration = 0.0
        samples.append({
            "wav": wav,
            "file_id": wav.stem,
            "reference": normalize_finnish(ref),
            "audio_duration_sec": duration,
        })
    return samples


# ---------------------------------------------------------------------------
# Azure client
# ---------------------------------------------------------------------------
def build_azure_client() -> AzureOpenAI:
    api_key = os.getenv("AZURE_API_KEY")
    endpoint = os.getenv("AZURE_API_BASE") or os.getenv("AZURE_ENDPOINT")
    version = os.getenv("AZURE_API_VERSION", "2024-12-01-preview")
    if not api_key or not endpoint:
        raise EnvironmentError(
            "AZURE_API_KEY and AZURE_API_BASE (or AZURE_ENDPOINT) must be set in .env"
        )
    return AzureOpenAI(api_key=api_key, azure_endpoint=endpoint, api_version=version)


# ---------------------------------------------------------------------------
# Transcription backends
# ---------------------------------------------------------------------------
def transcribe_azure_whisper(
    client: AzureOpenAI, wav_path: Path, language: str,
) -> str:
    kwargs = {"model": "whisper", "file": open(wav_path, "rb"), "response_format": "text"}
    if language != "auto":
        kwargs["language"] = language
    try:
        result = client.audio.transcriptions.create(**kwargs)
    finally:
        kwargs["file"].close()
    return result if isinstance(result, str) else result.text


def transcribe_azure_gpt4o(
    client: AzureOpenAI, wav_path: Path, language: str,
) -> str:
    kwargs = {"model": "gpt-4o-transcribe", "file": open(wav_path, "rb")}
    if language != "auto":
        kwargs["language"] = language
    try:
        result = client.audio.transcriptions.create(**kwargs)
    finally:
        kwargs["file"].close()
    return result if isinstance(result, str) else result.text


def transcribe_whisper_local(
    wav_path: Path,
    api_base: str,
    api_key: str,
    language: str,
    initial_prompt: str | None = None,
) -> str:
    """Call local WhisperX endpoint (same API as GAIK toolkit whisper_local.py)."""
    with open(wav_path, "rb") as f:
        payload = {
            "language": language,
            "diarization": False,
        }
        if initial_prompt:
            payload["initial_prompt"] = initial_prompt
        resp = requests.post(
            f"{api_base}/transcribe",
            data=payload,
            files={"file": (wav_path.name, f)},
            headers={"key": api_key},
            timeout=60 * 10,
        )
    resp.raise_for_status()
    data = resp.json()
    text = (data.get("text") or "").strip()
    if not text:
        segments = data.get("segments") or []
        text = " ".join(s.get("text", "").strip() for s in segments if s.get("text")).strip()
    return text


# ---------------------------------------------------------------------------
# Dispatch with retry
# ---------------------------------------------------------------------------
RETRY_DELAYS = [5, 10, 20]


def dispatch_transcribe(
    config: dict,
    wav_path: Path,
    azure_client: AzureOpenAI | None,
    local_api_base: str | None,
    local_api_key: str | None,
) -> str:
    backend = config["backend"]
    language = config["language"]

    for attempt in range(len(RETRY_DELAYS) + 1):
        try:
            if backend == "azure_whisper":
                return transcribe_azure_whisper(azure_client, wav_path, language)
            elif backend == "azure_gpt4o":
                return transcribe_azure_gpt4o(azure_client, wav_path, language)
            elif backend == "local_whisper":
                return transcribe_whisper_local(
                    wav_path, local_api_base, local_api_key, language,
                    initial_prompt=config.get("initial_prompt"),
                )
            else:
                raise ValueError(f"Unknown backend: {backend}")
        except Exception as e:
            err_str = str(e)
            is_rate_limit = "429" in err_str or "rate" in err_str.lower()
            if is_rate_limit and attempt < len(RETRY_DELAYS):
                wait = RETRY_DELAYS[attempt]
                tqdm.write(f"    Rate limited, retrying in {wait}s...")
                time.sleep(wait)
                continue
            raise


# ---------------------------------------------------------------------------
# Core benchmark runner
# ---------------------------------------------------------------------------
def run_benchmark(
    configs: list[dict],
    splits: list[str],
    limit: int | None,
    output_dir: Path,
    delay: float,
    seed: int,
    local_api_base: str | None,
    local_api_key: str | None,
):
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:20]
    run_dir = output_dir / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    # Build Azure client (may be None if only local configs)
    azure_client = None
    needs_azure = any(c["backend"].startswith("azure") for c in configs)
    if needs_azure:
        azure_client = build_azure_client()

    all_rows: list[dict] = []
    config_manifest = []

    for cfg in configs:
        config_manifest.append(cfg.copy())

    for split_name in splits:
        split_dir = SPLITS.get(split_name)
        if not split_dir or not split_dir.exists():
            print(f"  Skipping {split_name} (not found: {split_dir})")
            continue

        samples = load_samples(split_dir, limit, seed)
        print(f"\n{'='*60}")
        print(f"Split: {split_name} ({len(samples)} samples)")
        print(f"{'='*60}")

        for cfg in configs:
            # Skip local configs if no endpoint configured
            if cfg["backend"] == "local_whisper" and not local_api_base:
                print(f"  Skipping {cfg['name']} (LOCAL_WHISPER_API_BASE not set)")
                continue

            print(f"\n  Config: {cfg['name']}")
            success_count = 0
            error_count = 0

            for sample in tqdm(samples, desc=f"  {cfg['name']}", leave=False):
                row = {
                    "config": cfg["name"],
                    "backend": cfg["backend"],
                    "language": cfg["language"],
                    "split": split_name,
                    "file_id": sample["file_id"],
                    "audio_path": str(sample["wav"]),
                    "audio_duration_sec": sample["audio_duration_sec"],
                    "reference": sample["reference"],
                }

                start_t = time.perf_counter()
                try:
                    raw_hyp = dispatch_transcribe(
                        cfg, sample["wav"], azure_client, local_api_base, local_api_key,
                    )
                    elapsed = time.perf_counter() - start_t
                    hyp_norm = normalize_finnish(raw_hyp)

                    sample_wer = wer(sample["reference"], hyp_norm) if sample["reference"] else 0.0
                    sample_cer = cer(sample["reference"], hyp_norm) if sample["reference"] else 0.0

                    ref_words = len(sample["reference"].split()) if sample["reference"] else 0
                    hyp_words = len(hyp_norm.split()) if hyp_norm else 0
                    word_ratio = hyp_words / ref_words if ref_words > 0 else 0.0

                    row.update({
                        "hypothesis": hyp_norm,
                        "hypothesis_raw": raw_hyp.strip(),
                        "wer": round(sample_wer, 6),
                        "cer": round(sample_cer, 6),
                        "latency_sec": round(elapsed, 3),
                        "rtf": round(elapsed / sample["audio_duration_sec"], 4) if sample["audio_duration_sec"] > 0 else None,
                        "ref_words": ref_words,
                        "hyp_words": hyp_words,
                        "word_ratio": round(word_ratio, 3),
                        "error": "",
                    })
                    success_count += 1
                except Exception as e:
                    elapsed = time.perf_counter() - start_t
                    row.update({
                        "hypothesis": "",
                        "hypothesis_raw": "",
                        "wer": None,
                        "cer": None,
                        "latency_sec": round(elapsed, 3),
                        "rtf": None,
                        "error": str(e),
                    })
                    error_count += 1
                    tqdm.write(f"    ERROR {sample['file_id']}: {e}")

                all_rows.append(row)

                if delay > 0:
                    time.sleep(delay)

            # Print per-config summary
            cfg_rows = [r for r in all_rows if r["config"] == cfg["name"] and r["split"] == split_name and not r["error"]]
            if cfg_rows:
                refs = [r["reference"] for r in cfg_rows]
                hyps = [r["hypothesis"] for r in cfg_rows]
                agg_wer = wer(refs, hyps)
                agg_cer = cer(refs, hyps)
                avg_lat = sum(r["latency_sec"] for r in cfg_rows) / len(cfg_rows)
                print(f"    WER: {agg_wer*100:.2f}%  CER: {agg_cer*100:.2f}%  "
                      f"Avg latency: {avg_lat:.2f}s  Errors: {error_count}/{len(samples)}")

    # Save outputs
    save_per_file_csv(all_rows, run_dir / "per_file_results.csv")
    leaderboard_overall = build_leaderboard_overall(all_rows)
    leaderboard_by_split = build_leaderboard_by_split(all_rows)
    save_leaderboard_csv(leaderboard_overall, run_dir / "leaderboard_overall.csv")
    save_leaderboard_csv(leaderboard_by_split, run_dir / "leaderboard_by_split.csv")

    summary = {
        "run_id": run_id,
        "timestamp": datetime.now().isoformat(),
        "dataset_dir": str(BASE_DIR),
        "splits": splits,
        "limit": limit,
        "seed": seed,
        "delay": delay,
        "configs": config_manifest,
        "leaderboard_overall": leaderboard_overall,
        "leaderboard_by_split": leaderboard_by_split,
        "total_samples": len(all_rows),
        "total_errors": sum(1 for r in all_rows if r["error"]),
    }
    with open(run_dir / "summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    report_md = generate_report(summary, all_rows, leaderboard_overall, leaderboard_by_split)
    (run_dir / "report.md").write_text(report_md, encoding="utf-8")

    print(f"\nResults saved to: {run_dir}")
    print_console_summary(leaderboard_overall)


# ---------------------------------------------------------------------------
# Leaderboard builders
# ---------------------------------------------------------------------------
def _aggregate_rows(rows: list[dict]) -> dict:
    """Compute aggregate metrics for a list of per-file result rows."""
    valid = [r for r in rows if not r["error"]]
    if not valid:
        return {"n_samples": 0, "n_errors": len(rows), "wer_pct": None, "cer_pct": None,
                "avg_latency_sec": None, "avg_rtf": None}
    refs = [r["reference"] for r in valid]
    hyps = [r["hypothesis"] for r in valid]
    agg_wer = wer(refs, hyps)
    agg_cer = cer(refs, hyps)
    avg_lat = sum(r["latency_sec"] for r in valid) / len(valid)
    rtfs = [r["rtf"] for r in valid if r["rtf"] is not None]
    avg_rtf = sum(rtfs) / len(rtfs) if rtfs else None
    word_ratios = [r.get("word_ratio", 1.0) for r in valid if r.get("word_ratio") is not None]
    avg_word_ratio = sum(word_ratios) / len(word_ratios) if word_ratios else None
    truncated = sum(1 for wr in word_ratios if wr < 0.5)
    return {
        "n_samples": len(valid),
        "n_errors": len(rows) - len(valid),
        "wer_pct": round(agg_wer * 100, 2),
        "cer_pct": round(agg_cer * 100, 2),
        "avg_latency_sec": round(avg_lat, 3),
        "avg_rtf": round(avg_rtf, 4) if avg_rtf else None,
        "avg_word_ratio": round(avg_word_ratio, 3) if avg_word_ratio else None,
        "n_truncated": truncated,
    }


def build_leaderboard_overall(all_rows: list[dict]) -> list[dict]:
    configs_seen = {}
    for r in all_rows:
        configs_seen.setdefault(r["config"], []).append(r)
    board = []
    for config_name, rows in configs_seen.items():
        agg = _aggregate_rows(rows)
        entry = {"config": config_name, "backend": rows[0]["backend"], "language": rows[0]["language"]}
        entry.update(agg)
        board.append(entry)
    board.sort(key=lambda x: (x["wer_pct"] if x["wer_pct"] is not None else 999))
    return board


def build_leaderboard_by_split(all_rows: list[dict]) -> list[dict]:
    groups = {}
    for r in all_rows:
        key = (r["config"], r["split"])
        groups.setdefault(key, []).append(r)
    board = []
    for (config_name, split_name), rows in groups.items():
        agg = _aggregate_rows(rows)
        entry = {"config": config_name, "split": split_name, "backend": rows[0]["backend"], "language": rows[0]["language"]}
        entry.update(agg)
        board.append(entry)
    board.sort(key=lambda x: (x["split"], x["wer_pct"] if x["wer_pct"] is not None else 999))
    return board


# ---------------------------------------------------------------------------
# File writers
# ---------------------------------------------------------------------------
CSV_COLUMNS = [
    "config", "backend", "language", "split", "file_id",
    "reference", "hypothesis", "hypothesis_raw",
    "wer", "cer", "latency_sec", "rtf", "audio_duration_sec",
    "ref_words", "hyp_words", "word_ratio", "error",
]

LEADERBOARD_COLUMNS = [
    "config", "backend", "language", "n_samples", "n_errors",
    "wer_pct", "cer_pct", "avg_latency_sec", "avg_rtf",
]

LEADERBOARD_SPLIT_COLUMNS = [
    "config", "split", "backend", "language", "n_samples", "n_errors",
    "wer_pct", "cer_pct", "avg_latency_sec", "avg_rtf",
]


def save_per_file_csv(rows: list[dict], path: Path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS, extrasaction="ignore")
        writer.writeheader()
        for r in rows:
            writer.writerow(r)


def save_leaderboard_csv(board: list[dict], path: Path):
    if not board:
        return
    cols = LEADERBOARD_SPLIT_COLUMNS if "split" in board[0] else LEADERBOARD_COLUMNS
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        writer.writeheader()
        for r in board:
            writer.writerow(r)


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------
def generate_report(
    summary: dict,
    all_rows: list[dict],
    leaderboard_overall: list[dict],
    leaderboard_by_split: list[dict],
) -> str:
    lines = []
    lines.append("# Finnish Parliament ASR Benchmark Report")
    lines.append("")
    lines.append(f"**Run ID:** {summary['run_id']}")
    lines.append(f"**Timestamp:** {summary['timestamp']}")
    lines.append(f"**Dataset:** {summary['dataset_dir']}")
    lines.append(f"**Splits:** {', '.join(summary['splits'])}")
    lines.append(f"**Limit per split:** {summary['limit'] or 'all'}")
    lines.append(f"**Total samples:** {summary['total_samples']}")
    lines.append(f"**Total errors:** {summary['total_errors']}")
    lines.append("")

    # Dataset split sizes
    lines.append("## Dataset Splits")
    lines.append("")
    for split_name in summary["splits"]:
        split_dir = SPLITS.get(split_name)
        if split_dir and split_dir.exists():
            n_files = len(list(split_dir.rglob("*.wav")))
            lines.append(f"- **{split_name}**: {n_files} audio files")
    lines.append("")

    # Config manifest
    lines.append("## Configuration Matrix")
    lines.append("")
    lines.append("| Config | Backend | Language |")
    lines.append("| ------ | ------- | -------- |")
    for c in summary["configs"]:
        prompt_note = " (+prompt)" if c.get("initial_prompt") else ""
        lines.append(f"| {c['name']} | {c['backend']}{prompt_note} | {c['language']} |")
    lines.append("")

    # Overall leaderboard
    lines.append("## Overall Leaderboard")
    lines.append("")
    lines.append("| Rank | Config | WER% | CER% | Samples | Errors | Avg Latency | Avg RTF | Word Ratio | Truncated |")
    lines.append("| ---- | ------ | ---- | ---- | ------- | ------ | ----------- | ------- | ---------- | --------- |")
    for i, entry in enumerate(leaderboard_overall, 1):
        wer_s = f"{entry['wer_pct']:.2f}" if entry["wer_pct"] is not None else "N/A"
        cer_s = f"{entry['cer_pct']:.2f}" if entry["cer_pct"] is not None else "N/A"
        lat_s = f"{entry['avg_latency_sec']:.2f}s" if entry["avg_latency_sec"] is not None else "N/A"
        rtf_s = f"{entry['avg_rtf']:.3f}" if entry["avg_rtf"] is not None else "N/A"
        wr_s = f"{entry.get('avg_word_ratio', 0):.2f}" if entry.get("avg_word_ratio") else "N/A"
        tr_s = str(entry.get("n_truncated", 0))
        lines.append(f"| {i} | {entry['config']} | {wer_s} | {cer_s} | {entry['n_samples']} | {entry['n_errors']} | {lat_s} | {rtf_s} | {wr_s} | {tr_s} |")
    lines.append("")

    # Per-split leaderboard
    lines.append("## Per-Split Leaderboard")
    lines.append("")
    current_split = None
    for entry in leaderboard_by_split:
        if entry["split"] != current_split:
            current_split = entry["split"]
            lines.append(f"### {current_split}")
            lines.append("")
            lines.append("| Config | WER% | CER% | Samples | Errors | Avg Latency |")
            lines.append("| ------ | ---- | ---- | ------- | ------ | ----------- |")
        wer_s = f"{entry['wer_pct']:.2f}" if entry["wer_pct"] is not None else "N/A"
        cer_s = f"{entry['cer_pct']:.2f}" if entry["cer_pct"] is not None else "N/A"
        lat_s = f"{entry['avg_latency_sec']:.2f}s" if entry["avg_latency_sec"] is not None else "N/A"
        lines.append(f"| {entry['config']} | {wer_s} | {cer_s} | {entry['n_samples']} | {entry['n_errors']} | {lat_s} |")
    lines.append("")

    # fi vs auto delta table
    lines.append("## Language Setting Comparison: fi vs auto")
    lines.append("")
    fi_entries = {e["backend"]: e for e in leaderboard_overall if e["language"] == "fi"}
    auto_entries = {e["backend"]: e for e in leaderboard_overall if e["language"] == "auto"}
    if fi_entries and auto_entries:
        lines.append("| Backend | WER% (fi) | WER% (auto) | Delta | CER% (fi) | CER% (auto) | Delta |")
        lines.append("| ------- | --------- | ----------- | ----- | --------- | ----------- | ----- |")
        for backend in fi_entries:
            if backend in auto_entries:
                fi = fi_entries[backend]
                auto = auto_entries[backend]
                if fi["wer_pct"] is not None and auto["wer_pct"] is not None:
                    wer_delta = fi["wer_pct"] - auto["wer_pct"]
                    cer_delta = fi["cer_pct"] - auto["cer_pct"]
                    wer_sign = "+" if wer_delta > 0 else ""
                    cer_sign = "+" if cer_delta > 0 else ""
                    lines.append(
                        f"| {backend} | {fi['wer_pct']:.2f} | {auto['wer_pct']:.2f} | "
                        f"{wer_sign}{wer_delta:.2f} | {fi['cer_pct']:.2f} | {auto['cer_pct']:.2f} | "
                        f"{cer_sign}{cer_delta:.2f} |"
                    )
    lines.append("")

    # Top 5 worst files by WER
    lines.append("## Top 5 Worst Files by WER")
    lines.append("")
    valid_rows = [r for r in all_rows if r["wer"] is not None]
    worst = sorted(valid_rows, key=lambda r: r["wer"], reverse=True)[:5]
    if worst:
        lines.append("| Config | Split | File | WER | Reference (first 80 chars) |")
        lines.append("| ------ | ----- | ---- | --- | -------------------------- |")
        for r in worst:
            ref_short = r["reference"][:80] + ("..." if len(r["reference"]) > 80 else "")
            lines.append(f"| {r['config']} | {r['split']} | {r['file_id']} | {r['wer']*100:.1f}% | {ref_short} |")
    lines.append("")

    # Top 5 best files by WER
    lines.append("## Top 5 Best Files by WER")
    lines.append("")
    best = sorted(valid_rows, key=lambda r: r["wer"])[:5]
    if best:
        lines.append("| Config | Split | File | WER | Reference (first 80 chars) |")
        lines.append("| ------ | ----- | ---- | --- | -------------------------- |")
        for r in best:
            ref_short = r["reference"][:80] + ("..." if len(r["reference"]) > 80 else "")
            lines.append(f"| {r['config']} | {r['split']} | {r['file_id']} | {r['wer']*100:.1f}% | {ref_short} |")
    lines.append("")

    # Failure summary
    errors = [r for r in all_rows if r["error"]]
    if errors:
        lines.append("## Failure Summary")
        lines.append("")
        lines.append(f"Total failures: {len(errors)}")
        lines.append("")
        error_by_config = {}
        for r in errors:
            error_by_config.setdefault(r["config"], []).append(r)
        for config_name, errs in error_by_config.items():
            lines.append(f"- **{config_name}**: {len(errs)} failures")
            for e in errs[:3]:
                lines.append(f"  - `{e['file_id']}`: {e['error'][:100]}")
            if len(errs) > 3:
                lines.append(f"  - ... and {len(errs) - 3} more")
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Console output
# ---------------------------------------------------------------------------
def print_console_summary(leaderboard: list[dict]):
    print("\n" + "=" * 80)
    print(f"{'Config':<35} {'WER%':>8} {'CER%':>8} {'Samples':>8} {'Errors':>7} {'Latency':>9}")
    print("-" * 80)
    for entry in leaderboard:
        wer_s = f"{entry['wer_pct']:.2f}" if entry["wer_pct"] is not None else "N/A"
        cer_s = f"{entry['cer_pct']:.2f}" if entry["cer_pct"] is not None else "N/A"
        lat_s = f"{entry['avg_latency_sec']:.2f}s" if entry["avg_latency_sec"] is not None else "N/A"
        print(f"{entry['config']:<35} {wer_s:>8} {cer_s:>8} {entry['n_samples']:>8} {entry['n_errors']:>7} {lat_s:>9}")
    print("=" * 80)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Finnish Parliament ASR Benchmark")
    parser.add_argument(
        "--splits", nargs="+", default=["2016-dev-seen"],
        choices=list(SPLITS.keys()),
        help="Dataset splits to use (default: 2016-dev-seen)",
    )
    parser.add_argument("--all-splits", action="store_true", help="Run on all splits")
    parser.add_argument(
        "--limit", type=int, default=50,
        help="Max samples per split (default: 50, 0 = all)",
    )
    parser.add_argument(
        "--delay", type=float, default=0.5,
        help="Seconds between API calls (default: 0.5)",
    )
    parser.add_argument(
        "--output-dir", type=str, default="results",
        help="Output directory (default: results/)",
    )
    parser.add_argument(
        "--local-api-base", type=str,
        default=os.getenv("LOCAL_WHISPER_API_BASE"),
        help="Local WhisperX API base URL",
    )
    parser.add_argument(
        "--local-api-key", type=str,
        default=os.getenv("LOCAL_WHISPER_API_KEY"),
        help="Local WhisperX API key",
    )
    parser.add_argument("--seed", type=int, default=42, help="Random seed (default: 42)")
    parser.add_argument("--smoke", action="store_true", help="Quick test with 5 samples")
    parser.add_argument(
        "--include-optional", action="store_true",
        help="Include optional configs (initial_prompt experiment)",
    )
    parser.add_argument(
        "--backends", nargs="+",
        choices=["azure_whisper", "azure_gpt4o", "local_whisper"],
        help="Filter to specific backends",
    )

    args = parser.parse_args()

    splits = list(SPLITS.keys()) if args.all_splits else args.splits
    limit = 5 if args.smoke else (args.limit or None)

    # Build config list
    configs = list(CORE_CONFIGS)
    if args.include_optional:
        configs.extend(OPTIONAL_CONFIGS)
    if args.backends:
        configs = [c for c in configs if c["backend"] in args.backends]

    # Filter out local configs if no endpoint
    if not args.local_api_base:
        skipped = [c["name"] for c in configs if c["backend"] == "local_whisper"]
        if skipped:
            print(f"Note: Skipping local_whisper configs (no --local-api-base): {skipped}")
        configs = [c for c in configs if c["backend"] != "local_whisper"]

    if not configs:
        print("Error: No configs to run. Check --backends and endpoint settings.")
        return

    print("Finnish Parliament ASR Benchmark")
    print(f"  Configs: {[c['name'] for c in configs]}")
    print(f"  Splits:  {splits}")
    print(f"  Limit:   {limit or 'all'} samples per split")
    print(f"  Delay:   {args.delay}s between calls")
    print()

    run_benchmark(
        configs=configs,
        splits=splits,
        limit=limit,
        output_dir=Path(args.output_dir),
        delay=args.delay,
        seed=args.seed,
        local_api_base=args.local_api_base,
        local_api_key=args.local_api_key,
    )


if __name__ == "__main__":
    main()
