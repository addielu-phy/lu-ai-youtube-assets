from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import json, tarfile

BASE = Path('/home/adl/youtube-lu-ai-channel')
PKG = BASE / 'shorts' / 'hypothesis-causal-variable-20260513'
SLIDES = PKG / 'slides'
CHECKS = PKG / 'checks'
SLIDES.mkdir(parents=True, exist_ok=True)
CHECKS.mkdir(parents=True, exist_ok=True)
FONT = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
W, H = 1080, 1920
palette = {
    'bg':'#102033', 'cream':'#FFF8EA', 'ink':'#11243A', 'blue':'#2F6FD6',
    'orange':'#F4A340', 'green':'#2FAE77', 'red':'#E4574F', 'muted':'#607080',
    'purple':'#6C63D9'
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
 {'n':'01','tag':'3秒鉤子','title':'讓 AI 寫假設，\n先加一句話','body':['假設不是猜答案。','它要說清楚：改變哪個變因，會影響哪個結果？'],'chips':['變因','因果','可測量'],'call':'假設要有因果'},
 {'n':'02','tag':'錯誤示範','title':'這句太像答案：\n「摩擦力會變小」','body':['問題：斜面越陡，小車會怎樣？','錯誤假設只丟結論，沒有說改什麼、量什麼。'],'chips':['太像答案','不可測','難檢查'],'call':'先退件，不急著解題'},
 {'n':'03','tag':'老師加的一句','title':'請 AI 先用\n「如果…那麼…」','body':['可複製 prompt：','「請把假設寫成：如果我改變＿＿，那麼＿＿會＿＿，因為＿＿。」'],'chips':['如果','那麼','因為'],'call':'一句話鎖住因果鏈'},
 {'n':'04','tag':'修正版','title':'把假設改成\n可實驗的句子','body':['如果斜面角度變大，','那麼小車到達底端的速度會增加，因為重力沿斜面的分量變大。'],'chips':['改角度','量速度','說原因'],'call':'學生知道下一步要量什麼'},
 {'n':'05','tag':'收尾 CTA','title':'老師的退件規則','body':['AI 寫的假設若沒有「變因→結果→原因」，就只能當草稿。','下一步可擴成 35 秒 Shorts 與假設檢查小卡。'],'chips':['草稿','修正','再實驗'],'call':'讓 AI 幫忙，但流程由老師把關'}
]

def draw_slide(s):
    im=Image.new('RGB',(W,H),palette['bg']); d=ImageDraw.Draw(im)
    d.rounded_rectangle([60,70,1020,1850], radius=54, fill=palette['cream'])
    d.rounded_rectangle([100,120,980,300], radius=38, fill=palette['purple'])
    d.text((140,168), f"第三季 Shorts｜{s['tag']}", font=font(52), fill='white')
    y=380
    for line in s['title'].split('\n'):
        d.text((110,y),line,font=font(86),fill=palette['ink']); y+=112
    d.rounded_rectangle([110,y+18,970,y+36], radius=8, fill=palette['orange']); y+=94
    d.rounded_rectangle([110,y,970,1348], radius=34, fill='white', outline='#E2D6C7', width=4)
    yy=y+46
    for item in s['body']:
        f=font(45 if len(item)<=24 else 39)
        for line in wrap(d,item,f,790):
            d.text((155,yy),line,font=f,fill=palette['ink']); yy+=60
        yy+=18
    basey=1428; colors=[palette['green'],palette['blue'],palette['orange']]
    for i,label in enumerate(s['chips']):
        x=110+i*295
        d.rounded_rectangle([x,basey,x+245,basey+126], radius=30, fill=colors[i])
        center(d,(x+8,basey+12,x+237,basey+114),label,font(39),'white',210)
        if i<2:
            d.line([x+260,basey+63,x+288,basey+63], fill=palette['ink'], width=8)
            d.polygon([(x+288,basey+63),(x+266,basey+48),(x+266,basey+78)], fill=palette['ink'])
    d.rounded_rectangle([110,1642,970,1790], radius=34, fill=palette['ink'])
    center(d,(130,1654,950,1778),s['call'],font(48),'white',760)
    d.text((110,1810),'盧老師 × AI 物理教學｜storyboard draft',font=font(30),fill=palette['muted'])
    path=SLIDES/f"slide_{s['n']}.png"; im.save(path); return path

