from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import json, subprocess, tarfile, shutil

BASE = Path('/home/adl/youtube-lu-ai-channel')
PKG = BASE / 'shorts' / 'misconception-classification-first-20260513'
SLIDES = PKG / 'slides'
CHECKS = PKG / 'checks'
CHECKS.mkdir(parents=True, exist_ok=True)
FONT = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
W, H = 1080, 1920
TARGET = 35.0
SLUG = 'misconception-classification-first'
MP4 = PKG / f'{SLUG}-shorts-35s.mp4'
COVER = PKG / 'cover_misconception_classification_first_v1.png'
ARCHIVE = PKG / f'{SLUG}-upload-kit-20260513.tar.gz'
HANDOUT = PKG / 'misconception-classification-prompt-sheet-v1.md'

palette = {'bg':'#0E2433','cream':'#FFF8EA','ink':'#102033','blue':'#2F6FD6','orange':'#F4A340','green':'#2FAE77','red':'#E4574F','muted':'#607080','purple':'#6C63D9','pink':'#E95D8F'}

def font(size):
    return ImageFont.truetype(FONT, size)

def wrap(draw, text, fnt, maxw):
    out=[]
    for para in text.split('\n'):
        line=''
        for ch in para:
            if draw.textbbox((0,0), line+ch, font=fnt)[2] <= maxw:
                line += ch
            else:
                if line:
                    out.append(line)
                line = ch
        if line:
            out.append(line)
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
    center(d, (130,155,950,286), 'AI 整理學生迷思｜先分類再建議', font(48), 'white', 780)
    center(d, (110,350,970,650), '學生錯答\n不要急著補救', font(86), palette['ink'], 820, 12)
    d.rounded_rectangle([145,700,935,730], radius=10, fill=palette['orange'])
    cards = [
        ('概念', '規則想錯了', palette['green']),
        ('程序', '步驟亂掉了', palette['blue']),
        ('表徵', '圖文公式不一致', palette['orange']),
    ]
    y = 820
    for title, body, color in cards:
        d.rounded_rectangle([130,y,950,y+190], radius=36, fill='white', outline='#E2D6C7', width=4)
        d.rounded_rectangle([155,y+35,315,y+155], radius=26, fill=color)
        center(d, (165,y+42,305,y+148), title, font(48), 'white', 120)
        center(d, (345,y+38,920,y+154), body, font(50), palette['ink'], 520)
        y += 225
    d.rounded_rectangle([130,1608,950,1765], radius=34, fill=palette['ink'])
    center(d, (150,1626,930,1748), '請 AI 先分類，並引用匿名錯答證據', font(42), 'white', 740)
    im.save(COVER)

render_cover()

narration = '''學生錯答丟給 AI，先別急著要建議。
我會先請 AI 做三種分類：概念、程序、表徵。
概念迷思，是學生把規則想錯了，例如把速度變大直接當成受力變大。
程序迷思，是公式可能選對，但代入、單位或正負號開始亂掉。
表徵迷思，是文字、圖、公式對不起來，例如文字說向右，箭頭卻向左。
給 AI 的句子是：請先不要給補救建議，先把匿名錯答分成三類，並引用學生原句做理由。'''
(PKG/'narration_35s.txt').write_text(narration, encoding='utf-8')
mp3 = PKG/'narration_35s_edge_hsiaoyu.mp3'
if (not mp3.exists()) or mp3.stat().st_size < 1000:
    edge = shutil.which('edge-tts') or '/home/adl/.hermes/hermes-agent/venv/bin/edge-tts'
    subprocess.run([edge, '--voice', 'zh-TW-HsiaoYuNeural', '--rate=+6%', '--text', narration, '--write-media', str(mp3)], check=True)

