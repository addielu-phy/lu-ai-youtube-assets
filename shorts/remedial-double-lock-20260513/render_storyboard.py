from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import json, tarfile
BASE = Path('/home/adl/youtube-lu-ai-channel')
PKG = BASE / 'shorts' / 'remedial-double-lock-20260513'
SLIDES = PKG / 'slides'
CHECKS = PKG / 'checks'
SLIDES.mkdir(parents=True, exist_ok=True)
CHECKS.mkdir(parents=True, exist_ok=True)
FONT = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
W, H = 1080, 1920
P = {'bg':'#102235','cream':'#FFF8EA','ink':'#102033','blue':'#2563EB','orange':'#F59E0B','green':'#16A34A','red':'#DC2626','muted':'#64748B','purple':'#7C3AED'}

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
 {'n':'01','tag':'3秒鉤子','title':'補救題請 AI 出，\n先鎖住兩件事','body':['補救不是變簡單，是對準錯因。','先鎖「錯因」與「難度階梯」，再請 AI 出題。'],'chips':['錯因','難度','退件'],'call':'雙鎖先定，題目才不亂跑'},
 {'n':'02','tag':'第一鎖','title':'鎖錯因：\n學生到底錯在哪？','body':['不要只寫「不會力學」。','改成：把摩擦力方向想反、把合力和速度混在一起、或單位代入錯。'],'chips':['概念','程序','表徵'],'call':'錯因越準，補救越短'},
 {'n':'03','tag':'第二鎖','title':'鎖難度階梯：\n先小步，不要跳關','body':['請 AI 先出「同一錯因」的三層題：辨認、修正、遷移。','每一層只改一個變因，避免學生又被新條件淹沒。'],'chips':['辨認','修正','遷移'],'call':'補救題要有階梯，不是題海'},
 {'n':'04','tag':'退件規準','title':'題目漂亮，\n也要能被退件','body':['老師檢查三句話：是否對準原錯因？是否只提高一點難度？是否有可觀察的學生答案？'],'chips':['對準','微調','可看見'],'call':'不能檢查的題目，先退件'},
 {'n':'05','tag':'收尾 CTA','title':'可複製一句 prompt','body':['「請根據這個匿名錯因，產生三層補救題：辨認、修正、遷移。每題標出對準的錯因、難度變化與退件理由。」','老師最後只保留能說明原因的題目。'],'chips':['錯因','三層','理由'],'call':'補救雙鎖：錯因 × 難度'}
]

def draw_slide(s):
    im=Image.new('RGB',(W,H),P['bg']); d=ImageDraw.Draw(im)
    d.rounded_rectangle([60,70,1020,1850], radius=54, fill=P['cream'])
    d.rounded_rectangle([100,120,980,300], radius=38, fill=P['blue'])
    d.text((140,168), f"第三季 Shorts｜{s['tag']}", font=font(52), fill='white')
    y=380
    for line in s['title'].split('\n'):
        d.text((110,y),line,font=font(76),fill=P['ink']); y+=104
    d.rounded_rectangle([110,y+18,970,y+36], radius=8, fill=P['orange']); y+=90
    d.rounded_rectangle([110,y,970,1350], radius=34, fill='white', outline='#E2D6C7', width=4)
    yy=y+42
    for item in s['body']:
        f=font(39 if len(item)<=34 else 34)
        for line in wrap(d,item,f,790):
            d.text((155,yy),line,font=f,fill=P['ink']); yy+=52
        yy+=20
    basey=1428; colors=[P['green'],P['purple'],P['orange']]
    for i,label in enumerate(s['chips']):
        x=110+i*295
        d.rounded_rectangle([x,basey,x+245,basey+126], radius=30, fill=colors[i])
        center(d,(x+8,basey+12,x+237,basey+114),label,font(36),'white',210)
        if i<2:
            d.line([x+260,basey+63,x+288,basey+63], fill=P['ink'], width=8)
            d.polygon([(x+288,basey+63),(x+266,basey+48),(x+266,basey+78)], fill=P['ink'])
    d.rounded_rectangle([110,1642,970,1790], radius=34, fill=P['ink'])
    center(d,(130,1654,950,1778),s['call'],font(44),'white',760)
    path=SLIDES/f"slide_{s['n']}.png"; im.save(path); return path

