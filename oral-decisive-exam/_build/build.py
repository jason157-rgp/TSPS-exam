#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
整專口試作戰室 —— 索引與導覽重建

輸入：_build/source.html（自 artifact 匯出的原始單頁，勿手改）
輸出：index.html

做四件事：
  1. 統一領域分類：12 個領域貫穿主題軸與考官軸（原本三套：11 / 6 / 26）
  2. 章號可視化：考官軸依 Ch.A–E 分組，與索引裡「D 章〔陳天牧〕」的寫法對齊
  3. 全書交叉參照連結化：〔考官名〕與「X 章 §N」變成可點的跳轉
  4. 第一部索引重建：11 張分散表格 → 單一可篩選清單，91 列全部可點

重跑： python3 _build/build.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "_build" / "source.html"
OUT = ROOT / "index.html"

# ---------------------------------------------------------------- 領域定義

DOMAINS = [
    ("d1", "顱顏與顏面外傷"),
    ("d2", "眼整形"),
    ("d3", "手外科與周邊神經"),
    ("d4", "顯微重建"),
    ("d5", "乳房"),
    ("d6", "燒傷"),
    ("d7", "傷口與壓瘡"),
    ("d8", "皮膚腫瘤與局部皮瓣"),
    ("d9", "血管異常與淋巴"),
    ("d10", "唾液腺與顏面神經"),
    ("d11", "美容"),
    ("d12", "基本原則與倫理"),
]
DOMAIN_LABEL = dict(DOMAINS)

# 考官 tag（26 個）→ 領域。四個非領域的 tag 另外歸為「關卡性質」。
TAG2DOM = {
    "顱顏": "d1", "外傷評估": "d1",
    "眼整形": "d2",
    "手外科": "d3", "周邊神經": "d3", "先天手畸形": "d3",
    "顯微重建": "d4", "下肢重建": "d4", "肢體重建": "d4", "VCA": "d4",
    "乳房": "d5",
    "燒傷": "d6",
    "傷口壓瘡": "d7",
    "皮膚腫瘤": "d8", "局部皮瓣": "d8",
    "血管異常": "d9", "淋巴水腫": "d9",
    "唾液腺": "d10", "顏面神經": "d10",
    "美容": "d11",
    "基本原則": "d12", "倫理溝通": "d12",
}
STATIONS = ["魔王關", "聊天關", "跨領域", "未任考官"]

# 主題節 → 領域。tc/to/th 整組對應；tm/tb/tp 需要拆。
TOPIC_SPLIT = {
    "tm": [(range(98, 105), "d5"), (range(94, 95), "d9")],          # 其餘 d4
    "tb": [(range(115, 127), "d7"), (range(127, 137), "d9")],       # 其餘 d6
    "tp": [(range(150, 151), "d11"), (range(155, 158), "d11"),
           (range(151, 155), "d10"), (range(158, 162), "d12")],     # 其餘 d8
}
TOPIC_BASE = {"tc": "d1", "to": "d2", "th": "d3",
              "tm": "d4", "tb": "d6", "tp": "d8"}

# ------------------------------------------------------------ 章節（Ch.A–E）

CHAPTERS = [
    ("chA", "A", "Ch.A｜2025 第一批", ["s27", "s28", "s29", "s30", "s31", "s32", "s33"]),
    ("chB", "B", "Ch.B｜2025 第二批", ["s34", "s35", "s36", "s37", "s38", "s39", "s40", "s41", "s42"]),
    ("chC", "C", "Ch.C｜2025 第三批", ["s43", "s44", "s45", "s46", "s47", "s48", "s49", "s50"]),
    ("chD", "D", "Ch.D｜歷年核心（第一批）", ["s51", "s52", "s53", "s54", "s55", "s56"]),
    ("chE", "E", "Ch.E｜歷年核心（第二批）", ["s57", "s58", "s59", "s60", "s61", "s74", "s75"]),
    ("chE5", "E-5", "Ch.E 第五組｜104–105 年其他考官", ["s62", "s63", "s64", "s65", "s66", "s67", "s68"]),
    ("chE6", "E-6", "Ch.E 第六組｜111 年首次入圍", ["s69", "s70", "s71", "s72", "s73"]),
]

