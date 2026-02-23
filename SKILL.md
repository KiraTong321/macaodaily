---
name: macaodaily
description: 使用專案根目錄的 scrape_macaodaily.py，根據日期抓取澳門日報頭版與經濟版標題。若未提供日期則自動使用今天。
argument-hint: [date?]
disable-model-invocation: true
allowed-tools: Bash
---

### 執行步驟
1. 判斷傳入的 `$ARGUMENTS` 是否包含日期。
2. 如有 `$ARGUMENTS`，直接視為 `YYYY-MM-DD` 格式的查詢日期；如無，使用 `date +%F` 取今天日期。
3. 在專案根目錄執行 `python scrape_macaodaily.py <日期>`，其中 `<日期>` 為前兩步得到的值。
4. 讓使用者知道命令已執行並說明資料來源（澳門日報 node_2 區塊）。

### 注意事項
- 請避免直接修改腳本，若需更改邏輯請先告知使用者再修改 `scrape_macaodaily.py`。
- 確保 `$ARGUMENTS` 合法（格式為 `YYYY-MM-DD`）；若不合法，可回報：「請提供 YYYY-MM-DD 格式的日期」。
