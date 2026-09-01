#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
考官簡介與照片（醫院官網連結）

110 年之後仍有出題的考官，各自在服務醫院官網的醫師簡介頁。
點進去就是照片、學經歷與專長。

為什麼是連結不是內嵌照片：這個環境的網路政策擋掉所有醫院網站與圖床
（實測 CONNECT tunnel failed 403），抓不到圖檔。連結的另一個好處是
永遠是最新的，也不必轉載別人網站的照片。
"""

# (考官節代號 or None, 醫院, 姓名, 年份, 現職／專長一句話, 連結)
DOCS = [
    ("s29", "台大", "戴浩志", "114（今年確定出場）",
     "⭐ <strong>台灣整形外科醫學會理事長</strong>；台大整形外科主治醫師。頭頸顯微重建",
     "https://www.ntuh.gov.tw/surg/Vcard.action?q_type=7&q_itemCode=46"),
    ("s30", "北榮", "彭成康", "114",
     "外科部重建整形外科科主任",
     "https://wd.vghtpe.gov.tw/ps/Fpage.action?muid=1346&fid=937"),
    ("s31", "三總", "曾元生", "114",
     "行政副院長、燒傷中心主任；燒傷與傷口照護",
     "https://wwwv.tsgh.ndmctsgh.edu.tw/docdet/191/10060/24974/866"),
    ("s32", "馬偕", "董光義", "114",
     "燒燙傷中心副主任；燒燙傷、乳房重建、疤痕重整",
     "https://www.mmh.org.tw/doctor_view.php?depid=12&did=313"),
    ("s35", "中國醫", "陳宏基", "114",
     "國際醫療中心榮譽院長、整形外科教授；極困難重建、腸道移植發聲重建、淋巴重建",
     "https://www.cmuh.cmu.edu.tw/Doctor/DoctorInfo?docId=D19722"),
    ("s36", "成大", "潘信誠", "114",
     "整形外科主任、教授",
     "https://surgery.ncku.edu.tw/p/405-1126-124835,c15355.php?Lang=zh-tw"),
    ("s37", "奇美", "邱浩遠", "114",
     "整形外科顧問",
     "https://sub.chimei.org.tw/57550/index.php/members/15-members-list-01/13-hawyenchiu"),
    ("s38", "林口長庚", "林有德", "114",
     "外科部部長、專任教授；台灣手外科醫學會理事長。手腕外傷、周邊神經、足趾關節移植",
     "https://www.cgmh.org.tw/tw/Services/DoctorInfo/2254"),
    ("s39", "高雄長庚", "謝青華", "114",
     "整形外科教授級主治醫師；顯微與肢體重建、靜脈曲張",
     "https://www.cgmh.org.tw/tw/Services/DoctorInfo/4922"),
    ("s45", "高榮", "陳理維", "114",
     "整形外科主治醫師；燒傷、皮瓣移植、手外科、淋巴重建",
     "https://org.vghks.gov.tw/sur/News_DoctorList.aspx?n=FEF2EE17DCB68050&sms=1E32080A8E267B93"),
    ("s46", "高醫", "李書欣", "114",
     "外科部部主任、整形外科主任、手術室主任；顱顏外傷、燒傷、高壓氧",
     "https://www.kmuh.org.tw/Web/WebRegistration/DocIntro/DocDetail?lang=tw&doctorID=830170"),
    ("s47", "花蓮慈濟", "李俊達", "114",
     "整形外科主任、慈濟大學臨床教授；頭頸癌重建、糖尿病足、顯微重建",
     "https://hlm.tzuchi.com.tw/home/index.php/team-prs/dr0502"),
    ("s48", "新光", "林育賢", "114",
     "整形外科主任；顱顏重建、乳房重建、顯微重建、睡眠外科（史丹佛進修）",
     "https://skhcc.skh.org.tw/content/%E6%9E%97%E8%82%B2%E8%B3%A2-22"),
    ("s49", "義大", "施翔順", "114（未任考官）",
     "整形外科部部長、顯微重建外科主任",
     "https://webreg.edah.org.tw/Register/ChooseDoctorTime/2046"),
    ("s28", "國泰", "蒲啟明", "114",
     "整形外科主任（⚠ 這一關依你的指示不計分）",
     "https://www.cgh.org.tw/ec99/rwd1320/category.asp?category_id=342"),
    ("s52", "三總", "陳天牧", "104–111",
     "整形外科教授、醫學美容中心主任；前台灣整形外科醫學會理事長",
     "https://wwwv.tsgh.ndmctsgh.edu.tw/docdet/191/10060/24974/537"),
    ("s53", "台中慈濟", "簡守信", "104–111",
     "院長；皮膚腫瘤、頭頸腫瘤、慢性傷口、先天畸形。大愛「大愛醫生館」主持人",
     "https://taichungsub.tzuchi.com.tw/17/doctors/6/116"),
    ("s54", "北榮", "馬旭", "104–111",
     "整形外科主治醫師；台灣整形外科醫學會理事長、台灣燒傷暨傷口照護學會理事長",
     "https://wd.vghtpe.gov.tw/ps/Fpage.action?muid=1347&fid=938"),
    ("s55", "新光", "林煌基", "104–111",
     "整形外科主任級主治醫師；曾任三總整形外科主治醫師與燒傷中心主任",
     "https://skhcc.skh.org.tw/content/%E6%9E%97%E7%85%8C%E5%9F%BA-23"),
    ("s59", "成大", "謝式洲", "109–111",
     "醫學系系主任；顯微外科、手外科、頭頸重建、高壓氧、組織工程",
     "https://surgery.ncku.edu.tw/p/405-1126-124834,c15355.php?Lang=zh-tw"),
    ("s70", "基隆長庚", "陳志豪", "111",
     "整形外科教授、基隆長庚醫學研究部部長；顱顏整形、正顎削骨、3D 列印顱顏重建",
     "https://www.cgmh.org.tw/tw/Services/DoctorInfo/5027"),
    ("s71", "林口長庚", "林承弘", "111",
     "整形外科系系主任、教授；肢體與顯微重建、手外科、複合組織異體移植（手／臉移植）",
     "https://www.cgmh.org.tw/tw/Services/DoctorInfo/3690"),
    ("s72", "國泰", "呂旭彥", "111",
     "國泰顧問醫師、紐約整形外科診所院長；前中華民國美容外科醫學會理事長",
     "https://www.prsa.org.tw/people/map/content.php?id=1065"),
    ("s73", "高雄長庚", "林燦勳", "111",
     "整形外科主任、教授；顯微與肢體重建、乳房重建",
     "https://www.cgmh.org.tw/tw/Services/DoctorInfo/4438"),
    ("s61", "高雄長庚", "江原正", "104–107（今年確定出場）",
     "整形外科主治醫師、助理教授；手外科與先天手足畸形、皮膚軟組織腫瘤",
     "https://www.cgmh.org.tw/tw/Services/DoctorInfo/0137"),
    (None, "長庚", "林政輝", "今年新增",
     "⭐ <strong>整形外科顱顏中心主任、長庚睡眠中心主治醫師</strong>，副教授。"
     "專長正顎手術、睡眠呼吸中止症、唇顎裂及顱顏畸形；"
     "<strong>曾任美國史丹佛大學睡眠中心研究員</strong>。門診在台北唇顎裂及顱顏門診、桃園顱顏中心",
     "https://www.cgmh.org.tw/tw/Services/DoctorInfo/3344"),
    (None, "高醫", "郭耀仁", "110（今年確定出場）",
     "⭐ <strong>高雄醫學大學整形外科教授、高醫附設中和紀念醫院主治醫師</strong>"
     "（已由長庚轉任高醫）。頭頸腫瘤重建、乳房重建、蟹足腫、糖尿病足、手外科肢體重建、"
     "<strong>複合組織異體移植</strong>——2014 年完成台灣首例、亞洲第一例手臂移植",
     "https://www.kmuh.org.tw/Web/WebRegistration/DocIntro/DocDetail?lang=tw&doctorID=1040502"),
]

SID = "s0doc"
TITLE = "📇 考官簡介與照片（醫院官網）"
SUB = "115 年　110 年以後仍出題的 27 位"

INTRO = """
<p>110 年之後仍有出題的考官，各自在<strong>服務醫院官網的醫師簡介頁</strong>。
點進去就是<strong>照片、學經歷與專長</strong>。建議考前一晚一次點過一輪，
臉先對上名字，進考場才不會愣住。</p>

