# YouTube Upload Kit｜AI 幫老師出題，第一步不是按生成

建立時間：2026-05-09 15:50 巡視自動推進  
狀態：本機 Shorts 草稿、旁白、VTT、封面與交接包已完成；實際上傳仍需使用者登入 YouTube/Google。

## 1. 建議上傳檔

- 影片：`teacher-question-generation-first-shorts-draft-v1.mp4`
- 封面：`cover_teacher_question_generation_first_v1.png`
- 旁白：`narration_35s_edge_hsiaoyu.mp3`
- 字幕：`narration_35s_edge_hsiaoyu.vtt`
- 分鏡：`shotlist.json`

## 2. 標題候選

1. AI 幫老師出題，第一步不是按生成 #Shorts
2. 叫 AI 出題前，先給它這 3 個限制 #Shorts
3. 老師用 AI 出題：不要直接按生成 #Shorts
4. AI 出題能不能用？先看這三個限制 #Shorts

## 3. 說明欄草稿

叫 AI 幫老師出題，不是先按「生成五題」。  
先定義三個限制：概念、年級難度、學生常見迷思。這樣 AI 產出的不是最後答案，而是一份可以被老師審稿、修正、再帶進課堂的題目草稿。

這支是「AI Agent 備課實驗」系列：讓 AI 加速草稿，但由老師把關教學目標、學生程度與概念正確性。

#AI教學 #教師日常 #備課 #AI工具 #Shorts

## 4. 置頂留言

你最怕 AI 幫忙出題時出現哪一種問題？  
A. 難度不對　B. 概念混在一起　C. 題目很像但答案怪怪的　D. 沒有抓到學生迷思

留言一個，我會把它整理成下一支「AI 備課不亂教」系列。

## 5. 上傳前人工確認

- [ ] 使用者已登入 YouTube/Google 並建立／選定頻道。
- [ ] 確認本片使用的是自製 prompt/範例，不含未公開考題或學生資料。
- [ ] 手機預覽封面文字 `別直接生成`、`先給 3 個限制` 清楚可讀。

## 6. 本機驗證

- `ffprobe`：1080×1920、30fps、H.264 + AAC、34.272 秒。
- 抽幀：`checks/frame_2s.png`、`checks/frame_16s.png`、`checks/frame_31s.png`。
- 視覺檢查：封面與抽幀主標繁中可讀、無 tofu 方塊、無嚴重裁切或重疊；影片採乾淨畫面搭配 VTT sidecar，避免字幕壓到圖卡。
