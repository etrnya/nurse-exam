import os
import re
import sys
import requests
import urllib3
from bs4 import BeautifulSoup

# 停用 InsecureRequestWarning 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 強制 stdout 使用 UTF-8 以防 Windows 終端機 CP950 編碼出錯
sys.stdout.reconfigure(encoding='utf-8')

# 台南市衛生局甄試試題下載器
# 專案術語對齊：此腳本負責下載台南市衛生局歷屆護理人員甄試 PDF 試題與答案

BASE_URL = "https://health.tainan.gov.tw/"
PAGE_URL = "https://health.tainan.gov.tw/page.asp?mainid=05E5FB73-340E-4D5D-9A7B-59C2DCD4F194&srcorcaid=49027783-987D-4D70-A08E-2FB99422F8E0"
DOWNLOAD_DIR = "downloads/tainan"
CACHE_HTML_PATH = r"C:\Users\etrny\.gemini\antigravity-ide\brain\eee18983-49fb-4e26-a3a9-ee735d957d12\.system_generated\steps\551\content.md"

def fetch_html():
    """獲取網頁 HTML 內容，優先嘗試線上抓取，若失敗則讀取本機快取"""
    try:
        print(f"正在嘗試線上獲取網頁內容: {PAGE_URL}")
        response = requests.get(PAGE_URL, timeout=10, verify=False)
        response.raise_for_status()
        # 由於網頁編碼可能是 big5，此處進行解碼處理
        response.encoding = response.apparent_encoding
        return response.text
    except Exception as e:
        print(f"線上獲取失敗 ({e})，嘗試讀取本機快取檔案...")
        if os.path.exists(CACHE_HTML_PATH):
            with open(CACHE_HTML_PATH, "r", encoding="utf-8") as f:
                content = f.read()
                # 移除 markdown 頁首資訊，保留 HTML 部分
                html_start = content.find("<!DOCTYPE html>")
                if html_start != -1:
                    return content[html_start:]
                return content
        else:
            raise FileNotFoundError(f"找不到本機快取檔案且線上請求失敗。")

def clean_filename(text):
    """將中文標題與連結文字轉換為結構化檔名"""
    # 匹配年份，如「92年9月21日」或「101年」
    year_match = re.search(r"(\d+)年(?:(\d+)月(\d+)日)?", text)
    if not year_match:
        return None
    
    year = year_match.group(1)
    month = year_match.group(2)
    day = year_match.group(3)
    
    date_str = f"{year}"
    if month and day:
        date_str += f"-{int(month):02d}{int(day):02d}"
    
    # 區分試題與答案類型
    if "口試" in text:
        # 排除口試試題
        return None
    
    file_type = "both"
    if "試題" in text and "答案" in text:
        file_type = "both"
    elif "答案" in text:
        file_type = "answer"
    elif "試題" in text or "筆試" in text:
        file_type = "question"
        
    return f"tainan-{date_str}-{file_type}.pdf"

def main():
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    html_content = fetch_html()
    soup = BeautifulSoup(html_content, "html.parser")
    
    # 尋找所有 href 包含 warehouse 的連結
    links = soup.find_all("a", href=True)
    download_tasks = []
    
    for link in links:
        href = link["href"]
        if "warehouse" in href:
            title = link.get("title", "")
            text = link.get_text()
            
            # 使用 title 或 連結文字作為檔名解析依據
            desc = title if title else text
            filename = clean_filename(desc)
            
            if filename:
                full_download_url = href if href.startswith("http") else BASE_URL + href
                download_tasks.append((full_download_url, filename, desc))
    
    print(f"解析完成，共發現 {len(download_tasks)} 個待下載檔案。")
    
    success_count = 0
    for url, filename, desc in download_tasks:
        target_path = os.path.join(DOWNLOAD_DIR, filename)
        if os.path.exists(target_path):
            print(f"檔案已存在，跳過: {filename} ({desc})")
            success_count += 1
            continue
            
        try:
            print(f"正在下載: {filename} <- {desc}")
            res = requests.get(url, timeout=15, verify=False)
            res.raise_for_status()
            with open(target_path, "wb") as f:
                f.write(res.content)
            print(f"下載成功: {filename}")
            success_count += 1
        except Exception as e:
            print(f"下載失敗: {filename} ({e})")
            
    print(f"台南市衛生局試題下載完成，成功下載/已存在: {success_count}/{len(download_tasks)}。")

if __name__ == "__main__":
    main()
