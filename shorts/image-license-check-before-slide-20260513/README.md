# Shorts Storyboard｜AI 找到的圖，可以直接放簡報嗎？

狀態：2026-05-13 每小時雷達已完成第三季優先題 5 的 5 張 1080×1920 storyboard 圖卡與交接包。  
來源：第三季內容題庫優先題 5「AI 找到的圖，可以直接放簡報嗎？」。

## 30 秒製作簡報

- 核心鉤子：圖很漂亮，不代表授權漂亮。
- 教師可複製句：請 AI 列出每張圖片的來源、授權、是否可公開使用；不確定的請提出可替代的自製圖。
- 影片結構：來源 → 授權 → 替代方案 → 可複製 prompt。
- 公開提醒：不要使用未授權圖片、真實學生作品或不明來源截圖作公開素材。

## 圖卡

1. `slides/slide_01.png`｜AI 找到的圖，可以直接放簡報嗎？
2. `slides/slide_02.png`｜先問：這張圖從哪裡來？
3. `slides/slide_03.png`｜再問：能不能公開分享？
4. `slides/slide_04.png`｜最後準備替代方案
5. `slides/slide_05.png`｜給 AI 的可複製句

## 驗證

- PIL：5 張圖卡皆為 1080×1920 RGB。
- QA contact sheet：`checks/contact_sheet.png` 為 1120×1480 RGB，供手機快速檢查繁中可讀、無 tofu、無裁切、無重疊與不過度擁擠。
- 壓縮包：`image-license-check-before-slide-storyboard-kit-20260513.tar.gz` 已用 Python `tarfile` 讀回確認包含 README、manifest、render script、slides 與 contact sheet。

## 下一個自動推進

若 YouTube/Google 登入仍未完成：把本 storyboard 擴成 35 秒 Shorts MP4／封面／字幕／YouTube upload kit，並延伸一頁「圖片授權檢查表」。  
若使用者已完成登入：優先上傳已完成的第一季首批 Shorts 或第三季代表作。
