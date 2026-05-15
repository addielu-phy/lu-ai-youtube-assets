from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json, tarfile, textwrap

BASE = Path('/home/adl/youtube-lu-ai-channel')
PKG = BASE / 'shorts' / 'parent-message-draft-only-20260515'
SLIDES = PKG / 'slides'
CHECKS = PKG / 'checks'
SLIDES.mkdir(parents=True, exist_ok=True)
CHECKS.mkdir(parents=True, exist_ok=True)
FONT = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
W, H = 1080, 1920
palette = {
    'bg':'#102033', 'cream':'#FFF8EA', 'ink':'#10243A', 'blue':'#2F6FD6',
    'orange':'#F2A13B', 'green':'#2EA66F', 'red':'#D94B4B', 'muted':'#667085',
    'purple':'#6D5BD0', 'line':'#E2D2BC', 'soft':'#F7E8D2', 'yellow':'#F8C84E'
}

def font(size):
    return ImageFont.truetype(FONT, size)

def wrap(draw, text, fnt, maxw):
    out=[]
    for para in str(text).split('\n'):
        line=''
        for ch in para:
            if draw.textbbox((0,0), line+ch, font=fnt)[2] <= maxw:
                line += ch
            else:
                if line:
                    out.append(line)
                line = ch
        if line:
            out.append(line)
    return out

