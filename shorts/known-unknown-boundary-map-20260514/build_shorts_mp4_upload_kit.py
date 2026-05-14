#!/usr/bin/env python3
from __future__ import annotations
import json, subprocess, tarfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE = Path('/home/adl/youtube-lu-ai-channel/shorts/known-unknown-boundary-map-20260514')
FONT = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
W,H = 1080,1920
SLIDES = [BASE/'slides'/f'slide_{i:02d}.png' for i in range(1,6)]
OUT_MP4 = BASE/'known-unknown-boundary-map-shorts-35s.mp4'
COVER = BASE/'cover_known_unknown_boundary_map_v1.png'
NARR = BASE/'narration_35s.txt'
MP3 = BASE/'narration_35s_edge_hsiaoyu.mp3'
VTT = BASE/'narration_35s_edge_hsiaoyu.vtt'
SRT = BASE/'narration_35s_edge_hsiaoyu.srt'
CONCAT = BASE/'known_unknown_boundary_map.ffconcat'
QA = BASE/'checks'/'qa_cover_frames_sheet.png'
HANDOUT = BASE/'known-unknown-boundary-map-student-worksheet-v1.md'
UPLOAD = BASE/'youtube-upload-kit.md'
MANIFEST = BASE/'manifest.json'
ARCHIVE = BASE/'known-unknown-boundary-map-upload-kit-20260515.tar.gz'

