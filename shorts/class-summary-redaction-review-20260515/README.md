# Shorts storyboard｜AI 生成的課堂摘要，老師要刪掉哪一種句子？

狀態：2026-05-15 每小時雷達自動推進完成 storyboard package v1，並新增教師檢查表。  
來源：第三季內容題庫優先題 11。

## 30 秒製作簡報

- 3 秒鉤子：摘要越順，越要檢查誰被講錯。
- 核心觀點：AI 生成課堂摘要前，老師要先刪掉可辨識、定型標籤、無證據評價的句子，改成可教學改進的匿名描述。
- 對象：國高中自然／物理教師；可用於課堂紀錄、Exit Ticket 整理、公開作品回饋、家長或同儕溝通前審稿。
- 最小素材：課堂摘要範例、刪改標註、隱私提醒與教師審稿 checklist。

## 圖卡

1. `slides/slide_01.png`｜摘要越順，越要先審
2. `slides/slide_02.png`｜順口的摘要，可能藏個資與標籤
3. `slides/slide_03.png`｜丟給 AI 前，先加一條紅線
4. `slides/slide_04.png`｜把學生標籤，改成學習線索
5. `slides/slide_05.png`｜三種句子，摘要完成前先刪

## 延伸講義

- `summary-redaction-teacher-checklist-v1.md`｜AI 課堂摘要三刪三留教師檢查表。

## 驗證

- PIL 輸出：5 張 `1080×1920` RGB PNG。
- Contact sheet：`checks/contact_sheet.png`。
- 視覺 QA：繁中主文字可讀、無 tofu 方塊、無裁切、無重疊；contact sheet 排版不擁擠。
- 壓縮包：`class-summary-redaction-review-storyboard-kit-20260515.tar.gz` 可用 Python tarfile 讀回。

## 下一個自動推進

若 YouTube/Google 登入仍未完成：把本 storyboard 擴成 35 秒 Shorts MP4、封面、VTT/SRT、YouTube upload kit，並保留「AI 課堂摘要三刪三留教師檢查表」。  
若已登入：優先上傳第一季首批或第三季代表作。
