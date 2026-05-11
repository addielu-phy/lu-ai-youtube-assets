# YouTube Upload Kit｜量級荒謬：AI 算到接近光速？

建立時間：2026-05-09 巡視自動推進  
狀態：本機 Shorts 草稿、旁白、VTT、封面與交接包已完成；實際上傳仍需使用者登入 YouTube/Google。

## 1. 建議上傳檔

- 影片：`near-light-speed-by-ai-shorts-draft-v1.mp4`
- 封面：`cover_near_light_speed_by_ai_v1.png`
- 旁白：`narration_35s_edge_hsiaoyu.mp3`
- 字幕：`narration_35s_edge_hsiaoyu.vtt`
- 分鏡：`shotlist.json`

## 2. 標題候選

1. AI 算到接近光速？量級怪怪的先暫停 #Shorts
2. 國中題算出光速等級，AI 解答能信嗎？ #Shorts
3. 老師檢查 AI 解題：量級太離譜先別抄 #Shorts

## 3. 說明欄草稿

AI 解題步驟看起來很完整，不代表答案可信。  
如果日常物理題突然算到接近光速，先不要急著抄，也不用立刻從頭重算；先做量級檢查：像不像真實世界？單位對不對？條件有沒有被偷換？

這支是「老師抓包 AI 解題」系列：讓 AI 加速草稿，但由老師把關物理直覺、單位與條件。

#AI教學 #物理教學 #教師日常 #AI工具 #Shorts

## 4. 置頂留言

你看過 AI 把哪種物理題算到「量級離譜」？  
例如速度大到不合理、力大到像火箭、能量比日常情境高很多。  
留言丟一個案例，我會整理成下一支「老師抓包 AI」系列。

## 5. 上傳前人工確認

- [ ] 使用者已登入 YouTube/Google 並建立／選定頻道。
- [ ] 確認此片可用自製荒謬例，不涉及未公開考題或學生資料。
- [ ] 手機預覽封面文字 `量級怪怪的` 清楚可讀。

## 6. 本機驗證

- `ffprobe`：1080×1920、30fps、H.264 + AAC、約 33.0 秒音訊。
- 抽幀：`checks/frame_02s.png`、`checks/frame_15s.png`、`checks/frame_30s.png`。
- 視覺檢查：已用 contact sheet 檢查繁中可讀、無明顯 tofu／裁切；影片採乾淨畫面搭配 VTT sidecar，避免字幕壓到圖卡。
