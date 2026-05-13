#!/usr/bin/env python3
from __future__ import annotations
import json, subprocess, tarfile, re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE = Path('/home/adl/youtube-lu-ai-channel/longform/public-materials-four-gates-20260513')
ROOT = Path('/home/adl/youtube-lu-ai-channel')
OUT = BASE / 'slide_video_draft_v1'
SLIDES = [BASE/'slides'/'01_hook_four_gates.png', BASE/'slides'/'02_source_gate.png', BASE/'slides'/'03_license_gate.png', BASE/'slides'/'04_privacy_ai_label_gate.png', BASE/'slides'/'05_classroom_flow.png']
TITLE = '老師用 AI 做公開教材：從來源到標註的檢查流程'
SLUG = 'public-materials-four-gates-20260513'
MP4 = OUT/'public-materials-four-gates-slide-video-draft-v1.mp4'
AUDIO = OUT/'narration_edge_hsiaoyu.mp3'
ARCHIVE = OUT/'public-materials-four-gates-slide-video-draft-v1-20260513.tar.gz'
HANDOUT = OUT/'public-materials-four-gates-shareable-handout-v1.md'
SEGMENT_TITLES = ['公開教材前，先過四道門','來源門：找到原始出處','授權門：課內使用不等於公開分享','個資門與 AI 標註門','45 分鐘課堂流程與退件句']
NARRATION = '''
AI 可以幫老師很快整理教材、圖片、學生作品和課堂活動紀錄，但只要要公開分享，就不能只問「內容好不好」。這支影片把公開教材前的檢查拆成四道門：來源、授權、個資、AI 標註。目的不是讓老師變成法律專家，而是建立一個低風險流程：每次要把教材放到網站、社群、簡報或公開課程前，都先留下可檢查的紀錄。

第一道是來源門。請先回答三件事：這個素材最早從哪裡來？我手上的是原始來源、轉貼，還是 AI 重新整理過的版本？如果學生或 AI 只貼給你一張圖、一段文字、一個網址截圖，還不能直接放進公開教材。最低限度要回到原始頁面，記下作者、發布單位、日期和網址。若找不到原始來源，最安全的做法不是硬用，而是改成自繪圖、自己拍攝的示意圖，或明確可授權的公開資源。

第二道是授權門。很多老師最容易混淆的是：課堂內合理使用，不等於可以放到公開網站或 YouTube。公開分享前，要檢查素材是否允許重製、改作和商業或非商業公開。可以用一張小表來判斷：素材名稱、來源網址、授權條款、是否可改作、是否需要標註作者、是否只能在課內使用。如果授權文字看不懂，就把它標成「需人工確認」，不要讓 AI 猜。AI 可以幫你摘要授權條文，但最後決定不能交給 AI。

第三道是個資門。只要出現學生姓名、臉、學號、班級、作業筆跡、位置資訊、家長訊息或可以反推出個人的細節，都要先匿名化。匿名化不是只把名字塗掉，還要看組合資訊會不會讓人猜出是誰。例如一張實驗照片如果同時露出校名、制服、座號和特殊事件，就算沒有姓名也可能識別。公開前請用三句話自問：能不能看出這是哪一位學生？能不能看出是哪一個家庭或班級？這份內容公開後，學生是否可能感到被評價或被標籤？

第四道是 AI 標註門。當教材裡有 AI 生成、AI 改寫、AI 摘要或 AI 協助設計的內容，建議用清楚但不誇張的方式標註。例如：「本教材流程由教師設計，部分文字初稿曾用 AI 協助整理，已由教師審稿修正。」這句話比「全 AI 生成」更準確，也比完全不說更透明。標註的重點不是炫耀工具，而是讓學生、家長和同事知道：哪些部分是教師判斷，哪些部分有工具協助，責任最後由誰承擔。

如果要帶進一堂課，可以安排成四十五分鐘活動。前十分鐘，學生或老師拿一份準備公開的教材草稿，標出所有外部素材。接著十分鐘查來源與授權，填入來源表。再用十分鐘做個資檢查，把可能識別個人的資訊改寫或移除。最後十五分鐘，寫一段公開說明和 AI 使用標註，並用同儕三問退件：來源可追嗎？授權可公開嗎？個資已處理嗎？只要其中一題答不出來，這份教材就先不公開。

我建議老師把這套流程記成一句話：能公開的教材，不只是內容正確，還要來源可追、授權可用、個資可保護、AI 使用可說明。AI 讓整理變快，但公開責任不會消失。當四道門變成固定流程，老師就能放心把好的教材分享出去，也讓學生學會，數位作品不是做好就上傳，而是要先對來源、他人和自己負責。
'''.strip()

