# Shorts B 草稿包｜正負號不是裝飾

最後更新：2026-05-09 04:23 巡視自動推進

本資料夾把長片《AI 會算 ≠ 懂物理》的導流短片 B 製作成本機可預覽 9:16 Shorts 草稿。

## 內容
- `narration.txt`：約 35 秒旁白稿。
- `shotlist.json`：5 段式分鏡與視覺說明。
- `render_slides.py`：PIL 產生直式圖卡的腳本。
- `slides/slide_01.png`～`slide_05.png`：1080×1920 圖卡。
- `narration_edge_hsiaoyu.mp3`：zh-TW-HsiaoYuNeural 草稿旁白。
- `narration_edge_hsiaoyu.vtt`：旁白字幕。
- `slides_concat.ffconcat`：靜態圖卡串接時間軸。
- `sign-direction-not-decoration-shorts-draft-v1.mp4`：本機可預覽草稿。
- `checks/frame_3s.png`、`frame_14s.png`、`frame_27s.png`、`frame_33s.png`：抽幀檢查圖。
- `youtube-upload-kit.md`：標題、說明欄、hashtag、置頂留言與封面字建議。
- `cover_sign_direction_not_decoration_v1.png`：1080×1920 Shorts 封面 PNG。
- `sign-direction-not-decoration-shorts-draft-kit-20260509.tar.gz`：MP4、字幕、封面、上架文案與檢查圖的交接壓縮包。

## 驗證紀錄
- 影片規格：1080×1920、H.264、25fps、35.000 秒。
- 音訊：AAC；旁白 loudnorm 後 mean_volume 約 -17.6 dB、max_volume 約 -1.2 dB。
- 視覺抽幀：第三次檢查確認繁體中文可讀、無 tofu 方塊、無明顯裁切或重疊；底部提示在安全區內；物理語意可看出「題目正方向向右，但 AI 偷換成向左為正」。
- 封面：`cover_sign_direction_not_decoration_v1.png` 為 1080×1920 PNG；視覺檢查確認繁中無 tofu、無裁切或重疊，主標「數字對？方向錯了」手機可讀。
- 本輪修正：上移底部提示、加強安全區；把 `a` 改成 `加速度 a`，並避免箭頭穿過文字。

## 建議下一步
1. 已完成：Shorts B 封面 PNG 與最終交接壓縮包；若要繼續自動推進，可從長片素材包延伸下一支導流 Shorts 或整理首批上傳排程。
2. 若使用者完成 YouTube/Google 登入，可優先上傳 Shorts 01 的 34 秒版；本支 Shorts B 可作為長片導流短片排在後續。

## 需使用者操作
- YouTube/Google 登入與實際上傳。
