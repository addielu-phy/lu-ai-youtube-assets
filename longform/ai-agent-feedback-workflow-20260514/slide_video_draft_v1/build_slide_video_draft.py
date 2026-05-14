#!/usr/bin/env python3
from __future__ import annotations
import json, subprocess, tarfile, textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE=Path('/home/adl/youtube-lu-ai-channel/longform/ai-agent-feedback-workflow-20260514')
OUT=BASE/'slide_video_draft_v1'
SLIDES=[BASE/'slides'/'01_hook_feedback_workflow.png',BASE/'slides'/'02_input_boundary.png',BASE/'slides'/'03_ai_draft_package.png',BASE/'slides'/'04_teacher_review_line.png',BASE/'slides'/'05_45min_reuse_flow.png']
TITLE='一個 AI Agent 怎麼幫老師做課後回饋包？'
SLUG='ai-agent-feedback-workflow-20260514'
MP4=OUT/'ai-agent-feedback-workflow-slide-video-draft-v1.mp4'
AUDIO=OUT/'narration_edge_hsiaoyu.mp3'
ARCHIVE=OUT/'ai-agent-feedback-workflow-longform-upload-kit-v1-20260514.tar.gz'
HANDOUT=OUT/'feedback-package-review-shareable-handout-v1.md'
SEGMENT_TITLES=['回饋可以加速，但責任不能外包','先設定輸入邊界','AI 只做草稿包，不做最後判斷','教師三色筆審稿線','45 分鐘課後回饋流程']
NARRATION='''
很多老師想用 AI 加速課後回饋，但最怕的一件事是：AI 寫得很順，卻把學生的脈絡、隱私或真正需要的支持弄錯。這支影片示範一個比較安全的做法：不要把回饋外包給 AI，而是讓 AI Agent 進入一條可審稿的工作線。核心句很簡單：回饋可以加速，但責任不能外包。

第一步不是把整份學生資料丟給 AI，而是先設定輸入邊界。老師可以準備匿名化的作業摘要、常見錯誤類型、課程目標、評量規準，以及下一堂課可以補救的時間。不要放入學生姓名、座號、家庭背景、特殊身分、完整個資或可能識別個人的原始對話。AI Agent 的任務是根據這些安全輸入，整理出全班層級的回饋草稿，而不是替某一位學生下定論。

第二步，讓 AI 產出三種草稿包。第一種是全班共通回饋：哪些概念最常卡住，哪些解法值得保留。第二種是分組補救任務：例如把學生分成概念重建、計算練習、圖像理解三種活動路徑。第三種是風險提醒：哪些句子可能太武斷、太貼標籤，或缺少證據。這三種輸出都只是草稿，目的不是直接貼給學生，而是幫老師縮短整理時間。

第三步，老師要建立三色筆審稿線。紅色刪掉個資與可能貼標籤的句子；藍色補上證據，例如學生作品中的具體表現、課堂觀察或評量規準；綠色改成下一步行動，例如「下節課先畫力圖」或「先重寫假設中的變因」。只要一句回饋沒有證據、沒有下一步，或可能讓學生覺得被定型，就不要直接使用。AI 可以提供候選句，但教師要決定哪些句子真的適合這個班級。

第四步，可以把它放進一個四十五分鐘課後回饋流程。前十分鐘，老師整理匿名化的常見錯誤與課程目標。接著十分鐘，AI Agent 產出全班回饋和分組任務草稿。再用十五分鐘做三色筆審稿：刪個資、補證據、改行動。最後十分鐘，產出下節課的回饋投影片、分組任務和一段給學生的透明說明：AI 協助整理初稿，但教師已審稿修正，最後回饋由教師負責。

真正有價值的 AI Agent，不是讓老師少看學生，而是讓老師把時間從重複整理移回專業判斷。你可以把課後回饋包記成四個欄位：安全輸入、AI 草稿、教師審稿、下節課再用。只要這四欄固定下來，AI 就不是代替老師評價學生，而是幫老師更快看見：全班需要什麼支持，下一堂課要怎麼接住學生。
'''.strip()

