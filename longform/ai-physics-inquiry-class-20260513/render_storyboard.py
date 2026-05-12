#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json, tarfile

BASE = Path('/home/adl/youtube-lu-ai-channel/longform/ai-physics-inquiry-class-20260513')
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
F_TITLE, F_SUB, F_BODY, F_SMALL = font(66), font(38), font(31), font(25)
W, H = 1920, 1080
BG=(15,23,42); CARD=(248,250,252); INK=(30,41,59); MUTED=(71,85,105)
BLUE=(37,99,235); ORANGE=(234,88,12); GREEN=(5,150,105); RED=(220,38,38); PURPLE=(124,58,237); CYAN=(8,145,178)

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
        bbox=draw.textbbox((0,0), line, font=fnt)
        y += bbox[3]-bbox[1]+line_gap
    return y

def make_slide(idx,title,subtitle,panels,footer):
    im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
    d.ellipse((-260,-260,560,500), fill=(30,64,175))
    d.ellipse((1370,610,2180,1420), fill=(6,95,70))
    d.rectangle((0,0,W,16), fill=CYAN)
    d.rounded_rectangle((70,56,1850,1024), radius=44, outline=(71,85,105), width=3)
    d.text((96,76), f'45 分鐘 AI 物理探究課｜{idx}/5', font=F_SMALL, fill=(207,250,254))
    y=124
    y=add_text(d,(96,y),title,F_TITLE,(255,255,255),1360,14)
    y=add_text(d,(100,y+8),subtitle,F_SUB,(203,213,225),1390,10)
    x0=96; y0=358; gap=30; box_w=(W-192-gap*(len(panels)-1))//len(panels)
    for i,p in enumerate(panels):
        x=x0+i*(box_w+gap)
        d.rounded_rectangle((x,y0,x+box_w,878), radius=34, fill=CARD)
        color=p.get('color',BLUE)
        d.rounded_rectangle((x+30,y0+30,x+116,y0+116), radius=22, fill=color)
        d.text((x+57,y0+46), str(i+1), font=F_SUB, fill=(255,255,255))
        add_text(d,(x+34,y0+142),p['head'],F_SUB,INK,box_w-68,8)
        add_text(d,(x+34,y0+252),p['body'],F_BODY,MUTED,box_w-68,8)
    d.rounded_rectangle((96,924,1824,1012), radius=28, fill=(15,23,42), outline=(100,116,139), width=2)
    add_text(d,(130,948),footer,F_SMALL,(226,232,240),1640,5)
    out=SLIDES/f'slide_{idx:02d}.png'; im.save(out); return out

slides_data=[
('AI 可以進教室，但流程不能交給 AI','45 分鐘課不是把答案外包，而是把探究流程拆成可檢查的節點。',[{'head':'5 分鐘情境','body':'先給一個可觀察現象，不急著問公式或標準答案。','color':BLUE},{'head':'10 分鐘假設','body':'學生先寫「我預期會看到什麼」，AI 只能幫忙補因果句。','color':PURPLE},{'head':'全程留證據','body':'每個 AI 輸出都要回到觀察、變因、資料或圖像。','color':GREEN}],'老師把關句：AI 是探究助教，不是這堂課的裁判。'),
('第一段：先讓學生提出可檢查假設','讓 AI 介入前，學生要先說清楚變因與預期結果。',[{'head':'情境問題','body':'例如：斜面角度變大，滑下時間會怎麼改變？','color':BLUE},{'head':'學生先寫','body':'我認為＿＿會變＿＿，因為＿＿；先不查答案。','color':ORANGE},{'head':'AI 只修句型','body':'請 AI 檢查是否有自變因、應變因與因果連接。','color':GREEN}],'可複製句：請只幫我把假設改成可被實驗檢查，不要直接給答案。'),
('第二段：資料與證據要比答案早出現','AI 可以幫整理資料，但不能跳過學生的觀察紀錄。',[{'head':'小組紀錄','body':'每組先填觀察、測量值、圖像或截圖來源。','color':CYAN},{'head':'AI 整理表格','body':'把資料分成「支持假設／反對假設／還不確定」。','color':PURPLE},{'head':'老師抽查來源','body':'沒有來源的漂亮解釋，先標成待查，不進結論。','color':RED}],'課堂提醒：證據不足時，不是叫 AI 寫長一點，而是回去補資料。'),
('第三段：結論要經過同儕與老師退件','探究課的重點不是一次寫對，而是知道哪裡還不能公開。',[{'head':'同儕三問','body':'你的變因清楚嗎？證據夠嗎？有沒有反例？','color':BLUE},{'head':'AI 自評','body':'請 AI 用同一張 rubric 找出最弱的一格。','color':ORANGE},{'head':'老師退件','body':'只退流程錯誤：變因混亂、證據不足、結論超出資料。','color':GREEN}],'退件句：這不是失敗，是你找到下一輪要補的證據。'),
('把 45 分鐘變成可重用教案模板','最後留下的不是一份答案，而是一套之後每班都能複製的 AI 探究流程。',[{'head':'流程表','body':'5 情境、10 假設、15 資料、10 退件、5 Exit Ticket。','color':BLUE},{'head':'學生紀錄表','body':'預測、證據、AI 建議、我採納／不採納的理由。','color':PURPLE},{'head':'公開前提醒','body':'學生作品、截圖、真實資料與未公開教材，發布前仍需人工確認。','color':GREEN}],'下一步可自動推進：第三季優先題 4 storyboard 已完成；改把該 storyboard 擴成 35 秒 Shorts MP4 與公開檢查表。')]
outs=[make_slide(i,*data) for i,data in enumerate(slides_data,1)]
thumb_w,thumb_h=560,315
sheet=Image.new('RGB',(1880,1180),(241,245,249)); sd=ImageDraw.Draw(sheet)
sd.text((40,24),'45 分鐘 AI 物理探究課｜5 張 storyboard contact sheet', font=font(42), fill=INK)
positions=[(40,110),(660,110),(1280,110),(350,595),(970,595)]
for i,(p,pos) in enumerate(zip(outs,positions),1):
    im=Image.open(p).resize((thumb_w,thumb_h)); x,y=pos; sheet.paste(im,pos)
    sd.rectangle((x,y,x+thumb_w,y+thumb_h), outline=(148,163,184), width=3)
    sd.text((x,y+thumb_h+12), f'slide {i}', font=font(28), fill=INK)
