# Shorts｜學生用 AI 前，先寫一句「我預期會看到什麼」

狀態：2026-05-12 每小時雷達已由 storyboard package v1 擴成 35 秒本機 Shorts 草稿、封面、旁白、字幕、YouTube upload kit 與交接壓縮包。
來源：第二季內容題庫優先題 7。

## 主檔
- 影片：`student-prediction-before-ai-shorts-35s.mp4`
- 封面：`cover_student_prediction_before_ai_v1.png`
- 上傳包：`youtube-upload-kit.md`
- 旁白：`narration_35s_edge_hsiaoyu.mp3`
- 字幕：`narration_35s_edge_hsiaoyu.vtt`、`narration_35s_edge_hsiaoyu.srt`
- 壓縮包：`student-prediction-before-ai-upload-kit-20260512.tar.gz`

## 圖卡
1. `slides/slide_01.png`｜學生用 AI 前，先寫一句預測
2. `slides/slide_02.png`｜把問題變成可檢查的預測
3. `slides/slide_03.png`｜AI 回答後，不只問對錯
4. `slides/slide_04.png`｜一張 3 欄表就能開始
5. `slides/slide_05.png`｜老師把關句與 CTA

## 驗證
- storyboard：5 張 `1080×1920` RGB PNG；原 contact sheet：`checks/contact_sheet.png`。
- 影片：ffprobe 驗證 `1080×1920`、25fps、H.264 + AAC、35.000 秒。
- QA sheet：`checks/qa_cover_frames_sheet.png`，包含封面與 2s／12s／24s／33s 抽幀。
- 壓縮包：已用 Python tarfile 讀回驗證包含影片、封面、旁白、字幕、README、manifest、upload kit、slides、QA sheet 與腳本。

## 下一個自動推進
若 YouTube/Google 登入仍未完成：從第二季題庫挑選尚未完成的下一支 Shorts storyboard／講義延伸。  
若使用者已完成 YouTube/Google 登入：優先上傳第一季首批或本支第二季 Shorts。
