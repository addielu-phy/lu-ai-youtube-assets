# 第二季優先題 8｜讓學生幫 AI 打分：不是對錯，是證據夠不夠

狀態：已從本機 Shorts storyboard 擴成 35 秒 zh-TW 旁白 Shorts 草稿、封面、字幕、YouTube upload kit 與交接壓縮包。

## 30 秒製作簡報
- 3 秒鉤子：答案對一半時，分數怎麼給？
- 核心觀點：不要只問 AI 答案「對不對」，要讓學生用規準判斷「證據夠不夠」。
- 老師把關句：證據在哪裡？這句有條件嗎？
- 課堂延伸：4 格評分規準（概念、證據、條件、圖像／單位）＋一句扣分理由。

## 成品檔案
- 影片：`evidence-rubric-ai-answer-shorts-35s.mp4`
- 封面：`cover_evidence_rubric_ai_answer_v1.png`
- 上傳包：`youtube-upload-kit.md`
- 教師可列印講義：`evidence-rubric-teacher-printable-v1.md`
- 旁白：`narration_35s_edge_hsiaoyu.mp3`
- 字幕：`narration_35s_edge_hsiaoyu.vtt` / `narration_35s_edge_hsiaoyu.srt`
- QA：`checks/qa_sheet_video_v1.png`
- 壓縮包：`evidence-rubric-ai-answer-upload-kit-20260512.tar.gz`

## Storyboard 圖卡
1. `slides/slide_01.png` Hook：答案對一半，分數怎麼給？
2. `slides/slide_02.png` Case：AI 回答看起來很順，但缺證據。
3. `slides/slide_03.png` Rubric：四格評分規準。
4. `slides/slide_04.png` Activity：讓學生幫 AI 打分。
5. `slides/slide_05.png` CTA：把懷疑變成規準。

## 已驗證
- 影片 ffprobe：1080×1920、25fps、H.264 yuv420p + AAC、35.000 秒。
- 旁白：zh-TW-HsiaoYuNeural，約 32.928 秒，影片尾段以靜音補足 35 秒。
- PIL：5 張圖卡與封面皆為 1080×1920 RGB；QA sheet 已重建。
- 視覺 QA：二次檢查通過，繁中可讀，無 tofu／裁切／重疊／過度擁擠；封面標題行距、middle 頁換行、QA 標籤皆已修正。
- 教師講義：`evidence-rubric-teacher-printable-v1.md` 已讀回驗證，可作為 Google Docs-ready 可列印評分規準。
- 壓縮包：已用 Python tarfile 讀回驗證，包含 23 個交接項目，含教師講義。

## 下一個可自動推進項目
「AI 回答證據評分規準」可列印講義已完成。若 YouTube/Google 登入仍未完成，下一輪改從第二季題庫挑選尚未完成的下一支 Shorts storyboard／講義延伸；若已完成登入，優先上傳第一季首批或本支第二季 Shorts。
