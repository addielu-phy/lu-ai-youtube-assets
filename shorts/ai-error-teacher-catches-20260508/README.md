# AI 算錯？老師抓包！Shorts 草稿 v4

最後更新：2026-05-08 23:42 巡視自動推進

## 本輪新增輸出

- 直式 Shorts 成片草稿：`ai-error-teacher-catches-shorts-draft-v4-under60.mp4`
- 30 秒精簡版：`ai-error-teacher-catches-shorts-30s-v1.mp4`（34.30 秒，保留完整論點，較適合首支測試上線）
- 15 秒極短版：`ai-error-teacher-catches-shorts-15s-v1.mp4`（15.50 秒，適合 Reels/TikTok/Shorts 快速鉤子 A/B）
- 旁白文字：`narration.txt`、`narration_30s.txt`、`narration_15s.txt`
- Edge TTS 旁白：`narration_edge_hsiaoyu_slow.mp3`、`narration_30s_edge_hsiaoyu.mp3`、`narration_15s_edge_hsiaoyu.mp3`
- 分鏡資料：`shotlist.json`
- 直式分鏡圖：`slides/slide_01.png`～`slides/slide_05.png`
- 抽樣檢查圖：`checks/frame_28s_v4.png`、`checks_cutdowns/frame_30s_03s.png`、`checks_cutdowns/frame_30s_17s.png`、`checks_cutdowns/frame_30s_31s.png`、`checks_cutdowns/frame_15s_03s.png`、`checks_cutdowns/frame_15s_09s.png`、`checks_cutdowns/frame_15s_14s.png`

## 規格驗證

- 影片比例：三版皆為 1080×1920（9:16）。
- 影片長度：完整 v4 約 59.52 秒；30 秒精簡版 34.30 秒；15 秒極短版 15.50 秒。
- 影片編碼：H.264 + AAC。
- 旁白：zh-TW-HsiaoYuNeural；各版皆另附 `.vtt` 字幕檔。
- 抽幀視覺檢查：30 秒版與 15 秒版中文字可讀，無 tofu 方塊、無明顯裁切或重疊。

## 視覺迭代紀錄

初版中段畫面被檢查出：物理符號關係不夠明確、底部小字偏小、右側節點字太小。已修正為：

- 圓點標籤放大為 `AI → 錯 → 懂`
- 對「錯」加紅圈與教鞭/箭頭提示
- 增加 `假設方向`、`mg`、`正方向` 標籤
- 白框改成更短的兩行重點：`錯誤假設：／只代公式就會對？`
- 底部品牌文字上移，避免 Shorts 介面遮擋

## 建議下一步

1. 首支若想降低壓線風險，優先預覽／上傳 `ai-error-teacher-catches-shorts-30s-v1.mp4`；若想測試更強鉤子，可用 `ai-error-teacher-catches-shorts-15s-v1.mp4`。
2. YouTube 上傳仍需使用者登入/操作；本地素材與壓縮包已更新，可直接交接。
3. 下一個可自動推進項目：整理長片版腳本《AI 會算 ≠ 懂物理：老師如何檢查 AI 解題》。