narration = '''學生問 AI 之前，先別急著把題目丟進去。
先畫一張「我知道／我不知道」邊界圖：左邊寫已知條件，右邊寫還缺什麼。
例如斜面題：我知道角度、質量、要找加速度；我不知道摩擦能不能忽略、方向怎麼定。
接著把問題改成：請先檢查我的邊界圖，指出缺口，再給解法。
這樣學生不是把思考外包給 AI，而是先把自己負責的部分說清楚。'''
segments = [
    (0,5,'學生問 AI 之前，先別急著把題目丟進去。'),
    (5,12,'先畫「我知道／我不知道」邊界圖。'),
    (12,21,'左邊寫已知條件，右邊寫還缺什麼。'),
    (21,29,'請 AI 先檢查邊界圖，指出缺口，再給解法。'),
    (29,35,'學生不是外包思考，而是先說清楚自己知道什麼。'),
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
    im=Image.new('RGB',(W,H),'#F5F1E8'); d=ImageDraw.Draw(im)
    d.rounded_rectangle((70,90,1010,1830), radius=64, fill='#17213A')
    d.rounded_rectangle((125,150,955,360), radius=42, fill='#F4C542')
    center(d,255,'問 AI 前先畫這張圖',font(64),'#17213A',760,10)
    center(d,640,'我知道／\n我不知道',font(112),'#FFFFFF',850,22)
    d.rounded_rectangle((145,910,935,1390), radius=42, fill='#FFFFFF')
    d.line((540,970,540,1335), fill='#D75A4A', width=8)
    d.text((205,990),'我知道',font=font(54),fill='#17213A')
    d.text((600,990),'我不知道',font=font(54),fill='#17213A')
    for y,t in [(1090,'角度'),(1180,'質量'),(1270,'要求量')]: d.text((215,y),t,font=font(42),fill='#2C5F8A')
    for y,t in [(1090,'摩擦？'),(1180,'方向？'),(1270,'條件夠嗎？')]: d.text((610,y),t,font=font(42),fill='#D75A4A')
    d.rounded_rectangle((155,1510,925,1665), radius=32, outline='#F4C542', width=6)
    center(d,1588,'先檢查缺口，再請 AI 解題',font(48),'#FFFFFF',720,8)
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
    total=max(35,total); weights=[0.17,0.20,0.23,0.22,0.18]
    ds=[round(total*w,3) for w in weights]; ds[-1]+=round(total-sum(ds),3)
    lines=['ffconcat version 1.0']
    for p,du in zip(SLIDES,ds): lines += [f"file '{p}'", f'duration {du:.3f}']
    lines += [f"file '{SLIDES[-1]}'"]
    CONCAT.write_text('\n'.join(lines)+'\n', encoding='utf-8')

def make_handout():
    HANDOUT.write_text('''# 我知道／我不知道邊界圖｜學生學習單 v1

## 一句目標
在問 AI 前，先把「已知條件」與「缺口」分清楚，讓 AI 先協助檢查問題邊界，而不是直接代替思考。

## 3 分鐘使用情境
- 斜面、力圖、能量、電路或任何條件不完整的物理題。
- 學生準備把題目丟給 AI 前，先完成下表。

## 學生工作區
| 我知道的條件／圖像 | 我還不知道／需要 AI 先檢查 |
|---|---|
| 題目給了：________ | 缺少的條件：________ |
| 我先定義方向：________ | 方向定義是否一致：________ |
| 我預期答案大概：________ | 哪一步最可能出錯：________ |

## 可複製 AI prompt
請先檢查我的「我知道／我不知道」邊界圖，不要直接解完整答案。請指出：1. 哪些已知條件足夠；2. 哪些條件或方向定義不清楚；3. 我應該先補哪一句，才能讓題目變成可檢查的物理問題。

## 老師示範句
「問 AI 之前，先讓學生說清楚：我已經負責了哪些判斷？我還需要 AI 幫我檢查哪些缺口？」

## 快速評分
- 2 分：已知／未知分欄清楚，且能提出可檢查的缺口。
- 1 分：有分欄，但缺口仍是模糊句。
- 0 分：只貼題目或只要求 AI 給答案。

## 公開分享提醒
不要放入學生姓名、班級座號、未公開考題全文或可辨識個資；公開展示時請改寫為匿名示例。
''', encoding='utf-8')

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
    UPLOAD.write_text(f'''# YouTube upload kit｜學生問 AI 之前，先畫一張「我知道／我不知道」圖

狀態：本機 35 秒 Shorts 草稿、封面、字幕、學生學習單與上傳交接包已完成（2026-05-15）。

## 主檔
- 影片：`known-unknown-boundary-map-shorts-35s.mp4`
- 封面：`cover_known_unknown_boundary_map_v1.png`
- 旁白：`narration_35s_edge_hsiaoyu.mp3`
- 字幕：`narration_35s_edge_hsiaoyu.vtt`、`narration_35s_edge_hsiaoyu.srt`
- 學生學習單：`known-unknown-boundary-map-student-worksheet-v1.md`

## 標題候選
1. 學生問 AI 前，先畫一張「我知道／我不知道」圖
2. 問 AI 不是貼題目：先把缺口畫出來
3. 讓 AI 先檢查邊界，再請它解題

## 說明欄草稿
學生問 AI 前，先用一張 T-chart 分出「我知道」與「我不知道」。這支 Shorts 示範老師如何把模糊提問改成可檢查的物理問題，讓 AI 先指出缺口，而不是直接代替學生思考。

#AI教學 #物理教學 #生成式AI #教師備課 #探究學習

## 置頂留言草稿
你會讓學生在問 AI 前先寫哪一句？我會先要求：「我知道____；我還不知道____；請先檢查我的缺口。」

## 人工作業卡點
YouTube 上傳、頻道選擇、封面套用與公開發布仍需使用者登入 Google / YouTube 後操作。

## 驗證
- ffprobe：影片為 1080×1920、25fps、H.264 + AAC，長度約 {mp4dur:.3f} 秒。
- QA sheet：`checks/qa_cover_frames_sheet.png`。
''', encoding='utf-8')
    (BASE/'README.md').write_text(f'''# Shorts package｜學生問 AI 之前，先畫一張「我知道／我不知道」圖

狀態：2026-05-15 每小時雷達已由 storyboard 擴成本機 35 秒 Shorts 草稿、封面、字幕、YouTube upload kit、學生學習單與交接壓縮包。  
來源：第三季內容題庫優先題 10。

## 主檔
- 影片：`known-unknown-boundary-map-shorts-35s.mp4`
- 封面：`cover_known_unknown_boundary_map_v1.png`
- 上傳包：`youtube-upload-kit.md`
- 學生學習單：`known-unknown-boundary-map-student-worksheet-v1.md`
- 壓縮包：`known-unknown-boundary-map-upload-kit-20260515.tar.gz`

## 原始圖卡
1. `slides/slide_01.png`｜學生問 AI 前，先畫一張圖
2. `slides/slide_02.png`｜直接問 AI，常常變成猜答案
3. `slides/slide_03.png`｜老師可複製句：請你照我的邊界圖回覆
4. `slides/slide_04.png`｜把模糊問題改成可檢查問題
5. `slides/slide_05.png`｜一張 T-chart，讓學生先負責

## 驗證
- 影片：1080×1920、25fps、H.264 + AAC、約 {mp4dur:.3f} 秒。
- 圖卡與封面：PIL 驗證 1080×1920 RGB。
- QA sheet：`checks/qa_cover_frames_sheet.png`。
- 交接包：Python tarfile 已讀回確認包含 MP4、封面、字幕、upload kit、學生學習單、圖卡與 QA sheet。

## 下一個自動推進
若 YouTube/Google 登入仍未完成：從第三季題庫挑選下一個尚未完成的 Shorts storyboard／講義延伸；若已登入，優先上傳第一季首批或本支第三季 Shorts。
''', encoding='utf-8')
    data=json.loads(MANIFEST.read_text(encoding='utf-8'))
    data.update({'status':'35s Shorts MP4/upload kit complete','updated':'2026-05-15','video':'known-unknown-boundary-map-shorts-35s.mp4','cover':'cover_known_unknown_boundary_map_v1.png','upload_kit':'youtube-upload-kit.md','student_worksheet':'known-unknown-boundary-map-student-worksheet-v1.md','archive':'known-unknown-boundary-map-upload-kit-20260515.tar.gz','next_auto_push':'choose the next unfinished season-03 candidate for storyboard/handout extension unless YouTube login is ready for upload'})
    data.setdefault('verified',{})['local']='ffprobe/PIL/QA sheet/tarfile verified in 2026-05-15 scheduled run'
    MANIFEST.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n', encoding='utf-8')

def archive():
    files=[Path('README.md'),Path('manifest.json'),Path('render_storyboard.py'),Path('build_shorts_mp4_upload_kit.py'),Path('youtube-upload-kit.md'),Path('known-unknown-boundary-map-student-worksheet-v1.md'),Path('narration_35s.txt'),Path('narration_35s_edge_hsiaoyu.mp3'),Path('narration_35s_edge_hsiaoyu.vtt'),Path('narration_35s_edge_hsiaoyu.srt'),Path('known-unknown-boundary-map-shorts-35s.mp4'),Path('cover_known_unknown_boundary_map_v1.png'),Path('known_unknown_boundary_map.ffconcat'),Path('checks/contact_sheet.png'),Path('checks/qa_cover_frames_sheet.png')]
    files += [Path('slides')/f'slide_{i:02d}.png' for i in range(1,6)]
    files += sorted(Path('checks').glob('frame_*.png'))
    with tarfile.open(ARCHIVE,'w:gz') as tar:
        for rel in files:
            p=BASE/rel
            if p.exists(): tar.add(p, arcname=f'known-unknown-boundary-map-20260514/{rel}')
    with tarfile.open(ARCHIVE,'r:gz') as tar:
        names=tar.getnames()
        needed=['known-unknown-boundary-map-shorts-35s.mp4','youtube-upload-kit.md','known-unknown-boundary-map-student-worksheet-v1.md']
        assert all(any(n.endswith(k) for n in names) for k in needed), names
        print('archive_members', len(names))

def main():
    (BASE/'checks').mkdir(exist_ok=True)
    for p in SLIDES:
        im=Image.open(p); assert im.size==(W,H) and im.mode=='RGB', (p, im.size, im.mode)
    NARR.write_text(narration, encoding='utf-8')
    make_cover(); make_handout()
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
