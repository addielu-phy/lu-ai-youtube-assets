# YouTube Upload Kit｜邊界條件沒寫，AI 的公式先打問號

狀態：本機 Shorts 草稿已完成；YouTube/Google 登入與實際上傳仍需使用者操作。

## 主檔
- MP4：`boundary-condition-formula-check-shorts-35s.mp4`
- 封面：`cover_boundary_condition_formula_check_v1.png`
- 旁白音檔：`narration_35s_edge_hsiaoyu.mp3`
- 字幕：`narration_35s_edge_hsiaoyu.vtt`、`narration_35s_edge_hsiaoyu.srt`
- QA：`checks/upload_qa_sheet.png`

## 驗證
- ffprobe：1080×1920，25fps，H.264 + AAC，37.536 秒。
- PIL：封面與 5 張 slides 均為 1080×1920 RGB；QA sheet 為 780×1400 RGB。
- 視覺 QA：封面與 1s／18s／34s 抽幀繁中可讀，無 tofu、嚴重裁切、明顯重疊或過度擁擠；34s 已移除舊的「下一步可擴成 MP4」文字。
- 壓縮包：`boundary-condition-formula-check-upload-kit-20260511.tar.gz` 已用 Python tarfile 讀回驗證包含主檔、封面、字幕、腳本、slides、README、manifest 與 upload kit。

## 建議標題
1. 邊界條件沒寫，AI 的公式先打問號
2. AI 公式看起來對？先問條件在哪
3. 老師檢查 AI 物理解答：公式成立前先補條件卡

## 說明文
AI 可能把公式寫對，卻少交代「在哪些條件下才成立」。這支 Shorts 示範老師如何用三句話檢查 AI 物理解答：系統邊界、被忽略的量、初始／邊界狀態。把公式旁邊補一張條件卡，學生就能從「會套公式」進到「知道何時不能套」。

## Hashtags
#AI教學 #物理教學 #教師備課 #AI素養 #高中物理 #Shorts

## 置頂留言
你會要求學生先檢查公式，還是先檢查題目條件？可以把你最常看到 AI 漏掉的「邊界條件」留言下來。

## 上傳時人工確認
- 需登入 YouTube/Google。
- 選擇頻道／可見度／是否排程。
- 若正式頻道名稱或品牌視覺已定稿，可替換封面 footer。 
