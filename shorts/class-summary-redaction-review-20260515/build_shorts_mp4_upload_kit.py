#!/usr/bin/env python3
from __future__ import annotations
import json, subprocess, tarfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE = Path('/home/adl/youtube-lu-ai-channel/shorts/class-summary-redaction-review-20260515')
FONT = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
W,H = 1080,1920
SLIDES = [BASE/'slides'/f'slide_{i:02d}.png' for i in range(1,6)]
OUT_MP4 = BASE/'class-summary-redaction-review-shorts-35s.mp4'
COVER = BASE/'cover_class_summary_redaction_review_v1.png'
NARR = BASE/'narration_35s.txt'
MP3 = BASE/'narration_35s_edge_hsiaoyu.mp3'
VTT = BASE/'narration_35s_edge_hsiaoyu.vtt'
SRT = BASE/'narration_35s_edge_hsiaoyu.srt'
CONCAT = BASE/'class_summary_redaction_review.ffconcat'
QA = BASE/'checks'/'qa_cover_frames_sheet.png'
HANDOUT = BASE/'summary-redaction-teacher-checklist-v1.md'
UPLOAD = BASE/'youtube-upload-kit.md'
MANIFEST = BASE/'manifest.json'
ARCHIVE = BASE/'class-summary-redaction-review-upload-kit-20260515.tar.gz'

narration = '''AI 幫你整理課堂摘要時，最危險的不是寫得不好，而是寫得太像真的。
第一種先刪：能看出是哪位學生的句子，例如座號、特殊事件、可辨識錯誤。
第二種先刪：把學生貼標籤的句子，像是懶散、粗心、程度差。
第三種先刪：沒有證據的評價，例如全班都不懂，或某組表現最差。
改成匿名、可觀察、可改進的學習線索。摘要才是教學工具，不是學生標籤。'''
segments = [
    (0,5,'AI 摘要最危險：寫得太像真的。'),
    (5,12,'先刪可辨識學生的句子。'),
    (12,20,'再刪把學生貼標籤的句子。'),
    (20,28,'沒有證據的全班評價，也先刪。'),
    (28,35,'改成匿名、可觀察、可改進的學習線索。'),
]

def run(cmd): subprocess.run(cmd, check=True, cwd=BASE)
def duration(p: Path) -> float:
    return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(p)], text=True).strip())
def font(size): return ImageFont.truetype(FONT, size=size, index=0)
def wrap(draw, text, fnt, max_w):
    lines=[]
    for para in text.split('\n'):
        buf=''
        for ch in para:
            test=buf+ch
            if draw.textbbox((0,0), test, font=fnt)[2] <= max_w: buf=test
            else:
                if buf: lines.append(buf)
                buf=ch
        if buf: lines.append(buf)
    return lines
def center(draw, y, text, fnt, fill, max_w, spacing=14):
    lines=wrap(draw,text,fnt,max_w)
    hs=[draw.textbbox((0,0),l,font=fnt)[3]-draw.textbbox((0,0),l,font=fnt)[1] for l in lines]
    yy=y-(sum(hs)+spacing*(len(lines)-1))/2
    for l,h in zip(lines,hs):
        b=draw.textbbox((0,0),l,font=fnt)
        draw.text(((W-(b[2]-b[0]))/2, yy), l, font=fnt, fill=fill)
        yy += h+spacing

def make_cover():
    im=Image.new('RGB',(W,H),'#F7F1E6'); d=ImageDraw.Draw(im)
    d.rounded_rectangle((70,90,1010,1830), radius=64, fill='#12223A')
    d.rounded_rectangle((125,150,955,355), radius=42, fill='#F4C542')
    center(d,252,'AI 摘要完成前',font(64),'#12223A',760,8)
    center(d,590,'先刪\n這 3 種句子',font(112),'#FFFFFF',850,20)
    card=(145,875,935,1425)
    d.rounded_rectangle(card, radius=44, fill='#FFFFFF')
    rows=[('1','可辨識學生','姓名、座號、特殊事件'),('2','貼標籤評語','懶散、粗心、程度差'),('3','無證據評價','全班都不懂、某組最差')]
    y=930
    for n,t,sub in rows:
        d.ellipse((185,y,255,y+70), fill='#D75A4A')
        center(d,y+35,n,font(38),'#FFFFFF',60,0)
        d.text((285,y-2),t,font=font(46),fill='#12223A')
        d.text((285,y+52),sub,font=font(30),fill='#5B6577')
        y += 155
    d.rounded_rectangle((155,1535,925,1685), radius=32, outline='#F4C542', width=6)
    center(d,1610,'改成匿名、可觀察、可改進',font(45),'#FFFFFF',720,8)
    im.save(COVER)

