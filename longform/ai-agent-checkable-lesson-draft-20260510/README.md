# 長片 storyboard｜AI Agent 可檢查教案草稿

建立時間：2026-05-10 巡視自動推進  
最後更新：2026-05-10 13:53 巡視自動推進  
狀態：候選題 7 的 5 張 16:9 storyboard 卡、slide-video 草稿 v1、長片上傳文案包、「三色筆審稿檢查表」可分享講義與 1080×1920 Shorts／社群貼圖已完成；尚未上傳。

## 製作定位

- **題庫來源**：第一季候選題 7「我怎麼用 AI Agent 做一份可檢查教案草稿」。
- **目標片長**：5–8 分鐘長片或 4–6 分鐘 slide-video 草稿。
- **核心句**：AI 不是代課老師，而是先交一份能被老師審稿的草稿。
- **觀眾**：想用 AI Agent 備課、但擔心概念錯誤或不適班的國高中自然／物理教師。

## 5 張 storyboard 卡

1. `slides/01_01_hook.png` — AI 不是代課老師，而是交草稿的助教
2. `slides/02_02_inputs.png` — 先給 AI 三個邊界
3. `slides/03_03_agent_output.png` — 讓 Agent 交 4 份可檢查輸出
4. `slides/04_04_teacher_review.png` — 老師用三色筆審稿
5. `slides/05_05_video_plan.png` — 長片 5–8 分鐘骨架

## 下一步

- 已自動推進：`slide_video_draft_v1/` 已完成 5 分 23 秒本機 slide-video 草稿，含 zh-TW HsiaoYu 旁白、VTT/SRT、抽幀檢查與交接壓縮包 `ai-agent-checkable-lesson-slide-video-draft-v1-20260510.tar.gz`。
- 已自動推進：長片 YouTube upload kit `slide_video_draft_v1/youtube-upload-kit-longform-v1.md` 已完成，並已建立輕量上架交接包 `slide_video_draft_v1/ai-agent-checkable-lesson-longform-upload-kit-v1-20260510.tar.gz`。
- 已自動推進：可分享講義 `three-color-review-shareable-handout-v1.md` 已完成，可作為說明欄下載／貼文延伸素材。
- 已自動推進：三色筆檢查表 1080×1920 Shorts 封面／社群貼圖 `social-assets/three-color-review-social-card-v1.png` 已完成，產生腳本與 manifest 已保留並納入輕量交接包。
- 下一個可自動推進項目：若 YouTube 登入仍未完成，從第一季候選題 8「AI 找素材很快，但老師要檢查來源與難度」開始製作下一支 Shorts storyboard；若使用者已完成 YouTube/Google 登入，優先上傳首批 Shorts。
- 需使用者判斷：若要加入真實課堂教案、學生迷思、AI Agent 實際截圖或公開發布，需確認可公開性與 YouTube/Google 登入。

## 已驗證

- PIL：5 張 storyboard 卡皆為 1920×1080 RGB。
- Contact sheet：`checks/contact_sheet.png` 已輸出；視覺 QA 通過，五張卡片繁中可讀，未見 tofu 方塊、文字裁切、重疊或過度擁擠。
- Slide-video v1：`slide_video_draft_v1/ai-agent-checkable-lesson-slide-video-draft-v1.mp4` 已通過 ffprobe（1920×1080、30fps、H.264、yuv420p、AAC mono、322.600 秒、約 5.45 MB）。
- 抽幀 QA：`slide_video_draft_v1/checks/frame_contact_sheet.png` 視覺檢查通過，繁中可讀，未見 tofu／裁切／重疊／過度擁擠；交接壓縮包已通過 `tar -tzf` 列表驗證，且已納入可分享講義。
- 可分享講義：`three-color-review-shareable-handout-v1.md` 已讀回驗證，包含三色筆速查表、學生任務檢查格、教師示範、8 分鐘課堂流程與公開分享提醒。
- 社群貼圖：`social-assets/three-color-review-social-card-v1.png` 已由 PIL 驗證為 1080×1920 RGB；視覺 QA 通過，主標手機可讀，未見 tofu／裁切／文字重疊／過度擁擠；輕量交接壓縮包已重打包並通過 `tar -tzf` 列表驗證。
