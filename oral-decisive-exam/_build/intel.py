#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
考前情報更新（同學回報）

同學在群組回報的今年考官情報，逐則跟手冊既有的考官檔案對照，標出
「吻合／新增／衝突」，並把手冊真的沒有的部分列成缺口。

這一節放在卷首之後，是全手冊唯一一份「比手冊本身還新」的資料，
所以獨立一節、不併進任何章。
"""
import re

SID = "s0i"
TITLE = "🆕 考前情報更新（同學回報　8/26–8/30）"
SUB = "115 年　同學群組回報 × 手冊考官檔案對照"

INTRO = """
<p><strong>資料性質</strong>：以下全部是<strong>同學在群組回報的傳聞</strong>，不是考古題、
也不是教科書。可靠度低於本手冊其他任何一節，但<strong>新鮮度最高</strong>——
它講的是今年考官現在的狀態。用法是<strong>拿它去調整準備的權重，不是拿它去推翻手冊的內容</strong>。</p>

<p><strong>這批情報改變了三件事</strong>：</p>
<ol>
<li><strong>多出一位手冊完全沒有的考官</strong>（長庚 林政輝），而且他的三個專長在手冊裡是空白。</li>
<li><strong>成大 潘信誠的專長跟手冊記載不一致</strong>——手冊記手外科，同學回報是高壓氧與軟組織惡性腫瘤。兩邊都要備。</li>
<li><strong>至少三關是「準備好幾題、進去抽」</strong>（潘信誠、郭耀仁、林育賢）。抽題沒有僥倖，範圍要備滿，不能押單題。</li>
</ol>

<p>另外有一個共同訊號：<strong>多位主任主動說「不會問太難」「不用緊張」「輕鬆回答就好」</strong>。
今年整體語氣偏溫和，所以<strong>失分會出現在「講不完整」而不是「答不出來」</strong>——
把每一題的清單倒完，比答得快重要。</p>

