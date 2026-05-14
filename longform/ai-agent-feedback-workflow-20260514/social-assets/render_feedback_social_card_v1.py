from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import json, math, textwrap
BASE = Path('/home/adl/youtube-lu-ai-channel/longform/ai-agent-feedback-workflow-20260514')
OUT_DIR = BASE / 'social-assets'
OUT_DIR.mkdir(parents=True, exist_ok=True)
W,H = 1080,1920
S=2
img = Image.new('RGB',(W*S,H*S),(8,13,28))
d = ImageDraw.Draw(img)
# background gradients
for y in range(H*S):
    t=y/(H*S-1)
    r=int(8+18*t); g=int(13+22*t); b=int(28+45*t)
    d.line([(0,y),(W*S,y)], fill=(r,g,b))
# glows
for cx,cy,color,rad in [(210,260,(46,196,255),360),(880,520,(139,92,246),420),(820,1540,(34,197,94),360)]:
    layer=Image.new('RGBA',(W*S,H*S),(0,0,0,0)); ld=ImageDraw.Draw(layer)
    ld.ellipse([(cx*S-rad*S,cy*S-rad*S),(cx*S+rad*S,cy*S+rad*S)], fill=(*color,90))
    layer=layer.filter(ImageFilter.GaussianBlur(130*S))
    img=Image.alpha_composite(img.convert('RGBA'),layer).convert('RGB')
d=ImageDraw.Draw(img)
# font discovery
font_paths=[
 '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',
 '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
 '/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc',
 '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
 '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
def fp(idx=0):
    for p in font_paths:
        if Path(p).exists(): return p
    return None
FONT=fp()
def font(size, bold=False): return ImageFont.truetype(FONT, size*S)
F_title=font(92, True); F_sub=font(48); F_body=font(42); F_small=font(30); F_chip=font(34)
# helpers
def round_rect(xy, r, fill, outline=None, width=1):
    xy=tuple(int(v*S) for v in xy); r=int(r*S); width=int(width*S)
    d.rounded_rectangle(xy,r,fill=fill,outline=outline,width=width)
def txt(pos, text, f, fill, anchor=None, stroke=0, stroke_fill=(0,0,0)):
    d.text((pos[0]*S,pos[1]*S), text, font=f, fill=fill, anchor=anchor, stroke_width=stroke*S, stroke_fill=stroke_fill)
def wrap_text(text, f, max_w):
    lines=[]; line=''
    for ch in text:
        test=line+ch
        if d.textbbox((0,0),test,font=f)[2] <= max_w*S:
            line=test
        else:
            if line: lines.append(line)
            line=ch
    if line: lines.append(line)
    return lines
# top chip
round_rect((70,70,410,130),30,(15,23,42),(96,165,250),2)
txt((240,100),'AI Agent 課後回饋包',F_chip,(191,219,254),anchor='mm')
# main title
for i,line in enumerate(['回饋可以加速','責任不能外包']):
    txt((70,230+i*112), line, F_title, (255,244,179) if i==0 else (255,255,255), stroke=2, stroke_fill=(3,7,18))
# central card
round_rect((60,520,1020,1265),40,(15,23,42),(51,65,85),2)
# flow boxes
items=[('1','匿名輸入','不放姓名、座號、家庭背景'),('2','AI 草稿','全班回饋、分組任務、風險句'),('3','3 色筆審稿','紅刪個資／藍補證據／綠改行動'),('4','下節課再用','教師定稿，說明 AI 協助範圍')]
y=575
colors=[(59,130,246),(139,92,246),(239,68,68),(34,197,94)]
for n,head,body in items:
    round_rect((105,y,190,y+92),24,(*colors[int(n)-1],255)[:3])
    txt((147,y+45),n,F_body,(255,255,255),anchor='mm')
    txt((220,y+20),head,F_body,(248,250,252))
    for j,l in enumerate(wrap_text(body,F_small,690)[:2]):
        txt((220,y+65+j*38),l,F_small,(203,213,225))
    y += 165
# bottom CTA box
round_rect((70,1345,1010,1675),44,(250,204,21),(120,53,15),3)
txt((105,1395),'教師檢查句',F_body,(24,24,27))
for j,l in enumerate(['這句回饋有證據嗎？','有下一步行動嗎？','已移除可識別個資嗎？']):
    txt((120,1460+j*58),'- '+l,F_body,(24,24,27))
# footer
round_rect((70,1740,1010,1835),30,(15,23,42),(45,212,191),2)
txt((540,1788),'盧老師 × AI 物理教學｜可轉成 Shorts／社群貼文',F_small,(204,251,241),anchor='mm')
out=OUT_DIR/'ai-agent-feedback-workflow-social-card-v1.png'
img=img.resize((W,H),Image.Resampling.LANCZOS)
img.save(out)
manifest={
 'asset':'social-assets/ai-agent-feedback-workflow-social-card-v1.png',
 'render_script':'social-assets/render_feedback_social_card_v1.py',
 'size':[W,H], 'mode':'RGB',
 'source_handout':'slide_video_draft_v1/feedback-package-review-shareable-handout-v1.md',
 'purpose':'vertical Shorts/community card derived from the shareable handout',
 'text':['回饋可以加速','責任不能外包','匿名輸入','AI 草稿','3 色筆審稿','下節課再用']
}
(OUT_DIR/'ai-agent-feedback-workflow-social-card-v1.manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
# copy this script into package for reproducibility
(Path(__file__).read_text(encoding='utf-8'))
(OUT_DIR/'render_feedback_social_card_v1.py').write_text(Path(__file__).read_text(encoding='utf-8'),encoding='utf-8')
print(out)