<p><strong>為什麼是連結不是把照片放上來</strong>：這個環境的網路政策擋掉所有醫院網站與圖床
（實測回傳 <code>CONNECT tunnel failed, 403</code>），抓不到圖檔。
連結的另外兩個好處是<strong>永遠是最新的</strong>，而且不必把別人網站的照片轉載到這裡。
若要改成內嵌頭像，把照片存下來給我，我建一個 <code>img/</code> 資料夾接進每一節。</p>

<p class="note">⚠ 醫院網站改版時連結可能失效；連結後面的職稱是查詢當下（2026/08/30）的狀態。</p>
"""


def esc_note(who):
    return who


def html():
    cur = None
    out = [INTRO, "<h3>今年確定出場的（優先看這些）</h3>"]
    confirmed = {"林政輝", "彭成康", "陳理維", "簡守信", "潘信誠",
                 "郭耀仁", "江原正", "曾元生", "林育賢", "戴浩志"}

    def table(rows):
        t = ['<table>',
             '<thead><tr><th>醫院</th><th>考官</th><th>年份</th>'
             '<th>現職與專長</th><th>簡介頁</th></tr></thead>', '<tbody>']
        for _sid, hosp, name, yr, role, url in rows:
            t.append(f'<tr><td>{hosp}</td><td><strong>{name}</strong></td><td>{yr}</td>'
                     f'<td>{role}</td>'
                     f'<td><a href="{url}" target="_blank" rel="noopener">看照片</a></td></tr>')
        t += ['</tbody>', '</table>']
        return "\n".join(t)

    out.append(table([d for d in DOCS if d[2] in confirmed]))
    out.append("<h3>其餘（110 年之後仍出題）</h3>")
    out.append(table([d for d in DOCS if d[2] not in confirmed]))
    return "\n".join(out)


def strip_tags(s):
    import re
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def section():
    h = html()
    names = " ".join(f"{hosp} {name}" for _s, hosp, name, *_ in DOCS)
    return {
        "id": SID, "title": TITLE, "sub": SUB,
        "group": "start", "tags": [], "level": "",
        "headline": "27 位考官在醫院官網的簡介頁——照片、學經歷、專長",
        "html": h, "text": (TITLE + " " + names + " " + strip_tags(h)).strip(),
        "name": "", "axis": "both", "topicIds": [],
        "refIds": [], "refNames": [],
    }


def bar(sid):
    """貼在該考官那一節的簡介連結。"""
    for s, hosp, name, _yr, role, url in DOCS:
        if s == sid:
            return (f'<p class="docbar">📇 <a href="{url}" target="_blank" rel="noopener">'
                    f'{hosp}官網・{name}醫師簡介（含照片）</a>'
                    f'　<span class="note">{strip_tags(role)}</span></p>')
    return None


def bar_ids():
    return [s for s, *_ in DOCS if s]