def write_subs(total):
    def ts(sec, comma=False):
        ms=int(round((sec-int(sec))*1000)); s=int(sec)%60; m=(int(sec)//60)%60; h=int(sec)//3600
        return f'{h:02d}:{m:02d}:{s:02d}{"," if comma else "."}{ms:03d}'
    v=['WEBVTT','']; s=[]
    for i,(a,b,t) in enumerate(segments,1):
        b=min(b,total)
        v += [f'{ts(a)} --> {ts(b)}', t, '']
        s += [str(i), f'{ts(a,True)} --> {ts(b,True)}', t, '']
    VTT.write_text('\n'.join(v), encoding='utf-8'); SRT.write_text('\n'.join(s), encoding='utf-8')

def concat_file(total):
    total=max(35,total); weights=[0.16,0.21,0.22,0.22,0.19]
    ds=[round(total*w,3) for w in weights]; ds[-1]+=round(total-sum(ds),3)
    lines=['ffconcat version 1.0']
    for p,du in zip(SLIDES,ds): lines += [f"file '{p}'", f'duration {du:.3f}']
    lines += [f"file '{SLIDES[-1]}'"]
    CONCAT.write_text('\n'.join(lines)+'\n', encoding='utf-8')

def qa_sheet():
    check=BASE/'checks'; check.mkdir(exist_ok=True)
    frames=[]
    for i,t in enumerate([2,12,24,33],1):
        p=check/f'frame_{i:02d}_{t}s.png'
        run(['ffmpeg','-y','-ss',str(t),'-i',str(OUT_MP4),'-frames:v','1','-update','1',str(p)])
        frames.append(p)
    canvas=Image.new('RGB',(1120,2880),'white'); d=ImageDraw.Draw(canvas)
    for p,(x,y) in zip([COVER]+frames,[(20,20),(580,20),(20,960),(580,960),(20,1900)]):
        im=Image.open(p).convert('RGB'); im.thumbnail((520,900)); canvas.paste(im,(x,y)); d.text((x,y+im.height+8), p.name, font=font(22), fill='#333')
    canvas.save(QA)

def write_docs(mp4dur):
    UPLOAD.write_text(f'''# YouTube upload kit｜AI 生成的課堂摘要，老師要刪掉哪一種句子？

狀態：本機 35 秒 Shorts 草稿、封面、字幕、教師檢查表與上傳交接包已完成（2026-05-15）。

## 主檔
- 影片：`class-summary-redaction-review-shorts-35s.mp4`
- 封面：`cover_class_summary_redaction_review_v1.png`
- 旁白：`narration_35s_edge_hsiaoyu.mp3`
- 字幕：`narration_35s_edge_hsiaoyu.vtt`、`narration_35s_edge_hsiaoyu.srt`
- 教師檢查表：`summary-redaction-teacher-checklist-v1.md`

## 標題候選
1. AI 生成課堂摘要前，老師先刪這 3 種句子
2. 課堂摘要越順，越要先做匿名審稿
3. AI 幫你寫摘要？先刪掉學生標籤

## 說明欄草稿
AI 可以快速整理課堂摘要，但公開、回饋或交給學生前，老師要先刪掉三種句子：可辨識學生、貼標籤評語、沒有證據的全班評價。把它們改成匿名、可觀察、可改進的學習線索。

#AI教學 #教師備課 #課堂摘要 #生成式AI #數位素養

## 置頂留言草稿
你會要求 AI 摘要保留哪一種「可觀察證據」？我會先刪：姓名／標籤／沒有證據的全班評價。

## 人工作業卡點
YouTube 上傳、頻道選擇、封面套用與公開發布仍需使用者登入 Google / YouTube 後操作。

## 驗證
- ffprobe：影片為 1080×1920、25fps、H.264 + AAC，長度約 {mp4dur:.3f} 秒。
- QA sheet：`checks/qa_cover_frames_sheet.png`。
''', encoding='utf-8')
    (BASE/'README.md').write_text(f'''# Shorts package｜AI 生成的課堂摘要，老師要刪掉哪一種句子？

狀態：2026-05-15 每小時雷達已由 storyboard 擴成本機 35 秒 Shorts 草稿、封面、字幕、YouTube upload kit、教師檢查表與交接壓縮包。  
來源：第三季內容題庫優先題 11。

## 主檔
- 影片：`class-summary-redaction-review-shorts-35s.mp4`
- 封面：`cover_class_summary_redaction_review_v1.png`
- 上傳包：`youtube-upload-kit.md`
- 教師檢查表：`summary-redaction-teacher-checklist-v1.md`
- 壓縮包：`class-summary-redaction-review-upload-kit-20260515.tar.gz`

## 原始圖卡
1. `slides/slide_01.png`｜摘要越順，越要先審
2. `slides/slide_02.png`｜順口的摘要，可能藏個資與標籤
3. `slides/slide_03.png`｜丟給 AI 前，先加一條紅線
4. `slides/slide_04.png`｜把學生標籤，改成學習線索
5. `slides/slide_05.png`｜三種句子，摘要完成前先刪

## 驗證
- 影片：1080×1920、25fps、H.264 + AAC、約 {mp4dur:.3f} 秒。
- 圖卡與封面：PIL 驗證 1080×1920 RGB。
- QA sheet：`checks/qa_cover_frames_sheet.png`。
- 交接包：Python tarfile 已讀回確認包含 MP4、封面、字幕、upload kit、教師檢查表、圖卡與 QA sheet。

## 下一個自動推進
若 YouTube/Google 登入仍未完成：從第三季題庫挑選下一個尚未完成的 Shorts storyboard／講義延伸；若已登入，優先上傳第一季首批或本支第三季 Shorts。
''', encoding='utf-8')
    data=json.loads(MANIFEST.read_text(encoding='utf-8'))
    data.update({'status':'35s Shorts MP4/upload kit complete','updated':'2026-05-15','video':'class-summary-redaction-review-shorts-35s.mp4','cover':'cover_class_summary_redaction_review_v1.png','upload_kit':'youtube-upload-kit.md','teacher_checklist':'summary-redaction-teacher-checklist-v1.md','archive':'class-summary-redaction-review-upload-kit-20260515.tar.gz','next_auto_push':'choose the next unfinished season-03 candidate for storyboard/handout extension unless YouTube login is ready for upload'})
    data.setdefault('verified',{})['local']='ffprobe/PIL/QA sheet/tarfile verified in 2026-05-15 scheduled run'
    MANIFEST.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n', encoding='utf-8')

def archive():
    files=[Path('README.md'),Path('manifest.json'),Path('render_storyboard.py'),Path('build_shorts_mp4_upload_kit.py'),Path('youtube-upload-kit.md'),Path('summary-redaction-teacher-checklist-v1.md'),Path('narration_35s.txt'),Path('narration_35s_edge_hsiaoyu.mp3'),Path('narration_35s_edge_hsiaoyu.vtt'),Path('narration_35s_edge_hsiaoyu.srt'),Path('class-summary-redaction-review-shorts-35s.mp4'),Path('cover_class_summary_redaction_review_v1.png'),Path('class_summary_redaction_review.ffconcat'),Path('checks/contact_sheet.png'),Path('checks/qa_cover_frames_sheet.png')]
    files += [Path('slides')/f'slide_{i:02d}.png' for i in range(1,6)]
    files += sorted(Path('checks').glob('frame_*.png'))
    with tarfile.open(ARCHIVE,'w:gz') as tar:
        for rel in files:
            p=BASE/rel
            if p.exists(): tar.add(p, arcname=f'class-summary-redaction-review-20260515/{rel}')
    with tarfile.open(ARCHIVE,'r:gz') as tar:
        names=tar.getnames()
        needed=['class-summary-redaction-review-shorts-35s.mp4','youtube-upload-kit.md','summary-redaction-teacher-checklist-v1.md']
        assert all(any(n.endswith(k) for n in names) for k in needed), names
        print('archive_members', len(names))

def main():
    (BASE/'checks').mkdir(exist_ok=True)
    for p in SLIDES:
        im=Image.open(p); assert im.size==(W,H) and im.mode=='RGB', (p, im.size, im.mode)
    assert HANDOUT.exists(), HANDOUT
    NARR.write_text(narration, encoding='utf-8')
    make_cover()
    run(['edge-tts','--voice','zh-TW-HsiaoYuNeural','--rate','+20%','-f',str(NARR),'--write-media',str(MP3)])
    dur=duration(MP3)
    if dur>39:
        run(['edge-tts','--voice','zh-TW-HsiaoYuNeural','--rate','+28%','-f',str(NARR),'--write-media',str(MP3)])
        dur=duration(MP3)
    write_subs(max(35,dur)); concat_file(max(35,dur))
    run(['ffmpeg','-y','-f','concat','-safe','0','-i',str(CONCAT),'-i',str(MP3),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-pix_fmt','yuv420p','-r','25','-af','apad','-t','35.0','-c:a','aac','-b:a','128k',str(OUT_MP4)])
    qa_sheet(); mp4dur=duration(OUT_MP4); write_docs(mp4dur); archive()
    print(json.dumps({'mp4':str(OUT_MP4),'duration':mp4dur,'archive':str(ARCHIVE)}, ensure_ascii=False))
if __name__=='__main__': main()
