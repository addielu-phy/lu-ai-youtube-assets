# AI 分層練習題：老師要先鎖哪三個變因？

狀態：第二季優先題 5 已完成本機 Shorts 草稿與上傳交接包。

## 內容定位
- 3 秒鉤子：分層不是變簡單，是控制變因。
- 老師把關句：先鎖概念、表示法、數字範圍，再請 AI 產三層題。
- 不使用真實學生資料。

## 已產出
- MP4：`lock-three-variables-practice-shorts-35s.mp4`
- 5 張 1080×1920 storyboard 圖卡：`slides/`
- 封面：`cover_lock_three_variables_practice_v1.png`
- 旁白：`narration_35s_edge_hsiaoyu.mp3`（zh-TW-HsiaoYuNeural）
- 字幕：`narration_35s.vtt` / `narration_35s.srt` / `narration_35s_edge_hsiaoyu.vtt`
- YouTube 上傳文案：`youtube-upload-kit.md`
- 教師可列印講義：`three-locks-teacher-printable-v1.md`
- QA：`checks/contact_sheet.png`、`checks/frames_contact_sheet.png`
- 交接壓縮包：`lock-three-variables-practice-upload-kit-20260511.tar.gz`

## 已驗證
- ffprobe：1080×1920、25fps、H.264 yuv420p + AAC、38.112 秒。
- PIL：封面、圖卡、抽幀皆為 1080×1920 RGB。
- 視覺 QA：繁體中文可讀，無 tofu 方塊、無文字裁切、無重疊、無錯誤底部署名；第 5 張 prompt 稍密但可接受。
- 壓縮包：已用 Python tarfile 讀回列出內容。

## 人工卡點
YouTube/Google 登入、頻道建立與實際上傳仍需使用者操作。

## 下一個可自動推進
已完成本支教師可列印「三鎖檢查表」：`three-locks-teacher-printable-v1.md`。若 YouTube/Google 登入仍未完成，下一步改從第二季題庫挑選尚未完成的下一支 Shorts storyboard／講義延伸；若已完成登入，優先上傳第一季首批或本支第二季 Shorts。
