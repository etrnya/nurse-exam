import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("answers_db.js", "r", encoding="utf-8") as f:
    content = f.read()
    
match = re.search(r"const\s+answers_db\s*=\s*([\s\S]*?);", content)
db = json.loads(match.group(1).strip())
print("moex-114-2-basic-med-14 answer:", db.get("moex-114-2-basic-med-14"))
