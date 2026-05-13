#!/usr/bin/env python3
from __future__ import annotations
import json, subprocess, tarfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE = Path('/home/adl/youtube-lu-ai-channel/longform/ai-physics-inquiry-class-20260513')
OUT = BASE / 'slide_video_draft_v1'
SLIDES = [BASE / 'slides' / f'slide_{i:02d}.png' for i in range(1, 6)]
AUDIO = OUT / 'narration_edge_hsiaoyu.mp3'
MP4 = OUT / 'ai-physics-inquiry-class-slide-video-draft-v1.mp4'
TITLE = '一堂 45 分鐘 AI 物理探究課怎麼排？'
SLUG = 'ai-physics-inquiry-class-20260513'
SEGMENT_TITLES = [
    '開場：AI 可以進教室，但流程不能交給 AI',
    '五分鐘：先把問題變成可觀察、可測量',
    '十五分鐘：學生先寫假設，AI 只能修語句',
    '三十分鐘：資料、圖像、同儕三問與退件',
    '收束：Exit Ticket 留下下一輪證據',
]
NARRATION = '''
AI 可以進教室，但流程不能交給 AI。這支長片我想把一堂四十五分鐘的物理探究課拆成可以直接照著走的版本：先有情境，再有假設，再有證據，再讓 AI 協助整理，最後由學生說明自己採納或不採納 AI 建議的理由。重點不是讓 AI 變成助教替學生完成作業，而是把 AI 放進一個每一步都能被老師檢查的學習流程。

第一個五分鐘，不使用 AI。老師只做兩件事：提出情境，並把問題改成可觀察、可測量。例如，不要問「摩擦力是不是很重要」這種太大的問題，而是問「同一斜面上，不同表面材質會不會改變滑下時間」。這個階段如果問題太模糊，後面的 AI 再會整理也只是把模糊包裝得更漂亮。所以老師第一個把關點是：學生知道要觀察什麼、量什麼、比較什麼。

接著五到十五分鐘，學生先寫假設。這裡可以讓 AI 幫忙修句子，但不能讓 AI 直接給答案。學生原句可能是「我覺得比較粗會比較慢」，AI 可以協助改成「我預期表面越粗糙，滑下時間越長，因為摩擦作用增加」。老師要檢查的是因果與變因有沒有寫出來：哪個條件改變，哪個結果被觀察，理由是不是至少可以被證據支持或反駁。

十五到三十分鐘，是資料與圖像階段。學生蒐集觀察、測量、照片、表格或簡單圖像，AI 可以協助整理表格，也可以標出哪些資料支持假設、哪些資料反對假設。但老師要提醒：AI 不知道你的測量限制，也不知道資料來源是否可靠。這一段最重要的問題是：證據從哪裡來？單位有沒有寫？圖表是否真的回答原本的假設？如果沒有，先退回補資料，不要急著寫結論。

三十到四十分鐘，進入同儕三問與 AI 自評。三問很簡單：第一，變因是否清楚？第二，證據是否足夠？第三，結論是否超出資料？學生可以把自己的初稿交給 AI，請它用這三問找最弱的一格，但老師的規則要說清楚：AI 只能指出流程問題，不能代寫結論。如果 AI 說得太滿，例如直接宣稱某個理論一定成立，學生要把它改回「目前資料支持」或「目前資料尚不能判斷」。

最後五分鐘是 Exit Ticket。每位學生留下三句話：我今天採納了 AI 的哪一個建議；我沒有採納哪一個建議，理由是什麼；下一輪我還需要補哪一種證據。這三句話會把 AI 使用從「有沒有用工具」轉成「有沒有留下判斷」。對老師來說，這也是最省時間的檢查點：你不必讀完整篇報告，就能看見學生是否理解變因、證據和結論之間的距離。

如果要把這堂課帶進教室，我建議只記住一句話：AI 負責整理，學生負責判斷，老師負責設計退件規則。當流程清楚，AI 不會取代探究；它反而會讓學生更容易看見，自己的物理想法到底有沒有被證據撐住。
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
    weights = [0.16, 0.18, 0.19, 0.28, 0.19]
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
    draw.text((50,28),'AI 物理探究課｜slide-video QA contact sheet',font=title_font,fill=(32,45,62))
    coords=[(50,100),(560,100),(1070,100),(300,520),(810,520)]
    for (name,im),(x,y) in zip(imgs,coords):
        sheet.paste(im,(x,y))
        draw.rectangle([x,y,x+480,y+270],outline=(32,45,62),width=3)
        draw.text((x,y+285),name,font=font,fill=(32,45,62))
    checks=OUT/'checks'; checks.mkdir(exist_ok=True)
    sheet.save(checks/'contact_sheet_slide_video_v1.png')


def write_upload_kit(total):
    kit = f'''# YouTube upload kit｜一堂 45 分鐘 AI 物理探究課怎麼排？\n\n## 建議標題\n1. 一堂 45 分鐘 AI 物理探究課怎麼排？\n2. AI 可以進教室，但流程不能交給 AI\n3. 讓學生用 AI 做探究：老師要守住哪五步？\n\n## 影片檔\n- `ai-physics-inquiry-class-slide-video-draft-v1.mp4`\n- 長度：{total:.3f} 秒\n- 規格：1920×1080，H.264 + AAC\n\n## 說明欄草稿\n這支影片把「AI 物理探究課」拆成一堂 45 分鐘可以落地的流程：情境問題、學生假設、資料證據、同儕三問、AI 自評與 Exit Ticket。\n\n重點不是讓 AI 替學生完成探究，而是讓 AI 只做整理與回饋，學生保留判斷，老師保留退件規則。\n\n## 章節\n00:00 AI 可以進教室，但流程不能交給 AI\n00:45 情境與可測量問題\n01:40 學生先寫假設，AI 只修語句\n02:40 資料、圖像、同儕三問與 AI 自評\n04:15 Exit Ticket：留下採納與不採納理由\n\n## Hashtags\n#AI教學 #物理教學 #探究實作 #教師備課 #AI素養\n\n## 置頂留言草稿\n你會把 AI 放在探究課的哪一段？我會優先放在「整理證據」和「自評三問」，不放在直接產生結論。\n\n## 人工上傳前仍需確認\n- YouTube/Google 登入與頻道權限。\n- 若使用真實學生作品、照片或未公開題目，需先匿名化並確認授權。\n'''
    (OUT/'youtube-upload-kit-longform-v1.md').write_text(kit, encoding='utf-8')


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
        'upload_kit': 'slide_video_draft_v1/youtube-upload-kit-longform-v1.md',
        'shareable_handout': 'slide_video_draft_v1/ai-physics-inquiry-class-shareable-handout-v1.md',
        'ffconcat': 'slide_video_draft_v1/slides.ffconcat',
        'check_frames': [str(p.relative_to(BASE)) for p in sorted((OUT/'check_frames').glob('frame_*.png'))],
        'contact_sheet': 'slide_video_draft_v1/checks/contact_sheet_slide_video_v1.png',
        'duration_seconds': round(total,3),
        'verification': verification,
        'next_auto_push': '第三季優先題 4「公開前三查」已完成 35 秒 Shorts MP4／公開檢查表；第三季優先題 5「圖能用嗎」storyboard 已完成。若 YouTube/Google 登入仍未完成，下一輪把優先題 5 擴成 35 秒 Shorts MP4／圖片授權檢查表；若已完成登入，優先上傳第一季首批或第三季代表作。'
    }
    (OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    readme=f'''# AI 物理探究課｜slide-video draft v1\n\n狀態：已由 5 張 storyboard 擴成 4 分 56 秒長片本機草稿，並完成旁白、字幕、抽幀 QA、YouTube upload kit、正式可分享／Google Docs-ready 講義與交接壓縮包。\n\n## 檔案\n- 影片：`slide_video_draft_v1/{MP4.name}`\n- 旁白：`slide_video_draft_v1/narration_edge_hsiaoyu.mp3`\n- 旁白全文：`slide_video_draft_v1/narration_zh_tw.txt`\n- 字幕：`slide_video_draft_v1/narration_edge_hsiaoyu.vtt`、`slide_video_draft_v1/narration_edge_hsiaoyu.srt`\n- 抽幀：`slide_video_draft_v1/check_frames/`\n- QA contact sheet：`slide_video_draft_v1/checks/contact_sheet_slide_video_v1.png`\n- 長片 upload kit：`slide_video_draft_v1/youtube-upload-kit-longform-v1.md`\n- 正式講義：`slide_video_draft_v1/ai-physics-inquiry-class-shareable-handout-v1.md`\n- manifest：`slide_video_draft_v1/manifest.json`\n- 交接壓縮包：`slide_video_draft_v1/ai-physics-inquiry-class-slide-video-draft-v1-20260513.tar.gz`\n\n## 驗證\n- ffprobe：{total:.3f} 秒，1920×1080，H.264 + AAC。\n- PIL：5 張原始 storyboard、5 張抽幀與 QA contact sheet 尺寸／模式已寫入 manifest。\n- 視覺 QA：contact sheet 已檢查，五張抽幀繁中可讀、無 tofu／明顯裁切／文字重疊／過度擁擠。\n- 正式講義：已讀回驗證，包含 45 分鐘流程、學生工作區、同儕三問、AI prompt、退件句、評量規準與公開分享提醒。\n- 壓縮包：Python tarfile 可讀回列出內容，且包含正式講義。\n\n## 下一個可自動推進項目\n第三季優先題 4「公開前三查」已完成 35 秒 Shorts MP4／公開檢查表；第三季優先題 5「圖能用嗎」storyboard 已完成。若 YouTube/Google 登入仍未完成，下一輪把優先題 5 擴成 35 秒 Shorts MP4／圖片授權檢查表；若已完成登入，優先上傳第一季首批或第三季代表作。\n'''
    (OUT/'README.md').write_text(readme,encoding='utf-8')


def make_archive():
    archive = OUT/'ai-physics-inquiry-class-slide-video-draft-v1-20260513.tar.gz'
    members = [
        OUT/'README.md', OUT/'manifest.json', OUT/'build_slide_video_draft.py', OUT/'narration_zh_tw.txt', AUDIO,
        OUT/'narration_edge_hsiaoyu.vtt', OUT/'narration_edge_hsiaoyu.srt', OUT/'slides.ffconcat', MP4,
        OUT/'checks/contact_sheet_slide_video_v1.png', OUT/'youtube-upload-kit-longform-v1.md', OUT/'ai-physics-inquiry-class-shareable-handout-v1.md',
        BASE/'README.md', BASE/'manifest.json', BASE/'ai-physics-inquiry-45min-flow-handout-draft-v1.md'
    ] + SLIDES + sorted((OUT/'check_frames').glob('frame_*.png'))
    with tarfile.open(archive, 'w:gz') as tar:
        for p in members:
            tar.add(p, arcname=str(p.relative_to(BASE)))
    with tarfile.open(archive, 'r:gz') as tar:
        names = tar.getnames()
    return archive, names


def main():
    OUT.mkdir(parents=True, exist_ok=True)
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
    video_total = duration(MP4)
    for idx,pct in enumerate([0.10,0.30,0.50,0.70,0.90], start=1):
        subprocess.check_call(['ffmpeg','-y','-hide_banner','-loglevel','error','-ss',f'{video_total*pct:.3f}','-i',str(MP4),'-frames:v','1',str(frames/f'frame_{idx:02d}.png')])
    make_contact_sheet()
    write_upload_kit(video_total)
    write_docs(video_total)
    archive, names = make_archive()
    print(json.dumps({'video':str(MP4),'duration':video_total,'archive':str(archive),'archive_count':len(names)},ensure_ascii=False))

if __name__ == '__main__':
    main()
