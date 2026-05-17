# Shorts｜AI 給答案前，先叫它列出三個可驗證證據

狀態：2026-05-12 每小時雷達已把 storyboard 擴成 35 秒本機 Shorts 草稿、封面、字幕與 YouTube upload kit。  
來源：第三季內容題庫優先題 1。

## 成果檔案

- Shorts MP4：`three-verifiable-evidence-before-answer-shorts-35s.mp4`
- 推薦 Lu 旁白版：`three-verifiable-evidence-before-answer-shorts-35s-lu-f5tts-v1.mp4`
- 封面：`cover_three_verifiable_evidence_v1.png`
- 上傳包：`youtube-upload-kit.md`
- 教師追問小抄：`three-evidence-question-cheatsheet-v1.md`
- 原旁白：`narration_35s_edge_hsiaoyu.mp3`
- Lu 旁白：`narration_35s_lu_f5tts_v1.mp3` / `narration_35s_lu_f5tts_v1.wav`
- 字幕：`narration_35s_edge_hsiaoyu.vtt` / `narration_35s_edge_hsiaoyu.srt`
- QA sheet：`checks/qa_sheet_mp4.png`
- Lu QA sheet：`checks/qa_lu_f5v1_sheet.png`
- 壓縮包：`three-verifiable-evidence-before-answer-upload-kit-20260512.tar.gz`
- Lu 交接包：`three-verifiable-evidence-before-answer-lu-f5tts-v1-kit-20260518.tar.gz`

## 圖卡

1. `slides/slide_01.png`｜AI 給答案前，先要三個證據
2. `slides/slide_02.png`｜用一題問題把證據列出來
3. `slides/slide_03.png`｜不要只問 AI：答案是什麼？
4. `slides/slide_04.png`｜三欄證據卡 5 分鐘就能做
5. `slides/slide_05.png`｜老師把關句與 CTA

## 驗證

- MP4：1080×1920、25fps、H.264 + AAC、約 35 秒。
- PIL：封面、5 張圖卡與 QA 抽幀皆為 RGB 圖檔。
- 視覺 QA：`checks/qa_sheet_mp4.png` 已用於檢查繁中可讀、無 tofu 方塊、無裁切、無重疊與不過度擁擠。
- 教師追問小抄：已讀回驗證，可直接複製到 Google Docs／課堂講義。
- 壓縮包：已用 Python `tarfile` 讀回確認包含 MP4、封面、旁白、字幕、README、manifest、upload kit、教師追問小抄、slides 與 QA sheet。

## 穩定發布

- 手機索引：`https://addielu-phy.github.io/lu-ai-youtube-assets/mobile-index/index.html`
- 本機 package：`shorts/three-verifiable-evidence-before-answer-20260512/`
- GitHub Pages commit：content commit `8fd55e5`、cleanup commit `7d42b86` 已 live 驗證。

## 下一個自動推進

若 YouTube/Google 登入仍未完成：從第三季題庫挑選下一個尚未完成的 Shorts storyboard／講義延伸。  
若使用者已完成 YouTube/Google 登入：優先上傳已完成的第一季首批 Shorts 或本支第三季 Shorts。

## 音訊升級 v1（Lu Teacher F5-TTS）

- 改善原因：原版使用 zh-TW Edge HsiaoYu 女聲草稿；本版改用盧老師 F5-TTS voice clone。
- 推薦版 MP4：`three-verifiable-evidence-before-answer-shorts-35s-lu-f5tts-v1.mp4`
- 升級版旁白：`narration_35s_lu_f5tts_v1.mp3` / `narration_35s_lu_f5tts_v1.wav`
- 升級版字幕：`narration_35s_lu_f5tts_v1.vtt` / `narration_35s_lu_f5tts_v1.srt`
- QA sheet：`checks/qa_lu_f5v1_sheet.png`
- 音訊處理：F5-TTS chunked generation、0.22 秒短停頓、loudnorm I=-16、AAC 192k、35 秒完整輸出。

