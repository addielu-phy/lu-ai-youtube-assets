from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import json, subprocess, tarfile, re, textwrap, shutil

BASE = Path('/home/adl/youtube-lu-ai-channel')
PKG = BASE / 'shorts' / 'public-before-share-check-20260513'
SLIDES = PKG / 'slides'
CHECKS = PKG / 'checks'
CHECKS.mkdir(parents=True, exist_ok=True)
FONT = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
W, H = 1080, 1920
TARGET = 35.0
SLUG = 'public-before-share-check'
MP4 = PKG / f'{SLUG}-shorts-35s.mp4'
COVER = PKG / 'cover_public_before_share_check_v1.png'
ARCHIVE = PKG / f'{SLUG}-upload-kit-20260513.tar.gz'
CHECKLIST = PKG / 'student-work-public-checklist-v1.md'

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
    center(d, (130,155,950,286), '學生作品公開前｜三道檢查', font(50), 'white', 780)
    center(d, (110,355,970,690), '上網前\n先跑三查', font(94), palette['ink'], 820, 12)
    d.rounded_rectangle([145,730,935,760], radius=10, fill=palette['orange'])
    cards = [
        ('匿名', '拿掉姓名、臉、班級線索', palette['green']),
        ('授權', '圖片與資料可不可以公開', palette['orange']),
        ('標註', 'AI 幫了哪一步要說清楚', palette['purple']),
    ]
    y = 850
    for title, body, color in cards:
        d.rounded_rectangle([130,y,950,y+192], radius=36, fill='white', outline='#E2D6C7', width=4)
        d.rounded_rectangle([155,y+35,315,y+155], radius=26, fill=color)
        center(d, (165,y+42,305,y+148), title, font(48), 'white', 120)
        center(d, (345,y+38,920,y+154), body, font(46), palette['ink'], 520)
        y += 230
    d.rounded_rectangle([130,1618,950,1765], radius=34, fill=palette['ink'])
    center(d, (150,1636,930,1748), '最後仍由老師按下公開鍵', font(50), 'white', 740)
    im.save(COVER)

render_cover()

narration = '''能不能公開，不是看作品漂不漂亮。
學生作品放上網前，我會請 AI 先幫忙做三件事。
第一，匿名化：有姓名、臉、班級、學號，先拿掉。
第二，授權來源：圖片、音樂、資料，不是 AI 找到就能公開。
第三，AI 標註：哪裡由 AI 協助，哪裡由學生判斷，要說清楚。
最後一句最重要：AI 可以協助檢查，但公開責任由老師把關。'''
(PKG/'narration_35s.txt').write_text(narration, encoding='utf-8')
mp3 = PKG/'narration_35s_edge_hsiaoyu.mp3'
# Generate TTS if missing or tiny. Keep deterministic files otherwise.
if (not mp3.exists()) or mp3.stat().st_size < 1000:
    edge = shutil.which('edge-tts') or '/home/adl/.hermes/hermes-agent/venv/bin/edge-tts'
    subprocess.run([edge, '--voice', 'zh-TW-HsiaoYuNeural', '--rate=-6%', '--text', narration, '--write-media', str(mp3)], check=True)

# Coarse subtitles aligned to 35s.
segments = [
    (0.0, 4.4, '能不能公開，不是看作品漂不漂亮。'),
    (4.4, 9.5, '學生作品放上網前，請 AI 先幫忙做三件事。'),
    (9.5, 15.3, '第一，匿名化：姓名、臉、班級、學號，先拿掉。'),
    (15.3, 21.5, '第二，授權來源：圖片、音樂、資料，不是 AI 找到就能公開。'),
    (21.5, 28.0, '第三，AI 標註：哪裡由 AI 協助，哪裡由學生判斷，要說清楚。'),
    (28.0, 35.0, 'AI 可以協助檢查，但公開責任由老師把關。'),
]

