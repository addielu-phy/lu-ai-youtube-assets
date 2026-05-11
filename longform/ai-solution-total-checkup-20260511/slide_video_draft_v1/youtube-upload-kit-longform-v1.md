# YouTube 長片上架交接包 v1｜AI 解答總體檢

建立時間：2026-05-11 07:52 巡視自動推進  
狀態：本機 5 分 01 秒 slide-video 草稿已完成；此檔提供 YouTube Studio 可直接貼上的標題、說明欄、章節、置頂留言、縮圖方向與人工作業清單。公開上傳仍需使用者登入 Google / YouTube 並確認是否要補真實課堂素材。

## 建議主標題

1. 用一題物理題示範：老師怎麼做 AI 解答總體檢
2. AI 物理解答看起來很順？老師用五關檢查破口
3. 不用重算一遍：把 AI 解答變成學生可檢查的材料

## YouTube 標題建議

- `用一題物理題示範：老師怎麼做 AI 解答總體檢｜教師 AI 教學`
- `AI 物理解答看起來很順？老師用五關檢查破口`
- `不要只看答案：用五關讓學生檢查 AI 物理解題`

## 說明欄草稿

這支長片示範一個給自然／物理老師使用的 AI 解答總體檢流程：拿到 AI 產生的物理解答後，不急著重算一遍，而是把它拆成學生可以檢查的五個關卡。

五關流程：
1. 條件有沒有被偷換？
2. 圖像與方向有沒有來源？
3. 單位左右能不能相等？
4. 量級與極端情況合不合理？
5. 結論有沒有真的回答原題？

這個流程的重點不是抓 AI 出糗，而是把 AI 解答變成訓練學生審稿、提問與物理判斷的材料。老師可以讓每組學生負責一關，寫下「可疑處」、「引用證據」與「需要老師確認的問題」，再回到全班討論。

本片適合：
- 想把 AI 解答帶進課堂，但不想直接給學生抄答案的老師
- 想訓練學生檢查條件、圖像、單位、量級與結論的自然／物理教師
- 正在設計 AI 解題審稿活動、工作單或課堂討論流程的教學團隊

留言可以告訴我：你最想讓學生先練哪一關？條件、圖像、單位、量級，還是結論？

#教師AI #物理教學 #生成式AI #AI解題 #自然科教學 #學生審稿 #AI素養

## 章節時間碼

00:00 不是重算一遍，而是照順序找破口  
00:48 第一關：條件有沒有被偷換？  
01:48 第二關：圖像與方向先過關  
02:48 第三、四關：單位、量級與極端情況  
04:00 第五關：結論是否回答原題，並轉成學生工作單  
05:01 草稿結束／後續可補真實 AI 解題截圖與學生工作單

## 置頂留言草稿

拿到 AI 物理解答時，可以先不問「它算對了嗎？」  
改問五件事：
1. 它有沒有偷換條件？
2. 圖像和方向有沒有依據？
3. 單位左右能不能相等？
4. 量級和極端情況合不合理？
5. 最後一句有沒有回答原題？

如果要帶進課堂，可以讓每組學生只負責一關，先找證據，再請老師協助判斷。

## 縮圖／封面方向

主字建議：`AI 解答總體檢`  
副字建議：`五關找破口`  
視覺方向：左側放一份 AI 物理解答文件，右側放老師／學生的五關檢查清單：條件、圖像、單位、量級、結論。顏色沿用深藍背景、青綠重點與橘色警示，避免使用真實學生資料或未授權 AI 對話截圖。

## 上傳前人工作業

- [ ] 使用者登入 Google / YouTube Studio。
- [ ] 決定是否以本機草稿直接公開，或先補正式畫面素材：真實 AI 解題截圖、課堂工作單、學生分組檢查畫面。
- [ ] 若使用任何真實課堂資料，確認已去識別且可公開。
- [ ] 上傳影片：`ai-solution-total-checkup-slide-video-draft-v1.mp4`。
- [ ] 上傳字幕：`narration_edge_hsiaoyu.srt` 或 `narration_edge_hsiaoyu.vtt`。
- [ ] 貼上標題、說明欄、章節與置頂留言。

## 本機素材

- 影片：`ai-solution-total-checkup-slide-video-draft-v1.mp4`
- 旁白文字：`narration_zh_tw.txt`
- 字幕：`narration_edge_hsiaoyu.srt`、`narration_edge_hsiaoyu.vtt`
- 抽幀檢查：`checks/contact_sheet_slide_video_v1.png`
- Manifest：`manifest.json`
- 建置腳本：`build_slide_video_draft.py`
- 教師檢查表草稿：`../ai-solution-total-checkup-teacher-checklist-draft-v1.md`
- 正式可分享講義：`../ai-solution-total-checkup-shareable-handout-v1.md`
- Shorts／社群宣傳卡：`../social-assets/ai-solution-total-checkup-social-card-v1.png`
- 宣傳卡 manifest：`../social-assets/ai-solution-total-checkup-social-card-v1-manifest.json`
- 宣傳卡產生腳本：`../render_total_checkup_social_card_v1.py`
- 原始 storyboard contact sheet：`../checks/contact_sheet.png`

## 已驗證

- MP4 已用 ffprobe 驗證：1920×1080、30fps、H.264 yuv420p + AAC、300.984 秒。
- 抽幀 contact sheet 前一輪視覺 QA 通過：繁中可讀，無 tofu、嚴重裁切、文字重疊或過度擁擠。
- 本交接包為文字／字幕／manifest／檢查圖／講義草稿／正式可分享講義／社群宣傳卡的輕量包，不重複打包大型 MP4；上傳時請使用同資料夾內原 MP4。

## 下一個可自動推進項目

若 YouTube 登入仍未完成，下一步推進第二季優先題 9「一堂課怎麼安排 AI 回答評分規準活動」：先做 rubric 草稿與 5 張 16:9 storyboard；若已完成登入，優先上傳第一季首批 Shorts。
