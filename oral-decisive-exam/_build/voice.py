#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
語音課程頁（voice/）

_build/scripts/ 放 12 集講稿的純文字原稿（逐字，未經改寫）。這裡把它們
排成語意化的靜態網頁，讓 Safari 的「朗讀螢幕」可以從頭唸到尾。

排版的重點只有兩個：
  1. 內容在 DOM 裡就是朗讀順序，只有 h1／h2／p，沒有任何要靠 JS 才出現
     的文字，所以朗讀工具讀得到、也照得亮。
  2. 講稿裡的三行「（停頓）」是要你自己作答的三秒，不是要唸出來的字。
     預設把它換成一段省略號──畫面上看得到「停 3 秒」的提示，唸出來
     則是一段停頓。真的想聽到「停頓」兩個字，頁面上可以切換。
"""
import html as H
import re
from pathlib import Path

PAUSE = "（停頓）"

# 每一行開頭長什麼樣，就歸到哪一類。順序有意義，先比對到的先算。
KINDS = [
    ("cue",   re.compile(r"^先自己講一遍")),
    ("ask",   re.compile(r"^考官問：")),
    ("ans",   re.compile(r"^標準答案")),
    ("trap",  re.compile(r"^地雷或加分句")),
    ("next",  re.compile(r"^下一集")),
]
# 這些自成一段，行首那一小截當標題
BLOCKS = [
    ("sum",   re.compile(r"^(小結[一二三四五六七八九十]*)。\s*(.*)$")),
    ("sum",   re.compile(r"^(本集範圍)。\s*(.*)$")),
    ("recap", re.compile(r"^((?:最後 60 秒，)?必背數字快速複習[^。]*)。?\s*(.*)$")),
    ("recap", re.compile(r"^(上場前最後叮嚀[^。]*)。?\s*(.*)$")),
]
Q_HEAD = re.compile(r"^第([一二三四五六七八九十]+)題。\s*(.*)$")
TITLE = re.compile(r"^(?:第[一二三四五六七八九十]+集[，、]|EP\d+\s*)\s*(.*?)[。]?$")

CSS = """
:root{
  --ink:#141a18; --muted:#66736f; --rule:#dfe6e3; --surface:#fff; --bg:#f6f8f7;
  --accent:#0f6b5c; --accent-soft:#e6f1ee; --accent-ink:#0b5145; --warn:#8a4b16;
  --warn-soft:#fdf1e4;
  --fs:19px;
}
@media (prefers-color-scheme:dark){
  :root{ --ink:#e8eeec; --muted:#93a19d; --rule:#2b3634; --surface:#151d1b; --bg:#0e1413;
    --accent:#5ec4ae; --accent-soft:#17302b; --accent-ink:#8fdcc9;
    --warn:#e0a86a; --warn-soft:#2c2114; }
}
*{box-sizing:border-box}
body{margin:0; background:var(--bg); color:var(--ink);
  font-family:system-ui,-apple-system,"PingFang TC","Noto Sans TC",sans-serif;
  font-size:var(--fs); line-height:1.95;
  -webkit-text-size-adjust:100%;}
.wrap{max-width:40rem; margin:0 auto; padding:0 1.1rem 5rem}
a{color:var(--accent-ink)}
.top{position:sticky; top:0; z-index:5; background:var(--bg);
  border-bottom:1px solid var(--rule); margin-bottom:1.6rem}
.topin{max-width:40rem; margin:0 auto; padding:.55rem 1.1rem;
  display:flex; gap:.5rem; align-items:center; flex-wrap:wrap}
.topin a.back{font-size:.78em; text-decoration:none; color:var(--muted); margin-right:auto}
.topin a.back:hover{color:var(--accent-ink)}
button.t{font:inherit; font-size:.72em; line-height:1.5; padding:.15rem .6rem;
  border:1px solid var(--rule); border-radius:20px; background:var(--surface);
  color:var(--muted); cursor:pointer}
button.t:hover{border-color:var(--accent); color:var(--accent-ink)}
button.t[aria-pressed="true"]{background:var(--accent-soft); color:var(--accent-ink);
  border-color:var(--accent)}
h1{font-size:1.5em; line-height:1.55; margin:1.2rem 0 .3rem; letter-spacing:-.01em}
.sub{color:var(--muted); font-size:.78em; margin:0 0 1.8rem}
h2{font-size:1.08em; line-height:1.5; margin:0 0 .7rem; color:var(--accent-ink)}
p{margin:0 0 1.05rem}
section{margin:0 0 2.4rem; scroll-margin-top:4rem}
section.q{border-top:1px solid var(--rule); padding-top:1.6rem}
.ask{font-weight:600}
.cue{color:var(--muted); font-size:.85em; margin-bottom:.5rem}
.trap{background:var(--warn-soft); border-left:3px solid var(--warn);
  padding:.85rem 1rem; border-radius:0 6px 6px 0; margin:0 0 1.05rem}
.sum,.recap{background:var(--accent-soft); border-radius:8px; padding:1.1rem 1.1rem .3rem}
.sum h2,.recap h2{margin-top:0}
.next{color:var(--muted); font-size:.85em}

/* 停頓：畫面上是提示，唸出來是一段空白 */
.pause{margin:.2rem 0 1.4rem; color:var(--muted); font-size:.85em;
  border-left:3px solid var(--rule); padding-left:.9rem}
.pause::before{content:"⏸　停 3 秒　"}
.pause .quiet{opacity:.5; letter-spacing:.16em}
.pause .loud{display:none}
body.loud .pause::before{content:"⏸　"}
body.loud .pause .quiet{display:none}
body.loud .pause .loud{display:inline; font-size:1em; line-height:inherit}

/* 集內題目導覽 */
.qnav{border:1px solid var(--rule); background:var(--surface); border-radius:10px;
  padding:.9rem 1.1rem; margin:0 0 2.4rem; font-size:.85em}
.qnav b{display:block; font-size:.9em; color:var(--muted); font-weight:600;
  letter-spacing:.06em; margin-bottom:.5rem}
.qnav ol{margin:0; padding-left:1.4rem}
.qnav li{margin:0 0 .35rem; line-height:1.6}
.pager{display:flex; gap:.8rem; border-top:1px solid var(--rule); padding-top:1.2rem;
  font-size:.85em}
.pager .r{margin-left:auto}

/* 目錄頁 */
ul.eps{list-style:none; margin:0; padding:0}
ul.eps li{border-bottom:1px solid var(--rule)}
ul.eps a{display:block; padding:.95rem .2rem; text-decoration:none; color:var(--ink)}
ul.eps a:hover{background:var(--accent-soft)}
ul.eps .n{font-size:.72em; color:var(--muted); letter-spacing:.08em}
ul.eps .t{display:block; line-height:1.5}
ul.eps .m{font-size:.72em; color:var(--muted)}
.howto{background:var(--surface); border:1px solid var(--rule); border-radius:10px;
  padding:1.1rem 1.2rem .3rem; margin:0 0 2.4rem; font-size:.88em}
.howto h2{font-size:1em}
.howto ol{padding-left:1.3rem; margin:0 0 1rem}
.howto li{margin:0 0 .4rem}
"""

JS = """
(function(){
  var b=document.body, K='psoral.voice';
  var cfg={fs:0, loud:false};
  try{ cfg=Object.assign(cfg, JSON.parse(localStorage.getItem(K)||'{}')); }catch(e){}
  function save(){ try{ localStorage.setItem(K, JSON.stringify(cfg)); }catch(e){} }
  function paint(){
    document.documentElement.style.setProperty('--fs', (19+cfg.fs*2)+'px');
    b.classList.toggle('loud', !!cfg.loud);
    var p=document.getElementById('pz');
    if(p){ p.setAttribute('aria-pressed', cfg.loud?'true':'false');
           p.textContent = cfg.loud ? '停頓：唸出來' : '停頓：靜音'; }
  }
  document.addEventListener('click', function(e){
    var t=e.target.closest ? e.target.closest('button.t') : null;
    if(!t) return;
    if(t.id==='fsup')   { cfg.fs=Math.min(6, cfg.fs+1); }
    else if(t.id==='fsdn'){ cfg.fs=Math.max(-2, cfg.fs-1); }
    else if(t.id==='pz'){ cfg.loud=!cfg.loud; }
    else return;
    save(); paint();
  });
  paint();
})();
"""


def esc(s):
    return H.escape(s, quote=False)


def parse(text):
    """把講稿切成 [(kind, 標題, [段落…])]，順序即朗讀順序。"""
    lines = [l.rstrip() for l in text.split("\n")]
    lines = [l for l in lines if l.strip()]
    title = lines[0]
    m = TITLE.match(title)
    title = m.group(1) if m and m.group(1) else title.rstrip("。")

    blocks, cur = [], None

    def open_block(kind, head):
        nonlocal cur
        cur = {"kind": kind, "head": head, "body": []}
        blocks.append(cur)

    open_block("intro", "")
    i, n = 1, len(lines)
    while i < n:
        line = lines[i]

        if line == PAUSE:                       # 連著幾行併成一個停頓
            while i < n and lines[i] == PAUSE:
                i += 1
            cur["body"].append(("pause", ""))
            continue

        q = Q_HEAD.match(line)
        if q:
            open_block("q", "第" + q.group(1) + "題")
            if q.group(2):
                lines[i] = q.group(2)           # 同一行還有考官問：，留給下一輪
                continue
            i += 1
            continue

        hit = None
        for kind, pat in BLOCKS:
            m = pat.match(line)
            if m:
                hit = (kind, m.group(1), m.group(2))
                break
        if hit:
            open_block(hit[0], hit[1])
            if hit[2]:
                cur["body"].append(("p", hit[2]))
            i += 1
            continue

        cls = "p"
        for kind, pat in KINDS:
            if pat.match(line):
                cls = kind
                break
        cur["body"].append((cls, line))
        i += 1

    blocks = [b for b in blocks if b["body"] or b["head"]]
    return title, blocks


def render_body(blocks):
    out = []
    qn = 0
    for b in blocks:
        kind = b["kind"]
        cls, sid = kind, ""
        if kind == "q":
            qn += 1
            sid = f' id="q{qn}"'
        out.append(f'<section class="{cls}"{sid}>')
        if b["head"]:
            out.append(f"<h2>{esc(b['head'])}</h2>")
        for c, t in b["body"]:
            if c == "pause":
                out.append('<p class="pause"><span class="quiet">'
                           '……　……　……　……</span>'
                           f'<span class="loud">{PAUSE}{PAUSE}{PAUSE}</span></p>')
            else:
                klass = f' class="{c}"' if c != "p" else ""
                out.append(f"<p{klass}>{esc(t)}</p>")
        out.append("</section>")
    return "\n".join(out)


def q_nav(blocks):
    """集內題目清單：把每題的第一句考官問當標題。"""
    items, qn = [], 0
    for b in blocks:
        if b["kind"] != "q":
            continue
        qn += 1
        ask = next((t for c, t in b["body"] if c == "ask"), "")
        ask = re.sub(r"^考官問：", "", ask).strip()
        if len(ask) > 40:
            ask = ask[:39] + "…"
        items.append(f'<li><a href="#q{qn}">{esc(ask) or b["head"]}</a></li>')
    if not items:
        return ""
    return ('<nav class="qnav"><b>本集題目</b><ol>' + "".join(items) + "</ol></nav>")


def page(title, body, head_extra="", cls=""):
    return (
        '<!doctype html>\n<html lang="zh-Hant">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        f"<title>{esc(title)}</title>\n<style>{CSS}</style>\n</head>\n"
        f'<body{f" class={chr(34)}{cls}{chr(34)}" if cls else ""}>\n'
        f"{head_extra}\n<main class=\"wrap\">\n{body}\n</main>\n"
        f"<script>{JS}</script>\n</body>\n</html>\n"
    )


def toolbar(back_href, back_label):
    return ('<div class="top"><div class="topin">'
            f'<a class="back" href="{back_href}">← {esc(back_label)}</a>'
            '<button class="t" type="button" id="fsdn">小</button>'
            '<button class="t" type="button" id="fsup">大</button>'
            '<button class="t" type="button" id="pz" aria-pressed="false">停頓：靜音</button>'
            "</div></div>")


HOWTO = """<div class="howto">
<h2>用 Safari 朗讀</h2>
<ol>
<li>先到「設定 → 輔助使用 → 朗讀內容」，打開<b>朗讀螢幕</b>，順便把速度調到你聽得舒服的位置。</li>
<li>打開任何一集，<b>從螢幕最上緣往下滑兩指</b>，就會從頭開始唸。</li>
<li>浮動控制列可以暫停、加速、跳段落。想從某一題開始，先點那一題再兩指下滑。</li>
<li>畫面上的 <b>⏸ 停 3 秒</b> 是留給你自己作答的，唸到那裡會停一下。想改成把「停頓」兩個字唸出來，按上面的「停頓：靜音」切換。</li>
</ol>
<p>這 12 集是逐字稿原文，沒有改寫。</p>
</div>"""


def emit(src_dir: Path, outdir: Path):
    files = sorted(src_dir.glob("EP*.txt"))
    if not files:
        return 0, 0
    outdir.mkdir(parents=True, exist_ok=True)
    for old in outdir.glob("*.html"):
        old.unlink()

    eps = []
    for f in files:
        title, blocks = parse(f.read_text(encoding="utf-8"))
        num = f.name[:4].upper()                    # EP01
        nq = sum(1 for b in blocks if b["kind"] == "q")
        chars = sum(len(t) for b in blocks for _c, t in b["body"])
        eps.append({"file": f"{num.lower()}.html", "num": num, "title": title,
                    "blocks": blocks, "nq": nq, "chars": chars})

    total_q = 0
    for i, e in enumerate(eps):
        total_q += e["nq"]
        nav = ['<div class="pager">']
        if i:
            nav.append(f'<a href="{eps[i-1]["file"]}">← 上一集</a>')
        nav.append('<a href="index.html" class="r">全部 12 集</a>'
                   if i == len(eps) - 1 else
                   f'<a href="{eps[i+1]["file"]}" class="r">下一集 →</a>')
        nav.append("</div>")
        mins = round(e["chars"] / 260)              # 中文朗讀約每分鐘 260 字
        body = (f'<h1>{esc(e["num"])}　{esc(e["title"])}</h1>\n'
                f'<p class="sub">{e["nq"]} 題　·　約 {e["chars"]//1000}k 字　·　'
                f'朗讀約 {mins} 分鐘</p>\n'
                + q_nav(e["blocks"]) + "\n"
                + render_body(e["blocks"]) + "\n" + "".join(nav))
        (outdir / e["file"]).write_text(
            page(f'{e["num"]} {e["title"]}', body,
                 toolbar("index.html", "12 集語音課程")),
            encoding="utf-8")

    rows = []
    for e in eps:
        mins = round(e["chars"] / 260)
        rows.append(
            f'<li><a href="{e["file"]}"><span class="n">{esc(e["num"])}</span>'
            f'<span class="t">{esc(e["title"])}</span>'
            f'<span class="m">{e["nq"]} 題　·　朗讀約 {mins} 分鐘</span></a></li>')
    total_min = round(sum(e["chars"] for e in eps) / 260)
    idx = (f'<h1>12 集語音課程</h1>\n'
           f'<p class="sub">{len(eps)} 集　·　{total_q} 題　·　'
           f'全部聽完約 {total_min // 60} 小時 {total_min % 60} 分</p>\n'
           + HOWTO + '\n<ul class="eps">' + "".join(rows) + "</ul>")
    (outdir / "index.html").write_text(
        page("12 集語音課程", idx, toolbar("../index.html", "回作戰室")),
        encoding="utf-8")

    return len(eps), total_q


if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent
    n, q = emit(root / "_build" / "scripts", root / "voice")
    print(f"[voice] {n} 集、{q} 題")
