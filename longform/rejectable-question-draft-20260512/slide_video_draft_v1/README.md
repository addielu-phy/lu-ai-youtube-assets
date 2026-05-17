# 可退件題目草稿｜slide-video draft v1

狀態：已由 storyboard 擴成 4–6 分鐘長片本機草稿，並完成長片 upload kit、正式可分享講義、1080×1920 Shorts／社群宣傳卡與輕量交接包。

## 檔案
- 影片：`slide_video_draft_v1/rejectable-question-draft-slide-video-draft-v1.mp4`
- 旁白：`slide_video_draft_v1/narration_edge_hsiaoyu.mp3`
- 旁白全文：`slide_video_draft_v1/narration_zh_tw.txt`
- 字幕：`slide_video_draft_v1/narration_edge_hsiaoyu.vtt`、`slide_video_draft_v1/narration_edge_hsiaoyu.srt`
- 抽幀：`slide_video_draft_v1/check_frames/`
- QA contact sheet：`slide_video_draft_v1/checks/contact_sheet_slide_video_v1.png`
- manifest：`slide_video_draft_v1/manifest.json`
- Slide-video 草稿交接壓縮包：`slide_video_draft_v1/rejectable-question-draft-slide-video-draft-v1-20260512.tar.gz`
- 長片 upload kit：`slide_video_draft_v1/youtube-upload-kit-longform-v1.md`
- 正式可分享講義：`rejectable-question-draft-shareable-handout-v1.md`
- 長片上架輕量交接包：`slide_video_draft_v1/rejectable-question-draft-longform-upload-kit-v1-20260512.tar.gz`
- Shorts／社群宣傳卡：`social-assets/rejectable-question-draft-social-card-v1.png`
- 社群卡產生腳本／manifest：`render_rejectable_question_social_card_v1.py`、`social-assets/rejectable-question-draft-social-card-v1-manifest.json`

## 驗證
- ffprobe：258.672 秒，1920×1080，H.264 + AAC。
- PIL：5 張原始 storyboard、5 張抽幀與 QA contact sheet 尺寸／模式已寫入 manifest。
- 視覺 QA：contact sheet 已檢查，五張抽幀繁中可讀、無 tofu／明顯裁切／文字重疊／過度擁擠；縮圖小字略吃力但出版圖卡本身無 QA 問題。
- Upload kit／正式講義／輕量交接包已讀回驗證。
- 社群宣傳卡：PIL 驗證 1080×1920 RGB；視覺 QA 確認繁中可讀、無 tofu／裁切／重疊／過度擁擠。

## 下一個可自動推進項目
若 YouTube/Google 登入仍未完成，本長片社群宣傳卡與第三季內容題庫已完成；下一輪可製作第三季優先題 1「AI 給答案前，先叫它列出三個可驗證證據」的 5 張 Shorts storyboard 圖卡與交接包；若已完成登入，優先上傳第一季首批或本支第二季長片草稿。

## 音訊升級 v1（Lu Teacher F5-TTS）

- 推薦上傳影片：`rejectable-question-draft-slide-video-draft-lu-f5tts-v1.mp4`
- 改善原因：原版使用 zh-TW Edge HsiaoYu 女聲草稿；本版改用盧老師 F5-TTS voice clone。
- 升級版旁白：`narration_lu_f5tts_v1.mp3` / `narration_lu_f5tts_v1.wav`
- 升級版字幕：`narration_lu_f5tts_v1.vtt` / `narration_lu_f5tts_v1.srt`
- QA contact sheet：`checks/contact_sheet_lu_f5tts_v1.png`
- 驗證：ffprobe 215.115 秒，1920×1080，H.264 + AAC；旁白 loudnorm 後約 -16 LUFS；抽幀 QA 供視覺檢查。
