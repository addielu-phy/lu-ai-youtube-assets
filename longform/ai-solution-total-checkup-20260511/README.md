# AI 解答總體檢長片 storyboard v1

建立：2026-05-11 巡視自動推進  
狀態：已完成 5 張 16:9 storyboard PNG、contact sheet、教師檢查表講義草稿與交接壓縮包；並已擴成 5 分 01 秒本機 slide-video 草稿、zh-TW 旁白、VTT/SRT 字幕、抽幀 QA、長片 YouTube upload kit、正式可分享講義、1080×1920 Shorts／社群宣傳卡與輕量上架交接包。

## 定位
- 暫定標題：用一題物理題示範：老師怎麼做 AI 解答總體檢
- 片長目標：5–7 分鐘長片
- 核心鉤子：不是重算一遍，而是照順序找破口。
- 觀眾：國高中自然／物理教師、想把 AI 解答轉成可檢查課堂材料的人。

## Storyboard
1. 不是重算一遍，而是照順序找破口
2. 關卡一：條件有沒有被偷換？
3. 關卡二：圖像與方向先過關
4. 關卡三：單位、量級、極端情況
5. 把總體檢變成學生工作單

## 檔案
- `slide_video_draft_v1/`：5 分 01 秒本機 slide-video 草稿、zh-TW 旁白、VTT/SRT 字幕、抽幀 QA、manifest、README、YouTube upload kit 與輕量上架交接包
- `slides/slide_01.png`–`slides/slide_05.png`：1920×1080 RGB storyboard
- `checks/contact_sheet.png`：3+2 contact sheet
- `ai-solution-total-checkup-teacher-checklist-draft-v1.md`：教師檢查表講義草稿
- `ai-solution-total-checkup-shareable-handout-v1.md`：正式可分享講義／Google Docs-ready handout
- `social-assets/ai-solution-total-checkup-social-card-v1.png`：1080×1920 Shorts／社群宣傳卡
- `render_total_checkup_social_card_v1.py`：可重現宣傳卡的 PIL 腳本
- `render_storyboard.py`：可重現圖卡的 PIL 腳本
- `manifest.json`：檔案清單與驗證狀態
- `ai-solution-total-checkup-storyboard-20260511.tar.gz`：交接壓縮包

## 驗證
- Storyboard PIL：5 張 slide 均為 1920×1080 RGB；contact sheet 為 1880×1180 RGB。
- Storyboard 視覺 QA：contact sheet 已檢查通過；實際出版用圖卡繁中可讀，無 tofu、嚴重裁切、文字重疊或過度擁擠。
- Slide-video ffprobe：`slide_video_draft_v1/ai-solution-total-checkup-slide-video-draft-v1.mp4` 為 1920×1080、30fps、H.264 yuv420p + AAC、300.984 秒。
- Slide-video QA：5 張抽幀皆為 1920×1080 RGB；contact sheet 1600×980 RGB；視覺檢查確認繁中可讀，無 tofu、嚴重裁切、文字重疊或過度擁擠；草稿交接壓縮包與輕量上架交接包皆已用 Python tarfile 讀回驗證。
- 講義：正式可分享講義已讀回驗證，包含五關檢查表、學生工作區、示範答案、10 分鐘課堂流程、可複製提示詞與公開分享提醒。
- 社群宣傳卡：`social-assets/ai-solution-total-checkup-social-card-v1.png` PIL 驗證 1080×1920 RGB；視覺 QA 通過，繁中可讀、無 tofu、裁切、文字重疊或過度擁擠；底部文字確認為「盧老師 × AI 物理教學」。

## 下一個可自動推進項目
若 YouTube 登入仍未完成，下一步推進第二季優先題 9「一堂課怎麼安排 AI 回答評分規準活動」：先做 rubric 草稿與 5 張 16:9 storyboard；若已完成登入，優先上傳第一季首批 Shorts。
