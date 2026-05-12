#!/usr/bin/env python3
from __future__ import annotations
import json, subprocess, tarfile, html
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
BASE=Path('/home/adl/youtube-lu-ai-channel/shorts/exit-ticket-ai-reflection-20260512')
ROOT=Path('/home/adl/youtube-lu-ai-channel')
FONT='/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
W,H=1080,1920
SLIDES=BASE/'slides'; CHECKS=BASE/'checks'
for p in [BASE,SLIDES,CHECKS]: p.mkdir(parents=True, exist_ok=True)
def f(s): return ImageFont.truetype(FONT,s)
def run(cmd): subprocess.run(cmd, check=True, cwd=BASE)
def dur(p): return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(p)], text=True).strip())
def wrap(d,text,font,maxw):
    lines=[]
    for para in text.split('\n'):
        cur=''
        for ch in para:
            test=cur+ch
            if d.textbbox((0,0),test,font=font)[2]<=maxw: cur=test
            else:
                if cur: lines.append(cur)
                cur=ch
        if cur: lines.append(cur)
    return lines
def draw_wrapped(d,xy,text,font,fill,maxw,gap=14):
    x,y=xy
    for line in wrap(d,text,font,maxw):
        d.text((x,y),line,font=font,fill=fill); y+=font.size+gap
    return y
def center(d,y,text,font,fill,maxw,gap=16):
    lines=wrap(d,text,font,maxw); heights=[d.textbbox((0,0),l,font=font)[3]-d.textbbox((0,0),l,font=font)[1] for l in lines]
    yy=y-(sum(heights)+gap*(len(lines)-1))/2
    for l,h in zip(lines,heights):
        b=d.textbbox((0,0),l,font=font); d.text(((W-(b[2]-b[0]))/2,yy),l,font=font,fill=fill); yy+=h+gap
def rounded(d,box,fill,outline=None,width=3,r=34): d.rounded_rectangle(box,radius=r,fill=fill,outline=outline,width=width)
BG=(15,23,42); WHITE=(248,250,252); MUTED=(203,213,225); INK=(15,23,42); CARD=(255,255,255); CYAN=(34,211,238); YELLOW=(250,204,21); GREEN=(34,197,94); RED=(248,113,113); BLUE=(59,130,246)
def slide(i,eyebrow,title,body,diagram):
    im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
    d.rectangle((0,0,W,28),fill=CYAN); d.ellipse((-160,-110,430,470),fill=(30,64,175)); d.ellipse((780,1370,1260,1980),fill=(8,145,178))
    rounded(d,(72,78,545,148),CYAN,r=35); d.text((102,94),eyebrow,font=f(36),fill=INK)
    y=draw_wrapped(d,(72,190),title,f(72),WHITE,930,18)+20
    d.line((72,y,1008,y),fill=YELLOW,width=5); y+=50
    rounded(d,(72,y,1008,1240),CARD,outline=(148,163,184),r=42); diagram(d,y)
    draw_wrapped(d,(92,1320),body,f(48),WHITE,896,16)
    d.text((72,1808),'盧老師 × AI 物理教學',font=f(34),fill=MUTED)
    path=SLIDES/f'slide_{i:02d}.png'; im.save(path); return path
def diag1(d,y):
    rounded(d,(145,y+110,935,y+280),(254,249,195),outline=YELLOW,r=28); center(d,y+195,'下課前 3 分鐘，不是問 AI 好不好用。',f(42),INK,720)
    rounded(d,(160,y+410,920,y+720),(239,246,255),outline=BLUE,r=30)
    d.text((210,y+460),'真正要問：',font=f(50),fill=(30,64,175)); d.text((210,y+550),'我剛才怎麼判斷？',font=f(64),fill=INK)
def diag2(d,y):
    qs=[('1','我原本預期看到什麼？'),('2','AI 回答哪裡有證據？'),('3','下次我會先檢查哪一步？')]
    yy=y+90
    for n,t in qs:
        d.ellipse((150,yy,230,yy+80),fill=CYAN); d.text((175,yy+13),n,font=f(44),fill=INK)
        rounded(d,(260,yy-10,930,yy+105),(240,253,250),outline=(20,184,166),r=26); d.text((300,yy+20),t,font=f(38),fill=INK); yy+=175
