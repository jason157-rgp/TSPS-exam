#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
段落結構修復 —— 純標記層，不改動任何一個字。

原始 markdown 在標題行與其後的項目之間少了空行，轉檔時整段被當成一個
段落，於是：

  <p><strong>第一層，Skin…</strong>
  - <strong>全身最薄的皮膚…</strong>
  - 臨床意義：…</p>

HTML 會把換行摺成空白，所以條列、表格、編號全部擠成一坨文字。全書有
2,122 個條列項、77 個 markdown 表格、約 350 個編號項卡在這種段落裡。

這裡把它們還原成 <table>／<ul>／分行，並在切開後補平跨行的標籤。
"""
import re

BULLET = re.compile(r"^(\s*)[-－]\s+(.*)$")
NUMBERED = re.compile(r"^(\s*)((?:[①-⑳]|\d{1,2}[.)])）?)\s+(.*)$")
PIPE = re.compile(r"^\s*\|")
SEPARATOR = re.compile(r"^\s*\|[\s:|-]*\|\s*$")

PAIRED = ("strong", "em", "code", "sub", "sup", "del", "a")
TAG = re.compile(r"<(/?)(" + "|".join(PAIRED) + r")\b[^>]*>", re.I)


def balance(frag: str) -> str:
    """切行之後可能留下沒關的或多餘的標籤，補平它。"""
    stack, out, pos = [], [], 0
    for m in TAG.finditer(frag):
        out.append(frag[pos:m.start()])
        closing, name = m.group(1) == "/", m.group(2).lower()
        if closing:
            if name in stack:                     # 關掉它上面沒關的
                while stack and stack[-1] != name:
                    out.append(f"</{stack.pop()}>")
                stack.pop()
                out.append(m.group(0))
            # 沒有對應的開頭就丟掉這個結尾標籤
        else:
            stack.append(name)
            out.append(m.group(0))
        pos = m.end()
    out.append(frag[pos:])
    while stack:
        out.append(f"</{stack.pop()}>")
    return "".join(out)


def _cells(line: str):
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [balance(c.strip()) for c in line.split("|")]


def _table(lines, stats):
    """markdown 表格 → 真正的 <table>。沒有分隔列的就不當表格處理。"""
    if len(lines) < 2 or not any(SEPARATOR.match(l) for l in lines[:2]):
        return None
    head = _cells(lines[0])
    body = [_cells(l) for l in lines[1:] if not SEPARATOR.match(l)]
    width = max([len(head)] + [len(r) for r in body])
    pad = lambda r: r + [""] * (width - len(r))
    stats["tables"] += 1
    stats["table_rows"] += len(body)
    out = ["<table>", "<thead>", "<tr>"]
    out += [f"<th>{c}</th>" for c in pad(head)]
    out += ["</tr>", "</thead>", "<tbody>"]
    for r in body:
        out.append("<tr>")
        out += [f"<td>{c}</td>" for c in pad(r)]
        out.append("</tr>")
    out += ["</tbody>", "</table>"]
    return "\n".join(out)


def _list(items, stats, cls=None):
    """items: [(縮排, 前綴, 內容)]。縮排較深的收成巢狀清單。"""
    attr = f' class="{cls}"' if cls else ""
    out, depth = [f"<ul{attr}>"], 0
    for indent, marker, text in items:
        want = 1 if indent >= 2 else 0
        while want > depth:
            out.append(f"<ul{attr}>")
            depth += 1
        while want < depth:
            out.append("</ul>")
            depth -= 1
        body = (f'<span class="mk">{marker}</span> ' if marker else "") + text
        out.append(f"<li>{balance(body)}</li>")
        stats["items"] += 1
    out += ["</ul>"] * (depth + 1)
    return "\n".join(out)


def _classify(line):
    if PIPE.match(line):
        return "pipe"
    if BULLET.match(line):
        return "bullet"
    if NUMBERED.match(line):
        return "num"
    return "text"


def restructure_paragraph(inner: str, stats) -> str:
    lines = inner.split("\n")
    if len(lines) < 2:
        return f"<p>{inner}</p>"

    out, buf, kind = [], [], None

    def flush():
        nonlocal buf, kind
        if not buf:
            return
        if kind == "pipe":
            t = _table(buf, stats)
            out.append(t if t else f"<p>{balance(chr(10).join(buf))}</p>")
        elif kind == "bullet":
            items = []
            for l in buf:
                m = BULLET.match(l)
                items.append((len(m.group(1)), "", m.group(2)))
            out.append(_list(items, stats))
        elif kind == "num":
            items = []
            for l in buf:
                m = NUMBERED.match(l)
                items.append((len(m.group(1)), m.group(2), m.group(3)))
            out.append(_list(items, stats, cls="marked"))
        else:
            text = "\n".join(buf).strip()
            if text:
                out.append(f"<p>{balance(text)}</p>")
        buf, kind = [], None

    for line in lines:
        k = _classify(line)
        if k != kind:
            flush()
            kind = k
        buf.append(line)
    flush()
    return "\n".join(out)


def restructure(html: str, stats) -> str:
    def repl(m):
        inner = m.group(1)
        if "\n" not in inner:
            return m.group(0)
        return restructure_paragraph(inner, stats)
    return re.sub(r"<p>(.*?)</p>", repl, html, flags=re.S)


# ------------------------------------------------------------ 粗體降噪

BOLD_BLOCK = re.compile(r"<(li|p|td|th)>(.*?)</\1>", re.S)
STRONG = re.compile(r"</?strong>", re.I)


def _plain(s):
    return re.sub(r"<[^>]+>", "", s)


def denoise_bold(html: str, stats, threshold: float = 0.6) -> str:
    """整塊幾乎都粗體時，粗體就不再是重點——把那一塊的粗體拿掉。"""
    def repl(m):
        tag, inner = m.group(1), m.group(2)
        total = len(_plain(inner).strip())
        if total < 12:
            return m.group(0)
        bold = sum(len(_plain(b)) for b in re.findall(r"<strong>(.*?)</strong>", inner, re.S))
        if bold / total < threshold:
            return m.group(0)
        stats["debolded"] += 1
        return f"<{tag}>{STRONG.sub('', inner)}</{tag}>"
    return BOLD_BLOCK.sub(repl, html)


# ------------------------------------------------------------ 無損檢查

MARKERS = re.compile(r"[-－|:\s]")


def fingerprint(html: str) -> str:
    """把標記與結構符號都拿掉，只留內容字元，用來確認一個字都沒少。"""
    text = re.sub(r"<[^>]+>", "", html)
    text = text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    text = text.replace("&quot;", '"').replace("&#39;", "'").replace("&nbsp;", " ")
    return MARKERS.sub("", text)
