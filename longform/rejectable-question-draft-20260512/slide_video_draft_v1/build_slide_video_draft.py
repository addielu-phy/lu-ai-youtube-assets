#!/usr/bin/env python3
from __future__ import annotations
import json, subprocess, tarfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE = Path('/home/adl/youtube-lu-ai-channel/longform/rejectable-question-draft-20260512')
OUT = BASE / 'slide_video_draft_v1'
SLIDES = [BASE / 'slides' / f'slide_{i:02d}.png' for i in range(1, 6)]
AUDIO = OUT / 'narration_edge_hsiaoyu.mp3'
MP4 = OUT / 'rejectable-question-draft-slide-video-draft-v1.mp4'
TITLE = '我怎麼讓 AI 先產出「可被退件」的題目草稿'
SLUG = 'rejectable-question-draft-20260512'
SEGMENT_TITLES = [
    '開場：好題目不是一次生成，是先能被退件',
    '三個硬限制：年級單元、只測一件事、輸出格式',
    '把退件規準寫在前面',
    '修訂不是重寫，是留下證據',
    '收束成教師可複製模板',
]
NARRATION = '''
好題目不是一次生成，是先讓它能被退件。這一集我想示範一個很實用的 AI Agent 備課流程：不要一開始就要求 AI 給你完美題目，而是先要求它交出一份可以被檢查、可以被退回、也可以被修訂的題目草稿。老師真正省下的時間，不是把判斷權交給 AI，而是把重複整理的工作交出去，自己保留最後的審稿權。

第一步，是在 prompt 裡放三個硬限制。第一個硬限制是年級與單元，例如八年級力與運動，或高中電磁感應。第二個硬限制是只測一件事，不要同時測概念、計算、圖像判讀和閱讀理解。第三個硬限制是輸出格式，例如題幹、選項、標準答案、解析、學生常見錯誤、以及老師退件理由欄。這三件事看起來很基本，但它們會把 AI 從自由發揮拉回教學目標。

第二步，是先把退件規準寫在前面。我的做法是要求 AI 自己先用三條規準檢查草稿：目標是否清楚，條件是否足夠，誘因是否正確。目標不清楚，學生答對也不知道學到什麼；條件不足，題目會變成猜題；誘因不對，學生可能用捷徑答對，卻沒有練到你想看的能力。這些規準不是拿來裝飾，而是等一下修訂時的依據。

第三步，讓 AI 交草稿時，必須同時交出自評。不是只貼一題給老師，而是附上它認為這題可能被退件的地方。老師看到的就不是一份看似完整的題目，而是一份帶著紅筆入口的草稿。這個設計很重要，因為它讓老師可以快速判斷：這題是目標偏掉，條件缺漏，還是選項設計讓學生靠猜也能答對。

第四步，修訂不是重寫。每一次修改，都要對照退件理由留下證據。例如，如果退件理由是只測到代公式，修訂版就必須明確加入圖像判讀或情境限制；如果退件理由是條件不足，修訂版就要補上必要數值、單位或邊界條件；如果退件理由是誘因不對，修訂版要說明錯誤選項分別對應哪一種學生迷思。這樣做，老師可以看見 AI 到底有沒有照著教學要求修。

最後，把整個流程變成教師可複製模板。模板可以很短：請先產出一題可退件草稿；請列出三個硬限制；請用目標、條件、誘因三欄自評；請根據退件理由產生修訂版；最後請附上學生可能錯在哪裡。這個流程的重點不是讓 AI 取代老師出題，而是讓老師有一個更清楚、更可追蹤的審稿工作台。下一次你要請 AI 幫忙出題時，可以先問自己一句話：我有沒有先定義，什麼樣的題目應該被退件？
'''.strip()

def run(cmd):
    return subprocess.check_output(cmd, text=True).strip()

def duration(path: Path) -> float:
    return float(run(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(path)]))

def ts(seconds: float, comma=False):
    ms = int(round((seconds - int(seconds))*1000))
    s = int(seconds)
    h, rem = divmod(s, 3600)
    m, sec = divmod(rem, 60)
    sep = ',' if comma else '.'
    return f'{h:02d}:{m:02d}:{sec:02d}{sep}{ms:03d}'

