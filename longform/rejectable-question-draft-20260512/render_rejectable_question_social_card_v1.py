from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import json

BASE = Path('/home/adl/youtube-lu-ai-channel/longform/rejectable-question-draft-20260512')
OUT = BASE / 'social-assets'
OUT.mkdir(parents=True, exist_ok=True)
W, H = 1080, 1920
S = 2
FONT = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
CANVAS = (W*S, H*S)

def font(size):
    return ImageFont.truetype(FONT, size*S)

def rr(draw, xy, r, fill, outline=None, width=1):
    draw.rounded_rectangle(tuple(int(v*S) for v in xy), radius=int(r*S), fill=fill, outline=outline, width=max(1, int(width*S)))

def center_text(draw, box, text, fnt, fill, spacing=8, stroke_width=0, stroke_fill=(0,0,0)):
    x1,y1,x2,y2 = [v*S for v in box]
    lines = text.split('\n')
    dims = [draw.textbbox((0,0), line, font=fnt, stroke_width=stroke_width) for line in lines]
    heights = [b[3]-b[1] for b in dims]
    widths = [b[2]-b[0] for b in dims]
    total_h = sum(heights) + (len(lines)-1)*spacing*S
    y = y1 + (y2-y1-total_h)/2
    for line, h, w in zip(lines, heights, widths):
        x = x1 + (x2-x1-w)/2
        draw.text((x,y), line, font=fnt, fill=fill, stroke_width=stroke_width, stroke_fill=stroke_fill)
        y += h + spacing*S

def draw_wrapped(draw, xy, text, fnt, fill, max_chars, line_gap=8):
    x, y = xy
    lines = []
    for seg in text.split('\n'):
        while len(seg) > max_chars:
            lines.append(seg[:max_chars])
            seg = seg[max_chars:]
        lines.append(seg)
    for line in lines:
        draw.text((x*S, y*S), line, font=fnt, fill=fill)
        b = draw.textbbox((0,0), line, font=fnt)
        y += (b[3]-b[1])//S + line_gap
    return y

img = Image.new('RGB', CANVAS, '#07111f')
d = ImageDraw.Draw(img)
# premium dark gradient
for y in range(CANVAS[1]):
    t = y / CANVAS[1]
    r = int(5 + 17*t)
    g = int(13 + 22*t)
    b = int(28 + 40*t)
    d.line([(0,y),(CANVAS[0],y)], fill=(r,g,b))
# soft glows
for cx, cy, color, rad, alpha in [
    (170,240,(38,216,235),260,56),
    (920,385,(150,92,255),360,50),
    (820,1450,(255,215,82),300,36),
    (160,1480,(255,82,96),260,30),
]:
    layer = Image.new('RGBA', CANVAS, (0,0,0,0)); ld = ImageDraw.Draw(layer)
    ld.ellipse(((cx-rad)*S,(cy-rad)*S,(cx+rad)*S,(cy+rad)*S), fill=color+(alpha,))
    layer = layer.filter(ImageFilter.GaussianBlur(95*S))
    img = Image.alpha_composite(img.convert('RGBA'), layer).convert('RGB')
    d = ImageDraw.Draw(img)
# subtle grid
for x in range(80, 1080, 160):
    d.line([(x*S,0),(x*S,H*S)], fill=(255,255,255,10), width=1*S)
for y in range(120, 1920, 160):
    d.line([(0,y*S),(W*S,y*S)], fill=(255,255,255,8), width=1*S)

# header chip
rr(d, (70,78,470,142), 24, (15,31,54), (73,225,238), 2)
d.text((98*S,96*S), 'AI 出題工作流', font=font(30), fill=(168,240,248))
# title
center_text(d, (68,155,1012,430), '可退件\n草稿', font(106), (255,232,104), spacing=16, stroke_width=3*S, stroke_fill=(0,0,0))
d.text((134*S,432*S), '好題目不是一次生成', font=font(45), fill=(238,247,255))
d.text((134*S,492*S), '先讓 AI 交出能被老師退件的版本', font=font(34), fill=(178,207,230))

# main document panel
rr(d, (78,565,1002,1665), 44, (13,25,42), (84,118,152), 2)
rr(d, (124,614,956,716), 28, (20,45,72), (90,220,238), 2)
d.text((156*S,644*S), '退件前先鎖 3 件事', font=font(46), fill=(255,255,255))

items = [
    ('1', '年級與單元', '不要讓 AI 自己猜學生程度', '#4de1ff'),
    ('2', '只測一件事', '每題先對準一個學習目標', '#ffd84d'),
    ('3', '輸出格式', '題幹、答案、退件理由分欄', '#ff6b73'),
]
y = 760
for n, title, body, hexcol in items:
    rgb = tuple(int(hexcol[i:i+2], 16) for i in (1,3,5))
    rr(d, (132,y,948,y+205), 32, (18,36,58), rgb, 4)
    d.ellipse((166*S,(y+34)*S,236*S,(y+104)*S), fill=rgb, outline=(255,255,255), width=3*S)
    center_text(d, (166,y+34,236,y+104), n, font(38), (8,18,32), spacing=0)
    d.text((270*S,(y+26)*S), title, font=font(52), fill=(255,255,255))
    d.text((270*S,(y+98)*S), body, font=font(31), fill=(210,228,242))
    y += 245

# rejection badge and CTA
rr(d, (128,1504,952,1608), 26, (255,224,86), None, 1)
center_text(d, (148,1512,932,1602), '退件不是否定 AI，是把草稿變成可教的題目', font(31), (9,18,32), spacing=0)
rr(d, (70,1694,1010,1810), 30, (7,17,31), (73,226,239), 2)
d.text((105*S,1724*S), '搭配長片：AI 幫老師出題前的退件流程', font=font(30), fill=(196,240,246))
d.text((105*S,1767*S), '盧老師 × AI 物理備課室', font=font(27), fill=(142,165,190))

img = img.resize((W,H), Image.Resampling.LANCZOS)
out = OUT / 'rejectable-question-draft-social-card-v1.png'
img.save(out)
manifest = {
    'asset': str(out),
    'size': [W, H],
    'mode': 'RGB',
    'purpose': '1080x1920 Shorts cover / community post card derived from rejectable-question-draft shareable handout',
    'source': 'rejectable-question-draft-shareable-handout-v1.md',
    'text': ['可退件草稿', '好題目不是一次生成', '年級與單元', '只測一件事', '輸出格式'],
    'font': FONT,
    'created_by': 'render_rejectable_question_social_card_v1.py'
}
(OUT / 'rejectable-question-draft-social-card-v1-manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
print(out)