sheet.save(CHECKS/'contact_sheet.png')
handout = """# 45 分鐘 AI 物理探究課流程講義草稿 v1

## 目標
把 AI 放進可檢查的物理探究流程：學生先提出假設、留下證據，再讓 AI 協助整理與自評。

## 45 分鐘流程
| 時間 | 活動 | AI 可以做 | 老師把關 |
|---|---|---|---|
| 0–5 分 | 情境與問題 | 不使用 AI | 問題必須可觀察、可測量 |
| 5–15 分 | 學生寫假設 | 幫忙把句子改成「因果＋變因」 | 不准直接給答案 |
| 15–30 分 | 蒐集資料／畫圖 | 整理表格、標出支持／反對證據 | 檢查來源與測量限制 |
| 30–40 分 | 同儕三問與 AI 自評 | 用 rubric 找最弱一格 | 只退流程錯誤，不代寫結論 |
| 40–45 分 | Exit Ticket | 協助整理下一輪問題 | 學生寫採納／不採納 AI 建議的理由 |

## 學生紀錄表欄位
1. 我的預測句：我認為＿＿會變＿＿，因為＿＿。
2. 我目前的證據：觀察／測量／圖像／來源。
3. AI 給我的建議：＿＿。
4. 我採納或不採納的理由：＿＿。
5. 下一輪要補的證據：＿＿。

## 老師快速退件規準
- 變因沒有寫清楚：退回重寫假設。
- 證據不足或沒有來源：退回補資料。
- 結論超出資料：退回改成「目前資料支持／尚不能判斷」。
- 涉及學生作品、照片、未公開題目或真實資料：公開前需人工確認授權與匿名化。

## 下一步
可擴成 4–6 分鐘長片旁白、SRT/VTT 與 slide-video 草稿；YouTube/Google 登入完成後再上傳。
"""
(BASE/'ai-physics-inquiry-45min-flow-handout-draft-v1.md').write_text(handout, encoding='utf-8')
readme = """# 長片 storyboard｜一堂 45 分鐘 AI 物理探究課怎麼排？

建立：2026-05-13 巡視自動推進

## 狀態
已完成本機可驗證的長片前置包：5 張 1920×1080 storyboard、45 分鐘流程講義草稿、contact sheet、manifest 與交接壓縮包。

## 內容定位
把「AI 可以進教室，但流程不能交給 AI」拆成一堂 45 分鐘物理探究課：情境、假設、資料、退件、Exit Ticket。

## 檔案
- slides/slide_01.png – slide_05.png
- checks/contact_sheet.png
- ai-physics-inquiry-45min-flow-handout-draft-v1.md
- manifest.json
- render_storyboard.py
- ai-physics-inquiry-class-storyboard-kit-20260513.tar.gz

## 已驗證
- 5 張 storyboard：1920×1080 RGB。
- contact sheet：1880×1180 RGB。
- 壓縮包：Python tarfile 可讀回列出內容。

## 下一個可自動推進項目
擴成 4–6 分鐘旁白、SRT/VTT 與 slide-video 草稿；若 YouTube/Google 登入已完成，改優先上傳首批影片。
"""
(BASE/'README.md').write_text(readme, encoding='utf-8')
manifest={
  'title':'一堂 45 分鐘 AI 物理探究課怎麼排？',
  'format':'longform_storyboard_package_v1',
  'created':'2026-05-13',
  'dimensions':{'slides':'1920x1080','contact_sheet':'1880x1180'},
  'assets':[str(p.relative_to(BASE)) for p in outs]+['checks/contact_sheet.png','ai-physics-inquiry-45min-flow-handout-draft-v1.md','README.md','render_storyboard.py'],
  'next_auto_push':'擴成 4–6 分鐘旁白、SRT/VTT 與 slide-video 草稿；YouTube/Google 登入完成後則優先上傳首批影片。'
}
(BASE/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
archive=BASE/'ai-physics-inquiry-class-storyboard-kit-20260513.tar.gz'
with tarfile.open(archive,'w:gz') as tar:
    for rel in manifest['assets']:
        tar.add(BASE/rel, arcname=f'ai-physics-inquiry-class-20260513/{rel}')
with tarfile.open(archive,'r:gz') as tar:
    names=tar.getnames()
print(json.dumps({'base':str(BASE),'slides':len(outs),'archive':str(archive),'archive_count':len(names),'names':names}, ensure_ascii=False, indent=2))