<p class="note">依你的指示，<strong>國泰 蒲啟明</strong>那一關不計分（只聊天），本節不列。</p>
"""

# (醫院／考官, 判定, 一句話, 同學回報, 手冊對應, 你要做的)
ROWS = [
    ("長庚　林政輝", "🔴 全新",
     "手冊沒有這個人，三個專長全空白",
     "專長：正顎手術、睡眠醫學（OSA 正顎治療）、唇顎裂。"
     "⚠ 老師是<strong>第一次當口試考官</strong>，本人說還要想一下怎麼出題。"
     "〔許智凱・8/30〕",
     "<strong>手冊 33 位考官檔案裡沒有他。</strong>正顎只在 tc19（VSP／PSI）與李經維那關被順帶提到；"
     "OSA 與唇顎裂在全手冊是 <strong>0 筆</strong>。",
     "第一次當考官、又還沒想好題目，代表他<strong>幾乎一定出自己的專長 ＋ 教科書標準題</strong>，"
     "不會出刁鑽考古題。所以範圍反而最好抓：正顎的術式與順序、OSA 的診斷與手術階梯、唇顎裂的時序表。"),

    ("北榮　彭成康", "🟠 可能換方向",
     "改成翻相簿找少見 case，不是考古題",
     "主任人很好，但說<strong>要翻相簿找一些少見的 case</strong>；"
     "有提到之前遇到一個 <strong>Klippel–Trénaunay syndrome</strong>。〔李睿明・8/28〕",
     "手冊記的是 114 年的 post-TKR infection 下肢重建 ＋ 角色扮演倫理題。"
     "KTS 在手冊裡只到<strong>分類層級</strong>（＝CLVM，PIK3CA，見血管腫瘤 vs 血管畸形那一節），"
     "<strong>沒有 KTS 本身的診斷與處置</strong>。",
     "「翻相簿找少見 case」＝<strong>照片題、而且不是考古題</strong>。這種關手冊幫不上題目，只能靠打法："
     "彭成康那一節的四條贏法（不要沉默、用框架、角色扮演真的對他問診、倫理要選邊站）"
     "<strong>對任何題目都成立</strong>，那才是這關的分數來源。ISSVA 分類要能秒答。"),

    ("高榮　陳理維", "🟢 吻合",
     "手冊完全命中，只多一條美容線",
     "人很好；<strong>case 為主</strong>；有在做<strong>美容手術、BPI、手外科</strong>；"
     "主任說大家輕鬆回答就好，不會問太難。〔曾昱翔・8/28〕",
     "✅ <strong>手冊完全命中</strong>——陳理維那一節記的次專長就是"
     "「手外科、周邊神經；近年興趣為 BPI → Oberlin transfer、facial palsy → temporalis transfer」。"
     "唯一新增的是<strong>美容</strong>這條線。",
     "照手冊準備即可。⚠ 「不會問太難」跟手冊記的「問題連發、答完一題立刻下一題」<strong>不衝突</strong>——"
     "題目不難但<strong>量大</strong>，所以要慢慢答、每題把清單倒完，不要答太快換來更多題。"),

    ("台中慈濟　簡守信", "🟢🟢 最高吻合",
     "考古題固定，手冊已逐題收錄",
     "人很好；<strong>歷屆看起來考古題固定</strong>；結論：考古題背熟。〔羅子憲・8/27〕",
     "✅ 手冊寫的是「出席 7 屆、<strong>題庫幾乎逐年原封不動</strong>」，"
     "而且已經逐題收錄（指甲下黑色病灶三連問、酒精燈、足底 ALM…）。"
     "<strong>這是全手冊準備度最高的一關。</strong>",
     "把簡守信那一節從頭到尾背熟就好，不必再找新東西。"
     "唯一要盯的是節奏：照片有 7–8 張，<strong>每張抓 40–60 秒</strong>，"
     "手冊記過考生的教訓是「講太慢時間到」。"),

    ("成大　潘信誠", "🔴 與手冊不一致",
     "專長與手冊不一致，兩邊都要備",
     "專長為<strong>高壓氧、軟組織惡性腫瘤、慢性傷口</strong>；"
     "<strong>會準備幾個題目，進去抽題</strong>；主任表示不用太緊張。〔Vivi・8/27〕",
     "⚠ 手冊記的次專長是<strong>手外科／顯微重建</strong>，114 年題目是四指斷指再植。"
     "慢性傷口手冊是齊的（慢性傷口系統性評估、NPWT、放療後不癒等）；"
     "但<strong>高壓氧只以「輔助手段」四個字出現在清單裡，沒有專章</strong>；"
     "軟組織惡性腫瘤也只有零星（DFSP、angiosarcoma）。",
     "<strong>兩邊都要備，而且是抽題，沒有僥倖。</strong>斷指那一套照舊（手冊已完整、語音課 EP05 有）；"
     "慢性傷口直接用既有章節 ＋ 語音課 EP11；<strong>高壓氧與軟組織肉瘤要補</strong>。"),

    ("郭耀仁教授（醫院未報）", "🟠 只有側面資料",
     "手冊無檔案；抽題，備顯微＋手外＋melanoma",
     "專長是<strong>顯微重建手術、手外科</strong>；<strong>會準備好幾個題目，進去抽題</strong>；"
     "考完會開始聊天。〔Benjamin・8/26〕",
     "手冊<strong>沒有他的考官檔案</strong>，只知道他<strong>110 年沿用了簡守信的 melanoma 照片題組</strong>"
     "（見押題排行榜與黑色素瘤那一節）。",
     "抽題形式跟潘信誠、林育賢同型。主線用顯微重建（語音課 EP09、EP10）"
     "＋ 手外科（EP03–EP06）；另外把 <strong>melanoma 全套備好</strong>，因為那是他考過的題。"),

    ("高雄長庚　江原正", "🟢🟢 完全命中",
     "手冊有完整檔案，照那一節準備即可",
     "高雄長庚 江原正醫師。和藹的長輩，<strong>聽力稍差要大聲一點回答</strong>；專長手外科、"
     "<strong>congenital hand anomalies、hand tumors</strong>；情境題為主；"
     "也曾經考過<strong>請考生畫一隻手</strong>接著自由出題。〔寧・8/26〕",
     "✅ 手冊有他的完整檔案："
     "次專長就是先天手（足）畸形 ＋ skin tumor（melanoma、NF、hemangioma、DFSP）；"
     "手冊也記了他 108 年考過「<strong>畫手找錯</strong>」。",
     "三條贏法：<strong>拿到照片先完整描述、最後才給診斷</strong>（診斷猜錯不致命，描述不完整才致命）；"
     "PE 不要漏掉 arm 與 upper arm；完全沒概念時<strong>問考官病人的基本資料</strong>（性別、年齡、左右手）。"
     "⚠ 手冊記他是「口試的大魔王」、「幾乎每年出新題」，"
     "但主軸永遠是先天手足畸形 ＋ 手部基本功，評分永遠看描述的完整度。"),

    ("三總　曾元生", "🟢🟢 完全命中",
     "一字不差，守住 primary closure 那條紅線",
     "幽默風趣，大家不用擔心；要考 <strong>pressure ulcer 評估處置</strong>；"
     "副院長<strong>很喜歡 primary closure ＋ ciNPWT</strong>。〔翁御哲・8/26〕",
     "✅ 手冊<strong>一字不差</strong>——連「他最後會主動引導到『其實也沒有不能 primary closure』，"
     "並秀出他自己 primary closure ＋ ciNPWT 的照片」都寫在裡面。"
     "語音課 <strong>EP11 第七題</strong>就是這一題。",
     "不用再準備了，只要守住紅線：<strong>絕對不要說「這個不能 primary closure」</strong>，"
     "而且一定要<strong>從階梯最底層講起</strong>，讓直接縫合自然出現在你的清單裡。"),

    ("新光　林育賢", "🟠 新題目",
     "隆乳抗生素是新題，手冊現有說法會帶錯",
     "<strong>implant-based breast augmentation，antibiotics 怎麼給？</strong>"
     "（主任專長是 <strong>buccal ca. recon</strong>；美容刀以<strong>眼整型、breast、liposuction</strong> 為主）"
     "〔馬玉坤・8/26〕",
     "領域吻合（手冊記他橫跨顱顏、乳房、眼整形、傷口壓瘡，先聊天兩分鐘再抽題）。"
     "但<strong>「隆乳的抗生素怎麼給」手冊沒有</strong>。"
     "⚠⚠ 更糟的是手冊現有的說法會<strong>害你答錯</strong>——"
     "傷口那幾節寫的是「一般乾淨傷口不需要預防性抗生素」，"
     "那是<strong>裂傷</strong>的答案；<strong>有植入物的隆乳完全相反</strong>。",
     "把「有植入物」這條線單獨拉出來背，不要跟裂傷混在一起。"
     "四題全備的原則不變（抽籤）。buccal ca. recon 用頭頸重建那條線（語音課 EP09）。"),
]

GAPS = [
    ("🔴 1", "正顎手術 · OSA 的正顎治療 · 唇顎裂", "長庚 林政輝",
     "全手冊 0 筆。而且他是新考官、必出自己的專長。", "最高"),
    ("🔴 2", "隆乳（有植入物）的預防性抗生素", "新光 林育賢",
     "手冊沒有，而且現有的「乾淨傷口不需要抗生素」會把你帶到相反的答案。", "最高"),
    ("🟠 3", "高壓氧治療（適應症、機轉、併發症）", "成大 潘信誠",
     "只以「輔助手段」四個字出現在慢性傷口的清單裡，沒有專章。", "高"),
    ("🟠 4", "軟組織惡性腫瘤的 workup 與切緣", "成大 潘信誠",
     "只有零星的 DFSP、angiosarcoma，沒有整條「切片原則 → 影像 → 分期 → 切緣 → 輔助治療」。", "高"),
    ("🟡 5", "Klippel–Trénaunay 的診斷與處置", "北榮 彭成康",
     "分類層級有（＝CLVM，PIK3CA），但沒有 triad、檢查與治療。", "中"),
]

CLOSE = """
<h3>怎麼用這一節</h3>
<ol>
<li><strong>先看「判定」那一欄。</strong>🟢 的四關（陳理維、簡守信、曾元生、江原正）
手冊已經夠了，<strong>不要再花時間</strong>，直接背既有章節。</li>
<li><strong>時間全部投到 🔴 與 🟠。</strong>五個缺口裡，
<strong>林政輝的正顎／OSA／唇顎裂</strong>與<strong>隆乳的抗生素</strong>是最急的兩個——
前者是一整關完全空白，後者是手冊現有內容會把你帶到錯的答案。</li>
<li><strong>抽題的三關（潘信誠、郭耀仁、林育賢）範圍要備滿。</strong>
抽籤沒有僥倖，押單題是這三關唯一會輸的方式。</li>
<li>⚠ 這一節全部是<strong>傳聞</strong>。如果同學後續有更新（尤其林政輝的出題方向），以新的為準。</li>
</ol>
"""


def _overview(rows):
    """一覽表：三欄，手機上也讀得完。"""
    out = ['<table>',
           '<thead><tr><th>醫院／考官</th><th>判定</th><th>一句話</th></tr></thead>', '<tbody>']
    for who, verdict, one, *_ in rows:
        out.append(f"<tr><td><strong>{who.replace('<br>', '')}</strong></td>"
                   f"<td>{verdict}</td><td>{one}</td></tr>")
    out += ['</tbody>', '</table>']
    return "\n".join(out)


def _detail(rows):
    """逐關細節：一關一塊，欄位直排，窄螢幕不會被壓成一條線。"""
    out = []
    for who, verdict, _one, said, book, todo in rows:
        out.append(f"<h4>{who.replace('<br>', ' ')}　{verdict}</h4>")
        out.append("<table>")
        out.append(f"<tr><th>同學回報</th><td>{said}</td></tr>")
        out.append(f"<tr><th>手冊對應</th><td>{book}</td></tr>")
        out.append(f"<tr><th>你要做的</th><td>{todo}</td></tr>")
        out.append("</table>")
    return "\n".join(out)


def _gaps(rows):
    out = ['<table>',
           '<thead><tr><th>#</th><th>缺口</th><th>因為誰</th><th>手冊現況</th><th>優先度</th></tr></thead>',
           '<tbody>']
    for n, topic, who, state, pri in rows:
        out.append(f"<tr><td>{n}</td><td><strong>{topic}</strong></td><td>{who}</td>"
                   f"<td>{state}</td><td>{pri}</td></tr>")
    out += ['</tbody>', '</table>']
    return "\n".join(out)


def html():
    return "\n".join([
        INTRO,
        "<h3>一覽</h3>",
        _overview(ROWS),
        "<h3>逐關對照</h3>",
        _detail(ROWS),
        "<h3>⚠ 這批情報照出來的五個缺口（手冊補不了的部分）</h3>",
        "<p>下面五項是<strong>本手冊目前沒有、或不足以應付</strong>的內容。"
        "列在這裡是為了讓你知道<strong>不要在手冊裡找</strong>，要另外準備。</p>",
        _gaps(GAPS),
        CLOSE,
    ])


def strip_tags(s):
    s = re.sub(r"<[^>]+>", " ", s)
    for a, b in (("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"), ("&nbsp;", " ")):
        s = s.replace(a, b)
    return re.sub(r"\s+", " ", s).strip()


def section():
    h = html()
    return {
        "id": SID, "title": TITLE, "sub": SUB,
        "group": "start", "tags": [], "headline": "同學回報的今年考官情報 × 手冊考官檔案逐關對照",
        "html": h, "text": (TITLE + " " + strip_tags(h)).strip(),
        "name": "", "axis": "both", "topicIds": [],
        "level": "", "refIds": [], "refNames": [],
    }
