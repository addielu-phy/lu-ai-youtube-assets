#!/usr/bin/env python3
from __future__ import annotations
import json, subprocess, tarfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE = Path('/home/adl/youtube-lu-ai-channel/shorts/homework-feedback-teacher-review-20260512')
FONT = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
W,H = 1080,1920
SLIDES = [BASE/'slides'/f'slide_{i:02d}.png' for i in range(1,6)]
OUT_MP4 = BASE/'homework-feedback-teacher-review-shorts-35s.mp4'
COVER = BASE/'cover_homework_feedback_teacher_review_v1.png'
NARR = BASE/'narration_35s.txt'
MP3 = BASE/'narration_35s_edge_hsiaoyu.mp3'
VTT = BASE/'narration_35s_edge_hsiaoyu.vtt'
SRT = BASE/'narration_35s_edge_hsiaoyu.srt'
CONCAT = BASE/'homework_feedback_teacher_review.ffconcat'
QA = BASE/'checks'/'qa_cover_frames_sheet.png'
HANDOUT = BASE/'ai-feedback-review-teacher-checklist-v1.md'
ARCHIVE = BASE/'homework-feedback-teacher-review-upload-kit-20260512.tar.gz'

narration = '''AI 幫忙回饋作業，速度很快，但老師不能直接轉貼。
先看第一件事：語氣。這段話會鼓勵學生修正，還是讓學生覺得被否定？
第二件事：概念。AI 有沒有把錯誤說成只是小失誤？
第三件事：下一步。學生看完後，知道要改哪一句、補哪個理由嗎？
把 AI 回饋當初稿，老師最後審稿；學生收到的才是可行的學習建議。'''

