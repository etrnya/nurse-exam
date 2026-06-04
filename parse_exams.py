import os
import re
import json
import sys
import pypdf
import pdfplumber

# 強制 stdout 使用 UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# 專案術語對齊：此腳本負責提取試題與答案 PDF，進行標籤分類貼標，並生成 questions_db.js 與 answers_db.js

MOEX_DIR = "downloads/moex"
TAINAN_DIR = "downloads/tainan"
OUTPUT_QUESTIONS_JS = "questions_db.js"
OUTPUT_ANSWERS_JS = "answers_db.js"

# 5 大考科代碼與中文名稱映射
SUBJECT_NAME_MAP = {
    "basic-med": "基礎醫學",
    "basic-nursing": "基本護理學與護理行政",
    "med-surg": "內外科護理學",
    "obs-ped": "產兒科護理學",
    "psych-community": "精神科與社區衛生護理學"
}

# 標籤關鍵字字典，用於本地自動貼標
TAGS_KEYWORDS = {
    "解剖學": ["解剖", "骨骼", "肌肉", "關節", "血管", "神經", "心臟", "肺臟", "腎臟", "大腦", "小腦", "組織學", "韌帶", "軟骨", "上皮", "動脈", "靜脈"],
    "生理學": ["生理", "膜電位", "受體", "激素", "內分泌", "傳導", "收縮", "代謝", "反射", "呼吸", "消化", "排泄", "過濾", "重吸收"],
    "病理學": ["病理", "腫瘤", "癌症", "壞死", "纖維化", "栓塞", "梗塞", "發炎", "病變", "水腫", "萎縮", "增生", "轉移"],
    "藥理學": ["藥理", "藥物", "副作用", "拮抗", "抗生素", "機轉", "適應症", "給藥", "劑量", "半衰期", "交互作用", "學名"],
    "微生物學與免疫學": ["微生物", "免疫", "抗體", "抗原", "病毒", "細菌", "感染", "真菌", "寄生蟲", "疫苗", "補體", "淋巴球", "過敏"],
    "基本護理學": ["無菌", "洗手", "鋪床", "灌腸", "導尿", "給藥", "注射", "繃帶", "冷療", "熱療", "沐浴", "舒適", "姿勢", "擺位", "生命徵象", "評估", "護理過程", "護理記錄", "出院準備"],
    "護理行政": ["行政", "預算", "排班", "領導", "規劃", "控制", "組織", "衝突", "品管", "品質管理", "零基預算", "護理人力", "督導"],
    "內外科護理學": ["心肌梗塞", "高血壓", "糖尿病", "中風", "骨折", "手術", "休克", "氣喘", "心衰竭", "慢性腎病", "透析", "洗腎", "肝硬化", "肺炎", "癌症護理", "酸鹼平衡", "電解質"],
    "產兒科護理學": ["妊娠", "分娩", "產後", "新生兒", "兒科", "小兒", "母乳", "哺乳", "孕婦", "產道", "產前", "胎兒", "小兒發育", "預防接種"],
    "精神科與社區衛生護理學": ["精神病", "憂鬱", "精神分裂", "思覺失調", "幻覺", "妄想", "社區衛生", "傳染病防治", "十大死因", "篩檢", "敏感度", "特異度", "流行病學", "死亡率", "出生率", "家訪", "衛生教育", "健康促進"]
}

def parse_remarks_for_rules(text):
    """解析答案 PDF 備註中的給分更正規則"""
    corrections = {}
    # 匹配「一律給分」或「其餘均給分」
    for m in re.finditer(r"第\s*(\d+)\s*題[^，。]*?(?:一律給分|其餘均給分)", text):
        q_num = int(m.group(1))
        corrections[q_num] = "*"
        
    # 匹配「答Ｘ或Ｙ者均給分」或「答Ｘ、Ｙ或Ｚ者均給分」或「答Ｘ給分」等
    for m in re.finditer(r"第\s*(\d+)\s*題答\s*([A-ZＢ-ＤＡ-Ｄ\s、或]+)\s*(?:者均)?給分", text):
        q_num = int(m.group(1))
        ans_part = m.group(2)
        ans_part = ans_part.translate(str.maketrans("ＡＢＣＤ", "ABCD"))
        letters = re.findall(r"[A-D]", ans_part)
        if letters:
            corrections[q_num] = ",".join(sorted(list(set(letters))))
            
    return corrections

