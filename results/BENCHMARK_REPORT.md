# Finnish Parliament ASR Benchmark Report

**Date:** 2026-03-12
**Dataset:** Aalto Finnish Parliament ASR Corpus v2 (fi-parliament-asr)
**Azure Endpoint:** haagahelia-poc-gaik.openai.azure.com
**Local WhisperX:** AI Hub (myedge-unique-label.swedencentral.cloudapp.azure.com:8080)

## Summary

This benchmark compares three transcription backends on Finnish parliament speech data:
**Azure GPT-4o-transcribe**, **Azure Whisper**, and **Local WhisperX** (self-hosted on AI Hub).
Each was tested with two language settings: `language="fi"` (explicit Finnish) vs `language="auto"` (auto-detect).

### Key Findings

1. **GPT-4o-transcribe with `language=fi` has the best WER** at 11.51% (500 samples, ~1s/sample)
2. **Local WhisperX is a close second** at 11.79% WER — nearly matching GPT-4o at zero API cost
3. **Local WhisperX with `auto` has the best CER** at 5.07% — best character-level accuracy of all models
4. **Setting `language="fi"` matters significantly for GPT-4o** (-2.36% WER improvement)
5. **Setting `language="fi"` has small/negligible effect on Whisper models** (Azure: -0.03%, Local: -0.55% WER)
6. **Local WhisperX is 8x faster than Azure Whisper** (~2.3s vs ~20s) and free to run
7. **GPT-4o occasionally truncates output** (0.8-2.6% of files), worse with auto-detect

## Overall Leaderboard (Combined)

| Rank | Model | Language | WER% | CER% | Samples | Avg Latency | Word Ratio | Truncated |
| ---- | ----- | -------- | ---- | ---- | ------- | ----------- | ---------- | --------- |
| 1 | gpt-4o-transcribe | fi | **11.51** | 6.52 | 500 | **0.96s** | 0.95 | 4 |
| 2 | local whisperX | fi | 11.79 | 5.75 | 250 | 2.23s | 0.98 | 1 |
| 3 | local whisperX | auto | 12.34 | **5.07** | 250 | 2.38s | 0.98 | 0 |
| 4 | gpt-4o-transcribe | auto | 13.87 | 8.73 | 500 | 0.96s | 0.94 | 13 |
| 5 | azure whisper | fi | 15.50 | 6.93 | 150 | 19.63s | 0.96 | 2 |
| 6 | azure whisper | auto | 15.53 | 6.95 | 150 | 20.05s | 0.96 | 2 |

> **Note:** Sample sizes differ due to Azure rate limiting and run constraints.
> Azure Whisper: 3 splits × 50 samples. GPT-4o: 5 splits × 100 samples. Local WhisperX: 5 splits × 50 samples.
> WER/CER are not directly comparable across different sample sets, but trends are clear.

## Per-Split Results: GPT-4o-transcribe (100 samples per split)

| Split | fi WER% | fi CER% | auto WER% | auto CER% | fi-auto Delta WER |
| ----- | ------- | ------- | --------- | --------- | ----------------- |
| 2016-dev-seen | 14.38 | 8.63 | 18.92 | 13.18 | **-4.54** |
| 2016-dev-unseen | 14.48 | 8.05 | 15.78 | 9.43 | -1.30 |
| 2016-test-seen | 11.17 | 6.64 | 12.37 | 7.78 | -1.20 |
| 2016-test-unseen | 6.96 | 3.51 | 9.64 | 5.91 | **-2.68** |
| 2020-test | 9.12 | 4.84 | 10.51 | 5.46 | -1.39 |

## Per-Split Results: Azure Whisper (50 samples per split)

| Split | fi WER% | fi CER% | auto WER% | auto CER% | fi-auto Delta WER |
| ----- | ------- | ------- | --------- | --------- | ----------------- |
| 2016-dev-seen | 16.79 | 7.78 | 16.79 | 7.78 | 0.00 |
| 2016-dev-unseen | 17.07 | 7.41 | 17.18 | 7.49 | -0.11 |
| 2016-test-seen | 12.59 | 5.52 | 12.59 | 5.52 | 0.00 |

## Per-Split Results: Local WhisperX (50 samples per split)

| Split | fi WER% | fi CER% | auto WER% | auto CER% | fi-auto Delta WER |
| ----- | ------- | ------- | --------- | --------- | ----------------- |
| 2016-dev-seen | 13.23 | 6.40 | 13.23 | 5.52 | 0.00 |
| 2016-dev-unseen | 13.75 | 5.98 | 14.08 | 5.84 | -0.33 |
| 2016-test-seen | 11.67 | 6.25 | 12.69 | 5.00 | -1.02 |
| 2016-test-unseen | 8.87 | 5.02 | 9.48 | 4.19 | -0.61 |
| 2020-test | 11.11 | 4.49 | 12.20 | 4.60 | -1.09 |

