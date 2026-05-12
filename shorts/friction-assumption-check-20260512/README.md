# Shorts｜AI 說「忽略摩擦」時，老師要問的一句話

狀態：2026-05-12 每小時雷達已由 storyboard package v1 擴成 35 秒本機 Shorts 草稿、封面、旁白、字幕、YouTube upload kit、教師檢查表與交接壓縮包。
來源：第二季內容題庫優先題 10。

## 主檔
- 影片：`friction-assumption-check-shorts-35s.mp4`
- 封面：`cover_friction_assumption_check_v1.png`
- 上傳包：`youtube-upload-kit.md`
- 教師檢查表：`friction-assumption-teacher-checklist-v1.md`
- 旁白：`narration_35s_edge_hsiaoyu.mp3`
- 字幕：`narration_35s_edge_hsiaoyu.vtt`、`narration_35s_edge_hsiaoyu.srt`
- 壓縮包：`friction-assumption-check-upload-kit-20260512.tar.gz`

## 圖卡
1. `slides/slide_01.png`｜AI 說忽略摩擦，先別急著抄
2. `slides/slide_02.png`｜一句「忽略摩擦」藏了模型假設
3. `slides/slide_03.png`｜摩擦假設三問
4. `slides/slide_04.png`｜學生圈出被忽略的東西
5. `slides/slide_05.png`｜假設是假答案的開關

## 驗證
- storyboard：5 張 `1080×1920` RGB PNG；原 contact sheet：`checks/contact_sheet.png`。
- 影片：ffprobe 驗證 `1080×1920`、25fps、H.264 + AAC、35.000 秒。
- QA sheet：`checks/qa_cover_frames_sheet.png`，包含封面與 2s／12s／24s／33s 抽幀。
- 壓縮包：已用 Python tarfile 讀回驗證包含影片、封面、旁白、字幕、README、manifest、upload kit、教師檢查表、slides、QA sheet 與腳本。

## 下一個自動推進
若 YouTube/Google 登入仍未完成：下一輪改製作第二季優先題 6 長片 storyboard／退件規準講義草稿。  
若使用者已完成 YouTube/Google 登入：優先上傳第一季首批或本支第二季 Shorts。
