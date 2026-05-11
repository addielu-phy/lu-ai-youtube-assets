# YouTube 長片上架交接包 v1｜AI Agent 可檢查教案草稿

建立時間：2026-05-10 10:37 巡視自動推進  
狀態：本機 slide-video 草稿已完成；此檔提供 YouTube Studio 可直接貼上的標題、說明欄、章節、置頂留言與縮圖方向。公開上傳仍需使用者登入 Google / YouTube 並確認可公開素材。

## 建議主標題

1. AI Agent 幫老師備課前，先讓它交「可檢查草稿」
2. 不要讓 AI 直接代課：老師用 Agent 備課的安全流程
3. AI Agent 備課工作流：三個輸入邊界、四份輸出、三色審稿

## YouTube 標題建議

- `AI Agent 幫老師備課前，先讓它交「可檢查草稿」｜教師 AI 工作流`
- `不要讓 AI 直接代課：老師用 AI Agent 備課的安全流程`
- `AI Agent 備課怎麼不亂教？三個邊界、四份輸出、三色審稿`

## 說明欄草稿

這支 5 分鐘草稿示範一個給老師用的 AI Agent 備課流程：不要把 AI 當成代課老師，而是把它當成先交草稿的助教。

核心流程：
1. 先給 AI 三個邊界：學生、概念、課堂限制。
2. 讓 Agent 一次交四份可檢查輸出：課程流程、學生任務、檢查表、風險清單。
3. 老師再用三色筆審稿：綠色保留、黃色改寫、紅色不能直接用。

這個流程的重點不是神奇 prompt，而是讓 AI 產出能被老師看懂、改得動、也敢在進教室前再次檢查的材料。

延伸素材：可複製／下載「三色筆審稿檢查表」，把 AI 教案草稿標成綠色可保留、黃色要改寫、紅色不能直接用，再決定哪些內容能進教室。

本片適合：
- 想用 AI Agent 備課的國高中自然／物理教師
- 擔心 AI 產生概念錯誤、忽略學生迷思或不適合班級情境的老師
- 想建立「AI 先出草稿、老師專業審稿」工作流的教學團隊

留言可以告訴我：你最想讓 AI 幫你先產出哪一種備課草稿？

#教師AI #AIAgent #備課 #教學設計 #生成式AI #自然科教學 #物理教學

## 章節時間碼

00:00 AI 不是代課老師，而是交草稿的助教  
00:47 先給 AI 三個邊界：學生、概念、限制  
01:43 讓 Agent 一次交四份可檢查輸出  
02:40 老師用三色筆審稿  
03:34 把流程整理成 5–8 分鐘長片骨架  
05:23 草稿結束／後續可補 prompt、AI 輸出截圖與審稿檢查表

## 置頂留言草稿

如果你想把這個流程帶回備課，先不要問「AI 能不能幫我做教案」。  
先問它三件事：
1. 你知道我的學生有哪些迷思嗎？
2. 你交出的活動，我要用什麼證據檢查學生真的懂？
3. 哪些地方你自己也不確定、需要老師重看？

這樣 AI 比較像助教，而不是看起來很會講、但沒被審稿的代課老師。

## 縮圖／封面方向

主字建議：`AI 備課，先別直接用`  
副字建議：`三色筆審稿流程`  
視覺方向：左側放「AI Agent 草稿」文件感，右側放老師三色筆標註（綠：可保留、黃：要改寫、紅：不能用）。避免放真實學生資料或未授權截圖。

## Shorts／社群貼圖延伸素材

- 已完成直式圖：`../social-assets/three-color-review-social-card-v1.png`（1080×1920 RGB）。
- 用途：可作為長片導流 Shorts 封面、YouTube 社群貼文、限動式公告，搭配說明欄的「三色筆審稿檢查表」講義。
- 視覺 QA：主標手機可讀，未見 tofu 方塊、裁切、文字重疊或過度擁擠。

## 上傳前人工作業

- [ ] 使用者登入 Google / YouTube Studio。
- [ ] 選擇是否用草稿版直接公開，或先補正式版畫面素材：實際 prompt、AI 輸出截圖、老師三色筆審稿畫面。
- [ ] 確認若出現真實教案、學生迷思或課堂資料，已去識別且可公開。
- [ ] 上傳影片：`ai-agent-checkable-lesson-slide-video-draft-v1.mp4`。
- [ ] 上傳字幕：`chapter_subtitles_coarse_v1.srt` 或 `narration_zhTW_hsiaoyu_v1.vtt`。
- [ ] 貼上標題、說明欄、章節與置頂留言。

## 本機素材

- 影片：`ai-agent-checkable-lesson-slide-video-draft-v1.mp4`
- 旁白文字：`narration_slide_video_v1.txt`
- 字幕：`chapter_subtitles_coarse_v1.srt`、`narration_zhTW_hsiaoyu_v1.vtt`
- 抽幀檢查：`checks/frame_contact_sheet.png`
- Manifest：`draft_v1_manifest.json`
- 延伸講義：`../three-color-review-shareable-handout-v1.md`
- Shorts／社群貼圖：`../social-assets/three-color-review-social-card-v1.png`
- 社群貼圖產生腳本：`../render_three_color_social_card_v1.py`
- 社群貼圖 manifest：`../social-assets/three-color-review-social-card-v1-manifest.json`

## 已驗證

- MP4 已由前一輪 ffprobe 驗證為 1920×1080、30fps、H.264、AAC mono、片長 322.600 秒。
- `../social-assets/three-color-review-social-card-v1.png` 已驗證為 1080×1920 RGB；視覺 QA 通過，主標手機可讀，未見 tofu／裁切／重疊／過度擁擠。
- 本交接包為文字／字幕／manifest／檢查圖／延伸貼圖的輕量包，不重複打包大型 MP4；上傳時請使用同資料夾內原 MP4。
