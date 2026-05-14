from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
BASE = Path('/home/adl/youtube-lu-ai-channel/longform/ai-agent-feedback-workflow-20260514')
SLIDES = [
    ('slides/01_hook_feedback_workflow.png','第三季優先題 9｜長片 storyboard','AI 不是代寫評語，而是進入審稿線',['課後回饋包最怕兩件事：太快、太像罐頭','把 AI 放在「草稿產生」的位置，不放在「直接送出」的位置','這支片示範：匿名資料 → AI 草稿 → 教師審稿 → 回饋包'],'核心句：回饋可以加速，但責任不能外包。'),
    ('slides/02_input_boundary.png','Step 1｜輸入邊界','先餵匿名資料，不餵學生身分',['只放錯因類型、作答摘要、共通迷思，不放姓名座號','每組資料先標「可公開／不可公開／需改寫」','AI 看到的是學習證據，不是學生標籤'],'可複製句：請根據匿名作答摘要，先分類錯因，不要寫個人評價。'),
    ('slides/03_ai_draft_package.png','Step 2｜AI 只產草稿包','要求 AI 分成三格，不要一口氣寫完',['A 格：全班共通回饋，指出下一個練習方向','B 格：分組補救任務，對準錯因與難度階梯','C 格：教師需確認的風險句與可能誤判'],'把 AI 的輸出變成「可退件清單」，而不是可直接貼上的評語。'),
    ('slides/04_teacher_review_line.png','Step 3｜教師審稿線','三色筆審稿：刪、改、補',['紅筆：刪掉個資、貼標籤、過度保證的句子','藍筆：改成具體學習證據與下一步行動','綠筆：補上老師知道但 AI 不知道的課堂脈絡'],'審稿重點：學生收到的是老師負責的回饋，不是 AI 的判決。'),
    ('slides/05_45min_reuse_flow.png','45 分鐘課後回饋流程','把一次回饋變成下次教學素材',['10 分：整理匿名作答摘要與錯因標籤','15 分：AI 產出回饋草稿包與補救任務','15 分：教師三色筆審稿並定稿','5 分：把共通回饋變成下節課開場或 Exit Ticket'],'下一步：擴成 4–6 分鐘旁白、字幕、slide-video 與正式回饋包講義。'),
]
FONT_CANDIDATES = [
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
    '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
    '/usr/share/fonts/opentype/unifont/unifont.otf'
]
def font(size, bold=False):
    order = FONT_CANDIDATES if bold else FONT_CANDIDATES[1:]+FONT_CANDIDATES[:1]
    for p in order:
        if Path(p).exists(): return ImageFont.truetype(p, size)
    return ImageFont.load_default()
def wrap(draw, text, fnt, max_width):
    out=[]; line=''
    for ch in text:
        test=line+ch
        if draw.textbbox((0,0), test, font=fnt)[2] <= max_width:
            line=test
        else:
            if line: out.append(line)
            line=ch
    if line: out.append(line)
    return out
def draw_slide(item, idx):
    rel,kicker,title,body,takeaway=item
    img=Image.new('RGB',(1920,1080),'#f8fafc')
    d=ImageDraw.Draw(img)
    colors=['#4f46e5','#0f766e','#b45309','#be123c','#0369a1']
    accent=colors[(idx-1)%len(colors)]
    d.rounded_rectangle((70,70,1850,1010), radius=44, fill='#ffffff', outline='#dbeafe', width=4)
    d.rectangle((70,70,1850,184), fill=accent)
    d.text((120,106), kicker, font=font(42), fill='white')
    y=245
    for line in wrap(d,title,font(74,True),1580)[:2]:
        d.text((120,y), line, font=font(74,True), fill='#0f172a'); y += 88
    y += 22
    for b in body:
        lines=wrap(d,b,font(38),1440)
        h=82 + max(0,len(lines)-1)*42
        d.rounded_rectangle((130,y,1790,y+h), radius=24, fill='#eef2ff', outline='#c7d2fe', width=2)
        d.ellipse((160,y+28,192,y+60), fill=accent)
        yy=y+22
        for line in lines[:2]:
            d.text((225,yy), line, font=font(38), fill='#1e293b'); yy+=43
        y += h + 24
    d.rounded_rectangle((120,900,1800,972), radius=22, fill='#fff7ed', outline='#fed7aa', width=2)
    ty=914
    for line in wrap(d,takeaway,font(33,True),1580)[:2]:
        d.text((150,ty), line, font=font(33,True), fill='#9a3412'); ty += 36
    d.text((120,1000), '盧老師 AI 物理教學｜storyboard draft', font=font(26), fill='#64748b')
    img.save(BASE/rel)
for i,item in enumerate(SLIDES,1):
    draw_slide(item,i)
thumbs=[]
for rel, *_ in SLIDES:
    thumbs.append((rel,Image.open(BASE/rel).resize((576,324))))
sheet=Image.new('RGB',(1920,1180),'#f1f5f9')
d=ImageDraw.Draw(sheet)
d.text((60,35),'AI Agent 課後回饋包｜5 張長片 storyboard QA',font=font(44,True),fill='#0f172a')
positions=[(60,120),(672,120),(1284,120),(360,560),(972,560)]
for idx,((rel,im),(x,y)) in enumerate(zip(thumbs,positions),1):
    sheet.paste(im,(x,y)); d.rectangle((x,y,x+576,y+324), outline='#94a3b8', width=3)
    d.text((x,y+338), f'{idx}. {Path(rel).name}', font=font(26), fill='#334155')
sheet.save(BASE/'checks/contact_sheet.png')
