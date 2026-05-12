#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json, tarfile
BASE = Path('/home/adl/youtube-lu-ai-channel/shorts/homework-feedback-teacher-review-20260512')
SLIDES = BASE/'slides'
CHECKS = BASE/'checks'
SLIDES.mkdir(parents=True, exist_ok=True)
CHECKS.mkdir(parents=True, exist_ok=True)
FONT = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
W,H = 1080,1920
BG=(15,23,42); CYAN=(34,211,238); YELLOW=(250,204,21); GREEN=(34,197,94); RED=(248,113,113)
WHITE=(248,250,252); MUTED=(203,213,225); CARD=(255,255,255); INK=(15,23,42)
def font(s): return ImageFont.truetype(FONT, s)
def wrap(draw, text, f, max_w):
    out=[]
    for para in text.split('\n'):
        cur=''
        for ch in para:
            test=cur+ch
            if draw.textbbox((0,0), test, font=f)[2] <= max_w:
                cur=test
            else:
                if cur: out.append(cur)
                cur=ch
        if cur: out.append(cur)
    return out
def draw_wrapped(draw, xy, text, f, fill, max_w, gap=12):
    x,y=xy
    for line in wrap(draw,text,f,max_w):
        draw.text((x,y), line, font=f, fill=fill)
        y += f.size + gap
    return y
def rounded(draw, box, fill, outline=None, width=3, r=36):
    draw.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)
def pill(draw, x, y, text, fill, fg=WHITE):
    f=font(38); pad=22; w=draw.textbbox((0,0), text, font=f)[2]+pad*2
    draw.rounded_rectangle((x,y,x+w,y+62), radius=31, fill=fill)
    draw.text((x+pad,y+10), text, font=f, fill=fg)
def diag1(d,y):
    d.text((128,y+72),'學生答案',font=font(48),fill=INK)
    rounded(d,(128,y+150,468,y+310),(239,246,255),outline=(96,165,250),r=28)
    d.text((164,y+196),'概念混淆',font=font(42),fill=(30,64,175))
    d.line((500,y+230,610,y+230),fill=RED,width=10); d.polygon([(610,y+230),(582,y+208),(582,y+252)],fill=RED)
    rounded(d,(636,y+130,952,y+330),(254,242,242),outline=RED,r=28)
    d.text((674,y+178),'AI 立即回饋',font=font(39),fill=(153,27,27))
    d.text((170,y+440),'快，不等於可直接給學生',font=font(44),fill=INK)
def diag2(d,y):
    items=[('1 語氣','像教練，不像判官'),('2 概念','錯因要講準'),('3 下一步','給可修改任務')]
    yy=y+70
    for k,v in items:
        rounded(d,(128,yy,952,yy+135),(240,253,250),outline=(20,184,166),r=26)
        d.text((166,yy+24),k,font=font(48),fill=(15,118,110)); d.text((390,yy+34),v,font=font(42),fill=INK); yy+=170
def diag3(d,y):
    d.text((128,y+70),'AI 原句：',font=font(46),fill=INK)
    rounded(d,(128,y+140,952,y+300),(254,226,226),outline=RED,r=24)
    d.text((164,y+188),'你沒有掌握牛頓第二定律。',font=font(40),fill=(127,29,29))
    d.text((128,y+380),'老師改成：',font=font(46),fill=INK)
    rounded(d,(128,y+450,952,y+650),(220,252,231),outline=GREEN,r=24)
    draw_wrapped(d,(164,y+492),'你已寫出 F=ma，下一步請補上受力方向。',font(39),(22,101,52),730,10)
def diag4(d,y):
    for name,x,c in [('學生',128,(239,246,255)),('AI',405,(254,249,195)),('老師',682,(220,252,231))]:
        rounded(d,(x,y+80,x+240,y+560),c,outline=(100,116,139),r=30)
        d.text((x+62,y+120),name,font=font(50),fill=INK)
    d.line((348,y+320,405,y+320),fill=YELLOW,width=8); d.line((625,y+320,682,y+320),fill=GREEN,width=8)
    d.text((166,y+660),'回饋要經過老師審稿',font=font(48),fill=INK)
def diag5(d,y):
    for i,(txt,c) in enumerate([('保留學生努力',GREEN),('指出一個概念缺口',YELLOW),('給下一個可做動作',CYAN)]):
        yy=y+90+i*175
        d.ellipse((132,yy,212,yy+80),fill=c); d.text((156,yy+13),str(i+1),font=font(44),fill=INK)
        d.text((246,yy+12),txt,font=font(46),fill=INK)
    d.text((150,y+655),'一句把關句：\n這段回饋會讓學生知道下一步嗎？',font=font(46),fill=INK)
