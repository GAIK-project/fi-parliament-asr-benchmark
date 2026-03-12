# Finnish Parliament ASR Benchmark

Benchmarking tool for evaluating speech recognition systems on the [Finnish Parliament ASR Corpus](http://urn.fi/urn:nbn:fi:lb-2022052002) (dev and test sets).

## Backends

- **Azure Whisper** — Azure OpenAI Whisper API
- **Azure GPT-4o Transcribe** — Azure OpenAI gpt-4o-transcribe API
- **Local WhisperX** — Self-hosted WhisperX endpoint

## Metrics

WER, CER, latency, and RTF (real-time factor) per file and aggregated per split.

## Dataset

This repo uses the dev/test subset of the Aalto Finnish Parliament ASR Corpus v2:

| Split | Description |
|-------|-------------|
| 2016-dev-seen | Dev set, speakers seen in training |
| 2016-dev-unseen | Dev set, unseen speakers |
| 2016-test-seen | Test set, speakers seen in training |
| 2016-test-unseen | Test set, unseen speakers |
| 2020-test | Test set from 2020 sessions |

Audio files (`.wav`) and reference transcripts (`.trn`) are in `fi-parliament-asr/`.

## Setup

```bash
pip install requests python-dotenv jiwer openai soundfile tqdm
```

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

## Usage

```bash
# Quick smoke test (5 samples)
python benchmark.py --smoke

# Run on default split with 50 samples
python benchmark.py

# Run on all splits
python benchmark.py --all-splits --limit 100

# Specific backends only
python benchmark.py --backends azure_whisper local_whisper

# All samples, no limit
python benchmark.py --all-splits --limit 0
```

Results are saved to `results/<timestamp>/` with per-file CSV, leaderboard CSV, and a markdown report.

## Dataset Citation

```bibtex
@conference{mansikkaniemi2017,
  title={Automatic Construction of the Finnish Parliament Speech Corpus},
  author={Mansikkaniemi, Andre and Smit, Peter and Kurimo, Mikko},
  year={2017},
  series={Interspeech 2017},
  pages={3762-3766},
  doi={10.21437/Interspeech.2017-1115}
}
```

## License

See [LICENSE.md](LICENSE.md) for the corpus license (CLARIN PUB +BY).
