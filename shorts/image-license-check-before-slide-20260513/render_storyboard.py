from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json, tarfile, textwrap, re, shutil, subprocess, os
from datetime import datetime

BASE = Path('/home/adl/youtube-lu-ai-channel')
PKG = BASE / 'shorts' / 'image-license-check-before-slide-20260513'
SLIDES = PKG / 'slides'
CHECKS = PKG / 'checks'
SLIDES.mkdir(parents=True, exist_ok=True)
CHECKS.mkdir(parents=True, exist_ok=True)

font_candidates = [
    '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
    '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',
]
font_path = next((p for p in font_candidates if Path(p).exists()), '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')

def font(size, bold=False):
    return ImageFont.truetype(font_path, size)

W,H = 1080,1920
BG = (12,18,32)
CARD = (248,250,252)
INK = (15,23,42)
BLUE = (37,99,235)
CYAN = (14,165,233)
YELLOW = (245,158,11)
GREEN = (22,163,74)
RED = (220,38,38)
MUTED = (100,116,139)

def wrap(draw, text, fnt, max_width):
    out=[]
    for para in text.split('\n'):
        line=''
        for ch in para:
            trial=line+ch
            if draw.textbbox((0,0), trial, font=fnt)[2] <= max_width:
                line=trial
            else:
                if line: out.append(line)
                line=ch
        if line: out.append(line)
    return out

def rounded(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)

def draw_slide(num, kicker, title, body, accent, footer='AI 物理教學'):
    img=Image.new('RGB',(W,H),BG)
    d=ImageDraw.Draw(img)
    # background shapes
    d.ellipse((-260, -180, 520, 560), fill=(30,64,175))
    d.ellipse((690, 1240, 1240, 1880), fill=(8,145,178))
    d.rectangle((0,0,W,18), fill=accent)
    # top label
    rounded(d,(72,86,1008,210),34,(30,41,59),outline=(71,85,105),width=2)
    d.text((112,122), f'第三季優先題 5｜圖能用嗎｜{kicker}', font=font(34), fill=(226,232,240))
    # title card
    rounded(d,(72,270,1008,560),42,CARD)
    title_lines = wrap(d,title,font(78),820)
    y=318
    for line in title_lines[:3]:
        d.text((128,y),line,font=font(78),fill=INK)
        y += 92
    # visual: three gates
    y0=650
    gates=[('來源','誰做的？'),('授權','能公開？'),('替代','有備案？')]
    colors=[CYAN,YELLOW,GREEN]
    for i,(a,b) in enumerate(gates):
        x=90+i*330
        rounded(d,(x,y0,x+270,y0+230),34,(241,245,249),outline=colors[i],width=8)
        d.text((x+54,y0+46),a,font=font(58),fill=colors[i])
        d.text((x+42,y0+132),b,font=font(38),fill=INK)
    # body
    rounded(d,(72,950,1008,1590),42,(255,255,255),outline=(203,213,225),width=3)
    y=1015
    for idx,line in enumerate(wrap(d,body,font(50),830)[:9]):
        d.text((132,y),line,font=font(50),fill=INK)
        y += 70
    # footer / slide number
    rounded(d,(72,1668,1008,1810),34,(15,23,42),outline=accent,width=3)
    d.text((112,1712),f'{num}/5',font=font(48),fill=accent)
    d.text((248,1718),footer,font=font(38),fill=(226,232,240))
    return img

slides = [
    ('開場', 'AI 找到的圖，\n可以直接放簡報嗎？', '圖很漂亮，不代表授權漂亮。\n老師先做三件事：問來源、查授權、準備替代素材。', BLUE),
    ('第一關', '先問：這張圖從哪裡來？', '請 AI 不只貼圖，還要列出：網站名稱、作者、連結、授權說明。\n找不到來源，就先不要公開使用。', CYAN),
    ('第二關', '再問：能不能公開分享？', '課堂內部示範和公開簡報不一樣。\n看清楚是否允許改作、商用、署名，截圖也要留證據。', YELLOW),
    ('第三關', '最後準備替代方案', '不確定授權時，改用自己畫的簡圖、公有領域素材、或只用文字描述。\n快，不該換成風險。', GREEN),
    ('收束', '給 AI 的可複製句', '「請列出每張圖片的來源、授權、是否可公開使用；不確定的請提出可替代的自製圖。」', RED),
]

