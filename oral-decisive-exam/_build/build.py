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
import collections
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import restructure as R  # noqa: E402
import plain as P  # noqa: E402
import mdsource as MD  # noqa: E402
import voice as V  # noqa: E402
import intel as I  # noqa: E402
import newtopics as NT  # noqa: E402

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

# ------------------------------------------------------------ 標題與名詞

# 手冊自稱「第二部押題排行榜」，但切節時「第二部」這個標題掉了，
# 只剩兩個看不出是什麼的孤兒節。補回與第一部、第三部一致的稱呼。
SECTION_RENAMES = {
    "s22": "第二部｜2026 押題 Top 25 · 排序邏輯",
    "s23": "第二部｜2026 押題 Top 25 · 排行榜（25 題）",
}

# 全書提到這些名詞時直接可跳。長的排前面，避免被短的先吃掉。
TERM_LINKS = [
    ("押題排行榜", "s23"),
    ("押題 Top 25", "s23"),
    ("押題排行", "s23"),
    ("押題榜", "s23"),
    ("衝突裁決總表", "s24"),
]

# ------------------------------------------------- 讀書進度表（s2）重寫

# 「讀哪裡」欄指名的頁面
SCHEDULE_LINKS = {
    "索引": "s9",
    "Ch.A": "s27", "Ch.B": "s34", "Ch.C": "s43",
    "Ch.D": "s51", "Ch.E": "s57",
    "見第三節": "s4",
}


def _chip(label):
    return f'<button type="button" class="goto" data-go="{SCHEDULE_LINKS[label]}">{label}</button>'


# (D 高, D 低, 做什麼, 讀哪裡)。天數相對考試日，日期由前端依考試日算出。
SCHEDULE_ROWS = [
    (12, 9, "先讀「押題 Top 25」＋ 衝突裁決總表，把 20 個必背數字背起來",
     _chip("索引")),
    (8, 4, "<strong>2025 年 15 站</strong>逐關讀，每關讀完<strong>闔上檔案自己講一遍</strong>",
     "／".join(_chip(c) for c in ("Ch.A", "Ch.B", "Ch.C"))),
    (3, 2, "歷年核心考官（題庫沿用率最高的一批）",
     "／".join(_chip(c) for c in ("Ch.D", "Ch.E"))),
    (1, 1, "只讀每章末的「速記卡」＋ 衝突裁決總表＋ 態度救命句",
     _chip("索引")),
    (0, 0, "簡歷與手術紀錄本、證件、身分證",
     _chip("見第三節")),
]


# 2026/09/05 實際是星期六，原文誤植為（五）（已與作者確認）。
# 改成佔位符而不是直接寫死「六」，日期若再調整，星期會自己跟著對。
EXAM_WEEKDAY_TYPO = "2026/09/05（五）"
EXAM_WEEKDAY_FIXED = "2026/09/05（{{W}}）"


def patch_exam_weekday(sec):
    if EXAM_WEEKDAY_TYPO not in sec["html"]:
        sys.exit("[build] 找不到要更正的考試日星期標示")
    for field in ("html", "text"):
        sec[field] = sec[field].replace(EXAM_WEEKDAY_TYPO, EXAM_WEEKDAY_FIXED)


