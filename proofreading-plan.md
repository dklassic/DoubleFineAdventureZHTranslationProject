# Traditional Chinese Proofreading Plan

This plan covers proofreading the existing machine-pretranslated CSV subtitles in `pretranslated csv/` for the *Double Fine Adventure!* documentary project. The repository content is centered on the making of *Broken Age* at Double Fine, with references to other Double Fine and LucasArts games.

## Goals

- Produce natural Traditional Chinese subtitles suitable for a Taiwanese audience.
- Preserve the meaning, tone, jokes, and game-development context of the English source.
- Make the wording sound like normal people talking, not like machine translation, written prose, or corporate copy.
- Use Taiwan Traditional Chinese terminology only; do not use Simplified Chinese terminology, Mainland phrasing, or PRC-localized game/business terms.
- Use full-width punctuation appropriate for Traditional Chinese.
- Keep subtitle lines concise and readable on screen.
- Preserve CSV structure so the files can be converted back to SRT without data loss.

## Source Files

- Proofreading input: `pretranslated csv/*.csv`
- English reference: each row's `Content` column, plus matching files in `extracted csv/` if needed.
- Translation target: `Content_zh`
- Do not edit `Timecode` unless intentionally correcting subtitle timing.

The current set contains 20 CSV files and about 10,979 subtitle rows. Translation quality varies substantially. Later files such as `19_pretranslated.csv` and `20_pretranslated.csv` contain many half-width punctuation marks, inconsistent title translations, and literal machine-translation errors.

Episode summaries have been written to `summary/01.md` through `summary/20.md` based on the English `Content` column.

## Latest Pretranslation Sweep

A repository sweep of `pretranslated csv/*.csv` found:

- 20 files, 10,979 subtitle rows, and no empty `Content_zh` cells.
- Major recurring titles and names are already mostly stable: `Broken Age`, `Double Fine`, `Kickstarter`, `Psychonauts`, `Day of the Tentacle`, `Monkey Island`, `Grim Fandango`, `Act One`, and `Act Two` all matched the current glossary decisions in the checked rows.
- Obvious Mainland terms from the existing avoid list were not broadly present in the current files. The remaining risk is less terminology replacement and more context-sensitive meaning, tone, and subtitle flow.
- Half-width punctuation appears only in small numbers in the current sweep, but still needs per-file QA because punctuation can appear inside English names, acronyms, URLs, or speaker/cue labels where context matters.
- Speaker labels and cue-prefixed labels are broader than the current glossary originally covered, including variants such as `[Music] Schafer`, `Offscreen Voice`, `Phone voice`, `Nordic Rep`, `Web Streamer`, and many one-off interview or crowd labels.
- Recurring *Broken Age* place and character terms such as `Cloud Colony`, `Shellmound`, `Meriloft`, `Space Weaver`, `Mog Chothra`, `Vella`, `Shay`, and `Marek` should be checked carefully for consistency.

## Recommended Output Workflow

Overwriting `pretranslated csv/` directly.

Suggested pipeline:

1. Proofread only `Content_zh` during the main editing pass.
2. Run consistency and validation checks after each completed file.
3. Convert from `pretranslated csv/` to final SRT output when all files pass QA.

## Proofreading Order

Recommended order is chronological from `01` to `20` since continuity is more important than triage.

The latest sweep suggests the current `pretranslated csv/` files have already received some broad cleanup, so the next pass should be a manual contextual proofreading pass rather than a mechanical triage pass. Work from `01_pretranslated.csv` through `20_pretranslated.csv`, using the episode summaries to keep callbacks, character names, production milestones, and release-timeline references consistent.

If time is limited, prioritize the largest and densest files first after any in-progress episode:

1. `19_pretranslated.csv`
2. `20_pretranslated.csv`
3. `13_pretranslated.csv`
4. `15_pretranslated.csv`
5. `12_pretranslated.csv`
6. `09_pretranslated.csv`
7. `11_pretranslated.csv`
8. `10_pretranslated.csv`
9. `04_pretranslated.csv`
10. `08_pretranslated.csv`

## Core Style Priorities

These priorities are more important than preserving the shape of the English sentence:

1. Accurate meaning.
2. Natural spoken Traditional Chinese.
3. Taiwan terminology and usage.
4. Readable subtitle length.
5. Consistent glossary and punctuation.

If a literal translation sounds stiff, unnatural, or like a machine translated it, rewrite it into something a real person in Taiwan would actually say while keeping the original meaning.