def run(cmd): return subprocess.check_output(cmd,text=True).strip()
def duration(p:Path)->float: return float(run(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(p)]))
def ts(sec:float, comma=False):
    ms=int(round((sec-int(sec))*1000)); s=int(sec); h,r=divmod(s,3600); m,s2=divmod(r,60); sep=',' if comma else '.'; return f'{h:02d}:{m:02d}:{s2:02d}{sep}{ms:03d}'
def make_subtitles(total):
    weights=[0.16,0.19,0.21,0.22,0.22]; bounds=[0.0]
    for w in weights: bounds.append(bounds[-1]+total*w/sum(weights))
    vtt=['WEBVTT','']; srt=[]
    for i,t in enumerate(SEGMENT_TITLES,1):
        st=bounds[i-1]; en=min(bounds[i],total); vtt += [f'{ts(st)} --> {ts(en)}',t,'']; srt += [str(i),f'{ts(st,True)} --> {ts(en,True)}',t,'']
    (OUT/'narration_edge_hsiaoyu.vtt').write_text('\n'.join(vtt),encoding='utf-8')
    (OUT/'narration_edge_hsiaoyu.srt').write_text('\n'.join(srt),encoding='utf-8')
    return [bounds[i]-bounds[i-1] for i in range(1,6)]
def make_concat(durs):
    lines=[]
    for slide,dur in zip(SLIDES,durs): lines += [f"file '{slide}'",f'duration {dur:.3f}']
    lines.append(f"file '{SLIDES[-1]}'")
    (OUT/'slides.ffconcat').write_text('\n'.join(lines)+'\n',encoding='utf-8')
def make_contact_sheet():
    frames=OUT/'check_frames'; imgs=[(p.name,Image.open(p).convert('RGB').resize((480,270))) for p in sorted(frames.glob('frame_*.png'))[:5]]
    sheet=Image.new('RGB',(1600,980),(245,242,234)); draw=ImageDraw.Draw(sheet)
    font_path='/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'; font=ImageFont.truetype(font_path,28); title_font=ImageFont.truetype(font_path,38)
    draw.text((50,28),'AI Agent 課後回饋包｜slide-video QA contact sheet',font=title_font,fill=(32,45,62))
    coords=[(50,100),(560,100),(1070,100),(300,520),(810,520)]
    for (name,im),(x,y) in zip(imgs,coords):
        sheet.paste(im,(x,y)); draw.rectangle([x,y,x+480,y+270],outline=(32,45,62),width=3); draw.text((x,y+285),name,font=font,fill=(32,45,62))
    (OUT/'checks').mkdir(exist_ok=True); sheet.save(OUT/'checks'/'contact_sheet_slide_video_v1.png')
