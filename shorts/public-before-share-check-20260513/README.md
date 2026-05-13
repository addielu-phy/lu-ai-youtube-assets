# Shorts｜學生作品要放上網前，AI 幫忙檢查哪三件事？

狀態：2026-05-13 每小時雷達已把 storyboard 擴成 35 秒本機 Shorts 草稿、封面、字幕、YouTube upload kit，並新增「學生作品公開檢查表」。  
來源：第三季內容題庫優先題 4「公開前三查」。

## 成果檔案

- Shorts MP4：`public-before-share-check-shorts-35s.mp4`
- 封面：`cover_public_before_share_check_v1.png`
- 上傳包：`youtube-upload-kit.md`
- 教師／學生檢查表：`student-work-public-checklist-v1.md`
- 旁白：`narration_35s_edge_hsiaoyu.mp3`
- 字幕：`narration_35s_edge_hsiaoyu.vtt` / `narration_35s_edge_hsiaoyu.srt`
- QA sheet：`checks/qa_sheet_mp4.png`
- 壓縮包：`public-before-share-check-upload-kit-20260513.tar.gz`

## 圖卡

1. `slides/slide_01.png`｜公開前三查：匿名、授權、AI 標註
2. `slides/slide_02.png`｜匿名化：拿掉身分線索
3. `slides/slide_03.png`｜授權來源：AI 找到不等於可以公開
4. `slides/slide_04.png`｜AI 標註：說清楚協助範圍與責任
5. `slides/slide_05.png`｜公開閘門與 CTA

## 驗證

- MP4：1080×1920、25fps、H.264 + AAC、35 秒。
- PIL：封面、5 張圖卡與 QA 抽幀皆為 RGB 圖檔。
- 視覺 QA：`checks/qa_sheet_mp4.png` 已用於檢查繁中可讀、無 tofu 方塊、無裁切、無重疊與不過度擁擠。
- 檢查表：`student-work-public-checklist-v1.md` 已讀回驗證，含匿名化、授權來源、AI 標註、可複製 prompt、學生工作區與公開提醒。
- 壓縮包：已用 Python `tarfile` 讀回確認包含 MP4、封面、旁白、字幕、README、manifest、upload kit、檢查表、slides 與 QA sheet。

## 穩定發布

- 手機索引：`https://addielu-phy.github.io/lu-ai-youtube-assets/mobile-index/index.html`
- 本機 package：`shorts/public-before-share-check-20260513/`
- GitHub Pages：待同步後回填 commit 與 live 驗證。

## 下一個自動推進

若 YouTube/Google 登入仍未完成：從第三季題庫挑選下一個尚未完成的 storyboard／講義延伸。  
若使用者已完成 YouTube/Google 登入：優先上傳已完成的第一季首批 Shorts 或本支第三季 Shorts。
