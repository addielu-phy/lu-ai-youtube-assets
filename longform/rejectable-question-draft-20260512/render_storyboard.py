#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json
BASE = Path(__file__).resolve().parent
SLIDES = BASE / 'slides'
CHECKS = BASE / 'checks'
SLIDES.mkdir(parents=True, exist_ok=True)
CHECKS.mkdir(parents=True, exist_ok=True)
font_candidates = [
    Path('/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'),
    Path('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'),
    Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'),
]
font_path = next(p for p in font_candidates if p.exists())
def font(size): return ImageFont.truetype(str(font_path), size)
F_TITLE, F_SUB, F_BODY, F_SMALL = font(68), font(40), font(32), font(25)
W,H=1920,1080
BG=(17,24,39); CARD=(248,250,252); INK=(30,41,59); MUTED=(71,85,105)
BLUE=(37,99,235); ORANGE=(234,88,12); GREEN=(5,150,105); RED=(220,38,38); PURPLE=(124,58,237)

def wrap(draw, text, fnt, max_width):
    lines=[]
    for para in text.split('\n'):
        line=''
        for ch in para:
            trial=line+ch
            if draw.textbbox((0,0), trial, font=fnt)[2] <= max_width:
                line=trial
            else:
                if line: lines.append(line)
                line=ch
        if line: lines.append(line)
    return lines

def add_text(draw, xy, text, fnt, fill, max_width, line_gap=8):
    x,y=xy
    for line in wrap(draw,text,fnt,max_width):
        draw.text((x,y), line, font=fnt, fill=fill)
        y += (draw.textbbox((0,0), line, font=fnt)[3] - draw.textbbox((0,0), line, font=fnt)[1]) + line_gap
    return y

def make_slide(idx,title,subtitle,panels,footer):
    im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
    d.ellipse((-260,-260,560,500), fill=(30,64,175))
    d.ellipse((1430,650,2180,1380), fill=(7,89,75))
    d.rounded_rectangle((70,56,1850,1024), radius=42, outline=(51,65,85), width=3)
    d.rectangle((0,0,W,14), fill=PURPLE)
    d.text((95,74), f'可退件題目草稿｜{idx}/5', font=F_SMALL, fill=(221,214,254))
    y=122
    y=add_text(d,(95,y),title,F_TITLE,(255,255,255),1320,14)
    y=add_text(d,(99,y+8),subtitle,F_SUB,(203,213,225),1320,10)
    x0=95; y0=360; gap=32; box_w=(W-190-gap*(len(panels)-1))//len(panels)
    for i,p in enumerate(panels):
        x=x0+i*(box_w+gap)
        d.rounded_rectangle((x,y0,x+box_w,878), radius=34, fill=CARD)
        color=p.get('color', BLUE)
        d.rounded_rectangle((x+30,y0+30,x+116,y0+116), radius=22, fill=color)
        d.text((x+57,y0+46), str(i+1), font=F_SUB, fill=(255,255,255))
        add_text(d,(x+34,y0+142),p['head'],F_SUB,INK,box_w-68,8)
        add_text(d,(x+34,y0+252),p['body'],F_BODY,MUTED,box_w-68,8)
    d.rounded_rectangle((95,925,1825,1012), radius=28, fill=(15,23,42), outline=(71,85,105), width=2)
    add_text(d,(128,948),footer,F_SMALL,(226,232,240),1640,5)
    out=SLIDES / f'slide_{idx:02d}.png'; im.save(out); return out

