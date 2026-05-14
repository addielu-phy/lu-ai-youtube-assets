# Shorts storyboard｜讓 AI 幫忙寫家長訊息，第一版只准當草稿

狀態：2026-05-15 每小時雷達自動推進完成 storyboard package v1，並新增教師審稿 checklist。  
來源：第三季內容題庫優先題 12。

## 30 秒製作簡報

- 3 秒鉤子：語氣很客氣，不代表適合送出。
- 核心觀點：AI 可以幫老師起草家長訊息，但第一版只准當草稿；送出前要過「事實、語氣、隱私」三關。
- 對象：國高中自然／物理教師；可用於家長聯絡、作業提醒、課堂觀察回饋、補救教學溝通前審稿。
- 最小素材：家長訊息草稿、教師審稿 checklist、敏感資訊提醒。

## 圖卡

1. `slides/slide_01.png`｜語氣很客氣，不代表能送出
2. `slides/slide_02.png`｜第一關：這件事真的發生嗎？
3. `slides/slide_03.png`｜第二關：從指責改成合作
4. `slides/slide_04.png`｜第三關：敏感資訊先拿掉
5. `slides/slide_05.png`｜送出前，用三句話退件

## 延伸講義

- `parent-message-review-checklist-v1.md`｜AI 家長訊息三關教師審稿 checklist。

## 驗證

- PIL 輸出：5 張 `1080×1920` RGB PNG。
- Contact sheet：`checks/contact_sheet.png`。
- 視覺 QA：繁中主文字可讀、無 tofu 方塊、無裁切、無重疊；contact sheet 排版不擁擠。
- 壓縮包：`parent-message-draft-only-storyboard-kit-20260515.tar.gz` 可用 Python tarfile 讀回。

## 下一個自動推進

若 YouTube/Google 登入仍未完成：把本 storyboard 擴成 35 秒 Shorts MP4、封面、VTT/SRT、YouTube upload kit，並保留「家長訊息三關教師審稿 checklist」。  
若已登入：優先上傳第一季首批或第三季代表作。
