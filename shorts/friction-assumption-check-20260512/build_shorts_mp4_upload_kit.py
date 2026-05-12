#!/usr/bin/env python3
from __future__ import annotations
import json, subprocess, tarfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE = Path('/home/adl/youtube-lu-ai-channel/shorts/friction-assumption-check-20260512')
FONT = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
W,H = 1080,1920
SLIDES = [BASE/'slides'/f'slide_{i:02d}.png' for i in range(1,6)]
OUT_MP4 = BASE/'friction-assumption-check-shorts-35s.mp4'
COVER = BASE/'cover_friction_assumption_check_v1.png'
NARR = BASE/'narration_35s.txt'
MP3 = BASE/'narration_35s_edge_hsiaoyu.mp3'
VTT = BASE/'narration_35s_edge_hsiaoyu.vtt'
SRT = BASE/'narration_35s_edge_hsiaoyu.srt'
CONCAT = BASE/'friction_assumption_check.ffconcat'
QA = BASE/'checks'/'qa_cover_frames_sheet.png'
HANDOUT = BASE/'friction-assumption-teacher-checklist-v1.md'
ARCHIVE = BASE/'friction-assumption-check-upload-kit-20260512.tar.gz'

narration = '''AI 說「忽略摩擦」，先別急著抄。忽略，不是萬用步驟，而是一個模型假設。
老師可以追問一句：這個假設合理嗎？為什麼可以忽略？
讓學生圈出 AI 解答裡被省略的東西：摩擦、空氣阻力、接觸面，還是能量損失。
再寫一句理由：我同意，因為影響很小；或我不同意，因為題目正在問它。
這樣學生學到的不是背答案，而是知道什麼時候可以簡化。'''

segments = [
    (0.0, 5.5, 'AI 說「忽略摩擦」，先別急著抄。'),
    (5.5, 12.0, '忽略不是萬用步驟，而是一個模型假設。'),
    (12.0, 20.5, '追問：這個假設合理嗎？為什麼可以忽略？'),
    (20.5, 29.0, '圈出被省略的東西，再寫同意或不同意的理由。'),
    (29.0, 35.0, '學生學到的，是什麼時候可以簡化。'),
]

def run(cmd):
    subprocess.run(cmd, check=True, cwd=BASE)

def ffprobe_duration(p: Path) -> float:
    out = subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(p)], text=True)
    return float(out.strip())

def font(size):
    return ImageFont.truetype(FONT, size=size, index=0)

def wrap(draw, text, fnt, max_w):
    lines=[]
    for para in text.split('\n'):
        buf=''
        for ch in para:
            test=buf+ch
            if draw.textbbox((0,0), test, font=fnt)[2] <= max_w:
                buf=test
            else:
                if buf: lines.append(buf)
                buf=ch
        if buf: lines.append(buf)
    return lines

def draw_center(draw, y, text, fnt, fill, max_w, spacing=14):
    lines=wrap(draw, text, fnt, max_w)
    heights=[draw.textbbox((0,0), l, font=fnt)[3]-draw.textbbox((0,0), l, font=fnt)[1] for l in lines]
    yy=y-(sum(heights)+spacing*(len(lines)-1))/2
    for l,h in zip(lines,heights):
        b=draw.textbbox((0,0), l, font=fnt)
        draw.text(((W-(b[2]-b[0]))/2, yy), l, font=fnt, fill=fill)
        yy += h+spacing

