# Shorts｜讓 AI 幫學生寫假設，但老師要加上哪一句？

狀態：2026-05-13 每小時雷達已把 storyboard 擴成 35 秒本機 Shorts 草稿、封面、字幕與 YouTube upload kit。  
來源：第三季內容題庫優先題 2。

## 成果檔案

- Shorts MP4：`hypothesis-causal-variable-shorts-35s.mp4`
- 封面：`cover_hypothesis_causal_variable_v1.png`
- 上傳包：`youtube-upload-kit.md`
- 旁白：`narration_35s_edge_hsiaoyu.mp3`
- 字幕：`narration_35s_edge_hsiaoyu.vtt` / `narration_35s_edge_hsiaoyu.srt`
- QA sheet：`checks/qa_sheet_mp4.png`
- 壓縮包：`hypothesis-causal-variable-upload-kit-20260513.tar.gz`

## 圖卡

1. `slides/slide_01.png`｜讓 AI 寫假設，先加一句話
2. `slides/slide_02.png`｜錯誤示範：太像答案、不可測
3. `slides/slide_03.png`｜老師加的一句：如果／那麼／因為
4. `slides/slide_04.png`｜修正版：斜面角度、底端速度、原因
5. `slides/slide_05.png`｜退件規則與 CTA

## 驗證

- MP4：1080×1920、25fps、H.264 + AAC、35 秒。
- PIL：封面、5 張圖卡與 QA 抽幀皆為 RGB 圖檔。
- 視覺 QA：`checks/qa_sheet_mp4.png` 已用於檢查繁中可讀、無 tofu 方塊、無裁切、無重疊與不過度擁擠。
- 壓縮包：已用 Python `tarfile` 讀回確認包含 MP4、封面、旁白、字幕、README、manifest、upload kit、slides 與 QA sheet。

## 穩定發布

- 手機索引：`https://addielu-phy.github.io/lu-ai-youtube-assets/mobile-index/index.html`
- 本機 package：`shorts/hypothesis-causal-variable-20260513/`
- GitHub Pages content commit：`02e7a09` 已推送，待 cleanup commit live 驗證後回填最終狀態。

## 下一個自動推進

若 YouTube/Google 登入仍未完成：從第三季題庫挑選下一個尚未完成的 Shorts storyboard／講義延伸。  
若使用者已完成 YouTube/Google 登入：優先上傳已完成的第一季首批 Shorts 或本支第三季 Shorts。
