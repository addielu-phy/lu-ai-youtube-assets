# Shorts storyboard｜讓學生抓 AI 錯：一張 5 分鐘學習單

建立時間：2026-05-09 20:16 巡視自動推進  
更新時間：2026-05-09 22:27 巡視自動推進  
狀態：30 秒 brief、5 張 9:16 分鏡圖卡、35 秒本機 Shorts 草稿、封面、旁白、VTT、學習單草稿、正式老師可列印版學習單、YouTube upload kit 與交接壓縮包已完成。

## 30 秒製作 brief

- **主題**：把 AI 錯解變成 5 分鐘課堂活動，而不是只由老師單向糾錯。
- **核心觀眾**：國高中自然／物理老師、想讓學生練習判斷 AI 回答可信度的教師。
- **3 秒鉤子**：今天不是叫學生問 AI，而是叫學生抓 AI。
- **核心承諾**：只要一張三欄學習單，學生就能從「看答案」變成「找證據」。
- **格式**：9:16 Shorts，約 30–35 秒；先以靜態圖卡 + 旁白製作。
- **CTA**：留言「抓錯」，下支把這張學習單做成可複製版本。
- **人工作業／公開前檢查**：若要放真實學生作品或未公開題目，需使用者確認可公開；目前圖卡使用示意文字。

## 5 張分鏡圖卡

| 張 | 時間 | 畫面重點 | 旁白草稿 |
|---:|---:|---|---|
| 1 | 0–3s | 黑板式大標：今天不是問 AI，是抓 AI | 今天不是叫學生問 AI，而是叫學生抓 AI。 |
| 2 | 3–9s | 顯示 AI 錯解卡，標出「看起來很順」 | AI 的答案常常很順，但學生要練的是懷疑。 |
| 3 | 9–17s | 三欄學習單：AI 說法／我懷疑／我要驗證 | 一張 5 分鐘學習單，只留三欄就夠。 |
| 4 | 17–25s | 老師流程：丟題目 → 學生標疑點 → 找證據 | 老師不用每題重講，改成讓學生找證據。 |
| 5 | 25–33s | CTA：留言「抓錯」拿下一版學習單 | 想要可複製版，留言「抓錯」，我下一支整理。 |

## 檔案

- `render_storyboard.py`：可重跑的 deterministic PIL 產圖腳本。
- `finalize_static_draft.py`：產生封面、concat、VTT、manifest 與檢查 contact sheet 的 deterministic 腳本。
- `slides/slide_01.png` ~ `slides/slide_05.png`：1080×1920 分鏡圖卡。
- `narration_35s.txt`：35 秒版旁白稿。
- `narration_35s_hsiaoyu.mp3`：zh-TW HsiaoYu 旁白。
- `student-catches-ai-error-worksheet-35s.vtt`：上傳用字幕。
- `student-catches-ai-error-worksheet-35s.mp4`：35 秒本機 Shorts 草稿。
- `cover-student-catches-ai-error-worksheet.png`：Shorts 封面 PNG。
- `worksheet-draft-v1.md`：可複製三欄學習單草稿。
- `worksheet-teacher-printable-v1.md`：正式可列印／可貼到 Google Docs 的老師版學習單。
- `youtube-upload-kit.md`：標題、描述、hashtags、置頂留言與人工卡點。
- `checks/contact_sheet.png`：分鏡總覽檢查圖。
- `checks/final_frame_contact_sheet.png`：封面 + 影片抽幀檢查圖。
- `student-catches-ai-error-worksheet-upload-kit-20260509.tar.gz`：交接壓縮包。

## 驗證紀錄

- MP4：1080×1920、35.000 秒、25fps、H.264 + AAC。
- 旁白：zh-TW-HsiaoYuNeural，31.344 秒，已用 `apad` 對齊 35 秒影片。
- 圖像：封面與抽幀 contact sheet 視覺檢查通過，繁中可讀、無 tofu、無嚴重裁切／文字重疊／過度擁擠。
- 壓縮包：已用 `tar -tzf` 列出驗證；2026-05-09 22:27 已重打包加入 `worksheet-teacher-printable-v1.md`。
- 學習單：老師版可列印 Markdown 已讀回驗證，包含課堂目標、5 分鐘流程、學生表格、示範題、判讀規準與公開前檢查。

## 下一個可自動推進項目

優先題 9 已完成可上傳本機包與正式老師版學習單。下一個可自動推進：從內容題庫挑下一支「3 個問題，讓學生判斷 AI 答案能不能信」做 30 秒 storyboard。
