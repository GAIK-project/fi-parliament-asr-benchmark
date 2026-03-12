# Finnish Parliament ASR Benchmark Report

**Run ID:** 20260312_104918_9065
**Timestamp:** 2026-03-12T11:09:00.215839
**Dataset:** C:\Users\h03068\dev-test\benchmark\fi-parliament-asr
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
| 1 | azure_gpt4o_transcribe_fi | 11.51 | 6.52 | 500 | 0 | 0.96s | 0.127 | 0.95 | 4 |
| 2 | azure_gpt4o_transcribe_auto | 13.87 | 8.73 | 500 | 0 | 0.96s | 0.132 | 0.94 | 13 |

## Per-Split Leaderboard

### 2016-dev-seen

| Config | WER% | CER% | Samples | Errors | Avg Latency |
| ------ | ---- | ---- | ------- | ------ | ----------- |
| azure_gpt4o_transcribe_fi | 14.38 | 8.63 | 100 | 0 | 1.17s |
| azure_gpt4o_transcribe_auto | 18.92 | 13.18 | 100 | 0 | 0.99s |
### 2016-dev-unseen

| Config | WER% | CER% | Samples | Errors | Avg Latency |
| ------ | ---- | ---- | ------- | ------ | ----------- |
| azure_gpt4o_transcribe_fi | 14.48 | 8.05 | 100 | 0 | 0.90s |
| azure_gpt4o_transcribe_auto | 15.78 | 9.43 | 100 | 0 | 0.87s |
### 2016-test-seen

| Config | WER% | CER% | Samples | Errors | Avg Latency |
| ------ | ---- | ---- | ------- | ------ | ----------- |
| azure_gpt4o_transcribe_fi | 11.17 | 6.64 | 100 | 0 | 0.92s |
| azure_gpt4o_transcribe_auto | 12.37 | 7.78 | 100 | 0 | 0.93s |
### 2016-test-unseen

| Config | WER% | CER% | Samples | Errors | Avg Latency |
| ------ | ---- | ---- | ------- | ------ | ----------- |
| azure_gpt4o_transcribe_fi | 6.96 | 3.51 | 100 | 0 | 0.98s |
| azure_gpt4o_transcribe_auto | 9.64 | 5.91 | 100 | 0 | 0.95s |
### 2020-test

| Config | WER% | CER% | Samples | Errors | Avg Latency |
| ------ | ---- | ---- | ------- | ------ | ----------- |
| azure_gpt4o_transcribe_fi | 9.12 | 4.84 | 100 | 0 | 0.83s |
| azure_gpt4o_transcribe_auto | 10.51 | 5.46 | 100 | 0 | 1.09s |

## Language Setting Comparison: fi vs auto

| Backend | WER% (fi) | WER% (auto) | Delta | CER% (fi) | CER% (auto) | Delta |
| ------- | --------- | ----------- | ----- | --------- | ----------- | ----- |
| azure_gpt4o | 11.51 | 13.87 | -2.36 | 6.52 | 8.73 | -2.21 |

## Top 5 Worst Files by WER

| Config | Split | File | WER | Reference (first 80 chars) |
| ------ | ----- | ---- | --- | -------------------------- |
| azure_gpt4o_transcribe_fi | 2016-test-seen | matti_saarinen_06551 | 100.0% | herra puhemies |
| azure_gpt4o_transcribe_fi | 2016-test-unseen | pekka_vilkuna_00506 | 100.0% | minusta se oli akkamaista touhua |
| azure_gpt4o_transcribe_auto | 2016-dev-seen | jari_koskinen_03001 | 86.5% | ja kyl se meidän toivomus on kaikkien se että markkinat toimisi paremmin ja kysy... |
| azure_gpt4o_transcribe_auto | 2016-dev-unseen | matti_semi_00496 | 85.7% | edustaja semi rouva puhemies minulla ei ole |
| azure_gpt4o_transcribe_auto | 2016-test-seen | martti_korhonen_05447 | 85.1% | elikkä joka kansallispuiston kohdalla se on uniikki ja se metsästykseen pitää su... |

## Top 5 Best Files by WER

| Config | Split | File | WER | Reference (first 80 chars) |
| ------ | ----- | ---- | --- | -------------------------- |
| azure_gpt4o_transcribe_fi | 2016-dev-seen | eero_suutari_02968 | 0.0% | arvoisa puhemies |
| azure_gpt4o_transcribe_fi | 2016-dev-seen | carl_haglund_02703 | 0.0% | valitettavasti valtiontalouden tilasta johtuen eivät puolustusvoimauudistuksen h... |
| azure_gpt4o_transcribe_fi | 2016-dev-seen | anne_mari_virolainen_04368 | 0.0% | koska jo vuosien ajan korjausvelkaa on kerätty runsaasti on aivan ilmeistä että ... |
| azure_gpt4o_transcribe_fi | 2016-dev-seen | jouni_backman_01973 | 0.0% | se on ongelma niin yksittäisten kansalaisten koko yhteiskunnan tasolla ja siihen... |
| azure_gpt4o_transcribe_fi | 2016-dev-seen | leena_rauhala_04208 | 0.0% | toivon että nyt tulevassa äänestyksessä siihen saadaan kannatusta koska tämä on ... |
