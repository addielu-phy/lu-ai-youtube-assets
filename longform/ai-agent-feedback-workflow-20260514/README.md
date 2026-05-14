# 第三季優先題 9｜一個 AI Agent 怎麼幫老師做課後回饋包？

狀態：長片 slide-video 草稿 v1、YouTube upload kit、正式可分享講義與交接包已完成（2026-05-14 巡視自動推進）。

## 製作定位
- 格式：5–7 分鐘長片候選，已由 5 張 16:9 storyboard 擴成 slide-video 草稿。
- 核心觀眾：想用 AI 加速課後回饋，但不想把學生評價外包給 AI 的國高中自然／物理教師。
- 核心句：**回饋可以加速，但責任不能外包。**

## 已完成素材
- Storyboard：`slides/01_hook_feedback_workflow.png`～`slides/05_45min_reuse_flow.png`
- Storyboard QA：`checks/contact_sheet.png`
- Slide-video：`slide_video_draft_v1/ai-agent-feedback-workflow-slide-video-draft-v1.mp4`
- 旁白／字幕：`slide_video_draft_v1/narration_edge_hsiaoyu.mp3`、`.vtt`、`.srt`
- 長片 upload kit：`slide_video_draft_v1/youtube-upload-kit-longform-v1.md`
- 正式講義：`slide_video_draft_v1/feedback-package-review-shareable-handout-v1.md`
- QA contact sheet：`slide_video_draft_v1/checks/contact_sheet_slide_video_v1.png`
- 交接包：`slide_video_draft_v1/ai-agent-feedback-workflow-longform-upload-kit-v1-20260514.tar.gz`

## 5 張 storyboard
1. Hook：AI 不是代寫評語，而是進入審稿線。
2. 輸入邊界：先餵匿名資料，不餵學生身分。
3. AI 草稿包：全班共通回饋、分組補救任務、教師需確認風險句。
4. 教師審稿線：三色筆審稿，刪個資／改證據／補脈絡。
5. 45 分鐘課後回饋流程：匿名摘要、AI 草稿、教師定稿、下節課再用。

## 驗證
- ffprobe：253.464 秒，1920×1080，H.264 + AAC。
- PIL：5 張原始 storyboard、5 張抽幀與 QA contact sheet 尺寸／模式已寫入 manifest。
- 正式講義：已產生 `feedback-package-review-shareable-handout-v1.md`。
- 壓縮包：Python tarfile 可讀回列出內容。

## 下一個可自動推進項目
若 YouTube/Google 登入仍未完成，從第三季題庫挑選下一個尚未完成候選，或把本講義延伸成 Shorts／社群卡；若已完成登入，優先上傳第一季首批或第三季代表作。