Always proofread each subtitle line in context. Do not judge or rewrite a row in isolation; check the surrounding rows, speaker, scene, topic, and episode summary when needed so pronouns, jokes, callbacks, technical terms, emotional tone, and implied subjects remain accurate.

## Conversational Wording

- Treat the subtitles as spoken dialogue, not written essays.
- Prefer short, direct, natural phrasing.
- Preserve each speaker's tone: casual, joking, tired, nervous, sarcastic, frustrated, or excited.
- Reorder English sentences when needed so the Chinese sounds natural.
- Remove unnecessary filler if it does not affect tone or timing.
- Keep meaningful hesitation, false starts, and awkward pauses when they reveal character or mood.
- Avoid stiff written connectors such as `然而`, `因此`, `此外`, `進行`, `透過` when normal speech would use simpler wording like `可是`, `所以`, `而且`, `做`, `用`.
- Avoid machine-like literal phrasing such as `這是一個...的情況`, `它是關於...`, `我們將會進行...`, or `這對我們而言是...` unless the speaker is intentionally formal.
- Do not over-polish casual speech. The documentary includes office conversations, jokes, meetings, and offhand remarks; subtitles should feel human and conversational.

Spacing examples:

| Literal / Stiff | Prefer |
| --- | --- |
| `這是一個非常困難的情況。` | `這真的很難。` |
| `我們需要進行錯誤修復。` | `我們得修 bug。` |
| `這使我感到悲傷。` | `這讓我有點難過。` |
| `我無法記得那件事情。` | `我不記得了。` |
| `我們將會發布這個遊戲。` | `我們要推出這款遊戲。` |

## Taiwan Traditional Terminology

- Use Traditional Chinese characters and Taiwan terminology throughout.
- Do not use Simplified Chinese terminology, Mainland phrasing, or PRC-localized industry terms.
- Do not keep machine translations just because the characters are Traditional if the wording is Mainland usage.
- Prefer Taiwan usage for game, software, business, and internet terms.
- Check `glossary.md` first when choosing terms.

Examples of terminology to avoid:

| Avoid | Prefer |
| --- | --- |
| `視頻` | `影片` |
| `屏幕` | `螢幕` |
| `項目` | `專案` |
| `程序` | `程式` |
| `軟件` | `軟體` |
| `硬件` | `硬體` |
| `網絡` | `網路` |
| `質量` | `品質` |
| `渠道` | `管道` |
| `發佈` | `發布` |
| `打印` | `列印` |
| `數據` | `資料` |
| `用戶` | `使用者` |
| `服務器` | `伺服器` |
| `移動端` | `行動版 / 手機版` |
| `眾籌` | `群眾募資` |
| `支持者` in Kickstarter context | `贊助者` |
| `出版商` in game context | `發行商` |

## Style Guidelines

- Use Traditional Chinese for Taiwan.
- Avoid Simplified Chinese terminology, Mainland phrasing, and China-specific terminology unless directly quoting or discussing that usage as source context.
- Prefer natural spoken subtitle phrasing over literal English sentence structure.
- Keep proper nouns consistent with `glossary.md`.
- Use `《》` for game titles when the title is presented as a title in Chinese text.
- Keep official English titles in English unless the glossary specifies a localized form.
- Preserve speaker labels when they clarify the speaker.
- Translate bracketed sound/action cues consistently, such as `[音樂]`, `[笑聲]`, `[掌聲]`.
- Avoid over-translating filler words. Translate `um`, `uh`, `like`, and false starts only when they affect tone or rhythm.
- Keep profanity and jokes natural, but avoid making the subtitle harsher than the original.

## Punctuation Rules

Use full-width punctuation for Chinese subtitle text:

| Use | Avoid |
| --- | --- |
| `，` | `,` |
| `。` | `.` |
| `？` | `?` |
| `！` | `!` |
| `：` | `:` after speaker labels |
| `；` | `;` |
| `「」` | straight quotes for quoted speech in Chinese |
| `《》` | straight quotes around game titles in Chinese text |
| `……` | `...` when representing Chinese ellipsis |

Spacing rules:

- Insert one normal space between a full-width character and a half-width character when neither character is punctuation.
- Do not insert spaces before or after punctuation as a substitute for correct punctuation.
- Keep punctuation attached to the surrounding text according to normal Traditional Chinese usage.
- Use full-width Chinese punctuation instead of random spacing around half-width punctuation.

Punctuation examples:

