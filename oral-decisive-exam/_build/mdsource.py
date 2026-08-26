#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
以校訂版 markdown 取代各節內容（框架不動）

_build/md/ 放 11 個 .md 原始檔。這裡把它們切成節、轉成 HTML，
再依「節代號」覆蓋 source.html 既有節的 html／text。

框架完全不動：節代號、順序、axis、group、tags、level、refIds、
topicIds、sub 一律沿用 source.html，只換內容。

切節規則
--------
主題卷（t1–t6）：每個 `### ` 就是一節，標題與網站逐字對應。
考官章（ch_*）：以「邊界」切——標題能對上網站某一節才切新節，
其餘標題（固定題組、⚠ 地雷、資料缺口、事實查核記錄…）自然併入
前一節，因此 md 裡沒有一段會被丟掉。
"""
import re
from pathlib import Path

import markdown

TOPIC_FILES = [
    "t1_craniofacial.md", "t2_oculoplastic.md", "t3_hand.md",
    "t4_micro_breast.md", "t5_burn_wound.md", "t6_tumor_principles.md",
]
CHAPTER_FILES = [
    "ch_2025A.md", "ch_2025B.md", "ch_2025C.md", "ch_hist_D.md", "ch_hist_E.md",
]

# 主題卷卷首 → 網站的「卷首」節。t1 在網站沒有對應的卷首節，故不列。
VOLUME_INTRO = {
    "t2_oculoplastic.md": "tointro41",
    "t3_hand.md": "thintro82",
    "t4_micro_breast.md": "tmintro105",
    "t5_burn_wound.md": "tbintro137",
    "t6_tumor_principles.md": "tpintro162",
}

# 標題只差一個前綴符號，對不上字串，逐筆指定
TITLE_ALIAS = {
    "⭐ 本章速覽（考前 30 分鐘掃描用）": "本章速覽（考前 30 分鐘掃描用）",
    "📌 本章最後 10 分鐘複習清單": "本章最後 10 分鐘複習清單",
}

# 這個標題在五個考官章各出現一次，但網站的同名節屬於索引章。
# 不可當成切節邊界，否則會把索引章的節換成考官章的內容。
NEVER_BOUNDARY = {"📌 本章事實查核修正記錄（2026/08/24）"}

HEADING = re.compile(r"^(#{1,6})\s+(.*)$")
# 〔醫院〕姓名 / §1｜〔醫院〕姓名 / 5-4〔醫院〕姓名
EXAMINER_HEAD = re.compile(r"^(?:§\d+｜|\d-\d)?〔[^〕]+〕\s*(.+)$")

MD = markdown.Markdown(extensions=["tables", "sane_lists"])


def to_html(md_text: str) -> str:
    MD.reset()
    return MD.convert(md_text.strip())


def strip_tags(html: str) -> str:
    text = re.sub(r"<[^>]+>", " ", html)
    for a, b in (("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"),
                 ("&quot;", '"'), ("&#39;", "'"), ("&nbsp;", " ")):
        text = text.replace(a, b)
    return re.sub(r"\s+", " ", text).strip()


def _split_headings(text):
    lines = text.split("\n")
    marks = [(i, len(m.group(1)), m.group(2).strip())
             for i, l in enumerate(lines) if (m := HEADING.match(l))]
    return lines, marks


def load(md_dir: Path, sections):
    """回傳 {節代號: markdown 內容}，以及沒有用到的檔案／對不上的標題。"""
    by_title = {s["title"]: s for s in sections}
    examiner_by_name = {}
    for s in sections:
        if s["axis"] == "examiner":
            examiner_by_name[s["title"].split("　")[-1].strip()] = s["id"]

    out, report = {}, {"missing_files": [], "unmatched_titles": []}

    # ---- 主題卷 ----
    for fname in TOPIC_FILES:
        path = md_dir / fname
        if not path.exists():
            report["missing_files"].append(fname)
            continue
        raw = path.read_text(encoding="utf-8")
        head, *rest = re.split(r"\n### ", raw)
        intro_id = VOLUME_INTRO.get(fname)
        if intro_id and intro_id in {s["id"] for s in sections}:
            body = re.sub(r"^#\s+.*$", "", head, count=1, flags=re.M)
            out[intro_id] = body
        for chunk in rest:
            title = chunk.split("\n")[0].strip()
            target = by_title.get(title)
            if not target:
                report["unmatched_titles"].append((fname, title))
                continue
            body = "\n".join(chunk.split("\n")[1:])
            body = re.sub(r"^(?:LEVEL|REFS):.*$", "", body, flags=re.M)
            out[target["id"]] = body

    # ---- 考官章 ----
    for fname in CHAPTER_FILES:
        path = md_dir / fname
        if not path.exists():
            report["missing_files"].append(fname)
            continue
        lines, marks = _split_headings(path.read_text(encoding="utf-8"))

        def boundary(title):
            """這個標題是否對應到網站的某一節？是的話回傳節代號。"""
            if title in NEVER_BOUNDARY:
                return None
            t = TITLE_ALIAS.get(title, title)
            if t in by_title:
                return by_title[t]["id"]
            m = EXAMINER_HEAD.match(t)
            if m:
                tail = m.group(1)
                for name, sid in examiner_by_name.items():
                    if tail.startswith(name):
                        return sid
            return None

        cuts = [(i, boundary(t)) for i, _lv, t in marks]
        cuts = [(i, sid) for i, sid in cuts if sid]
        for k, (i, sid) in enumerate(cuts):
            end = cuts[k + 1][0] if k + 1 < len(cuts) else len(lines)
            out[sid] = "\n".join(lines[i + 1:end])

    return out, report


def apply(sections, md_dir: Path):
    """把校訂版內容寫回各節，回傳統計。"""
    replaced = {}
    content, report = load(md_dir, sections)
    for s in sections:
        body = content.get(s["id"])
        if body is None or not body.strip():
            continue
        html = to_html(body)
        replaced[s["id"]] = (len(s["text"]), len(strip_tags(html)))
        s["html"] = html
        s["text"] = (s["title"] + " " + strip_tags(html)).strip()
        s["fromMd"] = True
    return replaced, report
