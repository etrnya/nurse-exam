import os
import re
import sys
import time
import requests
import urllib3
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

# 停用 InsecureRequestWarning 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 強制 stdout 使用 UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# 專案術語對齊：此腳本負責下載考選部近 5 年 (110~114 年) 護理師高考 5 大科目的試題、答案與更正答案 PDF
# 5 大科目代碼映射：
SUBJECT_MAP = {
    "基礎醫學": "basic-med",
    "基本護理學與護理行政": "basic-nursing",
    "基本護理學(包括護理原理、護理技術)與護理行政": "basic-nursing",
    "基本護理學（包括護理原理、護理技術）與護理行政": "basic-nursing",
    "內外科護理學": "med-surg",
    "產兒科護理學": "obs-ped",
    "精神科與社區衛生護理學": "psych-community"
}

DOWNLOAD_DIR = "downloads/moex"
MOEX_SEARCH_URL = "https://wwwq.moex.gov.tw/exam/wFrmExamQandASearch.aspx"
BASE_URL = "https://wwwq.moex.gov.tw/exam/"

def clean_text(text):
    return re.sub(r'\s+', ' ', text.strip())

def parse_year(text):
    # 匹配民國年份
    match = re.search(r'(\d+)年', text)
    if match:
        roc_year = int(match.group(1))
        return roc_year
    return None