| Situation | Preferred | Avoid |
| --- | --- | --- |
| Chinese next to English name | `如果我們表現得不好，Justin 會說，沒辦法，我們總之得做到。` | `如果我們表現得不好，Justin會說，沒辦法，我們總之得做到。` |
| Chinese next to English term | `我們得修 bug。` | `我們得修bug。` |
| Punctuation around English name | `Justin 說：「沒辦法。」` | `Justin 說 ： 沒辦法 。` |
| Chinese punctuation | `真的嗎？` | `真的嗎 ?` |

Examples:

| English | Preferred `Content_zh` style |
| --- | --- |
| `Schafer: Hi, guys. How's it going?` | `Schafer：大家好，最近怎麼樣？` |
| `Oh, spoilers for "Act 2"!` | `喔，《第二幕》劇透！` |
| `We're done!` | `我們完成了！` |

## Speaker Labels

- Keep English surname labels unless a final decision is made to localize all names.
- Normalize the separator to full-width colon: `Schafer：`, `Rice：`, `Offscreen：`.
- If one subtitle contains two speakers, preserve both labels if needed for clarity.
- Preserve sound cues before labels when present, but localize the cue and normalize the label punctuation, such as `[音樂] Schafer：`.
- Normalize casing variants such as `Offscreen Voice`, `Offscreen voice`, and `Offscreen` according to the glossary.
- Do not invent a speaker label when the English source does not identify the speaker.
- Generic labels are localized globally in the first-pass output:
  - `Offscreen` / `Offscreen voice` -> `畫外音`
  - `TV` -> `電視`
  - `Phone` -> `電話`

## Common Issue Types To Fix

- Half-width punctuation in Chinese text.
- Simplified Chinese characters, Simplified Chinese terminology, or Mainland phrasing.
- Inconsistent game title translations, especially `Broken Age`.
- Incorrect machine translations of names, such as `Double Fine` becoming `雙倍精華` or `雙倍罰款`.
- Incorrect game-title translations, such as `Psychonauts` becoming `精神分裂`.
- Inconsistent *Broken Age* in-world terms such as `Cloud Colony`, `Shellmound`, `Meriloft`, `Space Weaver`, `Mog Chothra`, `Hexipal`, `Vella`, `Shay`, and `Marek`.
- Literal translations of game-development terms, such as `ship`, `build`, `review key`, `publisher`, and `backer`.
- Missing speaker labels or incorrectly translated speaker labels.
- Dropped clauses, reversed meanings, or subtitles that do not match the English source.
- Overlong subtitles that are difficult to read.

## File-Level Workflow

For each CSV file:

1. Read several surrounding rows to understand the scene and speaker context.
2. Compare `Content_zh` against `Content` row by row.
3. When a line is ambiguous, check nearby rows and the episode summary before deciding the translation.
4. Correct meaning first, then rewrite into natural spoken Taiwan Traditional Chinese, then fix punctuation.
5. Apply glossary decisions consistently.
6. Leave `Timecode` untouched unless timing is clearly wrong.
7. After finishing the file, run QA checks before moving on.

## QA Checklist

Before marking a CSV complete:

- CSV still has exactly `Timecode`, `Content`, and `Content_zh` columns.
- Row count matches the input file.
- No empty `Content_zh` cells.
- No unintended changes to `Timecode`.
- Ambiguous lines have been checked against surrounding rows, speaker context, scene context, or the matching episode summary.
- No Simplified Chinese characters, Simplified Chinese terminology, or Mainland phrasing remains.
- No half-width commas, periods, question marks, exclamation marks, colons, or semicolons remain in Chinese contexts.
- One normal space appears between adjacent full-width and half-width non-punctuation characters, such as Chinese text next to English names, acronyms, numbers, or technical terms.
- No random spaces appear around punctuation; punctuation is corrected to proper full-width Chinese punctuation instead.
- Game titles, company names, people names, and technical terms match `glossary.md`.
- Speaker labels use consistent punctuation.
- Bracketed cues are consistently translated.
- Cue-plus-speaker labels keep both parts readable, for example `[音樂] Schafer：`.
- Recurring *Broken Age* locations, characters, and internal project terms match `glossary.md`.
- File-specific one-off labels are either preserved in English or localized according to the same rule as comparable labels.
- Spot-check generated SRT output for subtitle formatting.

## Automation Notes

The existing `scripts/sanitize_content_zh.py` should be reviewed before relying on it for production proofreading. Its current `sanitize_content()` implementation appears risky because the loop only appends characters inside a condition that can fail for the first character. Prefer manual proofreading plus targeted validation until that script is fixed and tested.

Automation can help identify likely issues, but it should not replace human proofreading for this project because the current machine translations contain many context-sensitive errors.