slide_paths=[]
for i,(k,t,b,c) in enumerate(slides,1):
    im=draw_slide(i,k,t,b,c)
    p=SLIDES/f'slide_{i:02d}.png'
    im.save(p)
    slide_paths.append(p)

# contact sheet 3+2
thumb_w, thumb_h = 320, 568
sheet = Image.new('RGB',(1120,1480),(15,23,42))
d=ImageDraw.Draw(sheet)
d.text((44,32),'第三季優先題 5｜圖能用嗎｜Storyboard QA',font=font(42),fill=(226,232,240))
positions=[(44,110),(400,110),(756,110),(222,760),(578,760)]
for p,pos in zip(slide_paths,positions):
    im=Image.open(p).resize((thumb_w,thumb_h))
    sheet.paste(im,pos)
    d.text((pos[0],pos[1]+thumb_h+12),p.name,font=font(26),fill=(203,213,225))
contact=CHECKS/'contact_sheet.png'
sheet.save(contact)

readme = '''# Shorts Storyboard｜AI 找到的圖，可以直接放簡報嗎？

狀態：2026-05-13 每小時雷達已完成第三季優先題 5 的 5 張 1080×1920 storyboard 圖卡與交接包。  
來源：第三季內容題庫優先題 5「AI 找到的圖，可以直接放簡報嗎？」。

## 30 秒製作簡報

- 核心鉤子：圖很漂亮，不代表授權漂亮。
- 教師可複製句：請 AI 列出每張圖片的來源、授權、是否可公開使用；不確定的請提出可替代的自製圖。
- 影片結構：來源 → 授權 → 替代方案 → 可複製 prompt。
- 公開提醒：不要使用未授權圖片、真實學生作品或不明來源截圖作公開素材。

## 圖卡

1. `slides/slide_01.png`｜AI 找到的圖，可以直接放簡報嗎？
2. `slides/slide_02.png`｜先問：這張圖從哪裡來？
3. `slides/slide_03.png`｜再問：能不能公開分享？
4. `slides/slide_04.png`｜最後準備替代方案
5. `slides/slide_05.png`｜給 AI 的可複製句

## 驗證

- PIL：5 張圖卡皆為 1080×1920 RGB。
- QA contact sheet：`checks/contact_sheet.png` 為 1120×1480 RGB，供手機快速檢查繁中可讀、無 tofu、無裁切、無重疊與不過度擁擠。
- 壓縮包：`image-license-check-before-slide-storyboard-kit-20260513.tar.gz` 已用 Python `tarfile` 讀回確認包含 README、manifest、render script、slides 與 contact sheet。

## 下一個自動推進

若 YouTube/Google 登入仍未完成：把本 storyboard 擴成 35 秒 Shorts MP4／封面／字幕／YouTube upload kit，並延伸一頁「圖片授權檢查表」。  
若使用者已完成登入：優先上傳已完成的第一季首批 Shorts 或第三季代表作。
'''
(PKG/'README.md').write_text(readme, encoding='utf-8')