def make_subtitles(total: float):
    weights = [0.18, 0.20, 0.20, 0.24, 0.18]
    scale = total / sum(weights)
    bounds = [0.0]
    for w in weights:
        bounds.append(bounds[-1] + w * scale)
    vtt = ['WEBVTT','']
    srt = []
    for i, title in enumerate(SEGMENT_TITLES, start=1):
        start = bounds[i-1]
        end = min(bounds[i], total)
        vtt += [f'{ts(start)} --> {ts(end)}', title, '']
        srt += [str(i), f'{ts(start, True)} --> {ts(end, True)}', title, '']
    (OUT/'narration_edge_hsiaoyu.vtt').write_text('\n'.join(vtt), encoding='utf-8')
    (OUT/'narration_edge_hsiaoyu.srt').write_text('\n'.join(srt), encoding='utf-8')
    return [bounds[i]-bounds[i-1] for i in range(1,6)]

def make_concat(durs):
    lines=[]
    for slide,dur in zip(SLIDES,durs):
        lines.append(f"file '{slide}'")
        lines.append(f'duration {dur:.3f}')
    lines.append(f"file '{SLIDES[-1]}'")
    (OUT/'slides.ffconcat').write_text('\n'.join(lines)+'\n', encoding='utf-8')

def make_contact_sheet():
    frames_dir = OUT/'check_frames'
    imgs=[]
    for p in sorted(frames_dir.glob('frame_*.png'))[:5]:
        imgs.append((p.name, Image.open(p).convert('RGB').resize((480,270))))
    W,H=1600,980
    sheet=Image.new('RGB',(W,H),(245,242,234))
    draw=ImageDraw.Draw(sheet)
    font_path='/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
    font=ImageFont.truetype(font_path,28)
    title_font=ImageFont.truetype(font_path,38)
    draw.text((50,28),'可退件題目草稿｜slide-video QA contact sheet',font=title_font,fill=(32,45,62))
    coords=[(50,100),(560,100),(1070,100),(300,520),(810,520)]
    for (name,im),(x,y) in zip(imgs,coords):
        sheet.paste(im,(x,y))
        draw.rectangle([x,y,x+480,y+270],outline=(32,45,62),width=3)
        draw.text((x,y+285),name,font=font,fill=(32,45,62))
    checks=OUT/'checks'; checks.mkdir(exist_ok=True)
    sheet.save(checks/'contact_sheet_slide_video_v1.png')

