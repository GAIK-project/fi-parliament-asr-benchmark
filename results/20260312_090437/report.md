# Finnish Parliament ASR Benchmark Report

**Run ID:** 20260312_090437
**Timestamp:** 2026-03-12T09:23:27.690624
**Dataset:** fi-parliament-asr
**Splits:** 2016-dev-seen, 2016-dev-unseen, 2016-test-seen, 2016-test-unseen, 2020-test
**Limit per split:** 100
**Total samples:** 1000
**Total errors:** 0

## Dataset Splits

- **2016-dev-seen**: 843 audio files
- **2016-dev-unseen**: 954 audio files
- **2016-test-seen**: 966 audio files
- **2016-test-unseen**: 962 audio files
- **2020-test**: 2582 audio files

## Configuration Matrix

| Config | Backend | Language |
| ------ | ------- | -------- |
| azure_gpt4o_transcribe_fi | azure_gpt4o | fi |
| azure_gpt4o_transcribe_auto | azure_gpt4o | auto |

## Overall Leaderboard

| Rank | Config | WER% | CER% | Samples | Errors | Avg Latency | Avg RTF | Word Ratio | Truncated |
| ---- | ------ | ---- | ---- | ------- | ------ | ----------- | ------- | ---------- | --------- |
| 1 | azure_gpt4o_transcribe_fi | 11.47 | 6.51 | 500 | 0 | 0.93s | 0.121 | 0.95 | 7 |
| 2 | azure_gpt4o_transcribe_auto | 13.29 | 8.21 | 500 | 0 | 0.92s | 0.121 | 0.94 | 14 |

## Per-Split Leaderboard

### 2016-dev-seen

| Config | WER% | CER% | Samples | Errors | Avg Latency |
| ------ | ---- | ---- | ------- | ------ | ----------- |
| azure_gpt4o_transcribe_fi | 14.05 | 8.54 | 100 | 0 | 0.98s |
| azure_gpt4o_transcribe_auto | 16.29 | 10.85 | 100 | 0 | 1.00s |
### 2016-dev-unseen

| Config | WER% | CER% | Samples | Errors | Avg Latency |
| ------ | ---- | ---- | ------- | ------ | ----------- |
| azure_gpt4o_transcribe_fi | 14.53 | 8.24 | 100 | 0 | 0.98s |
| azure_gpt4o_transcribe_auto | 15.88 | 9.66 | 100 | 0 | 0.94s |
### 2016-test-seen

| Config | WER% | CER% | Samples | Errors | Avg Latency |
| ------ | ---- | ---- | ------- | ------ | ----------- |
| azure_gpt4o_transcribe_fi | 10.02 | 5.55 | 100 | 0 | 0.95s |
| azure_gpt4o_transcribe_auto | 10.67 | 6.37 | 100 | 0 | 0.87s |
### 2016-test-unseen

| Config | WER% | CER% | Samples | Errors | Avg Latency |
| ------ | ---- | ---- | ------- | ------ | ----------- |
| azure_gpt4o_transcribe_fi | 7.98 | 4.23 | 100 | 0 | 0.91s |
| azure_gpt4o_transcribe_auto | 11.25 | 7.19 | 100 | 0 | 1.00s |
### 2020-test

| Config | WER% | CER% | Samples | Errors | Avg Latency |
| ------ | ---- | ---- | ------- | ------ | ----------- |
| azure_gpt4o_transcribe_fi | 9.49 | 5.15 | 100 | 0 | 0.81s |
| azure_gpt4o_transcribe_auto | 10.78 | 5.48 | 100 | 0 | 0.80s |

## Language Setting Comparison: fi vs auto

| Backend | WER% (fi) | WER% (auto) | Delta | CER% (fi) | CER% (auto) | Delta |
| ------- | --------- | ----------- | ----- | --------- | ----------- | ----- |
| azure_gpt4o | 11.47 | 13.29 | -1.82 | 6.51 | 8.21 | -1.70 |

## Top 5 Worst Files by WER

| Config | Split | File | WER | Reference (first 80 chars) |
| ------ | ----- | ---- | --- | -------------------------- |
| azure_gpt4o_transcribe_fi | 2016-dev-unseen | laila_koskela_01077 | 100.0% | arvoisa puhemies |
| azure_gpt4o_transcribe_auto | 2016-dev-unseen | mikko_karna_00738 | 100.0% | arvoisa rouva puhemies |
| azure_gpt4o_transcribe_auto | 2016-dev-unseen | laila_koskela_01077 | 100.0% | arvoisa puhemies |
| azure_gpt4o_transcribe_fi | 2016-test-seen | matti_saarinen_06551 | 100.0% | herra puhemies |
| azure_gpt4o_transcribe_fi | 2016-test-unseen | pekka_vilkuna_00506 | 100.0% | minusta se oli akkamaista touhua |

## Top 5 Best Files by WER

| Config | Split | File | WER | Reference (first 80 chars) |
| ------ | ----- | ---- | --- | -------------------------- |
| azure_gpt4o_transcribe_fi | 2016-dev-seen | eero_suutari_02968 | 0.0% | arvoisa puhemies |
| azure_gpt4o_transcribe_fi | 2016-dev-seen | carl_haglund_02703 | 0.0% | valitettavasti valtiontalouden tilasta johtuen eivät puolustusvoimauudistuksen h... |
| azure_gpt4o_transcribe_fi | 2016-dev-seen | jouni_backman_01836 | 0.0% | se millä tavalla se muistuttaa taas sitä keskustan ajattelutapaa on tämä miljard... |
| azure_gpt4o_transcribe_fi | 2016-dev-seen | anne_mari_virolainen_04370 | 0.0% | liikennepoliittisen selonteon käsittelyn yhteydessä eduskunta hyväksyy kannanoto... |
| azure_gpt4o_transcribe_fi | 2016-dev-seen | anne_mari_virolainen_04368 | 0.0% | koska jo vuosien ajan korjausvelkaa on kerätty runsaasti on aivan ilmeistä että ... |
