# Shorts｜AI 幫忙回饋作業，老師不能跳過哪一步？

狀態：2026-05-12 每小時雷達已由 storyboard package v1 擴成 35 秒本機 Shorts 草稿、封面、旁白、字幕、YouTube upload kit、教師檢查表與交接壓縮包。
來源：第二季內容題庫優先題 11。

## 主檔
- 影片：`homework-feedback-teacher-review-shorts-35s.mp4`
- 封面：`cover_homework_feedback_teacher_review_v1.png`
- 上傳包：`youtube-upload-kit.md`
- 教師檢查表：`ai-feedback-review-teacher-checklist-v1.md`
- 旁白：`narration_35s_edge_hsiaoyu.mp3`
- 字幕：`narration_35s_edge_hsiaoyu.vtt`、`narration_35s_edge_hsiaoyu.srt`
- 壓縮包：`homework-feedback-teacher-review-upload-kit-20260512.tar.gz`

## 圖卡
1. `slides/slide_01.png`｜AI 回饋很快，但不能直接轉貼
2. `slides/slide_02.png`｜老師先審語氣
3. `slides/slide_03.png`｜再審概念
4. `slides/slide_04.png`｜最後補下一步
5. `slides/slide_05.png`｜AI 是初稿，老師做最後審稿

## 驗證
- storyboard：5 張 `1080×1920` RGB PNG；原 contact sheet：`checks/contact_sheet.png`。
- 影片：ffprobe 驗證 `1080×1920`、25fps、H.264 + AAC、35.000 秒。
- QA sheet：`checks/qa_cover_frames_sheet.png`，包含封面與 2s／12s／24s／33s 抽幀。
- 壓縮包：已用 Python tarfile 讀回驗證包含影片、封面、旁白、字幕、README、manifest、upload kit、教師檢查表、slides、QA sheet 與腳本。

## 下一個自動推進
若 YouTube/Google 登入仍未完成：下一輪改製作第二季優先題 6 長片 storyboard／退件規準講義草稿。  
若使用者已完成 YouTube/Google 登入：優先上傳第一季首批或本支第二季 Shorts。
