# Slide-video 草稿 v1｜AI Agent 可檢查教案草稿

建立時間：2026-05-10 09:30 巡視自動推進

## 目的

把既有 5 張 16:9 storyboard 卡，先組成一版可審節奏的 5 分鐘長片 slide-video 草稿。這不是最終精剪版；用途是快速檢查：

- 「AI Agent 備課」流程是否能被老師理解；
- 5 張卡是否足夠支撐 4–6 分鐘內容；
- 後續正式版是否需要補 prompt、AI 輸出截圖、老師三色筆審稿畫面或真人開場。

## 產物

- 影片草稿：`ai-agent-checkable-lesson-slide-video-draft-v1.mp4`
- 旁白音檔：`narration_zhTW_hsiaoyu_v1.mp3`
- 旁白文字：`narration_slide_video_v1.txt`
- Edge TTS 字幕：`narration_zhTW_hsiaoyu_v1.vtt`
- 粗章節字幕：`chapter_subtitles_coarse_v1.srt`
- 組片清單：`slides_concat_v1.ffconcat`
- 規格／素材 manifest：`draft_v1_manifest.json`
- 抽幀檢查：`checks/frame_005s.png`、`frame_064s.png`、`frame_129s.png`、`frame_193s.png`、`frame_264s.png`
- 抽幀 contact sheet：`checks/frame_contact_sheet.png`

## 已驗證

- MP4：1920×1080、30fps、H.264、yuv420p、AAC mono。
- 片長：322.600 秒，約 5 分 23 秒。
- 檔案大小：約 5.45 MB。
- 旁白：`zh-TW-HsiaoYuNeural`，rate `-8%`。
- 抽幀視覺檢查：中文字可讀，未見 tofu 方塊、裁切、重疊或過度擁擠；適合做長片草稿審閱。

## 下一步建議

1. 已自動推進：`youtube-upload-kit-longform-v1.md` 已完成，含標題、說明欄、章節時間碼、置頂留言、縮圖方向與人工作業清單。
2. 已自動推進：輕量交接壓縮包 `ai-agent-checkable-lesson-longform-upload-kit-v1-20260510.tar.gz` 已完成，包含 upload kit、README、manifest、字幕、旁白文字與抽幀 contact sheet；未重複打包大型 MP4。
3. 下一個可自動推進項目：若仍無法登入 YouTube，補這支長片的「三色筆審稿檢查表」可分享講義，作為說明欄下載／貼文延伸素材。
4. 若要提升成正式版，優先補 3 種畫面素材：實際 prompt、AI 輸出截圖、老師三色筆審稿畫面。
5. 若使用者完成 YouTube/Google 登入，仍優先上傳首批 Shorts；這支長片可作為頻道第二波內容。