# 章內的考官順序，供「C 章 §4」這類參照定位
CH_EX = {
    "A": ["s28", "s29", "s30", "s31", "s32"],
    "B": ["s35", "s36", "s37", "s38", "s39"],
    "C": ["s45", "s46", "s47", "s48", "s49"],
    "D": ["s52", "s53", "s54", "s55"],
    "E": ["s58", "s59", "s60", "s61"],
}
E5 = ["s63", "s64", "s65", "s66", "s67", "s68"]   # E 章「第五組」
E6 = ["s70", "s71", "s72", "s73"]                 # E 章「第六組」
CH_HEAD = {"A": "s27", "B": "s34", "C": "s43", "D": "s51", "E": "s57"}

# ------------------------------------------------- 第一部索引：領域與比對範圍

IDX_SECTIONS = [f"s{i}" for i in range(11, 22)]
IDX_DOMAIN = {
    "s11": "d1", "s12": "d2", "s13": "d3", "s14": "d4", "s15": "d5", "s16": "d6",
    "s17": "d7", "s18": "d8", "s19": "d9", "s20": "d11", "s21": "d12",
}
# 比對主題節時允許的來源組（同領域為主，跨領域者放寬）
IDX_ALLOW = {
    "s11": ["tc"], "s12": ["to"], "s13": ["th"], "s14": ["tm"], "s15": ["tm"],
    "s16": ["tb"], "s17": ["tb"], "s18": ["tp", "tb"], "s19": ["tb", "tm"],
    "s20": ["tp", "to", "tm"], "s21": ["tp", "th", "tm"],
}
# 自動比對會選錯或選不到的，逐筆指定（key 為主題欄的起始片段）
IDX_OVERRIDE = {
    "ZMC fracture 四個 buttress": "tc10",
    "小兒燒傷 fluid resuscitation": "tb107",
    "下眼皮成形術的併發症": "to35",
    "Reconstruction ladder 的階梯思維": "tp158",
    "答不出來時的標準句": "tp161",
    "被問「確定嗎？真的嗎？」": "tp161",
    "自己的手術經驗與案例數": "tp161",
    "MSAP flap": "tm88",
    "Marjolin's ulcer（潛伏期": "tp142",
    "顏面局部皮瓣設計": "tp146",
    "Syndactyly 未完全分開": "th79",
    "神經再生速度與運動終板": "th49",
    "Extramammary Paget's disease": "tp141",
}
MATCH_THRESHOLD = 3


# ---------------------------------------------------------------- 小工具

def strip_tags(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html).strip()


def num_of(sid: str):
    m = re.search(r"(\d+)$", sid)
    return int(m.group(1)) if m else None


def topic_domain(sec) -> str:
    g = sec["group"]
    base = TOPIC_BASE.get(g)
    if base is None:
        return ""
    n = num_of(sec["id"])
    if n is not None:
        for rng, dom in TOPIC_SPLIT.get(g, []):
            if n in rng:
                return dom
    return base


def tokens(text: str):
    low = text.lower()
    en = set(re.findall(r"[a-z][a-z\-]{3,}", low))
    zh = set()
    for word in re.sub(r"[^一-鿿]", " ", low).split():
        for i in range(len(word) - 1):
            zh.add(word[i:i + 2])
    return en, zh


# ------------------------------------------------ 交叉參照 → 可點的跳轉按鈕