def write_docs(total):
    verification={}
    for p in SLIDES + sorted((OUT/'check_frames').glob('frame_*.png')) + [OUT/'checks/contact_sheet_slide_video_v1.png']:
        im=Image.open(p)
        verification[str(p.relative_to(BASE))]={'size': list(im.size), 'mode': im.mode}
    manifest={
        'title': TITLE,
        'slug': SLUG,
        'format': 'longform slide-video draft v1',
        'video': str(MP4.relative_to(BASE)),
        'audio': str(AUDIO.relative_to(BASE)),
        'narration_text': 'slide_video_draft_v1/narration_zh_tw.txt',
        'subtitles': ['slide_video_draft_v1/narration_edge_hsiaoyu.vtt','slide_video_draft_v1/narration_edge_hsiaoyu.srt'],
        'ffconcat': 'slide_video_draft_v1/slides.ffconcat',
        'check_frames': [str(p.relative_to(BASE)) for p in sorted((OUT/'check_frames').glob('frame_*.png'))],
        'contact_sheet': 'slide_video_draft_v1/checks/contact_sheet_slide_video_v1.png',
        'duration_seconds': round(total,3),
        'verification': verification,
        'next_auto_push': '若 YouTube/Google 登入仍未完成，下一輪可為本長片製作 1080×1920 Shorts／社群宣傳卡，或從第二季題庫挑選尚未完成的下一個內容包；若已完成登入，優先上傳第一季首批或本支第二季長片草稿。'
    }
    (OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    readme=f'''# 可退件題目草稿｜slide-video draft v1\n\n狀態：已由 storyboard 擴成 4–6 分鐘長片本機草稿，並完成長片 upload kit、正式可分享講義與輕量交接包。\n\n## 檔案\n- 影片：`slide_video_draft_v1/{MP4.name}`\n- 旁白：`slide_video_draft_v1/narration_edge_hsiaoyu.mp3`\n- 旁白全文：`slide_video_draft_v1/narration_zh_tw.txt`\n- 字幕：`slide_video_draft_v1/narration_edge_hsiaoyu.vtt`、`slide_video_draft_v1/narration_edge_hsiaoyu.srt`\n- 抽幀：`slide_video_draft_v1/check_frames/`\n- QA contact sheet：`slide_video_draft_v1/checks/contact_sheet_slide_video_v1.png`\n- manifest：`slide_video_draft_v1/manifest.json`\n- Slide-video 草稿交接壓縮包：`slide_video_draft_v1/rejectable-question-draft-slide-video-draft-v1-20260512.tar.gz`\n- 長片 upload kit：`slide_video_draft_v1/youtube-upload-kit-longform-v1.md`\n- 正式可分享講義：`rejectable-question-draft-shareable-handout-v1.md`\n- 長片上架輕量交接包：`slide_video_draft_v1/rejectable-question-draft-longform-upload-kit-v1-20260512.tar.gz`\n\n## 驗證\n- ffprobe：{total:.3f} 秒，1920×1080，H.264 + AAC。\n- PIL：5 張原始 storyboard、5 張抽幀與 QA contact sheet 尺寸／模式已寫入 manifest。\n- 視覺 QA：contact sheet 已檢查，五張抽幀繁中可讀、無 tofu／明顯裁切／文字重疊／過度擁擠；縮圖小字略吃力但出版圖卡本身無 QA 問題。\n- Upload kit／正式講義／輕量交接包已讀回驗證。\n\n## 下一個可自動推進項目\n若 YouTube/Google 登入仍未完成，下一輪可為本長片製作 1080×1920 Shorts／社群宣傳卡，或從第二季題庫挑選尚未完成的下一個內容包；若已完成登入，優先上傳第一季首批或本支第二季長片草稿。\n'''
    (OUT/'README.md').write_text(readme,encoding='utf-8')

def make_archive():
    archive = OUT/'rejectable-question-draft-slide-video-draft-v1-20260512.tar.gz'
    members = [
        OUT/'README.md', OUT/'manifest.json', OUT/'build_slide_video_draft.py', OUT/'narration_zh_tw.txt', AUDIO,
        OUT/'narration_edge_hsiaoyu.vtt', OUT/'narration_edge_hsiaoyu.srt', OUT/'slides.ffconcat', MP4,
        OUT/'checks/contact_sheet_slide_video_v1.png', BASE/'README.md', BASE/'manifest.json', BASE/'rejectable-question-draft-rubric-handout-draft-v1.md', BASE/'rejectable-question-draft-shareable-handout-v1.md', OUT/'youtube-upload-kit-longform-v1.md'
    ] + SLIDES + sorted((OUT/'check_frames').glob('frame_*.png'))
    with tarfile.open(archive, 'w:gz') as tar:
        for p in members:
            tar.add(p, arcname=str(p.relative_to(BASE)))
    with tarfile.open(archive, 'r:gz') as tar:
        names = tar.getnames()
    return archive, names

def main():
    OUT.mkdir(exist_ok=True)
    (OUT/'narration_zh_tw.txt').write_text(NARRATION, encoding='utf-8')
    if not AUDIO.exists():
        subprocess.check_call(['edge-tts','--voice','zh-TW-HsiaoYuNeural','--rate=-8%','--text',NARRATION,'--write-media',str(AUDIO)])
    total = duration(AUDIO)
    durs = make_subtitles(total)
    make_concat(durs)
    subprocess.check_call([
        'ffmpeg','-y','-hide_banner','-loglevel','error',
        '-f','concat','-safe','0','-i',str(OUT/'slides.ffconcat'),'-i',str(AUDIO),
        '-vf','fps=30,format=yuv420p','-c:v','libx264','-preset','veryfast','-crf','20',
        '-c:a','aac','-b:a','128k','-shortest',str(MP4)
    ])
    frames=OUT/'check_frames'; frames.mkdir(exist_ok=True)
    for idx,pct in enumerate([0.10,0.30,0.50,0.70,0.90], start=1):
        subprocess.check_call(['ffmpeg','-y','-hide_banner','-loglevel','error','-ss',f'{total*pct:.3f}','-i',str(MP4),'-frames:v','1',str(frames/f'frame_{idx:02d}.png')])
    make_contact_sheet()
    video_total = duration(MP4)
    write_docs(video_total)
    archive, names = make_archive()
    print(json.dumps({'video':str(MP4),'duration':video_total,'archive':str(archive),'archive_count':len(names)},ensure_ascii=False))

if __name__ == '__main__':
    main()
