#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
今年確定出場的考官 × 老師本人給的提示

〈考前情報更新〉那一節做的是「同學回報 vs 手冊記載」的對照；這一節只收
一種東西：**老師自己說出口的提示**。這些不是推測、不是考古題統計，
是本人講的，所以視為一定會考的範圍。

每一位都寫成「原話 → 判讀 → 一定要會的題目 → 去哪一節準備」，
每一條都直接連到手冊的節。考官姓名寫成純文字，交給 build.py 的
linkify 自動接到各自的考官檔案。
"""
import re

SID = "s0hint"
TITLE = "🎯 今年確定出場的考官 × 老師本人給的提示"
SUB = "115 年　九關・老師親口說的範圍"

# (醫院, 姓名, 考官檔案節代號或 None, 原話, 出處, 判讀, [(該會的題目, [(標籤, 節代號)], 狀態)])
BLOCKS = [
    ("長庚", "林政輝", None,
     "專長：正顎手術、睡眠醫學（OSA 正顎治療）、唇顎裂。"
     "⚠ 老師是<strong>第一次當面試考官</strong>，說還要思考一下怎麼出題。",
     "許智凱・8/30",
     "第一次當考官、而且本人還沒想好題目——這代表他<strong>幾乎一定出自己的專長加教科書標準題</strong>，"
     "不會出刁鑽考古題。<strong>他講的三個專長，就是三個必考範圍</strong>，範圍反而是九關裡最好抓的。"
     "⚠ 手冊 33 位考官檔案裡沒有他。",
     [("唇顎裂：手術時序表、分類、修補術式、VPI", [], "⏳ 待補寫"),
      ("正顎：Le Fort I／BSSO／IVRO、cephalometric、順序、surgery-first", [], "⏳ 待補寫"),
      ("OSA：MMA 的機轉與成效、counterclockwise 加 mandible-first", [], "⏳ 待補寫"),
      ("現在就能讀的：虛擬手術規劃與患者專屬植入物",
       [("VSP／PSI", "tc19"), ("下顎骨折", "tc12")], "✅ 手冊已有")]),

    ("北榮", "彭成康", "s30",
     "主任人很好，但說<strong>要翻相簿找一些少見的 case</strong>；"
     "有提到之前遇到一個 <strong>Klippel–Trénaunay syndrome</strong>。",
     "李睿明・8/28",
     "「翻相簿找少見 case」等於明講<strong>照片題、而且不走考古題</strong>。"
     "這種關手冊幫不上題目，<strong>分數來自打法不是題庫</strong>——他最後會說「這題沒有標準答案」，"
     "評的是推理過程與說話方式。",
     [("ISSVA 分類要能秒答（KTS ＝ CLVM，PIK3CA）",
       [("血管腫瘤 vs 血管畸形", "tb127")], "✅ 手冊已有"),
      ("KTS 的三徵、與 Parkes Weber 的分界、治療與那條紅線", [], "⏳ 待補寫"),
      ("這一關的四條贏法：不要沉默、用框架、角色扮演真的問診、倫理要選邊站",
       [("彭成康那一關", "s30")], "✅ 手冊已有")]),

    ("高榮", "陳理維", "s45",
     "人很好；<strong>case 為主</strong>；有在做<strong>美容手術、BPI、手外科</strong>；"
     "主任說大家輕鬆回答就好，不會問太難。",
     "曾昱翔・8/28",
     "⭐ <strong>手冊記的次專長完全命中</strong>——「手外科、周邊神經；近年興趣為 BPI → Oberlin transfer」。"
     "⚠ 「不會問太難」跟手冊記的「問題連發、答完一題立刻下一題」<strong>不衝突</strong>："
     "題目不難但<strong>量大</strong>，所以要慢慢答、每題把清單倒完，答太快只會換來更多題。"
     "唯一新增的是<strong>美容</strong>這條線。",
     [("BPI → Oberlin transfer", [("神經轉移總論", "th48")], "✅ 手冊已有"),
      ("Ptosis 術後對側下垂／Hering's law（與林育賢第四題重疊）",
       [("陳理維那一關", "s45")], "✅ 手冊已有"),
      ("爪形手的四層治療階梯", [("爪形手", "th46")], "✅ 手冊已有"),
      ("顏面神經的解剖與分枝", [("顏面神經解剖", "tc18")], "✅ 手冊已有"),
      ("⭐ 美容（這次新增的線）",
       [("拉皮與 SMAS", "tp150"), ("美容題群", "tp157")], "✅ 手冊已有")]),

    ("台中慈濟", "簡守信", "s53",
     "人很好；<strong>歷屆看起來考古題固定</strong>；結論：考古題背熟。",
     "羅子憲・8/27",
     "⭐ <strong>這是九關裡唯一一關「背熟就會過」的。</strong>"
     "手冊寫的是「出席 7 屆、題庫幾乎逐年原封不動」，而且已經逐題收錄。"
     "⚠ 唯一的風險不是不會，是<strong>講太慢時間到</strong>——照片有 7 到 8 張，每張抓 40 到 60 秒。",
     [("整節逐題背熟：指甲下黑色病灶三連問、酒精燈、足底 ALM",
       [("簡守信那一關", "s53")], "✅ 手冊已有"),
      ("Melanoma 全套（他的招牌題，郭耀仁 110 年也沿用）",
       [("黑色素瘤全套", "tp140")], "✅ 手冊已有")]),

    ("成大", "潘信誠", "s36",
     "專長為<strong>高壓氧、軟組織惡性腫瘤、慢性傷口</strong>；"
     "<strong>會準備幾個題目，進去抽題</strong>；主任表示不用太緊張。",
     "Vivi・8/27",
     "⚠ <strong>他講的專長跟手冊記的不一樣。</strong>手冊記的是手外科／顯微重建，114 年題目是四指斷指再植。"
     "而且是<strong>抽題</strong>——沒有僥倖空間，<strong>兩邊都要備</strong>。",
     [("高壓氧：適應症、參數、機轉、禁忌與併發症", [], "⏳ 待補寫（指引層級）"),
      ("軟組織惡性腫瘤：切片原則、影像分期、切緣、放療時機", [], "⏳ 待補寫"),
      ("慢性傷口與糖尿病足", [("慢性傷口系統性評估", "tb120")], "✅ 手冊已有"),
      ("斷指再植（手冊記載的 114 年題，不能因為新情報就丟掉）",
       [("潘信誠那一關", "s36"), ("再植適應症與缺血時間", "th58"),
        ("優勢指動脈與 1A:2V", "th60")], "✅ 手冊已有")]),

    ("醫院未報", "郭耀仁", None,
     "專長是<strong>顯微重建手術、手外科</strong>；<strong>會準備好幾個題目，進去抽題</strong>；"
     "考完會開始聊天。",
     "Benjamin・8/26",
     "⚠ 手冊<strong>沒有他的考官檔案</strong>，只知道他 <strong>110 年沿用了簡守信的 melanoma 照片題組</strong>。"
     "抽題形式跟潘信誠、林育賢同型，所以一樣是<strong>範圍要備滿、不能押單題</strong>。",
     [("Melanoma 全套（他考過的題）", [("黑色素瘤全套", "tp140")], "✅ 手冊已有"),
      ("顯微重建主線",
       [("常用游離皮瓣總表", "tm88"), ("Flap 監測與搶救", "tm91"),
        ("一期複合重建", "tm97")], "✅ 手冊已有"),
      ("手外科主線", [("肌腱轉移六大原則", "th56"), ("爪形手", "th46")], "✅ 手冊已有")]),

    ("高雄長庚", "江原正", "s61",
     "<strong>和藹的長輩，聽力稍差要大聲一點回答</strong>；專長手外科、"
     "<strong>congenital hand anomalies、hand tumors</strong>；情境題為主；"
     "也曾經考過<strong>請考生畫一隻手</strong>接著自由出題。",
     "寧・8/26",
     "⭐ 四項特徵全中手冊的檔案：先天手（足）畸形、skin tumor、108 年考過「畫手找錯」。"
     "手冊記他是「口試的大魔王」、幾乎每年出新題，"
     "但<strong>主軸永遠是先天手足畸形加手部基本功，評分永遠看描述的完整度</strong>。",
     [("⭐ 拿到照片先完整描述、最後才給診斷（診斷猜錯不致命，描述不完整才致命）",
       [("江原正那一關", "s61")], "✅ 手冊已有"),
      ("先天性併指", [("先天性併指", "th79")], "✅ 手冊已有"),
      ("畫手：腕骨解剖與 Kaplan's cardinal line",
       [("腕骨解剖", "th64")], "✅ 手冊已有"),
      ("實務提醒：<strong>聽力稍差，回答要大聲</strong>；PE 不要漏掉 arm 與 upper arm；"
       "完全沒概念時問考官病人的基本資料", [], "📌 現場執行")]),

    ("三總", "曾元生", "s31",
     "幽默風趣，大家不用擔心；要考 <strong>pressure ulcer 評估處置</strong>；"
     "副院長<strong>很喜歡 primary closure ＋ ciNPWT</strong>。",
     "翁御哲・8/26",
     "⭐ <strong>這個提示等於把題目直接講出來了。</strong>手冊 s31 一字不差——"
     "連「他最後會主動引導到『其實也沒有不能 primary closure』並秀出自己的照片」都寫在裡面。"
     "語音課 <strong>EP11 第七題</strong>就是這一題。",
     [("壓瘡分期與現行用語（NPIAP 2016，pressure injury 不是 ulcer）",
       [("壓瘡分期", "tb115")], "✅ 手冊已有"),
      ("系統性評估：Braden、營養、骨髓炎、照護環境",
       [("壓瘡的系統性評估", "tb116")], "✅ 手冊已有"),
      ("⭐ 治療階梯與 primary closure 的爭議（本關勝負手）",
       [("治療階梯與 primary closure", "tb117"), ("NPWT 與敷料選擇", "tb123")], "✅ 手冊已有"),
      ("皮瓣選擇與各部位定式", [("壓瘡的皮瓣選擇", "tb118")], "✅ 手冊已有"),
      ("🔴 紅線：<strong>絕對不要說「這個不能 primary closure」</strong>，"
       "而且一定要從階梯最底層講起", [], "📌 現場執行")]),

    ("新光", "林育賢", "s48",
     "<strong>implant-based breast augmentation，antibiotics 怎麼給？</strong>"
     "（主任的專長是 <strong>buccal ca. recon</strong>；"
     "美容刀以<strong>眼整形、breast、liposuction</strong> 為主）",
     "馬玉坤・8/26",
     "⭐ <strong>九關裡最具體的一個提示——題目本身被講出來了。</strong>"
     "⚠ 而且這一題手冊原本會害你答錯：既有幾節寫的「一般乾淨傷口不需要預防性抗生素」是<strong>裂傷</strong>的答案，"
     "有植入物完全相反。這一節已經補寫。"
     "他先聊天兩分鐘再抽題，至少四題可抽，<strong>四題全備沒有僥倖</strong>。",
     [("🔴 隆乳的預防性抗生素與 pocket irrigation",
       [("植入物手術的預防性抗生素", "tm201")], "✅ 已補寫"),
      ("抽題四題全備（panfacial fracture 到 Hering's law）",
       [("林育賢那一關", "s48")], "✅ 手冊已有"),
      ("眼整形、breast、liposuction（他的美容刀）",
       [("美容題群", "tp157")], "✅ 手冊已有"),
      ("buccal ca. recon（頰黏膜癌重建）",
       [("常用游離皮瓣總表", "tm88")], "✅ 手冊已有")]),
]

INTRO = """
<p><strong>這一節只收一種東西：老師自己說出口的提示。</strong>不是考古題統計、不是我的推測——
是本人親口講的範圍，所以<strong>視為一定會考</strong>。〈考前情報更新〉那一節做的是「同學回報 vs 手冊記載」
的全面對照；這一節把其中<strong>最硬的那一塊單獨抽出來</strong>，每一條都直接連到該讀的節。</p>

