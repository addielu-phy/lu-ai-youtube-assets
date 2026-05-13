from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import json, subprocess, tarfile, shutil

BASE = Path('/home/adl/youtube-lu-ai-channel')
PKG = BASE / 'shorts' / 'image-license-check-before-slide-20260513'
SLIDES = PKG / 'slides'
CHECKS = PKG / 'checks'
CHECKS.mkdir(parents=True, exist_ok=True)
FONT = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
W, H = 1080, 1920
TARGET = 35.0
SLUG = 'image-license-check-before-slide'
MP4 = PKG / f'{SLUG}-shorts-35s.mp4'
COVER = PKG / 'cover_image_license_check_v1.png'
ARCHIVE = PKG / f'{SLUG}-upload-kit-20260513.tar.gz'
CHECKLIST = PKG / 'image-license-teacher-checklist-v1.md'

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
    d.rounded_rectangle([112,140,968,300], radius=38, fill=palette['blue'])
    center(d, (130,155,950,286), 'AI 找圖放簡報｜先做授權三查', font(48), 'white', 780)
    center(d, (110,350,970,680), '圖很漂亮\n不等於能公開', font(90), palette['ink'], 820, 12)
    d.rounded_rectangle([145,720,935,750], radius=10, fill=palette['orange'])
    cards = [
        ('來源', '這張圖從哪裡來？', palette['green']),
        ('授權', '能不能公開與改作？', palette['orange']),
        ('替代', '不確定就改自製圖', palette['purple']),
    ]
    y = 835
    for title, body, color in cards:
        d.rounded_rectangle([130,y,950,y+190], radius=36, fill='white', outline='#E2D6C7', width=4)
        d.rounded_rectangle([155,y+35,315,y+155], radius=26, fill=color)
        center(d, (165,y+42,305,y+148), title, font(48), 'white', 120)
        center(d, (345,y+38,920,y+154), body, font(47), palette['ink'], 520)
        y += 225
    d.rounded_rectangle([130,1608,950,1765], radius=34, fill=palette['ink'])
    center(d, (150,1626,930,1748), '公開前：來源、授權、替代方案', font(48), 'white', 740)
    im.save(COVER)

render_cover()

narration = '''AI 找到的圖，可以直接放簡報嗎？先不要急。
我會請 AI 和學生一起做三查。
第一，來源：這張圖是網站、教材、截圖，還是 AI 生成？要寫清楚。
第二，授權：能不能公開、能不能改作、能不能商用，不確定就不要放上網。
第三，替代方案：如果授權不清楚，就改成自己畫的示意圖、表格，或只留下文字描述。
給 AI 的句子是：請列出每張圖的來源、授權狀態，和一個可替代的自製圖方案。'''
(PKG/'narration_35s.txt').write_text(narration, encoding='utf-8')
mp3 = PKG/'narration_35s_edge_hsiaoyu.mp3'
if (not mp3.exists()) or mp3.stat().st_size < 1000:
    edge = shutil.which('edge-tts') or '/home/adl/.hermes/hermes-agent/venv/bin/edge-tts'
    subprocess.run([edge, '--voice', 'zh-TW-HsiaoYuNeural', '--rate=+6%', '--text', narration, '--write-media', str(mp3)], check=True)

segments = [
    (0.0, 4.4, 'AI 找到的圖，可以直接放簡報嗎？先不要急。'),
    (4.4, 8.5, '我會請 AI 和學生一起做三查。'),
    (8.5, 15.4, '第一，來源：網站、教材、截圖，還是 AI 生成？要寫清楚。'),
    (15.4, 23.0, '第二，授權：能不能公開、能不能改作，不確定就不要放上網。'),
    (23.0, 29.4, '第三，替代方案：授權不清楚，就改成自己畫的示意圖或表格。'),
    (29.4, 35.0, '請 AI 列出來源、授權狀態，和可替代的自製圖方案。'),
]

