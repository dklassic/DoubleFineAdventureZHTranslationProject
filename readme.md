# DoubleFineAdventureZHTranslationProject

Traditional Chinese (Taiwan) subtitle translation project for the [*Double Fine Adventure!*](https://www.youtube.com/playlist?list=PLIhLvue17Sd7F6pU2ByRRb0igiI-WKk3D) documentary series.

This repository is currently a subtitle data and workflow repository. It contains source English SRT files, cleaned subtitle files, extracted CSVs, machine pretranslations, first-pass proofread CSVs, episode summaries, a glossary, proofreading guidance, conversion scripts, and GitHub Actions workflow definitions.

## Current Status

| Stage | Directory / File | Current state |
| --- | --- | --- |
| Raw English subtitles | `raw subtitles/` | 20 SRT files |
| Preprocessed subtitles | `preprocessed subtitles/` | 20 cleaned SRT files |
| Extracted English CSVs | `extracted csv/` | 20 CSV files, 10,979 data rows |
| Machine pretranslations | `pretranslated csv/` | 20 CSV files, 10,979 data rows |
| First-pass proofread CSVs | `proofread csv/` | 20 CSV files, 10,979 data rows |
| Episode summaries | `summary/` | 20 Markdown summaries |
| Glossary | `glossary.md` | Traditional Chinese terminology and naming decisions |
| Proofreading plan | `proofreading-plan.md` | Style guide, QA checklist, and manual proofreading workflow |
| Sanitized CSV output | `sanitized csv/` | Not present in the current checkout |
| Final translated SRT output | `translated subtitles/` | Not present in the current checkout |

The current proofread CSVs are first-pass automated outputs, not final human-reviewed subtitles. The next major project step is manual row-by-row proofreading of `proofread csv/*.csv` against the English `Content` column.

## Repository Layout

| Path | Purpose |
| --- | --- |
| `raw subtitles/` | Original English SRT files for episodes `01` through `20`. |
| `preprocessed subtitles/` | Cleaned English SRT files with merged lines/cues and renumbered subtitle blocks. |
| `extracted csv/` | CSV files extracted from cleaned SRTs, with `Timecode` and `Content` columns. |
| `pretranslated csv/` | Machine-generated Traditional Chinese translations, with `Content_zh` added. |
| `proofread csv/` | First-pass proofread versions of the machine translations. |
| `summary/` | Episode summaries in Traditional Chinese, one Markdown file per episode. |
| `glossary.md` | Living glossary for recurring names, game titles, terminology, speaker labels, and machine-translation mistakes to avoid. |
| `proofreading-plan.md` | Detailed proofreading priorities, style rules, QA checklist, and recommended manual workflow. |
| `scripts/` | Python scripts for preprocessing, CSV extraction, machine translation, sanitization, first-pass proofreading, and SRT generation. |
| `.github/workflows/` | GitHub Actions definitions for extraction, pretranslation, sanitization, and SRT conversion. |

## Workflow

```mermaid
graph TD;
    RawSubtitles[raw subtitles/*.srt] --> PreprocessedSubtitles[preprocessed subtitles/*_cleaned.srt];
    PreprocessedSubtitles --> ExtractedCSV[extracted csv/*_cleaned.csv];
    ExtractedCSV --> PretranslatedCSV[pretranslated csv/*_pretranslated.csv];
    PretranslatedCSV --> ProofreadCSV[proofread csv/*_pretranslated.csv];
    PretranslatedCSV --> SanitizedCSV[sanitized csv/*.csv];
    ProofreadCSV --> FinalSRT[translated subtitles/*.srt];
    SanitizedCSV --> FinalSRT;
```

The checked-in project state has reached the first-pass proofreading stage. `sanitized csv/` and `translated subtitles/` are generated-output locations supported by scripts, but they are not currently present.

## Prerequisites

- Python 3.9+
- `openai` for machine pretranslation
- `opencc` for Simplified-to-Traditional conversion in the sanitizer
- An OpenAI API key for machine pretranslation, provided through `OPENAI_API_KEY` or `--api_key`

The project does not currently include a dependency manifest. Install dependencies manually before running scripts that need them:

```bash
python -m pip install openai opencc
```

## Local Usage

Run commands from the repository root.

### 1. Preprocess Raw SRT Files

```bash
python scripts/srt_preprocess.py --path "./"
```

Reads `raw subtitles/` and writes cleaned SRT files to `preprocessed subtitles/`.

### 2. Extract CSV Files

```bash
python scripts/extract_csv.py --path "./"
```

Reads `preprocessed subtitles/` and writes CSV files to `extracted csv/`.

### 3. Machine Translate CSV Files

```bash
OPENAI_API_KEY="your-api-key" python scripts/translate_csv_batch.py --path "./"
```

Reads `extracted csv/` and writes translated CSV files to `pretranslated csv/`.

### 4. Generate First-Pass Proofread CSVs

```bash
python3 scripts/proofread_content_zh.py
```

Reads `pretranslated csv/` and writes first-pass proofread files to `proofread csv/`. This script applies glossary-oriented replacements, punctuation normalization, cue normalization, and common machine-translation fixes. It is a helper pass and does not replace human proofreading.

### 5. Optional Sanitization

```bash
python scripts/sanitize_content_zh.py --path "./"
```

Reads `pretranslated csv/` by default and writes sanitized CSV files to `sanitized csv/`. The sanitizer is intended to convert Simplified Chinese to Traditional Chinese and add spacing between half-width and full-width text where appropriate.

Review `proofreading-plan.md` before relying on this step for production output; the current plan flags the sanitizer as needing careful review/testing.

### 6. Convert CSV Files Back To SRT

```bash
python scripts/convert_csv_to_srt.py --path "./" --input "proofread csv"
```

Reads CSV files with a `Content_zh` column and writes SRT files to `translated subtitles/`. The script defaults to `pretranslated csv/`, so pass `--input "proofread csv"` when generating subtitles from the first-pass proofread files.

## CSV Format

Extracted CSV files contain:

| Column | Description |
| --- | --- |
| `Timecode` | Original SRT time range, such as `00:00:32,655 --> 00:00:35,274`. |
| `Content` | English subtitle text. |

Pretranslated and proofread CSV files contain:

| Column | Description |
| --- | --- |
| `Timecode` | SRT time range preserved from the source file. |
| `Content` | Original English subtitle text. |
| `Content_zh` | Traditional Chinese subtitle text used when generating final SRT files. |

During proofreading, edit only `Content_zh` unless you are intentionally correcting subtitle timing. Preserve `Timecode` and `Content` so output can be compared and converted safely.

## Proofreading Guidance

- Use Traditional Chinese suitable for a Taiwanese audience.
- Prefer natural spoken subtitle phrasing over literal English sentence structure.
- Follow `glossary.md` for names, game titles, technical terms, speaker labels, and recurring machine-translation fixes.
- Preserve speaker labels when they clarify who is speaking.
- Use full-width punctuation in Chinese text.
- Keep subtitle text concise enough to read comfortably on screen.
- Do not remove or rewrite `Timecode` values unless timing correction is required.

For the detailed style guide and QA checklist, see `proofreading-plan.md`.

## Episode Summaries

The `summary/` directory contains one Traditional Chinese Markdown summary per episode, `01.md` through `20.md`. These summaries are based on the English `Content` column and are useful for continuity, context, names, and scene-level meaning during manual proofreading.

## GitHub Actions

The repository includes workflow definitions for common pipeline steps:

| Workflow file | Purpose |
| --- | --- |
| `.github/workflows/extract_csv.yml` | Runs CSV extraction and opens a pull request with extracted CSV changes. |
| `.github/workflows/pretranslation.yml` | Runs machine pretranslation and opens a pull request with pretranslated CSV changes. |
| `.github/workflows/sanitization.yml` | Runs Chinese content sanitization and opens a pull request with sanitized CSV changes. |
| `.github/workflows/convert_to_srt.yml` | Converts CSV files back to SRT and opens a pull request with generated subtitle changes. |

The pretranslation workflow requires an `OPENAI_API_KEY` repository secret.

## Known Maintenance Items

- Add a dependency manifest, such as `requirements.txt`, with pinned package versions.
- Update `translate_csv_batch.py` for the current OpenAI Python SDK or pin an SDK version compatible with `openai.ChatCompletion.create`.
- Review and test `sanitize_content_zh.py` before relying on it for production output.
- Clean up copied labels/comments in `.github/workflows/extract_csv.yml`.
- Align `.github/workflows/convert_to_srt.yml` with its sanitized-CSV name/trigger; it currently runs `convert_csv_to_srt.py` without `--input`, so the script default is `pretranslated csv/`.
- Decide whether final SRT generation should use `proofread csv/` or a later manually reviewed output folder by default.
- Continue manual row-by-row proofreading of `proofread csv/*.csv` before treating the subtitles as final.
