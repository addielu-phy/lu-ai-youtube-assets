from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import json, tarfile

BASE = Path('/home/adl/youtube-lu-ai-channel')
PKG = BASE / 'shorts' / 'three-verifiable-evidence-before-answer-20260512'
SLIDES = PKG / 'slides'
CHECKS = PKG / 'checks'
SLIDES.mkdir(parents=True, exist_ok=True)
CHECKS.mkdir(parents=True, exist_ok=True)
FONT = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
W, H = 1080, 1920
palette = {
    'bg': '#0F2034', 'ink': '#102033', 'blue': '#2F6FD6',
    'orange': '#F4A340', 'green': '#2FAE77', 'cream': '#FFF8EA',
    'red': '#E4574F', 'muted': '#5F6E7A'
}

def font(size):
    return ImageFont.truetype(FONT, size)

slides = [
    {'n':'01','tag':'3秒鉤子','title':'AI 給答案前，\n先要三個證據','body':['學生一問，AI 馬上給答案。','老師先按暫停：答案先放旁邊，證據在哪？'],'chips':['現象','數據','原理'],'call':'先要證據，再看答案'},
    {'n':'02','tag':'物理情境','title':'用一題問題\n把證據列出來','body':['題目：小車下滑時，速度為什麼變快？','請 AI 先列：① 觀察到什麼 ② 可量到什麼 ③ 用哪個原理。'],'chips':['看得到','量得到','說得通'],'call':'證據要能被檢查'},
    {'n':'03','tag':'老師追問句','title':'不要只問 AI：\n答案是什麼？','body':['改成可複製句：','「在回答前，請先列出三個可驗證證據，並標明每個證據怎麼檢查。」'],'chips':['列證據','標檢查法','再回答'],'call':'把 AI 變成受檢者'},
    {'n':'04','tag':'學生任務','title':'三欄證據卡\n5 分鐘就能做','body':['證據｜我怎麼驗證｜它支持哪一句答案','學生先填一格，再跟 AI 的說法比對。'],'chips':['證據','驗證','支持'],'call':'不是抄答案，是比對證據'},
    {'n':'05','tag':'收尾 CTA','title':'老師的把關句','body':['「沒有證據的 AI 答案，只能當草稿。」','下一步可延伸：一頁證據追問小抄＋35 秒 Shorts。'],'chips':['草稿','證據','修正'],'call':'答案漂亮，也要先過證據關'}
]

def wrap(draw, text, fnt, maxw):
    out = []
    for para in text.split('\n'):
        line = ''
        for ch in para:
            if draw.textbbox((0,0), line + ch, font=fnt)[2] <= maxw:
                line += ch
            else:
                if line:
                    out.append(line)
                line = ch
        if line:
            out.append(line)
    return out

