# 長片素材包｜AI 會算 ≠ 懂物理

最後更新：2026-05-09 04:17 巡視自動推進

本資料夾承接 `../ai-can-calculate-not-understand-physics-script-v1.md` 的下一步，把長片腳本拆成可製作素材。

## 本輪產物
- `slide-card-outline.md`：9 張 16:9 簡報圖卡大綱，對應長片 0:00–7:00。
- `ai-solution-checklist-handout-v1.md`：一頁式「AI 解題檢查單」講義草稿，可做影片附件／下一支影片素材。
- `shorts-cutdown-hooks-v1.md`：3 支可從長片剪出的 Shorts 鉤子與 30 秒共用腳本模板。
- `cards_preview/card_01_hook_ai_can_calculate.png`：開場鉤子 16:9 圖卡。
- `cards_preview/card_02_model_not_formula.png`：模型／套公式對比圖卡。
- `cards_preview/card_03_condition_swap_check.png`：條件偷換檢查圖卡。
- `cards_preview/card_04_sign_direction_check.png`：方向與正負號檢查圖卡。
- `cards_preview/card_05_units_magnitude_check.png`：單位與量級檢查圖卡。
- `cards_preview/card_06_physical_meaning_check.png`：物理意義檢查圖卡。
- `cards_preview/card_07_classroom_workflow.png`：AI 初解到修正答案課堂流程圖卡。
- `cards_preview/card_08_student_checklist.png`：學生四格檢查清單圖卡。
- `cards_preview/card_09_cta_checklist_next.png`：下一支檢查單 CTA 圖卡。
- `cards_preview/contact_sheet_all_nine.png`：9 張圖卡縮圖檢查表。
- `cards_preview/contact_sheet_first_three.png`：前三張圖卡縮圖檢查表（舊版保留）。
- `render_all_cards.py`：可重生 9 張圖卡與 contact sheet 的 PIL 腳本。
- `render_first_three_cards.py`：可重生前三張圖卡的 PIL 腳本（舊版保留）。
- `slide_video_draft_v1/ai-can-calculate-not-understand-physics-slide-video-draft-v1.mp4`：用 9 張圖卡與 zh-TW 旁白組成的 16:9 長片 slide-video 草稿。
- `slide_video_draft_v1/README.md`：草稿規格、驗證與下一步說明。
- `ai-can-calculate-longform-slide-video-draft-v1-20260509.tar.gz`：長片草稿交接壓縮包，含腳本、圖卡、影片、旁白、字幕與抽幀檢查。
- `youtube-upload-kit-longform-v1.md`：長片上架文案交接包，含標題、說明欄、章節時間碼、置頂留言、縮圖文案與上架前檢查清單。
- `ai-can-calculate-longform-upload-kit-v1-20260509.tar.gz`：輕量上傳文案包，含上架文案、README、manifest、章節字幕、旁白文字、contact sheet 與縮圖 v2。
- `thumbnail_longform_ai_understands_physics_v2.png`：長片 1280×720 縮圖，主標 `AI 真的懂物理嗎？`，通過手機可讀性與亂碼檢查。
- `render_thumbnail_longform_v1.py`：可重生縮圖的 PIL 腳本。
- `../../shorts/sign-direction-not-decoration-20260509/`：長片導流 Shorts B「正負號不是裝飾」本機草稿、上架文案與交接壓縮包。

## 驗證紀錄
- PNG 規格：9 張圖卡皆為 1920×1080、RGB；`contact_sheet_all_nine.png` 為 1440×810。
- 視覺檢查：9 張縮圖檢查表中文字可讀，無 tofu 方塊／亂碼，無嚴重裁切、文字重疊或明顯排版錯誤；少數小字在縮圖下略吃力，但原圖可讀。
- Slide-video 草稿 v1：1920×1080、30fps、H.264 + AAC、片長 334.776 秒；旁白 mean_volume 約 -22.1 dB、max_volume 約 -2.0 dB；5 張抽幀檢查圖已產出，其中 167 秒抽幀經視覺檢查確認中文字可讀、無 tofu／裁切／字幕重疊。
- 交接壓縮包：`ai-can-calculate-longform-slide-video-draft-v1-20260509.tar.gz` 已建立並通過 `tar -tzf` 列表驗證。
- 長片上架文案包：`youtube-upload-kit-longform-v1.md` 已建立；`ai-can-calculate-longform-upload-kit-v1-20260509.tar.gz` 已重建並通過 `tar -tzf` 列表驗證；影片再次以 `ffprobe` 確認 1920×1080、30fps、334.776 秒。
- 長片縮圖 v2：1280×720、RGB；視覺檢查確認主標手機可讀、無 tofu／亂碼／裁切，主要訊息一秒內可理解。
- 導流 Shorts B 草稿：`../../shorts/sign-direction-not-decoration-20260509/sign-direction-not-decoration-shorts-draft-v1.mp4` 已完成，1080×1920、35.000 秒、H.264 + AAC；抽幀檢查確認繁中可讀、無 tofu／裁切／重疊，方向語意清楚；交接壓縮包已通過 `tar -tzf` 列表驗證。

## 建議下一步
1. 導流 Shorts B「正負號不是裝飾」本機草稿、上架文案與交接壓縮包已完成；下一個可自動推進項目：為 Shorts B 補一張可當 YouTube/Shorts 封面的 PNG，並重建包含封面的最終上傳交接包。
2. 若要拍真人／螢幕錄影，優先準備一份「AI 方向錯但數字看似合理」的物理解題截圖。

## 仍需使用者操作
- YouTube/Google 登入與實際上傳。
- 若要加入真實課堂案例或學生作品，需要使用者挑選可公開素材。