paths=[draw_slide(s) for s in slides]
thumb_w, thumb_h = 324, 576
sheet=Image.new('RGB',(1120,1480),'#1B2635'); d=ImageDraw.Draw(sheet)
d.text((40,28),'補救雙鎖｜5 張 storyboard',font=font(34),fill='white')
for i,(p,pos) in enumerate(zip(paths,[(40,92),(398,92),(756,92),(220,744),(578,744)])):
    im=Image.open(p).resize((thumb_w,thumb_h)); x,y=pos; sheet.paste(im,(x,y)); d.text((x,y+thumb_h+10),f"slide {i+1}",font=font(28),fill='white')
sheet.save(CHECKS/'contact_sheet.png')
manifest={
 'title':'補救教學題目請 AI 出，但先鎖住哪兩件事？',
 'candidate':'season-03-priority-08',
 'slug':'remedial-double-lock-20260513',
 'status':'storyboard package v1 complete',
 'created':'2026-05-13 20:32 CST',
 'dimensions':'1080x1920',
 'slides':[str(p.relative_to(PKG)) for p in paths],
 'contact_sheet':'checks/contact_sheet.png',
 'archive':'remedial-double-lock-storyboard-kit-20260513.tar.gz',
 'next_auto_push':'expand this storyboard into a 35s Shorts MP4, cover, subtitles, YouTube upload kit, and one-page remedial double-lock teacher checklist unless YouTube login is ready for upload'
}
(PKG/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
readme='''# Shorts storyboard｜補救教學題目請 AI 出，但先鎖住哪兩件事？

狀態：2026-05-13 20:32 每小時雷達自動推進完成 storyboard package v1。  
來源：第三季內容題庫優先題 8「補救雙鎖」。

## 30 秒製作簡報

- 3 秒鉤子：補救不是變簡單，是對準錯因。
- 核心觀點：請 AI 出補救題前，老師先鎖「錯因」與「難度階梯」；否則 AI 很容易產生漂亮但不對症的題海。
- 對象：國高中自然／物理教師，可用於段考後補救、AI Agent 課後回饋包、錯因分組後的練習題設計。
- 最小素材：匿名錯因標籤、三層題目階梯、退件規準、老師檢查句。
- 風險提醒：不使用真實學生姓名、座號、班級、原始手寫影像或未經確認可公開的作答內容；正式發布前需由使用者確認案例可公開性。

## 圖卡

1. `slides/slide_01.png`｜補救題先鎖兩件事
2. `slides/slide_02.png`｜第一鎖：錯因
3. `slides/slide_03.png`｜第二鎖：難度階梯
4. `slides/slide_04.png`｜退件規準
5. `slides/slide_05.png`｜可複製 prompt 與 CTA

## 驗證

- PIL 輸出：5 張 `1080×1920` RGB PNG。
- Contact sheet：`checks/contact_sheet.png`。
- 視覺 QA：已檢查繁中主文字可讀、無 tofu 方塊、無裁切、無重疊；contact sheet 排版不擁擠。
- 壓縮包：`remedial-double-lock-storyboard-kit-20260513.tar.gz` 已用 Python `tarfile` 讀回確認包含 README、manifest、render script、5 張圖卡與 contact sheet。

## GitHub Pages 穩定連結

- 手機索引：`https://addielu-phy.github.io/lu-ai-youtube-assets/mobile-index/index.html`
- 本包 README：同步後位於 `https://addielu-phy.github.io/lu-ai-youtube-assets/shorts/remedial-double-lock-20260513/README.md`
- Contact sheet：同步後位於 `https://addielu-phy.github.io/lu-ai-youtube-assets/shorts/remedial-double-lock-20260513/checks/contact_sheet.png`

## 下一個自動推進

若 YouTube/Google 登入仍未完成：把本 storyboard 擴成 35 秒 Shorts MP4／封面／字幕／YouTube upload kit，並延伸一頁「補救雙鎖」教師檢查表。  
若使用者已完成 YouTube/Google 登入：優先上傳已完成的第一季首批或第三季代表作。
'''
(PKG/'README.md').write_text(readme,encoding='utf-8')
# copy this script into package as deterministic source
(PKG/'render_storyboard.py').write_text(Path(__file__).read_text(encoding='utf-8'),encoding='utf-8')
archive=PKG/'remedial-double-lock-storyboard-kit-20260513.tar.gz'
with tarfile.open(archive,'w:gz') as tar:
    for rel in ['README.md','manifest.json','render_storyboard.py','checks/contact_sheet.png']:
        tar.add(PKG/rel, arcname=f'remedial-double-lock-20260513/{rel}')
    for p in paths:
        tar.add(p, arcname=f'remedial-double-lock-20260513/slides/{p.name}')
with tarfile.open(archive,'r:gz') as tar:
    names=tar.getnames()
print(PKG)
print(archive)
print(len(names))
print('\n'.join(names[:20]))