slides_data=[
('好題目不是一次生成，是先讓它能被退件','把 AI 從「直接出題」改成「先交一份老師可審的草稿」。',[{'head':'先定目標','body':'這題要測哪一個概念？學生容易踩哪個坑？先寫給 AI。','color':BLUE},{'head':'要求可退件','body':'請 AI 同時交題目、標準答案、常見錯因與自評表。','color':ORANGE},{'head':'老師只審規準','body':'先看是否符合目標，不急著潤飾語句或排版。','color':GREEN}],'老師把關句：我不是要 AI 一次出好題，而是要它先交可審稿件。'),
('Prompt 裡放三個硬限制','沒有硬限制，AI 很容易做出「看起來合理但教學目標漂移」的題目。',[{'head':'年級與單元','body':'例如：國中力與運動；只用等速、力、摩擦概念。','color':BLUE},{'head':'只測一件事','body':'本題只檢查「摩擦力方向」，不要同時考太多公式。','color':PURPLE},{'head':'輸出格式','body':'題目、答案、錯誤誘因、退件自評，四欄都要交。','color':GREEN}],'可複製 prompt：請先產出可被退件的題目草稿，不要直接產出最終版。'),
('退件規準先寫在前面','老師要退的不是「不漂亮」，而是「不符合教學目的」。',[{'head':'目標不清','body':'題目解完卻不知道在考哪個概念，直接退件。','color':RED},{'head':'條件不足','body':'缺少方向、單位、初始條件或假設，先退回補齊。','color':ORANGE},{'head':'誘因不對','body':'錯誤選項沒有對應常見迷思，只是在湊選項。','color':PURPLE}],'退件句：這題不是不好，而是目前還不能安全拿進課堂。'),
('修訂不是重寫，是對照退件理由','每一次修訂都要留下「哪個理由被修掉」的證據。',[{'head':'保留 v0','body':'先保存 AI 原草稿，方便看它原本偏到哪裡。','color':BLUE},{'head':'逐條修 v1','body':'每次只修一類問題：目標、條件、迷思或語句。','color':GREEN},{'head':'再跑自評','body':'請 AI 用同一張退件規準重新檢查修訂版。','color':ORANGE}],'課堂應用：把 v0/v1 對照給學生看，示範「好題目如何被改出來」。'),
('把流程變成教師可複製模板','最後交付不是一題，而是一個之後每次都能重用的審稿流程。',[{'head':'題目草稿表','body':'目標、題幹、答案、錯因、退件理由，五欄一頁。','color':BLUE},{'head':'三色標註','body':'紅：必退；黃：需改；綠：可保留。','color':ORANGE},{'head':'發布前提醒','body':'真實題目、學生作品與未公開考題，公開前仍需人工確認。','color':GREEN}],'下一步可自動推進：擴成 4–6 分鐘旁白、字幕與 slide-video 草稿。')]
outs=[make_slide(i,*data) for i,data in enumerate(slides_data,1)]
thumb_w,thumb_h=560,315
sheet=Image.new('RGB',(1880,1180),(241,245,249)); sd=ImageDraw.Draw(sheet)
sd.text((40,24),'可退件題目草稿長片｜5 張 storyboard contact sheet', font=font(42), fill=INK)
positions=[(40,110),(660,110),(1280,110),(350,595),(970,595)]
for i,(p,pos) in enumerate(zip(outs,positions),1):
    im=Image.open(p).resize((thumb_w,thumb_h)); x,y=pos; sheet.paste(im,pos)
    sd.rectangle((x,y,x+thumb_w,y+thumb_h), outline=(148,163,184), width=3)
    sd.text((x,y+thumb_h+12), f'slide {i}', font=font(28), fill=INK)
sheet.save(CHECKS/'contact_sheet.png')
manifest={
  'title':'我怎麼讓 AI 先產出「可被退件」的題目草稿',
  'format':'longform_storyboard_package_v1',
  'created':'2026-05-12',
  'dimensions':{'slides':'1920x1080','contact_sheet':'1880x1180'},
  'assets':[str(p.relative_to(BASE)) for p in outs]+['checks/contact_sheet.png','rejectable-question-draft-rubric-handout-draft-v1.md','README.md','render_storyboard.py'],
  'next_auto_push':'擴成 4–6 分鐘旁白、SRT/VTT 與 slide-video 草稿；YouTube/Google 登入完成後則優先上傳首批影片。'
}
(BASE/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print('rendered', len(outs), 'slides to', BASE)
