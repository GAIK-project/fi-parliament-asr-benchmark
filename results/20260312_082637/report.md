# Finnish Parliament ASR Benchmark Report

**Run ID:** 20260312_082637
**Timestamp:** 2026-03-12T08:48:18.344636
**Dataset:** fi-parliament-asr
**Splits:** 2016-dev-seen
**Limit per split:** 30
**Total samples:** 120
**Total errors:** 0

## Dataset Splits

- **2016-dev-seen**: 843 audio files

## Configuration Matrix

| Config | Backend | Language |
| ------ | ------- | -------- |
| azure_whisper_fi | azure_whisper | fi |
| azure_whisper_auto | azure_whisper | auto |
| azure_gpt4o_transcribe_fi | azure_gpt4o | fi |
| azure_gpt4o_transcribe_auto | azure_gpt4o | auto |

## Overall Leaderboard

| Rank | Config | WER% | CER% | Samples | Errors | Avg Latency | Avg RTF |
| ---- | ------ | ---- | ---- | ------- | ------ | ----------- | ------- |
| 1 | azure_whisper_fi | 17.68 | 8.55 | 30 | 0 | 20.09s | 2.434 |
| 2 | azure_whisper_auto | 17.68 | 8.55 | 30 | 0 | 19.99s | 3.620 |
| 3 | azure_gpt4o_transcribe_fi | 18.55 | 11.74 | 30 | 0 | 1.06s | 0.133 |
| 4 | azure_gpt4o_transcribe_auto | 25.36 | 19.68 | 30 | 0 | 0.94s | 0.103 |

## Per-Split Leaderboard

### 2016-dev-seen

| Config | WER% | CER% | Samples | Errors | Avg Latency |
| ------ | ---- | ---- | ------- | ------ | ----------- |
| azure_whisper_fi | 17.68 | 8.55 | 30 | 0 | 20.09s |
| azure_whisper_auto | 17.68 | 8.55 | 30 | 0 | 19.99s |
| azure_gpt4o_transcribe_fi | 18.55 | 11.74 | 30 | 0 | 1.06s |
| azure_gpt4o_transcribe_auto | 25.36 | 19.68 | 30 | 0 | 0.94s |

## Language Setting Comparison: fi vs auto

| Backend | WER% (fi) | WER% (auto) | Delta | CER% (fi) | CER% (auto) | Delta |
| ------- | --------- | ----------- | ----- | --------- | ----------- | ----- |
| azure_whisper | 17.68 | 17.68 | 0.00 | 8.55 | 8.55 | 0.00 |
| azure_gpt4o | 18.55 | 25.36 | -6.81 | 11.74 | 19.68 | -7.94 |

## Top 5 Worst Files by WER

| Config | Split | File | WER | Reference (first 80 chars) |
| ------ | ----- | ---- | --- | -------------------------- |
| azure_gpt4o_transcribe_auto | 2016-dev-seen | jari_koskinen_03001 | 83.8% | ja kyl se meidän toivomus on kaikkien se että markkinat toimisi paremmin ja kysy... |
| azure_gpt4o_transcribe_auto | 2016-dev-seen | jyri_hakamies_02695 | 80.0% | sen yhtiön enemmistö on on on eduskuntavaltuuden takana ja yrityksellä on hyvin ... |
| azure_gpt4o_transcribe_fi | 2016-dev-seen | jyri_hakamies_02700 | 74.2% | meillä on esimerkiksi kaakkois suomessa tämmöinen liikuntaneuvoja mukana näissä ... |
| azure_gpt4o_transcribe_auto | 2016-dev-seen | jyri_hakamies_02700 | 74.2% | meillä on esimerkiksi kaakkois suomessa tämmöinen liikuntaneuvoja mukana näissä ... |
| azure_gpt4o_transcribe_auto | 2016-dev-seen | carl_haglund_02604 | 74.2% | mitä tulee tähän maanpuolustustahtoon näille alueille joista lakkaa varuskunnat ... |

## Top 5 Best Files by WER

| Config | Split | File | WER | Reference (first 80 chars) |
| ------ | ----- | ---- | --- | -------------------------- |
| azure_whisper_fi | 2016-dev-seen | anne_mari_virolainen_04370 | 0.0% | liikennepoliittisen selonteon käsittelyn yhteydessä eduskunta hyväksyy kannanoto... |
| azure_whisper_fi | 2016-dev-seen | anne_mari_virolainen_04368 | 0.0% | koska jo vuosien ajan korjausvelkaa on kerätty runsaasti on aivan ilmeistä että ... |
| azure_whisper_auto | 2016-dev-seen | anne_mari_virolainen_04370 | 0.0% | liikennepoliittisen selonteon käsittelyn yhteydessä eduskunta hyväksyy kannanoto... |
| azure_whisper_auto | 2016-dev-seen | anne_mari_virolainen_04368 | 0.0% | koska jo vuosien ajan korjausvelkaa on kerätty runsaasti on aivan ilmeistä että ... |
| azure_gpt4o_transcribe_fi | 2016-dev-seen | eero_suutari_02968 | 0.0% | arvoisa puhemies |
