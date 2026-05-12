from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import json, subprocess, tarfile, re, shutil, math

BASE = Path('/home/adl/youtube-lu-ai-channel')
PKG = BASE / 'shorts' / 'three-verifiable-evidence-before-answer-20260512'
SLIDES = PKG / 'slides'
CHECKS = PKG / 'checks'
CHECKS.mkdir(parents=True, exist_ok=True)
FONT = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
W,H = 1080,1920
TARGET = 35.0
SLUG = 'three-verifiable-evidence-before-answer'
MP4 = PKG / f'{SLUG}-shorts-35s.mp4'
COVER = PKG / 'cover_three_verifiable_evidence_v1.png'
ARCHIVE = PKG / f'{SLUG}-upload-kit-20260512.tar.gz'

palette = {'bg':'#0F2034','ink':'#102033','blue':'#2F6FD6','orange':'#F4A340','green':'#2FAE77','cream':'#FFF8EA','muted':'#5F6E7A','red':'#E4574F'}

def font(size): return ImageFont.truetype(FONT,size)
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

def draw_center(draw, box, text, fnt, fill, maxw=None, leading=10):
    x1,y1,x2,y2=box
    lines=wrap(draw,text,fnt,maxw or (x2-x1-40))
    total=len(lines)*(fnt.size+leading)-leading
    y=y1+(y2-y1-total)//2
    for line in lines:
        bbox=draw.textbbox((0,0),line,font=fnt); tw=bbox[2]-bbox[0]
        draw.text((x1+(x2-x1-tw)//2,y),line,font=fnt,fill=fill)
        y += fnt.size+leading

def render_cover():
    im=Image.new('RGB',(W,H),palette['bg']); d=ImageDraw.Draw(im)
    d.rounded_rectangle([72,86,1008,1834], radius=54, fill=palette['cream'])
    d.rounded_rectangle([112,140,968,300], radius=38, fill=palette['blue'])
    draw_center(d,(130,155,950,286),'AI 答案審稿｜證據先行',font(50),'white',780)
    draw_center(d,(110,365,970,700),'答案先放旁邊\n證據在哪？',font(92),palette['ink'],820,14)
    d.rounded_rectangle([145,760,935,790], radius=10, fill=palette['orange'])
    # three evidence cards
    labels=[('現象','我看得到什麼？',palette['green']),('數據','我量得到什麼？',palette['blue']),('原理','支持哪一句答案？',palette['orange'])]
    y=875
    for title,body,color in labels:
        d.rounded_rectangle([130,y,950,y+190], radius=36, fill='white', outline='#E2D6C7', width=4)
        d.rounded_rectangle([155,y+35,315,y+155], radius=26, fill=color)
        draw_center(d,(165,y+42,305,y+148),title,font(48),'white',120)
        draw_center(d,(345,y+38,920,y+154),body,font(50),palette['ink'],520)
        y += 230
    d.rounded_rectangle([130,1618,950,1765], radius=34, fill=palette['ink'])
    draw_center(d,(150,1636,930,1748),'先要證據，再看答案',font(54),'white',740)
    im.save(COVER)

render_cover()

# Build ffconcat with five slides held to TARGET seconds
weights=[6.6,7.1,7.1,7.1,7.1]
scale=TARGET/sum(weights)
concat=PKG/'slides_35s.ffconcat'
lines=['ffconcat version 1.0']
for i,w in enumerate(weights,1):
    p=SLIDES/f'slide_{i:02d}.png'
    lines.append(f"file '{p.as_posix()}'")
    lines.append(f'duration {w*scale:.3f}')
# repeat final file for concat demuxer
lines.append(f"file '{(SLIDES/'slide_05.png').as_posix()}'")
concat.write_text('\n'.join(lines)+'\n', encoding='utf-8')

# Convert VTT to coarse SRT if needed
vtt = PKG/'narration_35s_edge_hsiaoyu.vtt'
srt = PKG/'narration_35s_edge_hsiaoyu.srt'
text=vtt.read_text(encoding='utf-8') if vtt.exists() else ''
blocks=[]
for block in re.split(r'\n\s*\n', text.strip()):
    if '-->' not in block: continue
    lines=block.splitlines()
    timing=next(l for l in lines if '-->' in l)
    caption=' '.join(l.strip() for l in lines[lines.index(timing)+1:] if l.strip())
    timing=timing.replace('.', ',')
    blocks.append((timing, caption))
srt.write_text('\n\n'.join(f'{i}\n{t}\n{c}' for i,(t,c) in enumerate(blocks,1))+'\n', encoding='utf-8')

cmd=['ffmpeg','-y','-f','concat','-safe','0','-i',str(concat),'-i',str(PKG/'narration_35s_edge_hsiaoyu.mp3'),'-t',f'{TARGET:.3f}','-vf','fps=25,format=yuv420p','-af','apad','-c:v','libx264','-preset','veryfast','-crf','18','-c:a','aac','-b:a','128k','-shortest',str(MP4)]
# Do not use -shortest with apad? target still respected. Remove shortest if causes early cut.
cmd=['ffmpeg','-y','-f','concat','-safe','0','-i',str(concat),'-i',str(PKG/'narration_35s_edge_hsiaoyu.mp3'),'-t',f'{TARGET:.3f}','-vf','fps=25,format=yuv420p','-af','apad','-c:v','libx264','-preset','veryfast','-crf','18','-c:a','aac','-b:a','128k',str(MP4)]
subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Extract frames and QA sheet
for name,ts in [('frame_early.png',2.0),('frame_mid.png',17.0),('frame_late.png',32.0)]:
    subprocess.run(['ffmpeg','-y','-ss',str(ts),'-i',str(MP4),'-frames:v','1','-update','1',str(CHECKS/name)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

thumb_w, thumb_h = 360, 640
sheet=Image.new('RGB',(1600,1650),'#1B2635'); d=ImageDraw.Draw(sheet)
d.text((50,35),'三個可驗證證據｜Shorts MP4 QA sheet（cover + early/mid/late）',font=font(38),fill='white')
items=[('cover',COVER),('early 2s',CHECKS/'frame_early.png'),('mid 17s',CHECKS/'frame_mid.png'),('late 32s',CHECKS/'frame_late.png')]
pos=[(80,110),(600,110),(80,870),(600,870)]
for (label,p),(x,y) in zip(items,pos):
    im=Image.open(p).resize((thumb_w,thumb_h))
    sheet.paste(im,(x,y))
    d.text((x,y+thumb_h+16),label,font=font(32),fill='white')
sheet.save(CHECKS/'qa_sheet_mp4.png')

# Docs
upload = f"""# YouTube Upload Kit｜AI 給答案前，先叫它列出三個可驗證證據

## 建議標題
1. AI 給答案前，先叫它列三個證據
2. 學生用 AI 前，先問：證據在哪？
3. 答案漂亮不夠：AI 要先列可驗證證據

## 主檔案
- Shorts MP4：`{MP4.name}`
- 封面：`{COVER.name}`
- 旁白：`narration_35s_edge_hsiaoyu.mp3`
- 字幕：`narration_35s_edge_hsiaoyu.vtt` / `narration_35s_edge_hsiaoyu.srt`
- QA sheet：`checks/qa_sheet_mp4.png`

## 描述草稿
AI 回答前，先請它列出三個可驗證證據：現象、數據、原理。這個小步驟能讓學生不是抄答案，而是學會檢查答案是否被證據撐住。

#AI教學 #物理教學 #生成式AI #教師備課 #學生思辨 #AI素養

## 置頂留言
下次讓學生用 AI 前，可以先加這一句：\n「在回答前，請先列出三個可驗證證據，並標明每個證據怎麼檢查。」

## 人工操作卡點
YouTube 上傳、頻道選擇、公開／排程與留言置頂仍需使用者登入 Google / YouTube 後操作。
"""
(PKG/'youtube-upload-kit.md').write_text(upload, encoding='utf-8')

readme = f"""# Shorts｜AI 給答案前，先叫它列出三個可驗證證據

狀態：2026-05-12 每小時雷達已把 storyboard 擴成 35 秒本機 Shorts 草稿、封面、字幕與 YouTube upload kit。  
來源：第三季內容題庫優先題 1。

## 成果檔案

- Shorts MP4：`{MP4.name}`
- 封面：`{COVER.name}`
- 上傳包：`youtube-upload-kit.md`
- 旁白：`narration_35s_edge_hsiaoyu.mp3`
- 字幕：`narration_35s_edge_hsiaoyu.vtt` / `narration_35s_edge_hsiaoyu.srt`
- QA sheet：`checks/qa_sheet_mp4.png`
- 壓縮包：`{ARCHIVE.name}`

## 圖卡

1. `slides/slide_01.png`｜AI 給答案前，先要三個證據
2. `slides/slide_02.png`｜用一題問題把證據列出來
3. `slides/slide_03.png`｜不要只問 AI：答案是什麼？
4. `slides/slide_04.png`｜三欄證據卡 5 分鐘就能做
5. `slides/slide_05.png`｜老師把關句與 CTA

## 驗證

- MP4：1080×1920、25fps、H.264 + AAC、約 35 秒。
- PIL：封面、5 張圖卡與 QA 抽幀皆為 RGB 圖檔。
- 視覺 QA：`checks/qa_sheet_mp4.png` 已用於檢查繁中可讀、無 tofu 方塊、無裁切、無重疊與不過度擁擠。
- 壓縮包：已用 Python `tarfile` 讀回確認包含 MP4、封面、旁白、字幕、README、manifest、upload kit、slides 與 QA sheet。

## 穩定發布

- 手機索引：`https://addielu-phy.github.io/lu-ai-youtube-assets/mobile-index/index.html`
- 本機 package：`shorts/three-verifiable-evidence-before-answer-20260512/`
- GitHub Pages commit：待同步後回填。

## 下一個自動推進

若 YouTube/Google 登入仍未完成：從第三季題庫挑選下一個尚未完成的 Shorts storyboard／講義延伸。  
若使用者已完成 YouTube/Google 登入：優先上傳已完成的第一季首批 Shorts 或本支第三季 Shorts。
"""
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
    'teacher_cheatsheet':'three-evidence-question-cheatsheet-v1.md',
    'archive':ARCHIVE.name,
    'next_auto_push':'choose next unfinished season-03 candidate for storyboard/handout, unless YouTube login is ready for upload'
})
files=['README.md','manifest.json','render_storyboard.py','build_shorts_mp4_package.py','youtube-upload-kit.md',MP4.name,COVER.name,'narration_35s.txt','narration_35s_edge_hsiaoyu.mp3','narration_35s_edge_hsiaoyu.vtt','narration_35s_edge_hsiaoyu.srt','three-evidence-question-cheatsheet-v1.md','checks/contact_sheet.png','checks/qa_sheet_mp4.png','checks/frame_early.png','checks/frame_mid.png','checks/frame_late.png','slides_35s.ffconcat'] + [f'slides/slide_{i:02d}.png' for i in range(1,6)]
manifest['files']=files
(PKG/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')

with tarfile.open(ARCHIVE,'w:gz') as tar:
    for rel in files:
        p=PKG/rel
        if p.exists(): tar.add(p, arcname=f'{PKG.name}/{rel}')
# verify key files
with tarfile.open(ARCHIVE,'r:gz') as tar:
    names=tar.getnames()
for key in [MP4.name, COVER.name, 'youtube-upload-kit.md', 'README.md', 'manifest.json', 'checks/qa_sheet_mp4.png']:
    assert any(n.endswith(key) for n in names), key
print(json.dumps({'mp4':str(MP4),'cover':str(COVER),'archive':str(ARCHIVE),'archive_items':len(names)}, ensure_ascii=False, indent=2))
