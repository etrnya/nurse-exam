# -*- coding: utf-8 -*-
"""
用於更新 study_portal.html 以對齊護理師模擬測驗 SPA 的 Python 腳本。
"""
import os
import re

def main():
    file_path = "study_portal.html"
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read().replace("\r\n", "\n")

    # 1. 替換 CSS Root 變數為醫護配色
    old_root = """        :root {
            --bg-color: #0b0f19;
            --sidebar-bg: rgba(15, 23, 42, 0.95);
            --card-bg: rgba(22, 30, 49, 0.7);
            --card-border: rgba(255, 255, 255, 0.06);
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --accent-gradient: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
            --accent-color: #6366f1;
            --accent-hover: #4f46e5;
            --success-color: #10b981;
            --warning-color: #f59e0b;
            --error-color: #ef4444;
            --transition-speed: 0.3s;
            --font-family: 'Inter', 'Noto Sans TC', sans-serif;
            --sidebar-width: 320px;
            --card-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }

        [data-theme="light"] {
            --bg-color: #f8fafc;
            --sidebar-bg: #ffffff;
            --card-bg: #ffffff;
            --card-border: #e2e8f0;
            --text-primary: #0f172a;
            --text-secondary: #475569;
            --accent-gradient: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
            --accent-color: #4f46e5;
            --accent-hover: #3730a3;
            --card-shadow: 0 4px 12px rgba(15, 23, 42, 0.05);
        }"""
    
    new_root = """        :root {
            --bg-color: #0a1219;
            --sidebar-bg: rgba(13, 27, 38, 0.95);
            --card-bg: rgba(20, 39, 54, 0.7);
            --card-border: rgba(255, 255, 255, 0.06);
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --accent-gradient: linear-gradient(135deg, #0d9488 0%, #0284c7 100%);
            --accent-color: #0d9488;
            --accent-hover: #0f766e;
            --success-color: #10b981;
            --warning-color: #f59e0b;
            --error-color: #ef4444;
            --transition-speed: 0.3s;
            --font-family: 'Inter', 'Noto Sans TC', sans-serif;
            --sidebar-width: 320px;
            --card-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }

        [data-theme="light"] {
            --bg-color: #f0f7f4;
            --sidebar-bg: #ffffff;
            --card-bg: #ffffff;
            --card-border: #cbdbe5;
            --text-primary: #0f2922;
            --text-secondary: #47655f;
            --accent-gradient: linear-gradient(135deg, #0f766e 0%, #0369a1 100%);
            --accent-color: #0f766e;
            --accent-hover: #115e59;
            --card-shadow: 0 4px 12px rgba(15, 23, 42, 0.05);
        }"""
    content = content.replace(old_root, new_root)

    # 2. 在 </style> 之前插入自訂的選擇題作答按鈕與 Bento 統計卡片 CSS
    new_css = """
        /* Bento 統計卡片樣式 */
        .stats-card {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--card-border);
            border-radius: 0.75rem;
            padding: 1rem;
            margin-bottom: 1.25rem;
            transition: background-color var(--transition-speed), border-color var(--transition-speed);
        }
        [data-theme="light"] .stats-card {
            background: #ffffff;
            border-color: #cbdbe5;
        }
        .stats-progress-container {
            display: flex;
            align-items: center;
            gap: 1rem;
            margin-bottom: 0.75rem;
        }
        .stats-circular-progress {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            flex-shrink: 0;
            transition: background var(--transition-speed);
        }
        .stats-circular-progress::before {
            content: "";
            position: absolute;
            width: 40px;
            height: 40px;
            background: var(--bg-color);
            border-radius: 50%;
            transition: background var(--transition-speed);
        }
        [data-theme="light"] .stats-circular-progress::before {
            background: #ffffff;
        }
        .stats-progress-value {
            position: relative;
            font-size: 0.85rem;
            font-weight: 700;
            color: var(--text-primary);
        }
        .stats-text-group {
            display: flex;
            flex-direction: column;
        }
        .stats-main-label {
            font-size: 0.85rem;
            font-weight: 600;
            color: var(--text-primary);
        }
        .stats-sub-label {
            font-size: 0.75rem;
            color: var(--text-secondary);
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 0.5rem;
            border-top: 1px solid var(--card-border);
            padding-top: 0.75rem;
            margin-top: 0.25rem;
        }
        .stats-grid-item {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .stats-grid-num {
            font-size: 0.95rem;
            font-weight: 700;
        }
        .stats-grid-label {
            font-size: 0.7rem;
            color: var(--text-secondary);
        }

        /* 選擇題選項與互動樣式 */
        .options-container {
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
            margin-top: 1rem;
            margin-bottom: 1.25rem;
        }
        .option-btn {
            display: flex;
            align-items: flex-start;
            gap: 0.75rem;
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--card-border);
            border-radius: 0.5rem;
            padding: 0.85rem 1rem;
            text-align: left;
            color: var(--text-primary);
            cursor: pointer;
            font-family: var(--font-family);
            font-size: 0.92rem;
            transition: all 0.2s ease;
            width: 100%;
            outline: none;
        }
        [data-theme="light"] .option-btn {
            background: #ffffff;
            border-color: #cbd5e1;
        }
        .option-btn:hover:not(.success):not(.error):not(.disabled) {
            border-color: var(--accent-color);
            background: rgba(13, 148, 136, 0.05);
        }
        .option-letter {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 24px;
            height: 24px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.08);
            font-size: 0.8rem;
            font-weight: 700;
            flex-shrink: 0;
            color: var(--text-primary);
            transition: all 0.2s ease;
        }
        [data-theme="light"] .option-letter {
            background: #f1f5f9;
        }
        .option-btn:hover:not(.success):not(.error):not(.disabled) .option-letter {
            background: var(--accent-color);
            color: #ffffff;
        }
        .option-text {
            line-height: 1.4;
            flex: 1;
        }
        .option-btn.success {
            background: rgba(16, 185, 129, 0.12) !important;
            border-color: #10b981 !important;
            color: #10b981 !important;
        }
        .option-btn.success .option-letter {
            background: #10b981 !important;
            color: #ffffff !important;
        }
        .option-btn.error {
            background: rgba(239, 68, 68, 0.12) !important;
            border-color: #ef4444 !important;
            color: #ef4444 !important;
        }
        .option-btn.error .option-letter {
            background: #ef4444 !important;
            color: #ffffff !important;
        }
        .option-btn.disabled {
            cursor: default;
            opacity: 0.85;
        }

        /* 答題結果回饋 */
        .answer-feedback-box {
            border-radius: 0.5rem;
            padding: 1rem;
            margin-bottom: 1.25rem;
            display: flex;
            flex-direction: column;
            gap: 0.35rem;
            font-size: 0.9rem;
            animation: slideIn 0.3s ease;
        }
        .answer-feedback-box.success {
            background: rgba(16, 185, 129, 0.08);
            border: 1px solid rgba(16, 185, 129, 0.2);
            color: #10b981;
        }
        .answer-feedback-box.error {
            background: rgba(239, 68, 68, 0.08);
            border: 1px solid rgba(239, 68, 68, 0.2);
            color: #ef4444;
        }
        .answer-feedback-title {
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        /* Switch toggle round */
        .switch-container input:checked + .slider-round {
            background-color: var(--error-color) !important;
        }
        .slider-round::before {
            position: absolute;
            content: "";
            height: 14px;
            width: 14px;
            left: 3px;
            bottom: 3px;
            background-color: white;
            transition: .3s;
            border-radius: 50%;
        }
        .switch-container input:checked + .slider-round::before {
            transform: translateX(16px);
        }

        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(-10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
    </style>"""
    content = content.replace("    </style>", new_css)

    # 3. 替換 HTML Title
    old_title = "<title>食品衛生檢驗國考 - AI 智能學習與解題門戶</title>"
    new_title = "<title>護理師國考與歷屆甄選 - AI 智能測驗與錯題學習系統</title>"
    content = content.replace(old_title, new_title)

    # 4. 替換中間主題欄的 HTML
    old_topics_panel = """                    <!-- Column 1: Topics Selector -->
                    <div class="topics-panel" id="topics-panel">
                        <div class="panel-title" style="justify-content: space-between;">
                            <span class="title-text-group">
                                <i class="fa-solid fa-tags" style="color: var(--accent-color);"></i>
                                <span id="topics-panel-title">學習主題</span>
                            </span>
                            <button class="btn-icon-sm" id="topics-toggle-btn" title="收折/展開主題欄">
                                <i class="fa-solid fa-angle-left"></i>
                            </button>
                        </div>
                        <ul class="topic-list" id="topic-list">
                            <!-- Dynamic list of topics -->
                        </ul>
                    </div>"""
    
    new_topics_panel = """                    <!-- Column 1: Topics Selector -->
                    <div class="topics-panel" id="topics-panel">
                        <div class="panel-title" style="justify-content: space-between; margin-bottom: 1rem;">
                            <span class="title-text-group">
                                <i class="fa-solid fa-tags" style="color: var(--accent-color);"></i>
                                <span id="topics-panel-title">考點標籤分析</span>
                            </span>
                            <button class="btn-icon-sm" id="topics-toggle-btn" title="收折/展開主題欄">
                                <i class="fa-solid fa-angle-left"></i>
                            </button>
                        </div>
                        
                        <!-- 統計分析儀表板 -->
                        <div id="stats-dashboard"></div>
                        
                        <!-- 僅顯示錯題篩選開關 -->
                        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1.25rem; padding: 0.65rem 0.85rem; background: rgba(239, 68, 68, 0.05); border: 1px dashed rgba(239, 68, 68, 0.2); border-radius: 0.5rem;">
                            <span style="font-size: 0.8rem; font-weight: 600; color: var(--text-primary); display: flex; align-items: center; gap: 0.35rem;">
                                <i class="fa-solid fa-triangle-exclamation" style="color: var(--error-color);"></i> 僅複習錯題
                            </span>
                            <label class="switch-container" style="position: relative; display: inline-block; width: 36px; height: 20px;">
                                <input type="checkbox" id="wrong-filter-checkbox" style="opacity: 0; width: 0; height: 0;">
                                <span class="slider-round" style="position: absolute; cursor: pointer; top: 0; left: 0; right: 0; bottom: 0; background-color: var(--card-border); transition: .3s; border-radius: 20px;"></span>
                            </label>
                        </div>
                        
                        <ul class="topic-list" id="topic-list">
                            <!-- Dynamic list of topics -->
                        </ul>
                    </div>"""
    content = content.replace(old_topics_panel, new_topics_panel)

    # 5. 修改載入的 js 的變數與 initApp 開頭
    old_script_start = """        // Global State Management
        let currentSubject = "食品微生物學";
        let currentTopic = ""; 
        let searchQuery = "";
        let theme = localStorage.getItem("theme") || "dark";
        let viewMode = "questions"; // 'questions' or 'cards'
        let activeQuestion = null; // Currently clicked question object

        // DOM Elements
        const sidebarEl = document.getElementById("sidebar");
        const sidebarToggleEl = document.getElementById("sidebar-toggle");
        const subjectListEl = document.getElementById("subject-list");
        const topicListEl = document.getElementById("topic-list");
        const questionStreamEl = document.getElementById("question-stream");
        const searchInputEl = document.getElementById("search-input");
        const searchBarContainerEl = document.getElementById("search-bar-container");
        const themeToggleEl = document.getElementById("theme-toggle");
        
        // Mode switch elements
        const modeQuestionsBtn = document.getElementById("mode-questions-btn");
        const modeCardsBtn = document.getElementById("mode-cards-btn");
        const questionsWorkspaceLayout = document.getElementById("questions-workspace-layout");
        const cardsWorkspaceLayout = document.getElementById("cards-workspace-layout");
        const studyCardRenderArea = document.getElementById("study-card-render-area");

        // Split Details Panel Elements
        const detailPanelEl = document.getElementById("detail-panel");
        const detailPlaceholderEl = document.getElementById("detail-placeholder");
        const detailActiveContainer = document.getElementById("detail-active-container");
        const detailCloseBtn = document.getElementById("detail-close-btn");
        const detailContentEl = document.getElementById("detail-content");

        // API Key Settings elements
        const apiKeyInputEl = document.getElementById("api-key-input");
        const toggleKeyVisibilityBtn = document.getElementById("toggle-key-visibility");
        const apiModelSelectEl = document.getElementById("api-model-select");
        const btnSaveApiEl = document.getElementById("btn-save-api");
        let activeCardTopic = ""; // Selected topic name in Cards Mode

        function initApp() {
            // Populate Subjects
            populateSubjects();
            
            // Set Default Topic to first non-empty topic of selected subject
            const activeTopics = Object.keys(window.QUESTIONS_DB[currentSubject]).filter(t => window.QUESTIONS_DB[currentSubject][t].length > 0);
            currentTopic = activeTopics.includes("Topic 1: 食品指標微生物") ? "Topic 1: 食品指標微生物" : (activeTopics[0] || "");
            
            // Populate Topics and Questions
            renderTopics();
            renderQuestions();"""

    new_script_start = """        // Fallback for missing libraries
        window.STUDY_CARDS_DB = window.STUDY_CARDS_DB || {};
        window.ANSWERS_DB = typeof answers_db !== 'undefined' ? answers_db : {};

        // Convert flat questions_db to hierarchal window.QUESTIONS_DB
        function buildQuestionsDbHierarchy() {
            window.QUESTIONS_DB = {};
            
            const allSubjects = [
                "基礎醫學",
                "基本護理學與護理行政",
                "內外科護理學",
                "產兒科護理學",
                "精神科與社區衛生護理學",
                "綜合護理與公共衛生"
            ];
            
            allSubjects.forEach(subj => {
                window.QUESTIONS_DB[subj] = {};
            });
            
            const items = typeof questions_db !== 'undefined' ? questions_db : [];
            
            items.forEach(q => {
                const numberMatch = q.id.match(/-(\d+)$/);
                const number = numberMatch ? parseInt(numberMatch[1], 10) : 1;
                
                const qAdapted = {
                    id: q.id,
                    text: q.question, // Adapt to original key
                    question: q.question,
                    options: q.options,
                    year: `${q.year}年`,
                    level: q.category,
                    number: number,
                    subject: q.subject,
                    tags: q.tags || [q.subject],
                    weight: q.weight || 1.0
                };
                
                const subj = q.subject || "綜合護理與公共衛生";
                if (!window.QUESTIONS_DB[subj]) {
                    window.QUESTIONS_DB[subj] = {};
                }
                
                const tags = qAdapted.tags.length > 0 ? qAdapted.tags : [subj];
                tags.forEach(tag => {
                    if (!window.QUESTIONS_DB[subj][tag]) {
                        window.QUESTIONS_DB[subj][tag] = [];
                    }
                    window.QUESTIONS_DB[subj][tag].push(qAdapted);
                });
            });
        }

        buildQuestionsDbHierarchy();

        // Global State Management
        let currentSubject = "基礎醫學";
        let currentTopic = ""; 
        let searchQuery = "";
        let theme = localStorage.getItem("theme") || "dark";
        let viewMode = "questions"; // 'questions' or 'cards'
        let activeQuestion = null; // Currently clicked question object
        let showOnlyWrong = false; // Filter wrong questions

        // DOM Elements
        const sidebarEl = document.getElementById("sidebar");
        const sidebarToggleEl = document.getElementById("sidebar-toggle");
        const subjectListEl = document.getElementById("subject-list");
        const topicListEl = document.getElementById("topic-list");
        const questionStreamEl = document.getElementById("question-stream");
        const searchInputEl = document.getElementById("search-input");
        const searchBarContainerEl = document.getElementById("search-bar-container");
        const themeToggleEl = document.getElementById("theme-toggle");
        const wrongFilterCheckbox = document.getElementById("wrong-filter-checkbox");
        
        // Mode switch elements
        const modeQuestionsBtn = document.getElementById("mode-questions-btn");
        const modeCardsBtn = document.getElementById("mode-cards-btn");
        const questionsWorkspaceLayout = document.getElementById("questions-workspace-layout");
        const cardsWorkspaceLayout = document.getElementById("cards-workspace-layout");
        const studyCardRenderArea = document.getElementById("study-card-render-area");

        // Split Details Panel Elements
        const detailPanelEl = document.getElementById("detail-panel");
        const detailPlaceholderEl = document.getElementById("detail-placeholder");
        const detailActiveContainer = document.getElementById("detail-active-container");
        const detailCloseBtn = document.getElementById("detail-close-btn");
        const detailContentEl = document.getElementById("detail-content");

        // API Key Settings elements
        const apiKeyInputEl = document.getElementById("api-key-input");
        const toggleKeyVisibilityBtn = document.getElementById("toggle-key-visibility");
        const apiModelSelectEl = document.getElementById("api-model-select");
        const btnSaveApiEl = document.getElementById("btn-save-api");
        let activeCardTopic = ""; // Selected topic name in Cards Mode

        function initApp() {
            // Populate Subjects
            populateSubjects();
            
            // Set Default Topic to first non-empty topic of selected subject
            const activeTopics = Object.keys(window.QUESTIONS_DB[currentSubject]).filter(t => window.QUESTIONS_DB[currentSubject][t].length > 0);
            currentTopic = activeTopics[0] || "";
            
            // Populate Topics and Questions
            renderTopics();
            renderQuestions();

            // Wrong question filter switch listener
            if (wrongFilterCheckbox) {
                wrongFilterCheckbox.addEventListener("change", (e) => {
                    showOnlyWrong = e.target.checked;
                    renderQuestions();
                });
            }"""
    content = content.replace(old_script_start, new_script_start)

    # 6. 替換 populateSubjects 函數
    old_populate = """        function populateSubjects() {
            subjectListEl.innerHTML = "";
            const icons = {
                "食品微生物學": "fa-microscope",
                "食品安全與衛生法規": "fa-shield-halved",
                "食品化學": "fa-flask",
                "食品分析與檢驗": "fa-vials",
                "食品加工學": "fa-industry",
                "生物統計學": "fa-chart-simple"
            };

            Object.keys(window.QUESTIONS_DB).forEach(subj => {
                const btn = document.createElement("button");
                btn.className = `subject-btn ${subj === currentSubject ? 'active' : ''}`;
                
                // Count total questions for badge
                let total = 0;
                Object.values(window.QUESTIONS_DB[subj]).forEach(qList => {
                    total += qList.length;
                });
                
                const iconClass = icons[subj] || "fa-book";
                btn.innerHTML = `
                    <span class="subject-icon-wrapper"><i class="fa-solid ${iconClass}"></i></span>
                    <span class="subject-text">${subj}</span>
                    <span class="badge">${total}</span>
                `;
                
                btn.addEventListener("click", () => {
                    document.querySelectorAll(".subject-btn").forEach(el => el.classList.remove("active"));
                    btn.classList.add("active");
                    currentSubject = subj;
                    
                    // Reset selected topic to first non-empty topic
                    const activeTopics = Object.keys(window.QUESTIONS_DB[currentSubject]).filter(t => window.QUESTIONS_DB[currentSubject][t].length > 0);
                    currentTopic = activeTopics.includes("Topic 1: 食品指標微生物") ? "Topic 1: 食品指標微生物" : (activeTopics[0] || "");
                    
                    renderTopics();
                    renderQuestions();
                    closeDetailsPane();
                    
                    // If in cards mode, reload the ranking list for the new subject
                    if (viewMode === "cards") {
                        renderCardsModeRanking();
                    }
                });
                
                subjectListEl.appendChild(btn);
            });
        }"""

    new_populate = """        function populateSubjects() {
            subjectListEl.innerHTML = "";
            const icons = {
                "基礎醫學": "fa-brain",
                "基本護理學與護理行政": "fa-user-nurse",
                "內外科護理學": "fa-heartpulse",
                "產兒科護理學": "fa-baby",
                "精神科與社區衛生護理學": "fa-house-chimney-medical",
                "綜合護理與公共衛生": "fa-notes-medical"
            };

            Object.keys(window.QUESTIONS_DB).forEach(subj => {
                const btn = document.createElement("button");
                btn.className = `subject-btn ${subj === currentSubject ? 'active' : ''}`;
                
                // Count total questions for badge (deduplicated by id)
                const uniqueIds = new Set();
                Object.values(window.QUESTIONS_DB[subj]).forEach(qList => {
                    qList.forEach(q => uniqueIds.add(q.id));
                });
                const total = uniqueIds.size;
                
                const iconClass = icons[subj] || "fa-book-medical";
                btn.innerHTML = `
                    <span class="subject-icon-wrapper"><i class="fa-solid ${iconClass}"></i></span>
                    <span class="subject-text">${subj}</span>
                    <span class="badge">${total}</span>
                `;
                
                btn.addEventListener("click", () => {
                    document.querySelectorAll(".subject-btn").forEach(el => el.classList.remove("active"));
                    btn.classList.add("active");
                    currentSubject = subj;
                    
                    // Reset selected topic to first non-empty topic
                    const activeTopics = Object.keys(window.QUESTIONS_DB[currentSubject]).filter(t => window.QUESTIONS_DB[currentSubject][t].length > 0);
                    currentTopic = activeTopics[0] || "";
                    
                    renderTopics();
                    renderQuestions();
                    closeDetailsPane();
                    
                    // If in cards mode, reload the ranking list for the new subject
                    if (viewMode === "cards") {
                        renderCardsModeRanking();
                    }
                });
                
                subjectListEl.appendChild(btn);
            });
        }"""
    content = content.replace(old_populate, new_populate)

    # 7. 替換 renderTopics 函數並加上 renderStatsDashboard
    old_render_topics = """        function renderTopics() {
            topicListEl.innerHTML = "";
            const topicsObj = window.QUESTIONS_DB[currentSubject];
            
            // Filter out empty topics and re-order topics so comprehensive is last
            const topicsKeys = Object.keys(topicsObj)
                .filter(t => topicsObj[t] && topicsObj[t].length > 0)
                .sort((a, b) => {
                    if (a.includes("其他")) return 1;
                    if (b.includes("其他")) return -1;
                    return a.localeCompare(b);
                });
            
            topicsKeys.forEach((topic, idx) => {
                const qList = topicsObj[topic];
                const item = document.createElement("li");
                item.className = `topic-item ${topic === currentTopic ? 'active' : ''}`;
                item.setAttribute("data-index", idx + 1);
                item.innerHTML = `
                    <span>${topic}</span>
                    <span class="badge-topic">${qList.length}</span>
                `;
                
                item.addEventListener("click", () => {
                    document.querySelectorAll(".topic-item").forEach(el => el.classList.remove("active"));
                    item.classList.add("active");
                    currentTopic = topic;
                    renderQuestions();
                    closeDetailsPane();
                });
                
                topicListEl.appendChild(item);
            });
        }"""

    new_render_topics = """        function renderTopics() {
            topicListEl.innerHTML = "";
            const topicsObj = window.QUESTIONS_DB[currentSubject];
            
            // Filter out empty topics and re-order topics so comprehensive is last
            const topicsKeys = Object.keys(topicsObj)
                .filter(t => topicsObj[t] && topicsObj[t].length > 0)
                .sort((a, b) => {
                    if (a.includes("其他")) return 1;
                    if (b.includes("其他")) return -1;
                    return a.localeCompare(b);
                });
            
            topicsKeys.forEach((topic, idx) => {
                const qList = topicsObj[topic];
                const item = document.createElement("li");
                item.className = `topic-item ${topic === currentTopic ? 'active' : ''}`;
                item.setAttribute("data-index", idx + 1);
                item.innerHTML = `
                    <span>${topic}</span>
                    <span class="badge-topic">${qList.length}</span>
                `;
                
                item.addEventListener("click", () => {
                    document.querySelectorAll(".topic-item").forEach(el => el.classList.remove("active"));
                    item.classList.add("active");
                    currentTopic = topic;
                    renderQuestions();
                    closeDetailsPane();
                });
                
                topicListEl.appendChild(item);
            });

            // 繪製統計儀表板
            renderStatsDashboard();
        }

        // 繪製當前科目 Bento 統計分析儀表板
        function renderStatsDashboard() {
            const statsContainer = document.getElementById("stats-dashboard");
            if (!statsContainer) return;
            
            // 計算當前 Subject 下所有的不重複題目
            const questions = [];
            Object.values(window.QUESTIONS_DB[currentSubject]).forEach(qList => {
                qList.forEach(q => {
                    if (!questions.some(item => item.id === q.id)) {
                        questions.push(q);
                    }
                });
            });
            
            const totalCount = questions.length;
            
            // 從 localStorage 取得已作答的答對與答錯題目 id 陣列
            const wrongIds = JSON.parse(localStorage.getItem("wrong_questions") || "[]");
            const correctIds = JSON.parse(localStorage.getItem("correct_questions") || "[]");
            
            // 統計當前科目的正確與錯誤題量
            const subjectWrongCount = questions.filter(q => wrongIds.includes(q.id)).length;
            const subjectCorrectCount = questions.filter(q => correctIds.includes(q.id)).length;
            const answeredCount = subjectWrongCount + subjectCorrectCount;
            
            const accuracy = answeredCount > 0 ? Math.round((subjectCorrectCount / answeredCount) * 100) : 0;
            const progress = totalCount > 0 ? Math.round((answeredCount / totalCount) * 100) : 0;
            
            statsContainer.innerHTML = `
                <div class="stats-card">
                    <div class="stats-progress-container">
                        <div class="stats-circular-progress" style="background: conic-gradient(var(--accent-color) ${progress * 3.6}deg, var(--card-border) 0deg);">
                            <div class="stats-progress-value">${progress}%</div>
                        </div>
                        <div class="stats-text-group">
                            <div class="stats-main-label">學習進度</div>
                            <div class="stats-sub-label">已答 ${answeredCount} / 總計 ${totalCount} 題</div>
                        </div>
                    </div>
                    <div class="stats-grid">
                        <div class="stats-grid-item">
                            <span class="stats-grid-num" style="color: var(--success-color);">${subjectCorrectCount}</span>
                            <span class="stats-grid-label">答對</span>
                        </div>
                        <div class="stats-grid-item">
                            <span class="stats-grid-num" style="color: var(--error-color);">${subjectWrongCount}</span>
                            <span class="stats-grid-label">答錯</span>
                        </div>
                        <div class="stats-grid-item">
                            <span class="stats-grid-num" style="color: var(--warning-color);">${accuracy}%</span>
                            <span class="stats-grid-label">正確率</span>
                        </div>
                    </div>
                </div>
            `;
        }"""
    content = content.replace(old_render_topics, new_render_topics)

    # 8. 替換 renderQuestions 函數
    old_render_questions = """        function renderQuestions() {
            questionStreamEl.innerHTML = "";
            
            // Shallow copy questions to avoid DB mutation
            let questions = [...(window.QUESTIONS_DB[currentSubject][currentTopic] || [])];
            
            // Apply search filter if present
            if (searchQuery.trim() !== "") {
                const query = searchQuery.toLowerCase();
                questions = [];
                // If search query, search across ALL topics in the current subject
                Object.values(window.QUESTIONS_DB[currentSubject]).forEach(qList => {
                    qList.forEach(q => {
                        if (q.text.toLowerCase().includes(query) || q.year.toLowerCase().includes(query) || q.level.toLowerCase().includes(query)) {
                            questions.push(q);
                        }
                    });
                });
            }

            // SORT questions: Newest on Top (Descending)
            questions.sort((a, b) => getYearNumber(b.year) - getYearNumber(a.year));
            
            if (questions.length === 0) {
                questionStreamEl.innerHTML = `
                    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 200px; color: var(--text-secondary);">
                        <i class="fa-solid fa-magnifying-glass-minus" style="font-size: 2rem; margin-bottom: 1rem;"></i>
                        <p>未找到符合條件的考點，請更換主題或搜尋詞。</p>
                    </div>
                `;
                return;
            }
            
            questions.forEach(q => {
                const hasAnswer = window.ANSWERS_DB && window.ANSWERS_DB[q.text];
                const hasCachedAnswer = localStorage.getItem(`ai_answer_${q.year}_${q.level}_${q.number}`);
                const localNotes = localStorage.getItem(`notes_${q.year}_${q.level}_${q.number}`) || "";
                const isSelected = activeQuestion && activeQuestion.text === q.text;
                
                const card = document.createElement("div");
                card.className = `question-card ${isSelected ? 'active' : ''}`;
                
                card.innerHTML = `
                    <div class="question-card-left">
                        <div class="question-body" title="${q.text.replace(/"/g, '&quot;')}">${q.text}</div>
                    </div>
                    <div class="question-card-right">
                        <div style="display: flex; gap: 0.4rem; align-items: center;">
                            ${hasAnswer ? '<span class="meta-tag tag-has-answer" title="包含 AI 精選模擬解析"><i class="fa-solid fa-robot"></i> 預載</span>' : ''}
                            ${hasCachedAnswer ? '<span class="meta-tag tag-has-answer" style="background: rgba(16, 185, 129, 0.1); color: var(--success-color); border: 1px solid rgba(16, 185, 129, 0.2);" title="包含已保存之 AI 解題結果"><i class="fa-solid fa-robot"></i> 自訂 AI</span>' : ''}
                            ${localNotes ? '<span class="meta-tag tag-notes" title="您已編寫了個人筆記"><i class="fa-solid fa-pen-to-square"></i> 筆記</span>' : ''}
                        </div>
                        <div style="display: flex; gap: 0.4rem; align-items: center;">
                            <span class="meta-tag tag-year">${q.year}</span>
                            <span class="meta-tag tag-level">${q.level}</span>
                            <span class="meta-tag tag-number">第 ${q.number} 題</span>
                        </div>
                    </div>
                `;
                
                card.addEventListener("click", () => {
                    // Highlight selected card
                    document.querySelectorAll(".question-card").forEach(c => c.classList.remove("active"));
                    card.classList.add("active");
                    
                    activeQuestion = q;
                    openQuestionDetails(q);
                });
                
                questionStreamEl.appendChild(card);
            });
        }"""

    new_render_questions = """        function renderQuestions() {
            questionStreamEl.innerHTML = "";
            
            // Shallow copy questions to avoid DB mutation
            let questions = [...(window.QUESTIONS_DB[currentSubject][currentTopic] || [])];
            
            // Apply search filter if present
            if (searchQuery.trim() !== "") {
                const query = searchQuery.toLowerCase();
                const matchedSet = new Set();
                questions = [];
                // If search query, search across ALL topics in the current subject
                Object.values(window.QUESTIONS_DB[currentSubject]).forEach(qList => {
                    qList.forEach(q => {
                        if (!matchedSet.has(q.id)) {
                            if (q.question.toLowerCase().includes(query) || q.year.toLowerCase().includes(query) || q.level.toLowerCase().includes(query)) {
                                matchedSet.add(q.id);
                                questions.push(q);
                            }
                        }
                    });
                });
            }

            // Apply wrong question filter
            if (showOnlyWrong) {
                const wrongIds = JSON.parse(localStorage.getItem("wrong_questions") || "[]");
                questions = questions.filter(q => wrongIds.includes(q.id));
            }
            
            // Deduplicate questions to prevent rendering identical questions (due to topic mapping overlaps)
            const uniqueQuestions = [];
            const seenIds = new Set();
            questions.forEach(q => {
                if (!seenIds.has(q.id)) {
                    seenIds.add(q.id);
                    uniqueQuestions.push(q);
                }
            });
            questions = uniqueQuestions;

            // SORT questions: Newest on Top (Descending)
            questions.sort((a, b) => getYearNumber(b.year) - getYearNumber(a.year));
            
            if (questions.length === 0) {
                questionStreamEl.innerHTML = `
                    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 200px; color: var(--text-secondary);">
                        <i class="fa-solid fa-magnifying-glass-minus" style="font-size: 2rem; margin-bottom: 1rem;"></i>
                        <p>未找到符合條件的考點，請更換主題或搜尋詞。</p>
                    </div>
                `;
                return;
            }
            
            questions.forEach(q => {
                const hasAnswer = window.ANSWERS_DB && window.ANSWERS_DB[q.id];
                const hasCachedAnswer = localStorage.getItem(`ai_answer_${q.id}`);
                const localNotes = localStorage.getItem(`notes_${q.id}`) || "";
                const isSelected = activeQuestion && activeQuestion.id === q.id;
                
                // Get answer history status for badge
                const wrongIds = JSON.parse(localStorage.getItem("wrong_questions") || "[]");
                const correctIds = JSON.parse(localStorage.getItem("correct_questions") || "[]");
                
                let answerStatusBadge = "";
                if (wrongIds.includes(q.id)) {
                    answerStatusBadge = '<span class="meta-tag tag-level" style="background: rgba(239, 68, 68, 0.12); color: var(--error-color); border: 1px solid rgba(239,68,68,0.25);" title="此題先前回答錯誤"><i class="fa-solid fa-triangle-exclamation"></i> 錯題</span>';
                } else if (correctIds.includes(q.id)) {
                    answerStatusBadge = '<span class="meta-tag tag-has-answer" style="background: rgba(16, 185, 129, 0.12); color: var(--success-color); border: 1px solid rgba(16,185,129,0.25);" title="此題先前回答正確"><i class="fa-solid fa-circle-check"></i> 答對</span>';
                }
                
                const card = document.createElement("div");
                card.className = `question-card ${isSelected ? 'active' : ''}`;
                
                card.innerHTML = `
                    <div class="question-card-left">
                        <div class="question-body" title="${q.question.replace(/"/g, '&quot;')}">${q.question}</div>
                    </div>
                    <div class="question-card-right">
                        <div style="display: flex; gap: 0.4rem; align-items: center;">
                            ${answerStatusBadge}
                            ${hasAnswer ? '<span class="meta-tag tag-has-answer" title="包含官方標準答案與解析"><i class="fa-solid fa-robot"></i> 預載</span>' : ''}
                            ${hasCachedAnswer ? '<span class="meta-tag tag-has-answer" style="background: rgba(16, 185, 129, 0.1); color: var(--success-color); border: 1px solid rgba(16, 185, 129, 0.2);" title="包含已保存之 AI 解題結果"><i class="fa-solid fa-robot"></i> 自訂 AI</span>' : ''}
                            ${localNotes ? '<span class="meta-tag tag-notes" title="包含個人研讀筆記"><i class="fa-solid fa-pen-to-square"></i> 筆記</span>' : ''}
                        </div>
                        <div style="display: flex; gap: 0.4rem; align-items: center;">
                            <span class="meta-tag tag-year">${q.year}</span>
                            <span class="meta-tag tag-level">${q.level}</span>
                            <span class="meta-tag tag-number">第 ${q.number} 題</span>
                        </div>
                    </div>
                `;
                
                card.addEventListener("click", () => {
                    document.querySelectorAll(".question-card").forEach(c => c.classList.remove("active"));
                    card.classList.add("active");
                    
                    activeQuestion = q;
                    openQuestionDetails(q);
                });
                
                questionStreamEl.appendChild(card);
            });
        }"""
    content = content.replace(old_render_questions, new_render_questions)

    # 9. 替換 openQuestionDetails 函數
    old_open_details = """        function openQuestionDetails(q) {
            // Resilient matching of preloaded answers (whitespace and punctuation agnostic)
            const findPreloadedAnswer = (text) => {
                if (!window.ANSWERS_DB) return null;
                if (window.ANSWERS_DB[text]) return window.ANSWERS_DB[text];
                const clean = s => s.replace(/[\s\p{P}]/gu, "").trim();
                const targetClean = clean(text);
                for (let key in window.ANSWERS_DB) {
                    if (clean(key) === targetClean) return window.ANSWERS_DB[key];
                }
                return null;
            };

            const answerData = findPreloadedAnswer(q.text);
            const hasAnswer = !!answerData;
            const noteKey = `notes_${q.year}_${q.level}_${q.number}`;
            const aiAnswerKey = `ai_answer_${q.year}_${q.level}_${q.number}`;
            const savedNotes = localStorage.getItem(noteKey) || "";
            const cachedAiAnswer = localStorage.getItem(aiAnswerKey) || "";
            
            // Build inner HTML for the details side panel
            detailContentEl.innerHTML = `
                <div class="detail-section" style="border-left: 4px solid var(--accent-color);">
                    <div class="section-label"><i class="fa-solid fa-file-invoice"></i> 原始申論題目</div>
                    <div class="section-body" style="font-size: 1rem; font-weight: 600; color: var(--text-primary);">${q.text}</div>
                </div>
                
                <div class="tabs">
                    <button class="tab-btn active" id="tab-btn-notes">個人筆記 & 提問</button>
                    <button class="tab-btn" id="tab-btn-answer">
                        <i class="fa-solid fa-robot"></i> 預載精華解析
                    </button>
                </div>
                
                <!-- Tab Panel 1: Notes & Live AI -->
                <div id="panel-notes" class="tab-panel">
                    <div class="detail-section">
                        <div class="section-label"><i class="fa-solid fa-pen-to-square"></i> 我的研讀筆記（自動儲存）</div>
                        <textarea class="notes-textarea" id="notes-input" placeholder="輸入此題的解題公式、關鍵詞，或您的擬答...">${savedNotes}</textarea>
                        <button class="btn-save-note" id="btn-save-note">儲存筆記</button>
                    </div>
                    
                    <!-- Live AI Solver Box -->
                    <div class="live-solver-box">
                        <div class="section-label" style="color: var(--accent-color); margin-bottom: 0.25rem;">
                            <i class="fa-solid fa-bolt"></i> 智能學習教練即時答題
                        </div>
                        <p style="font-size: 0.75rem; color: var(--text-secondary); line-height: 1.4; margin-bottom: 0.75rem;">
                            點擊下方按鈕將調用您的 API 金鑰（Gemini 模型），針對此題進行即時解題。
                        </p>
                        
                        <div style="display: flex; gap: 0.5rem; align-items: center; margin-bottom: 0.75rem;">
                            <button class="btn-solve-live" id="btn-solve-live" style="margin: 0; flex: 1;">
                                <i class="fa-solid fa-robot"></i> ${cachedAiAnswer ? '重新呼叫 Gemini AI 解題' : '呼叫 Gemini AI 即時解題'}
                            </button>
                            ${cachedAiAnswer ? `
                                <button class="btn-save-note" id="btn-clear-ai-cache" title="清除此題的 AI 快取" style="background: rgba(239,68,68,0.1); border: 1px solid rgba(239,68,68,0.2); color: #ef4444; padding: 0.55rem 0.75rem; border-radius: 0.5rem; margin: 0; cursor: pointer;">
                                    <i class="fa-solid fa-trash-can"></i>
                                </button>
                            ` : ''}
                        </div>
 
                        <div id="ai-cache-indicator" style="font-size: 0.72rem; color: var(--success-color); margin-bottom: 0.75rem; display: ${cachedAiAnswer ? 'flex' : 'none'}; align-items: center; gap: 0.35rem;">
                            <i class="fa-solid fa-circle-check"></i>
                            <span>✨ 已載入本機快取解答（生成於先前研讀，不消耗 Token）</span>
                        </div>
                        
                        <!-- Streaming Loading Indicator -->
                        <div class="api-loading-spinner" id="live-ai-loading" style="display: none;">
                            <i class="fa-solid fa-circle-notch fa-spin"></i>
                            <span>AI 思考中，即時串流回答中...</span>
                        </div>
                        
                        <!-- Streaming Output Area -->
                        <div class="live-response-container markdown-rendered" id="live-ai-response-box" style="display: ${cachedAiAnswer ? 'block' : 'none'};">
                            ${cachedAiAnswer ? `
                                <div class="ai-answer-actions" style="display: flex; justify-content: flex-end; gap: 0.5rem; margin-bottom: 0.75rem; border-bottom: 1px solid var(--card-border); padding-bottom: 0.5rem;">
                                    <button class="btn-save-note" id="btn-copy-ai-answer" style="margin: 0; padding: 0.3rem 0.6rem; font-size: 0.72rem; align-self: auto; background: transparent; border: 1px solid var(--card-border); color: var(--text-secondary); cursor: pointer;">
                                        <i class="fa-solid fa-copy" style="margin-right: 0.25rem;"></i>複製 Markdown
                                    </button>
                                    <button class="btn-save-note" id="btn-download-ai-answer" style="margin: 0; padding: 0.3rem 0.6rem; font-size: 0.72rem; align-self: auto; background: transparent; border: 1px solid var(--card-border); color: var(--text-secondary); cursor: pointer;">
                                        <i class="fa-solid fa-download" style="margin-right: 0.25rem;"></i>下載 .md 檔
                                    </button>
                                </div>
                                <div class="ai-answer-body-content">
                                    ${marked.parse(cachedAiAnswer)}
                                </div>
                            ` : ''}
                        </div>

                        <!-- AI Hallucination Warning Footer -->
                        <div id="ai-hallucination-warning" style="display: ${cachedAiAnswer ? 'flex' : 'none'}; align-items: flex-start; gap: 0.4rem; font-size: 0.7rem; color: #f43f5e; background: rgba(244, 63, 94, 0.05); padding: 0.6rem 0.75rem; border-radius: 0.35rem; border: 1px solid rgba(244, 63, 94, 0.15); margin-top: 0.75rem; line-height: 1.4;">
                            <i class="fa-solid fa-triangle-exclamation" style="margin-top: 0.1rem;"></i>
                            <span><b>免責聲明與查核提醒</b>：AI 解題（含申論擬答、學理概念及計算公式）僅供學習輔助參考。AI 可能產生幻覺或將公式數值混淆，請務必對照官方全國法規資料庫及教科書標準答案進行查核。</span>
                        </div>
                    </div>
 
                    <div class="detail-section">
                        <div class="section-label"><i class="fa-solid fa-copy"></i> 複製 AI 提問提示詞</div>
                        <div class="prompt-box">
                            <span class="prompt-preview-text">請幫我解答「${q.year}${q.level} - ${q.subject}第${q.number}題...」</span>
                            <button class="btn-copy" id="btn-copy-prompt" title="複製完整 Prompt 範本"><i class="fa-solid fa-copy"></i></button>
                        </div>
                    </div>
                </div>
                
                <!-- Tab Panel 2: Preloaded AI Answer -->
                <div id="panel-answer" class="tab-panel" style="display: none;">
                    ${hasAnswer ? `
                        <div class="detail-section">
                            <div class="section-label" style="color: #a855f7;"><i class="fa-solid fa-star"></i> 核心考點關鍵詞</div>
                            <div style="display: flex; gap: 0.4rem; flex-wrap: wrap; margin-bottom: 1rem;">
                                ${answerData.key_terms.map(t => `<span class="meta-tag" style="background: rgba(168, 85, 247, 0.1); color: #c084fc; border: 1px solid rgba(168, 85, 247, 0.2);">${t}</span>`).join('')}
                            </div>
                            <div class="section-label" style="color: #6366f1;"><i class="fa-solid fa-circle-check"></i> 滿分模擬解答卡片</div>
                            <div class="section-body markdown-rendered" id="ai-answer-body"></div>
                        </div>
                    ` : `
                        <div style="color: var(--text-secondary); text-align: center; padding: 2.5rem 1.5rem; display: flex; flex-direction: column; align-items: center; gap: 0.75rem;">
                            <i class="fa-solid fa-robot" style="font-size: 2.5rem; background: var(--accent-gradient); -webkit-background-clip: text; -webkit-text-fill-color: transparent; opacity: 0.8; margin-bottom: 0.5rem;"></i>
                            <h4 style="color: var(--text-primary); margin: 0; font-size: 0.95rem;">本題尚無預載精華解析</h4>
                            <p style="font-size: 0.8rem; line-height: 1.5; margin: 0; max-width: 320px; margin-left: auto; margin-right: auto;">您可以點選左側「<b>個人筆記 & 提問</b>」分頁，利用您的 Gemini API 金鑰進行即時解題，系統將自動為您生成並保存詳盡解析！</p>
                        </div>
                    `}
                </div>
            `;
            
            // Render Preloaded AI Markdown Answer
            if (hasAnswer) {
                const answerBody = document.getElementById("ai-answer-body");
                if (answerBody) {
                    answerBody.innerHTML = marked.parse(answerData.model_answer);
                }
            }
            
            // Tab Toggle Listeners
            const btnNotes = document.getElementById("tab-btn-notes");
            const btnAnswer = document.getElementById("tab-btn-answer");
            const panelNotes = document.getElementById("panel-notes");
            const panelAnswer = document.getElementById("panel-answer");
            
            btnNotes.addEventListener("click", () => {
                btnNotes.classList.add("active");
                btnAnswer.classList.remove("active");
                panelNotes.style.display = "flex";
                panelAnswer.style.display = "none";
            });
            
            btnAnswer.addEventListener("click", () => {
                btnAnswer.classList.add("active");
                btnNotes.classList.remove("active");
                panelAnswer.style.display = "flex";
                panelNotes.style.display = "none";
            });
            
            // Notes Save Function
            const notesInput = document.getElementById("notes-input");
            const btnSave = document.getElementById("btn-save-note");
            btnSave.addEventListener("click", () => {
                localStorage.setItem(noteKey, notesInput.value);
                btnSave.innerText = "已儲存！";
                btnSave.style.background = "var(--success-color)";
                setTimeout(() => {
                    btnSave.innerText = "儲存筆記";
                    btnSave.style.background = "var(--accent-gradient)";
                    renderQuestions(); // Update the main list badge for "Has Notes"
                }, 1000);
            });
            
            // Prompt Copy Function
            const btnCopy = document.getElementById("btn-copy-prompt");
            btnCopy.addEventListener("click", () => {
                const promptText = `
你是一位食品衛生檢驗領域的國家考試專家。請為我解答以下這道國家考試題目，並提供：
1. 核心考點與學術概念解析。
2. 結構化的精準滿分擬答（包含大項與標題，字數約 800 - 1000 字）。
3. 延伸常考的關聯知識與易錯陷阱。

【考題資訊】
年度與考試：${q.year} ${q.level}
考科科目：${q.subject}
題目內容：
${q.text}
`;
                navigator.clipboard.writeText(promptText.trim()).then(() => {
                    const icon = btnCopy.querySelector("i");
                    icon.className = "fa-solid fa-check";
                    btnCopy.style.color = "var(--success-color)";
                    setTimeout(() => {
                        icon.className = "fa-solid fa-copy";
                        btnCopy.style.color = "var(--accent-color)";
                    }, 1500);
                });
            });
 
            // AI Answer Actions (Copy & Download)
            if (cachedAiAnswer) {
                const btnCopyAi = document.getElementById("btn-copy-ai-answer");
                const btnDownloadAi = document.getElementById("btn-download-ai-answer");
                
                if (btnCopyAi) {
                    btnCopyAi.addEventListener("click", () => {
                        navigator.clipboard.writeText(cachedAiAnswer).then(() => {
                            const icon = btnCopyAi.querySelector("i");
                            icon.className = "fa-solid fa-check";
                            btnCopyAi.innerText = "已複製！";
                            btnCopyAi.style.color = "var(--success-color)";
                            setTimeout(() => {
                                btnCopyAi.innerHTML = `<i class="fa-solid fa-copy" style="margin-right: 0.25rem;"></i>複製 Markdown`;
                                btnCopyAi.style.color = "";
                            }, 1500);
                        });
                    });
                }
                
                if (btnDownloadAi) {
                    btnDownloadAi.addEventListener("click", () => {
                        try {
                            const blob = new Blob([cachedAiAnswer], { type: "text/markdown;charset=utf-8" });
                            const url = URL.createObjectURL(blob);
                            const a = document.createElement("a");
                            a.href = url;
                            a.download = `${q.year}_${q.level}_${q.subject}_第${q.number}題_AI解答.md`;
                            document.body.appendChild(a);
                            a.click();
                            document.body.removeChild(a);
                            URL.revokeObjectURL(url);
                        } catch (err) {
                            alert("下載 AI 解答失敗：" + err.message);
                        }
                    });
                }
            }

            // Live AI Stream Solver Button
            const btnSolveLive = document.getElementById("btn-solve-live");
            const liveAiLoading = document.getElementById("live-ai-loading");
            const liveAiResponseBox = document.getElementById("live-ai-response-box");
            const cacheIndicator = document.getElementById("ai-cache-indicator");
            const btnClearAiCache = document.getElementById("btn-clear-ai-cache");

            if (btnClearAiCache) {
                btnClearAiCache.addEventListener("click", () => {
                    if (confirm("是否確定刪除此題的 AI 快取解答？此操作不可復原。")) {
                        localStorage.removeItem(aiAnswerKey);
                        alert("快取已清除！");
                        openQuestionDetails(q); // reload details
                        renderQuestions(); // reload question stream to update badges
                    }
                });
            }

            btnSolveLive.addEventListener("click", () => {
                const apiKey = localStorage.getItem("gemini_api_key");
                const model = localStorage.getItem("gemini_model") || "gemini-2.5-pro";

                if (!apiKey) {
                    alert("請先在設定視窗中輸入並儲存您的 Gemini API 金鑰！");
                    return;
                }

                liveAiLoading.style.display = "flex";
                liveAiResponseBox.style.display = "block";
                const warningBox = document.getElementById("ai-hallucination-warning");
                if (warningBox) warningBox.style.display = "flex";
                if (cacheIndicator) cacheIndicator.style.display = "none";
                liveAiResponseBox.innerHTML = "<p style='color: var(--text-secondary);'>正在建立連線...</p>";

                callGeminiAPIStream(apiKey, model, q, (text, isFinished, error) => {
                    if (error) {
                        liveAiLoading.style.display = "none";
                        liveAiResponseBox.innerHTML = `<p style="color: var(--error-color);"><i class="fa-solid fa-triangle-exclamation"></i> 錯誤: ${error}</p>`;
                        return;
                    }

                    // Render markdown on the fly
                    liveAiResponseBox.innerHTML = marked.parse(text);

                    if (isFinished) {
                        liveAiLoading.style.display = "none";
                        localStorage.setItem(aiAnswerKey, text);
                        
                        // Show cache indicator
                        if (cacheIndicator) {
                            cacheIndicator.style.display = "flex";
                            cacheIndicator.querySelector("span").innerText = "✨ 解答已自動保存至本機（下次開啟不消耗 Token）";
                        }
                        
                        // Update lists to show badge
                        renderQuestions();
                        
                        // We also add the delete button if not exists
                        if (!btnClearAiCache) {
                            openQuestionDetails(q); // simply reload details to render correct DOM state with delete button
                        }
                    }
                });
            });
            
            // Show Panel Details
            detailPlaceholderEl.style.display = "none";
            detailActiveContainer.style.display = "flex";
            detailPanelEl.classList.add("open");
            document.querySelector(".workspace-layout").classList.add("detail-open");
        }"""

    new_open_details = """        function openQuestionDetails(q) {
            const correctAnswer = (window.ANSWERS_DB && window.ANSWERS_DB[q.id]) || "";
            const noteKey = `notes_${q.id}`;
            const aiAnswerKey = `ai_answer_${q.id}`;
            const savedNotes = localStorage.getItem(noteKey) || "";
            const cachedAiAnswer = localStorage.getItem(aiAnswerKey) || "";
            
            // Build options buttons HTML
            let optionsHtml = "";
            Object.keys(q.options).forEach(key => {
                optionsHtml += `
                    <button class="option-btn" data-option="${key}">
                        <span class="option-letter">${key}</span>
                        <span class="option-text">${q.options[key]}</span>
                    </button>
                `;
            });

            // Build inner HTML for the details side panel
            detailContentEl.innerHTML = `
                <div class="detail-section" style="border-left: 4px solid var(--accent-color); margin-bottom: 1rem;">
                    <div class="section-label"><i class="fa-solid fa-file-invoice"></i> 考題正文 (${q.level})</div>
                    <div class="section-body" style="font-size: 1rem; font-weight: 600; color: var(--text-primary); margin-bottom: 0.5rem;">${q.question}</div>
                    
                    <div class="options-container" id="details-options-container">
                        ${optionsHtml}
                    </div>
                    
                    <div id="details-answer-feedback" class="answer-feedback-box" style="display: none;"></div>
                </div>
                
                <div class="tabs">
                    <button class="tab-btn active" id="tab-btn-notes">個人筆記 & AI 解題</button>
                    <button class="tab-btn" id="tab-btn-prompt">
                        <i class="fa-solid fa-robot"></i> 提示詞與中繼資料
                    </button>
                </div>
                
                <!-- Tab Panel 1: Notes & Live AI -->
                <div id="panel-notes" class="tab-panel">
                    <div class="detail-section">
                        <div class="section-label"><i class="fa-solid fa-pen-to-square"></i> 個人研讀筆記（自動儲存）</div>
                        <textarea class="notes-textarea" id="notes-input" placeholder="輸入此題的解題重點、關鍵詞或擬答...">${savedNotes}</textarea>
                        <button class="btn-save-note" id="btn-save-note">儲存筆記</button>
                    </div>
                    
                    <!-- Live AI Solver Box -->
                    <div class="live-solver-box">
                        <div class="section-label" style="color: var(--accent-color); margin-bottom: 0.25rem;">
                            <i class="fa-solid fa-bolt"></i> 智能學習教練即時分析
                        </div>
                        <p style="font-size: 0.75rem; color: var(--text-secondary); line-height: 1.4; margin-bottom: 0.75rem;">
                            呼叫大語言模型 (Gemini-2.5-Flash) 針對此題進行實時解題。
                        </p>
                        
                        <div style="display: flex; gap: 0.5rem; align-items: center; margin-bottom: 0.75rem;">
                            <button class="btn-solve-live" id="btn-solve-live" style="margin: 0; flex: 1;">
                                <i class="fa-solid fa-robot"></i> ${cachedAiAnswer ? '重新呼叫 Gemini AI 解題' : '呼叫 Gemini AI 即時解題'}
                            </button>
                            ${cachedAiAnswer ? `
                                <button class="btn-save-note" id="btn-clear-ai-cache" title="清除此題的 AI 快取" style="background: rgba(239,68,68,0.1); border: 1px solid rgba(239,68,68,0.2); color: #ef4444; padding: 0.55rem 0.75rem; border-radius: 0.5rem; margin: 0; cursor: pointer;">
                                    <i class="fa-solid fa-trash-can"></i>
                                </button>
                            ` : ''}
                        </div>
 
                        <div id="ai-cache-indicator" style="font-size: 0.72rem; color: var(--success-color); margin-bottom: 0.75rem; display: ${cachedAiAnswer ? 'flex' : 'none'}; align-items: center; gap: 0.35rem;">
                            <i class="fa-solid fa-circle-check"></i>
                            <span>✨ 已載入本機快取解答（生成於先前研讀，不消耗 Token）</span>
                        </div>
                        
                        <!-- Streaming Loading Indicator -->
                        <div class="api-loading-spinner" id="live-ai-loading" style="display: none;">
                            <i class="fa-solid fa-circle-notch fa-spin"></i>
                            <span>AI 思考中，即時串流回答中...</span>
                        </div>
                        
                        <!-- Streaming Output Area -->
                        <div class="live-response-container markdown-rendered" id="live-ai-response-box" style="display: ${cachedAiAnswer ? 'block' : 'none'};">
                            ${cachedAiAnswer ? `
                                <div class="ai-answer-actions" style="display: flex; justify-content: flex-end; gap: 0.5rem; margin-bottom: 0.75rem; border-bottom: 1px solid var(--card-border); padding-bottom: 0.5rem;">
                                    <button class="btn-save-note" id="btn-copy-ai-answer" style="margin: 0; padding: 0.3rem 0.6rem; font-size: 0.72rem; align-self: auto; background: transparent; border: 1px solid var(--card-border); color: var(--text-secondary); cursor: pointer;">
                                        <i class="fa-solid fa-copy" style="margin-right: 0.25rem;"></i>複製 Markdown
                                    </button>
                                    <button class="btn-save-note" id="btn-download-ai-answer" style="margin: 0; padding: 0.3rem 0.6rem; font-size: 0.72rem; align-self: auto; background: transparent; border: 1px solid var(--card-border); color: var(--text-secondary); cursor: pointer;">
                                        <i class="fa-solid fa-download" style="margin-right: 0.25rem;"></i>下載 .md 檔
                                    </button>
                                </div>
                                <div class="ai-answer-body-content">
                                    ${marked.parse(cachedAiAnswer)}
                                </div>
                            ` : ''}
                        </div>

                        <!-- AI Hallucination Warning Footer -->
                        <div id="ai-hallucination-warning" style="display: ${cachedAiAnswer ? 'flex' : 'none'}; align-items: flex-start; gap: 0.4rem; font-size: 0.7rem; color: #f43f5e; background: rgba(244, 63, 94, 0.05); padding: 0.6rem 0.75rem; border-radius: 0.35rem; border: 1px solid rgba(244, 63, 94, 0.15); margin-top: 0.75rem; line-height: 1.4;">
                            <i class="fa-solid fa-triangle-exclamation" style="margin-top: 0.1rem;"></i>
                            <span><b>免責聲明與查核提醒</b>：AI 解題（含學理概念及計算公式）僅供學習輔助參考。AI 可能產生錯誤或將公式混淆，請對照標準教科書進行查核。</span>
                        </div>
                    </div>
                </div>
                
                <!-- Tab Panel 2: Prompts & Meta -->
                <div id="panel-prompt" class="tab-panel" style="display: none;">
                    <div class="detail-section">
                        <div class="section-label" style="color: #a855f7;"><i class="fa-solid fa-star"></i> 題目中繼資料</div>
                        <div style="display: flex; gap: 0.4rem; flex-wrap: wrap; margin-bottom: 1rem;">
                            <span class="meta-tag" style="background: rgba(168, 85, 247, 0.1); color: #c084fc; border: 1px solid rgba(168, 85, 247, 0.2);">年份: ${q.year}</span>
                            <span class="meta-tag" style="background: rgba(168, 85, 247, 0.1); color: #c084fc; border: 1px solid rgba(168, 85, 247, 0.2);">科目: ${q.subject}</span>
                            <span class="meta-tag" style="background: rgba(168, 85, 247, 0.1); color: #c084fc; border: 1px solid rgba(168, 85, 247, 0.2);">題號: 第 ${q.number} 題</span>
                            ${q.tags.map(t => `<span class="meta-tag" style="background: rgba(99, 102, 241, 0.1); color: #818cf8; border: 1px solid rgba(99, 102, 241, 0.2);">${t}</span>`).join('')}
                        </div>
                        <div class="section-label"><i class="fa-solid fa-copy"></i> 複製外部 AI 提問提示詞</div>
                        <div class="prompt-box">
                            <span class="prompt-preview-text">請解答護理師國考 ${q.year} ${q.level} ${q.subject} 第 ${q.number} 題...</span>
                            <button class="btn-copy" id="btn-copy-prompt" title="複製完整 Prompt 範本"><i class="fa-solid fa-copy"></i></button>
                        </div>
                    </div>
                </div>
            `;

            // Setup Options Click Interactivity
            const optButtons = detailContentEl.querySelectorAll(".option-btn");
            const feedbackBox = document.getElementById("details-answer-feedback");

            optButtons.forEach(btn => {
                btn.addEventListener("click", () => {
                    const selectedOpt = btn.getAttribute("data-option");
                    
                    // Correct answer matching logic (support single, multiple like 'B,D', and all correct '*')
                    let isCorrect = false;
                    const answersArray = correctAnswer.split(",").map(a => a.trim());
                    
                    if (correctAnswer === "*") {
                        isCorrect = true;
                    } else if (answersArray.includes(selectedOpt)) {
                        isCorrect = true;
                    }

                    // Disable all buttons and show colors
                    optButtons.forEach(b => {
                        b.classList.add("disabled");
                        const optVal = b.getAttribute("data-option");
                        if (correctAnswer === "*") {
                            b.classList.add("success");
                        } else if (answersArray.includes(optVal)) {
                            b.classList.add("success");
                        } else if (optVal === selectedOpt && !isCorrect) {
                            b.classList.add("error");
                        }
                    });

                    // Update LocalStorage statistics
                    let wrongQuestions = JSON.parse(localStorage.getItem("wrong_questions") || "[]");
                    let correctQuestions = JSON.parse(localStorage.getItem("correct_questions") || "[]");

                    if (isCorrect) {
                        // Mark as correct, remove from wrong list
                        if (!correctQuestions.includes(q.id)) correctQuestions.push(q.id);
                        wrongQuestions = wrongQuestions.filter(id => id !== q.id);
                        
                        feedbackBox.className = "answer-feedback-box success";
                        feedbackBox.innerHTML = `
                            <div class="answer-feedback-title">
                                <i class="fa-solid fa-circle-check"></i> 答對了！
                            </div>
                            <div>標準答案為 <b>${correctAnswer === "*" ? "一律給分" : correctAnswer}</b>。回答正確。</div>
                        `;
                    } else {
                        // Mark as wrong, remove from correct list
                        if (!wrongQuestions.includes(q.id)) wrongQuestions.push(q.id);
                        correctQuestions = correctQuestions.filter(id => id !== q.id);

                        feedbackBox.className = "answer-feedback-box error";
                        feedbackBox.innerHTML = `
                            <div class="answer-feedback-title">
                                <i class="fa-solid fa-circle-xmark"></i> 答錯了！
                            </div>
                            <div>此題答案為 <b>${correctAnswer}</b>，選擇了 <b>${selectedOpt}</b>。</div>
                        `;
                    }

                    localStorage.setItem("wrong_questions", JSON.stringify(wrongQuestions));
                    localStorage.setItem("correct_questions", JSON.stringify(correctQuestions));
                    feedbackBox.style.display = "flex";

                    // Instantly refresh UI statistics
                    renderStatsDashboard();
                    renderQuestions();
                });
            });
            
            // Tab Toggle Listeners
            const btnNotes = document.getElementById("tab-btn-notes");
            const btnPrompt = document.getElementById("tab-btn-prompt");
            const panelNotes = document.getElementById("panel-notes");
            const panelPrompt = document.getElementById("panel-prompt");
            
            btnNotes.addEventListener("click", () => {
                btnNotes.classList.add("active");
                btnPrompt.classList.remove("active");
                panelNotes.style.display = "block";
                panelPrompt.style.display = "none";
            });
            
            btnPrompt.addEventListener("click", () => {
                btnPrompt.classList.add("active");
                btnNotes.classList.remove("active");
                panelPrompt.style.display = "block";
                panelNotes.style.display = "none";
            });
            
            // Notes Save Function
            const notesInput = document.getElementById("notes-input");
            const btnSave = document.getElementById("btn-save-note");
            btnSave.addEventListener("click", () => {
                localStorage.setItem(noteKey, notesInput.value);
                btnSave.innerText = "已儲存！";
                btnSave.style.background = "var(--success-color)";
                setTimeout(() => {
                    btnSave.innerText = "儲存筆記";
                    btnSave.style.background = "var(--accent-gradient)";
                    renderQuestions(); // Update the main list badge for "Has Notes"
                }, 1000);
            });
            
            // Prompt Copy Function
            const btnCopy = document.getElementById("btn-copy-prompt");
            btnCopy.addEventListener("click", () => {
                let optionsText = "";
                Object.keys(q.options).forEach(k => {
                    optionsText += `(${k}) ${q.options[k]}\n`;
                });

                const promptText = `
此模型為「${q.subject}」領域專技高考與歷屆甄選之解題專家。請針對以下這道選擇題，提供客觀、條理清晰且切合考點的解答。
要求如下，並請以 Markdown 格式撰寫，字數約 600 - 800 字：
1. 【考點剖析】說明此題的核心學理與病生理機轉。
2. 【選項解析】詳細論述為何正確答案為 (${correctAnswer})，並逐一說明其他干擾選項為何錯誤。
3. 【關聯知識點】歸納此主題常考的衍生重點、核心機轉與臨床照顧易錯陷阱。

【考題資訊】
年度與考試：${q.year} ${q.level}
考科科目：${q.subject}
題目內容：
${q.question}
選項：
${optionsText}
正確答案：${correctAnswer}
`;
                navigator.clipboard.writeText(promptText.trim()).then(() => {
                    const icon = btnCopy.querySelector("i");
                    icon.className = "fa-solid fa-check";
                    btnCopy.style.color = "var(--success-color)";
                    setTimeout(() => {
                        icon.className = "fa-solid fa-copy";
                        btnCopy.style.color = "var(--accent-color)";
                    }, 1500);
                });
            });
 
            // AI Answer Actions (Copy & Download)
            if (cachedAiAnswer) {
                const btnCopyAi = document.getElementById("btn-copy-ai-answer");
                const btnDownloadAi = document.getElementById("btn-download-ai-answer");
                
                if (btnCopyAi) {
                    btnCopyAi.addEventListener("click", () => {
                        navigator.clipboard.writeText(cachedAiAnswer).then(() => {
                            const icon = btnCopyAi.querySelector("i");
                            icon.className = "fa-solid fa-check";
                            btnCopyAi.innerText = "已複製！";
                            btnCopyAi.style.color = "var(--success-color)";
                            setTimeout(() => {
                                btnCopyAi.innerHTML = `<i class="fa-solid fa-copy" style="margin-right: 0.25rem;"></i>複製 Markdown`;
                                btnCopyAi.style.color = "";
                            }, 1500);
                        });
                    });
                }
                
                if (btnDownloadAi) {
                    btnDownloadAi.addEventListener("click", () => {
                        try {
                            const blob = new Blob([cachedAiAnswer], { type: "text/markdown;charset=utf-8" });
                            const url = URL.createObjectURL(blob);
                            const a = document.createElement("a");
                            a.href = url;
                            a.download = `${q.year}_${q.level}_${q.subject}_第${q.number}題_AI解答.md`;
                            document.body.appendChild(a);
                            a.click();
                            document.body.removeChild(a);
                            URL.revokeObjectURL(url);
                        } catch (err) {
                            alert("下載 AI 解答失敗：" + err.message);
                        }
                    });
                }
            }

            // Live AI Stream Solver Button
            const btnSolveLive = document.getElementById("btn-solve-live");
            const liveAiLoading = document.getElementById("live-ai-loading");
            const liveAiResponseBox = document.getElementById("live-ai-response-box");
            const cacheIndicator = document.getElementById("ai-cache-indicator");
            const btnClearAiCache = document.getElementById("btn-clear-ai-cache");

            if (btnClearAiCache) {
                btnClearAiCache.addEventListener("click", () => {
                    if (confirm("是否確定刪除此題的 AI 快取解答？此操作不可復原。")) {
                        localStorage.removeItem(aiAnswerKey);
                        alert("快取已清除！");
                        openQuestionDetails(q); // reload details
                        renderQuestions(); // reload question stream to update badges
                    }
                });
            }

            btnSolveLive.addEventListener("click", () => {
                const apiKey = localStorage.getItem("gemini_api_key");
                const model = localStorage.getItem("gemini_model") || "gemini-2.5-flash";

                if (!apiKey) {
                    alert("請先在設定視窗中輸入並儲存您的 Gemini API 金鑰！");
                    return;
                }

                liveAiLoading.style.display = "flex";
                liveAiResponseBox.style.display = "block";
                const warningBox = document.getElementById("ai-hallucination-warning");
                if (warningBox) warningBox.style.display = "flex";
                if (cacheIndicator) cacheIndicator.style.display = "none";
                liveAiResponseBox.innerHTML = "<p style='color: var(--text-secondary);'>正在建立連線...</p>";

                callGeminiAPIStream(apiKey, model, q, (text, isFinished, error) => {
                    if (error) {
                        liveAiLoading.style.display = "none";
                        liveAiResponseBox.innerHTML = `<p style="color: var(--error-color);"><i class="fa-solid fa-triangle-exclamation"></i> 錯誤: ${error}</p>`;
                        return;
                    }

                    // Render markdown on the fly
                    liveAiResponseBox.innerHTML = marked.parse(text);

                    if (isFinished) {
                        liveAiLoading.style.display = "none";
                        localStorage.setItem(aiAnswerKey, text);
                        
                        // Show cache indicator
                        if (cacheIndicator) {
                            cacheIndicator.style.display = "flex";
                            cacheIndicator.querySelector("span").innerText = "✨ 解答已自動保存至本機（下次開啟不消耗 Token）";
                        }
                        
                        // Update lists to show badge
                        renderQuestions();
                        
                        // We also add the delete button if not exists
                        if (!btnClearAiCache) {
                            openQuestionDetails(q); // simply reload details to render correct DOM state with delete button
                        }
                    }
                });
            });
            
            // Show Panel Details
            detailPlaceholderEl.style.display = "none";
            detailActiveContainer.style.display = "flex";
            detailPanelEl.classList.add("open");
            document.querySelector(".workspace-layout").classList.add("detail-open");
        }"""
    content = content.replace(old_open_details, new_open_details)

    # 10. 替換 callGeminiAPIStream Prompt 為第三人稱且為護理師選擇題
    old_api_stream = """        async function callGeminiAPIStream(apiKey, model, q, callback) {
            const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:streamGenerateContent?key=${apiKey}`;
            const promptText = `
你是一位食品衛生檢驗國考評分官與輔導教練。請針對以下考題，提供一份可信度高、條理清晰且切合考點的解答：
1. 【考點分析】歸納本題的核心化學/微生物學理。
2. 【法規依據與公式】若涉及食品衛生法規或公式（如D值、z值計算），請列出具體條文名稱與計算式。
3. 【申論擬答卡】字數約800字，大項層次分明（一、(一)、1.），模擬考生最佳作答格式。
4. 【易錯避坑點】警告考生最常寫錯的關鍵語詞或名詞混淆。

【考題內容】
年度：${q.year}
等級：${q.level}
考科：${q.subject}
題號：第${q.number}題
題目：
${q.text}
`;"""

    new_api_stream = """        async function callGeminiAPIStream(apiKey, model, q, callback) {
            const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:streamGenerateContent?key=${apiKey}`;
            
            let optionsText = "";
            Object.keys(q.options).forEach(k => {
                optionsText += `(${k}) ${q.options[k]}\\n`;
            });
            const correctAnswer = (window.ANSWERS_DB && window.ANSWERS_DB[q.id]) || "未知";

            const promptText = `
此模型為「${q.subject}」領域專技高考與歷屆甄選之解題專家。請針對以下選擇題，提供一份可信度高、條理清晰且切合考點的詳細分析與解答。
要求如下，並請以 Markdown 格式撰寫，字數約 600 - 800 字：
1. 【考點剖析】說明此題的核心學理與病生理機轉。
2. 【選項解析】詳細論述為何正確答案為 (${correctAnswer})，並逐一說明其他干擾選項為何錯誤。
3. 【關聯知識點】歸納此主題常考的衍生重點、核心機轉與臨床照顧易錯陷阱。

【考題資訊】
年度與考試：${q.year} ${q.level}
考科科目：${q.subject}
題目內容：
${q.question}
選項：
${optionsText}
正確答案：${correctAnswer}
`;"""
    content = content.replace(old_api_stream, new_api_stream)

    # 11. 替換 callGeminiCardGenerationStream 裡的 Prompt
    old_card_gen = """        // Dynamic streaming generator helper for Study Cards
        async function callGeminiCardGenerationStream(apiKey, model, subject, topic, callback) {
            const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:streamGenerateContent?key=${apiKey}`;
            const promptText = `
你是一位「${subject}」領域國家考試的頂尖指導教授與解題教練。請針對學習主題「${topic}」，為我精心撰寫一份巨觀的國考主題複習卡。
要求內容如下，並請以 Markdown 格式撰寫，字數約 800 - 1200 字：

1. 【主題概述與命題頻率分析】說明此主題在國考中的定位與核心命題趨勢。
2. 【核心學理機制與關鍵字】詳細說明此主題的核心機制、反應方程式、或核心法規架構，並使用表格進行對比。
3. 【核心公式與計算推導】（若為食品化學/微生物殺菌/生物統計學，請務必詳細列出數學公式或生化反應式；若為法規，請列出核心條文名稱與條款重點）。
4. 【答題寫作套路框架】提供考生如果在申論題遇到此主題題目時，可以直接採用的「滿分答題三段式架構（前言、主體論述、結論）」。
5. 【高難度考點陷阱與易錯辨析】列出考生最常寫錯或混淆的概念對照。
`;"""

    new_card_gen = """        // Dynamic streaming generator helper for Study Cards
        async function callGeminiCardGenerationStream(apiKey, model, subject, topic, callback) {
            const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:streamGenerateContent?key=${apiKey}`;
            const promptText = `
此模型為「${subject}」領域專技高考與歷屆甄選之頂尖指導教授與解題教練。請針對學習主題「${topic}」，精心撰寫一份客觀的護理師考試主題複習卡。
要求內容如下，並請以 Markdown 格式撰寫，字數約 800 - 1200 字：

1. 【主題概述與命題頻率分析】說明此主題在國考中的定位與核心命題趨勢。
2. 【核心學理機制與關鍵字】詳細說明此主題的核心病生理機制、解剖生理、或臨床護理照護重點，並使用表格進行對比。
3. 【核心護理措施與照護標準】詳細列出此主題的臨床照護要點、觀察指標、評估工具或照護措施重點。
4. 【選擇題速記要訣與關鍵口訣】提供考生快速記憶的口訣或核心概念速記。
5. 【高難度考點陷阱與易錯辨析】列出考生最常混淆或答錯的概念對照。
`;"""
    content = content.replace(old_card_gen, new_card_gen)

    # 12. 清理其他殘留的人稱代名詞
    # 替換關於備份說明的那句
    content = content.replace("將您所有的個人學習數據", "將所有個人學習數據")
    content = content.replace("我的研讀筆記", "個人研讀筆記")
    content = content.replace("還原您的所有學習數據", "還原所有學習數據")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print("Success: study_portal.html has been updated successfully.")

if __name__ == "__main__":
    main()