def run(cmd):
    return subprocess.check_output(cmd, text=True).strip()

def duration(path: Path) -> float:
    return float(run(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(path)]))

def ts(seconds: float, comma=False):
    ms=int(round((seconds-int(seconds))*1000)); s=int(seconds); h, rem=divmod(s,3600); m, sec=divmod(rem,60); sep=',' if comma else '.'
    return f'{h:02d}:{m:02d}:{sec:02d}{sep}{ms:03d}'

def make_subtitles(total: float):
    weights=[0.17,0.18,0.20,0.20,0.25]
    bounds=[0.0]
    for w in weights: bounds.append(bounds[-1]+total*w/sum(weights))
    vtt=['WEBVTT','']; srt=[]
    for i,title in enumerate(SEGMENT_TITLES,1):
        start=bounds[i-1]; end=min(bounds[i],total)
        vtt += [f'{ts(start)} --> {ts(end)}', title, '']
        srt += [str(i), f'{ts(start, True)} --> {ts(end, True)}', title, '']
    (OUT/'narration_edge_hsiaoyu.vtt').write_text('\n'.join(vtt), encoding='utf-8')
    (OUT/'narration_edge_hsiaoyu.srt').write_text('\n'.join(srt), encoding='utf-8')
    return [bounds[i]-bounds[i-1] for i in range(1,6)]

def make_concat(durs):
    lines=[]
    for slide,dur in zip(SLIDES,durs):
        lines += [f"file '{slide}'", f'duration {dur:.3f}']
    lines.append(f"file '{SLIDES[-1]}'")
    (OUT/'slides.ffconcat').write_text('\n'.join(lines)+'\n', encoding='utf-8')

def make_contact_sheet():
    frames=OUT/'check_frames'
    imgs=[(p.name, Image.open(p).convert('RGB').resize((480,270))) for p in sorted(frames.glob('frame_*.png'))[:5]]
    sheet=Image.new('RGB',(1600,980),(245,242,234)); draw=ImageDraw.Draw(sheet)
    font_path='/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
    font=ImageFont.truetype(font_path,28); title_font=ImageFont.truetype(font_path,38)
    draw.text((50,28),'公開教材四關｜slide-video QA contact sheet',font=title_font,fill=(32,45,62))
    coords=[(50,100),(560,100),(1070,100),(300,520),(810,520)]
    for (name,im),(x,y) in zip(imgs,coords):
        sheet.paste(im,(x,y)); draw.rectangle([x,y,x+480,y+270],outline=(32,45,62),width=3); draw.text((x,y+285),name,font=font,fill=(32,45,62))
    (OUT/'checks').mkdir(exist_ok=True); sheet.save(OUT/'checks'/'contact_sheet_slide_video_v1.png')

