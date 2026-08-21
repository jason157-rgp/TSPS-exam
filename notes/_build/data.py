# -*- coding: utf-8 -*-
"""「記不住的東西」筆記站內容資料。
新增筆記：在 NOTES 追加一則，然後執行 python3 build.py 重新產生 HTML。
block 型別：p / ol / ul / table / img / callout / linkout / h
callout kind：star(重點) / trap(考場地雷) / note(補充)
"""

SITE_TITLE = "記不住的東西"
SITE_SUB   = "整外專科考試 · 個人易忘點筆記"

DOMAINS = [
    {"code": "CRF", "name": "顱顏",            "file": "crf.html", "bank": "../crf.html"},
    {"code": "HNK", "name": "頭頸重建",         "file": "hnk.html", "bank": "../hnk.html"},
    {"code": "HND", "name": "手外科 / 上肢",    "file": "hnd.html", "bank": "../hnd.html"},
    {"code": "BRE", "name": "乳房",            "file": "bre.html", "bank": "../bre.html"},
    {"code": "SKB", "name": "皮膚 / 軟組織 / 燒傷", "file": "skb.html", "bank": "../skb.html"},
    {"code": "BAS", "name": "基礎",            "file": "bas.html", "bank": "../bas.html"},
]

NOTES = [

# ─────────────────────────── CRF 顱顏 ───────────────────────────
{
 "id": "pierre-robin", "domain": "CRF", "title": "Pierre Robin sequence 診斷三聯症",
 "sub": "A 顱顏症候群/畸形",
 "key": "三個特徵必須「同時、無條件」成立才叫 PRS；micrognathia 是原發缺陷，其餘兩項是骨牌效應。",
 "blocks": [
   {"t":"p","html":"<b>核心診斷三聯症矩陣（臨床直覺反射！🚨）</b>：在臨床上，必須<b>同時、無條件</b>滿足以下三大特徵聯套（combination of three features）方能確診。"},
   {"t":"ol","items":[
     "<b>小下頜畸形（micrognathia）</b>：下頜骨三維發育嚴重後縮與短小，此為<b>原發性胚胎起源</b>（primary defect）。",
     "<b>舌下垂（glossoptosis）</b>：下頜骨基底短小導致舌根肌肉失去向前支撐力，舌頭向後向下塌陷下垂。",
     "<b>上呼吸道阻塞</b>（upper airway obstruction）。"]},
   {"t":"callout","kind":"star","html":"記憶關鍵在「sequence」二字 —— micrognathia 是<b>因</b>，glossoptosis 與 airway obstruction 是被推倒的骨牌。因果順序講錯，這題就沒了。"},
 ],
 "related": ["syndrome-occlusion", "cleft-timeline"],
},
{
 "id": "syndrome-occlusion", "domain": "CRF", "title": "四大顱顏症候群的顎骨與咬合表現",
 "sub": "A 顱顏症候群/畸形 · F 正顎/咬合",
 "key": "Apert 是四者中唯一明列「下顎前突」的一列，最容易漏記。",
 "blocks": [
   {"t":"table","head":["症候群","顎骨與咬合表現"],"rows":[
     ["Crouzon","中臉發育不良，牽涉眼眶、顴骨、鼻、上顎"],
     ["<b>Apert</b>","⭐ <b>下顎前突</b>（mandibular protrusion）＋ <b>class III</b> ＋ <b>前開咬</b>（anterior open bite）＋ 上顎發育不良 ＋ 牙齒明顯而擁擠"],
     ["<b>Treacher Collins</b>","⭐ 上顎與下顎在前後徑皆發育不良，但<b>下顎的發育不良特別嚴重</b> —— 特徵為<b>短的下顎枝</b>（short ramus）與明顯彎曲且向後旋轉的<b>下顎角前切跡</b>（antegonial notch）"],
     ["Muenke","中臉發育不良併牙齒擁擠"]]},
   {"t":"callout","kind":"trap","html":"Apert 那一列是最容易被記漏的：它是四者中<b>唯一明列「下顎前突」</b>的 —— ⚠ 但注意，它的 class III <b>同時有下顎前突與上顎發育不良兩個成分</b>，與 Crouzon 的<b>純中臉問題</b>不同。這是一組很好的鑑別考點。"},
 ],
 "related": ["pierre-robin", "tcs-milestones", "orbital-shift"],
},
{
 "id": "pharyngeal-arch", "domain": "CRF", "title": "咽弓（Pharyngeal arch）衍生物總表",
 "sub": "胚胎學基礎",
 "key": "第 5 弓在人類不存在；stylopharyngeus 是第 3 弓唯一一條肌肉；cricothyroid 是喉內肌中唯一不歸 recurrent laryngeal 管的。",
 "blocks": [
   {"t":"h","html":"速記版"},
   {"t":"table","head":["咽弓","骨骼","肌肉","神經","動脈"],"rows":[
     ["1（下頜）","Meckel 軟骨→malleus 錘骨、incus 砧骨；下頜、上頜、顴、顳骨鱗部","咀嚼肌（＋mylohyoid、二腹肌前腹、tensor tympani、tensor veli palatini）","CN V 三叉","maxillary a.（上頜動脈）"],
     ["2（舌骨 hyoid）","Reichert 軟骨→stapes 鐙骨、styloid、舌骨小角＋上半","顏面表情肌（＋stapedius、stylohyoid、二腹肌後腹）","CN VII 顏面","stapedial a.（鐙骨動脈）"],
     ["3","舌骨大角＋下半體","stylopharyngeus、上中咽縮肌","CN IX 舌咽","總／內頸動脈"],
     ["4＆6","喉軟骨（甲狀、環狀、杓狀…）","咽縮肌、發聲肌、軟顎肌（除 tensor veli palatini）、上食道肌","CN X 迷走","主動脈弓、右鎖骨下、肺動脈、動脈導管"]]},
   {"t":"h","html":"完整版（含考點標記）"},
   {"t":"table","head":["弓","神經","軟骨衍生物","肌肉","動脈"],"rows":[
     ["1","⭐ V（三叉）","Meckel's：錘骨、砧骨、錘骨前韌帶、蝶下頜韌帶","咀嚼肌群、mylohyoid、二腹肌前腹、tensor tympani、⭐ <b>tensor veli palatini</b>","上頜動脈"],
     ["2","⭐ VII（顏面）","Reichert's：鐙骨、莖突、莖突舌骨韌帶、舌骨小角＋體上部","表情肌全體、stapedius、stylohyoid、二腹肌後腹","鐙骨動脈"],
     ["3","⭐ IX（舌咽）","⭐ 舌骨大角 ＋ 體下部","⭐ <b>Stylopharyngeus（唯一一條）</b>","總頸動脈 ＋ 內頸動脈近端"],
     ["4","⭐ X — superior laryngeal","甲狀軟骨、會厭軟骨","⭐ Cricothyroid、⭐ <b>Levator veli palatini</b>、咽縮肌群（上中下）","左：主動脈弓；右：右鎖骨下動脈近端"],
     ["⚠ 5","—","⭐ <b>人類無此弓</b>","—","—"],
     ["6","⭐ X — recurrent laryngeal","環狀、杓狀、小角、楔狀軟骨","⭐ 除 cricothyroid 外的<b>所有喉內肌</b>","左：肺動脈近端＋動脈導管；右：右肺動脈近端"]]},
   {"t":"h","html":"⭐ 三組必背的「同名不同弓」"},
   {"t":"p","html":"<b>① 顎的兩條張肌</b> —— 與先前讀的 IVV 直接接軌"},
   {"t":"table","head":["","弓","神經","功能"],"rows":[
     ["⭐ Tensor veli palatini","1","V3","開耳咽管"],
     ["⭐ Levator veli palatini","4","X／咽叢","提軟顎、顎咽閉合"]]},
   {"t":"callout","kind":"star","html":"⭐ 這就是 <b>Ch.21.10</b> 把「complete IVV（levator）」與「hamulus 處鬆開 tensor tendon」<b>分列兩條</b>的胚胎學根據 —— 它們從來不是同一個系統。"},
   {"t":"ul","items":[
     "<b>② 中耳兩條小肌</b>：tensor tympani（1，V3） vs stapedius（2，VII）—— 與其附著的聽小骨來源一致。",
     "<b>③ 二腹肌</b>：前腹（1，V3） vs 後腹（2，VII）。",
     "<b>④ 喉內肌</b>：cricothyroid（4，superior laryngeal） vs 其餘全部（6，recurrent laryngeal）。"]},
 ],
 "related": ["lamb", "cleft-timeline"],
},
{
 "id": "cleft-timeline", "domain": "CRF", "title": "唇顎裂全期治療黃金時程表",
 "sub": "B 唇顎裂/唇部重建",
 "key": "顎裂修補要卡在 12 個月語言發展前；ABG 要卡在恆犬齒萌發前；第 2 階段鼻整形絕對不能動鼻中隔。",
 "blocks": [
   {"t":"p","html":"📅 <b>Professor's Master Timeline</b>（GB & Neligan 聯合應證）"},
   {"t":"table","head":["病患年齡","治療階段與核心術式","手術目的與考場地雷細節"],"rows":[
     ["<b>0 – 3 個月</b>","術前嬰兒牙顎矯正<br>(Presurgical Infant Orthopedics, PSIO / NAM)","利用鼻牙槽塑形（NAM）縮小裂隙寬度、牽引牙槽骨，並利用鼻支架預先撐起塌陷的下側鼻軟骨（LLC），減輕後續手術張力。"],
     ["<b>3 – 6 個月</b>","一期唇裂修補術<br>(Primary Lip Repair)<br>＋<br>第一階段鼻整形<br>(Primary Rhinoplasty)","<b>唇部</b>：恢復垂直高度與口輪匝肌的連續性。<br><span class='ins'>教授額外補充：教科書外常考的黃金準則為「<b>Rule of 10s</b>」，即體重 10 磅、血紅素 10 g/dL、白血球不超過 10,000、出生 10 週，作為適合手術的安全門檻。</span><br><b>鼻部（第 1 階段）</b>：進行鼻尖與下三分之一的初步復位，僅作<b>有限度</b>的軟骨剝離與懸吊，絕對避免破壞生長潛力。也可合併執行牙齦骨膜成形術（GPP）。"],
     ["<b>9 – 12 個月</b>","一期顎裂修補術<br>(Primary Palate Repair)<br>＋<br>中耳通氣管置放","<b>致命考點：為什麼是這個時間點？</b>因為必須在「兒童發展出關鍵語言能力（大約 12 個月大）」<b>之前</b>完成，否則會發展出代償性的不良發音習慣（maladaptive errors）。通常會一併請耳鼻喉科研判是否置放中耳通氣管以治療耳咽管功能不全。"],
     ["<b>3 – 5 歲</b>","顎咽閉合不全治療<br>(Treatment of VPI)","若術後經語言治療仍有嚴重的顎咽閉合不全（hypernasality／鼻音過重），需進行咽瓣手術（pharyngeal flap）或二次語音手術。"],
     ["<b>4 – 6 歲</b><br>(學齡前)","第二階段鼻整形<br>(Intermediate Rhinoplasty)<br>＋<br>唇部小修整","<b>目的</b>：在入學前面對同儕壓力前，改善鼻部外觀。<br><b>術式（第 2 階段）</b>：核心在於矯正 LLC 的異常位置與鼻前庭蹼狀攣縮（vestibular webbing）。<br>🚨 <b>考場防雷（N3-21.10）</b>：這個階段「<b>絕對不能動鼻中隔</b>（septal surgery deferred）」以免破壞中面部生長，且「<b>不進行軟骨移植</b>（no cartilage grafting）」。"],
     ["<b>7 – 10 歲</b><br>(混合齒列期)","齒槽骨植骨重建<br>(Alveolar Bone Grafting, ABG)","<b>致命考點</b>：時機必須抓在「<b>恆犬齒（permanent canine）萌發之前</b>」！<br><b>目的</b>：關閉殘留的口鼻瘻管、提供萌發犬齒的骨骼支撐，並穩定上頜牙弓的連續性。"],
     ["<b>青少年期</b>","齒列矯正<br>(Orthodontics)","進行最終的術前或決定性牙齒矯正，替未來的正頜手術做準備。"],
     ["<b>骨骼發育成熟</b><br>(女 ~16 歲、男 18+ 歲)","正頜手術<br>(Orthognathic Surgery)<br>＋<br>第三階段鼻整形<br>(Definitive Septorhinoplasty)","<b>正頜</b>：唇顎裂患者常伴隨嚴重的「中臉發育不全／上頜後縮（midfacial hypoplasia）」，需執行 <b>Le Fort I 上頜前移術</b>，必要時合併下頜手術。<br><b>鼻部（第 3 階段）</b>：此時骨骼已發育成熟，終於可以進行徹底的「<b>開放式鼻中隔鼻整形</b>」，大刀闊斧地處理鼻中隔彎曲、並廣泛使用自體軟骨移植（如肋軟骨）進行精細的結構重建。"]]},
 ],
 "related": ["pharyngeal-arch", "calnan", "pierre-robin", "cleft-lip-designs", "cleft-age-thresholds"],
},
{
 "id": "calnan", "domain": "CRF", "title": "Calnan's triad（黏膜下顎裂）",
 "sub": "B 唇顎裂/唇部重建",
 "key": "zona pellucida、bifid uvula、硬顎後緣可觸摸的凹陷 —— 三項齊備。",
 "blocks": [
   {"t":"ul","items":[
     "<b>Zona pellucida</b>（軟顎中線透明帶）",
     "<b>Bifid uvula</b>（懸雍垂分岔）",
     "<b>硬顎後緣可觸摸的凹陷</b>（notch of the posterior hard palate）"]},
 ],
 "related": ["cleft-timeline", "pharyngeal-arch"],
},

{
 "id": "cleft-lip-designs", "domain": "CRF", "title": "單側唇裂修補術式總對照（Rose–Thompson → Fisher）",
 "sub": "B 唇顎裂/唇部重建",
 "key": "所有術式都在解同一題 —— 裂側唇高不夠。差別只在「補的組織從哪來、疤痕落在哪」。",
 "blocks": [
   {"t":"callout","kind":"star","html":"<b>一句話核心</b>：⭐ <b>裂側唇高不夠。</b>差別只在「<b>補的組織從哪來、疤痕落在哪</b>」。整章的比較表都只是這句話的展開。"},
   {"t":"img","src":"img/cl-repair-designs.jpg","cap":"FIGURE 22.11 CL repairs. A. Rose–Thompson. B. LeMesurier. C. Randall–Tennison. D. Millard."},
   {"t":"h","html":"主要設計對照"},
   {"t":"table","head":["術式","補長度的來源","疤痕位置","⭐ 主要優點","⚠ 主要缺點"],"rows":[
     ["直線縫合<br>（Rose–Thompson）","切口本身的弧度","完全沿 philtral column","疤痕最像人中脊","⚠ 寬裂時長度嚴重不足、notching"],
     ["三角瓣<br>（Tennison–Randall）","⭐ 外側唇的三角瓣插入內側唇下部","⚠ 橫越唇下三分之一","⭐ 幾何精確、延長可靠、Cupid's bow 保存好","⚠ 破壞 philtrum 次單位、日後極難修改、易過度延長"],
     ["Rotation–advancement<br>（Millard）","⭐ 內側唇向下旋轉，缺損由外側唇前推填補","大致沿 philtral column，⚠ 但上三分之一彎向對側","⭐ cut-as-you-go 彈性、C-flap 可用於鼻檻／columella","⚠ 破壞上三分之一次單位；寬裂需大 back cut → 外側唇過度內移 → <b>micronostril</b>（無明確矯正法）"],
     ["⭐ Extended<br>Mohler–Cutting","同上，但 ⭐ back cut 移到 columella，缺損由 C-flap 上旋填補","⭐ 完全沿次單位界線","⭐ 不需外側唇填缺損 → micronostril 風險降低、免 perialar 切口；C-flap 上旋順帶提起 medial crura、延長 columella；⭐ 提供 medial approach 鼻整形","⚠ 兩個標記點極敏感（頂點太偏裂側 → columella 過窄）；學習曲線陡"],
     ["⭐ Anatomic subunit<br>（Fisher）","⭐ 白唇緣正上方的小三角瓣","⭐ 沿次單位「接縫」，僅底部一小段橫向","⭐ measure-twice-cut-once，可在每一步前驗證設計；以標準人體測量點為基礎，自動適應任何裂寬","⚠ 彈性低，標記錯誤即難補救；仍有一小段橫向疤"]]},
   {"t":"h","html":"五個字的口訣"},
   {"t":"table","head":["術式","一個關鍵字","疤痕在哪"],"rows":[
     ["Rose–Thompson","⭐ 弧","沿人中脊（但長度不夠）"],
     ["LeMesurier","⭐ 方","⚠ 越過兩條人中脊"],
     ["Tennison–Randall","⭐ 三角","⚠ 橫越唇下部"],
     ["Millard","⭐ 旋轉","⚠ 越界在唇上部"],
     ["Mohler–Cutting","⭐ 上移","✅ 全在次單位界線"],
     ["Fisher","⭐ 量","✅ 次單位接縫，僅小三角"]]},
   {"t":"h","html":"演化 ＝ 疤痕一路往「不礙眼的地方」搬"},
   {"t":"p","html":"唇下部（三角瓣） → 唇上部（Millard） → 鼻柱（Mohler） → 白唇緣上方（Fisher）"},
   {"t":"callout","kind":"star","html":"⭐ <b>越晚的術式，橫向疤痕越短、越靠近次單位界線。</b>這條軸線把六個名字串成一條線，不用死背發明年代。"},
   {"t":"h","html":"Back cut 放哪裡 ＝ 誰來填缺損"},
   {"t":"table","head":["術式","Back cut 放哪","誰來填","副作用"],"rows":[
     ["Millard","上唇","⚠ 外側唇","micronostril"],
     ["Mohler–Cutting","鼻柱","⭐ C-flap","⚠ 鼻柱變窄"],
     ["Mulliken","⭐ 不做 back cut（改 columellar releasing incision）","—","為避開鼻柱變窄"],
     ["Fisher","白唇緣正上方","⭐ 外側小三角","彈性低"]]},
   {"t":"h","html":"兩大流派"},
   {"t":"ul","items":[
     "⭐ <b>幾何派（三角瓣）</b>：Tennison–Randall → Fisher。<b>特性</b>：先量後切，延長量有保證，可重現性高。",
     "⭐ <b>旋轉派</b>：Millard → Mohler → Cutting／Mulliken。<b>特性</b>：邊做邊調，上限高但吃經驗。",
     "⭐ <b>Fisher ＝ 兩派混血</b>（GS 原話：rotation advancement 與 Randall 的 blend）。"]},
   {"t":"h","html":"最後三個防混淆"},
   {"t":"callout","kind":"trap","html":"⚠ <b>Mohler ≠ Mulliken</b>：都想避開上唇疤，但 <b>Mohler 加大鼻柱 back cut</b>、<b>Mulliken 完全不做 back cut</b>。<br>⚠ <b>Noordhoff 三角瓣是「紅唇」的</b>（補 tubercle、防 whistling），與上述白唇設計無關，任何術式都能加。<br>⚠ <b>GS 結論</b>：沒有共識，經驗比術式重要。"},
   {"t":"h","html":"術中標記對照"},
   {"t":"img","src":"img/cl-mulliken-markings.jpg","cap":"Mulliken 標記法（雙側完全性唇裂）。上、中：術前設計 —— ⭐ 不做 back cut，改以 columellar releasing incision 取得長度；下：修復後外觀。"},
   {"t":"img","src":"img/cl-fisher-markings.jpg","cap":"Fisher anatomic subunit 標記法。上：標準人體測量點編號（measure twice, cut once）；中：據測量點畫出的切口設計（黑＝白唇、紅＝紅唇小三角）；下：縫合完成，⭐ 疤痕落在次單位接縫、僅白唇緣上方一小段橫向。"},
 ],
 "related": ["cleft-timeline", "cleft-age-thresholds", "calnan"],
},
{
 "id": "cleft-age-thresholds", "domain": "CRF", "title": "唇顎裂治療年齡閾值速查（含出處）",
 "sub": "B 唇顎裂/唇部重建",
 "key": "每個手術都綁一個年齡閾值；⭐ 定型裂鼻整形永遠排在正顎手術「之後」。",
 "blocks": [
   {"t":"table","head":["年齡","事件","出處"],"rows":[
     ["出生後 1–6 週起<br>共 8–10 週","NAM（單側裂）","Ch.19.3 §4"],
     ["3–4 個月","⭐ 初次唇修補 ＋ 初次鼻整形（輕微過度矯正、限制剝離）＋ 鼻底關閉 ± GPP","Ch.19.3"],
     ["9–12 個月","顎成形術（六項預防廔管的要素）","Ch.21.10 §5.2"],
     ["4–6 歲（入學前）","⭐ 中期鼻整形（只矯正 LLC 位置與前庭蹼）；⚠ <b>不做軟骨移植、不碰鼻中膈</b>","Ch.21.10 §6.1"],
     ["學齡前完成","⭐ 所有 VPI 手術（6 歲前每年語言評估）","Ch.21.10 §5.1"],
     ["6–12 歲（混合齒列）","⭐ 齒槽骨移植（Neligan：犬齒萌發前、9–11 歲；GS：犬齒牙根形成一半）","Ch.21.10 §6.2 ＋ GS"],
     ["青春期後","⭐ 鼻中膈手術才可施行","Ch.21.10 §6.1"],
     ["⭐⭐ 女 14–16／男 17–21 歲","⭐⭐ 正顎手術（骨骼成熟後；上顎十幾歲中期、下顎十幾歲晚期長完）","Ch.21.11 §5.4"],
     ["⭐⭐ 正顎「之後」","⭐⭐ 定型（二期）裂鼻整形（女 14–16／男 16–18）","Ch.21.10 §6.2 ＋ Ch.21.11 §5.1b"]]},
   {"t":"callout","kind":"note","html":"這則是<b>年齡閾值＋出處</b>的速查版；各階段「為什麼是這個時間點」的推理寫在〈唇顎裂全期治療黃金時程表〉那一則。兩則的年齡區間取自不同教科書段落，⚠ <b>對答時以題目引用的版本為準</b>。"},
 ],
 "related": ["cleft-timeline", "cleft-lip-designs", "tcs-milestones"],
},
{
 "id": "tcs-milestones", "domain": "CRF", "title": "Treacher Collins（TCS）年齡閾值表",
 "sub": "A 顱顏症候群/畸形",
 "key": "聽力最優先（出生數週內）；⭐ 外耳自體重建 >8 歲是第一選擇、植體式 >6 歲是第二選擇。",
 "blocks": [
   {"t":"table","head":["年齡","動作"],"rows":[
     ["出生後數週內","聽力檢查 <b>ASAP</b> → 需要則助聽器；監測吞嚥餵食 → 會診前語言期語言治療師"],
     ["&gt;2 歲","考慮腺樣體扁桃體切除"],
     ["4 歲起","定期檢查咬合與齒列發育"],
     ["&gt;4 歲","BAHA 植入（⚠ 須把日後的外耳重建一併納入考量）"],
     ["&lt;6 歲（眼／顴）","（真皮）脂肪移植／上瞼肌皮瓣／骨膜下顴部提升"],
     ["&gt;6 歲（外耳）","植體式外耳重建（<b>第二選擇</b>）"],
     ["6–17 歲（眼／顴）","客製植體"],
     ["&gt;8 歲（外耳）","⭐ 自體外耳重建（<b>第一選擇</b>）"],
     ["12 歲","心理諮詢（特別在升上中學與青春期）"],
     ["&gt;18 歲／骨骼成熟","雙顎手術＋矯正；顴／眼瞼重建（脂肪、提升、骨移植）；鼻中隔矯正；若想生育則遺傳諮詢"],
     ["通常不在一歲內","顎成形術"],
     ["術後 6–12 週","重複睡眠檢查"]]},
   {"t":"callout","kind":"trap","html":"⚠ 外耳那兩格最容易對調：<b>植體式（第二選擇）&gt;6 歲</b>、<b>自體（第一選擇）&gt;8 歲</b> —— <b>年紀大的那個才是首選</b>，因為要等肋軟骨量夠。另外 <b>BAHA &gt;4 歲</b>要先把外耳重建的切口位置算進去，順序講反就扣分。"},
 ],
 "related": ["syndrome-occlusion", "cleft-age-thresholds", "pharyngeal-arch", "orbital-shift"],
},

{
 "id": "orbital-shift", "domain": "CRF", "title": "Orbital shift 三術式對照（Box-shift／Bipartition／Monobloc）",
 "sub": "C 顱縫早閉/顱骨 · F 正顎/咬合",
 "key": "Box-shift 是「平移」、facial bipartition 是「旋轉」；⭐ 只有 box-shift 不改變咬合，只有 monobloc 不矯正眼距過寬。",
 "blocks": [
   {"t":"h","html":"層級關係"},
   {"t":"p","html":"<b>Orbital shift（眼眶移位）</b>底下只有兩個術式："},
   {"t":"ul","items":[
     "⭐ <b>Box-shift osteotomy</b> —— 只動眼眶，<b>平移</b>（translation）",
     "⭐ <b>Facial bipartition</b> —— 連上頜一起動，<b>旋轉</b>（rotation）"]},
   {"t":"callout","kind":"note","html":"<b>Monobloc 不屬於 orbital shift</b> —— 因為它做的是<b>前徙</b>，不是<b>橫向移位</b>。但考題常把三者放在同一組選項裡比較，所以一起記。"},
   {"t":"h","html":"三者對照"},
   {"t":"table","head":["","Box-shift osteotomy","Facial bipartition","Monobloc"],"rows":[
     ["<b>移動單位</b>","⭐ <b>兩個眼眶各自成「盒」</b>","⭐ <b>左右兩個半臉</b>（眼眶＋上頜連為一體）","額骨＋眼眶＋上頜整塊"],
     ["<b>運動方式</b>","⭐ <b>向內平移</b><br>（translation）","⭐ <b>繞中線楔形向內旋轉</b><br>（rotation）","⭐ <b>向前前徙</b><br>（advancement）"],
     ["<b>矯正眼距過寬</b>","✅","✅","❌"],
     ["<b>矯正中臉後縮</b>","❌","❌","✅"],
     ["⭐ <b>改變咬合</b>","⭐ <b>不改變</b>","⭐ <b>改變</b>","改變"],
     ["<b>上頜弓</b>","不動","⭐ <b>可擴張 V 形狹窄弓、關閉前開咬</b>","整塊前移"],
     ["<b>眼裂軸</b>","不變","⭐ <b>可把下斜眼裂轉正</b>","不變"]]},
   {"t":"callout","kind":"star","html":"兩個開關就分得完：<b>①「動不動上頜」</b>→ box-shift 不動上頜，所以<b>唯一不改變咬合</b>；<b>②「橫向 vs 前後」</b>→ 橫向的（box-shift、bipartition）矯正<b>眼距過寬</b>，前後的（monobloc）矯正<b>中臉後縮</b>。"},
   {"t":"callout","kind":"trap","html":"⚠ 只有 <b>facial bipartition</b> 同時具備「矯正眼距過寬」＋「擴張 V 形狹窄上頜弓、關閉前開咬」＋「把下斜眼裂（downslanting palpebral fissure）轉正」三項 —— 這正是它在 Apert 常被選用的理由。"},
 ],
 "related": ["syndrome-occlusion", "fibrous-dysplasia", "tcs-milestones"],
},
{
 "id": "fibrous-dysplasia", "domain": "CRF", "title": "Fibrous dysplasia —— 背景數字與 Zone 1–4 處置",
 "sub": "C 顱縫早閉/顱骨",
 "key": "⭐ Zone 1 完整切除＋即時骨移植；Zone 3 除非視神經壓迫否則不碰。積極度由「美觀權重 ÷ 手術代價」決定。",
 "blocks": [
   {"t":"h","html":"FD 背景數字"},
   {"t":"ul","items":[
     "<b>盛行率</b>：約 <b>1/4,000–1/30,000</b>",
     "<b>分型</b>：⭐ <b>單骨型 80–85%／多骨型 15–25%</b>",
     "⭐ <b>顱顏侵犯</b>：多骨型 <b>50–100%</b>；單骨型僅 <b>10%</b>",
     "<b>顱顏好發序</b>：<b>上頜骨 &gt; 下頜骨 &gt; 額 &gt; 蝶 &gt; 篩 &gt; 頂 &gt; 顳 &gt; 枕</b>",
     "<b>影像三型</b>：pagetoid（混合）／sclerotic（⭐ <b>磨砂玻璃</b>，顱顏最常見）／radiolucent 或 cystic",
     "<b>症候群</b>：<b>Mazabraud、Jaffe–Lichtenstein、McCune–Albright</b>（⭐ <b>多骨型是症候群的必要條件</b>；MAS 好發女性）",
     "<b>治療</b>：藥物僅能處理疼痛與減少骨吸收，⭐ <b>主力仍是手術</b>"]},
   {"t":"callout","kind":"trap","html":"⚠ <b>惡性轉化 0.5–4%</b>（骨肉瘤、纖維肉瘤、軟骨肉瘤）—— ⭐ <b>多骨型</b>與<b>曾照射過的部位</b>風險較高。這也是 FD <b>不做放射治療</b>的原因。"},
   {"t":"h","html":"四個分區（Zone 1–4）"},
   {"t":"table","head":["Zone","解剖範圍","⭐ 處置"],"rows":[
     ["⭐ <b>1</b>","<b>額眶、顴骨、上顎骨上部</b>","⭐⭐ <b>完整切除</b>以降低復發；<b>立即重建，通常用骨移植</b>"],
     ["<b>2</b>","<b>有頭髮覆蓋的顱骨</b>","⭐ <b>保守</b> —— 削骨／磨骨修飾輪廓"],
     ["⭐ <b>3</b>","<b>中央顱底、岩乳突、翼骨</b>","⭐⭐ <b>盡量不開</b>；⚠ <b>僅觀察</b>，除非出現症狀（如視神經壓迫造成視力障礙）→ 此時做<b>視神經管減壓</b>"],
     ["<b>4</b>","<b>含牙骨 —— 上頜齒槽與下頜骨</b>","⭐ <b>保守</b>；切除含牙骨會造成重大功能損害"]]},
   {"t":"h","html":"⭐ 為什麼「第一區犧牲最大」"},
   {"t":"p","html":"積極度<b>不是由病灶大小決定</b>，而是由「<b>美觀權重</b>」與「<b>手術代價</b>」的比值決定："},
   {"t":"table","head":["Zone","美觀重要性","手術代價","→ 結論"],"rows":[
     ["<b>1</b>","⭐ <b>最高</b>（正面看得見）","<b>低</b>（無重要神經血管、無牙齒）","⭐ <b>全切除</b>"],
     ["<b>2</b>","低（<b>頭髮遮住</b>）","低","削骨即可"],
     ["<b>3</b>","低（深部看不見）","⭐ <b>最高</b>（顱底神經血管）","⭐ <b>不動</b>"],
     ["<b>4</b>","中","⭐ <b>高</b>（牙齒、咬合、下頜功能）","保守"]]},
   {"t":"callout","kind":"star","html":"⭐ <b>一句話：能看見又切得起的地方就徹底切；看不見或切不起的地方就別碰。</b><br>Zone 1 之所以「犧牲最大」，正因為它是唯一同時滿足「<b>代價低 ＋ 效益高</b>」的區域 —— 原文用詞是 <b>most esthetically apparent area</b>。"},
   {"t":"h","html":"為什麼要「切乾淨」"},
   {"t":"p","html":"FD 的病理是 <b>GNAS1 突變（20q13.2-13.3）→ cAMP 活性持續 → 骨形成間葉細胞無法成熟</b>，留下<b>不成熟骨小樑陷在異常纖維組織中、持續代謝卻永遠完成不了重塑</b>。"},
   {"t":"callout","kind":"star","html":"⭐ 這是「<b>不會自己停止</b>」的病變 → <b>部分切除必然復發</b>。所以 Zone 1 選擇 <b>complete resection ＋ 即時骨移植重建</b>。"},
 ],
 "related": ["orbital-shift", "syndrome-occlusion"],
},

# ─────────────────────────── HNK 頭頸重建 ───────────────────────────
{
 "id": "lamb", "domain": "HNK", "title": "顏面表情肌的深層例外 —— LAMB 口訣",
 "sub": "HN1 顏面神經麻痺/facial reanimation",
 "key": "只有最深層的三條肌肉反而「從淺面」受支配：Levator anguli oris、Mentalis、Buccinator。",
 "blocks": [
   {"t":"p","html":"顏面表情肌絕大多數由顏面神經<b>從深面</b>進入支配。<b>只有最深層的三條肌肉，它們反而「從淺面」受支配</b> —— 這就是 GS 的 <b>LAMB</b> 口訣："},
   {"t":"ul","items":[
     "<b>L</b>evator anguli oris（提口角肌）",
     "<b>M</b>entalis（頦肌）",
     "<b>B</b>uccinator（頰肌）"]},
 ],
 "related": ["pharyngeal-arch"],
},
{
 "id": "cordeiro", "domain": "HNK", "title": "Cordeiro 上頜切除重建記憶矩陣",
 "sub": "HN11 midface/上頜重建(Cordeiro)",
 "key": "用「幾面牆 + 眼球在不在 + 硬顎在不在」三個開關，直接推出皮瓣選擇。",
 "blocks": [
   {"t":"p","html":"為了在考場上能用反射神經秒殺這類題目與後續的皮瓣選擇題，把這張矩陣印在腦海裡："},
   {"t":"table","head":["分類 (Type)","核心定義與切除範圍","關鍵保留結構（考場防雷）","重建戰術思維（N3-9 核心）"],"rows":[
     ["<b>Type I</b><br>(Limited)","1 ~ 2 面牆。","眼球保留、眼底保留、<b>硬顎保留</b>。","缺損<b>體積小但表面積大</b>。首選<b>橈前臂皮瓣</b>（radial forearm）或 <b>ALT</b>。"],
     ["<b>Type II</b><br>(Subtotal)","下方 <b>5 面牆</b>（含硬顎破洞）。","<b>眼眶底（orbital floor）必須完整</b>。","重點在<b>重建硬顎</b>。常選用骨皮瓣（fibula）或軟組織皮瓣（ALT／rectus）搭配閉塞器。"],
     ["<b>Type IIIA</b><br>(Total)","全部 <b>6 面牆</b>（含硬顎與眼底）。","<b>眼球保留</b>（orbital contents preserved）。","必須<b>同時</b>重建硬顎與眼眶底支撐。常以骨移植撐起眼眶底，再用腹直肌皮瓣（RAM）填補與鋪底；或使用<b>雙管腓骨皮瓣</b>（double-barreled fibula）。"],
     ["<b>Type IIIB</b><br>(Total + Exenteration)","全部 6 面牆 ＋ 眼窩剜除。","無（眼球與硬顎皆無）。","巨大的立體缺損。使用<b>多皮島的腹直肌皮瓣</b>（RAM）同時重建硬顎與填補眼眶死腔。"],
     ["<b>Type IV</b><br>(Orbitomaxillary)","上方 <b>5 面牆</b> ＋ 眼窩剜除。","⭐ <b>硬顎保留（palate is intact）！</b>","<b>不需重建硬顎</b>。主力為填補眼窩與顱底死腔，首選 <b>ALT</b> 或 <b>RAM</b> 皮瓣。"]]},
   {"t":"callout","kind":"trap","html":"最容易被混淆的是 <b>Type II vs Type IV</b>：兩者都是「5 面牆」，差別在 <b>Type II 破了硬顎、Type IV 硬顎完整</b>。硬顎在不在，直接決定要不要做閉塞器／骨重建。"},
 ],
 "related": ["pharyngoesoph-flaps"],
},

{
 "id": "pharyngoesoph-flaps", "domain": "HNK", "title": "咽喉食道重建 —— 三組皮瓣 × 十三項屬性（Table 13.2）",
 "sub": "HN10 咽喉食道重建",
 "key": "⭐ 環周缺損順位：ALT/AMT/PAP → RFF/UAP → Jejunum；⚠ jejunum 是唯一「不能用於部分缺損」的。",
 "blocks": [
   {"t":"table","head":["屬性","ALT／AMT／PAP","Jejunum","RFF／UAP"],"rows":[
     ["Flap elevation","Moderately difficult","Moderately difficult","Easy"],
     ["Flap reliability","Good","Good","Good"],
     ["Flap thickness","⚠ Can be too thick","Good","Good"],
     ["Primary healing","Good","⭐ Best","Good"],
     ["Donor site morbidity","⭐ Low","⚠ High","Moderate"],
     ["Recovery time","Quick","⚠ Can be slow","Quick"],
     ["Fistula rates","Low","Low","Moderate"],
     ["Stricture rates","Low","⚠ High","Moderate"],
     ["TEP voice","Good","⚠ Poor","Good"],
     ["Swallowing","Good","Good","Good"],
     ["<b>環周缺損使用順位</b>","⭐ First choice","Third choice","Second choice"],
     ["<b>部分缺損可否使用</b>","Yes","⚠ No","Yes"],
     ["<b>禁忌</b>","肥胖、大腿過厚","嚴重共病；曾接受腹部手術","瘦小、手臂太細而無法做環周重建者"]]},
   {"t":"callout","kind":"star","html":"整張表只要記<b>三條線</b>：① <b>順位</b> ALT → RFF → jejunum；② <b>jejunum 唯一的優點是 primary healing 最好</b>，其餘幾乎全是 ⚠（donor morbidity 高、恢復慢、stricture 高、TEP voice 差、不能做部分缺損）；③ <b>禁忌各自對應自己的解剖</b>（ALT 怕胖、jejunum 怕開過腹、RFF 怕手臂太細）。"},
   {"t":"callout","kind":"trap","html":"⚠ <b>TEP voice</b> 那一列是最愛考的單格：<b>jejunum 差</b>（分泌黏液、蠕動干擾氣流），ALT 與 RFF 都 Good。看到題目問「發聲重建效果最差的皮瓣」直接選 jejunum。"},
 ],
 "related": ["cordeiro"],
},

# ─────────────────────────── HND 手外科 / 上肢 ───────────────────────────
{
 "id": "brachial-plexus-atlas", "domain": "HND", "title": "Brachial plexus 圖譜",
 "sub": "D 臂神經叢",
 "key": "外部圖譜連結，臨考前掃一遍走向。",
 "blocks": [
   {"t":"linkout","href":"https://radiopaedia.org/cases/brachial-plexus-diagram","text":"Radiopaedia · Brachial plexus diagram"},
 ],
 "related": ["triple-nerve-transfer", "emg-ncs"],
},
{
 "id": "triple-nerve-transfer", "domain": "HND", "title": "三重神經轉移（Triple nerve transfers）",
 "sub": "D 臂神經叢 · E 周邊神經修復/移植",
 "key": "C5–C6（Erb palsy）的經典策略：CN XI→SSN、三頭肌支→腋神經、雙束轉移重建屈肘。",
 "blocks": [
   {"t":"p","html":"「三重神經轉移（Triple nerve transfers）」是專門用來治療 <b>C5–C6 臂神經叢損傷（Erb palsy）</b> 的經典手術策略，能有效重建<b>肩膀與手肘</b>的關鍵功能。這三項神經轉移具體包含："},
   {"t":"h","html":"1. 脊髓副神經 (CN XI) → 肩胛上神經 (Suprascapular nerve)"},
   {"t":"p","html":"將未受損的脊髓副神經遠端轉接，主要是為了恢復<b>肩膀的穩定度、外展以及外轉</b>功能。"},
   {"t":"ul","items":[
     "<b>棘上肌（supraspinatus）</b>：負責手臂外展（向外舉起）的<b>起始</b>動作。",
     "<b>棘下肌（infraspinatus）</b>：負責肩關節的<b>外旋</b>（向外轉動手臂）。"]},
   {"t":"img","src":"img/nt-san-ssn.jpg","cap":"脊髓副神經 → 肩胛上神經轉移。(A) 損傷後棘上肌／棘下肌失能（紅），斜方肌仍由 CN XI 支配（綠）；(B) 轉接後棘上肌／棘下肌恢復支配。"},
   {"t":"h","html":"2. 三頭肌運動神經 → 腋神經 (Axillary nerve)"},
   {"t":"p","html":"取用橈神經中支配三頭肌（<b>通常是內側頭</b>）的運動神經分支，轉接給腋神經，藉由重新支配<b>三角肌與小圓肌</b>，進一步增強肩膀的<b>外展與外轉</b>力量。"},
   {"t":"img","src":"img/nt-triceps-axillary.jpg","cap":"三頭肌分支 → 腋神經轉移。(A) 三角肌／小圓肌失能（紅）而三頭肌各頭功能完好（綠）；(B) 取內側頭分支轉接至腋神經前支。"},
   {"t":"h","html":"3. 雙束神經轉移 (Double fascicular transfers)"},
   {"t":"p","html":"從正常運作的<b>尺神經與正中神經</b>內，分離出可犧牲的運動神經束（通常是支配<b>尺側屈腕肌與橈側屈腕肌</b>的部位），轉接給支配<b>肱二頭肌與肱肌</b>的運動神經，藉此恢復強而有力的「<b>手肘彎曲</b>」功能。"},
   {"t":"ul","items":[
     "【<b>尺神經運動束支（ulnar fascicle）</b> ➔ 唯一指定修復「<b>肱二頭肌神經（biceps nerve）</b>」】",
     "【<b>正中神經運動束支（median fascicle）</b> ➔ 唯一指定修復深層的「<b>肱肌神經（brachialis nerve）</b>」】"]},
   {"t":"callout","kind":"star","html":"只要患者的尺神經與正中神經<b>皆完好</b>，且有可犧牲的供體神經，臨床上通常會<b>優先選擇雙束神經轉移</b>。因為同時重新支配肱二頭肌與肱肌，理論上能提供更強大且持久的屈肘力量。"},
 ],
 "related": ["brachial-plexus-atlas", "emg-ncs"],
},
{
 "id": "emg-ncs", "domain": "HND", "title": "電生理判讀速查（CMAP / SNAP / Fibs / PSW / MUP）",
 "sub": "D 臂神經叢 · E 周邊神經修復/移植",
 "key": "根性撕脫時 SNAP 會「騙你」—— 背根神經節在病灶遠端，感覺軸突未變性。",
 "blocks": [
   {"t":"table","head":["","一句話","好消息還壞消息"],"rows":[
     ["<b>CMAP</b>","還有幾條<b>運動</b>軸突到得了肌肉","振幅高＝好"],
     ["<b>SNAP</b>","還有幾條<b>感覺</b>軸突在傳導","振幅高＝好；⚠ <b>但根性撕脫時它會騙你</b>"],
     ["<b>Fibs</b>","肌肉<b>失去神經</b>了","壞消息（但 &lt;3 週看不到、&gt;1 年可能消失）"],
     ["<b>PSW</b>","同 Fibs，同一件事的另一種波形","壞消息"],
     ["<b>MUP</b>","有軸突<b>接回</b>肌肉了","好消息（<b>3 個月</b>是關鍵時點）"]]},
   {"t":"callout","kind":"trap","html":"⚠ 「感覺喪失但 SNAP 正常」＝ <b>節前（preganglionic）撕脫</b>的經典組合，這是最常被拿來出題的一格。"},
 ],
 "related": ["triple-nerve-transfer", "brachial-plexus-atlas", "forearm-flexors"],
},
{
 "id": "scaphoid-humpback", "domain": "HND", "title": "舟狀骨駝背畸形（Humpback deformity）",
 "sub": "G 骨折脫位/韌帶/生長板",
 "key": "掌側路徑 ＋ 髂骨楔形撐開 ＋ 螺絲內固定 —— 一套把生物學與力學綁在一起的公式。",
 "blocks": [
   {"t":"p","html":"天生向<b>掌側屈曲（flexion）</b>，診斷閾值：<b>舟狀骨內角（intrascaphoid angle）&gt; 35°</b> 或 <b>舟月骨角（scapholunate angle）&gt; 15°</b>。"},
   {"t":"callout","kind":"trap","html":"若在此狀態下<b>直接打入螺絲加壓</b>，會<b>加劇屈曲畸形</b>。"},
   {"t":"p","html":"因此，手術必須採用<b>掌側路徑（volar approach）</b>，並使用<b>結構性自體髂骨骨條（structural iliac crest strut）楔形撐開（wedge open）</b>，以恢復正常解剖長度，抗衡螺絲壓縮力。"},
   {"t":"callout","kind":"star","html":"此「<b>掌側路徑 ＋ 髂骨楔形撐開 ＋ 螺絲內固定</b>」是一套將生物學與力學完美結合的經典重建公式。"},
 ],
 "related": ["fx-deforming"],
},
{
 "id": "claw-hand", "domain": "HND", "title": "Claw hand —— 為什麼擋住 MCP，PIP 就伸得直",
 "sub": "C 神經壓迫與轉位",
 "key": "EDC 的力量從來沒消失，只是被 MCP 過度伸直「吃掉」了。",
 "blocks": [
   {"t":"callout","kind":"star","html":"<b>EDC 的伸直力量從來沒有消失，它只是被 MCP 的過度伸直「吃掉」了。堵住 MCP，力量就自動流向 PIP。</b>"},
   {"t":"p","html":"只要 <b>MCP 被穩定、不讓它過度伸直</b>，PIP 就可以被外在伸肌腱伸直 —— 這就是 lumbrical bar／Bouvier test 與所有 anti-claw 手術（如 Zancolli capsulodesis、靜態或動態阻擋）背後同一個力學道理。"},
 ],
 "related": ["fx-deforming", "forearm-flexors"],
},
{
 "id": "hand-arthritis", "domain": "HND", "title": "手部關節炎分佈與 arthrodesis 角度",
 "sub": "J 關節炎",
 "key": "OA 打兩端、RA 打中間；融合角度 MCP 25–40、PIP 40–55，每指 +5，DIP 幾乎打直。",
 "blocks": [
   {"t":"h","html":"分佈：誰打哪裡"},
   {"t":"p","html":"<b>OA 打兩端（DIP、CMC）、RA 打中間（MCP、PIP）</b>；<b>Heberden 在遠端</b>（H-D 配對：DIP–Heberden 記「遠」）、<b>Bouchard 在近端</b>（PIP）。"},
   {"t":"h","html":"Arthrodesis 建議角度"},
   {"t":"p","html":"<b>MCP 從 25–40°、PIP 從 40–55° 起，都是每指 +5°；DIP 幾乎打直（0–15°）。</b>唯一要多背的是 <b>拇指 MCP ＝ 15°</b>。"},
 ],
 "related": ["clino-campto"],
},
{
 "id": "cong-longitudinal", "domain": "HND", "title": "上肢先天縱向缺損圖譜（Radial / Ulnar deficiency）",
 "sub": "O 先天",
 "key": "橈側缺損看拇指與橈骨（Type N–5）；尺側缺損看 anlage 與 radiohumeral synostosis（Type 1–4）。",
 "blocks": [
   {"t":"h","html":"橈側縱向缺損（Radial longitudinal deficiency）"},
   {"t":"img","src":"img/cong-radial-deficiency.jpg","cap":"Type N（僅拇指發育不良）→ Type 0（腕骨異常）→ Type 1（遠端橈骨短 2 mm）→ Type 2（遠端橈骨發育不良）→ Type 3（橈骨部分缺失）→ Type 4（橈骨完全缺失）→ Type 5（橈骨與近端肱骨皆缺失）。"},
   {"t":"h","html":"尺側縱向缺損（Ulnar longitudinal deficiency）"},
   {"t":"img","src":"img/cong-ulnar-deficiency.jpg","cap":"Typical 正常對照 → Type 1 → Type 2（可見 anlage 纖維索）→ Type 3 → Type 4（radiohumeral synostosis 橈肱骨融合）。"},
   {"t":"callout","kind":"trap","html":"分級數字愈大不代表功能愈差 —— <b>尺側缺損 Type 4 的橈肱骨融合</b>常被誤認為是「最嚴重」，但真正決定功能的是<b>拇指與手部的狀態</b>。"},
 ],
 "related": ["clino-campto"],
},
{
 "id": "clino-campto", "domain": "HND", "title": "Clinodactyly vs Camptodactyly",
 "sub": "O 先天",
 "key": "Clino 是左右歪（冠狀面），Campto 是彎不直（矢狀面）。",
 "blocks": [
   {"t":"table","head":["","變形方向","部位"],"rows":[
     ["<b>Clinodactyly</b>","<b>橈–尺側偏斜</b>（冠狀面／左右歪）","常見小指遠端，<b>delta phalanx</b>"],
     ["<b>Camptodactyly</b>","<b>前後向屈曲攣縮</b>（矢狀面）","<b>PIP 關節</b>，常見小指"]]},
 ],
 "related": ["cong-longitudinal"],
},
{
 "id": "fx-deforming", "domain": "HND", "title": "掌骨與指骨骨折的變形方向",
 "sub": "G 骨折脫位/韌帶/生長板",
 "key": "掌骨與 P2 近端 → apex dorsal；P1 與 P2 遠端 → apex volar。記住是「誰拉住哪一塊」。",
 "blocks": [
   {"t":"table","head":["骨折部位","骨折成角方向（X 光呈現）","外觀塌陷方向","核心主導「變形鋼絲」"],"rows":[
     ["<b>掌骨 (Metacarpal)</b>","🔴 <b>Apex Dorsal</b>","掌側塌陷（拳骨凹陷）","<b>骨間肌（interossei）</b>將遠端掌骨頭往<b>掌側</b>拉。"],
     ["<b>近節指骨 (P1)</b>","🟢 <b>Apex Volar</b>","背側塌陷（PIP 過直）","<b>骨間肌</b>將<b>近端</b>拉往掌側 ＋ <b>central slip</b> 將<b>遠端</b>拉往背側。"],
     ["<b>中節指骨 (P2) — 近端骨折</b>","🔴 <b>Apex Dorsal</b>","掌側塌陷","<b>Central slip</b> 拉近端往背側 ＋ <b>FDS</b> 拉遠端往掌側。"],
     ["<b>中節指骨 (P2) — 遠端骨折</b>","🟢 <b>Apex Volar</b>","背側塌陷","<b>FDS</b> 將近端骨折塊死死拉往掌側。"]]},
   {"t":"img","src":"img/fx-deforming-forces.jpg","cap":"(A) 掌骨 (B) 近節指骨 (C) 中節指骨近端（幹骺端） (D) 中節指骨遠端 —— 紅色箭頭為主導變形的肌腱牽引方向。"},
   {"t":"callout","kind":"star","html":"判斷邏輯永遠是同一句：<b>先問「哪條肌腱抓住近端、哪條抓住遠端」，成角方向就自動掉出來。</b>"},
 ],
 "related": ["scaphoid-humpback", "claw-hand"],
},

{
 "id": "forearm-flexors", "domain": "HND", "title": "前臂屈側（掌側）八條肌肉的神經分工",
 "sub": "A 解剖/生物力學 · C 神經壓迫與轉位",
 "key": "⭐ 尺神經在前臂只管「一條半」：FCU ＋ FDP 尺側兩指；⚠ FDS 屬正中神經本幹，不是 AIN。",
 "blocks": [
   {"t":"h","html":"三層、共八條肌肉"},
   {"t":"table","head":["層","肌肉","⭐ 神經"],"rows":[
     ["<b>淺層</b><br><span class='ins'>（起自 medial epicondyle）</span>","<b>Pronator teres</b>","正中"],
     ["","<b>FCR</b>","正中"],
     ["","<b>Palmaris longus</b>","正中"],
     ["","⭐ <b>FCU</b>","⭐⭐ <b>尺神經</b>"],
     ["<b>中層</b>","⭐ <b>FDS（食、中、環、小指全部）</b>","⭐⭐ <b>正中神經本幹</b><br>（⚠ 非 AIN）"],
     ["<b>深層</b>","<b>FDP 食指、中指</b>","⭐ <b>AIN</b>"],
     ["","⭐ <b>FDP 環指、小指</b>","⭐⭐ <b>尺神經</b>"],
     ["","<b>FPL</b>","⭐ <b>AIN</b>"],
     ["","<b>Pronator quadratus</b>","⭐ <b>AIN</b>"]]},
   {"t":"callout","kind":"star","html":"<b>一句話總結：尺神經在前臂只管「一條半」—— FCU ＋ FDP 的尺側兩指。其餘全歸正中神經系統。</b>"},
   {"t":"h","html":"AIN vs 正中神經本幹的分界（高頻考點）"},
   {"t":"ul","items":[
     "⭐ <b>AIN 只管三樣</b>：<b>FPL</b>、<b>FDP（食、中）</b>、<b>pronator quadratus</b>。",
     "⚠ <b>FDS 是本幹，不是 AIN</b> —— 這是最常錯的一格。",
     "⭐ <b>AIN 是純運動神經</b>（僅有腕關節的感覺傳入），⚠ 所以 <b>AIN 症候群沒有感覺異常</b>。"]},
   {"t":"h","html":"分支順序（近端 → 遠端）"},
   {"t":"ul","items":[
     "<b>正中神經</b>：pronator teres → FCR → PL → FDS →（<b>穿過 pronator teres 兩頭之間後發出 AIN</b>）→ FPL、FDP(I, M)、PQ",
     "<b>尺神經</b>：（<b>穿過 FCU 兩頭之間進入前臂</b>）→ FCU → FDP(R, S)"]},
   {"t":"callout","kind":"star","html":"⭐ <b>兩條神經各自的「入口隧道」剛好是它支配的第一條肌肉</b> —— 正中穿 pronator teres、尺穿 FCU。好記。"},
   {"t":"h","html":"臨床推論（互補的兩組表現）"},
   {"t":"table","head":["麻痺部位","運動缺損","⚠ 鑑別要點"],"rows":[
     ["⭐ <b>孤立 AIN 麻痺</b>","FPL ＋ 食指（±中指）FDP 癱 → ⭐ <b>無法做「OK 手勢」</b>，捏起來變成扁平三角形","⚠ <b>無感覺異常</b>；環、小指 DIP 仍可屈"],
     ["⭐ <b>高位尺神經麻痺</b>","環、小指 <b>DIP 屈曲喪失</b>、FCU 癱（腕屈曲時偏橈側）","⚠ <b>PIP 屈曲保留</b>（FDS 完好）"],
     ["⭐ <b>正中神經高位麻痺</b>","<b>Benediction hand</b>（食、中指無法屈）＋ 拇指對掌喪失 ＋ 前臂旋前無力","與腕隧道不同 —— 旋前無力只見於高位"]]},
   {"t":"callout","kind":"star","html":"⭐ <b>Ulnar paradox</b>：高位損傷因 FDP 也癱，<b>爪狀反而較輕</b>；腕部損傷 FDP 完好 → <b>爪狀更明顯</b>。"},
   {"t":"h","html":"⚠ 三個變異要知道"},
   {"t":"ul","items":[
     "⭐ <b>中指 FDP 的支配浮動</b>：可為 AIN、尺神經或兩者共同。",
     "⭐ <b>Martin–Gruber anastomosis</b>：前臂內<b>正中（常來自 AIN）→ 尺神經</b>的交通支，約 <b>15–20%</b>；⚠ 會讓尺神經麻痺的表現比預期輕，且干擾神經傳導檢查判讀。",
     "⭐ <b>FDP 是「單一肌腹、雙重神經支配」</b> —— 橈側 AIN、尺側尺神經，肌腹卻連在一起（<b>quadriga effect</b> 的解剖基礎）。"]},
   {"t":"h","html":"與其他章節的連結"},
   {"t":"ul","items":[
     "⭐ <b>Transradial TMR（Table 40.3）</b>：保留 <b>Median → FCR、FDS</b>（腕屈、指屈）；轉移 <b>Median → AIN</b>、<b>Ulnar → FCU 運動支</b> —— 正好對應各自的原生領地。",
     "⭐ <b>四肢癱重建（Ch.24）</b>：<b>環指 FDS</b> 是最常用的移植腱與 lasso 材料（正中支配，C6–C7 損傷時常保留）；<b>ECRL→FDP</b> 因共用肌腹而能一次驅動四指。",
     "⭐ <b>Hunter 分期重建</b>：動力肌選擇 —— 中／環／小指用 <b>FDP 肌群</b>，<b>食指用自己的 FDP</b>（獨立肌腹）。"]},
 ],
 "related": ["claw-hand", "emg-ncs", "triple-nerve-transfer"],
},

# ─────────────────────────── BRE 乳房 ───────────────────────────
{
 "id": "bre-fascia", "domain": "BRE", "title": "乳房淺層筋膜系統（Superficial fascial system）",
 "sub": "S01 乳房/NAC解剖與美學",
 "key": "Zone of adhesion 在 IMF 與胸骨側最強、上外側最弱 —— 這決定了剝離與皺褶重建的難易。",
 "blocks": [
   {"t":"img","src":"img/bre-superficial-fascia.jpg","cap":"Fig 1.15 淺層筋膜系統：前葉（anterior lamina）與後葉（posterior lamina）包夾 corpus mammae；乳腺體從前葉脂肪的開口（anterior lamina annulus）突出。IMF 段的 circummammary ligament（zone of adhesion）位於腹直肌與胸大肌交界的腱劃之上（圓圈處）—— 沿 IMF 與胸骨緣（紅色半圓）沾黏最強，沿上緣與外側（藍色半圓）最弱。"},
 ],
 "related": [],
},

# ─────────────────────────── SKB 皮膚 / 軟組織 / 燒傷 ───────────────────────────
{
 "id": "topical-antimicrobial", "domain": "SKB", "title": "局部抗菌劑對照表",
 "sub": "S1 燒傷評估與復甦",
 "key": "選藥邏輯全在「穿透力」與「副作用」兩欄；耳鼻軟骨＝Mafenide。",
 "blocks": [
   {"t":"table","head":["藥物","⭐ 穿透焦痂／軟骨？","主要副作用","典型適應症"],"rows":[
     ["<b>Silver sulfadiazine（SSD）</b>","❌ 不穿透","暫時性<b>白血球低下</b>（可自行恢復，<b>不必停藥</b>）；部分認為延緩上皮化","最常用的一般燒傷創面"],
     ["⭐⭐ <b>Mafenide acetate（Sulfamylon）</b>","✅ <b>能穿透焦痂與軟骨</b>","⚠ <b>碳酸酐酶抑制</b>作用 → <b>代謝性酸中毒</b>；⚠ 塗抹時<b>明顯疼痛</b>","⭐ <b>耳、鼻等軟骨部位</b>；厚焦痂"],
     ["<b>Silver nitrate 0.5%</b>","❌ 不穿透","⚠ <b>低鈉血症</b>；染黑衣物與環境","對 sulfa 過敏者"],
     ["<b>Nanocrystalline silver（ACTICOAT）</b>","—","成本","可留置數日，減少換藥次數與疼痛（Fig 18.13）—— 部分層至全層、大面積、高汙染、免疫低下者"],
     ["<b>0.5–2% 醋酸〔GS〕</b>","—","—","sulfa 過敏的替代"]]},
   {"t":"callout","kind":"star","html":"考題最愛的兩組對子：<b>SSD → 白血球低下</b>（不必停藥）、<b>Mafenide → 代謝性酸中毒</b>（碳酸酐酶抑制）；<b>Silver nitrate → 低鈉</b>。三種副作用不能互換。"},
 ],
 "related": [],
},

# ─────────────────────────── BAS 基礎 ───────────────────────────
{
 "id": "graft-take", "domain": "BAS", "title": "植皮存活三階段",
 "sub": "B4 移植物基礎",
 "key": "Imbibition → Inosculation → Revascularization。",
 "blocks": [
   {"t":"ol","items":[
     "<b>Imbibition</b>（血漿吸收期）",
     "<b>Inosculation</b>（血管吻合期）",
     "<b>Revascularization</b>（血管再生期）"]},
 ],
 "related": [],
},
]
