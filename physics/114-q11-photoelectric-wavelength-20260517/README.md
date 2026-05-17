# 114 分科物理第 11 題｜Lu Teacher slide-video draft v1

狀態：已完成本機 private vault 內部 MP4 草稿、YouTube upload kit v1 與 1080×1920 封面；尚未發布穩定 GitHub/GitHub Pages 連結。

## 主要檔案

- Lu Teacher 旁白版 MP4：`114-physics-q11-photoelectric-wavelength-change-slide-video-lu-teacher-v1.mp4`
- 旁白音訊：`narration-lu-teacher-f5tts-v1.mp3` / `narration-lu-teacher-f5tts-v1.wav`
- 字幕：`subtitles-lu-teacher-v1.srt` / `subtitles-lu-teacher-v1.vtt`
- 旁白稿：`narration-lu-teacher-v1.txt`
- QA 抽幀：`qa-frames-lu-voice-v1/`
- QA contact sheet：`qa-contact-sheet-lu-voice-v1.png`
- 建置腳本：`build_lu_teacher_slide_video_v1.py`
- YouTube upload kit：`youtube-upload-kit-v1.md`
- 直式封面：`cover-1080x1920.png`
- 交接包：`114-physics-q11-photoelectric-wavelength-change-lu-teacher-v1-kit.tar.gz`

## Timing map

- 0–7s：鉤子：不要把 K 直接乘 4/3。
- 7–29s：建模：同一金屬，phi 固定；E_photon = phi + Kmax。
- 29–56s：波長 640 nm → 480 nm；光子能量變 4/3 倍，多出 E_red/3。
- 56–78s：因為 E_red > K，所以 K_blue > 4K/3，答案 C。
- 78–88s：老師教法：畫兩根能量柱與固定 phi 門檻線。

## 授權／公開 gate

本草稿只使用題目摘要與自繪圖，不重製完整題文。正式上架前，仍需老師人工確認大考中心題文引用、截圖與來源標註方式。

## 已驗證

- MP4：1080×1920，H.264 + AAC，長度約 88.000 秒。
- 音訊：Lu Teacher F5-TTS voice clone v1；來源可由 `audio_source` 與 `lu_teacher_voice_v1/chunks_wav/` 追蹤。
- 字幕：SRT/VTT 依 8 段 timing map 產生。
- QA：抽幀與 contact sheet 已產生，供繁中可讀性與裁切檢查。
- 封面：`cover-1080x1920.png` 為 1080×1920 RGB。
- 交接包：包含 MP4、字幕、upload kit、封面、manifest 與建置腳本。

## 下一步

不要重做第 11 題 brief/storyboard/MP4/upload kit/封面；下一輪若仍無 YouTube 登入與公開題文授權確認，改選下一題候選（優先 114 分科物理第 12 題或下一個可安全摘要題）製作內部 brief。