def build_linkifier(sections):
    names = {}
    for s in sections:
        if s["axis"] == "examiner":
            names[s["title"].split("　")[-1]] = s["id"]

    pattern = re.compile(
        r"〔(?P<nm>[^〕]{1,8})〕"
        r"|(?P<a>[A-E])\s*章\s*§\s*(?P<an>\d+)"
        r"|(?P<b>[A-E])\s*§\s*(?P<bn>\d+)"
        r"|(?P<c>[A-E])\s*章\s*(?P<cn>\d+)(?:-(?P<cs>\d+))?"
        r"|(?P<d>[A-E])\s*章"
    )

    def by_number(ch, n, sub):
        if ch == "E" and sub:
            grp = E5 if n == 5 else (E6 if n == 6 else None)
            if grp and 1 <= int(sub) <= len(grp):
                return grp[int(sub) - 1]
            return None
        if not sub and 1 <= n <= len(CH_EX.get(ch, [])):
            return CH_EX[ch][n - 1]
        return None

    def jump(target, label):
        return f'<button type="button" class="jump" data-go="{target}">{label}</button>'

    def repl(m):
        raw = m.group(0)
        if m.group("nm") is not None:
            tid = names.get(m.group("nm"))
            return f"〔{jump(tid, m.group('nm'))}〕" if tid else raw
        if m.group("a"):
            tid = by_number(m.group("a"), int(m.group("an")), None)
        elif m.group("b"):
            tid = by_number(m.group("b"), int(m.group("bn")), None)
        elif m.group("c"):
            tid = by_number(m.group("c"), int(m.group("cn")), m.group("cs"))
        else:
            tid = CH_HEAD.get(m.group("d"))
        return jump(tid, raw) if tid else raw

    def linkify(html):
        return pattern.sub(repl, html)

    return linkify, names


# ---------------------------------------------------- 第一部：抽出 91 列索引

def build_index_rows(by_id, sections, linkify, names):
    topics = [s for s in sections if s["axis"] == "topic"]
    rows = []
    unmatched = []

    for sid in IDX_SECTIONS:
        sec = by_id[sid]
        dom = IDX_DOMAIN[sid]
        for tr in re.findall(r"<tr>\s*(.*?)\s*</tr>", sec["html"], re.S):
            tds = re.findall(r"<td>(.*?)</td>", tr, re.S)
            if len(tds) != 4:
                continue
            topic_html, ex_html, level_html, loc_html = tds
            topic_txt = strip_tags(topic_html)

            # 等級欄常帶註記（「🔴🔴 全庫最高頻」「🟠 ⚠ 數字衝突」），
            # 拆成可篩選的鍵（單一顏色）＋ 顯示用的註記，雙圈另外標記
            level_txt = strip_tags(level_html)
            lm = re.match(r"^([🔴🟠🟡]+)\s*(.*)$", level_txt)
            level = lm.group(1)[0] if lm else ""
            level_note = (lm.group(2).strip() if lm else level_txt)
            hot = bool(lm and len(lm.group(1)) > 1)

            # 主題 → 主題節
            target = ""
            for prefix, tid in IDX_OVERRIDE.items():
                if topic_txt.startswith(prefix):
                    target = tid
                    break
            if not target:
                en1, zh1 = tokens(topic_txt)
                best, best_score = None, 0
                for t in topics:
                    if t["group"] not in IDX_ALLOW[sid]:
                        continue
                    en2, zh2 = tokens(t["title"])
                    score = len(en1 & en2) * 3 + len(zh1 & zh2)
                    if score > best_score:
                        best, best_score = t, score
                if best is not None and best_score >= MATCH_THRESHOLD:
                    target = best["id"]
            if not target:
                unmatched.append(topic_txt[:50])

            # 考官欄 → 一個個可點的名牌
            exams = []
            for part in re.split(r"[；;]", strip_tags(ex_html)):
                part = part.strip()
                if not part:
                    continue
                hit = next((n for n in names if n in part), None)
                note = ""
                mp = re.search(r"[（(]([^）)]*)[）)]", part)
                if mp:
                    note = mp.group(1).strip()
                exams.append({"n": hit or part[:12], "id": names.get(hit, ""), "y": note})

            rows.append({
                "dom": dom,
                "lv": level,
                "lvn": level_note,
                "hot": hot,
                "t": topic_html.strip(),
                "tt": topic_txt,
                "go": target,
                "ex": exams,
                "loc": linkify(loc_html.strip()),
            })

    return rows, unmatched


