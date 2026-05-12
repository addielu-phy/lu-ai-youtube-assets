# 長片 storyboard｜一堂 45 分鐘 AI 物理探究課怎麼排？

建立：2026-05-13 巡視自動推進

## 狀態
已完成本機可驗證的長片前置包，並已擴成 4 分 56 秒 slide-video 草稿：5 張 1920×1080 storyboard、45 分鐘流程講義草稿、正式可分享／Google Docs-ready 講義、zh-TW 旁白、SRT/VTT 字幕、MP4、抽幀 QA、YouTube upload kit、manifest 與交接壓縮包。

## 內容定位
把「AI 可以進教室，但流程不能交給 AI」拆成一堂 45 分鐘物理探究課：情境、假設、資料、退件、Exit Ticket。

## 檔案
- slides/slide_01.png – slide_05.png
- checks/contact_sheet.png
- ai-physics-inquiry-45min-flow-handout-draft-v1.md
- manifest.json
- render_storyboard.py
- ai-physics-inquiry-class-storyboard-kit-20260513.tar.gz
- slide_video_draft_v1/ai-physics-inquiry-class-slide-video-draft-v1.mp4
- slide_video_draft_v1/youtube-upload-kit-longform-v1.md
- slide_video_draft_v1/ai-physics-inquiry-class-shareable-handout-v1.md
- slide_video_draft_v1/ai-physics-inquiry-class-slide-video-draft-v1-20260513.tar.gz

## 穩定連結
- 手機索引：https://addielu-phy.github.io/lu-ai-youtube-assets/mobile-index/index.html
- 本包 README：https://addielu-phy.github.io/lu-ai-youtube-assets/longform/ai-physics-inquiry-class-20260513/README.md
- storyboard contact sheet：https://addielu-phy.github.io/lu-ai-youtube-assets/longform/ai-physics-inquiry-class-20260513/checks/contact_sheet.png
- 正式講義：https://addielu-phy.github.io/lu-ai-youtube-assets/longform/ai-physics-inquiry-class-20260513/slide_video_draft_v1/ai-physics-inquiry-class-shareable-handout-v1.md
- GitHub Pages commit：storyboard `20c9768` 已 live 驗證；slide-video `a37ef97` 已 live 驗證；正式講義／upload kit cleanup `5583857` 已 live 驗證。

## 已驗證
- 5 張 storyboard：1920×1080 RGB。
- contact sheet：1880×1180 RGB。
- storyboard 壓縮包：Python tarfile 可讀回列出內容。
- slide-video：ffprobe 295.632 秒、1920×1080、H.264 yuv420p、30fps、AAC；抽幀 contact sheet 視覺 QA 通過；正式講義已讀回驗證；交接壓縮包 Python tarfile 可讀回且包含正式講義。

## 下一個可自動推進項目
若 YouTube/Google 登入仍未完成，改推第三季優先題 4「公開前三查」Shorts storyboard；若已完成登入，優先上傳第一季首批或本支第三季長片草稿。