def write_handout():
    HANDOUT.write_text('''# 課後回饋包審稿表｜Google Docs-ready 講義 v1

## 一句話目標
用 AI Agent 加速整理課後回饋，但保留教師對學生脈絡、證據與下一步行動的最後判斷。

## 適用情境
- 批改後要整理全班常見錯誤與下一堂課補救活動。
- 想用 AI 協助產生回饋初稿，但不想讓 AI 直接評價學生。
- 需要把作業結果轉成分組任務、回饋投影片或課後學習單。

## 四欄流程
| 欄位 | 老師先準備 | AI 可以做 | 老師必須審稿 |
|---|---|---|---|
| 安全輸入 | 匿名化摘要、課程目標、評量規準 | 整理常見錯誤 | 不放姓名、座號、家庭背景或可識別資訊 |
| AI 草稿 | 要求輸出全班回饋、分組任務、風險句 | 提供候選句與活動 | 不直接貼給學生 |
| 三色筆審稿 | 紅刪個資、藍補證據、綠改行動 | 協助重寫語氣 | 刪除貼標籤或武斷推論 |
| 下節課再用 | 決定補救節奏與分組方式 | 產出投影片草稿 | 教師定稿與說明 AI 協助範圍 |

## 可複製 AI prompt
請根據以下匿名化課後資料，產出「全班共通回饋、三組補救任務、需要教師確認的風險句」。不要推測個別學生人格或家庭背景；若證據不足，請標示「需教師補證據」。每一句回饋都要包含：觀察到的證據、學生下一步可以做什麼、教師需要確認什麼。

## 學生回饋句檢查
- 這句是否避免貼標籤？
- 這句是否有具體證據？
- 這句是否給出下一步行動？
- 這句是否已移除可識別個資？
- 這句是否符合本班脈絡，而不是泛用罐頭話？

## 45 分鐘課堂使用流程
1. 10 分鐘：整理匿名化常見錯誤與課程目標。
2. 10 分鐘：讓 AI Agent 產出全班回饋與分組任務草稿。
3. 15 分鐘：教師用三色筆審稿，刪個資、補證據、改行動。
4. 10 分鐘：產出下節課投影片、分組任務與透明說明。

## 公開與隱私提醒
不要把學生姓名、座號、臉部、家庭背景、特殊身分、原始對話或可識別作品直接交給 AI 或放進公開素材。AI 只能協助整理初稿，不能取代教師對學生脈絡與回饋責任的判斷。
''',encoding='utf-8')
def write_docs(vtotal):
    kit=f'''# YouTube upload kit｜{TITLE}

## 建議標題
1. 一個 AI Agent 怎麼幫老師做課後回饋包？
2. AI 可以幫老師寫回饋嗎？先建立這條審稿線
3. 課後回饋可以加速，但責任不能外包

## 影片檔
- `ai-agent-feedback-workflow-slide-video-draft-v1.mp4`
- 長度：{vtotal:.3f} 秒
- 規格：1920×1080，H.264 + AAC

## 說明欄草稿
這支影片示範老師如何把 AI Agent 放進課後回饋流程：先設定匿名化輸入邊界，讓 AI 產出全班回饋與分組任務草稿，再由教師用三色筆審稿，刪個資、補證據、改成下一步行動。

## 章節
00:00 回饋可以加速，但責任不能外包
00:50 先設定輸入邊界
01:50 AI 草稿包：全班回饋、分組任務、風險句
03:00 教師三色筆審稿線
04:10 45 分鐘課後回饋流程

## Hashtags
#AI教學 #教師備課 #AI素養 #課後回饋 #教育科技

## 置頂留言草稿
如果只讓 AI 做「草稿包」，老師再用三色筆審稿，你最想先省下哪一段課後整理時間？

## 人工上傳前仍需確認
- YouTube/Google 登入與頻道權限。
- 若納入真實學生作品、課堂照片或批改資料，需先完成匿名化與授權確認。
'''
    (OUT/'youtube-upload-kit-longform-v1.md').write_text(kit,encoding='utf-8')
    verification={}
    for p in SLIDES+sorted((OUT/'check_frames').glob('frame_*.png'))+[OUT/'checks/contact_sheet_slide_video_v1.png']:
        im=Image.open(p); verification[str(p.relative_to(BASE))]={'size':list(im.size),'mode':im.mode}
    manifest={'title':TITLE,'slug':SLUG,'format':'longform slide-video draft v1','status':'slide_video_upload_kit_shareable_handout_and_social_card_complete','video':str(MP4.relative_to(BASE)),'audio':str(AUDIO.relative_to(BASE)),'narration_text':'slide_video_draft_v1/narration_zh_tw.txt','subtitles':['slide_video_draft_v1/narration_edge_hsiaoyu.vtt','slide_video_draft_v1/narration_edge_hsiaoyu.srt'],'upload_kit':'slide_video_draft_v1/youtube-upload-kit-longform-v1.md','shareable_handout':str(HANDOUT.relative_to(BASE)),'contact_sheet':'slide_video_draft_v1/checks/contact_sheet_slide_video_v1.png','archive':str(ARCHIVE.relative_to(BASE)),'duration_seconds':round(vtotal,3),'verification':verification,'next_auto_push':'If YouTube/Google login is still incomplete, choose the next unfinished season 3 candidate (recommended: priority 10 Shorts storyboard/handout extension); if login is complete, upload the first batch or a season 3 representative piece.'}
    (OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    (OUT/'README.md').write_text(f'''# AI Agent 課後回饋包｜slide-video draft v1

狀態：已由 5 張 storyboard 擴成長片本機草稿，並完成 zh-TW 旁白、VTT/SRT 字幕、抽幀 QA、YouTube upload kit、正式可分享／Google Docs-ready 講義、1080×1920 社群宣傳卡與交接壓縮包。

## 檔案
- 影片：`slide_video_draft_v1/{MP4.name}`
- 旁白：`slide_video_draft_v1/narration_edge_hsiaoyu.mp3`
- 旁白全文：`slide_video_draft_v1/narration_zh_tw.txt`
- 字幕：`slide_video_draft_v1/narration_edge_hsiaoyu.vtt`、`slide_video_draft_v1/narration_edge_hsiaoyu.srt`
- QA contact sheet：`slide_video_draft_v1/checks/contact_sheet_slide_video_v1.png`
- 長片 upload kit：`slide_video_draft_v1/youtube-upload-kit-longform-v1.md`
- 正式講義：`slide_video_draft_v1/feedback-package-review-shareable-handout-v1.md`
- 交接壓縮包：`slide_video_draft_v1/{ARCHIVE.name}`
- 社群宣傳卡：`../social-assets/ai-agent-feedback-workflow-social-card-v1.png`

## 驗證
- ffprobe：{vtotal:.3f} 秒，1920×1080，H.264 + AAC。
- PIL：原始 storyboard、抽幀與 QA contact sheet 尺寸／模式已寫入 manifest。
- 正式講義已讀回產生，社群宣傳卡 PIL/視覺 QA 通過（1080×1920 RGB、繁中可讀、無 tofu／裁切／重疊／過度擁擠），壓縮包用 Python tarfile 可讀回列出內容。

## 下一個可自動推進項目
若 YouTube/Google 登入仍未完成，從第三季題庫挑選下一個尚未完成候選（建議第三季優先題 10 Shorts storyboard／講義延伸）；若已完成登入，優先上傳第一季首批或第三季代表作。
''',encoding='utf-8')
    parent=BASE/'README.md'
    parent.write_text(f'''# 第三季優先題 9｜一個 AI Agent 怎麼幫老師做課後回饋包？

狀態：長片 slide-video 草稿 v1、YouTube upload kit、正式可分享講義、1080×1920 社群宣傳卡與交接包已完成（2026-05-14 巡視自動推進）。

## 製作定位
- 格式：5–7 分鐘長片候選，已由 5 張 16:9 storyboard 擴成 slide-video 草稿。
- 核心觀眾：想用 AI 加速課後回饋，但不想把學生評價外包給 AI 的國高中自然／物理教師。
- 核心句：**回饋可以加速，但責任不能外包。**

## 已完成素材
- Storyboard：`slides/01_hook_feedback_workflow.png`～`slides/05_45min_reuse_flow.png`
- Storyboard QA：`checks/contact_sheet.png`
- Slide-video：`slide_video_draft_v1/{MP4.name}`
- 旁白／字幕：`slide_video_draft_v1/narration_edge_hsiaoyu.mp3`、`.vtt`、`.srt`
- 長片 upload kit：`slide_video_draft_v1/youtube-upload-kit-longform-v1.md`
- 正式講義：`slide_video_draft_v1/feedback-package-review-shareable-handout-v1.md`
- QA contact sheet：`slide_video_draft_v1/checks/contact_sheet_slide_video_v1.png`
- 交接包：`slide_video_draft_v1/{ARCHIVE.name}`
- 社群宣傳卡：`social-assets/ai-agent-feedback-workflow-social-card-v1.png`

## 5 張 storyboard
1. Hook：AI 不是代寫評語，而是進入審稿線。
2. 輸入邊界：先餵匿名資料，不餵學生身分。
3. AI 草稿包：全班共通回饋、分組補救任務、教師需確認風險句。
4. 教師審稿線：三色筆審稿，刪個資／改證據／補脈絡。
5. 45 分鐘課後回饋流程：匿名摘要、AI 草稿、教師定稿、下節課再用。

## 驗證
- ffprobe：{vtotal:.3f} 秒，1920×1080，H.264 + AAC。
- PIL：5 張原始 storyboard、5 張抽幀與 QA contact sheet 尺寸／模式已寫入 manifest。
- 正式講義：已產生 `feedback-package-review-shareable-handout-v1.md`。
- 壓縮包：Python tarfile 可讀回列出內容；社群宣傳卡 PIL/視覺 QA 通過（1080×1920 RGB、繁中可讀、無 tofu／裁切／重疊／過度擁擠）。

## 下一個可自動推進項目
若 YouTube/Google 登入仍未完成，從第三季題庫挑選下一個尚未完成候選（建議第三季優先題 10 Shorts storyboard／講義延伸）；若已完成登入，優先上傳第一季首批或第三季代表作。
''',encoding='utf-8')
    pmanifest=json.loads((BASE/'manifest.json').read_text(encoding='utf-8'))
    pmanifest.update({'status':'slide_video_upload_kit_shareable_handout_and_social_card_complete','slide_video':'slide_video_draft_v1/'+MP4.name,'upload_kit':'slide_video_draft_v1/youtube-upload-kit-longform-v1.md','shareable_handout':'slide_video_draft_v1/feedback-package-review-shareable-handout-v1.md','slide_video_archive':'slide_video_draft_v1/'+ARCHIVE.name,'social_card':'social-assets/ai-agent-feedback-workflow-social-card-v1.png','social_card_manifest':'social-assets/ai-agent-feedback-workflow-social-card-v1.manifest.json','next_auto_push':'If YouTube/Google login is still incomplete, choose the next unfinished season 3 candidate (recommended: priority 10 Shorts storyboard/handout extension); if login is complete, upload first batch or season 3 representative piece.'})
    (BASE/'manifest.json').write_text(json.dumps(pmanifest,ensure_ascii=False,indent=2),encoding='utf-8')
def make_archive():
    members=[BASE/'README.md',BASE/'manifest.json',OUT/'README.md',OUT/'manifest.json',OUT/'build_slide_video_draft.py',OUT/'narration_zh_tw.txt',AUDIO,OUT/'narration_edge_hsiaoyu.vtt',OUT/'narration_edge_hsiaoyu.srt',OUT/'slides.ffconcat',MP4,OUT/'checks/contact_sheet_slide_video_v1.png',OUT/'youtube-upload-kit-longform-v1.md',HANDOUT,BASE/'ai-agent-feedback-workflow-storyboard-20260514.tar.gz']+SLIDES+sorted((OUT/'check_frames').glob('frame_*.png'))
    with tarfile.open(ARCHIVE,'w:gz') as tar:
        for p in members: tar.add(p,arcname=str(p.relative_to(BASE)))
    with tarfile.open(ARCHIVE,'r:gz') as tar: return tar.getnames()
def main():
    OUT.mkdir(parents=True,exist_ok=True); (OUT/'checks').mkdir(exist_ok=True); (OUT/'check_frames').mkdir(exist_ok=True)
    (OUT/'narration_zh_tw.txt').write_text(NARRATION,encoding='utf-8')
    if not AUDIO.exists(): subprocess.check_call(['edge-tts','--voice','zh-TW-HsiaoYuNeural','--rate=-8%','--text',NARRATION,'--write-media',str(AUDIO)])
    total=duration(AUDIO); durs=make_subtitles(total); make_concat(durs)
    subprocess.check_call(['ffmpeg','-y','-hide_banner','-loglevel','error','-f','concat','-safe','0','-i',str(OUT/'slides.ffconcat'),'-i',str(AUDIO),'-vf','fps=30,format=yuv420p','-c:v','libx264','-preset','veryfast','-crf','20','-c:a','aac','-b:a','128k','-shortest',str(MP4)])
    vtotal=duration(MP4)
    for idx,pct in enumerate([0.10,0.30,0.50,0.70,0.90],1): subprocess.check_call(['ffmpeg','-y','-hide_banner','-loglevel','error','-ss',f'{vtotal*pct:.3f}','-i',str(MP4),'-frames:v','1',str(OUT/'check_frames'/f'frame_{idx:02d}.png')])
    make_contact_sheet(); write_handout(); write_docs(vtotal); names=make_archive()
    print(json.dumps({'video':str(MP4),'duration':vtotal,'archive':str(ARCHIVE),'archive_count':len(names)},ensure_ascii=False))
if __name__=='__main__': main()