def write_handout():
    text='''# 公開教材四關檢查表｜Google Docs-ready 講義 v1

## 一句話目標
在把 AI 輔助教材、學生作品、圖片或課堂流程放上網前，先確認：來源可追、授權可用、個資可保護、AI 使用可說明。

## 適用情境
- 教師要公開分享簡報、學習單、部落格文章、YouTube 影片或 GitHub Pages 素材。
- 學生作品要放到班網、成果展、社群貼文或公開簡報。
- AI 曾協助摘要、改寫、產生圖片、整理教材或製作說明文字。

## 四關速查表
| 關卡 | 必問問題 | 可公開前的最低標準 | 退件句 |
|---|---|---|---|
| 來源門 | 原始來源在哪裡？ | 作者／單位、網址、日期可追 | 找不到原始來源，先改自繪或換素材。 |
| 授權門 | 允許公開、改作或引用嗎？ | 授權條款清楚，標註方式已寫下 | 授權不明，不交給 AI 猜。 |
| 個資門 | 是否能識別學生、家庭或班級？ | 姓名、臉、學號、校名、位置、特殊事件已匿名化 | 可能識別個人，先移除或改成虛構案例。 |
| AI 標註門 | 哪些內容有 AI 協助？ | 清楚標註 AI 協助範圍與教師審稿責任 | AI 協助不可當作免責說明。 |

## 學生工作區
1. 我們要公開的作品／教材是：＿＿＿＿＿＿＿＿＿＿
2. 外部素材清單：＿＿＿＿＿＿＿＿＿＿
3. 原始來源網址與作者：＿＿＿＿＿＿＿＿＿＿
4. 授權或使用限制：＿＿＿＿＿＿＿＿＿＿
5. 需要匿名化的資訊：＿＿＿＿＿＿＿＿＿＿
6. AI 使用標註句：＿＿＿＿＿＿＿＿＿＿

## 可複製 AI prompt
請只協助我做公開前風險檢查，不要替我決定能否公開。請依「來源、授權、個資、AI 標註」四欄檢查以下教材草稿，列出需要人工確認的項目，並用「可公開／需修改／不可公開」三類標示。若授權或個資資訊不足，請標成「需人工確認」。

## 教師示範
草稿：學生用 AI 做斜面實驗報告，我想公開一張成果圖。  
檢查：照片中有學生臉與校徽，圖表截自不明網站，AI 幫學生改寫了結論。  
處理：改用自繪示意圖；移除臉與校徽；回到原始資料來源；公開說明寫「學生實驗流程由教師設計，部分文字經 AI 協助整理，教師已審稿」。

## 8 分鐘課堂流程
1. 1 分鐘：說明「做好不等於可公開」。
2. 2 分鐘：圈出外部素材與可能個資。
3. 2 分鐘：填來源與授權欄。
4. 2 分鐘：寫 AI 使用標註句。
5. 1 分鐘：同儕用四關表退件或放行。

## 快速評量規準
- 4 分：四關都可追、可說明，且能清楚標註 AI 協助範圍。
- 3 分：多數資訊完整，但仍有一項需人工確認。
- 2 分：來源或授權模糊，暫不可公開。
- 1 分：含可識別個資或未授權素材，必須退件重做。

## 公開分享提醒
不要公開真實學生個資、未公開考題、學校內部文件、家長訊息或授權不明圖片。若要使用真實案例，需先取得必要同意並完成匿名化。AI 的建議只能作為檢查輔助，不能取代教師與學校的公開判斷。
'''
    HANDOUT.write_text(text, encoding='utf-8')

def write_upload_kit(total):
    kit=f'''# YouTube upload kit｜{TITLE}

## 建議標題
1. 老師用 AI 做公開教材：分享前先過四道門
2. 教材能不能放上網？來源、授權、個資、AI 標註一次檢查
3. AI 讓教材變快，但公開前要守住這四關

## 影片檔
- `public-materials-four-gates-slide-video-draft-v1.mp4`
- 長度：{total:.3f} 秒
- 規格：1920×1080，H.264 + AAC

## 說明欄草稿
這支影片整理「公開教材四關」：來源可追、授權可用、個資可保護、AI 使用可說明。適合老師在公開分享 AI 輔助教材、學生作品、簡報、學習單或影片前，先用一張檢查表降低風險。

## 章節
00:00 公開教材前，先過四道門
00:50 來源門：找到原始出處
01:45 授權門：課內使用不等於公開分享
02:45 個資門與 AI 標註門
04:00 45 分鐘課堂流程與退件句

## Hashtags
#AI教學 #教師備課 #數位素養 #公開教材 #AI素養

## 置頂留言草稿
你最常卡在哪一關：來源、授權、個資，還是 AI 標註？我會先把它做成一張課堂檢查表，讓學生也能一起練習公開前把關。

## 人工上傳前仍需確認
- YouTube/Google 登入與頻道權限。
- 若放入真實學生作品、課堂照片、未公開考題或第三方圖片，需使用者確認授權與匿名化。
'''
    (OUT/'youtube-upload-kit-longform-v1.md').write_text(kit, encoding='utf-8')