def get_pdf_session(pdf_path):
    """取得 PDF 考科之考試期別 (如：第一次、第二次、第三次)"""
    try:
        reader = pypdf.PdfReader(pdf_path)
        if not reader.pages:
            return None
        text = reader.pages[0].extract_text()
        if text:
            match = re.search(r"第[一二三四五六七八九十]次", text)
            if match:
                return match.group(0)
    except Exception as e:
        print(f"讀取 PDF 期別出錯: {pdf_path} -> {e}")
    return None

def extract_moex_answers(year, subject_code):
    """解析考選部答案 PDF (優先採用同考期 corrected，若無或不同期才採用 answer)"""
    answer_file = f"moex-{year}-{subject_code}-answer.pdf"
    corrected_file = f"moex-{year}-{subject_code}-corrected.pdf"
    
    answer_path = os.path.join(MOEX_DIR, answer_file)
    corrected_path = os.path.join(MOEX_DIR, corrected_file)
    
    target_path = answer_path
    
    if os.path.exists(corrected_path) and os.path.exists(answer_path):
        ans_session = get_pdf_session(answer_path)
        corr_session = get_pdf_session(corrected_path)
        if ans_session and corr_session and ans_session == corr_session:
            target_path = corrected_path
        else:
            target_path = answer_path
    elif os.path.exists(corrected_path):
        target_path = corrected_path
        
    if not os.path.exists(target_path):
        return {}
        
    answers = {}
    remarks_text = ""
    
    try:
        # 1. 使用 pdfplumber 提取表格
        with pdfplumber.open(target_path) as pdf:
            for page in pdf.pages:
                # 提取備註文字
                page_text = page.extract_text()
                if page_text and "備註" in page_text:
                    remarks_text += page_text
                
                tables = page.extract_tables()
                for table in tables:
                    if len(table) < 2:
                        continue
                    # 表格第 1 行为题号，第 2 行为答案
                    headers = table[0]
                    values = table[1]
                    for h, v in zip(headers, values):
                        if not h or not v:
                            continue
                        clean_h = clean_text(str(h))
                        clean_v = clean_text(str(v))
                        # 轉換全形字元為半形
                        clean_v = clean_v.translate(str.maketrans("ＡＢＣＤ", "ABCD"))
                        
                        # 匹配「第X題」或直接是數字
                        q_match = re.search(r"第?\s*(\d+)\s*題?", clean_h)
                        if q_match:
                            q_num = int(q_match.group(1))
                            if clean_v in ["A", "B", "C", "D", "#", "*"]:
                                answers[q_num] = clean_v
                                
        # 2. 解析備註更正規則，替換其中的 # 答案
        corrections = parse_remarks_for_rules(remarks_text)
        for q_num, correct_ans in corrections.items():
            answers[q_num] = correct_ans
            
        # 若仍然有 # 未替換，預設設為 * 一律給分
        for q_num, ans in list(answers.items()):
            if ans == "#":
                answers[q_num] = "*"
                
    except Exception as e:
        print(f"解析考選部答案出錯: {target_path} -> {e}")
        
    return answers