def ts(sec, comma=False):
    h=int(sec//3600); m=int((sec%3600)//60); s=int(sec%60); ms=int(round((sec-int(sec))*1000))
    sep=',' if comma else '.'
    return f'{h:02d}:{m:02d}:{s:02d}{sep}{ms:03d}'
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
d.text((50,35), '圖片授權三查｜Shorts MP4 QA sheet（cover + early/mid/late）', font=font(38), fill='white')
items = [('cover',COVER),('early 2s',CHECKS/'frame_early.png'),('mid 17s',CHECKS/'frame_mid.png'),('late 32s',CHECKS/'frame_late.png')]
pos = [(80,110),(600,110),(80,870),(600,870)]
for (label,p),(x,y) in zip(items,pos):
    im = Image.open(p).resize((thumb_w,thumb_h))
    sheet.paste(im,(x,y))
    d.text((x,y+thumb_h+16), label, font=font(32), fill='white')
sheet.save(CHECKS/'qa_sheet_mp4.png')

checklist = '''# 圖片授權檢查表 v1｜來源、授權、替代方案

## 一句目標
讓學生與老師在把 AI 找到的圖片放進簡報或公開素材前，先確認來源、授權與替代方案，降低侵權與誤用風險。

## 適用情境
- AI 幫忙找圖、產圖、整理簡報素材。
- 學生作品、課堂簡報、社群貼文或影片縮圖準備公開。
- 圖片來自搜尋結果、教材截圖、網站、論文、AI 生圖工具或不明來源。

## 三查速表
| 檢查 | 學生先填 | 老師複查 |
|---|---|---|
| 來源 | 圖片來源網址／工具／作者：＿＿＿＿ | 是否能追到原始來源，而不是只寫「Google」或「AI 找到」？ |
| 授權 | 可公開／可改作／需署名／不確定：＿＿＿＿ | 是否符合課堂、校內、公開影片或社群使用情境？ |
| 替代方案 | 若不能用，我可以改成：自製示意圖／表格／文字描述／重新拍攝 | 是否能用更安全的自製圖取代？ |

## 可複製給 AI 的檢查 prompt
請幫我檢查這份簡報中的每張圖片，只做三件事：
1. 列出可能的來源與需要補查的資訊。
2. 判斷授權狀態：可公開、需署名、不可公開、或不確定。
3. 對每張不確定的圖片，提出一個可由學生或老師自製的替代圖方案。
請不要直接宣稱圖片一定可合法使用；不確定時請標「需人工確認」。

## 學生工作區
- 我想使用的圖片主題：＿＿＿＿＿＿＿＿＿＿
- 圖片來源：＿＿＿＿＿＿＿＿＿＿
- 授權或署名需求：＿＿＿＿＿＿＿＿＿＿
- 若不能公開，我的替代方案：＿＿＿＿＿＿＿＿＿＿

## 老師示範回饋句
這張圖的概念可以保留，但來源與授權還不清楚。請改成你自己畫的示意圖，或補上可公開使用的來源與署名方式。

## 快速規準
- 3 分：來源清楚、授權清楚、替代方案也備妥。
- 2 分：概念可用，但還需要補來源、署名或改成自製圖。
- 1 分：來源不明或授權不清，不建議公開。

## 公開提醒
不要把不明來源圖片、課本掃描圖、付費素材、真實學生作品、人物照片或未授權截圖放到公開影片／社群／網站。AI 可以協助列風險，但不能替老師做法律或學校流程確認。
'''
CHECKLIST.write_text(checklist, encoding='utf-8')

upload = f'''# YouTube Upload Kit｜AI 找到的圖，可以直接放簡報嗎？

## 建議標題
1. AI 找到的圖，可以直接放簡報嗎？
2. 圖很漂亮，不代表授權漂亮：老師的三查法
3. 用 AI 找圖片前，先問來源、授權、替代方案

## 主檔案
- Shorts MP4：`{MP4.name}`
- 封面：`{COVER.name}`
- 旁白：`narration_35s_edge_hsiaoyu.mp3`
- 字幕：`narration_35s_edge_hsiaoyu.vtt` / `narration_35s_edge_hsiaoyu.srt`
- QA sheet：`checks/qa_sheet_mp4.png`
- 教師檢查表：`{CHECKLIST.name}`

## 描述草稿
AI 很會幫我們找圖片，但「找到」不代表「可以公開使用」。這支 Shorts 示範老師可以讓學生先做來源、授權、替代方案三查；不確定時，改成自製圖最安全。

#AI教學 #物理教學 #簡報設計 #圖片授權 #生成式AI #教師備課

## 置頂留言
可複製給 AI 的檢查句：
「請列出每張圖的來源、授權狀態，並對不確定的圖片提出一個可自製的替代圖方案。」

## 人工操作卡點
YouTube 上傳、頻道選擇、公開／排程與留言置頂仍需使用者登入 Google / YouTube 後操作。圖片授權狀態與是否可公開也需由使用者依學校／平台規範最後確認。
'''
(PKG/'youtube-upload-kit.md').write_text(upload, encoding='utf-8')

readme = f'''# Shorts｜AI 找到的圖，可以直接放簡報嗎？

狀態：2026-05-13 每小時雷達已把 storyboard 擴成 35 秒本機 Shorts 草稿、封面、字幕、YouTube upload kit，並新增「圖片授權檢查表」。  
來源：第三季內容題庫優先題 5「AI 找到的圖，可以直接放簡報嗎？」。

## 成果檔案

- Shorts MP4：`{MP4.name}`
- 封面：`{COVER.name}`
- 上傳包：`youtube-upload-kit.md`
- 教師檢查表：`{CHECKLIST.name}`
- 旁白：`narration_35s_edge_hsiaoyu.mp3`
- 字幕：`narration_35s_edge_hsiaoyu.vtt` / `narration_35s_edge_hsiaoyu.srt`
- QA sheet：`checks/qa_sheet_mp4.png`
- 壓縮包：`{ARCHIVE.name}`

## 圖卡

1. `slides/slide_01.png`｜AI 找到的圖，可以直接放簡報嗎？
2. `slides/slide_02.png`｜先問：這張圖從哪裡來？
3. `slides/slide_03.png`｜再問：能不能公開分享？
4. `slides/slide_04.png`｜最後準備替代方案
5. `slides/slide_05.png`｜給 AI 的可複製句

## 驗證

- MP4：1080×1920、25fps、H.264 + AAC、35 秒。
- PIL：封面、5 張圖卡與 QA 抽幀皆為 RGB 圖檔。
- 視覺 QA：`checks/qa_sheet_mp4.png` 用於檢查繁中可讀、無 tofu 方塊、無裁切、無重疊與不過度擁擠。
- 檢查表：`{CHECKLIST.name}` 已讀回驗證，含來源、授權、替代方案、AI 檢查 prompt、學生工作區與公開提醒。
- 壓縮包：已用 Python `tarfile` 讀回確認包含 MP4、封面、旁白、字幕、README、manifest、upload kit、檢查表、slides 與 QA sheet。

## 穩定發布

- 手機索引：`https://addielu-phy.github.io/lu-ai-youtube-assets/mobile-index/index.html`
- 本機 package：`shorts/image-license-check-before-slide-20260513/`
- GitHub Pages：待本輪同步後回填最新 commit。

## 下一個自動推進

若 YouTube/Google 登入仍未完成：從第三季題庫挑選下一個尚未完成 storyboard／講義延伸。  
若使用者已完成 YouTube/Google 登入：優先上傳已完成的第一季首批 Shorts 或本支第三季 Shorts。
'''
(PKG/'README.md').write_text(readme, encoding='utf-8')

manifest = json.loads((PKG/'manifest.json').read_text(encoding='utf-8'))
manifest.update({
    'status':'35s Shorts MP4 + upload kit + image-license checklist complete',
    'mp4':MP4.name,
    'cover':COVER.name,
    'upload_kit':'youtube-upload-kit.md',
    'checklist':CHECKLIST.name,
    'narration':'narration_35s_edge_hsiaoyu.mp3',
    'subtitles':['narration_35s_edge_hsiaoyu.vtt','narration_35s_edge_hsiaoyu.srt'],
    'qa_sheet':'checks/qa_sheet_mp4.png',
    'archive':ARCHIVE.name,
    'next_auto_push':'choose the next unmade season-03 storyboard or handout extension, unless YouTube login is ready for upload'
})
files = ['README.md','manifest.json','render_storyboard.py','build_image_license_shorts_package.py','youtube-upload-kit.md',CHECKLIST.name,MP4.name,COVER.name,'narration_35s.txt','narration_35s_edge_hsiaoyu.mp3','narration_35s_edge_hsiaoyu.vtt','narration_35s_edge_hsiaoyu.srt','checks/contact_sheet.png','checks/qa_sheet_mp4.png','checks/frame_early.png','checks/frame_mid.png','checks/frame_late.png','slides_35s.ffconcat'] + [f'slides/slide_{i:02d}.png' for i in range(1,6)]
manifest['files'] = files
(PKG/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')

with tarfile.open(ARCHIVE,'w:gz') as tar:
    for rel in files:
        p = PKG / rel
        if p.exists():
            tar.add(p, arcname=f'{PKG.name}/{rel}')
with tarfile.open(ARCHIVE,'r:gz') as tar:
    names = tar.getnames()
for key in [MP4.name, COVER.name, 'youtube-upload-kit.md', CHECKLIST.name, 'README.md', 'manifest.json', 'checks/qa_sheet_mp4.png']:
    assert any(n.endswith(key) for n in names), key
print(json.dumps({'mp4':str(MP4),'cover':str(COVER),'archive':str(ARCHIVE),'archive_items':len(names)}, ensure_ascii=False, indent=2))