segments = [
    (0.0, 4.5, '學生錯答丟給 AI，先別急著要建議。'),
    (4.5, 9.0, '先請 AI 做三種分類：概念、程序、表徵。'),
    (9.0, 16.0, '概念迷思：學生把規則想錯了，例如把速度變大當成受力變大。'),
    (16.0, 23.0, '程序迷思：公式可能選對，但代入、單位或正負號開始亂掉。'),
    (23.0, 29.5, '表徵迷思：文字、圖、公式對不起來，例如箭頭方向不一致。'),
    (29.5, 35.0, '請 AI 先分類，並引用學生原句做理由。'),
]

def ts(sec, comma=False):
    h=int(sec//3600); m=int((sec%3600)//60); s=int(sec%60); ms=int(round((sec-int(sec))*1000))
    return f'{h:02d}:{m:02d}:{s:02d}{"," if comma else "."}{ms:03d}'
(PKG/'narration_35s_edge_hsiaoyu.vtt').write_text('WEBVTT\n\n'+'\n\n'.join(f'{ts(a)} --> {ts(b)}\n{text}' for a,b,text in segments)+'\n', encoding='utf-8')
(PKG/'narration_35s_edge_hsiaoyu.srt').write_text('\n\n'.join(f'{i}\n{ts(a, True)} --> {ts(b, True)}\n{text}' for i,(a,b,text) in enumerate(segments,1))+'\n', encoding='utf-8')

weights = [6.8,6.9,7.0,7.1,7.2]
scale = TARGET/sum(weights)
concat = PKG / 'slides_35s.ffconcat'
lines = ['ffconcat version 1.0']
for i,w in enumerate(weights,1):
    p = SLIDES / f'slide_{i:02d}.png'
    lines.append(f"file '{p.as_posix()}'")
    lines.append(f'duration {w*scale:.3f}')
lines.append(f"file '{(SLIDES/'slide_05.png').as_posix()}'")
concat.write_text('\n'.join(lines)+'\n', encoding='utf-8')

subprocess.run(['ffmpeg','-y','-f','concat','-safe','0','-i',str(concat),'-i',str(mp3),'-t',f'{TARGET:.3f}','-vf','fps=25,format=yuv420p','-af','apad','-c:v','libx264','-preset','veryfast','-crf','18','-c:a','aac','-b:a','128k',str(MP4)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

for name, tssec in [('frame_early.png',2.0),('frame_mid.png',17.0),('frame_late.png',32.0)]:
    subprocess.run(['ffmpeg','-y','-ss',str(tssec),'-i',str(MP4),'-frames:v','1','-update','1',str(CHECKS/name)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

thumb_w, thumb_h = 360, 640
sheet = Image.new('RGB', (1600,1650), '#1B2635')
d = ImageDraw.Draw(sheet)
d.text((50,35), '先分迷思｜Shorts MP4 QA sheet（cover + early/mid/late）', font=font(38), fill='white')
items = [('cover',COVER),('early 2s',CHECKS/'frame_early.png'),('mid 17s',CHECKS/'frame_mid.png'),('late 32s',CHECKS/'frame_late.png')]
pos = [(80,110),(600,110),(80,870),(600,870)]
for (label,p),(x,y) in zip(items,pos):
    im = Image.open(p).resize((thumb_w,thumb_h))
    sheet.paste(im,(x,y))
    d.text((x,y+thumb_h+16), label, font=font(32), fill='white')
sheet.save(CHECKS/'qa_sheet_mp4.png')

handout = '''# 迷思分類 Prompt 教師小抄 v1

## 一句目標
把學生匿名錯答先分成「概念、程序、表徵」三類，避免 AI 一開始就給出不對症的補救建議。

## 使用時機
- 段考、形成性評量或課堂練習後，老師想快速整理常見錯因。
- 學生錯答數量多，需要先分群再設計補救活動。
- AI Agent 要協助產出課後回饋包，但不能直接替老師判定學生個資或成績。

## 三類迷思速表
| 類型 | 判斷線索 | 老師複查句 |
|---|---|---|
| 概念迷思 | 把規則、定義、因果關係想錯 | 這個錯答反映哪個物理概念被誤解？請引用原句。 |
| 程序迷思 | 公式選擇、代入、單位、正負號或步驟順序出錯 | 從哪一步開始偏離正確流程？下一個檢查點是什麼？ |
| 表徵迷思 | 文字、圖示、公式、表格互相不一致 | 哪兩種表徵對不起來？要怎麼改成一致？ |

## 可複製給 AI 的 prompt
請先不要給補救建議。請閱讀以下匿名錯答，把每一則分成「概念迷思、程序迷思、表徵迷思、暫時無法判斷」四欄；每一則都要引用學生原句或關鍵步驟作為理由。若資料不足，請標示「需老師人工確認」，不要自行補完學生想法。

## 學生錯答整理表
| 匿名錯答編號 | AI 初分類 | 引用證據 | 老師確認 | 下一個補救活動 |
|---|---|---|---|---|
| A | ＿＿＿＿ | ＿＿＿＿ | ＿＿＿＿ | ＿＿＿＿ |
| B | ＿＿＿＿ | ＿＿＿＿ | ＿＿＿＿ | ＿＿＿＿ |
| C | ＿＿＿＿ | ＿＿＿＿ | ＿＿＿＿ | ＿＿＿＿ |

## 老師示範回饋句
你這題不是「不會算」，而是文字敘述和圖上的方向沒有對齊。我們先把圖、文字、公式三個版本改成同一個方向，再重新檢查正負號。

## 公開與隱私提醒
不要把真實姓名、座號、班級、原始手寫影像、學校可識別資訊或未授權學生作品放入公開 AI 工具或公開影片素材。若要對外分享，請改寫成匿名、合成或老師自製的錯答例。
'''
HANDOUT.write_text(handout, encoding='utf-8')

upload = f'''# YouTube Upload Kit｜AI 幫忙整理學生迷思，老師先要求它分類而不是建議

## 建議標題
1. 學生錯答丟給 AI？先分類，不要急著補救
2. AI 整理學生迷思：老師先問這三類
3. 概念、程序、表徵：讓 AI 先當檢驗員

## 主檔案
- Shorts MP4：`{MP4.name}`
- 封面：`{COVER.name}`
- 旁白：`narration_35s_edge_hsiaoyu.mp3`
- 字幕：`narration_35s_edge_hsiaoyu.vtt` / `narration_35s_edge_hsiaoyu.srt`
- QA sheet：`checks/qa_sheet_mp4.png`
- 教師小抄：`{HANDOUT.name}`

## 描述草稿
學生錯答交給 AI 整理時，最怕它一開始就給補救建議。這支 Shorts 示範老師可以先要求 AI 做「概念、程序、表徵」三類分類，並引用匿名錯答證據，再決定下一步補救活動。

#AI教學 #物理教學 #學生迷思 #生成式AI #教師備課 #形成性評量

## 置頂留言
可複製給 AI 的句子：
「請先不要給補救建議。請把匿名錯答分成概念、程序、表徵三類，並引用學生原句做理由。」

## 人工操作卡點
YouTube 上傳、頻道選擇、公開／排程與留言置頂仍需使用者登入 Google / YouTube 後操作。若使用真實學生錯答，需先去識別化並確認可公開範圍。
'''
(PKG/'youtube-upload-kit.md').write_text(upload, encoding='utf-8')

readme = f'''# Shorts｜AI 幫忙整理學生迷思，老師先要求它分類而不是建議

狀態：2026-05-13 每小時雷達已把 storyboard 擴成 35 秒本機 Shorts 草稿、封面、字幕、YouTube upload kit，並新增「迷思分類 Prompt 教師小抄」。  
來源：第三季內容題庫優先題 7「先分迷思」。

## 成果檔案

- Shorts MP4：`{MP4.name}`
- 封面：`{COVER.name}`
- 上傳包：`youtube-upload-kit.md`
- 教師小抄：`{HANDOUT.name}`
- 旁白：`narration_35s_edge_hsiaoyu.mp3`
- 字幕：`narration_35s_edge_hsiaoyu.vtt` / `narration_35s_edge_hsiaoyu.srt`
- QA sheet：`checks/qa_sheet_mp4.png`
- 壓縮包：`{ARCHIVE.name}`

## 圖卡

1. `slides/slide_01.png`｜先分類，再補救
2. `slides/slide_02.png`｜概念迷思：規則想錯
3. `slides/slide_03.png`｜程序迷思：步驟亂掉
4. `slides/slide_04.png`｜表徵迷思：圖文公式不一致
5. `slides/slide_05.png`｜可複製 prompt 與 CTA

## 驗證

- MP4：1080×1920、25fps、H.264 + AAC、35 秒。
- PIL：封面、5 張圖卡與 QA 抽幀皆為 RGB 圖檔。
- 視覺 QA：`checks/qa_sheet_mp4.png` 用於檢查繁中可讀、無 tofu 方塊、無裁切、無重疊與不過度擁擠。
- 教師小抄：`{HANDOUT.name}` 已讀回驗證，含三類迷思速表、可複製 prompt、學生錯答整理表與公開隱私提醒。
- 壓縮包：已用 Python `tarfile` 讀回確認包含 MP4、封面、旁白、字幕、README、manifest、upload kit、教師小抄、slides 與 QA sheet。

## 穩定發布

- 手機索引：`https://addielu-phy.github.io/lu-ai-youtube-assets/mobile-index/index.html`
- 本機 package：`shorts/misconception-classification-first-20260513/`
- GitHub Pages：待本輪同步後回填最新 commit。

## 下一個自動推進

若 YouTube/Google 登入仍未完成：從第三季題庫挑選下一個尚未完成 storyboard／講義延伸。  
若使用者已完成 YouTube/Google 登入：優先上傳已完成的第一季首批 Shorts 或本支第三季 Shorts。
'''
(PKG/'README.md').write_text(readme, encoding='utf-8')

manifest = json.loads((PKG/'manifest.json').read_text(encoding='utf-8'))
manifest.update({
    'status':'35s Shorts MP4 + upload kit + misconception-classification prompt sheet complete',
    'mp4':MP4.name,
    'cover':COVER.name,
    'narration':'narration_35s_edge_hsiaoyu.mp3',
    'subtitles':['narration_35s_edge_hsiaoyu.vtt','narration_35s_edge_hsiaoyu.srt'],
    'upload_kit':'youtube-upload-kit.md',
    'teacher_prompt_sheet':HANDOUT.name,
    'qa_sheet':'checks/qa_sheet_mp4.png',
    'archive':ARCHIVE.name,
    'next_auto_push':'choose the next unfinished season-03 candidate for storyboard or handout extension unless YouTube login is ready for upload',
})
(PKG/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')

members = ['README.md','manifest.json','render_storyboard.py','build_misconception_classification_shorts_package.py','youtube-upload-kit.md',HANDOUT.name,MP4.name,COVER.name,'narration_35s.txt','narration_35s_edge_hsiaoyu.mp3','narration_35s_edge_hsiaoyu.vtt','narration_35s_edge_hsiaoyu.srt','slides_35s.ffconcat','checks/contact_sheet.png','checks/qa_sheet_mp4.png','checks/frame_early.png','checks/frame_mid.png','checks/frame_late.png']
with tarfile.open(ARCHIVE,'w:gz') as tar:
    for rel in members:
        p=PKG/rel
        if p.exists():
            tar.add(p, arcname=f'misconception-classification-first-20260513/{rel}')
    for p in sorted(SLIDES.glob('slide_*.png')):
        tar.add(p, arcname=f'misconception-classification-first-20260513/slides/{p.name}')
with tarfile.open(ARCHIVE,'r:gz') as tar:
    names=tar.getnames()
    required=[MP4.name,COVER.name,'youtube-upload-kit.md',HANDOUT.name,'checks/qa_sheet_mp4.png']
    missing=[r for r in required if not any(n.endswith(r) for n in names)]
    if missing:
        raise SystemExit(f'archive missing: {missing}')
print(json.dumps({'mp4':str(MP4),'cover':str(COVER),'archive':str(ARCHIVE),'members':len(names)}, ensure_ascii=False, indent=2))
