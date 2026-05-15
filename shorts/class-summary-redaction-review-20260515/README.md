# Shorts package｜AI 生成的課堂摘要，老師要刪掉哪一種句子？

狀態：2026-05-15 每小時雷達已由 storyboard 擴成本機 35 秒 Shorts 草稿、封面、字幕、YouTube upload kit、教師檢查表與交接壓縮包。  
來源：第三季內容題庫優先題 11。

## 主檔
- 影片：`class-summary-redaction-review-shorts-35s.mp4`
- 封面：`cover_class_summary_redaction_review_v1.png`
- 上傳包：`youtube-upload-kit.md`
- 教師檢查表：`summary-redaction-teacher-checklist-v1.md`
- 壓縮包：`class-summary-redaction-review-upload-kit-20260515.tar.gz`

## 原始圖卡
1. `slides/slide_01.png`｜摘要越順，越要先審
2. `slides/slide_02.png`｜順口的摘要，可能藏個資與標籤
3. `slides/slide_03.png`｜丟給 AI 前，先加一條紅線
4. `slides/slide_04.png`｜把學生標籤，改成學習線索
5. `slides/slide_05.png`｜三種句子，摘要完成前先刪

## 驗證
- 影片：1080×1920、25fps、H.264 + AAC、約 35.000 秒。
- 圖卡與封面：PIL 驗證 1080×1920 RGB。
- QA sheet：`checks/qa_cover_frames_sheet.png`。
- 交接包：Python tarfile 已讀回確認包含 MP4、封面、字幕、upload kit、教師檢查表、圖卡與 QA sheet。

## 下一個自動推進
若 YouTube/Google 登入仍未完成：從第三季題庫挑選下一個尚未完成的 Shorts storyboard／講義延伸；若已登入，優先上傳第一季首批或本支第三季 Shorts。


## 音訊升級 v1（Lu Teacher F5-TTS）

- 改善原因：原版使用 Edge HsiaoYu 女聲旁白；本版改用盧老師 F5-TTS voice clone。
- 升級版 MP4：`class-summary-redaction-review-shorts-35s-lu-f5tts-v1.mp4`
- 升級版旁白：`narration_35s_lu_f5tts_v1.mp3` / `narration_35s_lu_f5tts_v1.wav`
- 升級版字幕：`narration_35s_lu_f5tts_v1.vtt` / `narration_35s_lu_f5tts_v1.srt`
- 音訊處理：F5-TTS chunked generation、0.22 秒短停頓、loudnorm I=-16、AAC 192k、35 秒完整輸出。


## 音訊升級 v2（Lu Teacher F5-TTS）

- 改善原因：原版使用 Edge HsiaoYu 女聲旁白；本版改用盧老師 F5-TTS voice clone。
- 升級版 MP4：`class-summary-redaction-review-shorts-35s-lu-f5tts-v2.mp4`
- 升級版旁白：`narration_35s_lu_f5tts_v2.mp3` / `narration_35s_lu_f5tts_v2.wav`
- 升級版字幕：`narration_35s_lu_f5tts_v2.vtt` / `narration_35s_lu_f5tts_v2.srt`
- 音訊處理：F5-TTS chunked generation、0.22 秒短停頓、loudnorm I=-16、AAC 192k、35 秒完整輸出。