def fetch_moex_results_html():
    """使用 Playwright 模擬進階查詢護理師，並獲取結果頁面 HTML"""
    print("啟動 Playwright 瀏覽器...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        print(f"導向至考選部查詢頁面: {MOEX_SEARCH_URL}")
        page.goto(MOEX_SEARCH_URL, wait_until="networkidle", timeout=45000)
        
        print("點擊 '切換至進階查詢'...")
        page.click("#ctl00_holderContent_ibtnFull")
        page.wait_for_load_state("networkidle")
        time.sleep(1)
        
        # 選擇開始年份：110年 (對應西元 2021)
        print("選擇開始年份: 110年 (2021)...")
        page.select_option("#ctl00_holderContent_wUctlExamYearStart_ddlExamYear", value="2021")
        page.wait_for_load_state("networkidle")
        time.sleep(1.5)
        
        # 選擇結束年份：114年 (對應西元 2025)
        print("選擇結束年份: 114年 (2025)...")
        page.select_option("#ctl00_holderContent_wUctlExamYearEnd_ddlExamYear", value="2025")
        page.wait_for_load_state("networkidle")
        time.sleep(1.5)
        
        # 填入類科：護理師
        print("填入類科: 護理師...")
        page.fill("#ctl00_holderContent_txtCategoryName", "護理師")
        
        # 點擊查詢按鈕
        print("點擊查詢...")
        page.click("#ctl00_holderContent_btnQuery")
        
        # 等待查詢結果表格載入
        print("等待查詢結果表格載入...")
        try:
            page.wait_for_selector("#ctl00_holderContent_tblExamQand", timeout=30000)
            print("結果表格載入成功！")
        except Exception as e:
            print(f"等待結果表格超時或失敗: {e}")
            # 儲存截圖以供調試
            page.screenshot(path="moex_error_screenshot.png")
            print("已將錯誤截圖儲存至 moex_error_screenshot.png")
            browser.close()
            return None
            
        html = page.content()
        browser.close()
        return html

def download_file(url, target_path):
    """下載檔案並寫入磁碟，支援 verify=False 繞過憑證錯誤"""
    try:
        res = requests.get(url, timeout=20, verify=False)
        res.raise_for_status()
        with open(target_path, "wb") as f:
            f.write(res.content)
        return True
    except Exception as e:
        print(f"  下載失敗: {url} -> {e}")
        return False

def parse_and_download(html_content):
    if not html_content:
        print("沒有 HTML 內容可供解析。")
        return
        
    soup = BeautifulSoup(html_content, "html.parser")
    table = soup.find("table", {"id": "ctl00_holderContent_tblExamQand"})
    if not table:
        print("找不到結果表格 #ctl00_holderContent_tblExamQand。")
        return
        
    rows = table.find_all("tr")
    print(f"結果表格共包含 {len(rows)} 行，開始進行結構化解析與下載...")
    
    current_year = None
    current_session = "1"
    current_exam_name = ""
    current_level = ""
    
    download_tasks = []
    
    for row in rows:
        cells = [clean_text(c.text) for c in row.find_all(["td", "th"])]
        if not cells:
            continue
            
        row_text = cells[0]
        
        # 識別考試名稱與年份 (如: 114年專門職業及技術人員高等考試...)
        if "考試" in row_text and parse_year(row_text) is not None:
            current_year = parse_year(row_text)
            current_exam_name = re.sub(r'本考試.*$', '', row_text).strip()
            
            # 識別考期 (第一次 -> 1, 第二次 -> 2, 第三次 -> 3)
            current_session = "1"
            if "第二次" in current_exam_name:
                current_session = "2"
            elif "第三次" in current_exam_name:
                current_session = "3"
            continue
            
        # 識別類科組別
        if "護理師" in row_text and "_" in row_text:
            current_level = row_text.split("_")[0].strip()
            continue
            
        # 尋找科目的連結
        links = row.find_all("a", href=True)
        if not links:
            continue
            
        # 清理並提取科目名稱
        subject_name = row_text
        subject_name = re.sub(r'(試題|答案|更正答案)+$', '', subject_name).strip()
        subject_name = re.sub(r'試題.*$', '', subject_name).strip()
        
        # 檢查是否為 5 大核心考科之一
        matched_subject_code = None
        for k, v in SUBJECT_MAP.items():
            if k in subject_name:
                matched_subject_code = v
                break
                
        if not matched_subject_code:
            continue
            
        # 提取試題、答案、更正答案 PDF 網址
        for a in links:
            a_text = clean_text(a.text)
            a_href = a["href"]
            full_url = a_href if a_href.startswith("http") else BASE_URL + a_href
            
            file_type = None
            if "試題" in a_text:
                file_type = "question"
            elif "更正答案" in a_text:
                file_type = "corrected"
            elif "答案" in a_text:
                file_type = "answer"
                
            if file_type and current_year:
                # 建立結構化檔名: moex-{year}-{session}-{subject_code}-{file_type}.pdf
                filename = f"moex-{current_year}-{current_session}-{matched_subject_code}-{file_type}.pdf"
                download_tasks.append((full_url, filename, f"{current_year}年第{current_session}次 {subject_name} ({a_text})"))
                
    # 進行去重
    unique_tasks = []
    seen_filenames = set()
    for url, filename, desc in download_tasks:
        if filename not in seen_filenames:
            seen_filenames.add(filename)
            unique_tasks.append((url, filename, desc))
            
    print(f"解析完成，共篩選出 {len(unique_tasks)} 個待下載的考選部 PDF 檔案。")
    
    success_count = 0
    for url, filename, desc in unique_tasks:
        target_path = os.path.join(DOWNLOAD_DIR, filename)
        if os.path.exists(target_path) and os.path.getsize(target_path) > 0:
            print(f"檔案已存在，跳過: {filename} ({desc})")
            success_count += 1
            continue
            
        print(f"正在下載: {filename} <- {desc}")
        if download_file(url, target_path):
            print(f"下載成功: {filename}")
            success_count += 1
            # 延遲以防請求過於頻繁
            time.sleep(0.5)
        else:
            print(f"下載失敗: {filename}")
            
    print(f"考選部護理師考題下載完成，成功下載/已存在: {success_count}/{len(unique_tasks)}。")

def main():
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    html_content = fetch_moex_results_html()
    parse_and_download(html_content)

if __name__ == "__main__":
    main()
