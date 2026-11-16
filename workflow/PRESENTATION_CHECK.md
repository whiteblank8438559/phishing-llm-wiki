# Step 7｜教學 HTML 簡報檢查紀錄

檢查日期：2026-11-16（Asia/Taipei）。本紀錄只描述實際執行的檢查；未測試公開部署後的網址。

## 檢查流程與結果

| 檢查項目 | 實際結果 |
| --- | --- |
| Wiki 匯入與提綱 | `workflow/check_result.json` 為 `pass`；共有 5 篇來源、5 篇主題頁、7 張規劃投影片。 |
| 提綱與 HTML 數量 | `workflow/slide_plan.json` 規劃 7 張，`presentation/index.html` 實際有 7 張。 |
| 本機連結 | HTML 中 9 個本機資源或 Wiki 連結均指向現有檔案；CSS、JS 均成功載入。 |
| 瀏覽器開啟 | 以本機靜態伺服器開啟 `presentation/`，首頁顯示正常；HTML、CSS、JS 回應成功。 |
| 換頁 | 從「開始學習」進入第 2 張，再依序前進到第 7 張；頁碼依序更新，最後一張的「下一張」停用。 |
| 練習題 | 點錯誤選項會顯示提醒；點正確選項會提示自行開啟官方 App 或網站查證。 |
| 重看 | 最後一張的「從頭再看一次」能返回第 1 張。 |
| 手機版 | 390 × 844 視窗下檢查首頁與第 7 張；可閱讀、按鈕可操作，沒有水平溢出。 |
| 瀏覽器錯誤 | 互動測試後沒有 JavaScript console error。 |

瀏覽器有請求 `/favicon.ico`，因專案沒有設定分頁小圖示而回傳 404；不影響頁面、樣式、腳本或操作。

## 內容回查

| HTML 頁面 | 對應 Wiki／資料 |
| --- | --- |
| 1 開場與學習目標 | `PLAN.md` |
| 2 什麼是網路釣魚 | `topics/what-is-phishing.md`；S01、S04 |
| 3 五類警訊 | `topics/warning-signs.md`；S01–S05 |
| 4 暫停、查看、獨立查證 | `topics/verify-before-click.md`；S02、S03 |
| 5 假冒機關簡訊案例 | `topics/government-text-case.md`；S05 |
| 6 收到或誤點後處理 | `topics/respond-and-report.md`；S01、S04、S05 |
| 7 練習與重點回顧 | 前述主題頁及 `AUDIT_LOG.md` |

案例明示是依官方資料改寫，不是原始簡訊；示意訊息沒有可點的假網址。臺灣的 165 諮詢和美國 FTC 的回報方式有分開說明。若內容有來源問題，依 `workflow/WORKFLOW.md` 回 Wiki 主題頁及來源筆記修正，再重新產生提綱並核對簡報；若只是排版問題，修 HTML/CSS 後重測瀏覽器。

## 可核對的畫面

- [桌面版首頁](../evidence/desktop-home.jpg)
- [手機版首頁](../evidence/mobile-home.jpg)

## 本次反思

最容易出錯的是將來源濃縮成短句時失去適用範圍，例如把美國的通報方式當作臺灣做法，或把案例改寫說成原始簡訊。Wiki 檢查階段已修正這類表述；本次簡報檢查時逐頁回查 Wiki 與來源。第 5 步另以暫存副本移除 S05，驗證缺資料時會回到 Wiki 修正，而非直接產生簡報。後續若發現內容問題，仍先回到資料與主題頁；若是顯示問題，直接修簡報並重測。
