# Notion Daily Quote

靈感來自[這篇文章](https://vocus.cc/article/655b9360fd89780001b4c3f8)，原始構想是透過 Notion 展示自己記錄下來的佳句。此版本進一步結合 Notion API、GitHub Actions 與 Telegram Bot，實現全自動化的佳句推播。

---

## 功能特色

- 查詢 Notion 資料庫中 `tag` 欄位包含「佳句」的資料
- 從符合條件的項目中隨機挑選一則
- 將該則的 `Show` 欄位設為 `True`，其他設為 `False`
- 於每次執行後，發送訊息至 Telegram
- 每小時自動觸發（可自訂）
- 支援手動觸發與自動排程

---

## 使用前準備

### 1. 建立 Telegram Bot 與 Chat ID

1. 使用 [@BotFather](https://t.me/BotFather) 建立 Bot，取得 Bot Token
2. 傳送一則訊息給該 Bot（必要，否則無法主動傳訊）
3. 使用 [@userinfobot](https://t.me/userinfobot) 查詢你的 Telegram 使用者 ID（chat ID）

### 2. 建立 Notion Integration 並分享權限

1. 到 [Notion Developers](https://www.notion.com/my-integrations) 建立 integration 並取得 **token**
2. 將該整合加入你的佳句資料庫
3. 複製該資料庫的 ID（網址中 `/xxxxx?v=...` 前的部分）

### 3. 設定 GitHub Secrets

在 GitHub repository 的  
**Settings → Secrets and variables → Actions** 中加入以下 Secrets：

| 名稱                  | 說明                     |
|-----------------------|--------------------------|
| `NOTION_TOKEN`        | Notion Integration token |
| `NOTION_DATABASE_ID`  | 資料庫 ID                |
| `TELEGRAM_BOT_TOKEN`  | Telegram Bot token       |
| `TELEGRAM_CHAT_ID`    | Telegram Chat ID         |

---

## 自動化設定 (GitHub Actions)

內建 GitHub Actions：
- 每小時自動執行（可調整 `cron` 表達式）
- 支援手動執行

工作流程檔案：`.github/workflows/daily.yml`

---

## Notion 資料庫格式要求

| Name（title） | tag（multi-select） | Show（checkbox） |
|---------------|---------------------|------------------|
| 佳句內容       | 至少包含「佳句」     | 系統會更新此欄位 |

- 每次只會勾選一則 Show = `True`
- 主頁嵌入 view 時，可用 filter：`Show == true` 來展示當期佳句

---

## 專案結構

```plaintext
.
├── update_judgement.py      # 主程式，執行查詢與更新
├── requirements.txt         # 安裝 requests 套件
└── .github/
    └── workflows/
        └── daily.yml        # GitHub Actions 自動化排程
