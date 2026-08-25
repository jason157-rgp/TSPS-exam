#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
純文字版（不需 JavaScript）

主頁是單頁應用，全部內容存在 <script type="application/json"> 裡、由
瀏覽器端渲染。抓取工具把網頁轉成 markdown 時會丟掉 script 標籤，所以
不執行 JS 的讀取者只看得到外殼那 61 個字。

這裡從同一份資料另外產出一組靜態 HTML：每節一頁、每個群組一份合輯、
外加一份目錄。語意標籤（h1／table／ul／p）完整保留，任何抓取工具都能
直接轉成 markdown。
"""
import datetime
import html as H
import re
from pathlib import Path

EXAM = datetime.date(2026, 9, 5)
WEEK = "日一二三四五六"

CSS = """body{max-width:52rem;margin:0 auto;padding:2rem 1.2rem;line-height:1.75;
font-family:system-ui,-apple-system,"Noto Sans TC",sans-serif;color:#141a18}
h1{font-size:1.5rem;line-height:1.35} h2{font-size:1.15rem;margin-top:2rem}
table{border-collapse:collapse;width:100%;margin:1rem 0;font-size:.94rem}
th,td{border:1px solid #dce3e0;padding:.4rem .6rem;text-align:left;vertical-align:top}
th{background:#eef2f0}
code{background:#eef2f0;padding:.1rem .3rem;border-radius:3px}
blockquote{margin:1rem 0;padding-left:1rem;border-left:3px solid #0f6b5c}
.meta{color:#66736f;font-size:.9rem}
nav.bc{margin:0 0 1.5rem;font-size:.9rem}"""


def esc(s):
    return H.escape(s, quote=False)


def exam_date(n):
    d = EXAM - datetime.timedelta(days=n)
    return f"{d.month}/{d.day}（{WEEK[(d.weekday() + 1) % 7]}）"


def _page(title, body, crumb=""):
    return (
        "<!doctype html>\n<html lang=\"zh-Hant\">\n<head>\n<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">\n"
        f"<title>{esc(title)}</title>\n<style>{CSS}</style>\n</head>\n<body>\n"
        f"{crumb}{body}\n</body>\n</html>\n"
    )


def _deref(html, days):
    """把站內跳轉按鈕換成純連結，並把只有前端才會填的欄位補齊。"""
    html = re.sub(
        r'<button[^>]*\bdata-go="([^"]+)"[^>]*>(.*?)</button>',
        lambda m: f'<a href="{m.group(1)}.html">{m.group(2)}</a>',
        html, flags=re.S)

    def fill(m):
        row = m.group(0)
        hi, lo = int(m.group(1)), int(m.group(2))
        label = exam_date(hi) if hi == lo else f"{exam_date(hi)} – {exam_date(lo)}"
        return row.replace('<span class="dr"></span>',
                           f'<span class="dr">{label}</span>')

    html = re.sub(r'<tr data-dhi="(\d+)" data-dlo="(\d+)">.*?</tr>', fill, html, flags=re.S)
    html = html.replace("{{D}}", str(days)).replace("{{W}}", WEEK[(EXAM.weekday() + 1) % 7])
    return html


def _index_table(rows, dom_label):
    """第一部索引在主頁是前端渲染的，這裡另外攤成一張真表格。"""
    out = ['<table>', '<thead><tr><th>領域</th><th>等級</th><th>主題</th>'
           '<th>考官</th><th>模範答案位置</th></tr></thead>', '<tbody>']
    for r in rows:
        topic = r["t"]
        if r["go"]:
            topic = f'<a href="{r["go"]}.html">{topic}</a>'
        ex = "、".join(
            (f'<a href="{e["id"]}.html">{esc(e["n"])}</a>' if e["id"] else esc(e["n"]))
            + (f' {esc(e["y"])}' if e["y"] else "")
            for e in r["ex"])
        lv = (r["lv"] * 2 if r["hot"] else r["lv"]) + (f' {esc(r["lvn"])}' if r["lvn"] else "")
        out.append(f'<tr><td>{esc(dom_label(r["dom"]))}</td><td>{lv}</td>'
                   f'<td>{topic}</td><td>{ex}</td><td>{r["loc"]}</td></tr>')
    out += ['</tbody>', '</table>']
    return "\n".join(out)


def emit(sections, rows, outdir: Path, group_label, dom_label, days):
    outdir.mkdir(parents=True, exist_ok=True)
    for old in outdir.glob("*.html"):
        old.unlink()

    by_id = {s["id"]: s for s in sections}

    def head_of(s):
        bits = []
        if s.get("chapter"):
            bits.append(f"Ch.{s['chapter']}")
        bits += [dom_label(d) for d in (s.get("domains") or [])]
        if s.get("sub"):
            bits.append(s["sub"])
        if s.get("level"):
            bits.append(s["level"])
        seen_bits, uniq = set(), []
        for b in bits:                      # 領域與 sub 常常是同一個詞，去重
            if b not in seen_bits:
                seen_bits.add(b)
                uniq.append(b)
        return f'<p class="meta">{esc(" · ".join(uniq))}</p>' if uniq else ""

    def body_of(s):
        html = _deref(s["html"], days)
        if s.get("render") == "idx":
            html += "\n" + _index_table(rows, dom_label)
        return html

    # 每節一頁
    order = [s["id"] for s in sections]
    for i, s in enumerate(sections):
        nav = ['<nav class="bc"><a href="index.html">目錄</a>']
        if i:
            nav.append(f' · <a href="{order[i-1]}.html">上一節</a>')
        if i < len(sections) - 1:
            nav.append(f' · <a href="{order[i+1]}.html">下一節</a>')
        nav.append("</nav>")
        page = (f"<h1>{esc(s['title'])}</h1>\n{head_of(s)}\n{body_of(s)}")
        (outdir / f"{s['id']}.html").write_text(
            _page(s["title"], page, "".join(nav)), encoding="utf-8")

    # 群組合輯：主題節依領域、考官節依章、其餘依原分組
    bundles, seen = [], set()
    for key in ("gTo", "gEx"):
        for s in sections:
            if s["id"] in seen:
                continue
            if key == "gTo" and s["axis"] != "topic":
                continue
            if key == "gEx" and s["axis"] == "topic":
                continue
            g = s[key]
            members = [t for t in sections
                       if t["id"] not in seen and t[key] == g
                       and (t["axis"] == "topic") == (key == "gTo")]
            if not members:
                continue
            seen.update(t["id"] for t in members)
            bundles.append((g, group_label(g), members))

    for g, label, members in bundles:
        parts = [f"<h1>{esc(label)}</h1>",
                 f'<p class="meta">{len(members)} 節・'
                 f'{sum(len(m["text"]) for m in members)//1000}k 字</p>',
                 '<nav class="bc"><a href="index.html">回目錄</a></nav>']
        for s in members:
            parts.append(f'<h2 id="{s["id"]}">{esc(s["title"])}</h2>')
            parts.append(head_of(s))
            parts.append(body_of(s))
        (outdir / f"bundle-{g}.html").write_text(
            _page(label, "\n".join(parts)), encoding="utf-8")

    # 目錄
    stamp = datetime.date.today().isoformat()
    total = sum(len(s["text"]) for s in sections)
    toc = [
        "<h1>整專口試作戰室・純文字版</h1>",
        f'<p class="meta">靜態 HTML，不需 JavaScript。共 {len(sections)} 節、'
        f'{total//1000}k 字。建置於 {stamp}，考試日 {EXAM.isoformat()}（{exam_date(0)}）。</p>',
        "<p>主頁 <code>../index.html</code> 是單頁應用，內容存放在 JSON 區塊中由瀏覽器渲染；"
        "抓取工具轉 markdown 時會丟掉 script 標籤，因此另備這一份靜態版本供程式讀取。</p>",
        "<h2>合輯（建議先讀這個）</h2>",
        "<table><thead><tr><th>合輯</th><th>節數</th><th>字數</th></tr></thead><tbody>",
    ]
    for g, label, members in bundles:
        toc.append(f'<tr><td><a href="bundle-{g}.html">{esc(label)}</a></td>'
                   f'<td>{len(members)}</td>'
                   f'<td>{sum(len(m["text"]) for m in members)//1000}k</td></tr>')
    toc += ["</tbody></table>", "<h2>逐節</h2>",
            "<table><thead><tr><th>代號</th><th>標題</th><th>分類</th>"
            "<th>字數</th></tr></thead><tbody>"]
    for s in sections:
        cat = " · ".join(filter(None, [
            f"Ch.{s['chapter']}" if s.get("chapter") else "",
            *[dom_label(d) for d in (s.get("domains") or [])]])) or group_label(s["gTo"])
        toc.append(f'<tr><td><code>{s["id"]}</code></td>'
                   f'<td><a href="{s["id"]}.html">{esc(s["title"])}</a></td>'
                   f'<td>{esc(cat)}</td><td>{len(s["text"])//1000 or "<1"}k</td></tr>')
    toc += ["</tbody></table>"]
    (outdir / "index.html").write_text(
        _page("整專口試作戰室・純文字版", "\n".join(toc)), encoding="utf-8")

    return len(sections), len(bundles)