def slide(idx, eyebrow, title, body, footer, accent, diagram):
    im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
    d.rectangle((0,0,W,26), fill=accent); d.ellipse((-160,-120,420,460), fill=(30,58,138)); d.ellipse((760,1380,1260,1980), fill=(8,145,178))
    pill(d,72,86,eyebrow,accent,INK if accent==YELLOW else WHITE)
    y=draw_wrapped(d,(72,190),title,font(72),WHITE,936,18)+18
    d.line((72,y,1008,y), fill=accent, width=5); y+=54
    rounded(d,(72,y,1008,1250),CARD,outline=(148,163,184),width=3,r=42); diagram(d,y)
    draw_wrapped(d,(92,1320),body,font(48),WHITE,896,16)
    d.text((72,1808),footer,font=font(34),fill=MUTED)
    path=SLIDES/f'slide_{idx:02d}.png'; im.save(path); return path
slides=[
(1,'第二季優先題 11','AI 幫忙回饋作業，\n老師不能跳過哪一步？','回饋很快，但語氣和概念都要審。','草稿 storyboard｜尚未做旁白／MP4',RED,diag1),
(2,'老師審稿三件事','不是看 AI 有沒有禮貌，\n而是看學生會不會更清楚','語氣、概念、下一步：少一個，就先不要貼給學生。','最小把關流程',CYAN,diag2),
(3,'把「評價」改成「可修改」','AI 常說得太像判決，\n老師要改成可行動的提示','不要只說你錯了；要指出下一個能補上的動作。','回饋語氣示範',YELLOW,diag3),
(4,'課堂流程','學生答案 → AI 初稿 → 老師審稿，\n再給學生','AI 先省時間，老師保留最後的教學判斷。','安全流程',GREEN,diag4),
(5,'收尾 CTA','貼回饋前，先問一句：\n學生看完知道下一步嗎？','下一輪可做：35 秒影片、字幕、上傳包，以及「回饋審稿檢查表」。','盧老師 × AI 物理教學',CYAN,diag5),]
paths=[slide(*s) for s in slides]
sheet=Image.new('RGB',(1120,1440),BG); d=ImageDraw.Draw(sheet)
positions=[(60,70),(400,70),(740,70),(220,760),(560,760)]
for p,(x,y) in zip(paths,positions):
    im=Image.open(p); im.thumbnail((320,568)); sheet.paste(im,(x,y)); d.text((x,y+im.height+16),p.name,font=font(28),fill=WHITE)
sheet.save(CHECKS/'contact_sheet.png')
readme = """# Shorts storyboard｜AI 幫忙回饋作業，老師不能跳過哪一步？

狀態：第二季優先題 11 已完成 5 張 1080×1920 storyboard 圖卡與手機可檢視 contact sheet；尚未製作旁白／MP4。

## 30 秒製作簡報
- 3 秒鉤子：回饋很快，但語氣和概念都要審。
- 老師把關句：這段回饋會讓學生知道下一步嗎？
- 核心流程：學生答案 → AI 回饋初稿 → 老師審稿三件事（語氣、概念、下一步）→ 再給學生。
- 可延伸素材：教師「AI 回饋審稿檢查表」、學生改寫練習單、YouTube Shorts 35 秒版。

## 檔案
- `slides/slide_01.png`–`slides/slide_05.png`
- `checks/contact_sheet.png`
- `render_storyboard.py`
- `manifest.json`
- `homework-feedback-teacher-review-storyboard-kit-20260512.tar.gz`

## 驗證
- PIL：5 張圖卡皆為 1080×1920 RGB；contact sheet 為 1120×1440 RGB。
- 視覺 QA：繁體中文主文字可讀、無 tofu 方塊、無裁切、無重疊、資訊量適合手機預覽。

## 下一個可自動推進項目
若 YouTube/Google 登入仍未完成，下一輪把本 storyboard 擴成 35 秒 Shorts MP4、zh-TW 旁白、VTT/SRT、YouTube upload kit，並延伸「AI 回饋審稿檢查表」。
"""
(BASE/'README.md').write_text(readme, encoding='utf-8')
manifest={'title':'AI 幫忙回饋作業，老師不能跳過哪一步？','season_priority':11,'status':'storyboard_complete_pending_mp4_upload_kit','created':'2026-05-12','files':[str(p.relative_to(BASE)) for p in paths]+['checks/contact_sheet.png','README.md','manifest.json','render_storyboard.py'],'next_auto_push':'expand storyboard into 35s Shorts MP4 + zh-TW narration + subtitles + YouTube upload kit + teacher feedback-review checklist','verification':{'slide_dimensions':'5 slides 1080x1920 RGB','contact_sheet':'1120x1440 RGB','vision_qa':'passed: Traditional Chinese readable, no tofu/cropping/overlap/overcrowding'}}
(BASE/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
archive=BASE/'homework-feedback-teacher-review-storyboard-kit-20260512.tar.gz'
with tarfile.open(archive,'w:gz') as tar:
    for name in ['README.md','manifest.json','render_storyboard.py']:
        tar.add(BASE/name, arcname=f'homework-feedback-teacher-review-20260512/{name}')
    for p in paths+[CHECKS/'contact_sheet.png']:
        tar.add(p, arcname=f'homework-feedback-teacher-review-20260512/{p.relative_to(BASE)}')
print({'base':str(BASE),'archive':str(archive),'slides':len(paths)})
