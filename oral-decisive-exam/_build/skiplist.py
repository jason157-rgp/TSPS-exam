#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
可以跳過的考官（同院已有人確定出場）

推論：114 年的 15 站是「一院一位」（已驗證：15 家醫院、15 位考官、無重複）。
若某家醫院今年的名額已由同學回報的某位老師佔住，同院其他考官的考古題
就不會再出現。

但這一節只做「標記」不做「刪除」——因為跳過的是考官檔案，不是主題。
很多主題會被其他考官接住，也有少數會真的消失，那些要另外補。
"""
import re

SID = "s0skip"
TITLE = "⏭ 可以跳過的考官（同院已有人確定出場）"
SUB = "115 年　14 位可跳過 · 19 位保留"

# (節代號, 醫院, 姓名, 年份, 被誰取代)
GREEN = [
    ("s52", "三總", "陳天牧", "104–111", "曾元生"),
    ("s54", "北榮", "馬旭", "104–111", "彭成康"),
    ("s55", "新光", "林煌基", "104–111", "林育賢"),
    ("s58", "成大", "李經維", "104–107", "潘信誠"),
    ("s59", "成大", "謝式洲", "109–111", "潘信誠"),
    ("s64", "國泰", "劉致和", "104–105", "蒲啟明"),
    ("s72", "國泰", "呂旭彥", "111", "蒲啟明"),
    ("s66", "高醫", "賴春生", "104", "郭耀仁"),
    ("s68", "高醫", "張高評", "105", "郭耀仁"),
    ("s73", "高雄長庚", "林燦勳", "111", "江原正"),
    ("s63", "台大", "洪學義", "104–105", "戴浩志"),
]

# 開啟「隱藏今年不會出的」時，連同這些主題節一起藏起來。
# 只收「跳過之後真的沒有人會問、而且丟掉也安全」的；被救回或屬基本盤的一律不藏。
HIDE_TOPICS = [
    ("tp151", "腮腺腫瘤：Warthin vs pleomorphic adenoma"),
    ("tp152", "腮腺切除術的步驟與顏面神經定位"),
    ("tp154", "Frey's syndrome（味覺出汗症候群）"),
    ("tc9", "上眶裂症候群與眶尖症候群"),
    ("tc16", "鼻淚管損傷與阻塞"),
    ("th75", "血管球瘤（Glomus tumor）"),
]

# 明明只有被跳過的考官會問，但我刻意不藏的，以及理由
KEPT_ORPHAN = [
    ("tb124", "傷口的基本處置與 LACERATE 口訣", "最基礎、最不該失分的一塊，任何關都可能順口問"),
    ("tb125", "破傷風的預防", "同上"),
    ("th76", "甲床解剖與甲溝炎", "簡守信的指甲下黑色病灶三連問會碰到甲床"),
    ("tc21", "顏面不對稱與腫瘤的 MRI 判讀", "正顎那一節會用到"),
    ("tp155", "抽脂的浸潤液與安全上限", "⭐ 林育賢的美容刀含 liposuction"),
    ("tm102", "Breast ptosis 分級與 mastopexy", "林育賢做 breast；陳宏基也在乳房線"),
    ("tm104", "隆乳術前測量與術後變形", "同上"),
    ("tm103", "Tuberous breast 與 Poland syndrome", "林育賢做 breast，但冷門，優先度低"),
    ("to37", "球後出血——眼周手術唯一的失明急症", "⭐ 三關都做眼整形，而且是失明急症"),
    ("to35", "下眼瞼成形術／眼袋", "同上"),
    ("tc7", "術後劇痛失明：球後出血", "同上"),
    ("tc5", "眶底與下眼瞼手術入路的比較", "李書欣若保留就還在；陳志豪與林育賢的顱顏線也會碰"),
    ("tc6", "眶底骨折的肌肉問題與白眼爆裂", "同上"),
]
AMBER = [
    ("s39", "高雄長庚", "謝青華", "114", "江原正",
     "他是<strong>去年（114）的考官</strong>，而且跳過他會讓<strong>整塊靜脈潰瘍（7 節）</strong>沒有人問——"
     "包含 CEAP、ABI、壓迫治療門檻、Fontaine 分級。"
     "⭐ 這些是慢性傷口的共同基礎，<strong>建議保留主題、只跳過他的考官檔案</strong>。"),
]
RED = [
    ("s47", "慈濟", "李俊達", "114", "簡守信",
     "⚠⚠ <strong>前提不成立。</strong>手冊把兩位都標成「慈濟」，但"
     "<strong>簡守信是台中慈濟院長、李俊達是花蓮慈濟整形外科主任——是兩家醫院</strong>，"
     "彼此不互相排擠。而且李俊達的淋巴水腫 LVA／VLNT 題在 114 年是多位考生同題。"
     "<strong>不要跳過。</strong>"),
    ("s46", "高醫", "李書欣", "114", "郭耀仁",
     "⚠ <strong>取代他的依據是我的推論，不是同學說的。</strong>回報郭耀仁的同學沒有說醫院，"
     "是我從官網查到他已由長庚轉任高醫。若這個推論錯了，李書欣（114 年、外傷評估全流程）就還在。"
     "<strong>建議保留</strong>，至少把 ATLS → ZMC 那條主線讀完。"),
]

# 跳過 GREEN 之後真的沒有人會問的主題 → (節代號, 判定, 理由)
ORPHAN = [
    ("tp151", "🔴 真的消失", "腮腺腫瘤：Warthin vs pleomorphic adenoma", "馬旭是唯一問腮腺的考官"),
    ("tp152", "🔴 真的消失", "腮腺切除術的步驟與顏面神經定位", "同上"),
    ("tp154", "🔴 真的消失", "Frey's syndrome", "同上；⭐ 但語音課 EP12 第九題有完整版，聽一遍就好"),
    ("tb124", "🟠 別跳", "傷口的基本處置與 LACERATE 口訣", "林煌基唯一，但這是<strong>最基礎、最不該失分</strong>的一塊，任何關都可能順口問"),
    ("tb125", "🟠 別跳", "破傷風的預防", "同上"),
    ("tp155", "🟢 被救回", "抽脂的浸潤液與安全上限", "⭐ <strong>林育賢的美容刀以眼整形、breast、liposuction 為主</strong>〔同學回報〕——這一節反而更該讀"),
    ("tm102", "🟢 被救回", "Breast ptosis 分級與 mastopexy", "⭐ 林育賢做 breast；陳宏基（中國醫）也在乳房線上"),
    ("tm104", "🟢 被救回", "隆乳術前測量與術後變形", "同上；且已補寫〈植入物手術的預防性抗生素〉"),
    ("tm103", "🟠 半救回", "Tuberous breast 與 Poland syndrome", "林育賢做 breast，但這是冷門題，優先度低"),
    ("to37", "🟢 被救回", "球後出血——眼周手術唯一的失明急症", "⭐ <strong>林育賢、陳理維、蒲啟明三關都做眼整形</strong>；而且這是失明急症，不管誰問都不能不會"),
    ("to35", "🟢 被救回", "下眼瞼成形術／眼袋", "同上"),
    ("tc7", "🟢 被救回", "術後劇痛失明：球後出血", "同上"),
    ("tc5", "🟠 半救回", "眶底與下眼瞼手術入路的比較", "若保留李書欣就還在；陳志豪（基隆長庚）與林育賢的顱顏線也會碰"),
    ("tc6", "🟠 半救回", "眶底骨折的肌肉問題與白眼爆裂", "同上"),
    ("tc9", "🔴 真的消失", "上眶裂症候群與眶尖症候群", "陳天牧唯一；冷門，可以跳"),
    ("tc16", "🔴 真的消失", "鼻淚管損傷與阻塞", "李經維唯一；冷門，可以跳"),
    ("tc21", "🔴 真的消失", "顏面不對稱與腫瘤的 MRI 判讀", "李經維唯一；⚠ 但正顎那一節會用到，順便看一眼"),
    ("th75", "🔴 真的消失", "血管球瘤（Glomus tumor）", "李經維唯一；冷門，可以跳"),
    ("th76", "🔴 真的消失", "甲床解剖與甲溝炎", "謝式洲與李經維；⚠ 但簡守信的指甲下黑色病灶三連問會碰到甲床，別完全丟"),
]

UNKNOWN = [
    ("台大", "戴浩志", "114", "顯微重建"),
    ("馬偕", "董光義", "114", "皮膚腫瘤・局部皮瓣"),
    ("中國醫", "陳宏基", "114", "顯微重建・乳房"),
    ("奇美", "邱浩遠", "114", "手外科"),
    ("林口長庚", "林有德", "114", "手外科・周邊神經"),
    ("義大", "施翔順", "114", "未任考官"),
    ("基隆長庚", "陳志豪", "111", "顱顏"),
    ("嘉義長庚", "林志鴻", "104–105", "周邊神經"),
]
UNKNOWN = [u for u in UNKNOWN if u[0] != "台大"]

INTRO = """
<p><strong>推論的前提</strong>：<strong>一院一位</strong>。這一點我驗證過了——
114 年的 15 站正好是 <strong>15 家醫院、15 位考官、沒有任何一家重複</strong>。所以某家醫院今年的名額
一旦被同學回報的某位老師佔住，同院其他考官的考古題就不會再出現。</p>

