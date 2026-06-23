import argparse
import csv
import re
from pathlib import Path


FIELDNAMES = ["Timecode", "Content", "Content_zh"]

TERM_REPLACEMENTS = [
    ("雙倍精華", "Double Fine"),
    ("雙倍罰款", "Double Fine"),
    ("雙精靈線", "Double Fine Hint Line"),
    ("雙精", "Double Fine"),
    ("雙倍的好冒險", "《Double Fine Adventure!》"),
    ("雙倍的冒險", "《Double Fine Adventure!》"),
    ("雙倍精品", "Double Fine"),
    ("雙倍法恩", "Double Fine"),
    ("雙倍好", "Double Fine"),
    ("雙倍的Fine", "Double Fine"),
    ("雙倍的 Fine", "Double Fine"),
    ("白羅肯時代", "《Broken Age》"),
    ("白羅肯年代", "《Broken Age》"),
    ("破碎年代", "《Broken Age》"),
    ("破紀元", "《Broken Age》"),
    ("破紀念", "《Broken Age》"),
    ("破年紀", "《Broken Age》"),
    ("Broken時代", "《Broken Age》"),
    ("《Broken時代》", "《Broken Age》"),
    ("精神分裂", "《Psychonauts》"),
    ("精神病人", "《Psychonauts》"),
    ("踢球手", "Kickstarter"),
    ("踢踏者", "Kickstarter"),
    ("審查金鑰", "評測序號"),
    ("審查鍵", "評測序號"),
    ("審查複本", "評測版"),
    ("禁運", "禁評期"),
    ("船運", "推出"),
    ("切口", "過場動畫"),
    ("蟲子", "bug"),
    ("出版商", "發行商"),
    ("支持者", "贊助者"),
    ("眾籌", "群眾募資"),
    ("視頻", "影片"),
    ("屏幕", "螢幕"),
    ("項目", "專案"),
    ("程序", "程式"),
    ("軟件", "軟體"),
    ("硬件", "硬體"),
    ("網絡", "網路"),
    ("質量", "品質"),
    ("渠道", "管道"),
    ("打印", "列印"),
    ("數據", "資料"),
    ("用戶", "使用者"),
    ("服務器", "伺服器"),
    ("移動端", "行動版"),
    ("發射日期", "發行日"),
    ("碟片版本", "光碟版"),
    ("盤片版本", "光碟版"),
    ("自動售貨機", "自動販賣機"),
    ("馬奇納裏姆", "Machinarium"),
    ("Game Spot", "GameSpot"),
    ("羅恩·吉爾伯特", "Ron Gilbert"),
    ("蒂姆·斯切弗", "Tim Schafer"),
    ("理查德·布蘭森", "Richard Branson"),
    ("舍佛曰", "Schafer："),
    ("沙弗", "Schafer"),
    ("沙佛", "Schafer"),
    ("舍弗", "Schafer"),
    ("斯切弗", "Schafer"),
    ("雷莫", "Remo"),
    ("布朗", "Brown"),
    ("克魯克", "Crook"),
    ("Sp者", "劇透"),
]

TITLE_REPLACEMENTS = [
    ("Machinarium", "《Machinarium》"),
    ("Full Throttle", "《Full Throttle》"),
    ("Grim Fandango", "《Grim Fandango》"),
    ("Psychonauts 2", "《Psychonauts 2》"),
    ("Psychonauts", "《Psychonauts》"),
    ("Brutal Legend", "《Brütal Legend》"),
    ("Brütal Legend", "《Brütal Legend》"),
    ("Day of the Tentacle", "《Day of the Tentacle》"),
    ("Massive Chalice", "《Massive Chalice》"),
    ("Costume Quest", "《Costume Quest》"),
    ("Iron Brigade", "《Iron Brigade》"),
    ("Trenched", "《Trenched》"),
]

CUE_REPLACEMENTS = {
    "Music": "音樂",
    "Laughter": "笑聲",
    "Applause": "掌聲",
    "Yelling": "叫喊聲",
}

LABEL_REPLACEMENTS = {
    "Offscreen voice": "畫外音",
    "Offscreen": "畫外音",
    "Voice": "聲音",
    "TV": "電視",
    "Phone": "電話",
    "Host": "主持人",
    "Team Member": "團隊成員",
    "Narrator": "旁白",
    "螢幕外聲音": "畫外音",
    "屏幕外聲音": "畫外音",
    "畫面外聲音": "畫外音",
    "水稻": "Rice",
    "稻": "Rice",
    "布朗": "Brown",
    "克魯克": "Crook",
    "雷莫": "Remo",
    "沙弗": "Schafer",
    "沙佛": "Schafer",
    "舍弗": "Schafer",
}


def replace_titles(text):
    for source, target in TITLE_REPLACEMENTS:
        text = re.sub(rf"(?<!《){re.escape(source)}(?!》)", target, text)
    text = text.replace("《《", "《").replace("》》", "》")
    return text


def normalize_cues(text, english):
    text = text.replace("[大叫]", "[叫喊聲]")
    for source, target in CUE_REPLACEMENTS.items():
        text = text.replace(f"[{source}]", f"[{target}]")
        if english.startswith(f"[{source}]") and f"[{target}]" not in text:
            text = f"[{target}] {text}"
    return text


