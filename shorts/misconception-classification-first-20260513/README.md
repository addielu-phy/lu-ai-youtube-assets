# Shorts storyboard｜AI 幫忙整理學生迷思，老師先要求它分類而不是建議

狀態：2026-05-13 每小時雷達自動推進完成 storyboard package v1。  
來源：第三季內容題庫優先題 7「先分迷思」。

## 30 秒製作簡報

- 3 秒鉤子：先分類，再補救；不要一開始就開藥。
- 核心觀點：學生錯答可以先交給 AI 做「概念／程序／表徵」分類，但 AI 必須引用匿名錯答證據，不能直接跳到補救建議。
- 對象：國高中自然／物理教師，可用於段考後錯答整理、AI Agent 課後回饋包、補救教學分組前置作業。
- 最小素材：三類迷思卡、匿名學生錯答例、分類 prompt、老師二次確認句。
- 風險提醒：不使用真實學生姓名、座號、班級、原始手寫影像或未經確認可公開的作答內容；正式發布前需由使用者確認案例可公開性。

## 圖卡

1. `slides/slide_01.png`｜先分類，再補救
2. `slides/slide_02.png`｜概念迷思：規則想錯
3. `slides/slide_03.png`｜程序迷思：步驟亂掉
4. `slides/slide_04.png`｜表徵迷思：圖文公式不一致
5. `slides/slide_05.png`｜可複製 prompt 與 CTA

## 驗證

- PIL 輸出：5 張 `1080×1920` RGB PNG。
- Contact sheet：`checks/contact_sheet.png`。
- 視覺 QA：已檢查繁中主文字可讀、無 tofu 方塊、無裁切、無重疊；contact sheet 排版不擁擠。
- 壓縮包：`misconception-classification-first-storyboard-kit-20260513.tar.gz` 已用 Python `tarfile` 讀回確認包含 README、manifest、render script、5 張圖卡與 contact sheet。

## 下一個自動推進

若 YouTube/Google 登入仍未完成：把本 storyboard 擴成 35 秒 Shorts MP4／封面／字幕／YouTube upload kit，並延伸一頁「迷思分類 prompt」教師小抄。  
若使用者已完成 YouTube/Google 登入：優先上傳已完成的第一季首批或第三季代表作。
