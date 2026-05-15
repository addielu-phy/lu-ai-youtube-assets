# Shorts package｜讓 AI 幫忙寫家長訊息，第一版只准當草稿

狀態：2026-05-15 每小時雷達已從 storyboard package 擴成 35 秒 Shorts MP4／封面／字幕／YouTube upload kit，並保留教師審稿 checklist。  
來源：第三季內容題庫優先題 12。

## 核心觀點
AI 可以幫老師起草家長訊息，但第一版只准當草稿；送出前要過「事實、語氣、隱私」三關。

## 成果檔案
- 影片：`parent-message-draft-only-shorts-35s.mp4`
- 封面：`cover_parent_message_draft_only_v1.png`
- 旁白文字：`narration_35s.txt`
- 草稿旁白：`narration_35s_yunjhe.mp3`（zh-TW YunJhe 男聲，避免再用女聲草稿；使用者本人聲音仍待 voice-clone 樣本/工具）
- 字幕：`narration_35s_yunjhe.vtt`
- 上傳文案：`youtube-upload-kit.md`
- 教師審稿表：`parent-message-review-checklist-v1.md`
- QA：`checks/qa_sheet_mp4.png`、抽幀 `checks/frame_*.png`
- 壓縮包：`parent-message-draft-only-upload-kit-20260515.tar.gz`

## 原 storyboard 圖卡
1. `slides/slide_01.png`｜語氣很客氣，不代表能送出
2. `slides/slide_02.png`｜第一關：這件事真的發生嗎？
3. `slides/slide_03.png`｜第二關：從指責改成合作
4. `slides/slide_04.png`｜第三關：敏感資訊先拿掉
5. `slides/slide_05.png`｜送出前，用三句話退件

## 驗證
- PIL：封面與 5 張圖卡皆為 `1080×1920` RGB。
- ffprobe：影片為 1080×1920、H.264 + AAC、約 35 秒。
- 視覺 QA：封面與抽幀繁中可讀、無 tofu 方塊、無裁切、無嚴重重疊或過度擁擠。
- 壓縮包：已用 Python tarfile 讀回，包含 MP4、封面、字幕、upload kit、README、manifest、教師審稿表與 render/build scripts。

## 下一個自動推進
若 YouTube/Google 登入仍未完成：改挑下一個尚未完成的第三季/後續題庫候選，或先做頻道素材整體聲音替換盤點；不要重做本包。  
若已登入：優先上傳第一季首批或第三季代表作。

## 音訊升級 v1（Lu Teacher F5-TTS）

- 改善原因：原版使用 zh-TW YunJhe 男聲草稿；本版改用盧老師 F5-TTS voice clone。
- 推薦版 MP4：`parent-message-draft-only-shorts-35s-lu-f5tts-v1.mp4`
- 升級版旁白：`narration_35s_lu_f5tts_v1.mp3` / `narration_35s_lu_f5tts_v1.wav`
- 升級版字幕：`narration_35s_lu_f5tts_v1.vtt` / `narration_35s_lu_f5tts_v1.srt`
- 音訊處理：F5-TTS chunked generation、0.22 秒短停頓、loudnorm I=-16、AAC 192k、35 秒完整輸出。
- QA sheet：`checks/qa_lu_f5v1_sheet.png`（vision QA：繁中主文字可讀、無 tofu／裁切／重大重疊／過度擁擠）。