def patch_schedule(sec):
    """把倒數天數換成即時計算，「讀哪裡」欄換成可點的跳轉。"""
    rows = []
    for hi, lo, what, where in SCHEDULE_ROWS:
        label = "當天" if hi == 0 else (f"D-{hi}" if hi == lo else f"D-{hi} ～ D-{lo}")
        rows.append(
            f'<tr data-dhi="{hi}" data-dlo="{lo}">\n'
            f'<td><strong>{label}</strong><span class="dr"></span></td>\n'
            f'<td>{what}</td>\n'
            f'<td>{where}</td>\n'
            f'</tr>'
        )
    table = (
        '<table class="sched">\n'
        '<thead>\n<tr>\n<th>天數</th>\n<th>做什麼</th>\n<th>讀哪裡</th>\n</tr>\n</thead>\n'
        '<tbody>\n' + "\n".join(rows) + '\n</tbody>\n</table>'
    )
    tail = sec["html"][sec["html"].index("</table>") + len("</table>"):]
    sec["html"] = table + tail
    sec["title"] = re.sub(r"剩\s*\d+\s*天", "剩 {{D}} 天", sec["title"])
    sec["text"] = re.sub(r"剩\s*\d+\s*天", "剩 {{D}} 天", sec["text"])


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

    terms = "|".join(re.escape(t) for t, _ in TERM_LINKS)
    term_target = dict(TERM_LINKS)

    pattern = re.compile(
        r"〔(?P<nm>[^〕]{1,8})〕"
        r"|(?P<a>[A-E])\s*章\s*§\s*(?P<an>\d+)"
        r"|(?P<b>[A-E])\s*§\s*(?P<bn>\d+)"
        r"|(?P<c>[A-E])\s*章\s*(?P<cn>\d+)(?:-(?P<cs>\d+))?"
        r"|(?P<d>[A-E])\s*章"
        r"|(?P<t>" + terms + r")"
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

    def repl(m, skip=None):
        raw = m.group(0)
        if m.group("nm") is not None:
            tid = names.get(m.group("nm"))
            return f"〔{jump(tid, m.group('nm'))}〕" if tid else raw
        if m.group("t"):
            tid = term_target[m.group("t")]
            return raw if tid == skip else jump(tid, raw)
        if m.group("a"):
            tid = by_number(m.group("a"), int(m.group("an")), None)
        elif m.group("b"):
            tid = by_number(m.group("b"), int(m.group("bn")), None)
        elif m.group("c"):
            tid = by_number(m.group("c"), int(m.group("cn")), m.group("cs"))
        else:
            tid = CH_HEAD.get(m.group("d"))
        return jump(tid, raw) if tid else raw

    def linkify(html, skip=None):
        """skip：正在處理的節，避免名詞連到自己身上。"""
        return pattern.sub(lambda m: repl(m, skip), html)

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

    # 9) 倒數改成全域可用，並提供 {{D}} 代換與考試日回推
    js = sub_once(
        r"\(function\(\)\{\n  const exam = new Date\('2026-09-05T08:00:00\+08:00'\);.*?\n\}\)\(\);",
        lambda m: r"""const EXAM = new Date('2026-09-05T08:00:00+08:00');
const DAYS = Math.max(0, Math.ceil((EXAM - new Date())/86400000));
(function(){
  document.getElementById('cd').textContent = DAYS;
  const m = document.getElementById('cdmini'); if(m) m.textContent = 'D-' + DAYS;
})();

/* 考試日的星期，由考試日算出（+08:00），不寫死 */
const EXAM_W = '日一二三四五六'[new Date(EXAM.getTime() + 8*3600000).getUTCDay()];

/* 內文佔位符：{{D}} 剩餘天數、{{W}} 考試日星期 */
function live(t){
  return (t==null?'':String(t)).replace(/\{\{D\}\}/g, DAYS).replace(/\{\{W\}\}/g, EXAM_W);
}

/* 考前第 n 天是哪一天（以考試日的 +08:00 為準，不受讀者時區影響） */
function examDate(n){
  const t = new Date(EXAM.getTime() - n*86400000 + 8*3600000);
  return (t.getUTCMonth()+1)+'/'+t.getUTCDate()+'（'+'日一二三四五六'[t.getUTCDay()]+'）';
}
(function(){ const e=document.getElementById('cddate'); if(e) e.textContent=examDate(0); })();

/* 進度表：填上實際日期，並標出現在落在哪一段 */
function wireSchedule(art){
  art.querySelectorAll('tr[data-dhi]').forEach(tr=>{
    const hi=+tr.getAttribute('data-dhi'), lo=+tr.getAttribute('data-dlo');
    const dr=tr.querySelector('.dr');
    if(dr) dr.textContent = hi===lo ? examDate(hi) : examDate(hi)+' – '+examDate(lo);
    if(DAYS<=hi && DAYS>=lo){
      tr.classList.add('now');
      const cell=tr.querySelector('td');
      if(cell){ const b=document.createElement('span'); b.className='nowtag'; b.textContent='現在'; cell.appendChild(b); }
    }
  });
}""",
        js, "countdown")

    for pat, rep, what in [
        (r"nm\.textContent=s\.title;", "nm.textContent=live(s.title);", "nav title"),
        (r"h1\.textContent=s\.title;", "h1.textContent=live(s.title);", "article title"),
        (r"art\.innerHTML=s\.html;", "art.innerHTML=live(s.html);", "article html"),
        (r"document\.createTextNode\(s2\.title\)", "document.createTextNode(live(s2.title))", "pager"),
        (r"\(s\.title\+' '\+\(s\.headline\|\|''\)\+' '\+s\.text\)",
         "live(s.title+' '+(s.headline||'')+' '+s.text)", "search haystack"),
        (r"esc\(h\.s\.title\)", "esc(live(h.s.title))", "search title"),
        (r"const src=h\.s\.text,", "const src=live(h.s.text),", "search snippet"),
        (r"\+t\.title\.replace\('　','／'\)", "+live(t.title).replace('　','／')", "xlink label"),
    ]:
        js = sub_once(pat, rep, js, what)

    js = sub_once(
        r"(  view\.appendChild\(art\);)",
        lambda m: "  wireSchedule(art);\n" + m.group(1),
        js, "schedule wiring")

    # 10) 上一頁：接上瀏覽器 history，順便讓每一節有自己的網址
    js = sub_once(
        r"(function show\(id, scroll\)\{)",
        lambda m: r"""let histDepth = 0;        /* 目前疊了幾層站內歷史，0 代表沒得退 */
let histLast = null;      /* 最後一次寫進歷史的節，避免重繪時灌爆歷史 */
let histQuiet = false;    /* 由 popstate 觸發的 show()，不要再寫歷史 */

function pushHistory(id){
  if(histQuiet || id===histLast) return;
  const first = histLast===null;
  const st = {id: id, axis: axis, depth: first ? 0 : histDepth+1};
  try{
    if(first) history.replaceState(st, '', '#'+id);
    else history.pushState(st, '', '#'+id);
  }catch(e){ return; }   /* file:// 之類不給改網址時，靜靜略過 */
  histDepth = st.depth;
  histLast = id;
}

window.addEventListener('popstate', e=>{
  const st = e.state;
  const id = (st && st.id) || decodeURIComponent((location.hash||'').slice(1));
  if(!byId[id]) return;
  histQuiet = true;
  histDepth = (st && typeof st.depth==='number') ? st.depth : 0;
  histLast = id;
  if(st && st.axis && st.axis!==axis){ axis = st.axis; syncAxisUI(); }
  show(id);
  histQuiet = false;
});

""" + m.group(1),
        js, "history helpers")

    js = sub_once(
        r"(  current = id;\n)",
        lambda m: m.group(1) + "  pushHistory(id);\n",
        js, "push on navigate")

    js = sub_once(
        r"(  view\.innerHTML='';\n  const head=document\.createElement\('header'\))",
        lambda m: r"""  view.innerHTML='';
  if(histDepth>0){
    const bar=document.createElement('div'); bar.className='backbar';
    const bb=document.createElement('button'); bb.type='button'; bb.className='backbtn';
    bb.appendChild(document.createTextNode('← 返回'));
    bb.addEventListener('click', ()=>history.back());
    bar.appendChild(bb); view.appendChild(bar);
  }
  const head=document.createElement('header')""",
        js, "back bar")

    # 11) 全域跳轉委派（含 view 內所有 data-go）
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

    # 12) 每篇文章下的筆記（自動儲存），以及匯出／匯入
    js = sub_once(
        r"(let histDepth = 0;)",
        lambda m: r"""let notes = {};
try{ notes = JSON.parse(localStorage.getItem('psoral.notes')||'{}'); }catch(e){ notes = {}; }
function saveNotes(){
  try{ localStorage.setItem('psoral.notes', JSON.stringify(notes)); return true; }
  catch(e){ return false; }   /* 無痕模式或空間滿了 */
}
function noteCount(){ return Object.keys(notes).filter(k=>notes[k] && notes[k].t).length; }
function hasNote(id){ return !!(notes[id] && notes[id].t); }
function stamp(ms){
  const d=new Date(ms);
  const p=n=>String(n).padStart(2,'0');
  return p(d.getMonth()+1)+'/'+p(d.getDate())+' '+p(d.getHours())+':'+p(d.getMinutes());
}

let curNote=null;   /* 目前畫面上的筆記框，同步回來時就地更新，不重繪整頁 */
let curRead=null;   /* 目前畫面上的已讀按鈕，同上 */

function renderProgress(){
  const el=document.getElementById('progress');
  if(!el) return;
  el.innerHTML='';
  const done=readCount(), left=S.length-done;
  const t=document.createElement('span'); t.className='ptext';
  t.textContent = left ? ('未讀 '+left+' / '+S.length) : ('全部讀完了 · '+S.length+' 節');
  const b=document.createElement('button'); b.type='button'; b.className='ponly';
  b.textContent='只看未讀';
  b.setAttribute('aria-pressed', onlyUnread?'true':'false');
  b.addEventListener('click',()=>{
    onlyUnread=!onlyUnread;
    try{ localStorage.setItem('psoral.onlyunread', onlyUnread?'1':''); }catch(e){}
    renderProgress(); renderNav();
  });
  el.appendChild(t); el.appendChild(b);
}

function notePanel(s){
  const box=document.createElement('section'); box.className='notebox';
  const h=document.createElement('h2'); h.textContent='我的筆記';
  const st=document.createElement('span'); st.className='nstat'; h.appendChild(st);
  box.appendChild(h);

  const ta=document.createElement('textarea');
  ta.className='note'; ta.rows=3; ta.spellcheck=false;
  ta.placeholder='寫下你自己的講法、口訣、老師說過的話…（自動儲存）';
  const cur=notes[s.id];
  ta.value = (cur && cur.t) ? cur.t : '';
  const grow=()=>{ ta.style.height='auto'; ta.style.height=Math.max(72, ta.scrollHeight)+'px'; };
  const mark=()=>{ st.textContent = hasNote(s.id) ? '已儲存 '+stamp(notes[s.id].u) : ''; };
  mark();

  let timer;
  ta.addEventListener('input',()=>{
    grow();
    st.textContent='輸入中…';
    clearTimeout(timer);
    timer=setTimeout(()=>{
      const v=ta.value.trim();
      /* 刪除留成空字串的墓碑，否則同步時會被別台裝置的舊資料復活 */
      notes[s.id]={t: v ? ta.value : '', u: Date.now()};
      st.textContent = saveNotes() ? (v ? '已儲存 '+stamp(Date.now()) : '') : '⚠ 無法儲存（無痕模式？）';
      renderNav();
      scheduleSync();
    }, 400);
  });
  ta.addEventListener('blur',()=>{ clearTimeout(timer); ta.dispatchEvent(new Event('input')); });
  box.appendChild(ta);
  setTimeout(grow,0);
  curNote={id:s.id, ta:ta, mark:mark, grow:grow};
  return box;
}

/* 匯出／匯入：目前跨裝置要靠這個搬 */
function exportNotes(){
  const payload={kind:'psoral.notes', at:new Date().toISOString(), notes:notes};
  const blob=new Blob([JSON.stringify(payload,null,2)],{type:'application/json'});
  const a=document.createElement('a');
  a.href=URL.createObjectURL(blob);
  a.download='口試筆記-'+new Date().toISOString().slice(0,10)+'.json';
  document.body.appendChild(a); a.click();
  setTimeout(()=>{ URL.revokeObjectURL(a.href); a.remove(); },0);
}
function importNotes(file, done){
  const r=new FileReader();
  r.onload=()=>{
    let data;
    try{ data=JSON.parse(r.result); }catch(e){ done('讀不懂這個檔案'); return; }
    const inc=(data && data.notes) || (data && data.kind ? null : data);
    if(!inc || typeof inc!=='object'){ done('檔案裡沒有筆記'); return; }
    let add=0, upd=0;
    Object.keys(inc).forEach(id=>{
      const n=inc[id];
      if(!n || typeof n.t!=='string') return;
      const old=notes[id];
      if(!old){ notes[id]=n; add++; }
      else if((n.u||0) > (old.u||0)){ notes[id]=n; upd++; }   /* 較新的勝出 */
    });
    saveNotes(); renderNav(); renderProgress(); show(current, false);
    done(null, '匯入 '+add+' 則、更新 '+upd+' 則');
  };
  r.readAsText(file);
}

/* ---------- 跨裝置同步（Cloudflare Worker，選用）---------- */
let sync={url:'', key:'', on:false};
try{ sync=Object.assign(sync, JSON.parse(localStorage.getItem('psoral.sync')||'{}')); }catch(e){}
function saveSyncCfg(){ try{ localStorage.setItem('psoral.sync', JSON.stringify(sync)); }catch(e){} }

/* 密語不出瀏覽器，只把 SHA-256 當成存取金鑰送上去 */
async function deriveKey(pass){
  const buf=new TextEncoder().encode('psoral|'+pass);
  const h=await crypto.subtle.digest('SHA-256', buf);
  return Array.from(new Uint8Array(h)).map(b=>b.toString(16).padStart(2,'0')).join('');
}

let syncBusy=false, syncTimer=null;
function syncSay(msg){ const e=document.getElementById('syncstat'); if(e) e.textContent=msg; }

function mergeMapIn(target, incoming){
  let touched=false;
  Object.keys(incoming||{}).forEach(id=>{
    const n=incoming[id];
    if(!n || typeof n!=='object') return;
    const old=target[id];
    if(!old || (n.u||0)>(old.u||0)){ target[id]=n; touched=true; }
  });
  return touched;
}

async function syncNow(){
  if(!sync.on || !sync.url || !sync.key || syncBusy) return;
  syncBusy=true; syncSay('同步中…');
  try{
    const res=await fetch(sync.url+'?k='+sync.key, {
      method:'PUT', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({notes:notes, read:read})
    });
    if(!res.ok) throw new Error('HTTP '+res.status);
    const data=await res.json();
    const gotNotes=mergeMapIn(notes, data.notes);
    /* 舊版 Worker 不回傳 read，這時保留本機的就好 */
    const gotRead = data.read ? mergeMapIn(read, data.read) : false;
    if(gotNotes) saveNotes();
    if(gotRead) saveRead();
    if(gotNotes || gotRead){
      renderNav(); renderProgress();
      /* 就地更新目前開著的筆記框，正在打字時不動它 */
      if(gotNotes && curNote && document.activeElement!==curNote.ta){
        const n=notes[curNote.id];
        const v=(n && n.t) ? n.t : '';
        if(curNote.ta.value!==v){ curNote.ta.value=v; curNote.grow(); }
        curNote.mark();
      }
      if(gotRead && curRead) curRead.refresh();
    }
    syncSay('已同步 '+stamp(Date.now()));
  }catch(e){
    syncSay('離線，稍後重試');
  }finally{ syncBusy=false; }
}

function scheduleSync(){
  if(!sync.on) return;
  clearTimeout(syncTimer);
  syncTimer=setTimeout(syncNow, 800);
}

if(sync.on){
  setInterval(()=>{ if(!document.hidden) syncNow(); }, 30000);
  document.addEventListener('visibilitychange',()=>{ if(!document.hidden) syncNow(); });
}

let histDepth = 0;""",
        js, "notes core")

    js = sub_once(
        r"(  const pager=document\.createElement\('div'\); pager\.className='pager';)",
        lambda m: "  view.appendChild(notePanel(s));\n\n" + m.group(1),
        js, "note panel mount")

    # 導覽上標出哪些節寫過筆記
    js = sub_once(
        r"      const dot=document\.createElement\('span'\); dot\.className='dot'\+\(read\[s\.id\]\?' on':''\); b\.appendChild\(dot\);",
        ("      const dot=document.createElement('span'); dot.className='dot'+(isRead(s.id)?' on':'');"
         " b.appendChild(dot);\n"
         "      if(hasNote(s.id)){ const nm=document.createElement('span');"
         " nm.className='hasnote'; nm.textContent='✎'; nm.title='這一節有筆記';"
         " b.appendChild(nm); }"),
        js, "nav read/note marker")

    # 已讀：加上時間戳才能跨裝置合併；舊格式 {id:true} 就地升級
    js = sub_once(
        r"try\{ read = JSON\.parse\(localStorage\.getItem\('psoral\.read'\)\|\|'\{\}'\); \}catch\(e\)\{ read = \{\}; \}",
        lambda m: r"""try{ read = JSON.parse(localStorage.getItem('psoral.read')||'{}'); }catch(e){ read = {}; }
Object.keys(read).forEach(id=>{                     /* 舊格式 {id:true} 升級 */
  if(read[id]===true) read[id]={r:1,u:0};
  else if(!read[id] || typeof read[id]!=='object') delete read[id];
});
function isRead(id){ return !!(read[id] && read[id].r); }
function readCount(){ return Object.keys(read).filter(id=>isRead(id)).length; }
let onlyUnread=false;
try{ onlyUnread = !!localStorage.getItem('psoral.onlyunread'); }catch(e){}""",
        js, "read model")

    js = sub_once(
        r"const setRb=\(\)=>\{ const on=!!read\[s\.id\];",
        "const setRb=()=>{ const on=isRead(s.id);",
        js, "read button state")

    js = sub_once(
        r"rb\.addEventListener\('click',\(\)=>\{ read\[s\.id\]=!read\[s\.id\]; if\(!read\[s\.id\]\) delete read\[s\.id\]; saveRead\(\); setRb\(\); renderNav\(\); \}\);",
        ("rb.addEventListener('click',()=>{\n"
         "    read[s.id]={r: isRead(s.id)?0:1, u: Date.now()};   /* 取消也留時間戳，才不會被舊資料復活 */\n"
         "    saveRead(); setRb(); renderNav(); renderProgress(); scheduleSync();\n"
         "  });\n"
         "  curRead={id:s.id, refresh:setRb};"),
        js, "read toggle")

    # 只看未讀
    js = sub_once(
        r"(  const ds = s\.domains\|\|\[\];)",
        lambda m: ("  if(onlyUnread && isRead(s.id) && s.id!==current) return false;\n" + m.group(1)),
        js, "unread filter")

    # 側欄工具列
    js = sub_once(
        r"(stat\.textContent = S\.length\+' 節　·　')",
        lambda m: r"""(function(){
  const bar=document.getElementById('tools');
  if(!bar) return;
  const n=document.createElement('span'); n.className='ncount';
  const sync2=()=>{ const c=noteCount(); n.textContent = c ? c+' 則筆記' : '尚無筆記'; };
  const ex=document.createElement('button'); ex.type='button'; ex.textContent='匯出';
  ex.addEventListener('click',exportNotes);
  const im=document.createElement('button'); im.type='button'; im.textContent='匯入';
  const fi=document.createElement('input'); fi.type='file'; fi.accept='application/json,.json';
  fi.style.display='none';
  im.addEventListener('click',()=>fi.click());
  fi.addEventListener('change',()=>{
    if(!fi.files || !fi.files[0]) return;
    importNotes(fi.files[0],(err,msg)=>{ n.textContent = err ? '⚠ '+err : msg; fi.value=''; });
  });
  const sy=document.createElement('button'); sy.type='button'; sy.textContent='同步';
  bar.appendChild(n); bar.appendChild(ex); bar.appendChild(im); bar.appendChild(sy); bar.appendChild(fi);

  /* 同步設定面板 */
  const panel=document.createElement('div'); panel.className='syncpanel'; panel.hidden=true;
  const st=document.createElement('div'); st.className='syncstat'; st.id='syncstat';
  const u=document.createElement('input'); u.type='url'; u.placeholder='Worker 網址';
  const k=document.createElement('input'); k.type='password'; k.placeholder='通關密語';
  const row=document.createElement('div'); row.className='syncbtns';
  const go=document.createElement('button'); go.type='button';
  const off=document.createElement('button'); off.type='button'; off.textContent='停用';
  row.appendChild(go); row.appendChild(off);
  panel.appendChild(u); panel.appendChild(k); panel.appendChild(row); panel.appendChild(st);
  bar.parentNode.insertBefore(panel, bar.nextSibling);

  const paint=()=>{
    u.value=sync.url||''; go.textContent = sync.on ? '重新連線' : '啟用';
    off.hidden = !sync.on;
    st.textContent = sync.on ? '同步已開啟' : '目前只存在這台裝置';
  };
  paint();
  sy.addEventListener('click',()=>{ panel.hidden=!panel.hidden; if(!panel.hidden) paint(); });
  go.addEventListener('click', async ()=>{
    let url=(u.value||'').trim().replace(/\/+$/,'');
    const pass=(k.value||'').trim();
    const local=/^(https?:\/\/)?(127\.0\.0\.1|localhost)(:\d+)?$/i.test(url);
    if(url && !/^https?:\/\//i.test(url)) url='https://'+url;   /* 少打 https:// 就補上 */
    if(!local && !/^https:\/\/[^\s]+\.[^\s]+/.test(url)){
      st.textContent='網址看起來不對，應該像 https://xxx.workers.dev'; return;
    }
    if(pass.length<4){ st.textContent='密語太短，至少 4 個字'; return; }
    st.textContent='連線中…';
    try{
      sync.url=url; sync.key=await deriveKey(pass); sync.on=true;
      saveSyncCfg(); k.value='';
      await syncNow();
      paint(); sync2();
    }catch(e){ st.textContent='連不上，檢查網址是否正確'; }
  });
  off.addEventListener('click',()=>{
    sync.on=false; saveSyncCfg(); paint();
    st.textContent='已停用，筆記仍留在這台裝置';
  });

  sync2();
  const origSave=saveNotes;
  saveNotes=function(){ const ok=origSave(); sync2(); return ok; };
})();

""" + m.group(1),
        js, "notes toolbar")

    # 13) 開場：網址帶著節代號就直接開那一節（必須排在委派修補之後）
    js = sub_once(
        r"syncAxisUI\(\);\nshow\(S\[0\]\.id\);",
        lambda m: r"""syncAxisUI();
renderProgress();
(function(){
  const want = decodeURIComponent((location.hash||'').slice(1));
  show(byId[want] ? want : S[0].id);
})();""",
        js, "boot from hash")

    return js


# ---------------------------------------------------------------- CSS

EXTRA_CSS = """
/* ---- 側欄：語音課程入口 ---- */
.voicelink{display:flex; align-items:center; gap:9px; margin:10px 0 0;
  padding:9px 11px; border-radius:9px; text-decoration:none;
  background:var(--accent); color:var(--on-accent);
  box-shadow:0 1px 2px rgba(0,0,0,.12)}
.voicelink:hover{filter:brightness(1.08)}
.voicelink .vi{flex:none; font-size:11px; line-height:1;
  width:20px; height:20px; border-radius:50%; display:grid; place-items:center;
  background:rgba(255,255,255,.22)}
.voicelink .vt{font-size:12.5px; font-weight:600; letter-spacing:.01em}
.voicelink .vs{font-family:var(--mono); font-size:9.5px; opacity:.82;
  margin-left:auto; text-align:right; line-height:1.3}

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

/* ---- 還原後的編號清單（保留作者原本的 ①②③／1. 標記）---- */
article ul.marked{list-style:none; padding-left:1.7em}
article ul.marked>li{text-indent:-1.7em}
article ul.marked ul.marked{padding-left:1.7em; margin-top:5px}
.mk{color:var(--accent-ink); font-weight:600; font-variant-numeric:tabular-nums}

/* ---- 閱讀進度 ---- */
.progress{display:flex; align-items:center; gap:8px; margin:8px 0 0}
.progress .ptext{font-family:var(--mono); font-size:10.5px; color:var(--muted); margin-right:auto}
.ponly{font:inherit; font-size:11.5px; line-height:1.4; padding:3px 9px; border-radius:20px;
  border:1px solid var(--rule); background:var(--surface); color:var(--ink-2); cursor:pointer}
.ponly:hover{border-color:var(--accent); color:var(--accent-ink)}
.ponly[aria-pressed="true"]{background:var(--accent); border-color:var(--accent); color:var(--on-accent)}

/* ---- 筆記 ---- */
.tools{display:flex; align-items:center; gap:6px; margin:9px 0 0; flex-wrap:wrap}
.tools .ncount{font-family:var(--mono); font-size:10.5px; color:var(--muted); margin-right:auto}
.tools button{font:inherit; font-size:11.5px; line-height:1.4; padding:3px 9px; border-radius:20px;
  border:1px solid var(--rule); background:var(--surface); color:var(--ink-2); cursor:pointer}
.tools button:hover{border-color:var(--accent); color:var(--accent-ink); background:var(--accent-soft)}
.notebox{margin:26px 0 6px; padding:15px 16px; border:1px solid var(--rule);
  border-radius:10px; background:var(--surface-2)}
.notebox h2{font-family:var(--mono); font-size:10px; letter-spacing:.14em; text-transform:uppercase;
  color:var(--muted); margin:0 0 9px; display:flex; align-items:baseline; gap:9px; font-weight:500}
.notebox .nstat{font-size:9.5px; letter-spacing:.06em; color:var(--ok); text-transform:none}
textarea.note{display:block; width:100%; box-sizing:border-box; min-height:72px; resize:vertical;
  font:inherit; font-size:15px; line-height:1.75; color:var(--ink);
  background:var(--surface); border:1px solid var(--rule); border-radius:7px; padding:10px 12px}
textarea.note:focus{outline:none; border-color:var(--accent);
  box-shadow:0 0 0 3px var(--accent-soft)}
textarea.note::placeholder{color:var(--muted)}
.hasnote{flex:none; margin-left:5px; font-size:11px; color:var(--accent)}

/* ---- 同步設定 ---- */
.syncpanel{margin:9px 0 0; padding:11px 12px; border:1px solid var(--rule);
  border-radius:9px; background:var(--surface)}
.syncpanel input{display:block; width:100%; box-sizing:border-box; margin:0 0 7px;
  font:inherit; font-size:12px; padding:6px 9px; border:1px solid var(--rule);
  border-radius:6px; background:var(--ground); color:var(--ink)}
.syncpanel input:focus{outline:none; border-color:var(--accent)}
.syncbtns{display:flex; gap:6px}
.syncbtns button{font:inherit; font-size:11.5px; padding:4px 11px; border-radius:20px;
  border:1px solid var(--rule); background:var(--surface); color:var(--ink-2); cursor:pointer}
.syncbtns button:first-child{border-color:var(--accent); color:var(--on-accent);
  background:var(--accent)}
.syncstat{font-family:var(--mono); font-size:10px; color:var(--muted); margin:8px 0 0}

/* ---- 上一頁 ---- */
.backbar{margin:0 0 14px}
.backbtn{font:inherit; font-size:12.5px; line-height:1.5; padding:4px 11px 4px 9px;
  border-radius:20px; border:1px solid var(--rule); background:var(--surface);
  color:var(--ink-2); cursor:pointer}
.backbtn:hover{border-color:var(--accent); color:var(--accent-ink); background:var(--accent-soft)}

/* ---- 讀書進度表 ---- */
.sched td:first-child{white-space:nowrap}
.sched .dr{display:block; font-family:var(--mono); font-size:10.5px; font-weight:400;
  color:var(--muted); letter-spacing:.02em; margin-top:2px}
.sched tr.now td{background:var(--accent-soft)}
.sched tr.now td:first-child strong{color:var(--accent-ink)}
.nowtag{display:inline-block; margin-left:7px; padding:1px 6px; border-radius:20px;
  background:var(--accent); color:var(--on-accent);
  font-family:var(--mono); font-size:9.5px; letter-spacing:.08em; vertical-align:2px}
.goto{font-family:var(--mono); font-size:12.5px; line-height:1.5; padding:2px 7px;
  border-radius:5px; border:1px solid var(--rule); background:var(--surface-2);
  color:var(--accent-ink); cursor:pointer}
.goto:hover{border-color:var(--accent); background:var(--accent-soft)}

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

    # 考前情報更新：比手冊本身還新的一節，插在卷首章的最後
    sections.insert(next(i for i, s in enumerate(sections) if s["id"] == "s9"),
                    I.section())

    # 補寫的主題節：手冊原本沒有、但今年情報顯示會考的題目
    new_topics = NT.load(ROOT / "_build" / "newtopics")
    sections.extend(new_topics)          # 稍後的主題節重排會把它們放進各自的領域

    by_id = {s["id"]: s for s in sections}

    # 以校訂版 markdown 取代各節內容（框架不動：代號、順序、metadata 全部沿用）
    md_dir = ROOT / "_build" / "md"
    md_stats, md_report = ({}, {"missing_files": [], "unmatched_titles": []})
    if md_dir.is_dir():
        md_stats, md_report = MD.apply(sections, md_dir)
        if md_report["unmatched_titles"]:
            sys.exit(f"[build] markdown 標題對不上網站節：{md_report['unmatched_titles'][:3]}")

    linkify, names = build_linkifier(sections)

    # 1) 第一部 → 結構化索引
    rows, unmatched = build_index_rows(by_id, sections, linkify, names)

    rows += NT.index_rows(new_topics)          # 補寫的節也要能從索引找到

    # 索引各列的文字併回 s10，維持全文搜尋可以命中
    idx_text = " ".join(by_id[sid]["text"] for sid in IDX_SECTIONS)
    s10 = by_id["s10"]
    s10["text"] = (s10["text"] + " " + idx_text).strip()
    s10["render"] = "idx"
    s10["title"] = "第一部｜主題 → 考官 反查索引（91 題）"

    dropped = set(IDX_SECTIONS)
    sections = [s for s in sections if s["id"] not in dropped]

    # 2) 卷首考試日的星期更正、讀書進度表倒數即時化、「讀哪裡」變成跳轉
    patch_exam_weekday(by_id["s1"])
    patch_schedule(by_id["s2"])

    # 補回掉失的「第二部」標題（第一部、第三部都在，只有它沒有）
    for sid, title in SECTION_RENAMES.items():
        if sid not in by_id:
            sys.exit(f"[build] 要改名的節不存在：{sid}")
        by_id[sid]["title"] = title

    # 2) 領域 / 章號 / 關卡性質
    chapter_of, group_of = {}, {}
    for gid, letter, _label, ids in CHAPTERS:
        for sid in ids:
            chapter_of[sid] = letter
            group_of[sid] = gid

    fix = collections.Counter()
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
        # 段落結構修復（表格／清單／編號）→ 粗體降噪 → 交叉參照連結化。
        # 前兩步只動標記不動字，最後以指紋比對確認一字未失。
        before = R.fingerprint(s["html"])
        s["html"] = R.restructure(s["html"], fix)
        s["html"] = R.denoise_bold(s["html"], fix)
        if R.fingerprint(s["html"]) != before:
            sys.exit(f"[build] 結構修復動到了內容：{s['id']}")
        s["html"] = linkify(s["html"], skip=s["id"])

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

    # 側欄的考試日改成由考試日算出，避免與內文各處的星期標示各說各話
    if '天後口試　·　9/5（五）' not in html:
        sys.exit("[build] 找不到側欄倒數的日期標示")
    if '<div class="hint" id="stat"></div>' not in html:
        sys.exit("[build] 找不到側欄統計列，無法插入筆記工具列")
    html = html.replace('<div class="hint" id="stat"></div>',
                        '<div class="hint" id="stat"></div>\n'
                        '      <a class="voicelink" href="voice/index.html">'
                        '<span class="vi">▶</span>'
                        '<span class="vt">12 集語音課程</span>'
                        '<span class="vs">用 Safari 朗讀・107 題</span></a>\n'
                        '      <div class="progress" id="progress"></div>\n'
                        '      <div class="tools" id="tools"></div>', 1)

    html = html.replace('天後口試　·　9/5（五）',
                        '天後口試　·　<span id="cddate">—</span>', 1)

    html = html.replace("</style>\n<style>", "</style>\n<style>", 1)
    last_style = html.rfind("</style>")
    html = html[:last_style] + EXTRA_CSS + html[last_style:]

    OUT.write_text(html, encoding="utf-8")

    # 純文字版：同一份資料另外產出靜態 HTML，供不執行 JS 的抓取工具讀取
    import datetime
    days = max(0, (P.EXAM - datetime.date.today()).days)
    n_sec, n_bundle = P.emit(
        sections, rows, ROOT / "plain",
        group_label=lambda g: dict(
            [("start", "開始這裡"), ("index", "押題・索引・衝突裁決"),
             ("notes", "各章速記卡與附錄"), ("check", "事實查核與缺口")]
            + [(k, v) for k, v in DOMAINS]
            + [(gid, label) for gid, _l, label, _ids in CHAPTERS]).get(g, g),
        dom_label=lambda d: DOMAIN_LABEL.get(d, d),
        days=days)

    n_ep, n_q = V.emit(ROOT / "_build" / "scripts", ROOT / "voice")

    linked = sum(1 for r in rows if r["go"])
    ex_linked = sum(1 for r in rows for e in r["ex"] if e["id"])
    ex_total = sum(len(r["ex"]) for r in rows)
    print(f"[build] 寫出 {OUT}  ({OUT.stat().st_size/1024/1024:.2f} MB)")
    print(f"[build] 節數 {len(sections)}（原 {len(sections)+len(dropped)}，第一部 11 節併為 1）")
    print(f"[build] 索引 {len(rows)} 列：主題可跳轉 {linked}，考官名牌 {ex_linked}/{ex_total}")
    print(f"[build] 純文字版：plain/ 共 {n_sec} 節頁 + {n_bundle} 份合輯 + 目錄")
    print(f"[build] 語音課程：voice/ 共 {n_ep} 集、{n_q} 題")
    if new_topics:
        print(f"[build] 補寫主題節 {len(new_topics)} 節："
              + "、".join(f"{t['id']} {t['title'].split('（')[0]}" for t in new_topics))
    if md_stats:
        before = sum(a for a, _ in md_stats.values())
        after = sum(b for _, b in md_stats.values())
        print(f"[build] 內容換版：{len(md_stats)} 節改用校訂版 markdown"
              f"（{before//1000}k → {after//1000}k 字，{(after-before)/before*100:+.1f}%）")
        if md_report["missing_files"]:
            print(f"[build]   缺少來源檔，維持原內容：{md_report['missing_files']}")
    print(f"[build] 結構修復：還原表格 {fix['tables']} 張（{fix['table_rows']} 列）、"
          f"清單 {fix['items']} 項、粗體降噪 {fix['debolded']} 塊")
    if unmatched:
        print(f"[build] 無對應主題節（維持純文字）{len(unmatched)} 列：")
        for u in unmatched:
            print(f"          · {u}")


if __name__ == "__main__":
    main()
