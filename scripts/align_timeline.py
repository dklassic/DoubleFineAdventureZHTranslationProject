"""Force-align bilingual subtitle CSVs to the English release audio.

Install pocketsphinx>=5.0 and FFmpeg. Run from the repository root, e.g.
    python scripts/align_timeline.py "pretranslated csv" "aligned csv" --media-dir episodes

Pair 01_pretranslated.csv with 01.wav, 01.mp4, etc. Media can also live
beside the CSVs. Supply the English mix as the first audio stream.
"""

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path
import re
import subprocess
import sys
import tempfile

from srt_preprocess import read_srt

MEDIA = {".wav", ".mp3", ".flac", ".m4a", ".mp4", ".mkv", ".webm", ".mov", ".aac"}
STAMP = r"(\d{2}):([0-5]\d):([0-5]\d),(\d{3})"
EVENT = r"\[[^\[\]]+\]"
LABEL = re.compile(r"^[A-Za-z][\w.'’\-]*(?:\s+[A-Za-z][\w.'’\-]*){0,4}:\s*")


def milliseconds(parts):
    h, m, s, ms = map(int, parts)
    return ((h * 60 + m) * 60 + s) * 1000 + ms


def stamp(ms):
    seconds, ms = divmod(ms, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02},{ms:03}"


@dataclass
class Cue:
    row: dict
    source: int
    start: int
    end: int
    words: tuple = ()
    reason: str = ""
    aligned: tuple = ()


def raw_pairs(path):
    """Index adjacent raw cues by the outer times retained by the merger."""
    if not path.is_file():
        return {}
    subs = read_srt(path)
    return {(a.start.strftime("%H:%M:%S,%f")[:-3], b.end.strftime("%H:%M:%S,%f")[:-3]):
            (a, b) for a, b in zip(subs, subs[1:])}