def make_cover():
    im=Image.new('RGB',(W,H),'#F7F2E8')
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((70,90,1010,1830), radius=60, fill='#1F2A44')
    d.rounded_rectangle((125,150,955,430), radius=40, fill='#F6C453')
    d.text((175,205),'AI 說忽略摩擦？', font=font(66), fill='#1F2A44')
    draw_center(d, 730, '先問一句：\n為什麼可以忽略？', font(92), '#FFFFFF', 850, spacing=24)
    d.rounded_rectangle((150,1035,930,1415), radius=38, fill='#FFFFFF')
    d.text((205,1085),'假設檢查卡', font=font(54), fill='#D45D3A')
    d.text((205,1170),'1 影響小嗎？', font=font(48), fill='#1F2A44')
    d.text((205,1245),'2 題目允許嗎？', font=font(48), fill='#1F2A44')
    d.text((205,1320),'3 目的需要嗎？', font=font(48), fill='#1F2A44')
    d.rounded_rectangle((165,1515,915,1655), radius=30, outline='#F6C453', width=6)
    d.text((215,1555),'忽略不是口訣，是證據。', font=font(48), fill='#FFFFFF')
    im.save(COVER)

def write_subs(duration):
    def ts(sec, comma=False):
        ms=int(round((sec-int(sec))*1000)); s=int(sec)%60; m=(int(sec)//60)%60; h=int(sec)//3600
        return f'{h:02d}:{m:02d}:{s:02d}{"," if comma else "."}{ms:03d}'
    v=['WEBVTT','']; s=[]
    for idx,(a,b,t) in enumerate(segments,1):
        b=min(b,duration)
        v += [f'{ts(a)} --> {ts(b)}', t, '']
        s += [str(idx), f'{ts(a,True)} --> {ts(b,True)}', t, '']
    VTT.write_text('\n'.join(v), encoding='utf-8')
    SRT.write_text('\n'.join(s), encoding='utf-8')

def make_concat(duration):
    duration=max(35.0, duration)
    weights=[0.18,0.19,0.22,0.22,0.19]
    durs=[round(duration*w,3) for w in weights]
    durs[-1]+=round(duration-sum(durs),3)
    lines=['ffconcat version 1.0']
    for slide,dur in zip(SLIDES,durs):
        lines += [f"file '{slide}'", f'duration {dur:.3f}']
    lines += [f"file '{SLIDES[-1]}'"]
    CONCAT.write_text('\n'.join(lines)+'\n', encoding='utf-8')

def make_handout():
    HANDOUT.write_text('''# 忽略摩擦假設檢查表｜教師可列印 v1

## 一句目標
讓學生知道：「忽略摩擦」不是口訣，而是要能說明的模型假設。

## 3 分鐘使用情境
- AI 解答、課本例題或學生作答中出現「忽略摩擦／不計空阻／理想化」。
- 老師不重算整題，只要求學生檢查這個假設是否合理。

## 學生三問
| 問題 | 學生填寫 |
|---|---|
| 1. 被忽略的是什麼？ | 摩擦／空阻／能量損失／其他：____ |
| 2. 題目有沒有明說可以忽略？ | 有／沒有；證據：____ |
| 3. 如果不忽略，答案或概念會變很多嗎？ | 很小／可能很大；理由：____ |

## 可複製 AI 追問 prompt
請檢查這份解答中「忽略摩擦」是否合理。先列出被忽略的物理因素，再說明在什麼條件下可以忽略，最後指出若不能忽略，答案或模型會怎麼改變。

## 老師示範句
「我不是要你背摩擦一定要算，而是要你說清楚：這一題為什麼可以不算。」

## 快速評分
- 2 分：能指出被忽略因素，也能用題目條件或量級說明理由。
- 1 分：只說可以／不可以，但理由不完整。
- 0 分：只抄 AI 結論，沒有檢查假設。

## 公開分享提醒
不要使用未公開考題或學生個資；若使用學生回答，請改寫成匿名範例。
''', encoding='utf-8')

def extract_qa():
    check=BASE/'checks'; check.mkdir(exist_ok=True)
    times=[2,12,24,33]
    frames=[]
    for i,t in enumerate(times,1):
        p=check/f'frame_{i:02d}_{t}s.png'
        run(['ffmpeg','-y','-ss',str(t),'-i',str(OUT_MP4),'-frames:v','1',str(p)])
        frames.append(p)
    thumbs=[COVER]+frames
    # Non-overlapping 2-column / 3-row QA sheet so every asset can be inspected.
    canvas=Image.new('RGB',(1120,2880),'white')
    d=ImageDraw.Draw(canvas)
    positions=[(20,20),(580,20),(20,960),(580,960),(20,1900)]
    for p,(x,y) in zip(thumbs,positions):
        im=Image.open(p).convert('RGB'); im.thumbnail((520,900))
        canvas.paste(im,(x,y))
        d.text((x,y+im.height+8), p.name, font=font(22), fill='#333333')
    canvas.save(QA)

def main():
    (BASE/'checks').mkdir(exist_ok=True)
    NARR.write_text(narration, encoding='utf-8')
    make_cover(); make_handout()
    run(['edge-tts','--voice','zh-TW-HsiaoYuNeural','--rate','+20%','-f',str(NARR),'--write-media',str(MP3)])
    dur=ffprobe_duration(MP3)
    if dur > 42:
        run(['edge-tts','--voice','zh-TW-HsiaoYuNeural','--rate','+30%','-f',str(NARR),'--write-media',str(MP3)])
        dur=ffprobe_duration(MP3)
    make_concat(dur); write_subs(max(35.0,dur))
    run(['ffmpeg','-y','-f','concat','-safe','0','-i',str(CONCAT),'-i',str(MP3),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-pix_fmt','yuv420p','-r','25','-af','apad','-t','35.0','-c:a','aac','-b:a','128k',str(OUT_MP4)])
    extract_qa()
    mp4dur=ffprobe_duration(OUT_MP4)
    (BASE/'youtube-upload-kit.md').write_text(f'''# YouTube upload kit｜AI 說「忽略摩擦」時，老師要問的一句話

狀態：本機 35 秒 Shorts 草稿、封面、字幕、教師檢查表與上傳交接包已完成（2026-05-12）。

## 主檔
- 影片：`friction-assumption-check-shorts-35s.mp4`
- 封面：`cover_friction_assumption_check_v1.png`
- 旁白：`narration_35s_edge_hsiaoyu.mp3`
- 字幕：`narration_35s_edge_hsiaoyu.vtt`、`narration_35s_edge_hsiaoyu.srt`
- 教師檢查表：`friction-assumption-teacher-checklist-v1.md`

## 標題候選
1. AI 說「忽略摩擦」時，老師要問的一句話
2. 忽略摩擦可以嗎？先問這 3 件事
3. AI 解題看似合理？先檢查它省略了什麼

## 說明欄草稿
AI 解答常說「忽略摩擦」，但這不是固定口訣，而是需要被題目條件和模型目的支持的假設。這支 Shorts 給老師一張假設檢查卡：被忽略的是什麼？題目允許嗎？如果不忽略會差很多嗎？

#AI教學 #物理教學 #生成式AI #教師備課 #課堂活動

## 置頂留言草稿
你會讓學生怎麼判斷「忽略摩擦」合不合理？可以先用這句：被忽略的是____，我同意／不同意，因為____。

## 人工作業卡點
YouTube 上傳、頻道選擇、封面套用與公開發布仍需使用者登入 Google / YouTube 後操作。

## 驗證
- ffprobe：影片為 1080×1920、25fps、H.264 + AAC，長度約 {mp4dur:.3f} 秒。
- 視覺 QA：`checks/qa_cover_frames_sheet.png` 用於檢查封面與早／中／晚抽幀。
''', encoding='utf-8')
    manifest=json.loads((BASE/'manifest.json').read_text(encoding='utf-8'))
    manifest.update({
        'status':'35s Shorts MP4 + upload kit + teacher checklist complete',
        'video':'friction-assumption-check-shorts-35s.mp4',
        'cover':'cover_friction_assumption_check_v1.png',
        'narration':'narration_35s_edge_hsiaoyu.mp3',
        'subtitles':['narration_35s_edge_hsiaoyu.vtt','narration_35s_edge_hsiaoyu.srt'],
        'upload_kit':'youtube-upload-kit.md',
        'teacher_checklist':'friction-assumption-teacher-checklist-v1.md',
        'qa_sheet':'checks/qa_cover_frames_sheet.png',
        'archive':'friction-assumption-check-upload-kit-20260512.tar.gz',
        'next_auto_push':'choose the next unmade season-02 backlog item (priority 6, 11, or 12) or upload completed Shorts after YouTube login is ready'
    })
    (BASE/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    (BASE/'README.md').write_text(f'''# Shorts｜AI 說「忽略摩擦」時，老師要問的一句話

狀態：2026-05-12 每小時雷達已由 storyboard package v1 擴成 35 秒本機 Shorts 草稿、封面、旁白、字幕、YouTube upload kit、教師檢查表與交接壓縮包。
來源：第二季內容題庫優先題 10。

## 主檔
- 影片：`friction-assumption-check-shorts-35s.mp4`
- 封面：`cover_friction_assumption_check_v1.png`
- 上傳包：`youtube-upload-kit.md`
- 教師檢查表：`friction-assumption-teacher-checklist-v1.md`
- 旁白：`narration_35s_edge_hsiaoyu.mp3`
- 字幕：`narration_35s_edge_hsiaoyu.vtt`、`narration_35s_edge_hsiaoyu.srt`
- 壓縮包：`friction-assumption-check-upload-kit-20260512.tar.gz`

## 圖卡
1. `slides/slide_01.png`｜AI 說忽略摩擦，先別急著抄
2. `slides/slide_02.png`｜一句「忽略摩擦」藏了模型假設
3. `slides/slide_03.png`｜摩擦假設三問
4. `slides/slide_04.png`｜學生圈出被忽略的東西
5. `slides/slide_05.png`｜假設是假答案的開關

## 驗證
- storyboard：5 張 `1080×1920` RGB PNG；原 contact sheet：`checks/contact_sheet.png`。
- 影片：ffprobe 驗證 `1080×1920`、25fps、H.264 + AAC、{mp4dur:.3f} 秒。
- QA sheet：`checks/qa_cover_frames_sheet.png`，包含封面與 2s／12s／24s／33s 抽幀。
- 壓縮包：已用 Python tarfile 讀回驗證包含影片、封面、旁白、字幕、README、manifest、upload kit、教師檢查表、slides、QA sheet 與腳本。

## 下一個自動推進
若 YouTube/Google 登入仍未完成：從第二季題庫挑選尚未完成的優先題 6、11 或 12，製作下一支 storyboard／講義延伸。  
若使用者已完成 YouTube/Google 登入：優先上傳第一季首批或本支第二季 Shorts。
''', encoding='utf-8')
    include=['README.md','youtube-upload-kit.md','manifest.json','render_storyboard.py','build_shorts_mp4_upload_kit.py','narration_35s.txt','narration_35s_edge_hsiaoyu.mp3','narration_35s_edge_hsiaoyu.vtt','narration_35s_edge_hsiaoyu.srt','friction_assumption_check.ffconcat','friction-assumption-check-shorts-35s.mp4','cover_friction_assumption_check_v1.png','friction-assumption-teacher-checklist-v1.md','slides/slide_01.png','slides/slide_02.png','slides/slide_03.png','slides/slide_04.png','slides/slide_05.png','checks/contact_sheet.png','checks/qa_cover_frames_sheet.png','checks/frame_01_2s.png','checks/frame_02_12s.png','checks/frame_03_24s.png','checks/frame_04_33s.png']
    with tarfile.open(ARCHIVE,'w:gz') as tar:
        for rel in include:
            tar.add(BASE/rel, arcname=f'friction-assumption-check-20260512/{rel}')
    with tarfile.open(ARCHIVE,'r:gz') as tar:
        names=tar.getnames()
    print(json.dumps({'base':str(BASE),'duration':mp4dur,'archive_count':len(names),'archive_key_files':[n for n in names if n.endswith(('.mp4','youtube-upload-kit.md','friction-assumption-teacher-checklist-v1.md'))]}, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
