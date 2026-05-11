# Slide-video 草稿 v1｜AI 會算 ≠ 懂物理

建立時間：2026-05-09 01:54 巡視自動推進

## 目的

用既有 9 張 16:9 圖卡與長片腳本，先組成一版可審節奏的 YouTube 長片 slide-video 草稿。這不是最終精剪版；用途是快速檢查：

- 旁白節奏是否順；
- 9 張圖卡是否足夠支撐 5–7 分鐘內容；
- 哪些段落需要補真人、螢幕錄影或 AI 解題截圖。

## 產物

- 影片草稿：`ai-can-calculate-not-understand-physics-slide-video-draft-v1.mp4`
- 旁白音檔：`narration_zhTW_hsiaoyu_v1.mp3`
- 旁白文字：`narration_slide_video_v1.txt`
- Edge TTS 字幕：`narration_zhTW_hsiaoyu_v1.vtt`
- 粗章節字幕：`chapter_subtitles_coarse_v1.srt`
- 組片清單：`slides_concat_v1.ffconcat`
- 規格／素材 manifest：`draft_v1_manifest.json`
- 抽幀檢查：`checks/frame_005s.png`、`frame_083s.png`、`frame_167s.png`、`frame_251s.png`、`frame_329s.png`

## 已驗證

- MP4：1920×1080、30fps、H.264、yuv420p、AAC mono。
- 片長：334.776 秒，約 5 分 35 秒。
- 檔案大小：約 8.99 MB。
- 旁白：`zh-TW-HsiaoYuNeural`，rate `-8%`；音量檢查 mean_volume 約 -22.1 dB、max_volume 約 -2.0 dB。
- 抽幀視覺檢查：中文字可讀，未見 tofu 方塊、裁切、字幕重疊；適合做長片草稿審閱。

## 下一步建議

1. 補一份 `youtube-upload-kit-longform-v1.md`：長片標題、說明欄、章節時間碼、置頂留言與縮圖文案。
2. 若要提升成正式版，優先補 3 種畫面素材：AI 解題截圖、老師紅筆檢查畫面、真人／螢幕錄影開場。
3. 若維持全圖卡路線，建議把第 3–6 段每段再拆成「錯誤例子」與「老師追問」兩張卡，讓視覺節奏更快。
