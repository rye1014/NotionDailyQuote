import os
import random
import requests

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
NOTION_API_URL = "https://api.notion.com/v1"
HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

# 查詢所有 tag 包含 "佳句" 的資料
def query_quotes():
    url = f"{NOTION_API_URL}/databases/{DATABASE_ID}/query"
    payload = {
        "filter": {
            "property": "tag",
            "multi_select": {
                "contains": "佳句"
            }
        }
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    response.raise_for_status()
    return response.json()["results"]

# 將所有的「判定」改為 False
def clear_judgement(pages):
    for page in pages:
        page_id = page["id"]
        url = f"{NOTION_API_URL}/pages/{page_id}"
        payload = {
            "properties": {
                "判定": {
                    "checkbox": False
                }
            }
        }
        requests.patch(url, headers=HEADERS, json=payload)

# 隨機選一則，設為 True
def set_random_judgement(pages):
    if not pages:
        print("⚠ 沒有符合條件的佳句。")
        return
    chosen = random.choice(pages)
    page_id = chosen["id"]
    url = f"{NOTION_API_URL}/pages/{page_id}"
    payload = {
        "properties": {
            "判定": {
                "checkbox": True
            }
        }
    }
    requests.patch(url, headers=HEADERS, json=payload)
    name = chosen["properties"]["Name"]["title"][0]["plain_text"]
    print(f"✅ 今日佳句：{name}")

if __name__ == "__main__":
    quotes = query_quotes()
    clear_judgement(quotes)
    set_random_judgement(quotes)
