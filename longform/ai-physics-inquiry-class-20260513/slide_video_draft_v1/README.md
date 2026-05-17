# AI 物理探究課｜slide-video draft v1

狀態：已由 5 張 storyboard 擴成 4 分 56 秒長片本機草稿，並完成旁白、字幕、抽幀 QA、YouTube upload kit、正式可分享／Google Docs-ready 講義與交接壓縮包。

## 檔案
- 影片：`slide_video_draft_v1/ai-physics-inquiry-class-slide-video-draft-v1.mp4`
- 旁白：`slide_video_draft_v1/narration_edge_hsiaoyu.mp3`
- 旁白全文：`slide_video_draft_v1/narration_zh_tw.txt`
- 字幕：`slide_video_draft_v1/narration_edge_hsiaoyu.vtt`、`slide_video_draft_v1/narration_edge_hsiaoyu.srt`
- 抽幀：`slide_video_draft_v1/check_frames/`
- QA contact sheet：`slide_video_draft_v1/checks/contact_sheet_slide_video_v1.png`
- 長片 upload kit：`slide_video_draft_v1/youtube-upload-kit-longform-v1.md`
- 正式講義：`slide_video_draft_v1/ai-physics-inquiry-class-shareable-handout-v1.md`
- manifest：`slide_video_draft_v1/manifest.json`
- 交接壓縮包：`slide_video_draft_v1/ai-physics-inquiry-class-slide-video-draft-v1-20260513.tar.gz`

## 驗證
- ffprobe：295.632 秒，1920×1080，H.264 + AAC。
- PIL：5 張原始 storyboard、5 張抽幀與 QA contact sheet 尺寸／模式已寫入 manifest。
- 視覺 QA：contact sheet 已檢查，五張抽幀繁中可讀、無 tofu／明顯裁切／文字重疊／過度擁擠。
- 正式講義：已讀回驗證，包含 45 分鐘流程、學生工作區、同儕三問、AI prompt、退件句、評量規準與公開分享提醒。
- 壓縮包：Python tarfile 可讀回列出內容，且包含正式講義。

## 下一個可自動推進項目
第三季優先題 4「公開前三查」已完成 35 秒 Shorts MP4／公開檢查表；第三季優先題 5「圖能用嗎」storyboard 已完成。若 YouTube/Google 登入仍未完成，下一輪把優先題 5 擴成 35 秒 Shorts MP4／圖片授權檢查表；若已完成登入，優先上傳第一季首批或第三季代表作。

## 音訊升級 v1（Lu Teacher F5-TTS）

- 推薦上傳影片：`ai-physics-inquiry-class-slide-video-draft-lu-f5tts-v1.mp4`
- 改善原因：原版使用 zh-TW Edge HsiaoYu 女聲草稿；本版改用盧老師 F5-TTS voice clone。
- 升級版旁白：`narration_lu_f5tts_v1.mp3` / `narration_lu_f5tts_v1.wav`
- 升級版字幕：`narration_lu_f5tts_v1.vtt` / `narration_lu_f5tts_v1.srt`
- QA contact sheet：`checks/contact_sheet_lu_f5tts_v1.png`
- 驗證：ffprobe 241.633 秒，1920×1080，H.264 + AAC；旁白 loudnorm 後約 -16 LUFS；抽幀 QA 供視覺檢查。
