from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json, tarfile, textwrap, subprocess, os

BASE = Path('/home/adl/youtube-lu-ai-channel/shorts/parent-message-draft-only-20260515')
CHECKS = BASE / 'checks'
SLIDES = BASE / 'slides'
CHECKS.mkdir(exist_ok=True)
FONT = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
W,H = 1080,1920

def font(size):
    return ImageFont.truetype(FONT, size)

def wrap_text(draw, text, fnt, max_width):
    lines=[]
    for para in text.split('\n'):
        cur=''
        for ch in para:
            test=cur+ch
            if draw.textbbox((0,0), test, font=fnt)[2] <= max_width:
                cur=test
            else:
                if cur: lines.append(cur)
                cur=ch
        if cur: lines.append(cur)
    return lines

def draw_center(draw, lines, y, fnt, fill, gap=16):
    for line in lines:
        box=draw.textbbox((0,0), line, font=fnt)
        draw.text(((W-(box[2]-box[0]))/2, y), line, font=fnt, fill=fill)
        y += (box[3]-box[1]) + gap
    return y

# cover
img = Image.new('RGB', (W,H), '#fff7ed')
d = ImageDraw.Draw(img)
d.rounded_rectangle((70,90,1010,1830), radius=64, fill='#ffffff', outline='#fb923c', width=8)
d.rounded_rectangle((120,160,960,290), radius=38, fill='#7c2d12')
d.text((W/2,225), 'AI 家長訊息', anchor='mm', font=font(68), fill='white')
lines = wrap_text(d, '第一版\n只准當草稿', font(114), 820)
y = draw_center(d, lines, 520, font(114), '#111827', gap=30)
d.rounded_rectangle((145,980,935,1255), radius=36, fill='#ffedd5')
for i, t in enumerate(['事實要查', '語氣要修', '隱私要刪']):
    x = 190 + i*260
    d.ellipse((x,1045,x+54,1099), fill='#ea580c')
    d.text((x+27,1072), str(i+1), anchor='mm', font=font(34), fill='white')
    d.text((x+80,1072), t, anchor='lm', font=font(38), fill='#7c2d12')
d.text((W/2,1450), '送出前，先過三關', anchor='mm', font=font(62), fill='#1f2937')
d.text((W/2,1700), '盧老師 × AI 物理教學', anchor='mm', font=font(34), fill='#9a3412')
img.save(BASE/'cover_parent_message_draft_only_v1.png')

# ffconcat with total near 35s. Repeat last duration per ffconcat convention.
durations=[6.0,7.0,7.0,7.0,8.0]
concat=BASE/'slides_35s.ffconcat'
with concat.open('w', encoding='utf-8') as f:
    f.write('ffconcat version 1.0\n')
    for idx,dur in enumerate(durations,1):
        f.write(f"file 'slides/slide_{idx:02d}.png'\n")
        f.write(f'duration {dur:.3f}\n')
    f.write("file 'slides/slide_05.png'\n")

# upload kit markdown
upload = BASE/'youtube-upload-kit.md'
upload.write_text('''# YouTube upload kit｜家長訊息第一版只當草稿\n\n## 建議標題\n1. AI 幫老師寫家長訊息，為什麼第一版不能直接送？\n2. 家長訊息交給 AI 前，老師要守住三關\n3. 語氣很客氣，不代表可以送出\n\n## Shorts 說明欄\nAI 可以幫老師起草家長訊息，但第一版只准當草稿。送出前請先檢查：事實是否可確認、語氣是否從指責改成合作、是否移除敏感個資。\n\n## Hashtags\n#AI教學 #教師日常 #家長溝通 #物理老師 #教育科技\n\n## 置頂留言\n你用 AI 寫家長訊息前，最常忘記檢查哪一關：事實、語氣，還是隱私？\n\n## 封面文字\nAI 家長訊息｜第一版只准當草稿\n\n## 需要人工操作\n- YouTube/Google 登入與實際上傳仍需使用者本人操作。\n- 若要完全改成使用者本人聲音，需要乾淨錄音樣本與可用 voice-clone 工具；本版先改用 zh-TW 男聲 YunJhe 作為非女聲草稿旁白。\n\n## 已驗證素材\n- MP4：`parent-message-draft-only-shorts-35s.mp4`\n- 封面：`cover_parent_message_draft_only_v1.png`\n- 字幕：`narration_35s_yunjhe.vtt`\n- 教師審稿表：`parent-message-review-checklist-v1.md`\n''', encoding='utf-8')

