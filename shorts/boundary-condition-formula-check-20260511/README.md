# Shorts｜邊界條件沒寫，AI 的公式先打問號

建立時間：2026-05-11 每小時雷達自動推進  
來源：`publishing/content-backlog-season-02-v1.md` 第二季優先題 2  
狀態：已從 5 張 storyboard 擴成 37.5 秒本機 Shorts 草稿、zh-TW HsiaoYu 旁白、VTT/SRT 字幕、封面 PNG、YouTube upload kit、QA sheet 與交接壓縮包。

## 內容定位

- 主線：錯誤診斷進階
- 3 秒鉤子：公式看起來對，但條件沒交代。
- 封面字：條件在哪？
- 老師把關句：這個公式在什麼條件下才成立？

## 已產出檔案

- MP4：`boundary-condition-formula-check-shorts-35s.mp4`
- 封面：`cover_boundary_condition_formula_check_v1.png`
- 旁白：`narration_35s_edge_hsiaoyu.mp3`
- 字幕：`narration_35s_edge_hsiaoyu.vtt`、`narration_35s_edge_hsiaoyu.srt`
- Upload kit：`youtube-upload-kit.md`
- QA sheet：`checks/upload_qa_sheet.png`
- 壓縮包：`boundary-condition-formula-check-upload-kit-20260511.tar.gz`
- 可重現腳本：`render_storyboard.py`、`build_upload_package.py`

## 五張圖卡

1. Hook：漂亮公式先打問號
2. 公式不是只看對錯，要標使用條件
3. 斜面例：`a = g sinθ` 缺無摩擦／初速條件
4. 三句檢查：系統邊界、被忽略量、初始／邊界狀態
5. 課堂用法：公式旁補一張條件卡

## 已驗證

- ffprobe：1080×1920，25fps，H.264 + AAC，37.536 秒。
- PIL 尺寸驗證：封面與 5 張 slide 均為 1080×1920 RGB；QA sheet 為 780×1400 RGB。
- 視覺 QA：封面與 1s／18s／34s 抽幀繁中可讀、無 tofu、無嚴重裁切、無明顯重疊或過度擁擠；34s 已移除舊的「下一步可擴成 MP4」文字。
- 壓縮包：`boundary-condition-formula-check-upload-kit-20260511.tar.gz` 已用 Python tarfile 讀回驗證包含 README、manifest、upload kit、MP4、封面、旁白、字幕、slides、QA sheet 與腳本。

## 下一個可自動推進項目

若 YouTube/Google 登入仍未完成，改推進第二季下一個未完成題的 Shorts storyboard／MP4，避免重做本題；若使用者已完成登入，優先上傳第一季首批或本支第二季 Shorts。
