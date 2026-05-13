# Shorts｜AI 幫忙整理學生迷思，老師先要求它分類而不是建議

狀態：2026-05-13 每小時雷達已把 storyboard 擴成 35 秒本機 Shorts 草稿、封面、字幕、YouTube upload kit，並新增「迷思分類 Prompt 教師小抄」。  
來源：第三季內容題庫優先題 7「先分迷思」。

## 成果檔案

- Shorts MP4：`misconception-classification-first-shorts-35s.mp4`
- 封面：`cover_misconception_classification_first_v1.png`
- 上傳包：`youtube-upload-kit.md`
- 教師小抄：`misconception-classification-prompt-sheet-v1.md`
- 旁白：`narration_35s_edge_hsiaoyu.mp3`
- 字幕：`narration_35s_edge_hsiaoyu.vtt` / `narration_35s_edge_hsiaoyu.srt`
- QA sheet：`checks/qa_sheet_mp4.png`
- 壓縮包：`misconception-classification-first-upload-kit-20260513.tar.gz`

## 圖卡

1. `slides/slide_01.png`｜先分類，再補救
2. `slides/slide_02.png`｜概念迷思：規則想錯
3. `slides/slide_03.png`｜程序迷思：步驟亂掉
4. `slides/slide_04.png`｜表徵迷思：圖文公式不一致
5. `slides/slide_05.png`｜可複製 prompt 與 CTA

## 驗證

- MP4：1080×1920、25fps、H.264 + AAC、35 秒。
- PIL：封面、5 張圖卡與 QA 抽幀皆為 RGB 圖檔。
- 視覺 QA：`checks/qa_sheet_mp4.png` 用於檢查繁中可讀、無 tofu 方塊、無裁切、無重疊與不過度擁擠。
- 教師小抄：`misconception-classification-prompt-sheet-v1.md` 已讀回驗證，含三類迷思速表、可複製 prompt、學生錯答整理表與公開隱私提醒。
- 壓縮包：已用 Python `tarfile` 讀回確認包含 MP4、封面、旁白、字幕、README、manifest、upload kit、教師小抄、slides 與 QA sheet。

## 穩定發布

- 手機索引：`https://addielu-phy.github.io/lu-ai-youtube-assets/mobile-index/index.html`
- 本機 package：`shorts/misconception-classification-first-20260513/`
- GitHub Pages：`https://addielu-phy.github.io/lu-ai-youtube-assets/shorts/misconception-classification-first-20260513/README.md`（commit `526d6f1` 已 live 驗證）。

## 下一個自動推進

若 YouTube/Google 登入仍未完成：從第三季題庫挑選下一個尚未完成 storyboard／講義延伸。  
若使用者已完成 YouTube/Google 登入：優先上傳已完成的第一季首批 Shorts 或本支第三季 Shorts。


## 音訊升級 v2（Lu Teacher F5-TTS）

- 改善原因：原版使用 Edge HsiaoYu 旁白，音訊長度約 44.33 秒但影片只有 35 秒，會被截斷；本版改用盧老師 F5-TTS voice clone、重新濃縮旁白並 loudness normalization。
- 升級版 MP4：`misconception-classification-first-shorts-35s-lu-f5tts-v2.mp4`
- 升級版旁白：`narration_35s_lu_f5tts_v2.mp3` / `narration_35s_lu_f5tts_v2.wav`
- 升級版字幕：`narration_35s_lu_f5tts_v2.vtt` / `narration_35s_lu_f5tts_v2.srt`
- 音訊處理：F5-TTS chunked generation、短停頓串接、loudnorm I=-16、AAC 192k、35 秒完整輸出。


## 音訊升級 v3（推薦版）

- 推薦版 MP4：`misconception-classification-first-shorts-35s-lu-f5tts-v3.mp4`
- 旁白：`narration_35s_lu_f5tts_v3.mp3` / `narration_35s_lu_f5tts_v3.wav`
- 字幕：`narration_35s_lu_f5tts_v3.vtt` / `narration_35s_lu_f5tts_v3.srt`
- 原始 F5 串接長度：27.32 秒；最終輸出：35.00 秒；時間壓縮倍率：1.000。
- 說明：改用盧老師 F5-TTS voice clone、縮短腳本、分段生成、loudness normalization，避免原 Edge 旁白 44.33 秒被 35 秒影片截斷。


## 音訊升級 v4（推薦發布版）

- 推薦發布版 MP4：`misconception-classification-first-shorts-35s-lu-f5tts-v4.mp4`
- 旁白：`narration_35s_lu_f5tts_v4.mp3` / `narration_35s_lu_f5tts_v4.wav`
- 字幕：`narration_35s_lu_f5tts_v4.vtt` / `narration_35s_lu_f5tts_v4.srt`
- 原始 F5 串接長度：40.33 秒；最終輸出：35.00 秒；時間壓縮倍率：1.159。
- 說明：改用盧老師 F5-TTS voice clone、分段生成、loudness normalization，避免原 Edge 旁白 44.33 秒被 35 秒影片截斷。


## 品質檢查與升級 v5（推薦評估版）

- 推薦評估版 MP4：`misconception-classification-first-shorts-35s-quality-v5.mp4`
- 推薦旁白：`narration_35s_lu_f5tts_v5_quality.mp3` / `narration_35s_lu_f5tts_v5_quality.wav`
- 字幕：`narration_35s_lu_f5tts_v5_quality.vtt` / `narration_35s_lu_f5tts_v5_quality.srt`
- QA contact sheet：`checks/quality_v5_contact_sheet.png`
- 品質報告：`quality-review-and-upgrade-v5.json`
- 改善重點：放大手機可讀主文字、減少小字、底部安全區上移、加入簡單動畫節奏、重新生成較自然長度的盧老師 F5-TTS 旁白，避免 v4 的 1.159 倍時間壓縮。


## 品質檢查與升級 v6（目前推薦版）

- 推薦版 MP4：`misconception-classification-first-shorts-35s-quality-v6.mp4`
- 音訊沿用 v5 盧老師 F5-TTS：`narration_35s_lu_f5tts_v5_quality.mp3` / `.wav`
- QA contact sheet：`checks/quality_v6_contact_sheet.png`
- 品質報告：`quality-review-and-upgrade-v6.json`
- v6 修正 v5 QA 指出的問題：移除底部小字、進度條移到上方安全區、頂部標籤簡化、說明文字再放大、1s/34s 擁擠區微調。
