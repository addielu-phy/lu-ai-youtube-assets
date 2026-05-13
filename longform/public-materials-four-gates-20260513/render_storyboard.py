from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import textwrap
BASE = Path('/home/adl/youtube-lu-ai-channel/longform/public-materials-four-gates-20260513')
SLIDES = [
    ('slides/01_hook_four_gates.png','第三季優先題 6｜長片 storyboard','公開教材前，先過四道門',['AI 可以幫你把教材整理得很快','但能不能分享，不只看內容漂亮不漂亮','先檢查：來源、授權、個資、AI 標註'],'核心句：分享前先把風險變成清單。'),
    ('slides/02_source_gate.png','Gate 1｜來源門','這份資料從哪裡來？',['把每張圖、每段文字、每個數據都標出來源','找不到來源的素材，先不要放進公開版','學生作品只用匿名化與已授權版本'],'可複製問句：這個素材的原始出處可以被查到嗎？'),
    ('slides/03_license_gate.png','Gate 2｜授權門','可以用，不等於可以公開分享',['課內展示、下載講義、公開網站，授權需求不同','保留授權截圖、連結與使用日期','不確定就改用自繪圖、公開授權素材或摘要重製'],'把「看起來能用」改成「授權寫得清楚」。'),
    ('slides/04_privacy_ai_label_gate.png','Gate 3 + 4｜個資門與 AI 標註門','刪掉可識別資訊，說清楚 AI 做了什麼',['姓名、班級、座號、照片、聲音、作品細節都要檢查','AI 產生、AI 改寫、AI 摘要，標註方式要一致','讓學生知道：公開版是被老師審過的版本'],'公開不是把草稿貼出去，而是交出可負責版本。'),
    ('slides/05_classroom_flow.png','45 分鐘課堂流程草案','把四道門變成學生能做的檢查流程',['5 分：看一份 AI 整理的教材草稿','15 分：小組用四關表找出風險與缺口','15 分：改成可公開版本，補來源與標註','10 分：互評一句「還不能公開，因為…」'],'下一步：擴成 4–6 分鐘旁白、字幕與 slide-video 草稿。'),
]
FONT_CANDIDATES = [
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',
    '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
    '/usr/share/fonts/opentype/unifont/unifont.otf'
]
def font(size, bold=False):
    paths = FONT_CANDIDATES[1:2] + FONT_CANDIDATES if bold else FONT_CANDIDATES
    for p in paths:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()
def wrap(draw, text, fnt, max_width):
    out=[]
    line=''
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
    colors=['#1d4ed8','#0f766e','#b45309','#7c3aed','#be123c']
    accent=colors[(idx-1)%len(colors)]
    d.rounded_rectangle((70,70,1850,1010), radius=42, fill='#ffffff', outline='#dbeafe', width=4)
    d.rectangle((70,70,1850,180), fill=accent)
    d.text((120,105), kicker, font=font(42), fill='white')
    y=245
    for line in wrap(d,title,font(76,True),1560):
        d.text((120,y), line, font=font(76,True), fill='#0f172a')
        y += 92
    y += 25
    for b in body:
        d.rounded_rectangle((130,y,1790,y+92), radius=22, fill='#eef2ff', outline='#c7d2fe', width=2)
        d.ellipse((160,y+30,190,y+60), fill=accent)
        x=220
        yy=y+23
        lines=wrap(d,b,font(38),1480)
        for line in lines[:2]:
            d.text((x,yy), line, font=font(38), fill='#1e293b')
            yy += 43
        y += 112
    d.rounded_rectangle((120,900,1800,970), radius=22, fill='#fff7ed', outline='#fed7aa', width=2)
    d.text((150,914), takeaway, font=font(34,True), fill='#9a3412')
    d.text((120,1000), '盧老師 AI 物理教學｜storyboard draft', font=font(26), fill='#64748b')
    img.save(BASE/rel)
for i,item in enumerate(SLIDES,1):
    draw_slide(item,i)
# contact sheet
thumbs=[]
for rel, *_ in SLIDES:
    im=Image.open(BASE/rel).resize((576,324))
    thumbs.append((rel,im))
sheet=Image.new('RGB',(1920,1180),'#f1f5f9')
d=ImageDraw.Draw(sheet)
d.text((60,35),'公開教材四關｜5 張長片 storyboard QA',font=font(46,True),fill='#0f172a')
positions=[(60,120),(672,120),(1284,120),(360,560),(972,560)]
for idx,((rel,im),(x,y)) in enumerate(zip(thumbs,positions),1):
    sheet.paste(im,(x,y))
    d.rectangle((x,y,x+576,y+324), outline='#94a3b8', width=3)
    d.text((x,y+338), f'{idx}. {Path(rel).name}', font=font(28), fill='#334155')
sheet.save(BASE/'checks/contact_sheet.png')