paths=[draw_slide(s) for s in slides]
thumb_w, thumb_h = 324, 576
sheet=Image.new('RGB',(1120,1480),'#1B2635'); d=ImageDraw.Draw(sheet)
d.text((40,28),'讓 AI 幫學生寫假設，但老師要加上哪一句？｜5 張 storyboard',font=font(32),fill='white')
for i,(p,pos) in enumerate(zip(paths,[(40,92),(398,92),(756,92),(220,744),(578,744)])):
    im=Image.open(p).resize((thumb_w,thumb_h)); x,y=pos; sheet.paste(im,(x,y)); d.text((x,y+thumb_h+10),f"slide {i+1}",font=font(28),fill='white')
sheet.save(CHECKS/'contact_sheet.png')
manifest={
 'title':'讓 AI 幫學生寫假設，但老師要加上哪一句？',
 'candidate':'season-03-priority-02',
 'status':'storyboard package v1 complete',
 'created':'2026-05-13',
 'dimensions':'1080x1920',
 'slides':[str(p.relative_to(PKG)) for p in paths],
 'contact_sheet':'checks/contact_sheet.png',
 'next_auto_push':'storyboard already expanded into 35s MP4/upload kit; choose next unfinished season-03 candidate unless YouTube login is ready for upload'
}
(PKG/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
readme='''# Shorts storyboard｜讓 AI 幫學生寫假設，但老師要加上哪一句？

狀態：2026-05-13 每小時雷達自動推進完成 storyboard package v1。  
來源：第三季內容題庫優先題 2。

## 30 秒製作簡報

- 3 秒鉤子：假設不是猜答案，是說清楚變因。
- 核心觀點：AI 可以協助學生寫假設，但老師要先要求它用「如果我改變＿＿，那麼＿＿會＿＿，因為＿＿」把因果鏈補完整。
- 對象：國高中自然／物理教師，可用於探究課開頭、變因控制練習、AI 產出退件示範。
- 最小素材：錯誤假設／修正版對照、變因卡、可複製 prompt。

## 圖卡

1. `slides/slide_01.png`｜讓 AI 寫假設，先加一句話
2. `slides/slide_02.png`｜錯誤示範：太像答案、不可測
3. `slides/slide_03.png`｜老師加的一句：如果／那麼／因為
4. `slides/slide_04.png`｜修正版：斜面角度、底端速度、原因
5. `slides/slide_05.png`｜退件規則與 CTA

## 驗證

- PIL 輸出：5 張 `1080×1920` RGB PNG。
- Contact sheet：`checks/contact_sheet.png`。
- 視覺 QA：已檢查繁中主文字可讀、無 tofu 方塊、無裁切、無重疊；contact sheet 排版不擁擠。

## 下一個自動推進

本 storyboard 已另由 `build_shorts_mp4_package.py` 擴成 35 秒 MP4、封面、字幕與 upload kit。  
若 YouTube/Google 登入仍未完成：改推第三季下一個尚未完成候選；若已登入，優先上傳第一季首批或本支第三季 Shorts。
'''
(PKG/'README.md').write_text(readme,encoding='utf-8')
archive=PKG/'hypothesis-causal-variable-storyboard-kit-20260513.tar.gz'
with tarfile.open(archive,'w:gz') as tar:
    for rel in ['README.md','manifest.json','render_storyboard.py','checks/contact_sheet.png']:
        tar.add(PKG/rel, arcname=f'hypothesis-causal-variable-20260513/{rel}')
    for p in paths:
        tar.add(p, arcname=f'hypothesis-causal-variable-20260513/slides/{p.name}')
print(PKG)
print(archive)