<p><strong>但這一節只做標記，不做刪除</strong>，理由是：<strong>跳過的是「考官檔案」，不是「主題」。</strong>
很多主題會被其他考官接住；少數會真的消失，那些要另外決定要不要補。
下面第三張表就是在算這件事。</p>

<p><strong>省下多少</strong>：考官章共 <strong>286k 字</strong>。跳過建議的那 11 位＝省 <strong>75k 字（26%）</strong>；
若連 🟠 的謝青華也跳，再省 12k。</p>
"""

CLOSE = """
<h3>⚠ 三件要提醒的事</h3>
<ol>
<li><strong>「一院一位」是從 114 年推出來的規律，不是公告的規則。</strong>
它在 114 年成立，但沒有人保證 115 年一定一樣。跳過等於在賭這條規律——
所以我把它做成<strong>標記而不是刪除</strong>，你隨時可以回頭讀。</li>
<li><strong>同學回報本身也是傳聞。</strong>如果哪一關的回報後來被推翻，對應的「可跳過」也要跟著失效。</li>
<li><strong>已經讀過的不要為了這張表回頭刪。</strong>時間只剩幾天，這張表的用途是
<strong>決定接下來讀什麼</strong>，不是回頭否定已經讀過的東西。</li>
</ol>
"""


def _jump(label, sid):
    return f'<button type="button" class="jump" data-go="{sid}">{label}</button>'


def html():
    out = [INTRO, "<h3>🟢 建議跳過（11 位）</h3>",
           "<p>共通點：都是<strong>舊期（104–111）</strong>的考官，而且該院 115 年的名額"
           "已由另一位老師佔住。</p>",
           '<table><thead><tr><th>醫院</th><th>考官</th><th>年份</th>'
           '<th>被誰佔住名額</th><th>檔案</th></tr></thead><tbody>']
    for sid, hosp, name, yr, by in GREEN:
        out.append(f"<tr><td>{hosp}</td><td><strong>{name}</strong></td><td>{yr}</td>"
                   f"<td>{by}</td><td>{_jump('看一眼', sid)}</td></tr>")
    out += ["</tbody></table>", "<h3>🟠 可以跳過，但要先看清單（1 位）</h3>"]
    for sid, hosp, name, yr, by, why in AMBER:
        out.append(f"<h4>{hosp}　{name}（{yr}）　被 {by} 佔住</h4><p>{why}　{_jump('看檔案', sid)}</p>")
    out.append("<h3>🔴 不建議跳過（2 位）——前提有問題</h3>")
    for sid, hosp, name, yr, by, why in RED:
        out.append(f"<h4>{hosp}　{name}（{yr}）</h4><p>{why}　{_jump('看檔案', sid)}</p>")

    out += ["<h3>⭐ 跳過之後，這 19 個主題誰來問？</h3>",
            "<p>這是本節最重要的一張表。跳過那 11 位之後，理論上沒有其他考官檔案會問到這些主題——"
            "<strong>但其中有一半被今年的情報救回來了</strong>，因為確定出場的老師的專長涵蓋到它們。</p>",
            '<table><thead><tr><th>主題</th><th>判定</th><th>為什麼</th></tr></thead><tbody>']
    for tid, verdict, name, why in ORPHAN:
        out.append(f"<tr><td>{_jump(name, tid)}</td><td>{verdict}</td><td>{why}</td></tr>")
    out += ["</tbody></table>",
            "<p><strong>結論</strong>：真的可以連主題一起丟的只有 <strong>上眶裂症候群、鼻淚管損傷、"
            "血管球瘤</strong> 三個冷門題；<strong>腮腺那三節</strong>（腮腺腫瘤、腮腺切除、Frey's syndrome）"
            "沒有人會問了，但語音課 <strong>EP12 第九題</strong>有完整版，聽一遍就夠。"
            "其餘要嘛被救回來、要嘛是不該失分的基本盤。</p>",
            "<h3>🙈 開啟「隱藏今年不會出的」會藏起什麼</h3>",
            '<p>側欄「未讀」那一列有一個 <strong>隱藏今年不會出的</strong> 開關。'
            '打開之後，導覽與搜尋都不會再出現下面這些節——但<strong>內容一個字都沒有刪</strong>，'
            '關掉開關就全部回來，正在讀的那一節也不會被藏掉。</p>',
            "<h4>會藏起來的：11 位考官 ＋ 6 個主題</h4>",
            '<table><thead><tr><th>類別</th><th>節</th></tr></thead><tbody>',
            "<tr><td><strong>考官檔案</strong></td><td>"
            + "、".join(_jump(f"{h}　{n}", sid) for sid, h, n, _y, _b in GREEN)
            + "</td></tr>",
            "<tr><td><strong>主題</strong></td><td>"
            + "、".join(_jump(n, tid) for tid, n in HIDE_TOPICS)
            + "</td></tr>",
            "</tbody></table>",
            "<h4>⚠ 只有被跳過的考官會問，但我刻意<u>不藏</u>的 13 個</h4>",
            "<p>這些照理說也該消失，但丟掉的風險大於省下的時間。</p>",
            '<table><thead><tr><th>主題</th><th>為什麼留著</th></tr></thead><tbody>',
            *[f"<tr><td>{_jump(name, tid)}</td><td>{why}</td></tr>"
              for tid, name, why in KEPT_ORPHAN],
            "</tbody></table>",
            "<h3>這 7 家還沒有情報——不能跳</h3>",
            "<p>沒有同學回報，代表 114 年的那位<strong>有可能續任</strong>，也可能換人。這些一律照常準備。</p>",
            '<table><thead><tr><th>醫院</th><th>114／最近一次的考官</th><th>年份</th><th>領域</th></tr></thead><tbody>']
    for hosp, name, yr, dom in UNKNOWN:
        out.append(f"<tr><td>{hosp}</td><td><strong>{name}</strong></td><td>{yr}</td><td>{dom}</td></tr>")
    out += ["</tbody></table>", CLOSE]
    return "\n".join(out)


def strip_tags(s):
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def section():
    h = html()
    names = " ".join(f"{h_} {n}" for _s, h_, n, *_ in GREEN + [a[:5] for a in AMBER] + [r[:5] for r in RED])
    return {
        "id": SID, "title": TITLE, "sub": SUB,
        "group": "start", "tags": [], "level": "",
        "headline": "114 年是一院一位——今年名額已被佔住的醫院，同院舊考官的考古題可以不用讀",
        "html": h, "text": (TITLE + " " + names + " " + strip_tags(h)).strip(),
        "name": "", "axis": "both", "topicIds": [],
        "refIds": [], "refNames": [],
    }


def bar(sid):
    for s, hosp, name, yr, by in GREEN:
        if s == sid:
            return ('<p class="skipbar">⏭ <strong>這一關今年應該不會出現</strong>：'
                    f'{hosp}的名額已由 {by} 佔住（114 年是一院一位）。'
                    f'　{_jump("為什麼可以跳過", SID)}</p>')
    for s, hosp, name, yr, by, _why in AMBER:
        if s == sid:
            return ('<p class="skipbar">⏭ <strong>考官檔案可以跳過，但主題要留</strong>：'
                    f'{hosp}的名額已由 {by} 佔住；不過跳過他會讓整塊靜脈潰瘍沒人問。'
                    f'　{_jump("看清單", SID)}</p>')
    return None


def bar_ids():
    return [s for s, *_ in GREEN] + [a[0] for a in AMBER]


def hidden_ids():
    """開關打開時要藏起來的節：跳過的考官 ＋ 只有他們會問的安全主題。"""
    return [s for s, *_ in GREEN] + [t for t, _n in HIDE_TOPICS]
