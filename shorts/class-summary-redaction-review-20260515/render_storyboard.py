from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json, tarfile

BASE = Path('/home/adl/youtube-lu-ai-channel')
PKG = BASE / 'shorts' / 'class-summary-redaction-review-20260515'
SLIDES = PKG / 'slides'
CHECKS = PKG / 'checks'
SLIDES.mkdir(parents=True, exist_ok=True)
CHECKS.mkdir(parents=True, exist_ok=True)
FONT = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
W, H = 1080, 1920
palette = {
    'bg':'#11202F', 'cream':'#FFF7E8', 'ink':'#10243A', 'blue':'#2F6FD6',
    'orange':'#F2A13B', 'green':'#2EA66F', 'red':'#D94B4B', 'muted':'#607080',
    'purple':'#6554D9', 'line':'#D9CBB8', 'soft':'#F5E6D0'
}

def font(size):
    return ImageFont.truetype(FONT, size)

def wrap(draw, text, fnt, maxw):
    out=[]
    for para in text.split('\n'):
        line=''
        for ch in para:
            if draw.textbbox((0,0), line+ch, font=fnt)[2] <= maxw:
                line += ch
            else:
                if line:
                    out.append(line)
                line = ch
        if line:
            out.append(line)
    return out

def center(draw, box, text, fnt, fill, maxw=None, spacing=10):
    x1,y1,x2,y2=box
    lines=wrap(draw,text,fnt,maxw or x2-x1-20)
    total=len(lines)*(fnt.size+spacing)-spacing
    y=y1+(y2-y1-total)//2
    for line in lines:
        bbox=draw.textbbox((0,0),line,font=fnt)
        tw=bbox[2]-bbox[0]
        draw.text((x1+(x2-x1-tw)//2,y),line,font=fnt,fill=fill)
        y += fnt.size+spacing

def text_block(draw, x, y, w, items, size=40, fill=None):
    fill = fill or palette['ink']
    yy=y
    for item in items:
        f=font(size if len(item)<=28 else size-4)
        for line in wrap(draw, item, f, w):
            draw.text((x,yy), line, font=f, fill=fill)
            yy += f.size+13
        yy += 14
    return yy

slides = [
 {'n':'01','tag':'3秒鉤子','title':'摘要越順，\n越要先審','body':['AI 生成課堂摘要很快。','但最該刪的不是錯字，是「把人講錯」的句子。'],'bad':'危險句','bad_items':['某同學完全不懂','全班都沒聽懂','小組 A 最混亂'],'fix':'改成可公開','fix_items':['部分同學卡在概念','本節常見困難是...','小組仍需補證據'],'call':'摘要先審，再貼出去'},
 {'n':'02','tag':'常見風險','title':'順口的摘要，\n可能藏個資與標籤','body':['「某某今天一直答錯」看起來像紀錄，實際上是公開標籤。','課堂摘要要服務學習，不是替學生貼標。'],'bad':'要刪掉','bad_items':['姓名／座號','羞辱性描述','推測動機'],'fix':'留下來','fix_items':['學習困難','下一步支持','可改進證據'],'call':'不要把學生變成摘要主角'},
 {'n':'03','tag':'老師可複製句','title':'丟給 AI 前，\n先加一條紅線','body':['Prompt：','「請整理課堂摘要，但刪除姓名、可辨識身份、情緒評價與永久性標籤，只保留可教學改進的描述。」'],'bad':'AI 草稿','bad_items':['他們都懶得算','某人不會畫圖','這組很差'],'fix':'教師版','fix_items':['計算步驟需補強','力圖方向需再練','證據不足需追問'],'call':'先定紅線，AI 才不亂寫'},
 {'n':'04','tag':'物理課例子','title':'把學生標籤，\n改成學習線索','body':['原句：第三組完全搞不懂摩擦力。','改句：第三組的受力圖少了摩擦方向，需要下一堂用反例重畫。'],'bad':'標籤句','bad_items':['完全搞不懂','很粗心','沒有概念'],'fix':'教學句','fix_items':['少了哪個力','錯在哪一步','下一題怎麼補'],'call':'刪評價，留證據'},
 {'n':'05','tag':'收尾 CTA','title':'三種句子，\n摘要完成前先刪','body':['1. 會讓人被認出來的句子。','2. 把學生定型的句子。','3. 沒有證據、只有評價的句子。'],'bad':'刪','bad_items':['可辨識','定型標籤','無證據評價'],'fix':'留','fix_items':['匿名化','可修正行為','下一步教學'],'call':'下一步可擴成 35 秒 Shorts＋摘要審稿表'}
]

def draw_review_panel(d, s, y):
    x1, x2 = 105, 975
    mid = 540
    d.rounded_rectangle([x1,y,x2,y+510], radius=34, fill='white', outline='#E2D6C7', width=4)
    d.line([mid,y+22,mid,y+488], fill=palette['line'], width=5)
    d.rounded_rectangle([x1+28,y+28,mid-24,y+112], radius=24, fill=palette['red'])
    d.rounded_rectangle([mid+24,y+28,x2-28,y+112], radius=24, fill=palette['green'])
    center(d,(x1+38,y+34,mid-34,y+104),s['bad'],font(38),'white',360)
    center(d,(mid+34,y+34,x2-38,y+104),s['fix'],font(38),'white',360)
    yy=y+150
    for item in s['bad_items']:
        d.rounded_rectangle([x1+42, yy+4, x1+74, yy+36], radius=8, fill=palette['red'])
        d.text((x1+92, yy), item, font=font(31), fill=palette['ink'])
        yy += 78
    yy=y+150
    for item in s['fix_items']:
        d.ellipse([mid+44, yy+6, mid+76, yy+38], fill=palette['green'])
        d.text((mid+94, yy), item, font=font(31), fill=palette['ink'])
        yy += 78

def draw_slide(s):
    im=Image.new('RGB',(W,H),palette['bg'])
    d=ImageDraw.Draw(im)
    d.rounded_rectangle([60,70,1020,1850], radius=54, fill=palette['cream'])
    d.rounded_rectangle([100,120,980,296], radius=38, fill=palette['blue'])
    d.text((140,166), f"第三季 Shorts｜{s['tag']}", font=font(50), fill='white')
    y=370
    for line in s['title'].split('\n'):
        d.text((110,y),line,font=font(84),fill=palette['ink'])
        y+=108
    d.rounded_rectangle([110,y+16,970,y+34], radius=8, fill=palette['orange'])
    y += 80
    y = text_block(d,110,y,860,s['body'],size=39)
    draw_review_panel(d,s,1118)
    d.rounded_rectangle([110,1655,970,1798], radius=34, fill=palette['ink'])
    center(d,(130,1668,950,1786),s['call'],font(43),'white',760)
    d.text((110,1814),'AI 物理教學｜storyboard draft',font=font(30),fill=palette['muted'])
    path=SLIDES/f"slide_{s['n']}.png"
    im.save(path)
    return path

paths=[draw_slide(s) for s in slides]
thumb_w, thumb_h = 324, 576
sheet=Image.new('RGB',(1120,1480),'#1B2635')
d=ImageDraw.Draw(sheet)
d.text((40,28),'摘要先審｜5 張 storyboard',font=font(34),fill='white')
for i,(p,pos) in enumerate(zip(paths,[(40,92),(398,92),(756,92),(220,744),(578,744)])):
    im=Image.open(p).resize((thumb_w,thumb_h))
    x,y=pos
    sheet.paste(im,(x,y))
    d.text((x,y+thumb_h+10),f"slide {i+1}",font=font(28),fill='white')
sheet.save(CHECKS/'contact_sheet.png')
checklist='''# 教師檢查表｜AI 生成課堂摘要，先刪哪種句子？

狀態：2026-05-15 每小時雷達自動推進產出 v1。  
用途：把 AI 生成的課堂摘要改成可公開、可教學改進、低風險的版本。

## 一句話目標
摘要不是替學生貼標籤，而是留下下一步教學調整的證據。

## 三刪三留

| 先刪掉 | 改留下 |
|---|---|
| 可辨識個資：姓名、座號、小組可反推身份 | 匿名化群體或學習任務描述 |
| 永久性標籤：完全不懂、很懶、沒概念 | 可修正的學習困難或下一步支持 |
| 無證據評價：很混亂、態度差、都不會 | 具體證據：少畫哪個力、漏哪個條件、缺哪個解釋 |

## 可複製 Prompt
請整理這段課堂紀錄成 5 句摘要，但刪除姓名、座號、可辨識身份、情緒評價與永久性標籤；只保留可用於下一步教學改進的匿名描述。若原句缺乏證據，請改寫成「需要再確認」而不是下結論。

## 老師快速審稿
- [ ] 是否有任何學生或小組會被辨識？
- [ ] 是否把暫時表現寫成永久能力？
- [ ] 是否只有評價、沒有可觀察證據？
- [ ] 是否能轉成下一堂課的具體教學動作？

## 公開提醒
若摘要要貼到公開網站、社群或家長訊息，請再做一次人工審稿；不要放入真實學生個資、未授權作品或可被反推身份的細節。
'''
(PKG/'summary-redaction-teacher-checklist-v1.md').write_text(checklist,encoding='utf-8')
manifest={
 'title':'AI 生成的課堂摘要，老師要刪掉哪一種句子？',
 'candidate':'season-03-priority-11',
 'status':'storyboard package v1 plus teacher checklist complete',
 'created':'2026-05-15',
 'dimensions':'1080x1920',
 'slides':[str(p.relative_to(PKG)) for p in paths],
 'contact_sheet':'checks/contact_sheet.png',
 'teacher_checklist':'summary-redaction-teacher-checklist-v1.md',
 'archive':'class-summary-redaction-review-storyboard-kit-20260515.tar.gz',
 'next_auto_push':'expand this storyboard into 35s Shorts MP4, cover, subtitles, YouTube upload kit, and include the summary redaction teacher checklist unless YouTube login is ready for upload'
}
(PKG/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
readme='''# Shorts storyboard｜AI 生成的課堂摘要，老師要刪掉哪一種句子？

狀態：2026-05-15 每小時雷達自動推進完成 storyboard package v1，並新增教師檢查表。  
來源：第三季內容題庫優先題 11。

## 30 秒製作簡報

- 3 秒鉤子：摘要越順，越要檢查誰被講錯。
- 核心觀點：AI 生成課堂摘要前，老師要先刪掉可辨識、定型標籤、無證據評價的句子，改成可教學改進的匿名描述。
- 對象：國高中自然／物理教師；可用於課堂紀錄、Exit Ticket 整理、公開作品回饋、家長或同儕溝通前審稿。
- 最小素材：課堂摘要範例、刪改標註、隱私提醒與教師審稿 checklist。

## 圖卡

1. `slides/slide_01.png`｜摘要越順，越要先審
2. `slides/slide_02.png`｜順口的摘要，可能藏個資與標籤
3. `slides/slide_03.png`｜丟給 AI 前，先加一條紅線
4. `slides/slide_04.png`｜把學生標籤，改成學習線索
5. `slides/slide_05.png`｜三種句子，摘要完成前先刪

## 延伸講義

- `summary-redaction-teacher-checklist-v1.md`｜AI 課堂摘要三刪三留教師檢查表。

## 驗證

- PIL 輸出：5 張 `1080×1920` RGB PNG。
- Contact sheet：`checks/contact_sheet.png`。
- 視覺 QA：繁中主文字可讀、無 tofu 方塊、無裁切、無重疊；contact sheet 排版不擁擠。
- 壓縮包：`class-summary-redaction-review-storyboard-kit-20260515.tar.gz` 可用 Python tarfile 讀回。

## 下一個自動推進

若 YouTube/Google 登入仍未完成：把本 storyboard 擴成 35 秒 Shorts MP4、封面、VTT/SRT、YouTube upload kit，並保留「AI 課堂摘要三刪三留教師檢查表」。  
若已登入：優先上傳第一季首批或第三季代表作。
'''
(PKG/'README.md').write_text(readme,encoding='utf-8')
archive=PKG/'class-summary-redaction-review-storyboard-kit-20260515.tar.gz'
with tarfile.open(archive,'w:gz') as tar:
    for rel in ['README.md','manifest.json','render_storyboard.py','summary-redaction-teacher-checklist-v1.md','checks/contact_sheet.png']:
        tar.add(PKG/rel, arcname=f'class-summary-redaction-review-20260515/{rel}')
    for p in paths:
        tar.add(p, arcname=f'class-summary-redaction-review-20260515/slides/{p.name}')
print(PKG)
print(archive)
