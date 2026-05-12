from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import json, subprocess, tarfile, re

BASE = Path('/home/adl/youtube-lu-ai-channel')
PKG = BASE / 'shorts' / 'hypothesis-causal-variable-20260513'
SLIDES = PKG / 'slides'
CHECKS = PKG / 'checks'
CHECKS.mkdir(parents=True, exist_ok=True)
FONT = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
W, H = 1080, 1920
TARGET = 35.0
SLUG = 'hypothesis-causal-variable'
MP4 = PKG / f'{SLUG}-shorts-35s.mp4'
COVER = PKG / 'cover_hypothesis_causal_variable_v1.png'
ARCHIVE = PKG / f'{SLUG}-upload-kit-20260513.tar.gz'

palette = {'bg':'#102033','cream':'#FFF8EA','ink':'#11243A','blue':'#2F6FD6','orange':'#F4A340','green':'#2FAE77','red':'#E4574F','muted':'#607080','purple':'#6C63D9'}

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

def center(draw, box, text, fnt, fill, maxw=None, leading=10):
    x1,y1,x2,y2 = box
    lines = wrap(draw, text, fnt, maxw or (x2-x1-40))
    total = len(lines)*(fnt.size+leading)-leading
    y = y1 + (y2-y1-total)//2
    for line in lines:
        bbox = draw.textbbox((0,0), line, font=fnt)
        tw = bbox[2]-bbox[0]
        draw.text((x1+(x2-x1-tw)//2, y), line, font=fnt, fill=fill)
        y += fnt.size + leading

def render_cover():
    im = Image.new('RGB', (W,H), palette['bg'])
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([72,86,1008,1834], radius=54, fill=palette['cream'])
    d.rounded_rectangle([112,140,968,300], radius=38, fill=palette['purple'])
    center(d, (130,155,950,286), 'AI 假設生成｜變因先鎖住', font(50), 'white', 780)
    center(d, (110,355,970,700), '讓 AI 寫假設\n先加一句話', font(86), palette['ink'], 820, 12)
    d.rounded_rectangle([145,748,935,778], radius=10, fill=palette['orange'])
    cards = [
        ('如果', '我改變＿＿', palette['green']),
        ('那麼', '＿＿會＿＿', palette['blue']),
        ('因為', '原因要可檢查', palette['orange']),
    ]
    y = 875
    for title, body, color in cards:
        d.rounded_rectangle([130,y,950,y+190], radius=36, fill='white', outline='#E2D6C7', width=4)
        d.rounded_rectangle([155,y+35,315,y+155], radius=26, fill=color)
        center(d, (165,y+42,305,y+148), title, font(48), 'white', 120)
        center(d, (345,y+38,920,y+154), body, font(52), palette['ink'], 520)
        y += 230
    d.rounded_rectangle([130,1618,950,1765], radius=34, fill=palette['ink'])
    center(d, (150,1636,930,1748), '沒有因果鏈，就先退件', font(52), 'white', 740)
    im.save(COVER)

render_cover()

weights = [6.5,7.0,7.2,7.2,7.1]
scale = TARGET/sum(weights)
concat = PKG / 'slides_35s.ffconcat'
lines = ['ffconcat version 1.0']
for i,w in enumerate(weights,1):
    p = SLIDES / f'slide_{i:02d}.png'
    lines.append(f"file '{p.as_posix()}'")
    lines.append(f'duration {w*scale:.3f}')
lines.append(f"file '{(SLIDES/'slide_05.png').as_posix()}'")
concat.write_text('\n'.join(lines)+'\n', encoding='utf-8')

vtt = PKG / 'narration_35s_edge_hsiaoyu.vtt'
srt = PKG / 'narration_35s_edge_hsiaoyu.srt'
text = vtt.read_text(encoding='utf-8') if vtt.exists() else ''
blocks=[]
for block in re.split(r'\n\s*\n', text.strip()):
    if '-->' not in block: continue
    b_lines = block.splitlines()
    timing = next(l for l in b_lines if '-->' in l)
    caption = ' '.join(l.strip() for l in b_lines[b_lines.index(timing)+1:] if l.strip())
    blocks.append((timing.replace('.', ','), caption))
srt.write_text('\n\n'.join(f'{i}\n{t}\n{c}' for i,(t,c) in enumerate(blocks,1))+'\n', encoding='utf-8')

subprocess.run(['ffmpeg','-y','-f','concat','-safe','0','-i',str(concat),'-i',str(PKG/'narration_35s_edge_hsiaoyu.mp3'),'-t',f'{TARGET:.3f}','-vf','fps=25,format=yuv420p','-af','apad','-c:v','libx264','-preset','veryfast','-crf','18','-c:a','aac','-b:a','128k',str(MP4)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

for name, ts in [('frame_early.png',2.0),('frame_mid.png',17.0),('frame_late.png',32.0)]:
    subprocess.run(['ffmpeg','-y','-ss',str(ts),'-i',str(MP4),'-frames:v','1','-update','1',str(CHECKS/name)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

thumb_w, thumb_h = 360, 640
sheet = Image.new('RGB', (1600,1650), '#1B2635')
d = ImageDraw.Draw(sheet)
d.text((50,35), 'AI 假設因果變因｜Shorts MP4 QA sheet（cover + early/mid/late）', font=font(38), fill='white')
items = [('cover',COVER),('early 2s',CHECKS/'frame_early.png'),('mid 17s',CHECKS/'frame_mid.png'),('late 32s',CHECKS/'frame_late.png')]
pos = [(80,110),(600,110),(80,870),(600,870)]
for (label,p),(x,y) in zip(items,pos):
    im = Image.open(p).resize((thumb_w,thumb_h))
    sheet.paste(im,(x,y))
    d.text((x,y+thumb_h+16), label, font=font(32), fill='white')
sheet.save(CHECKS/'qa_sheet_mp4.png')

upload = f'''# YouTube Upload Kit｜讓 AI 幫學生寫假設，但老師要加上哪一句？

## 建議標題
1. 讓 AI 寫假設前，老師先加這一句
2. 假設不是猜答案：用一句話鎖住變因
3. AI 產生探究假設，先檢查如果／那麼／因為

## 主檔案
- Shorts MP4：`{MP4.name}`
- 封面：`{COVER.name}`
- 旁白：`narration_35s_edge_hsiaoyu.mp3`
- 字幕：`narration_35s_edge_hsiaoyu.vtt` / `narration_35s_edge_hsiaoyu.srt`
- QA sheet：`checks/qa_sheet_mp4.png`

## 描述草稿
學生請 AI 寫假設時，老師可以先加一句：請用「如果我改變＿＿，那麼＿＿會＿＿，因為＿＿」來回答。這會把操縱變因、應變變因與原因鎖在同一條因果鏈裡，假設才可測、可退件、可修正。

#AI教學 #物理教學 #探究實作 #生成式AI #教師備課 #AI素養

## 置頂留言
可直接複製給學生：
「請把假設寫成：如果我改變＿＿，那麼＿＿會＿＿，因為＿＿。沒有變因、結果與原因，就先重寫。」

## 人工操作卡點
YouTube 上傳、頻道選擇、公開／排程與留言置頂仍需使用者登入 Google / YouTube 後操作。
'''
(PKG/'youtube-upload-kit.md').write_text(upload, encoding='utf-8')

readme = f'''# Shorts｜讓 AI 幫學生寫假設，但老師要加上哪一句？

狀態：2026-05-13 每小時雷達已把 storyboard 擴成 35 秒本機 Shorts 草稿、封面、字幕與 YouTube upload kit。  
來源：第三季內容題庫優先題 2。

## 成果檔案

- Shorts MP4：`{MP4.name}`
- 封面：`{COVER.name}`
- 上傳包：`youtube-upload-kit.md`
- 旁白：`narration_35s_edge_hsiaoyu.mp3`
- 字幕：`narration_35s_edge_hsiaoyu.vtt` / `narration_35s_edge_hsiaoyu.srt`
- QA sheet：`checks/qa_sheet_mp4.png`
- 壓縮包：`{ARCHIVE.name}`

## 圖卡

1. `slides/slide_01.png`｜讓 AI 寫假設，先加一句話
2. `slides/slide_02.png`｜錯誤示範：太像答案、不可測
3. `slides/slide_03.png`｜老師加的一句：如果／那麼／因為
4. `slides/slide_04.png`｜修正版：斜面角度、底端速度、原因
5. `slides/slide_05.png`｜退件規則與 CTA

## 驗證

- MP4：1080×1920、25fps、H.264 + AAC、35 秒。
- PIL：封面、5 張圖卡與 QA 抽幀皆為 RGB 圖檔。
- 視覺 QA：`checks/qa_sheet_mp4.png` 已用於檢查繁中可讀、無 tofu 方塊、無裁切、無重疊與不過度擁擠。
- 壓縮包：已用 Python `tarfile` 讀回確認包含 MP4、封面、旁白、字幕、README、manifest、upload kit、slides 與 QA sheet。

## 穩定發布

- 手機索引：`https://addielu-phy.github.io/lu-ai-youtube-assets/mobile-index/index.html`
- 本機 package：`shorts/hypothesis-causal-variable-20260513/`
- GitHub Pages commit：待同步後回填。

## 下一個自動推進

若 YouTube/Google 登入仍未完成：從第三季題庫挑選下一個尚未完成的 Shorts storyboard／講義延伸。  
若使用者已完成 YouTube/Google 登入：優先上傳已完成的第一季首批 Shorts 或本支第三季 Shorts。
'''
(PKG/'README.md').write_text(readme, encoding='utf-8')

manifest = json.loads((PKG/'manifest.json').read_text(encoding='utf-8'))
manifest.update({
    'status':'35s Shorts MP4 + upload kit complete',
    'mp4':MP4.name,
    'cover':COVER.name,
    'upload_kit':'youtube-upload-kit.md',
    'narration':'narration_35s_edge_hsiaoyu.mp3',
    'subtitles':['narration_35s_edge_hsiaoyu.vtt','narration_35s_edge_hsiaoyu.srt'],
    'qa_sheet':'checks/qa_sheet_mp4.png',
    'archive':ARCHIVE.name,
    'next_auto_push':'choose next unfinished season-03 candidate for storyboard/handout, unless YouTube login is ready for upload'
})
files = ['README.md','manifest.json','render_storyboard.py','build_shorts_mp4_package.py','youtube-upload-kit.md',MP4.name,COVER.name,'narration_35s.txt','narration_35s_edge_hsiaoyu.mp3','narration_35s_edge_hsiaoyu.vtt','narration_35s_edge_hsiaoyu.srt','checks/contact_sheet.png','checks/qa_sheet_mp4.png','checks/frame_early.png','checks/frame_mid.png','checks/frame_late.png','slides_35s.ffconcat'] + [f'slides/slide_{i:02d}.png' for i in range(1,6)]
manifest['files'] = files
(PKG/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')

with tarfile.open(ARCHIVE,'w:gz') as tar:
    for rel in files:
        p = PKG / rel
        if p.exists():
            tar.add(p, arcname=f'{PKG.name}/{rel}')
with tarfile.open(ARCHIVE,'r:gz') as tar:
    names = tar.getnames()
for key in [MP4.name, COVER.name, 'youtube-upload-kit.md', 'README.md', 'manifest.json', 'checks/qa_sheet_mp4.png']:
    assert any(n.endswith(key) for n in names), key
print(json.dumps({'mp4':str(MP4),'cover':str(COVER),'archive':str(ARCHIVE),'archive_items':len(names)}, ensure_ascii=False, indent=2))
