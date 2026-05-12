from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json, tarfile
BASE=Path('/home/adl/youtube-lu-ai-channel')
PKG=BASE/'shorts'/'friction-assumption-check-20260512'
SLIDES=PKG/'slides'; CHECKS=PKG/'checks'
SLIDES.mkdir(parents=True, exist_ok=True); CHECKS.mkdir(parents=True, exist_ok=True)
W,H=1080,1920
FONT_CANDIDATES=['/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc','/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc','/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc','/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
def font_path():
    for p in FONT_CANDIDATES:
        if Path(p).exists(): return p
    return '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FP=font_path()
def f(size): return ImageFont.truetype(FP,size)
def wrap(draw,text,font,maxw):
    out=[]
    for para in text.split('\n'):
        cur=''
        for ch in para:
            test=cur+ch
            if draw.textbbox((0,0),test,font=font)[2] <= maxw: cur=test
            else:
                if cur: out.append(cur)
                cur=ch
        if cur: out.append(cur)
    return out
def text_box(d,xy,text,font,fill,maxw,gap=12):
    x,y=xy
    for line in wrap(d,text,font,maxw):
        d.text((x,y),line,font=font,fill=fill)
        y += font.size+gap
    return y
slides=[
 {'k':'HOOK','tag':'第二季優先題 10','title':'AI 說「忽略摩擦」\n先別急著抄','body':'忽略可以，\n但老師要先問：\n「為什麼可以忽略？」','footer':'老師把關句：這個假設合理嗎？'},
 {'k':'CASE','tag':'常見風險','title':'一句話，\n藏了整個模型','body':'AI：忽略摩擦，\n所以機械能守恆。\n\n問題是：題目真的允許嗎？','footer':'不要讓假設自動滑過去'},
 {'k':'CHECK','tag':'三步檢查','title':'摩擦假設三問','body':'1 接觸面是什麼？\n2 題目有沒有說光滑？\n3 摩擦會不會改變結論？','footer':'學生可直接照三問標註'},
 {'k':'CLASS','tag':'課堂 5 分鐘','title':'讓學生先圈\n「被忽略的東西」','body':'每組拿一段 AI 解答，\n圈出被忽略的力、條件或限制，\n再補一句理由。','footer':'活動句型：我同意忽略，因為……'},
 {'k':'CTA','tag':'下一步','title':'假設不是小字，\n是假答案的開關','body':'AI 解題越順，\n越要把假設拿出來問。\n\n留言：你最常看到 AI 忽略什麼？','footer':'可擴成 MP4／假設檢查表'},
]
BG=(15,23,42); CARD=(248,250,252); INK=(17,24,39); BLUE=(56,189,248); AMBER=(251,191,36); GREEN=(74,222,128)
for i,s in enumerate(slides,1):
    im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
    d.rounded_rectangle([54,58,1026,180],radius=34,fill=(30,41,59),outline=BLUE,width=3)
    d.text((88,90),s['k'],font=f(52),fill=AMBER)
    d.text((660,104),s['tag'],font=f(30),fill=(203,213,225))
    d.rounded_rectangle([70,250,1010,1540],radius=46,fill=CARD)
    d.rounded_rectangle([110,305,970,560],radius=34,fill=(239,246,255),outline=(125,211,252),width=3)
    text_box(d,(140,330),s['title'],f(70),INK,800,16)
    if i==3:
        qs=['接觸面？','有說光滑？','會改變結論？']
        for idx,q in enumerate(qs):
            yy=650+idx*220
            d.rounded_rectangle([140,yy,940,yy+155],radius=28,fill=(255,255,255),outline=[BLUE,AMBER,GREEN][idx],width=5)
            d.text((175,yy+38),str(idx+1),font=f(62),fill=[BLUE,AMBER,GREEN][idx])
            text_box(d,(270,yy+50),q,f(50),INK,600,8)
    else:
        text_box(d,(140,640),s['body'],f(54),INK,800,18)
    d.rounded_rectangle([96,1605,984,1788],radius=34,fill=(15,23,42),outline=(148,163,184),width=2)
    text_box(d,(136,1650),s['footer'],f(44),(248,250,252),800,12)
    d.text((500,1836),f'{i}/5',font=f(42),fill=(148,163,184))
    im.save(SLIDES/f'slide_{i:02d}.png')
sheet=Image.new('RGB',(1120,1440),(226,232,240)); sd=ImageDraw.Draw(sheet)
for idx in range(5):
    im=Image.open(SLIDES/f'slide_{idx+1:02d}.png').resize((320,569))
    x,y=(35+idx*360,40) if idx<3 else (215+(idx-3)*360,760)
    sheet.paste(im,(x,y)); sd.text((x,y+578),f'slide {idx+1}',font=f(24),fill=(15,23,42))
sheet.save(CHECKS/'contact_sheet.png')
readme = """# 第二季優先題 10｜AI 說「忽略摩擦」時，老師要問的一句話

狀態：本機 Shorts storyboard 包完成；尚未做旁白／MP4／upload kit。

## 30–40 秒製作簡報
- 3 秒鉤子：AI 說「忽略摩擦」，先別急著抄。
- 核心觀點：忽略摩擦不是固定步驟，而是需要被題目條件與模型目的支持的假設。
- 老師把關句：這個假設合理嗎？為什麼可以忽略？
- 課堂延伸：讓學生圈出 AI 解答中「被忽略的東西」，再寫一句同意或不同意的理由。

## 圖卡
1. `slides/slide_01.png` Hook：AI 說忽略摩擦，先別急著抄。
2. `slides/slide_02.png` Case：一句「忽略摩擦」藏了模型假設。
3. `slides/slide_03.png` Check：摩擦假設三問。
4. `slides/slide_04.png` Class：學生圈出被忽略的東西。
5. `slides/slide_05.png` CTA：假設是假答案的開關。

## 已驗證
- 5 張 storyboard 圖卡皆為 1080×1920 RGB。
- `checks/contact_sheet.png` 為 1120×1440 RGB，用於手機快速審閱。
- 壓縮包：`friction-assumption-check-storyboard-kit-20260512.tar.gz`。

## 下一個可自動推進項目
若 YouTube/Google 登入仍未完成，下一輪可把本 storyboard 擴成 30–40 秒 Shorts MP4、封面、字幕、YouTube upload kit 與假設檢查表；若已登入，優先上傳第一季首批 Shorts。
"""
(PKG/'README.md').write_text(readme,encoding='utf-8')
manifest={'title':'AI 說「忽略摩擦」時，老師要問的一句話','season':2,'priority':10,'status':'storyboard_complete','created_at':'2026-05-12 08:58 CST','slides':[str(p.relative_to(PKG)) for p in sorted(SLIDES.glob('slide_*.png'))],'checks':['checks/contact_sheet.png'],'next_auto_push':'expand storyboard into 30–40s Shorts MP4, cover, subtitles, upload kit, and friction-assumption teacher checklist'}
(PKG/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
archive=PKG/'friction-assumption-check-storyboard-kit-20260512.tar.gz'
with tarfile.open(archive,'w:gz') as tar:
    for p in [PKG/'README.md', PKG/'manifest.json', PKG/'render_storyboard.py', CHECKS/'contact_sheet.png'] + sorted(SLIDES.glob('slide_*.png')):
        tar.add(p,arcname=str(p.relative_to(PKG)))
print(PKG)