def normalize_labels(text):
    for source, target in sorted(LABEL_REPLACEMENTS.items(), key=lambda item: -len(item[0])):
        text = re.sub(rf"(^|\s){re.escape(source)}\s*[:：]", rf"\1{target}：", text)
    text = re.sub(r"(^|\s)([A-Z][A-Za-z'’-]+)\s*:", r"\1\2：", text)
    for label in [
        "Schafer", "Rice", "Petty", "Crook", "Franzke", "Bailey", "Kipnis", "Stapley",
        "Hansen", "Brown", "McConnell", "Bagel", "Stoddard", "Ryken", "Gardner",
        "Spafford", "Min", "Chan", "Gilbert", "Muir", "Remo", "Stamos", "Swisshelm",
        "Annable", "Peck", "Dillon", "Romero", "Turi", "Wood", "Russell", "LeBreton",
        "Roberts", "Garner", "Kaufman", "Fietzek",
    ]:
        text = re.sub(rf"{label}\s*:", f"{label}：", text)
    return text


def normalize_punctuation(text):
    text = text.replace("...", "……")
    text = text.replace("…", "……")
    text = re.sub(r"……+", "……", text)
    text = re.sub(r"(?<=[\u4e00-\u9fff》）\]])\s*,\s*", "，", text)
    text = re.sub(r",\s*(?=[\u4e00-\u9fff《（\[])", "，", text)
    text = re.sub(r"(?<=[\u4e00-\u9fff》）\]])\s*\.\s*", "。", text)
    text = re.sub(r"\.\s*(?=[\u4e00-\u9fff《（\[])", "。", text)
    text = re.sub(r"(?<=[\u4e00-\u9fff》）\]])\s*\?", "？", text)
    text = re.sub(r"\?\s*(?=[\u4e00-\u9fff《（\[])", "？", text)
    text = re.sub(r"(?<=[\u4e00-\u9fff》）\]])\s*!", "！", text)
    text = re.sub(r"!\s*(?=[\u4e00-\u9fff《（\[])", "！", text)
    text = re.sub(r"(?<=[\u4e00-\u9fff》）\]])\s*;", "；", text)
    text = re.sub(r";\s*(?=[\u4e00-\u9fff《（\[])", "；", text)
    text = re.sub(r"(?<=[\u4e00-\u9fff》）\]])\s*:\s*(?=[\u4e00-\u9fff《（\[])", "：", text)
    text = re.sub(r"(?<=[\u4e00-\u9fff》）\]])\s*:\s*(?=[\"“”])", "：", text)
    text = re.sub(r"(?<=[\u4e00-\u9fff》）\]])\s*:$", "：", text)
    text = re.sub(r"(?i)spoiler\s*:\s*", "劇透：", text)
    text = re.sub(r'"(《[^》]+》)"', r"\1", text)
    text = re.sub(r"：\s+", "：", text)
    text = re.sub(r"\s+([，。？！：；])", r"\1", text)
    text = re.sub(r"([，。？！：；])(?=[^\s，。？！：；》）\]])", r"\1", text)
    return text.strip()


def proofread_text(text, english):
    if not text:
        return text

    text = normalize_cues(text, english)
    for source, target in TERM_REPLACEMENTS:
        text = text.replace(source, target)

    if "Broken Age" in english:
        text = re.sub(r"(?<!《)Broken Age(?!》)", "《Broken Age》", text)
    if "Act 1" in english or "Act One" in english:
        text = text.replace("Act 1", "第一幕").replace("Act One", "第一幕")
    if "Act 2" in english or "Act Two" in english:
        text = text.replace("Act 2", "第二幕").replace("Act Two", "第二幕")

    text = replace_titles(text)
    text = normalize_labels(text)
    text = normalize_punctuation(text)
    return text


def process_file(input_path, output_path):
    with input_path.open(newline="", encoding="utf-8-sig") as infile:
        reader = csv.DictReader(infile)
        if reader.fieldnames != FIELDNAMES:
            raise ValueError(f"Unexpected columns in {input_path}: {reader.fieldnames}")
        rows = list(reader)

    changed = 0
    for row in rows:
        original = row["Content_zh"]
        row["Content_zh"] = proofread_text(original, row["Content"])
        changed += original != row["Content_zh"]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=FIELDNAMES, quoting=csv.QUOTE_ALL, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    return len(rows), changed


def main():
    parser = argparse.ArgumentParser(description="First-pass proofread Content_zh in subtitle CSV files.")
    parser.add_argument("--input", default="pretranslated csv")
    parser.add_argument("--output", default="proofread csv")
    args = parser.parse_args()

    input_dir = Path(args.input)
    output_dir = Path(args.output)
    total_rows = 0
    total_changed = 0

    for input_path in sorted(input_dir.glob("*_pretranslated.csv")):
        output_path = output_dir / input_path.name
        rows, changed = process_file(input_path, output_path)
        total_rows += rows
        total_changed += changed
        print(f"{input_path.name}: {changed}/{rows} rows changed")

    print(f"Total: {total_changed}/{total_rows} rows changed")


if __name__ == "__main__":
    main()