segments = [
    (0.0, 5.5, 'AI 回饋很快，但老師不能直接轉貼。'),
    (5.5, 12.0, '先看語氣：是鼓勵修正，還是否定學生？'),
    (12.0, 20.0, '再看概念：有沒有把錯誤說成小失誤？'),
    (20.0, 28.5, '最後看下一步：學生知道要改哪裡嗎？'),
    (28.5, 35.0, '把 AI 回饋當初稿，老師最後審稿。'),
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
    d.rounded_rectangle((125,150,955,420), radius=42, fill='#F6C453')
    draw_center(d, 285, 'AI 幫忙回饋作業', font(68), '#1F2A44', 760, spacing=18)
    draw_center(d, 720, '老師不能\n跳過哪一步？', font(94), '#FFFFFF', 860, spacing=28)
    d.rounded_rectangle((145,1015,935,1435), radius=38, fill='#FFFFFF')
    d.text((205,1070),'三件審稿事', font=font(56), fill='#D45D3A')
    d.text((205,1160),'1 語氣：能鼓勵修正嗎？', font=font(43), fill='#1F2A44')
    d.text((205,1235),'2 概念：有沒有講錯？', font=font(43), fill='#1F2A44')
    d.text((205,1310),'3 下一步：學生會改嗎？', font=font(43), fill='#1F2A44')
    d.rounded_rectangle((165,1530,915,1665), radius=30, outline='#F6C453', width=6)
    d.text((215,1570),'AI 是初稿，老師做最後審稿。', font=font(42), fill='#FFFFFF')
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
    weights=[0.18,0.19,0.21,0.23,0.19]
    durs=[round(duration*w,3) for w in weights]
    durs[-1]+=round(duration-sum(durs),3)
    lines=['ffconcat version 1.0']
    for slide,dur in zip(SLIDES,durs):
        lines += [f"file '{slide}'", f'duration {dur:.3f}']
    lines += [f"file '{SLIDES[-1]}'"]
    CONCAT.write_text('\n'.join(lines)+'\n', encoding='utf-8')

def make_handout():
    HANDOUT.write_text('''# AI 回饋審稿檢查表｜教師可列印 v1

## 一句目標
讓老師把 AI 產生的作業回饋改成「語氣合適、概念正確、下一步清楚」的學習建議。

## 適用情境
- 老師想用 AI 協助批改、回饋作業或產生個別化建議。
- 學生答案可以匿名改寫後放入 AI，不使用真實姓名、座號或可辨識個資。

## 三步審稿表
| 檢查點 | 老師快速判斷 | 需要改寫時的提示 |
|---|---|---|
| 1. 語氣 | 這段話會鼓勵學生修正嗎？ | 把「你錯了」改成「下一步可以先修正____」。 |
| 2. 概念 | AI 有沒有把錯誤原因講錯或講太快？ | 要求 AI 指出依據，老師再保留正確部分。 |
| 3. 下一步 | 學生知道要改哪一句、補哪個理由嗎？ | 加上「請先改____，再補一句因為____」。 |

## 可複製 AI prompt
請根據這份學生作答產生回饋初稿，但必須符合三點：語氣鼓勵修正、物理概念正確、給出一個學生下一步可以立即修改的具體行動。不要放入學生個資。

## 學生改寫區
AI 原回饋：______________________________

我覺得需要調整的地方：語氣／概念／下一步

我改寫後的回饋：________________________

## 老師示範句
「AI 可以先幫我們寫初稿，但給學生之前，老師一定要確認：這句話是不是能讓學生知道下一步。」

## 快速評分
- 2 分：能同時修正語氣、概念與下一步。
- 1 分：只修正其中一到兩項。
- 0 分：直接複製 AI 回饋，沒有審稿。

## 公開分享提醒
不要上傳學生姓名、成績、座號、照片或未授權作業截圖；公開示範請使用匿名、改寫後的範例。
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
    (BASE/'youtube-upload-kit.md').write_text(f'''# YouTube upload kit｜AI 幫忙回饋作業，老師不能跳過哪一步？

狀態：本機 35 秒 Shorts 草稿、封面、字幕、教師檢查表與上傳交接包已完成（2026-05-12）。

## 主檔
- 影片：`homework-feedback-teacher-review-shorts-35s.mp4`
- 封面：`cover_homework_feedback_teacher_review_v1.png`
- 旁白：`narration_35s_edge_hsiaoyu.mp3`
- 字幕：`narration_35s_edge_hsiaoyu.vtt`、`narration_35s_edge_hsiaoyu.srt`
- 教師檢查表：`ai-feedback-review-teacher-checklist-v1.md`

## 標題候選
1. AI 幫忙回饋作業，老師不能跳過哪一步？
2. AI 批改很快，但老師要審這 3 件事
3. 給學生 AI 回饋前，先做三步審稿

## 說明欄草稿
AI 可以協助老師快速產生作業回饋，但給學生之前，老師仍要做最後審稿：語氣是否鼓勵修正？概念是否正確？學生是否知道下一步怎麼改？這支 Shorts 提供一張「AI 回饋審稿檢查表」。

#AI教學 #教師備課 #生成式AI #作業回饋 #課堂活動

## 置頂留言草稿
你會先審 AI 回饋的哪一項？語氣、概念，還是下一步？我會先問：學生看完知道要改哪裡嗎？

## 人工作業卡點
YouTube 上傳、頻道選擇、封面套用與公開發布仍需使用者登入 Google / YouTube 後操作。

## 驗證
- ffprobe：影片為 1080×1920、25fps、H.264 + AAC，長度約 {mp4dur:.3f} 秒。
- 視覺 QA：`checks/qa_cover_frames_sheet.png` 用於檢查封面與早／中／晚抽幀。
''', encoding='utf-8')
    manifest=json.loads((BASE/'manifest.json').read_text(encoding='utf-8'))
    manifest.update({
        'status':'35s Shorts MP4 + upload kit + teacher checklist complete',
        'video':'homework-feedback-teacher-review-shorts-35s.mp4',
        'cover':'cover_homework_feedback_teacher_review_v1.png',
        'narration':'narration_35s_edge_hsiaoyu.mp3',
        'subtitles':['narration_35s_edge_hsiaoyu.vtt','narration_35s_edge_hsiaoyu.srt'],
        'upload_kit':'youtube-upload-kit.md',
        'teacher_checklist':'ai-feedback-review-teacher-checklist-v1.md',
        'qa_sheet':'checks/qa_cover_frames_sheet.png',
        'archive':'homework-feedback-teacher-review-upload-kit-20260512.tar.gz',
        'next_auto_push':'choose the next unmade season-02 backlog item (priority 6 or 12) or upload completed Shorts after YouTube login is ready'
    })
    (BASE/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    (BASE/'README.md').write_text(f'''# Shorts｜AI 幫忙回饋作業，老師不能跳過哪一步？

狀態：2026-05-12 每小時雷達已由 storyboard package v1 擴成 35 秒本機 Shorts 草稿、封面、旁白、字幕、YouTube upload kit、教師檢查表與交接壓縮包。
來源：第二季內容題庫優先題 11。

## 主檔
- 影片：`homework-feedback-teacher-review-shorts-35s.mp4`
- 封面：`cover_homework_feedback_teacher_review_v1.png`
- 上傳包：`youtube-upload-kit.md`
- 教師檢查表：`ai-feedback-review-teacher-checklist-v1.md`
- 旁白：`narration_35s_edge_hsiaoyu.mp3`
- 字幕：`narration_35s_edge_hsiaoyu.vtt`、`narration_35s_edge_hsiaoyu.srt`
- 壓縮包：`homework-feedback-teacher-review-upload-kit-20260512.tar.gz`

## 圖卡
1. `slides/slide_01.png`｜AI 回饋很快，但不能直接轉貼
2. `slides/slide_02.png`｜老師先審語氣
3. `slides/slide_03.png`｜再審概念
4. `slides/slide_04.png`｜最後補下一步
5. `slides/slide_05.png`｜AI 是初稿，老師做最後審稿

## 驗證
- storyboard：5 張 `1080×1920` RGB PNG；原 contact sheet：`checks/contact_sheet.png`。
- 影片：ffprobe 驗證 `1080×1920`、25fps、H.264 + AAC、{mp4dur:.3f} 秒。
- QA sheet：`checks/qa_cover_frames_sheet.png`，包含封面與 2s／12s／24s／33s 抽幀。
- 壓縮包：已用 Python tarfile 讀回驗證包含影片、封面、旁白、字幕、README、manifest、upload kit、教師檢查表、slides、QA sheet 與腳本。

## 下一個自動推進
若 YouTube/Google 登入仍未完成：從第二季題庫挑選尚未完成的優先題 6 或 12，製作下一支 storyboard／講義延伸。  
若使用者已完成 YouTube/Google 登入：優先上傳第一季首批或本支第二季 Shorts。
''', encoding='utf-8')
    include=['README.md','youtube-upload-kit.md','manifest.json','render_storyboard.py','build_shorts_mp4_upload_kit.py','narration_35s.txt','narration_35s_edge_hsiaoyu.mp3','narration_35s_edge_hsiaoyu.vtt','narration_35s_edge_hsiaoyu.srt','homework_feedback_teacher_review.ffconcat','homework-feedback-teacher-review-shorts-35s.mp4','cover_homework_feedback_teacher_review_v1.png','ai-feedback-review-teacher-checklist-v1.md','slides/slide_01.png','slides/slide_02.png','slides/slide_03.png','slides/slide_04.png','slides/slide_05.png','checks/contact_sheet.png','checks/qa_cover_frames_sheet.png','checks/frame_01_2s.png','checks/frame_02_12s.png','checks/frame_03_24s.png','checks/frame_04_33s.png']
    with tarfile.open(ARCHIVE,'w:gz') as tar:
        for rel in include:
            tar.add(BASE/rel, arcname=f'homework-feedback-teacher-review-20260512/{rel}')
    with tarfile.open(ARCHIVE,'r:gz') as tar:
        names=tar.getnames()
    print(json.dumps({'base':str(BASE),'duration':mp4dur,'archive_count':len(names),'archive_key_files':[n for n in names if n.endswith(('.mp4','youtube-upload-kit.md','ai-feedback-review-teacher-checklist-v1.md'))]}, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