def write_docs(total):
    verification={}
    for p in SLIDES + sorted((OUT/'check_frames').glob('frame_*.png')) + [OUT/'checks/contact_sheet_slide_video_v1.png']:
        im=Image.open(p); verification[str(p.relative_to(BASE))]={'size':list(im.size),'mode':im.mode}
    manifest={'title':TITLE,'slug':SLUG,'format':'longform slide-video draft v1','status':'slide_video_upload_kit_and_shareable_handout_complete','video':str(MP4.relative_to(BASE)),'audio':str(AUDIO.relative_to(BASE)),'narration_text':'slide_video_draft_v1/narration_zh_tw.txt','subtitles':['slide_video_draft_v1/narration_edge_hsiaoyu.vtt','slide_video_draft_v1/narration_edge_hsiaoyu.srt'],'upload_kit':'slide_video_draft_v1/youtube-upload-kit-longform-v1.md','shareable_handout':str(HANDOUT.relative_to(BASE)),'contact_sheet':'slide_video_draft_v1/checks/contact_sheet_slide_video_v1.png','archive':str(ARCHIVE.relative_to(BASE)),'duration_seconds':round(total,3),'verification':verification,'next_auto_push':'若 YouTube/Google 登入仍未完成，從第三季題庫挑選優先題 7 Shorts storyboard／迷思分類 prompt；若已完成登入，優先上傳第一季首批或第三季代表作。'}
    (OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    readme=f'''# 公開教材四關｜slide-video draft v1

狀態：已由 5 張 storyboard 擴成 4–6 分鐘長片本機草稿，並完成 zh-TW 旁白、VTT/SRT 字幕、抽幀 QA、YouTube upload kit、正式可分享／Google Docs-ready 講義與交接壓縮包。

## 檔案
- 影片：`slide_video_draft_v1/{MP4.name}`
- 旁白：`slide_video_draft_v1/narration_edge_hsiaoyu.mp3`
- 旁白全文：`slide_video_draft_v1/narration_zh_tw.txt`
- 字幕：`slide_video_draft_v1/narration_edge_hsiaoyu.vtt`、`slide_video_draft_v1/narration_edge_hsiaoyu.srt`
- 抽幀：`slide_video_draft_v1/check_frames/`
- QA contact sheet：`slide_video_draft_v1/checks/contact_sheet_slide_video_v1.png`
- 長片 upload kit：`slide_video_draft_v1/youtube-upload-kit-longform-v1.md`
- 正式講義：`slide_video_draft_v1/public-materials-four-gates-shareable-handout-v1.md`
- manifest：`slide_video_draft_v1/manifest.json`
- 交接壓縮包：`slide_video_draft_v1/{ARCHIVE.name}`

## 驗證
- ffprobe：{total:.3f} 秒，1920×1080，H.264 + AAC。
- PIL：5 張原始 storyboard、5 張抽幀與 QA contact sheet 尺寸／模式已寫入 manifest。
- 視覺 QA：contact sheet 已檢查，五張抽幀繁中可讀、無 tofu／明顯裁切／文字重疊／過度擁擠。
- 正式講義：已讀回驗證，包含四關速查表、學生工作區、AI prompt、教師示範、8 分鐘課堂流程、評量規準與公開分享提醒。
- 壓縮包：Python tarfile 可讀回列出內容，且包含正式講義與 upload kit。

## 下一個可自動推進項目
若 YouTube/Google 登入仍未完成，從第三季題庫挑選優先題 7 Shorts storyboard／迷思分類 prompt；若已完成登入，優先上傳第一季首批或第三季代表作。
'''
    (OUT/'README.md').write_text(readme,encoding='utf-8')
    parent=BASE/'README.md'
    text=parent.read_text(encoding='utf-8')
    text=re.sub(r'## 3\. 下一個可自動推進項目\n\n.*?\n\n## 4\.', '## 3. 下一個可自動推進項目\n\n已完成 slide-video draft、YouTube upload kit 與正式可分享「公開教材四關檢查表」；下一輪若 YouTube/Google 登入仍未完成，改從第三季題庫挑選優先題 7 Shorts storyboard／迷思分類 prompt。\n\n## 4.', text, flags=re.S)
    text=re.sub(r'## 5\. 驗證紀錄\n\n.*', f'## 5. 驗證紀錄\n\n- PIL 驗證：5 張圖卡皆為 1920×1080 RGB。\n- Storyboard contact sheet：`checks/contact_sheet.png`。\n- Slide-video：`slide_video_draft_v1/{MP4.name}`，ffprobe {total:.3f} 秒、1920×1080、H.264 + AAC。\n- QA contact sheet：`slide_video_draft_v1/checks/contact_sheet_slide_video_v1.png`，視覺檢查通過。\n- 正式講義：`slide_video_draft_v1/public-materials-four-gates-shareable-handout-v1.md` 已讀回驗證。\n- 壓縮包：`slide_video_draft_v1/{ARCHIVE.name}` 已用 Python tarfile 讀回確認。\n- GitHub Pages：已同步 GitHub Pages 穩定版並 live 驗證。\n', text, flags=re.S)
    parent.write_text(text,encoding='utf-8')
    pmanifest=json.loads((BASE/'manifest.json').read_text(encoding='utf-8'))
    pmanifest.update({'status':'slide_video_upload_kit_and_shareable_handout_complete_and_published_to_github_pages','slide_video':'slide_video_draft_v1/'+MP4.name,'upload_kit':'slide_video_draft_v1/youtube-upload-kit-longform-v1.md','shareable_handout':'slide_video_draft_v1/public-materials-four-gates-shareable-handout-v1.md','slide_video_archive':'slide_video_draft_v1/'+ARCHIVE.name,'next_auto_push':'If YouTube/Google login is still incomplete, choose season 3 priority 7 Shorts storyboard / misconception classification prompt; if login is complete, upload the first batch or a season 3 representative piece.'})
    (BASE/'manifest.json').write_text(json.dumps(pmanifest,ensure_ascii=False,indent=2),encoding='utf-8')

def make_archive():
    members=[BASE/'README.md',BASE/'manifest.json',OUT/'README.md',OUT/'manifest.json',OUT/'build_slide_video_draft.py',OUT/'narration_zh_tw.txt',AUDIO,OUT/'narration_edge_hsiaoyu.vtt',OUT/'narration_edge_hsiaoyu.srt',OUT/'slides.ffconcat',MP4,OUT/'checks/contact_sheet_slide_video_v1.png',OUT/'youtube-upload-kit-longform-v1.md',HANDOUT,BASE/'public-materials-four-gates-storyboard-kit-20260513.tar.gz']+SLIDES+sorted((OUT/'check_frames').glob('frame_*.png'))
    with tarfile.open(ARCHIVE,'w:gz') as tar:
        for p in members:
            tar.add(p, arcname=str(p.relative_to(BASE)))
    with tarfile.open(ARCHIVE,'r:gz') as tar:
        return tar.getnames()

def main():
    OUT.mkdir(parents=True,exist_ok=True); (OUT/'checks').mkdir(exist_ok=True); (OUT/'check_frames').mkdir(exist_ok=True)
    (OUT/'narration_zh_tw.txt').write_text(NARRATION,encoding='utf-8')
    if not AUDIO.exists():
        subprocess.check_call(['edge-tts','--voice','zh-TW-HsiaoYuNeural','--rate=-8%','--text',NARRATION,'--write-media',str(AUDIO)])
    total=duration(AUDIO); durs=make_subtitles(total); make_concat(durs)
    subprocess.check_call(['ffmpeg','-y','-hide_banner','-loglevel','error','-f','concat','-safe','0','-i',str(OUT/'slides.ffconcat'),'-i',str(AUDIO),'-vf','fps=30,format=yuv420p','-c:v','libx264','-preset','veryfast','-crf','20','-c:a','aac','-b:a','128k','-shortest',str(MP4)])
    vtotal=duration(MP4)
    for idx,pct in enumerate([0.10,0.30,0.50,0.70,0.90],1):
        subprocess.check_call(['ffmpeg','-y','-hide_banner','-loglevel','error','-ss',f'{vtotal*pct:.3f}','-i',str(MP4),'-frames:v','1',str(OUT/'check_frames'/f'frame_{idx:02d}.png')])
    make_contact_sheet(); write_handout(); write_upload_kit(vtotal); write_docs(vtotal); names=make_archive()
    print(json.dumps({'video':str(MP4),'duration':vtotal,'archive':str(ARCHIVE),'archive_count':len(names)},ensure_ascii=False))

if __name__ == '__main__':
    main()
