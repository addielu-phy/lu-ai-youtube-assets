# Shorts storyboard｜學生作品要放上網前，AI 幫忙檢查哪三件事？

狀態：2026-05-13 每小時雷達自動推進完成 storyboard package v1。  
來源：第三季內容題庫優先題 4「公開前三查」。

## 30 秒製作簡報

- 3 秒鉤子：能不能公開，不是看作品漂不漂亮。
- 核心觀點：學生作品公開前，老師可以讓 AI 協助跑「匿名化、授權來源、AI 標註」三道檢查，但最後公開責任仍由教師把關。
- 對象：國高中自然／物理教師，可用於學生作品展示、課堂成果上網、社群貼文或教學網站發布前。
- 最小素材：匿名化清單、授權／來源提醒、AI 使用標註句、公開前教師確認語。
- 風險提醒：不使用真實學生個資、照片、未公開作品或未確認授權素材；正式發布前需由使用者確認案例可公開。

## 圖卡

1. `slides/slide_01.png`｜公開前三查：匿名、授權、AI 標註
2. `slides/slide_02.png`｜匿名化：拿掉身分線索
3. `slides/slide_03.png`｜授權來源：AI 找到不等於可以公開
4. `slides/slide_04.png`｜AI 標註：說清楚協助範圍與責任
5. `slides/slide_05.png`｜公開閘門與 CTA

## 驗證

- PIL 輸出：5 張 `1080×1920` RGB PNG。
- Contact sheet：`checks/contact_sheet.png`。
- 視覺 QA：已檢查繁中主文字可讀、無 tofu 方塊、無裁切、無重疊；contact sheet 排版不擁擠。
- 壓縮包：`public-before-share-check-storyboard-kit-20260513.tar.gz` 已用 Python `tarfile` 讀回確認包含 README、manifest、render script、5 張圖卡與 contact sheet。

## 下一個自動推進

若 YouTube/Google 登入仍未完成：把本 storyboard 擴成 35 秒 Shorts MP4／封面／字幕／YouTube upload kit，並延伸一頁「學生作品公開檢查表」。  
若使用者已完成 YouTube/Google 登入：優先上傳已完成的第一季首批或第三季代表作。
