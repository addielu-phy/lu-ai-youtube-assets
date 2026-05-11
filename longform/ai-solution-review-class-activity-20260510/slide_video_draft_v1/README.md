# Slide-video draft v1｜一堂課怎麼安排 AI 解題審稿活動

狀態：已由 storyboard 擴成本機 16:9 slide-video 草稿，尚未上傳 YouTube。

## 主要輸出
- 影片：`ai-solution-review-class-activity-slide-video-draft-v1.mp4`
- 旁白全文：`narration_full_text.md`
- 字幕：`narration.srt`、`narration.vtt`
- 抽幀 QA：`checks/contact_sheet_frames.png`
- 建置腳本：`build_slide_video_draft.py`
- 可分享講義：`ai-solution-review-45min-class-activity-shareable-handout-v1.md`
- 社群宣傳卡：`../social-assets/ai-solution-review-class-activity-social-card-v1.png`

## 規格
- 解析度：1920×1080
- 長度：284.1 秒
- 語音：zh-TW-HsiaoChenNeural，rate -8%
- 內容：5 段 slide-video，對應原 storyboard 5 張卡。

## 已驗證
- `ffprobe` 可讀影片規格。
- 已抽出 5 張代表畫面並產生 contact sheet 供視覺 QA。
- 壓縮包可用 `tar -tzf` 檢查內容。
- 可分享講義已讀回驗證，並加入輕量上架交接包。
- 社群宣傳卡已通過 PIL 尺寸檢查與視覺 QA，並加入輕量上架交接包。

## 下一步
- 已完成自動推進：`youtube-upload-kit-longform-v1.md` 已完成，含標題、說明欄、章節時間碼、置頂留言、縮圖方向與人工作業清單。
- 已完成自動推進：`ai-solution-review-45min-class-activity-shareable-handout-v1.md` 已完成，提供 45 分鐘流程、學生工作區、老師示範問句、評量規準與公開分享提醒。
- 輕量上架交接包：`ai-solution-review-class-activity-longform-upload-kit-v1-20260510.tar.gz`，包含 upload kit、README、manifest、旁白全文、SRT/VTT、抽幀 contact sheet、建置腳本、可分享講義與社群宣傳卡；未重複打包大型 MP4。
- 已完成自動推進：1080×1920 Shorts／社群宣傳卡 `../social-assets/ai-solution-review-class-activity-social-card-v1.png` 已完成。
- 下一個可自動推進項目：若 YouTube 登入仍未完成，從第一季尚未製作的候選題挑選下一支 Shorts／長片 storyboard；若使用者已完成 YouTube/Google 登入，優先上傳首批 Shorts。
- 人工卡點：YouTube 頻道建立／上傳仍需已登入 Google / YouTube 的可操作環境。