## Language Setting Analysis

| Model | WER% (fi) | WER% (auto) | Delta | CER% (fi) | CER% (auto) | Delta | Impact |
| ----- | --------- | ----------- | ----- | --------- | ----------- | ----- | ------ |
| gpt-4o-transcribe | 11.51 | 13.87 | **-2.36** | 6.52 | 8.73 | **-2.21** | Significant improvement with fi |
| local whisperX | 11.79 | 12.34 | -0.55 | 5.75 | 5.07 | +0.68 | Small WER gain, but auto has better CER |
| azure whisper | 15.50 | 15.53 | -0.03 | 6.93 | 6.95 | -0.02 | No meaningful difference |

**Conclusion:** For GPT-4o-transcribe, always set `language="fi"` when transcribing Finnish.
For Whisper-based models (Azure and local), the language setting has little practical effect on WER.
Interestingly, local WhisperX with `auto` achieves the best CER of any model tested (5.07%).

## Speed Comparison

| Model | Avg Latency | Real-Time Factor (RTF) | Cost | Notes |
| ----- | ----------- | ---------------------- | ---- | ----- |
| gpt-4o-transcribe | **0.96s** | 0.13 | ~$0.01/sample | Fastest, pay-per-use |
| local whisperX | 2.23s | 0.28 | Free (self-hosted) | Good speed, zero marginal cost |
| azure whisper | 19.63s | 3.10 | ~$0.006/sample | Heavily rate-limited on Azure |

GPT-4o-transcribe is ~2x faster than local WhisperX and ~20x faster than Azure Whisper.
Local WhisperX is ~8x faster than Azure Whisper with zero API cost.
The Azure Whisper latency is dominated by rate limiting (429 throttling every ~3 requests).

## Truncation Analysis

| Config | Files with <50% word ratio | Out of |
| ------ | -------------------------- | ------ |
| gpt-4o fi | 4 | 500 |
| gpt-4o auto | 13 | 500 |
| local whisperX fi | 1 | 250 |
| local whisperX auto | 0 | 250 |
| azure whisper fi | 2 | 150 |
| azure whisper auto | 2 | 150 |

GPT-4o with auto-detect truncates 3x more often than with explicit `language="fi"`.
Local WhisperX has essentially no truncation issues.

## Common Error Patterns

1. **Very short utterances** ("arvoisa puhemies", "herra puhemies") often get 100% WER
   because models add/change words
2. **Colloquial Finnish** and rare political terms cause higher WER
3. **Compound words** (yhdyssanat) are sometimes split or merged differently
4. **Numbers and abbreviations** are transcribed inconsistently

## Recommendations

1. **Use `gpt-4o-transcribe` with `language="fi"`** for best WER accuracy + speed (if budget allows)
2. **Use local WhisperX** for best cost-effectiveness — nearly matches GPT-4o at zero API cost
3. **Use local WhisperX with `auto`** when character-level precision matters most (CER 5.07%)
4. **Always set `language="fi"`** for GPT-4o on Finnish content (saves 2.36% WER)
5. **For mixed Finnish/English content**, consider `auto` to preserve English words
6. **Post-processing** could improve results: normalize compound words, fix common substitutions

## Dataset Information

- **Source:** Aalto Finnish Parliament ASR Corpus 2008-2020, v2
- **Audio:** 16kHz mono WAV, 16-bit
- **Transcriptions:** Hand-corrected .trn files (ground truth)
- **Splits tested:** 2016-dev (seen/unseen), 2016-test (seen/unseen), 2020-test
- **Total available:** 6,307 audio files across all splits

## Methodology

- Text normalization: Unicode NFC, lowercase, remove punctuation (keep a-z äöå 0-9), collapse whitespace
- Metrics: WER (word error rate) and CER (character error rate) via jiwer library
- Same normalization applied to both reference and hypothesis
- No LLM judge used - all scoring is deterministic
- `enhanced_transcript=False` and `diarization=False` for fair comparison

## Run Details

| Run | Models | Splits | Samples/Split | Total Samples |
| --- | ------ | ------ | ------------- | ------------- |
| GPT-4o run | gpt-4o-transcribe fi/auto | all 5 | 100 | 1,000 |
| Whisper run | azure whisper fi/auto | 3 of 5 | 50 | 300 |
| Local WhisperX run | local whisperX fi/auto | all 5 | 50 | 500 |
| **Total** | **6 configs** | **5 splits** | | **1,800** |