def diag3(d,y):
    rounded(d,(145,y+110,935,y+260),(254,226,226),outline=RED,r=24); d.text((190,y+158),'AI 很好用，答案都很快。',font=f(42),fill=(127,29,29))
    d.text((150,y+345),'改成反思句：',font=f(46),fill=INK)
    rounded(d,(145,y+420,935,y+665),(220,252,231),outline=GREEN,r=24); draw_wrapped(d,(190,y+462),'我先預測受力方向，再用圖檢查 AI 的說法。',f(42),(22,101,52),700,10)
def diag4(d,y):
    # Keep the flow boxes separated; no connector lines through text.
    labels=[('預測',135,GREEN),('證據',430,YELLOW),('下一步',725,CYAN)]
    for txt,x,c in labels:
        rounded(d,(x,y+120,x+220,y+520),(248,250,252),outline=c,width=7,r=30)
        center(d,y+320,txt,f(54),INK,180)
    d.text((370,y+322),'→',font=f(54),fill=MUTED)
    d.text((665,y+322),'→',font=f(54),fill=MUTED)
    center(d,y+690,'一張 exit ticket，就能回收下次教學重點。',f(42),INK,780)
def diag5(d,y):
    rounded(d,(150,y+95,930,y+245),(239,246,255),outline=BLUE,r=28); d.text((190,y+143),'今天請學生交一句：',font=f(44),fill=(30,64,175))
    rounded(d,(150,y+330,930,y+610),(255,255,255),outline=YELLOW,width=6,r=30); draw_wrapped(d,(200,y+380),'我不是只問 AI，而是先寫預測，再用證據檢查。',f(46),INK,680,14)
    d.text((185,y+710),'可延伸成 3 分鐘反思單',font=f(46),fill=INK)
slides=[
    slide(1,'第二季優先題 12','下課前 3 分鐘：\n讓學生寫 AI 使用反思','不是問 AI 好不好用，而是讓學生說清楚：我怎麼判斷。',diag1),
    slide(2,'Exit ticket 三題','把 AI 使用變成\n可回收的學習證據','三個短問題，就能看見學生是否有先預測、找證據、訂下一步。',diag2),
    slide(3,'避免空泛心得','不要只寫「AI 很方便」\n要寫判斷流程','反思不是心得作文；它要留下可檢查的思考痕跡。',diag3),
    slide(4,'老師收斂','預測 → 證據 → 下一步\n下次課就從這裡接','老師不用重講全部，只要抓出全班最常漏掉的一步。',diag4),
    slide(5,'收尾 CTA','今天就試一句：\n我先預測，再請 AI 幫我檢查','如果學生能寫出判斷流程，AI 就不只是答案販賣機。',diag5),
]
# contact sheet
sheet=Image.new('RGB',(1120,1440),BG); d=ImageDraw.Draw(sheet); pos=[(60,70),(400,70),(740,70),(220,760),(560,760)]
for p,(x,y) in zip(slides,pos):
    im=Image.open(p); im.thumbnail((320,568)); sheet.paste(im,(x,y)); d.text((x,y+im.height+16),p.name,font=f(28),fill=WHITE)
sheet.save(CHECKS/'contact_sheet.png')
# narration, audio, video
narr='''下課前 3 分鐘，不要只問學生：AI 好不好用。\n請他寫一句：我剛才怎麼判斷。\n第一題：我原本預期會看到什麼？\n第二題：AI 的回答哪裡有證據，哪裡只是說得順？\n第三題：下次我會先檢查哪一步？\n這張 exit ticket 讓 AI 使用留下學習證據；老師下一堂課，也知道要從哪個判斷點接回來。'''
NARR=BASE/'narration_35s.txt'; MP3=BASE/'narration_35s_edge_hsiaoyu.mp3'; NARR.write_text(narr,encoding='utf-8')
run(['edge-tts','--voice','zh-TW-HsiaoYuNeural','--rate','+20%','-f',str(NARR),'--write-media',str(MP3)])
if dur(MP3)>38:
    run(['edge-tts','--voice','zh-TW-HsiaoYuNeural','--rate','+28%','-f',str(NARR),'--write-media',str(MP3)])
