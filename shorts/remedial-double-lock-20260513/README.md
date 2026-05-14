# Shorts｜補救教學題目請 AI 出，但先鎖住哪兩件事？

狀態：2026-05-14 每小時雷達已把 storyboard 擴成 35 秒本機 Shorts 草稿、封面、字幕、YouTube upload kit，並新增「補救雙鎖教師檢查表」。  
來源：第三季內容題庫優先題 8「補救雙鎖」。

## 成果檔案
- Shorts MP4：`remedial-double-lock-shorts-35s.mp4`
- 封面：`cover_remedial_double_lock_v1.png`
- 旁白：`narration_35s_edge_hsiaoyu.mp3`
- 字幕：`narration_35s_edge_hsiaoyu.vtt` / `narration_35s_edge_hsiaoyu.srt`
- YouTube upload kit：`youtube-upload-kit.md`
- 教師檢查表：`remedial-double-lock-teacher-checklist-v1.md`
- QA sheet：`checks/qa_sheet_mp4.png`
- 交接壓縮包：`remedial-double-lock-upload-kit-20260514.tar.gz`

## 驗證
- MP4：1080×1920、25fps、H.264 yuv420p + AAC、約 35 秒。
- PIL：封面／抽幀／QA sheet 皆為 RGB。
- 視覺 QA：封面與抽幀繁中可讀、無 tofu／裁切／嚴重重疊／過度擁擠。
- 壓縮包：已用 Python tarfile 讀回確認包含主檔、封面、旁白、字幕、README、manifest、upload kit、教師檢查表、slides、QA sheet 與腳本。

## GitHub Pages 穩定連結
- 發布狀態：已同步並 live 驗證 content commit `9486d53`。
- 手機索引：`https://addielu-phy.github.io/lu-ai-youtube-assets/mobile-index/index.html`
- 本包 README：同步後位於 `https://addielu-phy.github.io/lu-ai-youtube-assets/shorts/remedial-double-lock-20260513/README.md`
- MP4：同步後位於 `https://addielu-phy.github.io/lu-ai-youtube-assets/shorts/remedial-double-lock-20260513/remedial-double-lock-shorts-35s.mp4`

## 下一個自動推進
若 YouTube/Google 登入仍未完成：從第三季題庫挑選下一個尚未完成 storyboard／講義延伸。  
若使用者已完成 YouTube/Google 登入：優先上傳第一季首批或本支第三季 Shorts。
