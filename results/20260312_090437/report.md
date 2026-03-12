# Finnish Parliament ASR Benchmark Report

**Run ID:** 20260312_090437
**Timestamp:** 2026-03-12T10:45:21.569296
**Dataset:** C:\Users\h03068\dev-test\benchmark\fi-parliament-asr
**Splits:** 2016-dev-seen, 2016-dev-unseen, 2016-test-seen
**Limit per split:** 50
**Total samples:** 300
**Total errors:** 0

## Dataset Splits

- **2016-dev-seen**: 843 audio files
- **2016-dev-unseen**: 954 audio files
- **2016-test-seen**: 966 audio files

## Configuration Matrix

| Config | Backend | Language |
| ------ | ------- | -------- |
| azure_whisper_fi | azure_whisper | fi |
| azure_whisper_auto | azure_whisper | auto |

## Overall Leaderboard

| Rank | Config | WER% | CER% | Samples | Errors | Avg Latency | Avg RTF | Word Ratio | Truncated |
| ---- | ------ | ---- | ---- | ------- | ------ | ----------- | ------- | ---------- | --------- |
| 1 | azure_whisper_fi | 15.50 | 6.93 | 150 | 0 | 19.63s | 3.097 | 0.96 | 2 |
| 2 | azure_whisper_auto | 15.53 | 6.95 | 150 | 0 | 20.05s | 2.717 | 0.96 | 2 |

## Per-Split Leaderboard

### 2016-dev-seen

| Config | WER% | CER% | Samples | Errors | Avg Latency |
| ------ | ---- | ---- | ------- | ------ | ----------- |
| azure_whisper_fi | 16.79 | 7.78 | 50 | 0 | 19.23s |
| azure_whisper_auto | 16.79 | 7.78 | 50 | 0 | 20.37s |
### 2016-dev-unseen

| Config | WER% | CER% | Samples | Errors | Avg Latency |
| ------ | ---- | ---- | ------- | ------ | ----------- |
| azure_whisper_fi | 17.07 | 7.41 | 50 | 0 | 19.24s |
| azure_whisper_auto | 17.18 | 7.49 | 50 | 0 | 20.44s |
### 2016-test-seen

| Config | WER% | CER% | Samples | Errors | Avg Latency |
| ------ | ---- | ---- | ------- | ------ | ----------- |
| azure_whisper_fi | 12.59 | 5.52 | 50 | 0 | 20.41s |
| azure_whisper_auto | 12.59 | 5.52 | 50 | 0 | 19.34s |

## Language Setting Comparison: fi vs auto

| Backend | WER% (fi) | WER% (auto) | Delta | CER% (fi) | CER% (auto) | Delta |
| ------- | --------- | ----------- | ----- | --------- | ----------- | ----- |
| azure_whisper | 15.50 | 15.53 | -0.03 | 6.93 | 6.95 | -0.02 |

## Top 5 Worst Files by WER

| Config | Split | File | WER | Reference (first 80 chars) |
| ------ | ----- | ---- | --- | -------------------------- |
| azure_whisper_fi | 2016-dev-unseen | matti_semi_00496 | 100.0% | edustaja semi rouva puhemies minulla ei ole |
| azure_whisper_auto | 2016-dev-unseen | matti_semi_00496 | 100.0% | edustaja semi rouva puhemies minulla ei ole |
| azure_whisper_fi | 2016-test-seen | matti_saarinen_06551 | 100.0% | herra puhemies |
| azure_whisper_auto | 2016-test-seen | matti_saarinen_06551 | 100.0% | herra puhemies |
| azure_whisper_auto | 2016-dev-unseen | antti_kalliomaki_00271 | 80.0% | se koskee myöskin eduskunnan edustajaa |

## Top 5 Best Files by WER

| Config | Split | File | WER | Reference (first 80 chars) |
| ------ | ----- | ---- | --- | -------------------------- |
| azure_whisper_fi | 2016-dev-seen | anne_mari_virolainen_04370 | 0.0% | liikennepoliittisen selonteon käsittelyn yhteydessä eduskunta hyväksyy kannanoto... |
| azure_whisper_fi | 2016-dev-seen | anne_mari_virolainen_04368 | 0.0% | koska jo vuosien ajan korjausvelkaa on kerätty runsaasti on aivan ilmeistä että ... |
| azure_whisper_fi | 2016-dev-seen | hanna_tainio_01934 | 0.0% | yhteiskunnalle syntyvä säästö olisi siis merkittävä |
| azure_whisper_fi | 2016-dev-seen | hanna_tainio_02078 | 0.0% | kehyksessä on edellä mainittujen lisäksi useita keinoja työllisyyden lisäämiseks... |
| azure_whisper_fi | 2016-dev-seen | hanna_tainio_02199 | 0.0% | arvoisa puhemies |
