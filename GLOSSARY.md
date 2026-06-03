# 專案統一詞彙表 (GLOSSARY.md)

本文件明確定義「護理師歷屆甄選試題智能學習系統 (`nurse-exam`)」中使用的所有專業術語、英文對照及程式碼變數命名標準。後續所有系統規劃與代碼編寫必須嚴格遵守此規範。

---

## 📌 1. 核心專案名詞 (Project Core Terms)

| 中文專業術語 | 英文術語 (English Term) | 程式碼命名標準 (Code Variable / Path) | 定義與業務邏輯 |
| :--- | :--- | :--- | :--- |
| 護理師歷屆甄選試題系統 | Nurse Exam Study System | `nurse-exam` | 專案的根目錄與儲存庫識別名稱 |
| 模擬測驗門戶網頁 | Nurse Study Portal | `study_portal.html` | 前端單網頁應用程式 (SPA) 的主要進入點與呈現介面 |
| 題庫資料庫 | Question Database | `questions_db.js` | 儲存提取出的所有選擇題 JSON 資料之靜態 JS 檔案 |
| 答案資料庫 | Answer Database | `answers_db.js` | 儲存每道試題對應之標準答案的靜態 JS 檔案 |
| 學習卡片資料庫 | Study Cards Database | `study_cards_db.js` | 儲存間隔重複複習卡片的本地瀏覽器 (LocalStorage) 結構名稱 |

---

## ⚙️ 2. 資料獲取與解析術語 (Ingestion & Parsing Terms)

| 中文專業術語 | 英文術語 (English Term) | 程式碼命名標準 (Code Variable / Path) | 定義與業務邏輯 |
| :--- | :--- | :--- | :--- |
| 臺南市歷屆試題下載器 | Tainan Exam Downloader | `download_tainan_exams.py` | 自動化爬取並下載臺南市衛生局甄試 PDF 題庫的腳本 |
| 考選部護理師考題下載器 | MOEX Exam Downloader | `download_moex_exams.py` | 下載考選部護理師高考 PDF 題庫的自動化指令腳本 |
| 試題解析器 | Exam Question Parser | `parse_exams.py` | 讀取並提煉 PDF 內容，將其轉換為結構化選擇題 JSON 的解析腳本 |
| 試題快取目錄 | Exam PDF Cache | `downloads/` | 用於暫存下載的試題 PDF 檔案的實體資料夾名稱 |

---

## 🧠 3. 業務模型與資料欄位 (Domain Models & Database Fields)

在程式碼、JSON 結構與前端變數中，凡涉及考題資料模型，均須嚴格對齊以下欄位標準：

| 欄位名稱 (中文) | 欄位名稱 (代碼) | 資料型態 | 範例與值域限制 |
| :--- | :--- | :--- | :--- |
| 題目唯一識別碼 | `id` | String | `tainan-102-01` (來源-年份-題號) 或 `moex-114-1-01` (來源-年份-科目代碼-題號) |
| 題目主體 | `question` | String | "下列何者為急性闌尾炎的最典型症狀？" |
| 選項列表 | `options` | Object | `{"A": "...", "B": "...", "C": "...", "D": "..."}` |
| 標準答案 | `answer` | String | `"A"`、`"B"`、`"C"` 或 `"D"` |
| 試卷來源分類 | `category` | String | `"臺南市衛生局甄試"` 或 `"考選部護理師高考"` |
| 專業科目分類 | `subject` | String | `"基礎醫學"`, `"基本護理學與護理行政"`, `"內外科護理學"`, `"產兒科護理學"`, `"精神科與社區衛生護理學"` |
| 試卷年份 | `year` | Integer | `114` (一律採用民國年份) |
| 標籤與範圍分類 | `tags` | Array | `["生理學", "呼吸系統"]` |
| 考題解析與重點 | `explanation`| String | AI 生成或快取的考點解析與說明 (Markdown 格式) |
| 考題推薦權重 | `weight` | Float | 台南市衛生局甄試預設為 `1.5`，考選部高考預設為 `1.0` |
| 答題狀態 | `status` | String | `"correct"` (答對)、`"incorrect"` (答錯)、`"unattempted"` (未作答) |