manifest = {
    'slug':'image-license-check-before-slide-20260513',
    'title':'AI 找到的圖，可以直接放簡報嗎？',
    'season':'第三季',
    'priority':5,
    'status':'storyboard_complete',
    'created_at':'2026-05-13 11:50 CST',
    'slides':[str(p.relative_to(PKG)) for p in slide_paths],
    'contact_sheet':'checks/contact_sheet.png',
    'next_auto_push':'expand storyboard into 35s Shorts MP4, cover, subtitles, YouTube upload kit, and image-license checklist if YouTube login remains blocked',
    'public_caution':'Do not publish unlicensed images, real student work, or unknown-source screenshots without human confirmation.'
}
(PKG/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')

render_script = Path('/tmp/create_image_license_storyboard.py').read_text(encoding='utf-8')
(PKG/'render_storyboard.py').write_text(render_script, encoding='utf-8')

# verify dimensions
for p in slide_paths:
    im=Image.open(p)
    assert im.size == (1080,1920) and im.mode == 'RGB', (p, im.size, im.mode)
im=Image.open(contact)
assert im.size == (1120,1480) and im.mode == 'RGB', (contact, im.size, im.mode)

# archive
archive = PKG/'image-license-check-before-slide-storyboard-kit-20260513.tar.gz'
with tarfile.open(archive, 'w:gz') as tf:
    for rel in ['README.md','manifest.json','render_storyboard.py']:
        tf.add(PKG/rel, arcname=f'image-license-check-before-slide-20260513/{rel}')
    for p in slide_paths:
        tf.add(p, arcname=f'image-license-check-before-slide-20260513/slides/{p.name}')
    tf.add(contact, arcname='image-license-check-before-slide-20260513/checks/contact_sheet.png')
with tarfile.open(archive, 'r:gz') as tf:
    names=tf.getnames()
    assert 'image-license-check-before-slide-20260513/README.md' in names
    assert 'image-license-check-before-slide-20260513/checks/contact_sheet.png' in names
    assert len(names) == 9

# update mobile index by prepending card
index = BASE/'mobile-index'/'index.html'
html = index.read_text(encoding='utf-8')
html = re.sub(r'更新：[^<]+<br>', '更新：2026-05-13 11:50<br>', html, count=1)
card = '''<section class="card"><div class="date">05/13 11:50</div><h2>第三季優先題 5｜圖能用嗎｜Shorts storyboard</h2><div class="links"><a class="btn " href="../shorts/image-license-check-before-slide-20260513/checks/contact_sheet.png">🖼 QA contact sheet</a><a class="btn " href="../shorts/image-license-check-before-slide-20260513/slides/slide_01.png">🖼 slide 01</a><a class="btn " href="../shorts/image-license-check-before-slide-20260513/README.md">📝 README.md</a><a class="btn " href="../shorts/image-license-check-before-slide-20260513/image-license-check-before-slide-storyboard-kit-20260513.tar.gz">📦 壓縮包</a></div></section>'''
html = html.replace('</p><section class="card">','</p>'+card+'<section class="card">',1)
index.write_text(html, encoding='utf-8')

# update backlog stale next item and append progress note
backlog = BASE/'publishing'/'content-backlog-season-03-v1.md'
btxt = backlog.read_text(encoding='utf-8')
btxt = btxt.replace('06:20 第三季優先題 4「公開前三查」Shorts storyboard package 已完成並同步 Pages content commit `2d85910`、cleanup commit `1a0b8a7` live 驗證）', '06:20 第三季優先題 4「公開前三查」Shorts storyboard package 已完成並同步 Pages content commit `2d85910`、cleanup commit `1a0b8a7` live 驗證；11:50 第三季優先題 5「圖能用嗎」storyboard package 已完成，本機 QA 通過，待同步 Pages）')
btxt = btxt.replace('4. **優先題 4｜學生作品要放上網前，AI 幫忙檢查哪三件事？**  \n   - 理由：補上學生作品公開前的責任／授權主題，能直接延伸成 Shorts 與公開檢查表。\n   - 進度：5 張 1080×1920 storyboard 圖卡與交接包已完成：`../shorts/public-before-share-check-20260513/README.md`。\n   - 下一步：若 YouTube/Google 登入仍未完成，把本 storyboard 擴成 35 秒 Shorts MP4／封面／字幕／YouTube upload kit，並延伸一頁學生作品公開檢查表。\n5. **優先題 6｜老師用 AI 做公開教材：從來源到標註的檢查流程**', '4. **優先題 4｜學生作品要放上網前，AI 幫忙檢查哪三件事？**  \n   - 理由：補上學生作品公開前的責任／授權主題，能直接延伸成 Shorts 與公開檢查表。\n   - 進度：35 秒 Shorts MP4、封面、字幕、YouTube upload kit 與學生作品公開檢查表已完成：`../shorts/public-before-share-check-20260513/README.md`。\n   - 下一步：已接續優先題 5 storyboard。\n5. **優先題 5｜AI 找到的圖，可以直接放簡報嗎？**  \n   - 理由：補上圖片授權與替代素材檢查，是公開責任主線的下一個低風險 Shorts。\n   - 進度：5 張 1080×1920 storyboard 圖卡與交接包已完成：`../shorts/image-license-check-before-slide-20260513/README.md`。\n   - 下一步：若 YouTube/Google 登入仍未完成，把本 storyboard 擴成 35 秒 Shorts MP4／封面／字幕／YouTube upload kit，並延伸一頁圖片授權檢查表。\n6. **優先題 6｜老師用 AI 做公開教材：從來源到標註的檢查流程**')
btxt = btxt.replace('若 YouTube/Google 登入仍未完成，下一輪把第三季優先題 4「公開前三查」storyboard 擴成 35 秒 Shorts MP4／封面／字幕／YouTube upload kit，並延伸一頁學生作品公開檢查表；若使用者已完成登入，改優先上傳第一季首批 Shorts 或第三季代表作。', '若 YouTube/Google 登入仍未完成，下一輪把第三季優先題 5「圖能用嗎」storyboard 擴成 35 秒 Shorts MP4／封面／字幕／YouTube upload kit，並延伸一頁圖片授權檢查表；若使用者已完成登入，改優先上傳第一季首批 Shorts 或第三季代表作。')
backlog.write_text(btxt, encoding='utf-8')

progress = BASE/'CHANNEL_PROGRESS.md'
ptxt = progress.read_text(encoding='utf-8')
ptxt = ptxt.replace('最後更新：2026-05-13 09:36 巡視自動推進', '最後更新：2026-05-13 11:50 巡視自動推進')
old='''50. 第三季優先題 4「公開前三查」已由 storyboard 擴成 35 秒本機 Shorts 草稿、封面、字幕、YouTube upload kit 與「學生作品公開檢查表」：`shorts/public-before-share-check-20260513/`，包含 `public-before-share-check-shorts-35s.mp4`、`cover_public_before_share_check_v1.png`、zh-TW HsiaoYu 旁白、VTT/SRT 字幕、`youtube-upload-kit.md`、`student-work-public-checklist-v1.md`、QA sheet、deterministic build script 與壓縮包 `public-before-share-check-upload-kit-20260513.tar.gz`；ffprobe 驗證 1080×1920、25fps、H.264 yuv420p + AAC、35.000 秒，PIL 驗證封面／圖卡／抽幀皆為 RGB，視覺 QA 通過（繁中可讀、無 tofu／裁切／重疊，僅 footer 小字略小但不影響主要訊息），壓縮包已用 Python tarfile 讀回確認包含檢查表。手機索引已改成本支 MP4／封面／QA／upload kit／檢查表連結，已同步到 GitHub Pages content commit `3061aca`、cleanup commit `cbdc6a2`、final metadata sync commit `1aab46e`、final asset refresh commit `2758b0b` 並 live 驗證（index／MP4／封面／README／檢查表／壓縮包皆 HTTP 200，瀏覽器標題與卡片正確、console 無錯）。下一個可自動推進項目：若 YouTube/Google 登入仍未完成，從第三季題庫挑選下一個尚未完成 storyboard／講義延伸；若已登入，優先上傳第一季首批或本支第三季 Shorts。'''
new=old+'\n51. 第三季優先題 5「AI 找到的圖，可以直接放簡報嗎？」已完成 5 張 1080×1920 Shorts storyboard 圖卡與交接包：`shorts/image-license-check-before-slide-20260513/`，包含 `README.md`、`manifest.json`、deterministic render script、`slides/slide_01.png`–`slide_05.png`、`checks/contact_sheet.png` 與壓縮包 `image-license-check-before-slide-storyboard-kit-20260513.tar.gz`；PIL 驗證 5 張圖卡皆為 1080×1920 RGB，contact sheet 為 1120×1480 RGB，壓縮包已用 Python tarfile 讀回確認 9 個項目。手機索引已加入本 storyboard 的手機可點連結；下一個可自動推進項目：若 YouTube/Google 登入仍未完成，把本 storyboard 擴成 35 秒 Shorts MP4／封面／字幕／YouTube upload kit，並延伸一頁圖片授權檢查表；若已登入，優先上傳第一季首批或第三季代表作。'
if old not in ptxt:
    raise SystemExit('progress target not found')
ptxt = ptxt.replace(old,new)
progress.write_text(ptxt, encoding='utf-8')

print('created', PKG)
print('archive_members', len(names))
print('font', font_path)
print('contact', contact)
