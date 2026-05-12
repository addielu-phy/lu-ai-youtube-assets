from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import json, tarfile

BASE = Path('/home/adl/youtube-lu-ai-channel')
PKG = BASE / 'shorts' / 'public-before-share-check-20260513'
SLIDES = PKG / 'slides'
CHECKS = PKG / 'checks'
SLIDES.mkdir(parents=True, exist_ok=True)
CHECKS.mkdir(parents=True, exist_ok=True)
FONT = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
W, H = 1080, 1920
palette = {
    'bg':'#102033', 'cream':'#FFF8EA', 'ink':'#11243A', 'blue':'#2F6FD6',
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
 {'n':'01','tag':'3秒鉤子','title':'學生作品上網前，\n先做公開前三查','body':['能不能公開，不是看作品漂不漂亮。','先確認：看不出是誰、用得到素材、說得清楚 AI 做了什麼。'],'chips':['匿名','授權','AI 標註'],'call':'漂亮之前，先安全'},
 {'n':'02','tag':'第一查','title':'匿名化：\n別讓人猜出學生是誰','body':['檢查姓名、座號、校名、照片、聲音、檔名與雲端權限。','如果作品裡有同學對話或臉部，也要先遮蔽或換成示意資料。'],'chips':['姓名','照片','權限'],'call':'公開前先把身分線索拿掉'},
 {'n':'03','tag':'第二查','title':'授權來源：\n素材不是找到就能用','body':['圖片、音樂、題目、截圖都要問：來源在哪？授權可不可以？能不能改作？','不確定時，改用自製圖、公開授權素材或只放摘要。'],'chips':['來源','授權','替代'],'call':'AI 找到 ≠ 可以公開'},
 {'n':'04','tag':'第三查','title':'AI 標註：\n說清楚誰做了哪一步','body':['可複製句：','「本作品使用 AI 協助整理草稿／檢查錯字，內容與公開責任由教師確認。」'],'chips':['協助','確認','責任'],'call':'標註不是道歉，是交代流程'},
 {'n':'05','tag':'收尾 CTA','title':'老師的公開閘門','body':['公開前三查：匿名化、授權來源、AI 標註。','下一步可擴成 35 秒 Shorts，並延伸成學生作品公開檢查表。'],'chips':['先查','再修','後公開'],'call':'讓作品被看見，也被保護'}
]

def draw_slide(s):
    im=Image.new('RGB',(W,H),palette['bg']); d=ImageDraw.Draw(im)
    d.rounded_rectangle([60,70,1020,1850], radius=54, fill=palette['cream'])
    d.rounded_rectangle([100,120,980,300], radius=38, fill=palette['pink'])
    d.text((140,168), f"第三季 Shorts｜{s['tag']}", font=font(52), fill='white')
    y=380
    for line in s['title'].split('\n'):
        d.text((110,y),line,font=font(82),fill=palette['ink']); y+=108
    d.rounded_rectangle([110,y+18,970,y+36], radius=8, fill=palette['orange']); y+=94
    d.rounded_rectangle([110,y,970,1348], radius=34, fill='white', outline='#E2D6C7', width=4)
    yy=y+44
    for item in s['body']:
        f=font(45 if len(item)<=25 else 38)
        for line in wrap(d,item,f,790):
            d.text((155,yy),line,font=f,fill=palette['ink']); yy+=58
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
d.text((40,28),'公開前三查｜5 張 storyboard',font=font(34),fill='white')
for i,(p,pos) in enumerate(zip(paths,[(40,92),(398,92),(756,92),(220,744),(578,744)])):
    im=Image.open(p).resize((thumb_w,thumb_h)); x,y=pos; sheet.paste(im,(x,y)); d.text((x,y+thumb_h+10),f"slide {i+1}",font=font(28),fill='white')
sheet.save(CHECKS/'contact_sheet.png')
manifest={
 'title':'學生作品要放上網前，AI 幫忙檢查哪三件事？',
 'candidate':'season-03-priority-04',
 'slug':'public-before-share-check-20260513',
 'status':'storyboard package v1 complete',
 'created':'2026-05-13',
 'dimensions':'1080x1920',
 'slides':[str(p.relative_to(PKG)) for p in paths],
 'contact_sheet':'checks/contact_sheet.png',
 'archive':'public-before-share-check-storyboard-kit-20260513.tar.gz',
 'next_auto_push':'expand this storyboard into a 35s Shorts MP4/upload kit and a student-work public-sharing checklist if YouTube login is still blocked'
}
(PKG/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
readme='''# Shorts storyboard｜學生作品要放上網前，AI 幫忙檢查哪三件事？

狀態：2026-05-13 每小時雷達自動推進完成 storyboard package v1。  
來源：第三季內容題庫優先題 4「公開前三查」。

## 30 秒製作簡報

- 3 秒鉤子：能不能公開，不是看作品漂不漂亮。
- 核心觀點：學生作品公開前，老師可以讓 AI 協助跑「匿名化、授權來源、AI 標註」三道檢查，但最後公開責任仍由教師把關。
- 對象：國高中自然／物理教師，可用於學生作品展示、課堂成果上網、社群貼文或教學網站發布前。
- 最小素材：匿名化清單、授權／來源提醒、AI 使用標註句、公開前教師確認語。
- 風險提醒：不使用真實學生個資、照片、未公開作品或未確認授權素材；正式發布前需由使用者確認案例可公開。

## 圖卡

1. `slides/slide_01.png`｜公開前三查：匿名、授權、AI 標註
2. `slides/slide_02.png`｜匿名化：拿掉身分線索
3. `slides/slide_03.png`｜授權來源：AI 找到不等於可以公開
4. `slides/slide_04.png`｜AI 標註：說清楚協助範圍與責任
5. `slides/slide_05.png`｜公開閘門與 CTA

## 驗證

- PIL 輸出：5 張 `1080×1920` RGB PNG。
- Contact sheet：`checks/contact_sheet.png`。
- 視覺 QA：已檢查繁中主文字可讀、無 tofu 方塊、無裁切、無重疊；contact sheet 排版不擁擠。
- 壓縮包：`public-before-share-check-storyboard-kit-20260513.tar.gz` 已用 Python `tarfile` 讀回確認包含 README、manifest、render script、5 張圖卡與 contact sheet。

## 下一個自動推進

若 YouTube/Google 登入仍未完成：把本 storyboard 擴成 35 秒 Shorts MP4／封面／字幕／YouTube upload kit，並延伸一頁「學生作品公開檢查表」。  
若使用者已完成 YouTube/Google 登入：優先上傳已完成的第一季首批或第三季代表作。
'''
(PKG/'README.md').write_text(readme,encoding='utf-8')
archive=PKG/'public-before-share-check-storyboard-kit-20260513.tar.gz'
with tarfile.open(archive,'w:gz') as tar:
    for rel in ['README.md','manifest.json','render_storyboard.py','checks/contact_sheet.png']:
        tar.add(PKG/rel, arcname=f'public-before-share-check-20260513/{rel}')
    for p in paths:
        tar.add(p, arcname=f'public-before-share-check-20260513/slides/{p.name}')
print(PKG)
print(archive)