# ---------------------------------------------------------------- JS 改寫

def patch_js(js, rows_json):
    def sub_once(pattern, repl, text, what, flags=re.S):
        new, n = re.subn(pattern, repl, text, count=1, flags=flags)
        if n != 1:
            sys.exit(f"[build] 找不到要替換的片段：{what}")
        return new

    # 1) 分組定義
    dom_js = ",\n  ".join(f"['{k}','{v}']" for k, v in DOMAINS)
    ch_js = ",\n  ".join(f"['{k}','{label}']" for k, _, label, _ in CHAPTERS)
    js = sub_once(
        r"const EX_GROUPS = \[.*?\];\nconst TO_GROUPS = \[.*?\];",
        lambda m: (
            "const DOMAINS = [\n  " + dom_js + "\n];\n"
            "const CHAPTERS = [\n  " + ch_js + "\n];\n"
            "const EX_GROUPS = [['start','開始這裡'],['index','押題・索引・衝突裁決']]\n"
            "  .concat(CHAPTERS).concat([['check','事實查核與缺口']]);\n"
            "const TO_GROUPS = [['start','開始這裡'],['index','押題・索引・衝突裁決']]\n"
            "  .concat(DOMAINS).concat([['notes','各章速記卡與附錄'],['check','事實查核與缺口']]);"
        ),
        js, "EX_GROUPS/TO_GROUPS")

    js = sub_once(
        r"function groupLabel\(g\)\{[^\n]*\}",
        lambda m: ("function gkey(s){ return axis==='examiner' ? (s.gEx||s.group) : (s.gTo||s.group); }\n"
                   "function groupLabel(g){ const f=[...EX_GROUPS,...TO_GROUPS].find(x=>x[0]===g); return f?f[1]:g; }\n"
                   "function domLabel(d){ const f=DOMAINS.find(x=>x[0]===d); return f?f[1]:d; }"),
        js, "groupLabel")

    # 2) 篩選：領域（兩軸共用）＋ 等級（主題軸）＋ 關卡性質（考官軸）
    js = sub_once(
        r"const allTags = .*?\nfunction renderChips\(\)\{.*?\n\}\n",
        lambda m: r"""const LEVELS = [['🔴','🔴 必背'],['🟠','🟠 高機率'],['🟡','🟡 補充']];
const STATIONS = ['魔王關','聊天關','跨領域','未任考官'];
let activeDom = new Set(), activeLv = new Set(), activeSt = new Set();

function chipRow(host, title, items, set, after){
  const wrap=document.createElement('div'); wrap.className='chipset';
  const h=document.createElement('div'); h.className='chiphead'; h.textContent=title; wrap.appendChild(h);
  const box=document.createElement('div'); box.className='chips'; wrap.appendChild(box);
  items.forEach(([val,label])=>{
    const b=document.createElement('button');
    b.className='chip'; b.type='button'; b.textContent=label;
    b.setAttribute('aria-pressed', set.has(val)?'true':'false');
    b.addEventListener('click',()=>{
      set.has(val) ? set.delete(val) : set.add(val);
      if(after) after();
    });
    box.appendChild(b);
  });
  host.appendChild(wrap);
}

function filterCount(){ return activeDom.size + (axis==='topic'?activeLv.size:activeSt.size); }

function renderChips(){
  chipBox.innerHTML='';
  fsum.childNodes[0].nodeValue = '篩選';
  const redraw=()=>{ renderChips(); renderNav(); if(current==='s10') show('s10', false); };
  chipRow(chipBox,'領域（兩軸共用）', DOMAINS, activeDom, redraw);
  if(axis==='topic') chipRow(chipBox,'必背等級', LEVELS, activeLv, redraw);
  else chipRow(chipBox,'關卡性質', STATIONS.map(t=>[t,t]), activeSt, redraw);
  fcount.textContent = filterCount() ? '　'+filterCount() : '';
}
""",
        js, "renderChips")

    # 3) visible()
    js = sub_once(
        r"function visible\(s\)\{.*?\n\}\n",
        lambda m: r"""function visible(s){
  if(!inAxis(s)) return false;
  const ds = s.domains||[];
  if(activeDom.size && ds.length && !ds.some(d=>activeDom.has(d))) return false;
  if(axis==='topic' && activeLv.size && s.axis==='topic' && !activeLv.has(s.level)) return false;
  if(axis==='examiner' && activeSt.size && s.axis==='examiner'
     && !(s.stations||[]).some(t=>activeSt.has(t))) return false;
  return true;
}
""",
        js, "visible")

    # 4) 導覽依 gkey 分組，考官項目掛上章號
    js = sub_once(
        r"const items = S\.filter\(s=>s\.group===g && visible\(s\)\);",
        "const items = S.filter(s=>gkey(s)===g && visible(s));",
        js, "renderNav filter")

    js = sub_once(
        r"const parts=s\.title\.split\('　'\);",
        ("if(s.chapter){ const cb=document.createElement('span'); cb.className='chn';"
         " cb.textContent=s.chapter; b.appendChild(cb); }\n      const parts=s.title.split('　');"),
        js, "nav chapter badge")

    # 5) 麵包屑改用 gkey
    js = sub_once(
        r"crumb\.textContent=groupLabel\(s\.group\);",
        "crumb.textContent=groupLabel(gkey(s));",
        js, "breadcrumb")

    js = sub_once(
        r"esc\(groupLabel\(h\.s\.group\)\)",
        "esc(groupLabel(h.s.axis==='topic'?(h.s.gTo||h.s.group):(h.s.gEx||h.s.group)))",
        js, "search crumb")

    # 6) 文章標頭補上領域徽章
    js = sub_once(
        r"if\(s\.sub\)\{ const t=document\.createElement\('span'\); t\.className='tag'; t\.textContent=s\.sub; meta\.appendChild\(t\); \}",
        ("(s.domains||[]).forEach(dv=>{ const t=document.createElement('span');"
         " t.className='tag dom'; t.textContent=domLabel(dv); meta.appendChild(t); });\n"
         "  if(s.sub){ const t=document.createElement('span'); t.className='tag'; t.textContent=s.sub; meta.appendChild(t); }"),
        js, "domain badge")

    # 7) 第一部索引的渲染，插在 article 之前
    js = sub_once(
        r"  const art=document\.createElement\('article'\); art\.innerHTML=s\.html;",
        lambda m: r"""  if(s.render==='idx') view.appendChild(indexPanel());

  const art=document.createElement('article'); art.innerHTML=s.html;""",
        js, "index panel hook")

    # 8) 索引面板 + 全域跳轉委派，插在 show() 之前
    js = sub_once(
        r"function show\(id, scroll\)\{",
        lambda m: r"""const IDX = JSON.parse(document.getElementById('idxdata').textContent);

function indexPanel(){
  const box=document.createElement('section'); box.className='idx';

  const bar=document.createElement('div'); bar.className='idxbar';
  const redraw=()=>{ renderChips(); renderNav(); show('s10', false); };
  chipRow(bar,'領域', DOMAINS, activeDom, redraw);
  chipRow(bar,'必背等級', LEVELS, activeLv, redraw);
  box.appendChild(bar);

  const rows = IDX.filter(r=>(!activeDom.size || activeDom.has(r.dom))
                          && (!activeLv.size || activeLv.has(r.lv)));
  const tally=document.createElement('div'); tally.className='idxtally';
  tally.textContent = rows.length===IDX.length
    ? IDX.length+' 列'
    : rows.length+' / '+IDX.length+' 列';
  box.appendChild(tally);

  if(!rows.length){
    const p=document.createElement('p'); p.className='idxempty';
    p.textContent='這個組合沒有題目。點掉幾個篩選再看看。';
    box.appendChild(p); return box;
  }

  let lastDom='';
  const list=document.createElement('div'); list.className='idxlist';
  rows.forEach(r=>{
    if(r.dom!==lastDom){
      lastDom=r.dom;
      const h=document.createElement('h3'); h.className='idxdom'; h.textContent=domLabel(r.dom);
      list.appendChild(h);
    }
    const row=document.createElement('div'); row.className='idxrow';

    const top=document.createElement('div'); top.className='irtop';
    if(r.lv){
      const lv=document.createElement('span'); lv.className='lv'+(r.hot?' hot':'');
      lv.textContent = r.hot ? r.lv+r.lv : r.lv;
      if(r.hot) lv.title='全庫最高頻';
      top.appendChild(lv);
    }
    if(r.go){
      const b=document.createElement('button'); b.type='button'; b.className='irtopic';
      b.setAttribute('data-go', r.go); b.innerHTML=r.t; top.appendChild(b);
    } else {
      const sp=document.createElement('span'); sp.className='irtopic plain'; sp.innerHTML=r.t; top.appendChild(sp);
    }
    row.appendChild(top);

    if(r.lvn){
      const n=document.createElement('div'); n.className='irnote'; n.textContent=r.lvn;
      row.appendChild(n);
    }

    if(r.ex.length){
      const line=document.createElement('div'); line.className='irline';
      const k=document.createElement('span'); k.className='irk'; k.textContent='考官'; line.appendChild(k);
      r.ex.forEach(e=>{
        const label=e.n+(e.y?' '+e.y:'');
        if(e.id){
          const b=document.createElement('button'); b.type='button'; b.className='exchip';
          b.setAttribute('data-go', e.id); b.textContent=label; line.appendChild(b);
        } else {
          const sp=document.createElement('span'); sp.className='exchip plain'; sp.textContent=label; line.appendChild(sp);
        }
      });
      row.appendChild(line);
    }

    if(r.loc){
      const line=document.createElement('div'); line.className='irline';
      const k=document.createElement('span'); k.className='irk'; k.textContent='答案'; line.appendChild(k);
      const v=document.createElement('span'); v.className='irloc'; v.innerHTML=r.loc; line.appendChild(v);
      row.appendChild(line);
    }

    list.appendChild(row);
  });
  box.appendChild(list);
  return box;
}

function show(id, scroll){""",
        js, "indexPanel")

    # 9) 全域跳轉委派（含 view 內所有 data-go）
    js = sub_once(
        r"syncAxisUI\(\);\nshow\(S\[0\]\.id\);",
        lambda m: r"""view.addEventListener('click', e=>{
  const b = e.target.closest ? e.target.closest('[data-go]') : null;
  if(!b) return;
  const t = byId[b.getAttribute('data-go')];
  if(!t) return;
  e.preventDefault();
  if(!inAxis(t)){ axis = t.axis==='topic' ? 'topic' : 'examiner'; syncAxisUI(); }
  show(t.id); closeNav();
});

syncAxisUI();
show(S[0].id);""",
        js, "data-go delegation")

    return js


