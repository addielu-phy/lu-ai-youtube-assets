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
