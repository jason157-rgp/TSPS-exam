# -*- coding: utf-8 -*-
"""產生 notes/ 底下的靜態頁面。用法： python3 build.py"""
import os, sys, json, html, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
from data import SITE_TITLE, SITE_SUB, DOMAINS, NOTES

CSS = """
:root{--green:#4A7C59;--forest:#2C4A38;--steel:#6B7B8D;--pale:#A8D5B5;--amber:#C99A3B;
--bg:#F4F6F3;--ink:#22322A;--rightbg:#E9F5EC;--line:#E1E7E0;--card:#fff;--red:#B4483C}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang TC","Noto Sans TC",sans-serif;
background:var(--bg);color:var(--ink);line-height:1.68;-webkit-text-size-adjust:100%}
.wrap{max-width:940px;margin:0 auto;padding:20px 16px 70px}
a{color:var(--green)}
header.hd{background:linear-gradient(135deg,#2C4A38,#3E6B4E);color:#fff;border-radius:18px;padding:24px 22px;
box-shadow:0 6px 22px rgba(44,74,56,.22)}
header.hd h1{margin:0 0 4px;font-size:22px;letter-spacing:.5px}
header.hd .sub{opacity:.85;font-size:13.5px}
header.hd .crumb{font-size:12px;opacity:.8;margin-bottom:10px}
header.hd .crumb a{color:#DCEFE2;text-decoration:none}
header.hd .crumb a:hover{text-decoration:underline}
.stats{display:flex;gap:10px;flex-wrap:wrap;margin-top:16px}
.stat{background:rgba(255,255,255,.13);border:1px solid rgba(255,255,255,.18);border-radius:12px;padding:9px 14px;flex:1;min-width:88px}
.stat b{display:block;font-size:22px;font-weight:800;line-height:1.15}
.stat span{font-size:11.5px;opacity:.82}
.hdlinks{margin-top:14px;display:flex;gap:8px;flex-wrap:wrap}
.hdlinks a{background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.2);color:#fff;text-decoration:none;
font-size:12.5px;padding:6px 12px;border-radius:20px}
.hdlinks a:hover{background:rgba(255,255,255,.24)}
/* search */
.searchbox{margin:20px 0 6px;position:relative}
.searchbox input{width:100%;padding:13px 15px 13px 40px;border:1px solid var(--line);border-radius:13px;
font-size:15px;background:#fff;color:var(--ink);font-family:inherit}
.searchbox input:focus{outline:none;border-color:var(--pale);box-shadow:0 0 0 3px rgba(168,213,181,.35)}
.searchbox .ic{position:absolute;left:14px;top:50%;transform:translateY(-50%);opacity:.45;font-size:15px}
.hint{font-size:11.5px;color:var(--steel);margin:0 0 4px 2px}
/* sections */
section{margin-top:24px}
section h2{font-size:13.5px;color:var(--green);font-weight:800;margin:0 0 11px;padding-left:10px;
border-left:4px solid var(--pale);letter-spacing:1px;display:flex;align-items:center;gap:8px}
section h2 .n{color:var(--steel);font-weight:600;font-size:11.5px;letter-spacing:0}
.grid{display:grid;grid-template-columns:1fr;gap:11px}
@media(min-width:720px){.grid{grid-template-columns:1fr 1fr}}
.ncard{display:block;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 15px;
text-decoration:none;color:inherit;transition:transform .12s,box-shadow .12s,border-color .12s}
.ncard:hover{transform:translateY(-2px);box-shadow:0 8px 22px rgba(44,74,56,.13);border-color:var(--pale)}
.ncard .top{display:flex;align-items:flex-start;gap:10px}
.badge{flex:none;min-width:42px;height:24px;padding:0 8px;border-radius:8px;background:var(--forest);color:#fff;
font-weight:800;font-size:11px;display:flex;align-items:center;justify-content:center;letter-spacing:.5px}
.ncard .ttl{font-weight:800;font-size:15.5px;line-height:1.4;flex:1}
.ncard .key{font-size:12.5px;color:var(--steel);margin-top:7px;line-height:1.6}
.ncard .sb{font-size:11px;color:#93A29A;margin-top:6px}
.noresult{display:none;text-align:center;color:var(--steel);font-size:13px;padding:30px 0}
/* toc */
.toc{background:#fff;border:1px solid var(--line);border-radius:14px;padding:13px 16px;margin-top:20px}
.toc b{font-size:12px;color:var(--green);letter-spacing:1px}
.toc ol{margin:8px 0 0;padding-left:20px}
.toc li{margin:3px 0;font-size:13.5px}
.toc a{text-decoration:none}
.toc a:hover{text-decoration:underline}
/* note article */
article.note{background:#fff;border:1px solid var(--line);border-radius:16px;padding:20px 20px 18px;margin-top:18px;
scroll-margin-top:14px}
article.note>h3{margin:0;font-size:19px;line-height:1.5;display:block}
article.note>h3 .num{margin-right:9px}
@media(max-width:640px){article.note{padding:17px 15px 15px}article.note>h3{font-size:17.5px}}
article.note>h3 .num{display:inline-block;color:#fff;background:var(--green);font-size:12px;font-weight:800;
border-radius:7px;padding:1px 8px;vertical-align:2px}
article.note>h3 a.anchor{font-size:14px;color:#C3CFC7;text-decoration:none;font-weight:400}
article.note>h3 a.anchor:hover{color:var(--green)}
.subtag{font-size:11.5px;color:var(--steel);margin-top:7px}
.keyline{background:var(--rightbg);border:1px solid #D5E7DB;border-radius:11px;padding:10px 13px;
font-size:13.5px;margin:13px 0 4px;color:#2B5340}
.keyline b{color:var(--forest)}
article.note h4{font-size:14.5px;color:var(--forest);margin:20px 0 8px;padding-bottom:5px;border-bottom:1px dashed var(--line)}
article.note p{margin:11px 0;font-size:14.5px}
article.note ul,article.note ol{margin:11px 0;padding-left:23px;font-size:14.5px}
article.note li{margin:5px 0}
.tw{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:14px 0;border:1px solid var(--line);border-radius:12px;
position:relative;background:linear-gradient(to right,#fff 30%,rgba(255,255,255,0)),
linear-gradient(to right,rgba(255,255,255,0),#fff 70%) 100% 0,
radial-gradient(farthest-side at 0 50%,rgba(44,74,56,.14),rgba(0,0,0,0)),
radial-gradient(farthest-side at 100% 50%,rgba(44,74,56,.14),rgba(0,0,0,0)) 100% 0;
background-repeat:no-repeat;background-size:36px 100%,36px 100%,14px 100%,14px 100%;background-attachment:local,local,scroll,scroll}
.swipe{display:none;font-size:11.5px;color:var(--steel);margin:-8px 0 12px 2px}
@media(max-width:700px){.swipe.on{display:block}}
table{border-collapse:collapse;width:100%;font-size:13.5px;background:#fff;min-width:520px}
th{background:#EEF4F0;color:var(--forest);font-weight:800;text-align:left;padding:9px 11px;
border-bottom:2px solid var(--line);font-size:12.5px;white-space:nowrap}
td{padding:9px 11px;border-bottom:1px solid #F0F3F1;vertical-align:top;line-height:1.62}
tr:last-child td{border-bottom:none}
tbody tr:nth-child(even){background:#FBFCFB}
td:first-child{white-space:nowrap}
@media(max-width:640px){td:first-child{white-space:normal}}
.ins{color:#5C6B62;font-size:.94em}
.co{border-radius:12px;padding:11px 14px;margin:14px 0;font-size:13.8px;line-height:1.68}
.co.star{background:#FFF8E8;border:1px solid #F0DFB4;border-left:4px solid var(--amber)}
.co.trap{background:#FDEEEC;border:1px solid #F3D2CD;border-left:4px solid var(--red)}
.co.note{background:var(--rightbg);border:1px solid #D5E7DB;border-left:4px solid var(--green)}
.co .lb{display:block;font-size:11px;font-weight:800;letter-spacing:1px;margin-bottom:4px;opacity:.85}
.co.star .lb{color:#8A6A1E}.co.trap .lb{color:#93372C}.co.note .lb{color:var(--forest)}
figure{margin:16px 0}
figure img{width:100%;height:auto;display:block;border:1px solid var(--line);border-radius:12px;background:#fff;cursor:zoom-in}
figcaption{font-size:12px;color:var(--steel);margin-top:7px;line-height:1.6}
.lnk{display:inline-flex;align-items:center;gap:7px;background:var(--rightbg);border:1px solid #D5E7DB;
border-radius:10px;padding:9px 13px;text-decoration:none;font-size:13.5px;font-weight:700;margin:6px 0}
.lnk:hover{background:#DDEEE3}
.rel{margin-top:16px;padding-top:12px;border-top:1px dashed var(--line);font-size:12.5px;color:var(--steel)}
.rel b{color:var(--green);letter-spacing:1px;font-size:11px}
.rel a{display:inline-block;background:#F3F7F4;border:1px solid var(--line);border-radius:18px;padding:3px 11px;
margin:5px 5px 0 0;text-decoration:none;font-size:12.5px}
.rel a:hover{border-color:var(--pale);background:var(--rightbg)}
/* nav */
.pager{display:flex;gap:10px;margin-top:26px;flex-wrap:wrap}
.pager a{flex:1;min-width:150px;background:#fff;border:1px solid var(--line);border-radius:13px;padding:12px 14px;
text-decoration:none;color:inherit;font-size:13px}
.pager a:hover{border-color:var(--pale);box-shadow:0 6px 16px rgba(44,74,56,.1)}
.pager .lb{display:block;font-size:10.5px;color:var(--steel);letter-spacing:1px;margin-bottom:2px}
.pager .nm{font-weight:800;color:var(--forest)}
.pager a.nx{text-align:right}
.tip{margin-top:24px;font-size:12px;color:var(--steel);background:#fff;border:1px dashed var(--line);
border-radius:12px;padding:13px 15px;line-height:1.75}
.tip b{color:var(--green)}
footer{margin-top:24px;text-align:center;font-size:11px;color:#9AA79E}
.btop{position:fixed;right:16px;bottom:16px;width:42px;height:42px;border-radius:50%;background:var(--forest);
color:#fff;border:none;font-size:17px;box-shadow:0 4px 14px rgba(44,74,56,.3);cursor:pointer;display:none;z-index:40}
/* lightbox */
#lb{position:fixed;inset:0;background:rgba(20,30,24,.92);display:none;align-items:center;justify-content:center;
z-index:90;padding:16px;cursor:zoom-out}
#lb img{max-width:100%;max-height:100%;border-radius:8px}
@media print{
 body{background:#fff}.btop,.searchbox,.hdlinks,.pager{display:none!important}
 article.note{break-inside:avoid;box-shadow:none;border-color:#ccc}
 header.hd{background:#2C4A38!important;-webkit-print-color-adjust:exact;print-color-adjust:exact}
}
"""