# ---------------------------------------------------------------- CSS

EXTRA_CSS = """
/* ---- 統一篩選器 ---- */
.chipset{margin:0 0 10px}
.chipset:last-child{margin-bottom:0}
.chiphead{font-family:var(--mono); font-size:9.5px; letter-spacing:.12em;
  text-transform:uppercase; color:var(--muted); margin:0 0 5px}
.chn{font-family:var(--mono); font-size:9px; font-weight:500; letter-spacing:.06em;
  color:var(--on-accent); background:var(--accent); border-radius:3px;
  padding:1px 4px; margin-right:6px; flex:none}
.tag.dom{background:var(--accent-soft); color:var(--accent-ink)}

/* ---- 第一部：可篩選索引 ---- */
.idx{margin:0 0 30px}
.idxbar{border:1px solid var(--rule); border-radius:10px; padding:13px 14px;
  background:var(--surface); margin:0 0 14px}
.idxtally{font-family:var(--mono); font-size:11px; color:var(--muted); margin:0 0 14px}
.idxempty{color:var(--muted)}
.idxdom{font-family:var(--display); font-size:17px; font-weight:700; margin:26px 0 10px;
  padding-bottom:6px; border-bottom:1px solid var(--rule)}
.idxdom:first-child{margin-top:0}
.idxrow{padding:11px 0; border-bottom:1px solid var(--rule)}
.idxrow:last-child{border-bottom:0}
.irtop{display:flex; gap:8px; align-items:baseline}
.irtop .lv{flex:none; font-size:12px; line-height:1.6}
.irtopic{font:inherit; font-size:15px; line-height:1.6; text-align:left; color:var(--ink);
  background:none; border:0; padding:0; cursor:pointer; border-bottom:1px solid var(--rule)}
.irtopic:hover{color:var(--accent-ink); border-bottom-color:var(--accent)}
.irtopic.plain{cursor:default; border-bottom:0}
.irtopic strong{font-weight:600}
.lv.hot{letter-spacing:-2px}
.irnote{font-size:12px; color:var(--warn); margin:4px 0 0; padding-left:20px}
.irline{display:flex; flex-wrap:wrap; gap:5px; align-items:baseline; margin:7px 0 0; padding-left:20px}
.irk{font-family:var(--mono); font-size:9.5px; letter-spacing:.1em; color:var(--muted);
  flex:none; width:30px}
.exchip{font:inherit; font-size:12px; line-height:1.5; padding:2px 8px; border-radius:20px;
  border:1px solid var(--rule); background:var(--surface); color:var(--ink-2); cursor:pointer}
.exchip:hover{border-color:var(--accent); color:var(--accent-ink); background:var(--accent-soft)}
.exchip.plain{cursor:default; opacity:.75}
.irloc{font-size:13px; color:var(--ink-2); flex:1; min-width:0}

/* ---- 全書交叉參照 ---- */
.jump{font:inherit; font-size:inherit; color:var(--accent-ink); background:none;
  border:0; border-bottom:1px solid var(--accent); padding:0; cursor:pointer;
  text-align:left; line-height:inherit}
.jump:hover{background:var(--accent-soft)}
article .jump{font-weight:600}
@media (max-width:820px){
  .irline{padding-left:0}
  .irk{width:auto}
}
"""