def ts(sec, comma=False):
    h=int(sec//3600); m=int((sec%3600)//60); s=int(sec%60); ms=int(round((sec-int(sec))*1000))
    sep=',' if comma else '.'
    return f'{h:02d}:{m:02d}:{s:02d}{sep}{ms:03d}'
(PKG/'narration_35s_edge_hsiaoyu.vtt').write_text('WEBVTT\n\n'+'\n\n'.join(f'{ts(a)} --> {ts(b)}\n{text}' for a,b,text in segments)+'\n', encoding='utf-8')
(PKG/'narration_35s_edge_hsiaoyu.srt').write_text('\n\n'.join(f'{i}\n{ts(a, True)} --> {ts(b, True)}\n{text}' for i,(a,b,text) in enumerate(segments,1))+'\n', encoding='utf-8')

weights = [6.6,7.0,7.0,7.2,7.2]
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
d.text((50,35), '公開前三查｜Shorts MP4 QA sheet（cover + early/mid/late）', font=font(38), fill='white')
items = [('cover',COVER),('early 2s',CHECKS/'frame_early.png'),('mid 17s',CHECKS/'frame_mid.png'),('late 32s',CHECKS/'frame_late.png')]
pos = [(80,110),(600,110),(80,870),(600,870)]
for (label,p),(x,y) in zip(items,pos):
    im = Image.open(p).resize((thumb_w,thumb_h))
    sheet.paste(im,(x,y))
    d.text((x,y+thumb_h+16), label, font=font(32), fill='white')
sheet.save(CHECKS/'qa_sheet_mp4.png')

checklist = '''# 學生作品公開檢查表 v1｜匿名、授權、AI 標註

## 一句目標
讓學生作品上網前，先用三道低摩擦檢查降低個資、授權與 AI 使用標示風險。

## 適用情境
- 課堂成果要放到班級網站、社群貼文、簡報、校內展覽或對外公開頁面。
- 學生有使用 AI 產生文字、圖片、摘要、翻譯、修稿或版面建議。
- 老師想讓學生保留作品亮點，但不要把身分與未授權素材一起公開。

## 三查速表
| 檢查 | 學生先勾 | 老師複查 |
|---|---|---|
| 匿名化 | 我已移除姓名、學號、臉部、班級座號、可定位的照片背景。 | 是否仍能從截圖、檔名、浮水印或留言推回身分？ |
| 授權來源 | 我列出圖片、音樂、資料、AI 產物與引用來源。 | 是否有不可公開的課本截圖、商用圖、他人照片或未註明資料？ |
| AI 標註 | 我寫清楚 AI 協助的是草稿、修句、翻譯、圖片或檢查。 | 是否誤導讀者以為全部是學生獨立完成，或把 AI 輸出當成事實？ |

## 可複製給學生的 AI 檢查 prompt
請幫我檢查這份準備公開的學生作品說明，只檢查三件事：
1. 是否還有姓名、臉、班級、學號、地點等身分線索？
2. 是否有圖片、資料、音樂或截圖需要授權或補來源？
3. 是否需要補一句 AI 使用標註？
請用「可公開 / 需修改 / 不建議公開」三欄列出理由，不要替我做最終公開決定。

## 學生工作區
- 我想公開的作品主題：＿＿＿＿＿＿＿＿＿＿
- 可能暴露身分的地方：＿＿＿＿＿＿＿＿＿＿
- 我使用的外部素材來源：＿＿＿＿＿＿＿＿＿＿
- AI 協助我的地方：＿＿＿＿＿＿＿＿＿＿
- 我準備放在作品下方的 AI 標註句：＿＿＿＿＿＿＿＿＿＿

## 老師示範標註句
本作品由學生完成主要想法與解釋，AI 協助進行語句修整與公開前風險檢查；公開前已由教師確認匿名化與授權來源。

## 快速評分規準
- 3 分：匿名、授權、AI 標註都清楚，可進入公開審核。
- 2 分：有一項需要補充或改寫，修正後再公開。
- 1 分：含個資、未授權素材或 AI 角色不清楚，不建議公開。

## 公開提醒
不要公開真實學生個資、未取得同意的照片、可辨識家庭或校外地點、未授權素材，或任何可能讓學生被搜尋到的私人資訊。AI 只能協助找風險，最後公開責任仍由老師與學校流程把關。
'''
CHECKLIST.write_text(checklist, encoding='utf-8')

upload = f'''# YouTube Upload Kit｜學生作品要放上網前，AI 幫忙檢查哪三件事？

## 建議標題
1. 學生作品上網前，先用 AI 跑三道檢查
2. 公開學生作品前，老師不能跳過這三件事
3. AI 幫忙檢查作品公開風險：匿名、授權、標註

## 主檔案
- Shorts MP4：`{MP4.name}`
- 封面：`{COVER.name}`
- 旁白：`narration_35s_edge_hsiaoyu.mp3`
- 字幕：`narration_35s_edge_hsiaoyu.vtt` / `narration_35s_edge_hsiaoyu.srt`
- QA sheet：`checks/qa_sheet_mp4.png`
- 教師／學生檢查表：`{CHECKLIST.name}`

## 描述草稿
學生作品公開前，讓 AI 協助跑三道檢查：匿名化、授權來源、AI 使用標註。但最後要不要公開，仍由老師依學校流程與學生權益把關。

#AI教學 #物理教學 #學生作品 #生成式AI #教師備課 #AI素養

## 置頂留言
可複製給學生的公開前檢查句：
「請用匿名化、授權來源、AI 標註三欄幫我檢查這份作品；只列風險，不要替我決定公開。」

## 人工操作卡點
YouTube 上傳、頻道選擇、公開／排程與留言置頂仍需使用者登入 Google / YouTube 後操作。
'''
(PKG/'youtube-upload-kit.md').write_text(upload, encoding='utf-8')

readme = f'''# Shorts｜學生作品要放上網前，AI 幫忙檢查哪三件事？

狀態：2026-05-13 每小時雷達已把 storyboard 擴成 35 秒本機 Shorts 草稿、封面、字幕、YouTube upload kit，並新增「學生作品公開檢查表」。  
來源：第三季內容題庫優先題 4「公開前三查」。

## 成果檔案

- Shorts MP4：`{MP4.name}`
- 封面：`{COVER.name}`
- 上傳包：`youtube-upload-kit.md`
- 教師／學生檢查表：`{CHECKLIST.name}`
- 旁白：`narration_35s_edge_hsiaoyu.mp3`
- 字幕：`narration_35s_edge_hsiaoyu.vtt` / `narration_35s_edge_hsiaoyu.srt`
- QA sheet：`checks/qa_sheet_mp4.png`
- 壓縮包：`{ARCHIVE.name}`

## 圖卡

1. `slides/slide_01.png`｜公開前三查：匿名、授權、AI 標註
2. `slides/slide_02.png`｜匿名化：拿掉身分線索
3. `slides/slide_03.png`｜授權來源：AI 找到不等於可以公開
4. `slides/slide_04.png`｜AI 標註：說清楚協助範圍與責任
5. `slides/slide_05.png`｜公開閘門與 CTA

## 驗證

- MP4：1080×1920、25fps、H.264 + AAC、35 秒。
- PIL：封面、5 張圖卡與 QA 抽幀皆為 RGB 圖檔。
- 視覺 QA：`checks/qa_sheet_mp4.png` 已用於檢查繁中可讀、無 tofu 方塊、無裁切、無重疊與不過度擁擠。
- 檢查表：`{CHECKLIST.name}` 已讀回驗證，含匿名化、授權來源、AI 標註、可複製 prompt、學生工作區與公開提醒。
- 壓縮包：已用 Python `tarfile` 讀回確認包含 MP4、封面、旁白、字幕、README、manifest、upload kit、檢查表、slides 與 QA sheet。

## 穩定發布

- 手機索引：`https://addielu-phy.github.io/lu-ai-youtube-assets/mobile-index/index.html`
- 本機 package：`shorts/public-before-share-check-20260513/`
- GitHub Pages content commit：`3061aca`；metadata cleanup commit：`cbdc6a2` 已 live 驗證（本 README 若由後續 metadata-only commit 送出，仍以最新 GitHub Pages 頁面為準）。

## 下一個自動推進

若 YouTube/Google 登入仍未完成：從第三季題庫挑選下一個尚未完成的 storyboard／講義延伸。  
若使用者已完成 YouTube/Google 登入：優先上傳已完成的第一季首批 Shorts 或本支第三季 Shorts。
'''
(PKG/'README.md').write_text(readme, encoding='utf-8')

manifest = json.loads((PKG/'manifest.json').read_text(encoding='utf-8'))
manifest.update({
    'status':'35s Shorts MP4 + upload kit + public checklist complete',
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
files = ['README.md','manifest.json','render_storyboard.py','build_public_before_share_shorts_package.py','youtube-upload-kit.md',CHECKLIST.name,MP4.name,COVER.name,'narration_35s.txt','narration_35s_edge_hsiaoyu.mp3','narration_35s_edge_hsiaoyu.vtt','narration_35s_edge_hsiaoyu.srt','checks/contact_sheet.png','checks/qa_sheet_mp4.png','checks/frame_early.png','checks/frame_mid.png','checks/frame_late.png','slides_35s.ffconcat'] + [f'slides/slide_{i:02d}.png' for i in range(1,6)]
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
