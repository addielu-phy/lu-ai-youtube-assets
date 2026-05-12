# 第二季優先題 6｜我怎麼讓 AI 先產出「可被退件」的題目草稿

建立時間：2026-05-12 每小時巡視自動推進  
狀態：長片 storyboard 前置包、4 分 19 秒本機 slide-video 草稿、長片 YouTube upload kit、正式可分享／Google Docs-ready 講義與 1080×1920 Shorts／社群宣傳卡皆已完成。

## 內容定位

- 格式：長片 5–8 分鐘，16:9 slide-video 可延伸。
- 主線：AI Agent 工作流。
- 3 秒鉤子：好題目不是一次生成，是先讓它交可退件版本。
- 縮圖字：可退件草稿。
- 承接：Shorts 02「AI Agent 幫老師備課，但不亂教」與「AI 幫老師出題，第一步不是按生成」。

## 已完成素材

- Storyboard 圖卡：`slides/slide_01.png`–`slides/slide_05.png`（1920×1080）。
- QA contact sheet：`checks/contact_sheet.png`。
- 可重現腳本：`render_storyboard.py`。
- Manifest：`manifest.json`。
- 退件規準講義草稿：`rejectable-question-draft-rubric-handout-draft-v1.md`。
- 正式可分享講義：`rejectable-question-draft-shareable-handout-v1.md`。
- 長片 YouTube upload kit：`slide_video_draft_v1/youtube-upload-kit-longform-v1.md`。
- 長片上架輕量交接包：`slide_video_draft_v1/rejectable-question-draft-longform-upload-kit-v1-20260512.tar.gz`。
- Shorts／社群宣傳卡：`social-assets/rejectable-question-draft-social-card-v1.png`。
- 社群卡產生腳本／manifest：`render_rejectable_question_social_card_v1.py`、`social-assets/rejectable-question-draft-social-card-v1-manifest.json`。
- Slide-video 草稿：`slide_video_draft_v1/rejectable-question-draft-slide-video-draft-v1.mp4`。
- 旁白／字幕／抽幀 QA：`slide_video_draft_v1/narration_edge_hsiaoyu.mp3`、`slide_video_draft_v1/narration_edge_hsiaoyu.vtt`、`slide_video_draft_v1/checks/contact_sheet_slide_video_v1.png`。
- Slide-video 交接壓縮包：`slide_video_draft_v1/rejectable-question-draft-slide-video-draft-v1-20260512.tar.gz`。

## 5 張 storyboard 大綱

1. 好題目不是一次生成，是先讓它能被退件。
2. Prompt 裡放三個硬限制：年級單元、只測一件事、輸出格式。
3. 退件規準先寫在前面：目標不清、條件不足、誘因不對。
4. 修訂不是重寫，是對照退件理由留下證據。
5. 把流程變成教師可複製模板。

## 驗證紀錄

- PIL 驗證：5 張圖卡皆為 1920×1080 RGB；contact sheet 為 1880×1180 RGB。
- 視覺 QA：繁體中文主文字可讀、無 tofu 方塊、無明顯裁切、無文字重疊或過度擁擠。
- 壓縮包：`rejectable-question-draft-storyboard-kit-20260512.tar.gz` 已用 Python tarfile 讀回確認包含 README、manifest、render script、5 張 slides、contact sheet 與講義草稿。
- GitHub Pages：storyboard 版已同步到穩定手機索引 `https://addielu-phy.github.io/lu-ai-youtube-assets/mobile-index/index.html`（內容 commit `9f49f43`；README／壓縮包 cleanup commit `b7f0971`），本輪 slide-video 草稿已同步到穩定手機索引（內容 commit `8f50930`；cleanup commit `ad2a385`）；長片 upload kit／正式講義已同步到穩定 GitHub Pages（commit `7ebf311`）。
- Slide-video 驗證：ffprobe 1920×1080、30fps、H.264 yuv420p + AAC、258.672 秒；PIL 驗證抽幀與 contact sheet；視覺 QA 確認繁中可讀、無 tofu／裁切／文字重疊／過度擁擠；壓縮包已用 Python tarfile 讀回確認 23 個項目。
- Upload kit／正式講義驗證：`youtube-upload-kit-longform-v1.md` 與 `rejectable-question-draft-shareable-handout-v1.md` 已讀回；輕量交接包已用 Python tarfile 讀回確認包含 upload kit、README、manifest、字幕、旁白文字、QA contact sheet 與正式講義。
- 社群宣傳卡驗證：PIL 驗證 1080×1920 RGB；視覺 QA 確認繁中可讀、無 tofu／裁切／重疊／過度擁擠；輕量交接包已重打包並讀回確認包含 PNG、manifest 與 render script。

## 下一個自動推進

若 YouTube/Google 登入仍未完成：本長片 1080×1920 Shorts／社群宣傳卡已完成；下一輪可開始整理第三季候選題庫，或從既有長片/Shorts 製作跨平台貼文文案包。若使用者已完成登入：優先上傳第一季首批 Shorts／長片或最新穩定 GitHub Pages 索引中的候選影片。
