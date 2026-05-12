# 第二季優先題 6｜我怎麼讓 AI 先產出「可被退件」的題目草稿

建立時間：2026-05-12 每小時巡視自動推進  
狀態：長片 5–8 分鐘 storyboard 前置包已完成；尚未製作旁白／MP4。

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

## 下一個自動推進

若 YouTube/Google 登入仍未完成：把本 storyboard 擴成 4–6 分鐘旁白、SRT/VTT 與 slide-video 草稿。  
若使用者已完成登入：優先上傳第一季首批 Shorts／長片或最新穩定 GitHub Pages 索引中的候選影片。
