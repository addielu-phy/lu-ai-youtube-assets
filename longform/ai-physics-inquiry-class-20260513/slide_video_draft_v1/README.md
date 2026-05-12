# AI 物理探究課｜slide-video draft v1

狀態：已由 5 張 storyboard 擴成 4–6 分鐘長片本機草稿，並完成旁白、字幕、抽幀 QA、YouTube upload kit 與交接壓縮包。

## 檔案
- 影片：`slide_video_draft_v1/ai-physics-inquiry-class-slide-video-draft-v1.mp4`
- 旁白：`slide_video_draft_v1/narration_edge_hsiaoyu.mp3`
- 旁白全文：`slide_video_draft_v1/narration_zh_tw.txt`
- 字幕：`slide_video_draft_v1/narration_edge_hsiaoyu.vtt`、`slide_video_draft_v1/narration_edge_hsiaoyu.srt`
- 抽幀：`slide_video_draft_v1/check_frames/`
- QA contact sheet：`slide_video_draft_v1/checks/contact_sheet_slide_video_v1.png`
- 長片 upload kit：`slide_video_draft_v1/youtube-upload-kit-longform-v1.md`
- manifest：`slide_video_draft_v1/manifest.json`
- 交接壓縮包：`slide_video_draft_v1/ai-physics-inquiry-class-slide-video-draft-v1-20260513.tar.gz`

## 驗證
- ffprobe：295.632 秒，1920×1080，H.264 + AAC。
- PIL：5 張原始 storyboard、5 張抽幀與 QA contact sheet 尺寸／模式已寫入 manifest。
- 視覺 QA：contact sheet 已檢查，五張抽幀繁中可讀、無 tofu／明顯裁切／文字重疊／過度擁擠。
- 壓縮包：Python tarfile 可讀回列出內容。

## 下一個可自動推進項目
製作正式可分享／Google Docs-ready AI 物理探究課流程講義，並更新輕量上架交接包；若 YouTube/Google 登入完成，優先上傳第一季首批或本支第三季長片草稿。