# ---------------------------------------------------------------- 主流程

def main():
    if not SRC.exists():
        sys.exit(f"[build] 找不到來源：{SRC}")
    html = SRC.read_text(encoding="utf-8")

    m = re.search(r'(<script id="data" type="application/json">)(.*?)(</script>)', html, re.S)
    if not m:
        sys.exit("[build] 找不到資料區塊")
    sections = json.loads(m.group(2))
    by_id = {s["id"]: s for s in sections}

    linkify, names = build_linkifier(sections)

    # 1) 第一部 → 結構化索引
    rows, unmatched = build_index_rows(by_id, sections, linkify, names)

    # 索引各列的文字併回 s10，維持全文搜尋可以命中
    idx_text = " ".join(by_id[sid]["text"] for sid in IDX_SECTIONS)
    s10 = by_id["s10"]
    s10["text"] = (s10["text"] + " " + idx_text).strip()
    s10["render"] = "idx"
    s10["title"] = "第一部｜主題 → 考官 反查索引（91 題）"

    dropped = set(IDX_SECTIONS)
    sections = [s for s in sections if s["id"] not in dropped]

    # 2) 領域 / 章號 / 關卡性質
    chapter_of, group_of = {}, {}
    for gid, letter, _label, ids in CHAPTERS:
        for sid in ids:
            chapter_of[sid] = letter
            group_of[sid] = gid

    for s in sections:
        doms, stations = [], []
        if s["axis"] == "topic":
            d = topic_domain(s)
            if d:
                doms = [d]
        elif s["axis"] == "examiner":
            seen = []
            for t in (s.get("tags") or []):
                if t in TAG2DOM and TAG2DOM[t] not in seen:
                    seen.append(TAG2DOM[t])
                elif t in STATIONS:
                    stations.append(t)
            doms = seen
        s["domains"] = doms
        s["stations"] = stations
        if s["id"] in chapter_of:
            s["chapter"] = chapter_of[s["id"]]
        s["gEx"] = group_of.get(s["id"], s["group"])
        s["gTo"] = s["group"]
        if s["axis"] == "topic" and doms:
            s["gTo"] = doms[0]
        # 交叉參照連結化（索引各列已在上面處理過）
        s["html"] = linkify(s["html"])

    order = {k: i for i, (k, _) in enumerate(DOMAINS)}

    # 考官的領域再由第一部索引補強：在索引裡被哪個領域引用，就歸進那個領域。
    # 只靠 26 個 tag 會漏掉人（「跨領域」「魔王關」本身不是領域）。
    cited = {}
    for r in rows:
        for e in r["ex"]:
            if e["id"]:
                cited.setdefault(e["id"], set()).add(r["dom"])
    for s in sections:
        if s["axis"] != "examiner":
            continue
        merged = set(s["domains"]) | cited.get(s["id"], set())
        s["domains"] = sorted(merged, key=lambda d: order.get(d, 99))

    # 主題節依 12 領域重排，導覽順序才跟篩選器一致（就地換位，不動其他節）
    slots = [i for i, s in enumerate(sections) if s["axis"] == "topic"]
    ordered = sorted((sections[i] for i in slots),
                     key=lambda s: (order.get(s["gTo"], 99), num_of(s["id"]) or 0))
    for slot, sec in zip(slots, ordered):
        sections[slot] = sec

    # 3) 寫回
    data_json = json.dumps(sections, ensure_ascii=False).replace("</", "<\\/")
    rows_json = json.dumps(rows, ensure_ascii=False).replace("</", "<\\/")
    html = html[:m.start(2)] + data_json + html[m.end(2):]

    html = html.replace(
        '<script id="data" type="application/json">',
        f'<script id="idxdata" type="application/json">{rows_json}</script>\n'
        '<script id="data" type="application/json">',
        1)

    js_m = re.search(r"(<script>\n\(function\(\)\{\n\"use strict\";)(.*?)(</script>)", html, re.S)
    if not js_m:
        sys.exit("[build] 找不到主程式")
    html = html[:js_m.start(2)] + patch_js(js_m.group(2), rows_json) + html[js_m.end(2):]

    html = html.replace("</style>\n<style>", "</style>\n<style>", 1)
    last_style = html.rfind("</style>")
    html = html[:last_style] + EXTRA_CSS + html[last_style:]

    OUT.write_text(html, encoding="utf-8")

    linked = sum(1 for r in rows if r["go"])
    ex_linked = sum(1 for r in rows for e in r["ex"] if e["id"])
    ex_total = sum(len(r["ex"]) for r in rows)
    print(f"[build] 寫出 {OUT}  ({OUT.stat().st_size/1024/1024:.2f} MB)")
    print(f"[build] 節數 {len(sections)}（原 {len(sections)+len(dropped)}，第一部 11 節併為 1）")
    print(f"[build] 索引 {len(rows)} 列：主題可跳轉 {linked}，考官名牌 {ex_linked}/{ex_total}")
    if unmatched:
        print(f"[build] 無對應主題節（維持純文字）{len(unmatched)} 列：")
        for u in unmatched:
            print(f"          · {u}")


if __name__ == "__main__":
    main()
