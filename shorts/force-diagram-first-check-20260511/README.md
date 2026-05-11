# Shorts 第二季優先題 1｜AI 畫的力圖，第一眼先看哪裡？

建立時間：2026-05-11 03:18 巡視自動推進  
最後更新：2026-05-11 04:20 巡視自動推進  
狀態：5 張 1080×1920 storyboard 已擴成本機 35 秒 Shorts 草稿、zh-TW 旁白、VTT 字幕、封面 PNG、YouTube upload kit 與交接壓縮包。

## 製作定位

- 格式：YouTube Shorts / 直式 9:16 / 35 秒
- 主線：錯誤診斷進階
- 承接：第一季「畫圖驗證」「5 句追問」
- 核心訊息：AI 的文字解釋看似合理時，老師仍要先看力圖是否漏力、多力、方向錯或受力物混淆。

## 主要檔案

- 影片：`force-diagram-first-check-shorts-35s.mp4`
- 封面：`cover_force_diagram_first_check_v1.png`
- 旁白文字：`narration_35s.txt`
- 旁白音檔：`narration_35s_edge_hsiaoyu.mp3`
- 字幕：`narration_35s_edge_hsiaoyu.vtt`
- 上傳文案：`youtube-upload-kit.md`
- manifest：`manifest.json`
- storyboard slides：`slides/slide_01_hook.png` ～ `slides/slide_05_cta.png`
- QA：`checks/contact_sheet.png`、`checks/upload_qa_sheet.png`、`checks/frame_01s.png`、`checks/frame_15s.png`、`checks/frame_31s.png`
- deterministic scripts：`render_storyboard.py`、`render_cover.py`、`make_upload_qa_sheet.py`
- 交接壓縮包：`force-diagram-first-check-upload-kit-20260511.tar.gz`

## 已驗證

- 原 storyboard：5 張圖卡皆為 1080×1920 RGB；contact sheet 為 1200×1500 RGB。
- MP4：`ffprobe` 驗證 1080×1920、25fps、H.264 + AAC、33.936 秒。
- 封面：PIL 驗證 1080×1920 RGB。
- 視覺 QA：封面與 01s／15s／31s 抽幀繁中可讀、無 tofu 方塊、無嚴重裁切／重疊／過度擁擠；封面底部已修正為不擁擠。
- 壓縮包：`force-diagram-first-check-upload-kit-20260511.tar.gz` 已建立並讀回驗證，包含影片、封面、旁白、VTT、upload kit、manifest、slides、QA 圖與 render scripts。

## 旁白稿

AI 畫出力圖時，不要先看公式漂不漂亮。第一眼先問：有哪些力？重力、正向力、摩擦力，有沒有漏掉，或多畫不存在的力。第二眼看方向：重力向下，正向力垂直接觸面，摩擦力要反抗相對滑動趨勢。第三眼圈出受力物：這個箭頭是誰施力，作用在誰身上？把這三句交給學生，AI 的圖就不只是答案，而是可以被檢查的材料。

## 下一個可自動推進項目

第二季優先題 3「AI 解答總體檢長片」的 5 張 16:9 storyboard + 檢查表講義草稿已完成於 longform/ai-solution-total-checkup-20260511/；下一步若 YouTube 登入仍未完成，將該長片 storyboard 擴成 4–6 分鐘 zh-TW 旁白、VTT/SRT 與 slide-video draft。
