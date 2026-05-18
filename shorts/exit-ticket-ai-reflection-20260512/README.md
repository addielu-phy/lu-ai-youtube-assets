# Shorts｜下課前 3 分鐘：讓學生寫 AI 使用反思

狀態：2026-05-12 每小時雷達已完成第二季優先題 12 的 35 秒本機 Shorts 草稿、封面、旁白、字幕、YouTube upload kit、教師可列印 Exit Ticket 與交接壓縮包。

## 主檔
- 影片：`exit-ticket-ai-reflection-shorts-35s.mp4`
- 封面：`cover_exit_ticket_ai_reflection_v1.png`
- 上傳包：`youtube-upload-kit.md`
- 教師講義：`exit-ticket-ai-reflection-teacher-printable-v1.md`
- QA：`checks/qa_cover_frames_sheet.png`
- 壓縮包：`exit-ticket-ai-reflection-upload-kit-20260512.tar.gz`

## 驗證
- 影片：ffprobe 驗證 `1080×1920`、25fps、H.264 + AAC、35.000 秒。
- 圖卡／封面／QA sheet：PIL 驗證 RGB 尺寸完成；視覺 QA 用 `checks/qa_cover_frames_sheet.png`。
- 壓縮包：已用 Python tarfile 讀回驗證包含影片、封面、字幕、講義、README、manifest、upload kit、slides、QA sheet 與腳本。

## 下一個自動推進
若 YouTube/Google 登入仍未完成：第二季優先題 6 可製作長片 storyboard／講義草稿；若已登入，優先上傳第一季首批或本支第二季 Shorts。

## 音訊升級 v1（Lu Teacher F5-TTS）

- 改善原因：原版使用 zh-TW Edge HsiaoYu 女聲草稿；本版改用盧老師 F5-TTS voice clone。
- 推薦版 MP4：`exit-ticket-ai-reflection-shorts-35s-lu-f5tts-v1.mp4`
- 升級版旁白：`narration_35s_lu_f5tts_v1.mp3` / `narration_35s_lu_f5tts_v1.wav`
- 升級版字幕：`narration_35s_lu_f5tts_v1.vtt` / `narration_35s_lu_f5tts_v1.srt`
- QA sheet：`checks/qa_lu_f5v1_sheet.png`
- 音訊處理：F5-TTS chunked generation、0.22 秒短停頓、loudnorm I=-16、AAC 192k、35 秒完整輸出。

