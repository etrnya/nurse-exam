# PENDING.md (護理師歷屆甄選試題學習系統待辦清單)

本清單用於追蹤 `nurse-exam` 專案的開發與測試進度，以及後續規劃之項目。

---

## 📅 開發進度

- [x] **第一階段：基礎設定與規劃確認**
  - [x] 建立 [GLOSSARY.md](file:///c:/Users/etrny/.gemini/antigravity/scratch/nurse-exam/GLOSSARY.md) (字典先行)
  - [x] 建立正式的 [RPD.md](file:///c:/Users/etrny/.gemini/antigravity/scratch/nurse-exam/RPD.md)
  - [x] 獲取操作者對 RPD 規劃的確認

- [x] **第二階段：自動化題庫爬取與提煉**
  - [x] 撰寫 `download_tainan_exams.py` 下載臺南市衛生局歷屆試題與答案 PDF (92~114 年)
  - [x] 撰寫 `download_moex_exams.py` 下載考選部近 5 年護理師高考 5 大科目的試題、答案、更正答案 PDF (110~114 年)
  - [x] 撰寫 `parse_exams.py` 提取 PDF 文字並對齊答案（更正答案優先），結合大語言模型 (LLM) 進行標籤分類自動貼標，生成 `questions_db.js` 與 `answers_db.js`

- [x] **第三階段：前端模擬測驗門戶移植與優化**
  - [x] 移植並修改前端 `study_portal.html` 入口，調整為醫護調和色系
  - [x] 串接結構化題庫資料（`questions_db.js`、`answers_db.js`）
  - [x] 實作標籤統計儀表板與標籤過濾篩選功能
  - [x] 整合 Gemini API 智能解題助手，並快取解析內容至 LocalStorage
  - [x] 實作選擇題作答互動機制（A/B/C/D 作答按鈕、多重答案比對、一律給分 `*` 比對與歷史紀錄統計）
  - [x] 清除全專案之第一人稱與第二人稱代名詞，對齊人稱規約
  - [x] 進行整體語法編譯與 Pre-Commit 安全門禁檢驗，完成推送與收工

---

## 🧪 測試結果
- [x] 已完成前端單網頁應用程式 (SPA) 的核心渲染測試
- [x] 已通過自動化修補與語意標記驗證，無人稱代詞規約衝突

---

## 📋 後續待辦 (Future Backlog)
- [ ] **Notion-tw-legal-rag 專案**（暫緩執行，待後續重新啟動後規劃技術架構）
