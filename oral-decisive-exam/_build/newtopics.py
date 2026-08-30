#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
補寫的主題節（_build/newtopics/*.md）

手冊原本沒有、但今年的考官情報顯示會考的題目。每個檔案開頭是幾行
`key: value` 的抬頭，後面就是內文，格式與 _build/md/ 相同。

來源分級沿用手冊既有的方括號慣例，並把出處寫到章：
    〔Grabb 9e Ch13〕〔Neligan 5e Vol5 Ch25〕  課本，考官手上那一本，可以講死
    〔指引〕〔文獻〕                            課本沒有，第二層彈藥
    ⚠ 課本查無明確出處                          照手冊慣例，被追問時不要硬掰
"""
import re
from pathlib import Path

import markdown

MD = markdown.Markdown(extensions=["tables", "sane_lists"])
HEAD = re.compile(r"^([a-z]+):[ \t]*(.*)$")


def strip_tags(html: str) -> str:
    text = re.sub(r"<[^>]+>", " ", html)
    for a, b in (("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"),
                 ("&quot;", '"'), ("&#39;", "'"), ("&nbsp;", " ")):
        text = text.replace(a, b)
    return re.sub(r"\s+", " ", text).strip()


def parse(path: Path):
    lines = path.read_text(encoding="utf-8").split("\n")
    meta, i = {}, 0
    while i < len(lines) and (m := HEAD.match(lines[i])):
        meta[m.group(1)] = m.group(2).strip()
        i += 1
    body = "\n".join(lines[i:]).strip()
    for need in ("id", "title", "domain"):
        if need not in meta:
            raise SystemExit(f"[newtopics] {path.name} 缺少抬頭 {need}")

    MD.reset()
    html = MD.convert(body)
    return {
        "id": meta["id"],
        "title": meta["title"],
        "sub": meta.get("sub", ""),
        "group": meta["domain"],
        "tags": [t for t in meta.get("tags", "").split("、") if t],
        "headline": meta.get("headline", ""),
        "html": html,
        "text": (meta["title"] + " " + strip_tags(html)).strip(),
        "name": "",
        "axis": "topic",
        "topicIds": [],
        "level": meta.get("level", ""),
        "refIds": [],
        "refNames": [],
        "isNew": True,
        # 第一部索引用：examiners 寫成「姓名|節代號|年份」，以頓號分隔
        "_idx": {"lv": meta.get("level", ""), "lvn": meta.get("lvn", ""),
                 "topic": meta.get("idx", meta["title"].split("（")[0]),
                 "ex": [tuple((e.split("|") + ["", ""])[:3])
                        for e in meta.get("examiners", "").split("、") if e],
                 "loc": meta.get("loc", "")},
    }


def load(src: Path):
    if not src.is_dir():
        return []
    return [parse(p) for p in sorted(src.glob("*.md"))]


def index_rows(topics):
    """把補寫的節也放進第一部索引，否則從索引找不到它們。"""
    rows = []
    for t in topics:
        ix = t["_idx"]
        rows.append({
            "dom": t["group"], "lv": ix["lv"] or "🟡", "lvn": ix["lvn"], "hot": False,
            "t": f"<strong>{ix['topic']}</strong>　<em>（新增）</em>",
            "tt": ix["topic"], "go": t["id"],
            "ex": [{"n": n, "id": sid, "y": y} for n, sid, y in ix["ex"]],
            "loc": ix["loc"] or f'<button type="button" class="jump" '
                               f'data-go="{t["id"]}">本節</button>',
        })
    return rows
