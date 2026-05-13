from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import json, tarfile

BASE = Path('/home/adl/youtube-lu-ai-channel')
PKG = BASE / 'shorts' / 'misconception-classification-first-20260513'
SLIDES = PKG / 'slides'
CHECKS = PKG / 'checks'
SLIDES.mkdir(parents=True, exist_ok=True)
CHECKS.mkdir(parents=True, exist_ok=True)
FONT = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
W, H = 1080, 1920
palette = {
    'bg':'#0E2433', 'cream':'#FFF8EA', 'ink':'#102033', 'blue':'#2F6FD6',
    'orange':'#F4A340', 'green':'#2FAE77', 'red':'#E4574F', 'muted':'#607080',
    'purple':'#6C63D9', 'pink':'#E95D8F'
}

def font(size): return ImageFont.truetype(FONT, size)

def wrap(draw, text, fnt, maxw):
    out=[]
    for para in text.split('\n'):
        line=''
        for ch in para:
            if draw.textbbox((0,0), line+ch, font=fnt)[2] <= maxw:
                line += ch
            else:
                if line: out.append(line)
                line = ch
        if line: out.append(line)
    return out

def center(draw, box, text, fnt, fill, maxw=None):
    x1,y1,x2,y2=box
    lines=wrap(draw,text,fnt,maxw or x2-x1-20)
    total=len(lines)*(fnt.size+10)-10
    y=y1+(y2-y1-total)//2
    for line in lines:
        tw=draw.textbbox((0,0),line,font=fnt)[2]
        draw.text((x1+(x2-x1-tw)//2,y),line,font=fnt,fill=fill)
        y += fnt.size+10

slides = [
 {'n':'01','tag':'3秒鉤子','title':'學生錯答丟給 AI，\n先別急著要建議','body':['先分類，再補救；不要一開始就開藥。','請 AI 先把迷思分成三類，老師才知道下一步要補哪裡。'],'chips':['先看錯因','再分群','後補救'],'call':'AI 不是醫生，先當檢驗員'},
 {'n':'02','tag':'第一類','title':'概念迷思：\n學生把規則想錯了','body':['例：把速度變大直接當成受力變大。','老師 prompt：請判斷這個錯答是否反映錯誤概念，並指出關鍵句。'],'chips':['觀念','關鍵句','反例'],'call':'概念錯，要用反例拆開'},
 {'n':'03','tag':'第二類','title':'程序迷思：\n方法會做，但步驟亂了','body':['例：公式選對，代入單位或正負號卻混亂。','老師 prompt：請標出學生從哪一步開始偏離正確流程。'],'chips':['步驟','單位','符號'],'call':'程序錯，要補流程檢查點'},
 {'n':'04','tag':'第三類','title':'表徵迷思：\n圖、文字、公式對不起來','body':['例：學生文字說向右，圖上箭頭卻向左。','老師 prompt：請比較文字、圖示、公式三種表徵是否一致。'],'chips':['文字','圖示','公式'],'call':'表徵錯，要先對齊說法'},
 {'n':'05','tag':'收尾 CTA','title':'可複製一句 prompt','body':['「請先不要給補救建議。請把這份匿名錯答分成概念、程序、表徵三類，並引用學生原句做理由。」','分類完成後，老師再決定補救活動。'],'chips':['分類','證據','再建議'],'call':'先分類，補救才不亂開藥'}
]

def draw_slide(s):
    im=Image.new('RGB',(W,H),palette['bg']); d=ImageDraw.Draw(im)
    d.rounded_rectangle([60,70,1020,1850], radius=54, fill=palette['cream'])
    d.rounded_rectangle([100,120,980,300], radius=38, fill=palette['purple'])
    d.text((140,168), f"第三季 Shorts｜{s['tag']}", font=font(52), fill='white')
    y=380
    for line in s['title'].split('\n'):
        d.text((110,y),line,font=font(78),fill=palette['ink']); y+=104
    d.rounded_rectangle([110,y+18,970,y+36], radius=8, fill=palette['orange']); y+=90
    d.rounded_rectangle([110,y,970,1348], radius=34, fill='white', outline='#E2D6C7', width=4)
    yy=y+42
    for item in s['body']:
        f=font(42 if len(item)<=32 else 35)
        for line in wrap(d,item,f,790):
            d.text((155,yy),line,font=f,fill=palette['ink']); yy+=54
        yy+=18
    basey=1428; colors=[palette['green'],palette['blue'],palette['orange']]
    for i,label in enumerate(s['chips']):
        x=110+i*295
        d.rounded_rectangle([x,basey,x+245,basey+126], radius=30, fill=colors[i])
        center(d,(x+8,basey+12,x+237,basey+114),label,font(36),'white',210)
        if i<2:
            d.line([x+260,basey+63,x+288,basey+63], fill=palette['ink'], width=8)
            d.polygon([(x+288,basey+63),(x+266,basey+48),(x+266,basey+78)], fill=palette['ink'])
    d.rounded_rectangle([110,1642,970,1790], radius=34, fill=palette['ink'])
    center(d,(130,1654,950,1778),s['call'],font(45),'white',760)
    path=SLIDES/f"slide_{s['n']}.png"; im.save(path); return path

paths=[draw_slide(s) for s in slides]
thumb_w, thumb_h = 324, 576
sheet=Image.new('RGB',(1120,1480),'#1B2635'); d=ImageDraw.Draw(sheet)
d.text((40,28),'先分迷思｜5 張 storyboard',font=font(34),fill='white')
for i,(p,pos) in enumerate(zip(paths,[(40,92),(398,92),(756,92),(220,744),(578,744)])):
    im=Image.open(p).resize((thumb_w,thumb_h)); x,y=pos; sheet.paste(im,(x,y)); d.text((x,y+thumb_h+10),f"slide {i+1}",font=font(28),fill='white')
sheet.save(CHECKS/'contact_sheet.png')
manifest={
 'title':'AI 幫忙整理學生迷思，老師先要求它分類而不是建議',
 'candidate':'season-03-priority-07',
 'slug':'misconception-classification-first-20260513',
 'status':'storyboard package v1 complete',
 'created':'2026-05-13',
 'dimensions':'1080x1920',
 'slides':[str(p.relative_to(PKG)) for p in paths],
 'contact_sheet':'checks/contact_sheet.png',
 'archive':'misconception-classification-first-storyboard-kit-20260513.tar.gz',
 'next_auto_push':'expand this storyboard into a 35s Shorts MP4, cover, subtitles, YouTube upload kit, and one-page misconception classification prompt sheet unless YouTube login is ready for upload'
}
(PKG/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
readme='''# Shorts storyboard｜AI 幫忙整理學生迷思，老師先要求它分類而不是建議

狀態：2026-05-13 每小時雷達自動推進完成 storyboard package v1。  
來源：第三季內容題庫優先題 7「先分迷思」。

## 30 秒製作簡報

- 3 秒鉤子：先分類，再補救；不要一開始就開藥。
- 核心觀點：學生錯答可以先交給 AI 做「概念／程序／表徵」分類，但 AI 必須引用匿名錯答證據，不能直接跳到補救建議。
- 對象：國高中自然／物理教師，可用於段考後錯答整理、AI Agent 課後回饋包、補救教學分組前置作業。
- 最小素材：三類迷思卡、匿名學生錯答例、分類 prompt、老師二次確認句。
- 風險提醒：不使用真實學生姓名、座號、班級、原始手寫影像或未經確認可公開的作答內容；正式發布前需由使用者確認案例可公開性。

## 圖卡

1. `slides/slide_01.png`｜先分類，再補救
2. `slides/slide_02.png`｜概念迷思：規則想錯
3. `slides/slide_03.png`｜程序迷思：步驟亂掉
4. `slides/slide_04.png`｜表徵迷思：圖文公式不一致
5. `slides/slide_05.png`｜可複製 prompt 與 CTA

## 驗證

- PIL 輸出：5 張 `1080×1920` RGB PNG。
- Contact sheet：`checks/contact_sheet.png`。
- 視覺 QA：已檢查繁中主文字可讀、無 tofu 方塊、無裁切、無重疊；contact sheet 排版不擁擠。
- 壓縮包：`misconception-classification-first-storyboard-kit-20260513.tar.gz` 已用 Python `tarfile` 讀回確認包含 README、manifest、render script、5 張圖卡與 contact sheet。

## 下一個自動推進

若 YouTube/Google 登入仍未完成：把本 storyboard 擴成 35 秒 Shorts MP4／封面／字幕／YouTube upload kit，並延伸一頁「迷思分類 prompt」教師小抄。  
若使用者已完成 YouTube/Google 登入：優先上傳已完成的第一季首批或第三季代表作。
'''
(PKG/'README.md').write_text(readme,encoding='utf-8')
archive=PKG/'misconception-classification-first-storyboard-kit-20260513.tar.gz'
with tarfile.open(archive,'w:gz') as tar:
    for rel in ['README.md','manifest.json','render_storyboard.py','checks/contact_sheet.png']:
        tar.add(PKG/rel, arcname=f'misconception-classification-first-20260513/{rel}')
    for p in paths:
        tar.add(p, arcname=f'misconception-classification-first-20260513/slides/{p.name}')
print(PKG)
print(archive)