def draw_center(draw, xy, text, fnt, fill, maxw=None):
    x1, y1, x2, y2 = xy
    lines = wrap(draw, text, fnt, maxw or (x2-x1-40))
    total = len(lines) * (fnt.size + 10) - 10
    y = y1 + ((y2-y1-total)//2)
    for line in lines:
        bbox = draw.textbbox((0,0), line, font=fnt)
        tw = bbox[2] - bbox[0]
        draw.text((x1 + ((x2-x1-tw)//2), y), line, font=fnt, fill=fill)
        y += fnt.size + 10

def draw_slide(s):
    im = Image.new('RGB', (W,H), palette['bg'])
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([60,70,1020,1850], radius=52, fill=palette['cream'])
    d.rounded_rectangle([100,120,980,298], radius=38, fill=palette['blue'])
    d.text((140,168), f"第三季 Shorts｜{s['tag']}", font=font(52), fill='white')
    y = 380
    for line in s['title'].split('\n'):
        d.text((110,y), line, font=font(86), fill=palette['ink'])
        y += 110
    d.rounded_rectangle([110,y+18,970,y+36], radius=8, fill=palette['orange'])
    y += 94
    d.rounded_rectangle([110,y,970,1338], radius=34, fill='white', outline='#E2D6C7', width=4)
    yy = y + 50
    for item in s['body']:
        f = font(46 if len(item) <= 20 else 41)
        for line in wrap(d, item, f, 790):
            d.text((155, yy), line, font=f, fill=palette['ink'])
            yy += 60
        yy += 20
    basey = 1418
    chip_colors = [palette['green'], palette['blue'], palette['orange']]
    for i, label in enumerate(s['chips']):
        x = 110 + i*295
        d.rounded_rectangle([x,basey,x+245,basey+126], radius=30, fill=chip_colors[i])
        draw_center(d, (x+8, basey+12, x+237, basey+114), label, font(40), 'white', 210)
        if i < 2:
            d.line([x+260,basey+63,x+288,basey+63], fill=palette['ink'], width=8)
            d.polygon([(x+288,basey+63),(x+266,basey+48),(x+266,basey+78)], fill=palette['ink'])
    d.rounded_rectangle([110,1635,970,1788], radius=34, fill=palette['ink'])
    draw_center(d, (130,1650,950,1778), s['call'], font(50), 'white', 760)
    d.text((110,1810), '盧老師 × AI 物理教學｜storyboard draft', font=font(30), fill=palette['muted'])
    path = SLIDES / f"slide_{s['n']}.png"
    im.save(path)
    return path

paths = [draw_slide(s) for s in slides]
thumb_w, thumb_h = 324, 576
sheet = Image.new('RGB', (1120,1480), '#1B2635')
d = ImageDraw.Draw(sheet)
d.text((40,28), 'AI 給答案前，先叫它列出三個可驗證證據｜5 張 storyboard', font=font(34), fill='white')
positions = [(40,92),(398,92),(756,92),(220,744),(578,744)]
for i, p in enumerate(paths):
    im = Image.open(p).resize((thumb_w, thumb_h))
    x, y = positions[i]
    sheet.paste(im, (x,y))
    d.text((x,y+thumb_h+10), f"slide {i+1}", font=font(28), fill='white')
sheet.save(CHECKS / 'contact_sheet.png')

manifest = {
    'title': 'AI 給答案前，先叫它列出三個可驗證證據',
    'candidate': 'season-03-priority-01',
    'status': 'storyboard package v1 complete',
    'created': '2026-05-12',
    'dimensions': '1080x1920',
    'slides': [str(p.relative_to(PKG)) for p in paths],
    'contact_sheet': 'checks/contact_sheet.png',
    'next_auto_push': 'expand storyboard into zh-TW narration/VTT/SRT/35s MP4/cover/upload kit, unless YouTube login is ready for upload'
}
(PKG / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')

readme = """# Shorts storyboard｜AI 給答案前，先叫它列出三個可驗證證據

狀態：2026-05-12 每小時雷達自動推進完成 storyboard package v1。  
來源：第三季內容題庫優先題 1。

## 30 秒製作簡報

- 3 秒鉤子：答案先放旁邊，證據在哪？
- 核心觀點：AI 回答前先列三個可驗證證據，學生才有基準判斷答案是不是只是在「講得很順」。
- 對象：國高中自然／物理教師，可用於 5 分鐘暖身、AI 解題審稿或證據評分規準延伸活動。
- 最小素材：5 張 9:16 圖卡、三欄證據卡、老師追問句。

## 圖卡

1. `slides/slide_01.png`｜AI 給答案前，先要三個證據
2. `slides/slide_02.png`｜用一題問題把證據列出來
3. `slides/slide_03.png`｜不要只問 AI：答案是什麼？
4. `slides/slide_04.png`｜三欄證據卡 5 分鐘就能做
5. `slides/slide_05.png`｜老師把關句與 CTA

## 驗證

- PIL 輸出：5 張 `1080×1920` RGB PNG。
- Contact sheet：`checks/contact_sheet.png`。
- 視覺 QA：已檢查繁中主文字可讀、無 tofu 方塊、無裁切、無重疊；contact sheet 排版不擁擠。

## 穩定發布

- 手機索引：`https://addielu-phy.github.io/lu-ai-youtube-assets/mobile-index/index.html`
- Storyboard README：`https://addielu-phy.github.io/lu-ai-youtube-assets/shorts/three-verifiable-evidence-before-answer-20260512/README.md`
- QA contact sheet：`https://addielu-phy.github.io/lu-ai-youtube-assets/shorts/three-verifiable-evidence-before-answer-20260512/checks/contact_sheet.png`
- GitHub Pages commit：`dbe57b9` 已驗證。

## 下一個自動推進

若 YouTube/Google 登入仍未完成：把本 storyboard 擴成 zh-TW 旁白、VTT/SRT、35 秒 MP4、封面與 upload kit。  
若使用者已完成 YouTube/Google 登入：優先上傳已完成的第一季首批 Shorts 或第二季代表作。
"""
(PKG / 'README.md').write_text(readme, encoding='utf-8')

archive = PKG / 'three-verifiable-evidence-before-answer-storyboard-kit-20260512.tar.gz'
with tarfile.open(archive, 'w:gz') as tar:
    for rel in ['README.md','manifest.json','render_storyboard.py','checks/contact_sheet.png']:
        tar.add(PKG / rel, arcname=f'three-verifiable-evidence-before-answer-20260512/{rel}')
    for p in paths:
        tar.add(p, arcname=f'three-verifiable-evidence-before-answer-20260512/slides/{p.name}')
print(PKG)
print(archive)
