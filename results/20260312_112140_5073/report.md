# Finnish Parliament ASR Benchmark Report

**Run ID:** 20260312_112140_5073
**Timestamp:** 2026-03-12T11:42:41.555029
**Dataset:** C:\Users\h03068\dev-test\benchmark\fi-parliament-asr
**Splits:** 2016-dev-seen, 2016-dev-unseen, 2016-test-seen, 2016-test-unseen, 2020-test
**Limit per split:** 50
**Total samples:** 500
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
| local_whisper_fi | local_whisper | fi |
| local_whisper_auto | local_whisper | auto |

## Overall Leaderboard

| Rank | Config | WER% | CER% | Samples | Errors | Avg Latency | Avg RTF | Word Ratio | Truncated |
| ---- | ------ | ---- | ---- | ------- | ------ | ----------- | ------- | ---------- | --------- |
| 1 | local_whisper_fi | 11.79 | 5.75 | 250 | 0 | 2.23s | 0.280 | 0.98 | 1 |
| 2 | local_whisper_auto | 12.34 | 5.07 | 250 | 0 | 2.38s | 0.363 | 0.98 | 0 |

## Per-Split Leaderboard

### 2016-dev-seen

| Config | WER% | CER% | Samples | Errors | Avg Latency |
| ------ | ---- | ---- | ------- | ------ | ----------- |
| local_whisper_fi | 13.23 | 6.40 | 50 | 0 | 2.49s |
| local_whisper_auto | 13.23 | 5.52 | 50 | 0 | 2.54s |
### 2016-dev-unseen

| Config | WER% | CER% | Samples | Errors | Avg Latency |
| ------ | ---- | ---- | ------- | ------ | ----------- |
| local_whisper_fi | 13.75 | 5.98 | 50 | 0 | 2.29s |
| local_whisper_auto | 14.08 | 5.84 | 50 | 0 | 2.52s |
### 2016-test-seen

| Config | WER% | CER% | Samples | Errors | Avg Latency |
| ------ | ---- | ---- | ------- | ------ | ----------- |
| local_whisper_fi | 11.67 | 6.25 | 50 | 0 | 2.41s |
| local_whisper_auto | 12.69 | 5.00 | 50 | 0 | 2.83s |
### 2016-test-unseen

| Config | WER% | CER% | Samples | Errors | Avg Latency |
| ------ | ---- | ---- | ------- | ------ | ----------- |
| local_whisper_fi | 8.87 | 5.02 | 50 | 0 | 2.38s |
| local_whisper_auto | 9.48 | 4.19 | 50 | 0 | 2.36s |
### 2020-test

| Config | WER% | CER% | Samples | Errors | Avg Latency |
| ------ | ---- | ---- | ------- | ------ | ----------- |
| local_whisper_fi | 11.11 | 4.49 | 50 | 0 | 1.60s |
| local_whisper_auto | 12.20 | 4.60 | 50 | 0 | 1.66s |

## Language Setting Comparison: fi vs auto

| Backend | WER% (fi) | WER% (auto) | Delta | CER% (fi) | CER% (auto) | Delta |
| ------- | --------- | ----------- | ----- | --------- | ----------- | ----- |
| local_whisper | 11.79 | 12.34 | -0.55 | 5.75 | 5.07 | +0.68 |

## Top 5 Worst Files by WER

| Config | Split | File | WER | Reference (first 80 chars) |
| ------ | ----- | ---- | --- | -------------------------- |
| local_whisper_auto | 2016-test-seen | lyly_rajala_02467 | 300.0% | arvoisa puhemies |
| local_whisper_auto | 2016-test-seen | matti_saarinen_06551 | 150.0% | herra puhemies |
| local_whisper_auto | 2016-dev-unseen | matti_semi_00496 | 100.0% | edustaja semi rouva puhemies minulla ei ole |
| local_whisper_auto | 2016-dev-unseen | antti_kalliomaki_00271 | 80.0% | se koskee myöskin eduskunnan edustajaa |
| local_whisper_fi | 2016-dev-unseen | matti_semi_00496 | 71.4% | edustaja semi rouva puhemies minulla ei ole |

## Top 5 Best Files by WER

| Config | Split | File | WER | Reference (first 80 chars) |
| ------ | ----- | ---- | --- | -------------------------- |
| local_whisper_fi | 2016-dev-seen | eero_suutari_02968 | 0.0% | arvoisa puhemies |
| local_whisper_fi | 2016-dev-seen | carl_haglund_02703 | 0.0% | valitettavasti valtiontalouden tilasta johtuen eivät puolustusvoimauudistuksen h... |
| local_whisper_fi | 2016-dev-seen | carl_haglund_02557 | 0.0% | taustalla on etenkin se että on haluttu päivittää tätä nykyistä puitelakia jossa... |
| local_whisper_fi | 2016-dev-seen | jouni_backman_01836 | 0.0% | se millä tavalla se muistuttaa taas sitä keskustan ajattelutapaa on tämä miljard... |
| local_whisper_fi | 2016-dev-seen | anne_mari_virolainen_04370 | 0.0% | liikennepoliittisen selonteon käsittelyn yhteydessä eduskunta hyväksyy kannanoto... |