def extract_tainan_answers(year, date_str):
    """解析台南市答案 PDF"""
    # 尋找檔名如 tainan-92-0921-answer.pdf 或 tainan-95-0813-both.pdf
    ans_file = f"tainan-{year}-{date_str}-answer.pdf" if date_str else f"tainan-{year}-answer.pdf"
    both_file = f"tainan-{year}-{date_str}-both.pdf" if date_str else f"tainan-{year}-both.pdf"
    
    target_file = ans_file if os.path.exists(os.path.join(TAINAN_DIR, ans_file)) else both_file
    target_path = os.path.join(TAINAN_DIR, target_file)
    
    if not os.path.exists(target_path):
        # 嘗試只用年份尋找
        files = os.listdir(TAINAN_DIR)
        for f in files:
            if f.startswith(f"tainan-{year}-") and ("answer" in f or "both" in f):
                target_path = os.path.join(TAINAN_DIR, f)
                break
        else:
            return {}
            
    answers = {}
    try:
        reader = pypdf.PdfReader(target_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
                
        # 全面清理文字中的全形括弧以利於匹配
        text = text.replace("（", "(").replace("）", ")").replace("［", "[").replace("］", "]")
        # 將全形英文字母轉換為半形
        text = text.translate(str.maketrans("ＡＢＣＤ", "ABCD"))
        
        lines = text.split("\n")
        for line in lines:
            if "年" in line and "月" in line and "答案" in line:
                continue
            if "年度" in line and "公開徵選" in line:
                continue
                
            # 1. 匹配如 1. (B) 或 1 (B) 
            matches1 = re.findall(r"(\d+)\s*[.．]?\s*\(\s*([A-D])\s*\)", line)
            
            # 2. 匹配如 1. D 或 1.D
            matches2 = re.findall(r"\b(\d+)\s*[.．]\s*([A-D])\b", line)
            
            # 3. 匹配如 1 D 26 B
            matches3 = re.findall(r"\b(\d+)\s+([A-D])\b", line)
            
            for q_num_str, ans in matches1 + matches2 + matches3:
                q_num = int(q_num_str)
                if 0 < q_num <= 100:
                    answers[q_num] = ans.strip()
    except Exception as e:
        print(f"解析台南市答案出錯: {target_path} -> {e}")
        
    return answers

def clean_text(text):
    return re.sub(r"\s+", " ", text.strip())

def auto_tag_question(question_text, default_subject):
    """根據題目文字內容，執行本地關鍵字貼標並回傳標籤陣列"""
    tags = []
    # 1. 根據關鍵字字典比對
    for tag_name, keywords in TAGS_KEYWORDS.items():
        for kw in keywords:
            if kw in question_text:
                tags.append(tag_name)
                break
                
    # 2. 補上預設的學科子分類標籤
    if default_subject == "基礎醫學":
        # 若無細分，可補充基本基礎醫學標籤
        if not any(t in tags for t in ["解剖學", "生理學", "病理學", "藥理學", "微生物學與免疫學"]):
            tags.append("基礎醫學")
            
    # 去重
    tags = list(set(tags))
    if not tags:
        tags = [default_subject]
    return tags

def parse_moex_questions(year, subject_code, official_answers):
    """解析考選部試題 PDF"""
    q_file = f"moex-{year}-{subject_code}-question.pdf"
    q_path = os.path.join(MOEX_DIR, q_file)
    if not os.path.exists(q_path):
        return []
        
    questions = []
    try:
        reader = pypdf.PdfReader(q_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
                
        # 替換特殊字元
        text = text.replace("", "(A)").replace("", "(B)").replace("", "(C)").replace("", "(D)")
        
        # 清除標頭與標尾無效行
        lines = text.split("\n")
        filtered_lines = []
        for line in lines:
            if re.search(r"代號：|頁次：|注意：|本科目共|分 階 段 考 試|中醫師考試|高等考試|類 科：|科 目：|考試時間：", line):
                continue
            filtered_lines.append(line)
        cleaned_text = "\n".join(filtered_lines)
        
        # 依據已知的答案題號，進行循序漸進式定位切割，以防止 113/114 年無空格格式及其他小數混淆問題
        expected_nums = sorted(list(official_answers.keys()))
        if not expected_nums:
            expected_nums = list(range(1, 51))
            
        positions = []
        current_pos = 0
        search_text = "\n" + cleaned_text
        
        for q_num in expected_nums:
            # 標準匹配：題號後接點或空格，且不為其他小數 (如 2.0)
            pattern = re.compile(r"\n\s*" + str(q_num) + r"(?:\s*[.．]\s*(?!\d)|\s+)")
            match = pattern.search(search_text, current_pos)
            if match:
                positions.append((q_num, match.start(), match.end()))
                current_pos = match.end()
            else:
                # 備用匹配：題號後直接緊鄰中文字元等非數字空格字元
                fallback_pattern = re.compile(r"\n\s*" + str(q_num) + r"\s*(?=[^\d\s])")
                match = fallback_pattern.search(search_text, current_pos)
                if match:
                    positions.append((q_num, match.start(), match.end()))
                    current_pos = match.end()
                else:
                    pass
        
        # 根據定位點重構題目內容
        matches = []
        for idx in range(len(positions)):
            q_num, start_idx, end_idx = positions[idx]
            next_start = positions[idx+1][1] if idx + 1 < len(positions) else len(search_text)
            content = search_text[end_idx:next_start]
            matches.append((str(q_num), content))
        
        subject_name = SUBJECT_NAME_MAP.get(subject_code, "未分類")
        
        for num_str, content in matches:
            q_num = int(num_str)
            flat_content = re.sub(r"\s+", " ", content)
            opt_match = re.search(r"(?:\(A\)|A\.)(.*?)(?:\(B\)|B\.)(.*?)(?:\(C\)|C\.)(.*?)(?:\(D\)|D\.)(.*)", flat_content)
            
            if opt_match:
                q_text = re.split(r"\(A\)|A\.", flat_content)[0].strip()
                options = {
                    "A": opt_match.group(1).strip(),
                    "B": opt_match.group(2).strip(),
                    "C": opt_match.group(3).strip(),
                    "D": opt_match.group(4).strip()
                }
                
                q_id = f"moex-{year}-{subject_code}-{q_num:02d}"
                ans = official_answers.get(q_num, "A") # 若無答案，預設給 A 作為容錯
                
                tags = auto_tag_question(q_text, subject_name)
                
                questions.append({
                    "id": q_id,
                    "question": q_text,
                    "options": options,
                    "answer": ans,
                    "category": "考選部護理師高考",
                    "subject": subject_name,
                    "year": int(year),
                    "tags": tags,
                    "weight": 1.0
                })
    except Exception as e:
        print(f"解析考選部試題出錯: {q_file} -> {e}")
        
    return questions

def parse_tainan_questions(year, date_str, official_answers):
    """解析台南市試題 PDF"""
    q_file = f"tainan-{year}-{date_str}-question.pdf" if date_str else f"tainan-{year}-question.pdf"
    both_file = f"tainan-{year}-{date_str}-both.pdf" if date_str else f"tainan-{year}-both.pdf"
    
    target_file = q_file if os.path.exists(os.path.join(TAINAN_DIR, q_file)) else both_file
    target_path = os.path.join(TAINAN_DIR, target_file)
    
    if not os.path.exists(target_path):
        # 嘗試用年份尋找
        files = os.listdir(TAINAN_DIR)
        for f in files:
            if f.startswith(f"tainan-{year}-") and ("question" in f or "both" in f):
                target_path = os.path.join(TAINAN_DIR, f)
                break
        else:
            return []
            
    questions = []
    try:
        reader = pypdf.PdfReader(target_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
                
        # 替換選項括號
        text = text.replace("（A）", "(A)").replace("（B）", "(B)").replace("（C）", "(C)").replace("（D）", "(D)")
        text = text.replace("]A^", "(A)").replace("]B^", "(B)").replace("]C^", "(C)").replace("]D^", "(D)")
        text = re.sub(r"[\[（(]A[\]）)]", "(A)", text)
        text = re.sub(r"[\[（(]B[\]）)]", "(B)", text)
        text = re.sub(r"[\[（(]C[\]）)]", "(C)", text)
        text = re.sub(r"[\[（(]D[\]）)]", "(D)", text)
        
        # 清除無效行
        lines = text.split("\n")
        filtered_lines = []
        for line in lines:
            if re.search(r"臺南市.*年度|共\s*\d+\s*題|答錯不倒扣|頁次：", line):
                continue
            if re.match(r"^\s*\d+\s*$", line):
                continue
            filtered_lines.append(line)
        cleaned_text = "\n".join(filtered_lines)
        
        # 切割題目
        pattern = r"\n(?:\(\s*\)|（\s*）)?\s*(\d+)\s*[.．]\s*([\s\S]*?)(?=\n(?:\(\s*\)|（\s*）)?\s*(?:\d+)\s*[.．]|\Z)"
        matches = re.findall(pattern, "\n" + cleaned_text)
        
        # 台南市題目大多屬於綜合護理
        subject_name = "綜合護理與公共衛生"
        
        for num_str, content in matches:
            q_num = int(num_str)
            # 排除噪音題號
            if q_num > 100 or q_num <= 0:
                continue
                
            flat_content = re.sub(r"\s+", " ", content)
            opt_match = re.search(r"\(A\)(.*?)\(B\)(.*?)\(C\)(.*?)\(D\)(.*)", flat_content)
            
            if opt_match:
                q_text = flat_content.split("(A)")[0].strip()
                options = {
                    "A": opt_match.group(1).strip(),
                    "B": opt_match.group(2).strip(),
                    "C": opt_match.group(3).strip(),
                    "D": opt_match.group(4).strip()
                }
                
                suffix = f"-{date_str}" if date_str else ""
                q_id = f"tainan-{year}{suffix}-{q_num:02d}"
                ans = official_answers.get(q_num, "A")
                
                tags = auto_tag_question(q_text, "社區衛生學")
                
                questions.append({
                    "id": q_id,
                    "question": q_text,
                    "options": options,
                    "answer": ans,
                    "category": "臺南市衛生局甄試",
                    "subject": subject_name,
                    "year": int(year),
                    "tags": tags,
                    "weight": 1.5
                })
    except Exception as e:
        print(f"解析台南市試題出錯: {target_file} -> {e}")
        
    return questions

def main():
    print("開始解析 PDF 試題與對齊答案...")
    
    all_questions = []
    
    # 1. 解析考選部近 5 年 (110~114 年) 題目
    moex_years = ["110", "111", "112", "113", "114"]
    for year in moex_years:
        for code in SUBJECT_NAME_MAP.keys():
            # 先拿答案
            ans_map = extract_moex_answers(year, code)
            if not ans_map:
                continue
            # 解析題目
            qs = parse_moex_questions(year, code, ans_map)
            if qs:
                all_questions.extend(qs)
                print(f"  [考選部] 已解析 {year} 年 {SUBJECT_NAME_MAP[code]}: {len(qs)} 題")
                
    # 2. 解析台南市衛生局歷屆題目
    # 掃描下載目錄下所有的 tainan- 試題檔案，自動識別年份與日期
    tainan_files = os.listdir(TAINAN_DIR)
    parsed_tainan_keys = set() # 用於防止重複解析
    
    for f in tainan_files:
        if f.startswith("tainan-") and ("question" in f or "both" in f):
            # 提取年份與日期標記，如 tainan-100-0618-question.pdf -> year=100, date_str=0618
            match = re.search(r"tainan-(\d+)(?:-(\d+))?", f)
            if match:
                year = match.group(1)
                date_str = match.group(2)
                
                key = (year, date_str)
                if key in parsed_tainan_keys:
                    continue
                parsed_tainan_keys.add(key)
                
                # 先拿答案
                ans_map = extract_tainan_answers(year, date_str)
                # 解析題目
                qs = parse_tainan_questions(year, date_str, ans_map)
                if qs:
                    all_questions.extend(qs)
                    date_info = f" {date_str}" if date_str else ""
                    print(f"  [台南市] 已解析 {year}年{date_info} 甄試: {len(qs)} 題 (答案匹配率: {len(ans_map)}/{len(qs)})")

    # 3. 檢查總題數
    print(f"\n全部解析完畢！共生成 {len(all_questions)} 筆題目資料。")
    
    # 4. 輸出 questions_db.js
    # 移除 answer 欄位，因其必須存放在答案資料庫中
    js_questions = []
    js_answers = {}
    
    for q in all_questions:
        ans = q.pop("answer")
        js_questions.append(q)
        js_answers[q["id"]] = ans
        
    print(f"正在寫入資料庫檔案...")
    with open(OUTPUT_QUESTIONS_JS, "w", encoding="utf-8") as f:
        f.write("/* eslint-disable */\n")
        f.write("const questions_db = ")
        json.dump(js_questions, f, ensure_ascii=False, indent=2)
        f.write(";\n\nif (typeof module !== 'undefined') { module.exports = { questions_db }; }\n")
        
    with open(OUTPUT_ANSWERS_JS, "w", encoding="utf-8") as f:
        f.write("/* eslint-disable */\n")
        f.write("const answers_db = ")
        json.dump(js_answers, f, ensure_ascii=False, indent=2)
        f.write(";\n\nif (typeof module !== 'undefined') { module.exports = { answers_db }; }\n")
        
    print("寫入 questions_db.js 與 answers_db.js 成功。")
    
    # 5. 進行統計分析並印出，以利確認
    subjects_count = {}
    tags_count = {}
    categories_count = {}
    
    for q in js_questions:
        sub = q["subject"]
        subjects_count[sub] = subjects_count.get(sub, 0) + 1
        
        cat = q["category"]
        categories_count[cat] = categories_count.get(cat, 0) + 1
        
        for t in q["tags"]:
            tags_count[t] = tags_count.get(t, 0) + 1
            
    print("\n====== 📊 題庫統計摘要 ======")
    print("【考題來源分布】")
    for k, v in categories_count.items():
        print(f"  - {k}: {v} 題")
        
    print("【學科分布】")
    for k, v in subjects_count.items():
        print(f"  - {k}: {v} 題")
        
    print("【標籤分布 (前 15 名)】")
    sorted_tags = sorted(tags_count.items(), key=lambda x: x[1], reverse=True)
    for k, v in sorted_tags[:15]:
        print(f"  - {k}: {v} 題")
    print("============================\n")

if __name__ == "__main__":
    main()