<p><strong>怎麼用</strong>：先看下面的一覽表把 ⏳ 待補寫的認出來，那是目前手冊還接不住的部分；
其餘每一條都可以直接點進去讀。九關裡<strong>只有簡守信那一關是「背熟就會過」</strong>，
其他八關給的是<strong>範圍</strong>不是題目，所以要備滿。</p>

<p class="note">依你的指示，國泰 蒲啟明那一關不計分（只聊天），本節不列。</p>
"""

CLOSE = """
<h3>三個橫跨多關的共同訊號</h3>
<ol>
<li><strong>三關是「準備好幾題、進去抽」</strong>——潘信誠、郭耀仁、林育賢。
抽籤沒有僥倖，<strong>押單題是這三關唯一會輸的方式</strong>。</li>
<li><strong>多位主任主動說「不會問太難」「不用緊張」「輕鬆回答就好」。</strong>
今年整體語氣偏溫和，所以<strong>失分會出現在「講不完整」而不是「答不出來」</strong>——
把每一題的清單倒完，比答得快重要。</li>
<li><strong>兩關明講靠什麼</strong>：簡守信說靠考古題、彭成康說要翻相簿找少見 case——
剛好是光譜的兩端，準備方式完全相反，不要用同一套打法。</li>
</ol>

<p>⚠ 這一節全部是<strong>同學轉述的傳聞</strong>。可靠度低於手冊其他任何一節，但新鮮度最高。
如果後續有更新（尤其林政輝的出題方向），以新的為準。</p>
"""


def _jump(label, sid):
    return f'<button type="button" class="jump" data-go="{sid}">{label}</button>'


def _overview():
    out = ['<table>',
           '<thead><tr><th>醫院／考官</th><th>老師給的範圍</th><th>手冊接得住嗎</th></tr></thead>',
           '<tbody>']
    for hosp, name, _sid, _said, _src, _read, items in BLOCKS:
        todo = sum(1 for _t, _l, st in items if st.startswith("⏳"))
        state = f"⏳ 還缺 {todo} 項" if todo else "✅ 全部有"
        scope = "、".join(re.sub(r"<[^>]+>|（.*?）|^[🔴⭐📌]\s*", "", t).split("：")[0]
                          for t, _l, _st in items[:3])
        out.append(f"<tr><td><strong>{hosp}　{name}</strong></td>"
                   f"<td>{scope}</td><td>{state}</td></tr>")
    out += ['</tbody>', '</table>']
    return "\n".join(out)


def html():
    parts = [INTRO, "<h3>一覽</h3>", _overview(), "<h3>逐關</h3>"]
    for hosp, name, sid, said, src, read, items in BLOCKS:
        tag = "" if sid else "　<em>（手冊無考官檔案）</em>"
        parts.append(f"<h4>{hosp}　{name}{tag}</h4>")
        parts.append(f'<blockquote><p><strong>老師說的</strong>：{said}'
                     f'<br><span class="note">〔{src}〕</span></p></blockquote>')
        parts.append(f"<p><strong>判讀</strong>：{read}</p>")
        parts.append('<table><thead><tr><th>一定要會的</th><th>去哪裡讀</th><th>狀態</th></tr></thead><tbody>')
        for topic, links, state in items:
            where = "、".join(_jump(l, s) for l, s in links) or "—"
            parts.append(f"<tr><td>{topic}</td><td>{where}</td><td>{state}</td></tr>")
        parts.append("</tbody></table>")
    parts.append(CLOSE)
    return "\n".join(parts)


def strip_tags(s):
    s = re.sub(r"<[^>]+>", " ", s)
    for a, b in (("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"), ("&nbsp;", " ")):
        s = s.replace(a, b)
    return re.sub(r"\s+", " ", s).strip()


def section():
    h = html()
    # 全文搜尋要能用老師的名字命中這一節
    names = " ".join(f"{hosp} {name}" for hosp, name, *_ in BLOCKS)
    return {
        "id": SID, "title": TITLE, "sub": SUB,
        "group": "start", "tags": [], "level": "🔴",
        "headline": "老師親口說出來的範圍——不是推測，是一定會考的那一塊",
        "html": h, "text": (TITLE + " " + names + " " + strip_tags(h)).strip(),
        "name": "", "axis": "both", "topicIds": [],
        "refIds": [], "refNames": [],
    }


def banner(sid):
    """貼在該考官自己那一節最上面的提示條。"""
    for hosp, name, s, said, src, _read, _items in BLOCKS:
        if s == sid:
            return ('<p class="hintbar">🎯 <strong>今年老師本人給了提示</strong>：'
                    + re.sub(r"<[^>]+>", "", said)
                    + f'　〔{src}〕　'
                    + _jump("看這一關該準備什麼", SID) + "</p>")
    return None


def banner_ids():
    return [s for _h, _n, s, *_ in BLOCKS if s]