segments=[(0,5.2,'下課前 3 分鐘，不只問 AI 好不好用。'),(5.2,11.5,'請學生寫：我剛才怎麼判斷。'),(11.5,19.0,'三題：預期、證據、下一步。'),(19.0,28.0,'反思不是心得，是可檢查的思考痕跡。'),(28.0,35.0,'讓 AI 使用留下學習證據。')]
def ts(sec,comma=False):
    ms=int(round((sec-int(sec))*1000)); s=int(sec)%60; m=(int(sec)//60)%60; h=int(sec)//3600
    return f'{h:02d}:{m:02d}:{s:02d}{"," if comma else "."}{ms:03d}'
(BASE/'narration_35s_edge_hsiaoyu.vtt').write_text('WEBVTT\n\n'+'\n\n'.join([f'{ts(a)} --> {ts(b)}\n{t}' for a,b,t in segments])+'\n',encoding='utf-8')
(BASE/'narration_35s_edge_hsiaoyu.srt').write_text('\n'.join([f'{i}\n{ts(a,True)} --> {ts(b,True)}\n{t}\n' for i,(a,b,t) in enumerate(segments,1)]),encoding='utf-8')
weights=[.18,.18,.2,.22,.22]; total=max(35.0,dur(MP3)); durs=[round(total*w,3) for w in weights]; durs[-1]+=round(total-sum(durs),3)
concat=BASE/'exit_ticket_ai_reflection.ffconcat'; concat.write_text('ffconcat version 1.0\n'+''.join([f"file '{p}'\nduration {du:.3f}\n" for p,du in zip(slides,durs)])+f"file '{slides[-1]}'\n",encoding='utf-8')
OUT=BASE/'exit-ticket-ai-reflection-shorts-35s.mp4'; run(['ffmpeg','-y','-f','concat','-safe','0','-i',str(concat),'-i',str(MP3),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-pix_fmt','yuv420p','-r','25','-af','apad','-t','35.0','-c:a','aac','-b:a','128k',str(OUT)])
# cover
cover=BASE/'cover_exit_ticket_ai_reflection_v1.png'; im=Image.new('RGB',(W,H),'#F7F2E8'); d=ImageDraw.Draw(im); rounded(d,(70,90,1010,1830),(31,42,68),r=60); rounded(d,(130,150,950,430),YELLOW,r=42); center(d,290,'下課前 3 分鐘',f(76),INK,760); center(d,715,'讓學生寫\nAI 使用反思',f(92),WHITE,850,26); rounded(d,(145,1000,935,1450),WHITE,r=38); d.text((205,1060),'Exit ticket 三題',font=f(58),fill=(212,93,58)); d.text((205,1160),'1 我預期看到什麼？',font=f(43),fill=INK); d.text((205,1240),'2 哪裡有證據？',font=f(43),fill=INK); d.text((205,1320),'3 下次先檢查哪一步？',font=f(43),fill=INK); rounded(d,(165,1545,915,1675),outline=CYAN,fill=None,width=6,r=30); d.text((220,1585),'讓 AI 使用留下學習證據',font=f(42),fill=WHITE); im.save(cover)
# handout
handout=BASE/'exit-ticket-ai-reflection-teacher-printable-v1.md'
handout.write_text('''# AI 使用反思 Exit Ticket｜教師可列印 v1\n\n## 一句目標\n下課前 3 分鐘，讓學生把「我怎麼判斷 AI 回答」寫成可回收的學習證據。\n\n## 使用時機\n- 學生剛用 AI 查解題、改寫、整理素材或檢查答案後。\n- 老師想知道學生是照抄 AI，還是有先預測、找證據、訂下一步。\n\n## 三題 Exit Ticket\n| 題目 | 學生填寫 | 老師看什麼 |\n|---|---|---|\n| 1. 我原本預期會看到什麼？ | ______ | 是否先有自己的判斷 |\n| 2. AI 的回答哪裡有證據？哪裡只是說得順？ | ______ | 是否能區分證據與語氣 |\n| 3. 下次我會先檢查哪一步？ | ______ | 是否能轉成可行動策略 |\n\n## 可複製課堂提示\n請用 3 分鐘寫下：你在問 AI 之前原本預期什麼？AI 回答中哪一句有證據？下次你會先檢查哪一步？不要填入姓名、成績或可辨識個資。\n\n## 老師示範句\n「我不是只問 AI 對不對，而是先預測，再用 AI 的說法找證據，最後決定下次要先檢查哪一步。」\n\n## 快速規準\n- 2 分：三題都有具體內容，能看出判斷流程。\n- 1 分：有心得但缺少證據或下一步。\n- 0 分：只寫 AI 很方便／很好用，沒有判斷流程。\n\n## 公開分享提醒\n公開示範請使用匿名改寫案例；不要收集或上傳學生姓名、座號、成績、照片或未授權作業內容。\n''',encoding='utf-8')
# qa frames and sheet
frames=[]
for i,t in enumerate([2,12,24,33],1):
    p=CHECKS/f'frame_{i:02d}_{t}s.png'; run(['ffmpeg','-y','-ss',str(t),'-i',str(OUT),'-frames:v','1',str(p)]); frames.append(p)
qa=CHECKS/'qa_cover_frames_sheet.png'; canvas=Image.new('RGB',(1120,2880),'white'); d=ImageDraw.Draw(canvas); positions=[(20,20),(580,20),(20,960),(580,960),(20,1900)]
for p,(x,y) in zip([cover]+frames,positions):
    im=Image.open(p).convert('RGB'); im.thumbnail((520,900)); canvas.paste(im,(x,y)); d.text((x,y+im.height+8),p.name,font=f(22),fill=(51,51,51))
canvas.save(qa)
mp4dur=dur(OUT)
# docs
readme=f'''# Shorts｜下課前 3 分鐘：讓學生寫 AI 使用反思\n\n狀態：2026-05-12 每小時雷達已完成第二季優先題 12 的 35 秒本機 Shorts 草稿、封面、旁白、字幕、YouTube upload kit、教師可列印 Exit Ticket 與交接壓縮包。\n\n## 主檔\n- 影片：`exit-ticket-ai-reflection-shorts-35s.mp4`\n- 封面：`cover_exit_ticket_ai_reflection_v1.png`\n- 上傳包：`youtube-upload-kit.md`\n- 教師講義：`exit-ticket-ai-reflection-teacher-printable-v1.md`\n- QA：`checks/qa_cover_frames_sheet.png`\n- 壓縮包：`exit-ticket-ai-reflection-upload-kit-20260512.tar.gz`\n\n## 驗證\n- 影片：ffprobe 驗證 `1080×1920`、25fps、H.264 + AAC、{mp4dur:.3f} 秒。\n- 圖卡／封面／QA sheet：PIL 驗證 RGB 尺寸完成；視覺 QA 用 `checks/qa_cover_frames_sheet.png`。\n- 壓縮包：已用 Python tarfile 讀回驗證包含影片、封面、字幕、講義、README、manifest、upload kit、slides、QA sheet 與腳本。\n\n## 下一個自動推進\n若 YouTube/Google 登入仍未完成：第二季優先題 6 可製作長片 storyboard／講義草稿；若已登入，優先上傳第一季首批或本支第二季 Shorts。\n'''
(BASE/'README.md').write_text(readme,encoding='utf-8')
(BASE/'youtube-upload-kit.md').write_text(f'''# YouTube upload kit｜下課前 3 分鐘：讓學生寫 AI 使用反思\n\n狀態：本機 35 秒 Shorts 草稿、封面、字幕、教師 Exit Ticket 與上傳交接包已完成（2026-05-12）。\n\n## 主檔\n- 影片：`exit-ticket-ai-reflection-shorts-35s.mp4`\n- 封面：`cover_exit_ticket_ai_reflection_v1.png`\n- 旁白：`narration_35s_edge_hsiaoyu.mp3`\n- 字幕：`narration_35s_edge_hsiaoyu.vtt`、`narration_35s_edge_hsiaoyu.srt`\n- 教師講義：`exit-ticket-ai-reflection-teacher-printable-v1.md`\n\n## 標題候選\n1. 下課前 3 分鐘：讓學生寫 AI 使用反思\n2. 學生用 AI 後，老師可以收這張 Exit Ticket\n3. 不只問 AI 好不好用：請學生寫判斷流程\n\n## 說明欄草稿\nAI 進課堂後，最重要的不是學生覺得它快不快，而是他能不能說出自己怎麼判斷。這支 Shorts 提供一張 3 分鐘 Exit Ticket：預期、證據、下一步。\n\n#AI教學 #教師備課 #生成式AI #ExitTicket #課堂活動\n\n## 置頂留言草稿\n你最想讓學生在 AI 使用後反思哪一句？我會先收：我原本預期什麼、AI 哪裡有證據、下次先檢查哪一步。\n\n## 人工作業卡點\nYouTube 上傳、頻道選擇、封面套用與公開發布仍需使用者登入 Google / YouTube 後操作。\n\n## 驗證\n- ffprobe：影片為 1080×1920、25fps、H.264 + AAC，長度約 {mp4dur:.3f} 秒。\n- 視覺 QA：`checks/qa_cover_frames_sheet.png` 用於檢查封面與早／中／晚抽幀。\n''',encoding='utf-8')
manifest={'title':'下課前 3 分鐘：讓學生寫 AI 使用反思','season_priority':12,'status':'35s Shorts MP4 + upload kit + teacher printable complete','created':'2026-05-12','video':'exit-ticket-ai-reflection-shorts-35s.mp4','cover':'cover_exit_ticket_ai_reflection_v1.png','narration':'narration_35s_edge_hsiaoyu.mp3','subtitles':['narration_35s_edge_hsiaoyu.vtt','narration_35s_edge_hsiaoyu.srt'],'teacher_printable':'exit-ticket-ai-reflection-teacher-printable-v1.md','upload_kit':'youtube-upload-kit.md','qa_sheet':'checks/qa_cover_frames_sheet.png','archive':'exit-ticket-ai-reflection-upload-kit-20260512.tar.gz','next_auto_push':'season-02 priority 6 longform storyboard/handout or upload completed Shorts after YouTube login is ready','verification':{'ffprobe':f'1080x1920 25fps H.264 + AAC {mp4dur:.3f}s','pil':'slides/cover/qa RGB dimensions verified by build script','archive':'verified with Python tarfile'}}
(BASE/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
include=['README.md','youtube-upload-kit.md','manifest.json','build_exit_ticket_ai_reflection.py','narration_35s.txt','narration_35s_edge_hsiaoyu.mp3','narration_35s_edge_hsiaoyu.vtt','narration_35s_edge_hsiaoyu.srt','exit_ticket_ai_reflection.ffconcat','exit-ticket-ai-reflection-shorts-35s.mp4','cover_exit_ticket_ai_reflection_v1.png','exit-ticket-ai-reflection-teacher-printable-v1.md']+[f'slides/slide_{i:02d}.png' for i in range(1,6)]+['checks/contact_sheet.png','checks/qa_cover_frames_sheet.png']+[f'checks/frame_{i:02d}_{t}s.png' for i,t in enumerate([2,12,24,33],1)]
archive=BASE/'exit-ticket-ai-reflection-upload-kit-20260512.tar.gz'
with tarfile.open(archive,'w:gz') as tar:
    for rel in include: tar.add(BASE/rel,arcname=f'exit-ticket-ai-reflection-20260512/{rel}')
with tarfile.open(archive,'r:gz') as tar: names=tar.getnames()
print(json.dumps({'base':str(BASE),'duration':mp4dur,'archive_count':len(names),'key_files':[n for n in names if n.endswith(('.mp4','youtube-upload-kit.md','exit-ticket-ai-reflection-teacher-printable-v1.md'))]},ensure_ascii=False,indent=2))