def split_event(cue, pairs):
    pair = pairs.get((stamp(cue.start), stamp(cue.end)))
    if not pair:
        return [cue]
    left, right = pair
    en = [" ".join(sub.text).strip() for sub in pair]
    if " ".join(en) != " ".join(cue.row["Content"].split()):
        return [cue]
    zh = cue.row["Content_zh"].strip()
    # Split only when both languages have an identifiable standalone event.
    if re.fullmatch(EVENT, en[0]) and not re.search(EVENT, en[1]):
        match = re.fullmatch(f"({EVENT})\\s*(.+)", zh, re.S)
    elif re.fullmatch(EVENT, en[1]) and not re.search(EVENT, en[0]):
        match = re.fullmatch(f"(.+?)\\s*({EVENT})", zh, re.S)
    else:
        return [cue]
    if not match or len(re.findall(EVENT, zh)) != 1:
        return [cue]
    left_end, right_start = [
        milliseconds((t.hour, t.minute, t.second, t.microsecond // 1000))
        for t in (left.end, right.start)
    ]
    if not cue.start < left_end <= right_start < cue.end:
        return [cue]
    return [Cue(dict(cue.row, Content=e, Content_zh=z), cue.source, a, b)
            for e, z, a, b in zip(en, match.groups(), (cue.start, right_start),
                                   (left_end, cue.end))]


def read_csv(path, pairs):
    cues = []
    with path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames or []
        if not {"Timecode", "Content", "Content_zh"}.issubset(fields):
            raise ValueError(f"{path}: missing bilingual CSV columns")
        for number, row in enumerate(reader, 1):
            if None in row or None in row.values():
                raise ValueError(f"{path}: malformed CSV row {number}")
            match = re.fullmatch(STAMP + r"\s*-->\s*" + STAMP, row["Timecode"].strip())
            if not match:
                raise ValueError(f"{path}: invalid Timecode at row {number}")
            start = milliseconds(match.groups()[:4])
            end = milliseconds(match.groups()[4:])
            if end <= start or (cues and start < cues[-1].end):
                raise ValueError(f"{path}: invalid or overlapping interval at row {number}")
            cues.extend(split_event(Cue(row, number, start, end), pairs))
    return fields, cues


def prepare(cue, decoder):
    text = LABEL.sub("", cue.row["Content"].strip()).lower().replace("’", "'")
    if re.search(r"[\[\]()♪♫:]", text):
        cue.reason = "event or mixed dialogue"
    elif re.search(r"[^a-z\s'.,!?…—–\"-]", text):
        cue.reason = "spoken form needs review"
    elif cue.end - cue.start > 30000:
        cue.reason = "long interval"
    else:
        cue.words = tuple(re.findall(r"[a-z]+(?:'[a-z]+)*", text))
        unknown = sorted({word for word in cue.words if not decoder.lookup_word(word)})
        if not cue.words:
            cue.reason = "no spoken words"
        elif unknown:
            cue.reason = "unknown pronunciation: " + ", ".join(unknown)


def align_group(group, decoder, pcm, lo, hi):
    words = [word for cue in group for word in cue.words]
    pcm.seek(lo * 32)  # 16 kHz, mono, signed 16-bit samples
    data = pcm.read((hi - lo) * 32)
    if not any(data):
        for cue in group:
            cue.reason = "silent audio window"
        return
    decoder.set_align_text(" ".join(words))
    decoder.start_utt()
    decoder.process_raw(data, full_utt=True)
    decoder.end_utt()
    segments = [(re.sub(r"\(\d+\)$", "", s.word), s.start_frame, s.end_frame)
                for s in (decoder.seg() or ()) if not s.word.startswith(("<", "["))]
    if [s[0] for s in segments] != words:
        if len(group) == 1:
            group[0].reason = "incomplete word alignment"
            return
        # A missed word in one row can invalidate the entire search. Retry
        # shorter transcripts with context on both sides of the shared edge.
        mid = len(group) // 2
        align_group(group[:mid], decoder, pcm, lo, min(hi, group[mid - 1].end + 750))
        align_group(group[mid:], decoder, pcm, max(lo, group[mid].start - 750), hi)
        return
    index = 0
    for cue in group:
        start = lo + segments[index][1] * 10
        index += len(cue.words)
        end = min(hi, lo + (segments[index - 1][2] + 1) * 10)
        if max(abs(start - cue.start), abs(end - cue.end)) > 1000:
            cue.reason = "boundary moved over one second"
        elif end - start < 100:
            cue.reason = "implausibly short speech"
        else:
            cue.aligned = (start, end)


def align(cues, decoder, pcm, duration):
    if cues and cues[-1].end > duration:
        raise ValueError("last cue exceeds audio duration; verify the release cut")
    for cue in cues:
        prepare(cue, decoder)
    i = 0
    while i < len(cues):
        if cues[i].reason:
            i += 1
            continue
        j = i + 1
        while (j < len(cues) and not cues[j].reason and
               cues[j].end - cues[i].start <= 30000 and
               cues[j].start - cues[j - 1].end <= 1000):
            j += 1
        lo = max(cues[i - 1].end if i else 0, cues[i].start - 750)
        hi = min(cues[j].start if j < len(cues) else duration, cues[j - 1].end + 750)
        align_group(cues[i:j], decoder, pcm, lo, hi)
        i = j

    # Reverting a rejected neighbor can itself introduce an overlap. Propagate
    # rejections until every retained candidate fits beside its final neighbors.
    while True:
        conflicts = []
        for left, right in zip(cues, cues[1:]):
            if (left.aligned or (left.start, left.end))[1] > (right.aligned or (right.start, right.end))[0]:
                conflicts.extend(c for c in (left, right) if c.aligned)
        if not conflicts:
            return
        for cue in conflicts:
            cue.aligned = ()
            cue.reason = "conflict with neighboring cue"


def process(path, media, raw, output, decoder):
    fields, cues = read_csv(path, raw_pairs(raw))
    with tempfile.TemporaryFile() as pcm:
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", str(media),
                        "-map", "0:a:0", "-af", "aresample=async=1:first_pts=0",
                        "-ac", "1", "-ar", "16000", "-f", "s16le", "pipe:1"],
                       stdout=pcm, check=True)
        align(cues, decoder, pcm, pcm.tell() // 32)
    report_dir = output / "review"
    report_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=output) as stage:
        csv_path = Path(stage) / "aligned.csv"
        report_path = Path(stage) / "review.csv"
        with csv_path.open("w", newline="", encoding="utf-8") as f, report_path.open(
                "w", newline="", encoding="utf-8") as r:
            writer = csv.DictWriter(f, fields, quoting=csv.QUOTE_ALL)
            writer.writeheader()
            report = csv.writer(r)
            report.writerow(["source_cue", "output_cue", "original", "output", "result"])
            for number, cue in enumerate(cues, 1):
                a, b = cue.aligned or (cue.start, cue.end)
                timecode = f"{stamp(a)} --> {stamp(b)}"
                writer.writerow(dict(cue.row, Timecode=timecode))
                report.writerow([cue.source, number, cue.row["Timecode"], timecode,
                                 cue.reason or "aligned"])
        report_path.replace(report_dir / path.name)
        csv_path.replace(output / path.name)
    print(f"{path.name}: {sum(bool(c.aligned) for c in cues)}/{len(cues)} output cues aligned")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("input_dir", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--media-dir", type=Path, help="defaults to the input directory")
    parser.add_argument("--raw-dir", type=Path, help="defaults to sibling 'raw subtitles'")
    args = parser.parse_args()
    if args.input_dir.resolve() == args.output_dir.resolve():
        parser.error("choose a separate output directory")
    paths = sorted(args.input_dir.glob("*.csv"))
    if not paths:
        parser.error(f"no CSV files in {args.input_dir}")
    media_dir = args.media_dir or args.input_dir
    media = [p for p in media_dir.iterdir() if p.is_file() and p.suffix.lower() in MEDIA]
    jobs = []
    for path in paths:
        episode = path.stem.split("_")[0]
        matches = [p for p in media if p.stem in {episode, path.stem}]
        if len(matches) != 1:
            parser.error(f"{path.name}: expected one media file named {episode} or {path.stem} "
                         f"in {media_dir}, found {len(matches)}")
        raw_dir = args.raw_dir or args.input_dir.parent / "raw subtitles"
        jobs.append((path, matches[0], raw_dir / f"{episode}.srt"))
    try:
        from pocketsphinx import Decoder
    except ImportError:
        parser.error("install the aligner with: python -m pip install 'pocketsphinx>=5.0,<6'")
    decoder = Decoder(lm=None, frate=100, loglevel="ERROR")
    for path, media_file, raw in jobs:
        process(path, media_file, raw, args.output_dir, decoder)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError) as exc:
        sys.exit(f"Alignment failed: {exc}")