def center(draw, box, text, fnt, fill, maxw=None, spacing=10):
    x1,y1,x2,y2=box
    lines=wrap(draw,text,fnt,maxw or x2-x1-20)
    total=len(lines)*(fnt.size+spacing)-spacing
    y=y1+(y2-y1-total)//2
    for line in lines:
        bbox=draw.textbbox((0,0),line,font=fnt)
        tw=bbox[2]-bbox[0]
        draw.text((x1+(x2-x1-tw)//2,y),line,font=fnt,fill=fill)
        y += fnt.size+spacing

def text_block(draw, x, y, w, items, size=39, fill=None, gap=14):
    fill = fill or palette['ink']
    yy=y
    for item in items:
        f=font(size if len(item)<=30 else size-4)
        for line in wrap(draw, item, f, w):
            draw.text((x,yy), line, font=f, fill=fill)
            yy += f.size+12
        yy += gap
    return yy

slides = [
 {'n':'01','tag':'3秒鉤子','title':'語氣很客氣，\n不代表能送出','body':['AI 很會把家長訊息寫得禮貌。','但第一版只能當草稿：要先審事實、語氣與隱私。'],'left':'AI 草稿風險','left_items':['太快下結論','暗示學生問題','放入敏感細節'],'right':'教師送出前','right_items':['核對事實','改成可合作','移除個資'],'call':'家長訊息：只當草稿'},
 {'n':'02','tag':'先審事實','title':'第一關：\n這件事真的發生嗎？','body':['家長訊息不是作文比賽。','AI 寫得順，老師仍要逐項核對時間、作業、觀察與下一步。'],'left':'不要送','left_items':['他最近都沒交','上課一直分心','成績明顯退步'],'right':'改成','right_items':['5/10 作業未補','本週兩次需提醒','下次小考再觀察'],'call':'只寫可確認事實'},
 {'n':'03','tag':'再審語氣','title':'第二關：\n從指責改成合作','body':['同一件事，可以寫成壓力，也可以寫成合作。','AI 草稿要被老師改成「我們一起支持」。'],'left':'指責句','left_items':['請家長多管教','他就是不專心','問題很嚴重'],'right':'合作句','right_items':['想一起確認狀況','可否協助提醒','我們先試一週'],'call':'語氣要能開啟對話'},
 {'n':'04','tag':'最後審隱私','title':'第三關：\n敏感資訊先拿掉','body':['不要把其他學生、家庭狀況、未確認診斷或公開不得知的細節放進訊息。','能少寫，就先少寫。'],'left':'刪掉','left_items':['其他同學姓名','家庭推測','未確認標籤'],'right':'留下','right_items':['本次觀察','可做行動','回覆方式'],'call':'保護學生，也保護老師'},
 {'n':'05','tag':'收尾 CTA','title':'送出前，\n用三句話退件','body':['1. 這句有可確認事實嗎？','2. 這句能讓家長願意合作嗎？','3. 這句有不該公開的敏感資訊嗎？'],'left':'未通過','left_items':['無證據','像責備','有個資'],'right':'可送出','right_items':['有事實','可合作','低風險'],'call':'下一步可擴成 35 秒 Shorts＋家長訊息審稿表'}
]

def draw_review_panel(d, s, y):
    x1, x2 = 105, 975
    mid = 540
    d.rounded_rectangle([x1,y,x2,y+500], radius=34, fill='white', outline=palette['line'], width=4)
    d.line([mid,y+24,mid,y+476], fill=palette['line'], width=5)
    d.rounded_rectangle([x1+28,y+28,mid-24,y+112], radius=24, fill=palette['red'])
    d.rounded_rectangle([mid+24,y+28,x2-28,y+112], radius=24, fill=palette['green'])
    center(d,(x1+38,y+34,mid-34,y+104),s['left'],font(37),'white',360)
    center(d,(mid+34,y+34,x2-38,y+104),s['right'],font(37),'white',360)
    yy=y+150
    for item in s['left_items']:
        d.rounded_rectangle([x1+42, yy+4, x1+74, yy+36], radius=8, fill=palette['red'])
        d.text((x1+92, yy), item, font=font(31), fill=palette['ink'])
        yy += 76
    yy=y+150
    for item in s['right_items']:
        d.ellipse([mid+44, yy+6, mid+76, yy+38], fill=palette['green'])
        d.text((mid+94, yy), item, font=font(31), fill=palette['ink'])
        yy += 76

def draw_slide(s):
    im=Image.new('RGB',(W,H),palette['bg'])
    d=ImageDraw.Draw(im)
    d.rounded_rectangle([60,70,1020,1850], radius=54, fill=palette['cream'])
    d.rounded_rectangle([100,120,980,296], radius=38, fill=palette['purple'])
    d.text((140,166), f"第三季 Shorts｜{s['tag']}", font=font(50), fill='white')
    y=365
    for line in s['title'].split('\n'):
        d.text((110,y),line,font=font(82),fill=palette['ink'])
        y+=106
    d.rounded_rectangle([110,y+16,970,y+34], radius=8, fill=palette['orange'])
    y += 76
    y = text_block(d,110,y,860,s['body'],size=39)
    draw_review_panel(d,s,1110)
    d.rounded_rectangle([110,1648,970,1796], radius=34, fill=palette['ink'])
    center(d,(130,1660,950,1788),s['call'],font(43),'white',760)
    d.text((110,1815),'AI 物理教學｜storyboard draft',font=font(30),fill=palette['muted'])
    path=SLIDES/f"slide_{s['n']}.png"
    im.save(path)
    return path

paths=[draw_slide(s) for s in slides]
thumb_w, thumb_h = 324, 576
sheet=Image.new('RGB',(1120,1480),'#1B2635')
d=ImageDraw.Draw(sheet)
d.text((40,28),'家長訊息只當草稿｜5 張 storyboard',font=font(34),fill='white')
for i,(p,pos) in enumerate(zip(paths,[(40,92),(398,92),(756,92),(220,744),(578,744)])):
    im=Image.open(p).resize((thumb_w,thumb_h))
    x,y=pos
    sheet.paste(im,(x,y))
    d.text((x,y+thumb_h+10),f"slide {i+1}",font=font(28),fill='white')
sheet.save(CHECKS/'contact_sheet.png')

checklist='''# 教師審稿 checklist｜家長訊息第一版只當草稿

狀態：2026-05-15 每小時雷達自動推進產出 v1。  
用途：把 AI 產生的家長訊息，改成事實清楚、語氣可合作、低隱私風險的教師版。

## 一句話目標
家長訊息不是讓 AI 代替老師判斷，而是先產生草稿，再由老師做三關審稿。

## 三關審稿

| 關卡 | 先問 | 建議改法 |
|---|---|---|
| 事實 | 這句是否有可確認的時間、事件或作品證據？ | 把「都、一直、完全」改成具體日期與觀察 |
| 語氣 | 這句會讓家長覺得被責備，還是被邀請合作？ | 改成「想一起確認」「可否協助」「我們先試」 |
| 隱私 | 這句是否包含其他學生、家庭推測、未確認診斷或敏感資訊？ | 刪除可辨識細節，只保留必要行動 |

## 可複製 Prompt
請把以下家長訊息草稿改寫成教師可審稿版本：保留可確認事實，刪除未證實推測、情緒評價、其他學生資訊與敏感個資；語氣改成邀請合作；最後列出老師送出前還需要人工確認的 3 件事。

## 送出前 30 秒 checklist
- [ ] 是否只寫我能確認的事實？
- [ ] 是否避免把暫時狀況寫成永久標籤？
- [ ] 是否沒有其他學生或家庭隱私？
- [ ] 是否有明確、可合作的下一步？
- [ ] 是否需要先和導師、輔導室或行政確認？

## 公開與隱私提醒
不要把真實學生個資、家長聯絡資訊、家庭背景、診斷／疑似診斷、其他學生姓名或未授權截圖交給 AI 或放入公開素材。真實案例發布前需使用者人工確認可公開性。
'''
(PKG/'parent-message-review-checklist-v1.md').write_text(checklist,encoding='utf-8')
manifest={
 'title':'讓 AI 幫忙寫家長訊息，第一版只准當草稿',
 'candidate':'season-03-priority-12',
 'status':'storyboard package source retained; 35s Shorts MP4/upload kit completed in build_mp4_upload_kit.py',
 'created':'2026-05-15',
 'dimensions':'1080x1920',
 'slides':[f'slides/slide_{i:02d}.png' for i in range(1,6)],
 'contact_sheet':'checks/contact_sheet.png',
 'teacher_checklist':'parent-message-review-checklist-v1.md',
 'archive':'parent-message-draft-only-upload-kit-20260515.tar.gz',
 'next_auto_push':'do not rebuild this storyboard; choose the next unfinished candidate or publish/upload after human YouTube login'
}
(PKG/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
readme='''# Shorts storyboard｜讓 AI 幫忙寫家長訊息，第一版只准當草稿

狀態：2026-05-15 每小時雷達自動推進完成 storyboard package v1，並新增教師審稿 checklist。  
來源：第三季內容題庫優先題 12。

## 30 秒製作簡報

- 3 秒鉤子：語氣很客氣，不代表適合送出。
- 核心觀點：AI 可以幫老師起草家長訊息，但第一版只准當草稿；送出前要過「事實、語氣、隱私」三關。
- 對象：國高中自然／物理教師；可用於家長聯絡、作業提醒、課堂觀察回饋、補救教學溝通前審稿。
- 最小素材：家長訊息草稿、教師審稿 checklist、敏感資訊提醒。

## 圖卡

1. `slides/slide_01.png`｜語氣很客氣，不代表能送出
2. `slides/slide_02.png`｜第一關：這件事真的發生嗎？
3. `slides/slide_03.png`｜第二關：從指責改成合作
4. `slides/slide_04.png`｜第三關：敏感資訊先拿掉
5. `slides/slide_05.png`｜送出前，用三句話退件

## 延伸講義

- `parent-message-review-checklist-v1.md`｜AI 家長訊息三關教師審稿 checklist。

## 驗證

- PIL 輸出：5 張 `1080×1920` RGB PNG。
- Contact sheet：`checks/contact_sheet.png`。
- 視覺 QA：繁中主文字可讀、無 tofu 方塊、無裁切、無重疊；contact sheet 排版不擁擠。
- 壓縮包：`parent-message-draft-only-storyboard-kit-20260515.tar.gz` 可用 Python tarfile 讀回。

## 下一個自動推進

若 YouTube/Google 登入仍未完成：不要重做本 storyboard；改挑下一個尚未完成候選，或先做頻道素材聲音替換盤點。  
若已登入：優先上傳第一季首批或第三季代表作。
'''
(PKG/'README.md').write_text(readme,encoding='utf-8')
archive=PKG/'parent-message-draft-only-storyboard-kit-20260515.tar.gz'
with tarfile.open(archive,'w:gz') as tar:
    for rel in ['README.md','manifest.json','render_storyboard.py','parent-message-review-checklist-v1.md','checks/contact_sheet.png']:
        tar.add(PKG/rel, arcname=f'parent-message-draft-only-20260515/{rel}')
    for p in paths:
        tar.add(p, arcname=f'parent-message-draft-only-20260515/slides/{p.name}')
print(PKG)
print(archive)
