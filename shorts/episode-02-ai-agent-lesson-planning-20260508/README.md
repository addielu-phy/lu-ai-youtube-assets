# Shorts 02 草稿包｜AI Agent 幫老師備課，但不亂教

本資料夾為 2026-05-08 每小時雷達自動推進產物。

## 內容
- `narration.txt`：60 秒內旁白草稿
- `slides/slide_01.png`～`slide_05.png`：9:16 分鏡圖（1080×1920）
- `make_episode02_slides.py`：可重生分鏡圖的腳本
- `narration_edge_hsiaoyu.mp3`：zh-TW Edge TTS 試聽旁白（58.392 秒）
- `episode-02-ai-agent-lesson-planning-draft-v1.mp4`：9:16 本機可預覽草稿（1080×1920 / 30fps / H.264 + AAC）
- `episode-02-ai-agent-lesson-planning-30s-v1.mp4`：30 秒剪短版草稿（1080×1920 / 30fps / H.264 + AAC，無燒錄字幕、另附 VTT）
- `narration_30s.txt`、`narration_30s_edge_hsiaoyu.mp3`、`narration_30s_edge_hsiaoyu.vtt`：30 秒版旁白與字幕檔
- `youtube-upload-kit.md`：標題、說明欄、hashtag、置頂留言與封面字建議
- `episode-02-ai-agent-lesson-planning-upload-kit-20260508.tar.gz`：可交接上傳壓縮包（約 3.1MB）
- `checks/frame_03s.png`、`frame_28s.png`、`frame_54s.png`：驗證抽幀

## 驗證紀錄
- `ffprobe`：60 秒版 1080×1920、30fps、58.392 秒。
- `ffprobe`：30 秒版 1080×1920、30fps、30.960 秒。
- 視覺抽幀檢查：中文字可讀，無 tofu 方塊，無明顯裁切或重疊。

## 上傳標題候選
1. AI Agent 可以幫老師備課嗎？先檢查這 3 件事 #Shorts
2. AI 幫你備課，不代表可以直接上課 #Shorts
3. 把 AI 當助教，不是代課老師 #Shorts

## 下一步
30 秒剪短版已完成，可優先預覽 `episode-02-ai-agent-lesson-planning-30s-v1.mp4`；若採用此版上傳，建議同步附上 `narration_30s_edge_hsiaoyu.vtt` 作為字幕檔。下一個可自動推進項目：製作 Shorts 01 的 30 秒／15 秒剪短版，降低首支片超過 59 秒的壓線風險。
