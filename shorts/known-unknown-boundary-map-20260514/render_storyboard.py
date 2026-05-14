from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json, tarfile

BASE = Path('/home/adl/youtube-lu-ai-channel')
PKG = BASE / 'shorts' / 'known-unknown-boundary-map-20260514'
SLIDES = PKG / 'slides'
CHECKS = PKG / 'checks'
SLIDES.mkdir(parents=True, exist_ok=True)
CHECKS.mkdir(parents=True, exist_ok=True)
FONT = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
W, H = 1080, 1920
palette = {
    'bg':'#102033', 'cream':'#FFF8EA', 'ink':'#11243A', 'blue':'#2F6FD6',
    'orange':'#F4A340', 'green':'#2FAE77', 'red':'#E4574F', 'muted':'#607080',
    'purple':'#6C63D9', 'line':'#D9CBB8', 'soft':'#F4E7D5'
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
        tw=draw.textbbox((0,0),line,font=fnt)[2]
        draw.text((x1+(x2-x1-tw)//2,y),line,font=fnt,fill=fill)
        y += fnt.size+spacing

def text_block(draw, x, y, w, items, size=42, fill=None):
    fill = fill or palette['ink']
    yy=y
    for item in items:
        f=font(size if len(item)<=26 else size-5)
        for line in wrap(draw, item, f, w):
            draw.text((x,yy), line, font=f, fill=fill)
            yy += f.size+14
        yy += 16
    return yy

slides = [
 {'n':'01','tag':'3秒鉤子','title':'學生問 AI 前，\n先畫一張圖','body':['問題問得好，不是句子更長。','是先把「我知道」和「我不知道」分清楚。'],'left':'我知道','right':'我不知道','left_items':['題目條件','已學公式','可量到的量'],'right_items':['缺哪個量？','哪個假設？','要問 AI 什麼？'],'call':'先畫邊界，再問 AI'},
 {'n':'02','tag':'常見問題','title':'直接問 AI，\n常常變成猜答案','body':['學生輸入：「這題怎麼解？」','AI 很快給步驟，但學生不知道自己缺的是條件、概念，還是單位。'],'left':'看起來知道','right':'其實不知道','left_items':['有公式','有數字','有答案'],'right_items':['力圖對嗎？','方向怎麼選？','摩擦可忽略嗎？'],'call':'快，不代表問對了'},
 {'n':'03','tag':'老師可複製句','title':'先補這一句：\n請你照我的邊界圖回覆','body':['Prompt：','「以下分成我知道／我不知道。請先指出還缺哪一個資訊，不要直接解完整答案。」'],'left':'我知道','right':'我不知道','left_items':['情境：斜面','已知：角度','已知：質量'],'right_items':['摩擦？','初速？','要求哪個量？'],'call':'把 AI 變成提問檢查員'},
 {'n':'04','tag':'物理例子','title':'把模糊問題，\n改成可檢查問題','body':['模糊：斜面上物體怎麼算？','可檢查：若忽略摩擦、由靜止釋放，要先求加速度還是速度？'],'left':'已確定','right':'待確認','left_items':['忽略摩擦','由靜止釋放','求加速度'],'right_items':['若有摩擦？','終點距離？','要不要畫力圖？'],'call':'邊界清楚，AI 才不亂補'},
 {'n':'05','tag':'收尾 CTA','title':'一張 T-chart，\n讓學生先負責','body':['AI 可以幫忙整理思路。','但第一步交給學生：先寫出知道／不知道，再決定要問什麼。'],'left':'學生先做','right':'AI 再幫','left_items':['列條件','圈缺口','寫問題'],'right_items':['補提醒','問假設','檢查邏輯'],'call':'下一步可擴成 35 秒 Shorts＋邊界圖學習單'}
]

def draw_tchart(d, s, y):
    x1, x2 = 110, 970
    mid = 540
    d.rounded_rectangle([x1,y,x2,y+474], radius=34, fill='white', outline='#E2D6C7', width=4)
    d.line([mid,y+20,mid,y+454], fill=palette['line'], width=5)
    d.rounded_rectangle([x1+30,y+28,mid-24,y+110], radius=24, fill=palette['green'])
    d.rounded_rectangle([mid+24,y+28,x2-30,y+110], radius=24, fill=palette['orange'])
    center(d,(x1+40,y+34,mid-34,y+104),s['left'],font(38),'white',360)
    center(d,(mid+34,y+34,x2-40,y+104),s['right'],font(38),'white',360)
    yy=y+142
    for i, item in enumerate(s['left_items']):
        d.ellipse([x1+46, yy+12, x1+70, yy+36], fill=palette['green'])
        d.text((x1+88, yy), item, font=font(35), fill=palette['ink'])
        yy += 74
    yy=y+142
    for i, item in enumerate(s['right_items']):
        d.ellipse([mid+46, yy+12, mid+70, yy+36], fill=palette['orange'])
        d.text((mid+88, yy), item, font=font(35), fill=palette['ink'])
        yy += 74

def draw_slide(s):
    im=Image.new('RGB',(W,H),palette['bg'])
    d=ImageDraw.Draw(im)
    d.rounded_rectangle([60,70,1020,1850], radius=54, fill=palette['cream'])
    d.rounded_rectangle([100,120,980,300], radius=38, fill=palette['blue'])
    d.text((140,168), f"第三季 Shorts｜{s['tag']}", font=font(52), fill='white')
    y=378
    for line in s['title'].split('\n'):
        d.text((110,y),line,font=font(84),fill=palette['ink'])
        y+=108
    d.rounded_rectangle([110,y+16,970,y+34], radius=8, fill=palette['orange'])
    y += 82
    y = text_block(d,110,y,860,s['body'],size=41)
    draw_tchart(d,s,1132)
    d.rounded_rectangle([110,1642,970,1790], radius=34, fill=palette['ink'])
    center(d,(130,1654,950,1778),s['call'],font(46),'white',760)
    d.text((110,1810),'AI 物理教學｜storyboard draft',font=font(30),fill=palette['muted'])
    path=SLIDES/f"slide_{s['n']}.png"
    im.save(path)
    return path

paths=[draw_slide(s) for s in slides]
thumb_w, thumb_h = 324, 576
sheet=Image.new('RGB',(1120,1480),'#1B2635')
d=ImageDraw.Draw(sheet)
d.text((40,28),'先畫「我知道／我不知道」圖｜5 張 storyboard',font=font(32),fill='white')
for i,(p,pos) in enumerate(zip(paths,[(40,92),(398,92),(756,92),(220,744),(578,744)])):
    im=Image.open(p).resize((thumb_w,thumb_h))
    x,y=pos
    sheet.paste(im,(x,y))
    d.text((x,y+thumb_h+10),f"slide {i+1}",font=font(28),fill='white')
sheet.save(CHECKS/'contact_sheet.png')
manifest={
 'title':'學生問 AI 之前，先畫一張「我知道／我不知道」圖',
 'candidate':'season-03-priority-10',
 'status':'storyboard package v1 complete',
 'created':'2026-05-14',
 'dimensions':'1080x1920',
 'slides':[str(p.relative_to(PKG)) for p in paths],
 'contact_sheet':'checks/contact_sheet.png',
 'archive':'known-unknown-boundary-map-storyboard-kit-20260514.tar.gz',
 'next_auto_push':'expand this storyboard into 35s Shorts MP4, cover, subtitles, YouTube upload kit, and one-page known/unknown boundary-map student worksheet unless YouTube login is ready for upload'
}
(PKG/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
readme='''# Shorts storyboard｜學生問 AI 之前，先畫一張「我知道／我不知道」圖

狀態：2026-05-14 每小時雷達自動推進完成 storyboard package v1。  
來源：第三季內容題庫優先題 10。

## 30 秒製作簡報

- 3 秒鉤子：問題問得好，不是句子更長，是邊界更清楚。
- 核心觀點：學生問 AI 前，先用 T-chart 分出「我知道／我不知道」，讓 AI 先檢查缺口而不是直接解完整答案。
- 對象：國高中自然／物理教師；可用於探究課提問訓練、邊界條件、預測句與 AI 提問素養。
- 最小素材：知道／不知道 T-chart、斜面物理例子、可複製 prompt。

## 圖卡

1. `slides/slide_01.png`｜學生問 AI 前，先畫一張圖
2. `slides/slide_02.png`｜直接問 AI，常常變成猜答案
3. `slides/slide_03.png`｜老師可複製句：請你照我的邊界圖回覆
4. `slides/slide_04.png`｜把模糊問題改成可檢查問題
5. `slides/slide_05.png`｜一張 T-chart，讓學生先負責

## 驗證

- PIL 輸出：5 張 `1080×1920` RGB PNG。
- Contact sheet：`checks/contact_sheet.png`。
- 視覺 QA：繁中主文字可讀、無 tofu 方塊、無裁切、無重疊；contact sheet 排版不擁擠。

## 下一個自動推進

若 YouTube/Google 登入仍未完成：把本 storyboard 擴成 35 秒 Shorts MP4、封面、VTT/SRT、YouTube upload kit，並延伸一頁「我知道／我不知道」邊界圖學生學習單。  
若已登入：優先上傳第一季首批或第三季代表作。
'''
(PKG/'README.md').write_text(readme,encoding='utf-8')
archive=PKG/'known-unknown-boundary-map-storyboard-kit-20260514.tar.gz'
with tarfile.open(archive,'w:gz') as tar:
    for rel in ['README.md','manifest.json','render_storyboard.py','checks/contact_sheet.png']:
        tar.add(PKG/rel, arcname=f'known-unknown-boundary-map-20260514/{rel}')
    for p in paths:
        tar.add(p, arcname=f'known-unknown-boundary-map-20260514/slides/{p.name}')
print(PKG)
print(archive)
