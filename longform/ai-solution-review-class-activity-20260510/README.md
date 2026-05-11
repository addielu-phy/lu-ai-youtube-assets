# 長片 storyboard｜一堂課怎麼安排「AI 解題審稿」活動

建立時間：2026-05-10 巡視自動推進  
狀態：候選題 10 的 5 張 16:9 storyboard／課堂流程包、4 分 44 秒 16:9 slide-video 草稿、長片上架文案包、「AI 解題審稿 45 分鐘課堂活動單」可分享講義與 1080×1920 Shorts／社群宣傳卡已完成；尚未上傳 YouTube。

## 製作定位

- **題庫來源**：第一季候選題 10「一堂課怎麼安排『AI 解題審稿』活動」。
- **目標片長**：5–7 分鐘長片或 slide-video。
- **核心句**：把 AI 錯誤變成學生討論，而不是老師恐慌。
- **觀眾**：想把 AI 放進課堂，但需要可控流程、分組任務與評量規準的國高中自然／物理教師。

## 5 張 storyboard 卡

1. `slides/01_01_01_hook.png` — 一堂課怎麼安排「AI 解題審稿」活動？
2. `slides/02_02_02_flow.png` — 45 分鐘四段式流程
3. `slides/03_03_03_group_roles.png` — 每組只負責一種審稿視角
4. `slides/04_04_04_rubric.png` — 評量看證據，不看有沒有用 AI
5. `slides/05_05_05_video_plan.png` — 5–7 分鐘長片骨架與 CTA

## 課堂流程草案

- 0–5 分：全班看一段 AI 解題，先標出「看起來太順」的位置。
- 5–15 分：小組依條件、單位、圖像、量級分工圈疑點。
- 15–30 分：每組提出一個證據，不要求立刻完整重算。
- 30–40 分：全班把證據整理成「AI 解題審稿規準」。
- 40–45 分：學生改寫一句更可靠的解題說明，作為 exit ticket。

## 下一步

- 已完成自動推進：`slide_video_draft_v1/` 已產出 4 分 44 秒 zh-TW 旁白 slide-video 草稿、VTT/SRT、抽幀 contact sheet、manifest、建置腳本與交接壓縮包 `ai-solution-review-class-activity-slide-video-draft-v1-20260510.tar.gz`。
- 已完成自動推進：長片 YouTube upload kit `slide_video_draft_v1/youtube-upload-kit-longform-v1.md` 與輕量上架交接包 `slide_video_draft_v1/ai-solution-review-class-activity-longform-upload-kit-v1-20260510.tar.gz` 已建立，包含標題、說明欄、章節時間、置頂留言、縮圖方向、字幕、manifest、抽幀檢查圖與建置腳本；未重複打包大型 MP4。
- 已完成自動推進：`slide_video_draft_v1/ai-solution-review-45min-class-activity-shareable-handout-v1.md` 已完成，讓影片說明欄可附 45 分鐘課堂活動單／可分享講義。
- 已完成自動推進：1080×1920 Shorts／社群宣傳卡 `social-assets/ai-solution-review-class-activity-social-card-v1.png` 已完成，產生腳本 `render_class_activity_social_card_v1.py` 與 manifest `social-assets/ai-solution-review-class-activity-social-card-v1-manifest.json` 已保留並納入輕量交接包。
- 下一個可自動推進項目：若 YouTube 登入仍未完成，從第一季尚未製作的候選題挑選下一支 Shorts／長片 storyboard；若使用者已完成 YouTube/Google 登入，優先上傳首批 Shorts。
- 需使用者判斷：若要使用真實學生作品、未公開題目、或課堂照片，需先確認可公開性；YouTube 頻道建立／上傳仍需已登入 Google / YouTube 的可操作環境。

## 已驗證

- PIL：5 張 storyboard 卡皆為 1920×1080 RGB。
- Contact sheet：`checks/contact_sheet.png` 已輸出，供視覺 QA 檢查繁中可讀性、無 tofu、無裁切、無重疊與不過度擁擠。
- Slide-video：`slide_video_draft_v1/ai-solution-review-class-activity-slide-video-draft-v1.mp4` 已用 `ffprobe` 驗證 1920×1080、30fps、H.264、yuv420p，長度 284.106667 秒。
- 抽幀 QA：`slide_video_draft_v1/checks/contact_sheet_frames.png` 視覺檢查通過，五個實際畫面繁中可讀，無 tofu／裁切／重疊／過度擁擠。
- 交接包：`ai-solution-review-class-activity-slide-video-draft-v1-20260510.tar.gz` 已用 `tar -tzf` 驗證包含影片、旁白、VTT/SRT、抽幀、manifest、README 與建置腳本。
- 可分享講義：`slide_video_draft_v1/ai-solution-review-45min-class-activity-shareable-handout-v1.md` 已讀回驗證，並加入長片輕量上架交接包。
- 社群宣傳卡：`social-assets/ai-solution-review-class-activity-social-card-v1.png` 已由 PIL 驗證為 1080×1920 RGB；視覺 QA 通過，主標手機可讀，未見 tofu／裁切／文字重疊／過度擁擠；輕量交接壓縮包已重打包並通過 `tar -tzf` 列表驗證。