JS_COMMON = """
(function(){
 var b=document.createElement('button');b.className='btop';b.innerHTML='↑';b.title='回到頂端';
 b.onclick=function(){window.scrollTo({top:0,behavior:'smooth'})};document.body.appendChild(b);
 window.addEventListener('scroll',function(){b.style.display=window.scrollY>420?'block':'none'});
 var lb=document.createElement('div');lb.id='lb';lb.innerHTML='<img alt="">';document.body.appendChild(lb);
 lb.onclick=function(){lb.style.display='none'};
 document.addEventListener('keydown',function(e){if(e.key==='Escape')lb.style.display='none'});
 document.querySelectorAll('figure img').forEach(function(im){
   im.onclick=function(){lb.querySelector('img').src=im.src;lb.style.display='flex'};});
})();
"""

def esc(s): return html.escape(s, quote=False)

def render_blocks(blocks):
    o = []
    for b in blocks:
        t = b["t"]
        if t == "p":
            o.append("<p>%s</p>" % b["html"])
        elif t == "h":
            o.append("<h4>%s</h4>" % b["html"])
        elif t == "ul":
            o.append("<ul>%s</ul>" % "".join("<li>%s</li>" % i for i in b["items"]))
        elif t == "ol":
            o.append("<ol>%s</ol>" % "".join("<li>%s</li>" % i for i in b["items"]))
        elif t == "table":
            th = "".join("<th>%s</th>" % h for h in b["head"])
            rows = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % c for c in r) for r in b["rows"])
            o.append('<div class="tw"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % (th, rows))
            if len(b["head"]) >= 4:
                o.append('<div class="swipe on">← 表格可左右滑動 →</div>')
        elif t == "img":
            o.append('<figure><img src="%s" alt="%s" loading="lazy"><figcaption>%s</figcaption></figure>'
                     % (b["src"], esc(b.get("cap", "")[:90]), b.get("cap", "")))
        elif t == "callout":
            lb = {"star": "⭐ 記憶錨點", "trap": "🚨 考場地雷", "note": "📌 補充"}[b["kind"]]
            o.append('<div class="co %s"><span class="lb">%s</span>%s</div>' % (b["kind"], lb, b["html"]))
        elif t == "linkout":
            o.append('<a class="lnk" href="%s" target="_blank" rel="noopener">🔗 %s ↗</a>'
                     % (b["href"], esc(b["text"])))
        else:
            raise ValueError("unknown block " + t)
    return "\n".join(o)

def page(title, body, extra_js=""):
    return ("""<!DOCTYPE html><html lang="zh-Hant"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#2C4A38">
<title>%s</title>
<style>%s</style></head><body>
<div class="wrap">
%s
</div>
<script>%s%s</script>
</body></html>""" % (esc(title), CSS, body, JS_COMMON, extra_js))

DMAP = {d["code"]: d for d in DOMAINS}
BY_DOMAIN = {d["code"]: [n for n in NOTES if n["domain"] == d["code"]] for d in DOMAINS}
NOTE_BY_ID = {n["id"]: n for n in NOTES}

def note_url(nid, from_index=False):
    n = NOTE_BY_ID[nid]
    return "%s#%s" % (DMAP[n["domain"]]["file"], nid)

# ── 索引頁 ──────────────────────────────────────────────────────────
def build_index():
    secs = []
    for d in DOMAINS:
        ns = BY_DOMAIN[d["code"]]
        if not ns: continue
        cards = []
        for n in ns:
            cards.append("""<a class="ncard" href="%s" data-s="%s">
  <div class="top"><span class="badge">%s</span><span class="ttl">%s</span></div>
  <div class="key">%s</div><div class="sb">%s</div></a>""" % (
                note_url(n["id"]), esc((n["title"] + " " + n["key"] + " " + n.get("sub", "")).lower()),
                d["code"], esc(n["title"]), n["key"], esc(n.get("sub", ""))))
        secs.append("""<section data-dom="%s"><h2>%s <span class="n">%s · %d 則</span></h2>
<div class="grid">%s</div></section>""" % (d["code"], esc(d["name"]), d["code"], len(ns), "".join(cards)))

    body = """<header class="hd">
  <h1>%s</h1>
  <div class="sub">%s</div>
  <div class="stats">
    <div class="stat"><b>%d</b><span>則筆記</span></div>
    <div class="stat"><b>%d</b><span>領域</span></div>
    <div class="stat"><b>%d</b><span>對照表</span></div>
    <div class="stat"><b>%d</b><span>圖解</span></div>
  </div>
  <div class="hdlinks"><a href="../index.html">← 回題庫總覽</a><a href="../finalsprint.html">最後衝刺</a></div>
</header>

<div class="searchbox"><span class="ic">🔍</span>
  <input id="q" type="search" placeholder="搜尋筆記標題、重點、子類…" autocomplete="off"></div>
<div class="hint">輸入關鍵字即時過濾；點卡片直接跳到該則筆記。</div>

%s
<div class="noresult" id="nr">沒有符合的筆記。</div>

<div class="tip">
  <b>怎麼用：</b>這裡只放「反覆記不住」的點，依九領域題庫的代碼分類。每則筆記底部有「相關筆記」可以互跳。<br>
  <b>加新筆記：</b>編輯 <code>notes/_build/data.py</code>，執行 <code>python3 build.py</code> 即可重新產生全部頁面。<br>
  <b>離線：</b>整站為純靜態 HTML，存到手機書籤或加入主畫面即可離線翻閱（圖片需先載入過）。
</div>
<footer>%s · 共 %d 則</footer>""" % (
        esc(SITE_TITLE), esc(SITE_SUB), len(NOTES), len([d for d in DOMAINS if BY_DOMAIN[d["code"]]]),
        sum(1 for n in NOTES for b in n["blocks"] if b["t"] == "table"),
        sum(1 for n in NOTES for b in n["blocks"] if b["t"] == "img"),
        "\n".join(secs), esc(SITE_TITLE), len(NOTES))

    js = """
var q=document.getElementById('q'),nr=document.getElementById('nr');
q.addEventListener('input',function(){
  var v=q.value.trim().toLowerCase(),hit=0;
  document.querySelectorAll('section[data-dom]').forEach(function(s){
    var c=0;
    s.querySelectorAll('.ncard').forEach(function(a){
      var ok=!v||a.dataset.s.indexOf(v)>-1;a.style.display=ok?'':'none';if(ok)c++;});
    s.style.display=c?'':'none';hit+=c;});
  nr.style.display=hit?'none':'block';});
"""
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(
        page(SITE_TITLE + " · 索引", body, js))

# ── 領域頁 ──────────────────────────────────────────────────────────
def build_domain(d, prev_d, next_d):
    ns = BY_DOMAIN[d["code"]]
    toc = "".join('<li><a href="#%s">%s</a></li>' % (n["id"], esc(n["title"])) for n in ns)
    arts = []
    for i, n in enumerate(ns, 1):
        rel = ""
        if n["related"]:
            links = "".join('<a href="%s">%s</a>' % (note_url(r), esc(NOTE_BY_ID[r]["title"])) for r in n["related"])
            rel = '<div class="rel"><b>相關筆記</b><br>%s</div>' % links
        arts.append("""<article class="note" id="%s">
  <h3><span class="num">%02d</span>%s<a class="anchor" href="#%s" title="複製此段連結">§</a></h3>
  <div class="subtag">%s · %s</div>
  <div class="keyline">%s</div>
  %s
  %s
</article>""" % (n["id"], i, esc(n["title"]), n["id"], d["code"], esc(n.get("sub", "")),
                 n["key"], render_blocks(n["blocks"]), rel))

    pager = []
    if prev_d:
        pager.append('<a class="pv" href="%s"><span class="lb">← 上一領域</span><span class="nm">%s</span></a>'
                     % (prev_d["file"], esc(prev_d["name"])))
    if next_d:
        pager.append('<a class="nx" href="%s"><span class="lb">下一領域 →</span><span class="nm">%s</span></a>'
                     % (next_d["file"], esc(next_d["name"])))

    body = """<header class="hd">
  <div class="crumb"><a href="index.html">%s</a> ／ %s</div>
  <h1>%s</h1>
  <div class="sub">%s · 共 %d 則易忘點</div>
  <div class="hdlinks"><a href="index.html">← 筆記索引</a><a href="%s">%s 題庫 App</a><a href="../index.html">題庫總覽</a></div>
</header>

<div class="toc"><b>本頁目錄</b><ol>%s</ol></div>

%s

<div class="pager">%s</div>
<footer>%s · %s</footer>""" % (
        esc(SITE_TITLE), esc(d["name"]), esc(d["name"]), d["code"], len(ns),
        d["bank"], d["code"], toc, "\n".join(arts), "".join(pager), esc(SITE_TITLE), esc(d["name"]))

    js = """
document.querySelectorAll('a.anchor').forEach(function(a){
  a.addEventListener('click',function(e){
    var u=location.href.split('#')[0]+a.getAttribute('href');
    if(navigator.clipboard){navigator.clipboard.writeText(u).then(function(){
      var o=a.textContent;a.textContent='✓';setTimeout(function(){a.textContent=o},900);});}
  });});
"""
    open(os.path.join(OUT, d["file"]), "w", encoding="utf-8").write(
        page("%s · %s" % (SITE_TITLE, d["name"]), body, js))

def sync_root_index():
    """同步根目錄 index.html 上「記不住的東西」卡片的數字。"""
    import re
    p = os.path.abspath(os.path.join(OUT, "..", "index.html"))
    if not os.path.exists(p): return
    s = open(p, encoding="utf-8").read()
    if "notes/index.html" not in s: return
    n = len(NOTES); dn = len([d for d in DOMAINS if BY_DOMAIN[d["code"]]])
    s2 = re.sub(r'(<b data-notes-count>)\d+(</b>)', r'\g<1>%d\g<2>' % n, s)
    s2 = re.sub(r'(<span data-notes-domains>)\d+(</span>)', r'\g<1>%d\g<2>' % dn, s2)
    if s2 != s:
        open(p, "w", encoding="utf-8").write(s2); print("synced root index.html")

def main():
    active = [d for d in DOMAINS if BY_DOMAIN[d["code"]]]
    build_index()
    sync_root_index()
    for i, d in enumerate(active):
        build_domain(d, active[i-1] if i > 0 else None, active[i+1] if i < len(active)-1 else None)
    print("built: index.html + %s" % ", ".join(d["file"] for d in active))

if __name__ == "__main__":
    main()
