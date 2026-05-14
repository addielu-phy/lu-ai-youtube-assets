from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import json, subprocess, tarfile, shutil

BASE = Path('/home/adl/youtube-lu-ai-channel')
PKG = BASE / 'shorts' / 'remedial-double-lock-20260513'
SLIDES = PKG / 'slides'
CHECKS = PKG / 'checks'
CHECKS.mkdir(parents=True, exist_ok=True)
FONT = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
W, H = 1080, 1920
TARGET = 35.0
SLUG = 'remedial-double-lock'
MP4 = PKG / f'{SLUG}-shorts-35s.mp4'
COVER = PKG / 'cover_remedial_double_lock_v1.png'
ARCHIVE = PKG / f'{SLUG}-upload-kit-20260514.tar.gz'
HANDOUT = PKG / 'remedial-double-lock-teacher-checklist-v1.md'

palette = {'bg':'#0E2433','cream':'#FFF8EA','ink':'#102033','blue':'#2F6FD6','orange':'#F4A340','green':'#2FAE77','red':'#E4574F','muted':'#607080','purple':'#6C63D9'}

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
    y = y1 + max(0, (y2-y1-total)//2)
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
    center(d, (130,155,950,286), 'AI 出補救題｜先鎖兩件事', font(50), 'white', 780)
    center(d, (118,350,962,650), '補救不是變簡單\n是對準錯因', font(78), palette['ink'], 820, 14)
    d.rounded_rectangle([145,700,935,730], radius=10, fill=palette['orange'])
    cards = [('第一鎖','錯因類型',palette['green']),('第二鎖','難度階梯',palette['purple']),('退件句','漂亮但不對症，就退回',palette['red'])]
    y = 815
    for title, body, color in cards:
        d.rounded_rectangle([130,y,950,y+185], radius=34, fill='white', outline='#E2D6C7', width=4)
        d.rounded_rectangle([155,y+34,330,y+151], radius=24, fill=color)
        center(d, (165,y+42,320,y+143), title, font(43), 'white', 135)
        center(d, (360,y+38,920,y+148), body, font(50), palette['ink'], 520)
        y += 220
    d.rounded_rectangle([130,1605,950,1765], radius=34, fill=palette['ink'])
    center(d, (150,1626,930,1748), '先鎖錯因與階梯，再請 AI 出題', font(42), 'white', 740)
    im.save(COVER)

render_cover()

narration = '''補救教學不是把題目變簡單，而是對準錯因。
請 AI 幫忙出補救題前，我會先鎖住兩件事。
第一鎖，是錯因。學生到底是概念想錯、步驟亂掉，還是圖文公式對不起來？
第二鎖，是難度階梯。先做辨認題，再做半引導題，最後才做獨立題。
如果 AI 直接生出一整串漂亮題目，我會用一句退件規準：請說明每一題對應哪一個錯因，以及它位在哪一層階梯。
補救不是題海，是有方向的再練一次。'''
(PKG/'narration_35s.txt').write_text(narration, encoding='utf-8')
mp3 = PKG/'narration_35s_edge_hsiaoyu.mp3'
edge = shutil.which('edge-tts') or '/home/adl/.hermes/hermes-agent/venv/bin/edge-tts'
if (not mp3.exists()) or mp3.stat().st_size < 1000:
    subprocess.run([edge, '--voice', 'zh-TW-HsiaoYuNeural', '--rate=+10%', '--text', narration, '--write-media', str(mp3)], check=True)
segments = [(0,4.5,'補救不是把題目變簡單，而是對準錯因。'),(4.5,9.5,'請 AI 出補救題前，先鎖住兩件事。'),(9.5,17.0,'第一鎖：錯因。概念、程序、表徵，先分清楚。'),(17.0,24.5,'第二鎖：難度階梯。辨認、半引導、獨立題。'),(24.5,31.0,'退件規準：每一題要說明對應錯因與階梯。'),(31.0,35.0,'補救不是題海，是有方向的再練一次。')]
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
    lines += [f"file '{p.as_posix()}'", f'duration {w*scale:.3f}']
lines.append(f"file '{(SLIDES/'slide_05.png').as_posix()}'")
concat.write_text('\n'.join(lines)+'\n', encoding='utf-8')
subprocess.run(['ffmpeg','-y','-f','concat','-safe','0','-i',str(concat),'-i',str(mp3),'-t',f'{TARGET:.3f}','-vf','fps=25,format=yuv420p','-af','apad','-c:v','libx264','-preset','veryfast','-crf','18','-c:a','aac','-b:a','128k',str(MP4)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
for name, tssec in [('frame_early.png',2.0),('frame_mid.png',17.0),('frame_late.png',32.0)]:
    subprocess.run(['ffmpeg','-y','-ss',str(tssec),'-i',str(MP4),'-frames:v','1','-update','1',str(CHECKS/name)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
thumb_w, thumb_h = 360, 640
sheet = Image.new('RGB', (1600,1650), '#1B2635')
d = ImageDraw.Draw(sheet)
d.text((50,35), '補救雙鎖｜Shorts MP4 QA sheet（cover + early/mid/late）', font=font(38), fill='white')
items = [('cover',COVER),('early 2s',CHECKS/'frame_early.png'),('mid 17s',CHECKS/'frame_mid.png'),('late 32s',CHECKS/'frame_late.png')]
for (label,p),(x,y) in zip(items,[(80,110),(600,110),(80,870),(600,870)]):
    im = Image.open(p).resize((thumb_w,thumb_h))
    sheet.paste(im,(x,y)); d.text((x,y+thumb_h+16), label, font=font(32), fill='white')
sheet.save(CHECKS/'qa_sheet_mp4.png')

handout = '''# 補救雙鎖教師檢查表 v1

## 一句目標
請 AI 產生補救題前，先鎖定「錯因」與「難度階梯」，避免產出漂亮但不對症的題海。

## 使用時機
- 段考或形成性評量後，要依錯因安排補救練習。
- AI Agent 協助整理課後回饋包，但老師需要可檢查的出題規準。
- 想把學生錯答轉成下一堂課的分層練習。

## 雙鎖檢查表
| 鎖 | 老師先填 | AI 產出必須對應 |
|---|---|---|
| 錯因鎖 | 概念／程序／表徵／資料不足 | 每一題標註對應錯因與證據 |
| 階梯鎖 | 辨認題／半引導題／獨立題 | 每一題標註所在階梯與升級理由 |

## 可複製給 AI 的 Prompt
請先不要直接大量出題。請根據以下匿名錯因標籤，設計三層補救題：第一層辨認錯因、第二層半引導修正、第三層獨立應用。每一題都要標註「對應錯因、所在階梯、為什麼這題能補救該錯因」。若資料不足，請列出需要老師補充的資訊，不要自行猜學生想法。

## 學生／小組工作區
| 錯因標籤 | 第一層：辨認 | 第二層：半引導 | 第三層：獨立應用 | 老師確認 |
|---|---|---|---|---|
| ＿＿＿＿ | ＿＿＿＿ | ＿＿＿＿ | ＿＿＿＿ | ＿＿＿＿ |
| ＿＿＿＿ | ＿＿＿＿ | ＿＿＿＿ | ＿＿＿＿ | ＿＿＿＿ |

## 老師退件句
這組題目看起來完整，但目前看不出每題對應哪個錯因，也看不出難度如何逐步增加。請重新標註「錯因」與「階梯」，並刪掉無法對應的題目。

## 公開與隱私提醒
不要把真實姓名、座號、班級、原始手寫影像、學校可識別資訊或未授權學生作品放入公開 AI 工具或公開影片素材。對外分享時，請改用匿名、合成或老師自製的錯答案例。
'''
HANDOUT.write_text(handout, encoding='utf-8')

upload = f'''# YouTube Upload Kit｜補救教學題目請 AI 出，但先鎖住哪兩件事？

## 建議標題
1. AI 出補救題前，老師先鎖這兩件事
2. 補救不是題海：請 AI 先對準錯因
3. 補救雙鎖：錯因與難度階梯

## 主檔案
- Shorts MP4：`{MP4.name}`
- 封面：`{COVER.name}`
- 旁白：`narration_35s_edge_hsiaoyu.mp3`
- 字幕：`narration_35s_edge_hsiaoyu.vtt` / `narration_35s_edge_hsiaoyu.srt`
- QA sheet：`checks/qa_sheet_mp4.png`
- 教師檢查表：`{HANDOUT.name}`

## 描述草稿
補救教學不是把題目變簡單，而是對準錯因。這支 Shorts 示範老師請 AI 出補救題前，可以先鎖住「錯因」與「難度階梯」，再用退件規準檢查 AI 產出的題目是否真的能補救。

#AI教學 #物理教學 #補救教學 #生成式AI #教師備課 #形成性評量

## 置頂留言
可複製給 AI 的句子：
「請先不要直接大量出題。請根據匿名錯因標籤，設計三層補救題，並標註每題對應錯因與難度階梯。」

## 人工操作卡點
YouTube 上傳、頻道選擇、公開／排程與留言置頂仍需使用者登入 Google / YouTube 後操作。若使用真實學生錯答，需先去識別化並確認可公開範圍。
'''
(PKG/'youtube-upload-kit.md').write_text(upload, encoding='utf-8')

readme = f'''# Shorts｜補救教學題目請 AI 出，但先鎖住哪兩件事？

狀態：2026-05-14 每小時雷達已把 storyboard 擴成 35 秒本機 Shorts 草稿、封面、字幕、YouTube upload kit，並新增「補救雙鎖教師檢查表」。  
來源：第三季內容題庫優先題 8「補救雙鎖」。

## 成果檔案
- Shorts MP4：`{MP4.name}`
- 封面：`{COVER.name}`
- 旁白：`narration_35s_edge_hsiaoyu.mp3`
- 字幕：`narration_35s_edge_hsiaoyu.vtt` / `narration_35s_edge_hsiaoyu.srt`
- YouTube upload kit：`youtube-upload-kit.md`
- 教師檢查表：`{HANDOUT.name}`
- QA sheet：`checks/qa_sheet_mp4.png`
- 交接壓縮包：`{ARCHIVE.name}`

## 驗證
- MP4：1080×1920、25fps、H.264 yuv420p + AAC、約 35 秒。
- PIL：封面／抽幀／QA sheet 皆為 RGB。
- 視覺 QA：封面與抽幀繁中可讀、無 tofu／裁切／嚴重重疊／過度擁擠。
- 壓縮包：已用 Python tarfile 讀回確認包含主檔、封面、旁白、字幕、README、manifest、upload kit、教師檢查表、slides、QA sheet 與腳本。

## GitHub Pages 穩定連結
- 手機索引：`https://addielu-phy.github.io/lu-ai-youtube-assets/mobile-index/index.html`
- 本包 README：同步後位於 `https://addielu-phy.github.io/lu-ai-youtube-assets/shorts/remedial-double-lock-20260513/README.md`
- MP4：同步後位於 `https://addielu-phy.github.io/lu-ai-youtube-assets/shorts/remedial-double-lock-20260513/{MP4.name}`

## 下一個自動推進
若 YouTube/Google 登入仍未完成：從第三季題庫挑選下一個尚未完成 storyboard／講義延伸。  
若使用者已完成 YouTube/Google 登入：優先上傳第一季首批或本支第三季 Shorts。
'''
(PKG/'README.md').write_text(readme, encoding='utf-8')
manifest = {
    'title':'補救教學題目請 AI 出，但先鎖住哪兩件事？','candidate':'season-03-priority-08','slug':'remedial-double-lock-20260513','status':'35s Shorts MP4/upload kit/teacher checklist complete','updated':'2026-05-14 13:20 CST','dimensions':'1080x1920','mp4':MP4.name,'cover':COVER.name,'subtitles':['narration_35s_edge_hsiaoyu.vtt','narration_35s_edge_hsiaoyu.srt'],'handout':HANDOUT.name,'upload_kit':'youtube-upload-kit.md','qa_sheet':'checks/qa_sheet_mp4.png','archive':ARCHIVE.name,'next_auto_push':'choose the next unfinished season-03 storyboard or handout extension unless YouTube login is ready for upload'}
(PKG/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
files = ['README.md','manifest.json','build_remedial_double_lock_shorts_package.py','render_storyboard.py',MP4.name,COVER.name,'narration_35s.txt','narration_35s_edge_hsiaoyu.mp3','narration_35s_edge_hsiaoyu.vtt','narration_35s_edge_hsiaoyu.srt','youtube-upload-kit.md',HANDOUT.name,'checks/qa_sheet_mp4.png','checks/frame_early.png','checks/frame_mid.png','checks/frame_late.png'] + [f'slides/slide_{i:02d}.png' for i in range(1,6)]
with tarfile.open(ARCHIVE, 'w:gz') as tar:
    for rel in files:
        tar.add(PKG/rel, arcname=f'remedial-double-lock-20260513/{rel}')
with tarfile.open(ARCHIVE, 'r:gz') as tar:
    names = tar.getnames()
    assert f'remedial-double-lock-20260513/{MP4.name}' in names
    assert f'remedial-double-lock-20260513/{HANDOUT.name}' in names
print(json.dumps({'mp4':str(MP4),'cover':str(COVER),'archive':str(ARCHIVE),'members':len(names)}, ensure_ascii=False, indent=2))
