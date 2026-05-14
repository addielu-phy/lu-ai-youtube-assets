# Shorts package｜學生問 AI 之前，先畫一張「我知道／我不知道」圖

狀態：2026-05-15 每小時雷達已由 storyboard 擴成本機 35 秒 Shorts 草稿、封面、字幕、YouTube upload kit、學生學習單與交接壓縮包。  
來源：第三季內容題庫優先題 10。

## 主檔
- 影片：`known-unknown-boundary-map-shorts-35s.mp4`
- 封面：`cover_known_unknown_boundary_map_v1.png`
- 上傳包：`youtube-upload-kit.md`
- 學生學習單：`known-unknown-boundary-map-student-worksheet-v1.md`
- 壓縮包：`known-unknown-boundary-map-upload-kit-20260515.tar.gz`

## 原始圖卡
1. `slides/slide_01.png`｜學生問 AI 前，先畫一張圖
2. `slides/slide_02.png`｜直接問 AI，常常變成猜答案
3. `slides/slide_03.png`｜老師可複製句：請你照我的邊界圖回覆
4. `slides/slide_04.png`｜把模糊問題改成可檢查問題
5. `slides/slide_05.png`｜一張 T-chart，讓學生先負責

## 驗證
- 影片：1080×1920、25fps、H.264 + AAC、約 35.000 秒。
- 圖卡與封面：PIL 驗證 1080×1920 RGB。
- QA sheet：`checks/qa_cover_frames_sheet.png`。
- 交接包：Python tarfile 已讀回確認包含 MP4、封面、字幕、upload kit、學生學習單、圖卡與 QA sheet。
- GitHub Pages：content commit `14d24e5` 已 live 驗證 index／MP4／封面／upload kit／學生學習單皆 HTTP 200；手機索引卡片與 console 已驗證。
- 穩定索引：`https://addielu-phy.github.io/lu-ai-youtube-assets/mobile-index/index.html`。

## 下一個自動推進
若 YouTube/Google 登入仍未完成：從第三季題庫挑選下一個尚未完成的 Shorts storyboard／講義延伸；若已登入，優先上傳第一季首批或本支第三季 Shorts。
