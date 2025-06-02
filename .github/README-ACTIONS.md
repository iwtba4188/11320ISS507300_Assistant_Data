# GitHub Action - Dcard 爬蟲自動化

## 📋 概述

這個 GitHub Action 會自動執行 Dcard 寵物送養資料的爬取任務，包括：

1. **URL 爬取**: 從 Dcard 送養版面獲取文章 URL
2. **內容爬取**: 獲取每篇文章的詳細內容
3. **資料存儲**: 將資料保存為 CSV 和 JSON 格式
4. **自動提交**: 將更新的資料提交到 GitHub 倉庫

## ⏰ 執行時間

- **自動執行**: 每小時執行一次 (UTC 時間)
- **手動觸發**: 可以在 GitHub Actions 頁面手動執行
- **程式碼更新**: 當相關程式碼有變更時自動執行

## 🔧 技術細節

### 環境配置

- **Python 版本**: 3.13.2
- **套件管理**: 使用 `uv` 進行快速安裝
- **運行環境**: Ubuntu Latest
- **超時設定**: 30 分鐘

### 執行步驟

1. **🛠️ 環境準備**
   - 檢出程式碼
   - 設定 Python 環境
   - 安裝 uv 套件管理器
   - 安裝專案依賴

2. **🔍 URL 爬取**
   - 執行 `src/crawl_dcard_title_urls.py`
   - 獲取最新的文章 URL
   - 避免重複爬取已存在的 URL

3. **📖 內容爬取**
   - 執行 `src/crawl_dcard_url_content.py`
   - 爬取所有未處理文章的詳細內容
   - 更新爬取狀態

4. **💾 資料提交**
   - 檢查是否有新資料
   - 自動提交變更到 GitHub
   - 包含統計資訊的提交訊息

## 📊 輸出檔案

- **`static/dcard_urls.csv`**: 包含所有文章 URL 和元資料
- **`static/dcard_contents.json`**: 包含所有文章的詳細內容

## 🔍 監控與除錯

### GitHub Actions 頁面功能

- **即時日誌**: 查看每個步驟的執行狀況
- **統計摘要**: 每次執行後顯示爬取統計
- **錯誤截圖**: 失敗時自動上傳錯誤截圖
- **執行歷史**: 追蹤所有執行記錄

### 日誌資訊

- 🚀 開始/完成標記
- 📊 統計資料 (URL 數量、文章數量)
- ✅/❌ 成功/失敗狀態
- 📈 進度追蹤

### 錯誤處理

- 失敗時自動保存錯誤截圖
- 詳細的錯誤日誌
- 7 天的錯誤資料保留期

## 🚀 手動執行

在 GitHub 倉庫頁面：

1. 點擊 "Actions" 標籤
2. 選擇 "Crawl Dcard Data" workflow
3. 點擊 "Run workflow" 按鈕
4. 確認執行

## ⚙️ 配置選項

如需修改爬取行為，可以編輯：

- `src/crawl_dcard_title_urls.py` - URL 爬取邏輯
- `src/crawl_dcard_url_content.py` - 內容爬取邏輯
- `.github/workflows/crawl-dcard.yml` - GitHub Action 配置

## 📝 提交訊息格式

自動提交會包含以下資訊：

```md
🤖 Auto-crawl: Updated Dcard data

📊 Stats:
- URLs: [數量]
- Articles: [數量]  
- Time: [執行時間]
- Run: #[執行編號]
```

## 🔒 權限要求

Action 需要以下權限：

- **Contents**: 讀寫倉庫內容
- **Actions**: 執行 workflow
- **Metadata**: 讀取倉庫元資料

這些權限已在 workflow 檔案中正確配置。
