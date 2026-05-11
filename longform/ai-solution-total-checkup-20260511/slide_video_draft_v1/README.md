# AI 解答總體檢｜slide-video draft v1

狀態：已由 storyboard 擴成長片本機草稿；已補齊 YouTube upload kit、正式可分享講義、1080×1920 Shorts／社群宣傳卡與輕量上架交接包。

## 檔案
- 影片：`slide_video_draft_v1/ai-solution-total-checkup-slide-video-draft-v1.mp4`
- 旁白：`slide_video_draft_v1/narration_edge_hsiaoyu.mp3`
- 旁白全文：`slide_video_draft_v1/narration_zh_tw.txt`
- 字幕：`slide_video_draft_v1/narration_edge_hsiaoyu.vtt`、`slide_video_draft_v1/narration_edge_hsiaoyu.srt`
- 抽幀：`slide_video_draft_v1/check_frames/`
- QA contact sheet：`slide_video_draft_v1/checks/contact_sheet_slide_video_v1.png`
- manifest：`slide_video_draft_v1/manifest.json`
- 草稿交接壓縮包：`slide_video_draft_v1/ai-solution-total-checkup-slide-video-draft-v1-20260511.tar.gz`
- 長片上架文案：`slide_video_draft_v1/youtube-upload-kit-longform-v1.md`
- 正式可分享講義：`../ai-solution-total-checkup-shareable-handout-v1.md`
- Shorts／社群宣傳卡：`../social-assets/ai-solution-total-checkup-social-card-v1.png`
- 宣傳卡 manifest：`../social-assets/ai-solution-total-checkup-social-card-v1-manifest.json`
- 宣傳卡產生腳本：`../render_total_checkup_social_card_v1.py`
- 輕量上架交接包：`slide_video_draft_v1/ai-solution-total-checkup-longform-upload-kit-v1-20260511.tar.gz`

## 驗證
- ffprobe：300.984 秒，1920×1080，30fps，H.264 yuv420p + AAC。
- PIL：5 張抽幀皆為 1920×1080 RGB；contact sheet 為 1600×980 RGB；結果已寫入 manifest。
- 視覺 QA：contact sheet 通過；繁中可讀，無 tofu、嚴重裁切、文字重疊或過度擁擠。
- 草稿壓縮包：已用 Python tarfile 讀回驗證，包含 MP4、旁白、字幕、README、manifest、抽幀與 contact sheet。
- Shorts／社群宣傳卡：PIL 驗證 1080×1920 RGB；視覺 QA 通過，繁中可讀、無 tofu、裁切、文字重疊或過度擁擠；底部文字確認為「盧老師 × AI 物理教學」。
- 輕量上架交接包：已用 Python tarfile 讀回驗證，包含 upload kit、README、manifest、旁白文字、SRT/VTT、抽幀 contact sheet、教師檢查表草稿、正式可分享講義、社群宣傳卡、宣傳卡 manifest 與產生腳本；不重複打包大型 MP4。

## 下一個可自動推進項目
若 YouTube 登入仍未完成，下一步推進第二季優先題 9「一堂課怎麼安排 AI 回答評分規準活動」：先做 rubric 草稿與 5 張 16:9 storyboard；若已完成登入，優先上傳第一季首批 Shorts。