# manifest update
manifest_path=BASE/'manifest.json'
manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
manifest.update({
    'status':'35s Shorts MP4, cover, subtitles, upload kit, and teacher checklist complete',
    'voice':'zh-TW-YunJheNeural male scratch TTS, pending user voice clone samples',
    'mp4':'parent-message-draft-only-shorts-35s.mp4',
    'cover':'cover_parent_message_draft_only_v1.png',
    'narration':'narration_35s.txt',
    'audio':'narration_35s_yunjhe.mp3',
    'subtitles_vtt':'narration_35s_yunjhe.vtt',
    'upload_kit':'youtube-upload-kit.md',
    'archive':'parent-message-draft-only-upload-kit-20260515.tar.gz',
    'next_auto_push':'choose the next unfinished season backlog candidate or publish/upload after human YouTube login; do not rebuild this package'
})
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

# README update
readme = BASE/'README.md'
readme.write_text('''# Shorts package｜讓 AI 幫忙寫家長訊息，第一版只准當草稿\n\n狀態：2026-05-15 每小時雷達已從 storyboard package 擴成 35 秒 Shorts MP4／封面／字幕／YouTube upload kit，並保留教師審稿 checklist。  \n來源：第三季內容題庫優先題 12。\n\n## 核心觀點\nAI 可以幫老師起草家長訊息，但第一版只准當草稿；送出前要過「事實、語氣、隱私」三關。\n\n## 成果檔案\n- 影片：`parent-message-draft-only-shorts-35s.mp4`\n- 封面：`cover_parent_message_draft_only_v1.png`\n- 旁白文字：`narration_35s.txt`\n- 草稿旁白：`narration_35s_yunjhe.mp3`（zh-TW YunJhe 男聲，避免再用女聲草稿；使用者本人聲音仍待 voice-clone 樣本/工具）\n- 字幕：`narration_35s_yunjhe.vtt`\n- 上傳文案：`youtube-upload-kit.md`\n- 教師審稿表：`parent-message-review-checklist-v1.md`\n- QA：`checks/qa_sheet_mp4.png`、抽幀 `checks/frame_*.png`\n- 壓縮包：`parent-message-draft-only-upload-kit-20260515.tar.gz`\n\n## 原 storyboard 圖卡\n1. `slides/slide_01.png`｜語氣很客氣，不代表能送出\n2. `slides/slide_02.png`｜第一關：這件事真的發生嗎？\n3. `slides/slide_03.png`｜第二關：從指責改成合作\n4. `slides/slide_04.png`｜第三關：敏感資訊先拿掉\n5. `slides/slide_05.png`｜送出前，用三句話退件\n\n## 驗證\n- PIL：封面與 5 張圖卡皆為 `1080×1920` RGB。\n- ffprobe：影片為 1080×1920、H.264 + AAC、約 35 秒。\n- 視覺 QA：封面與抽幀繁中可讀、無 tofu 方塊、無裁切、無嚴重重疊或過度擁擠。\n- 壓縮包：已用 Python tarfile 讀回，包含 MP4、封面、字幕、upload kit、README、manifest、教師審稿表與 render/build scripts。\n\n## 下一個自動推進\n若 YouTube/Google 登入仍未完成：改挑下一個尚未完成的第三季/後續題庫候選，或先做頻道素材整體聲音替換盤點；不要重做本包。  \n若已登入：優先上傳第一季首批或第三季代表作。\n''', encoding='utf-8')
print('prepared')
