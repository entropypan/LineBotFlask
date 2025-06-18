# LineBotFlask

0. first commit : nothing

1. AI - 1 : 根據我的敘述生成程式碼
回饋：「
    幫我把 parse_reminder(text)、load_reminders()、save_reminders()、notify_reminders() 抽成獨立函式各自放到 calendar_utils.py、storage.py、notifier.py，然後在 app.py 只做路由呼叫嗎? 這樣我才能方便進行unit test
」

2. AI - 2 separate modules : 將程式碼分成多個模組
回饋：「
    以下是我code review後的建議：
    1. 錯誤處理
    load_reminders() 加 try-except 避免錯誤導致系統炸掉
    執行失敗時用 logging 記錄。
    2. 常數化
    將提醒提前分鐘數、檔名等 Magic Number/Strings 抽成常數，方便維護。
    3. 刪除邏輯
    「OK」只刪單一或最近一筆提醒，不要一次砍光。
    4. 測試重點
    parse_reminder() 增補「下午」「晚上」等格式測試
    notify_reminders() mock 推播失敗情境
    請幫我寫入程式中
」

3. AI-3 improve (see README for details) : 根據我的回饋改善程式碼

4. 根據對話針對LINE BOT進行串接，以及增加.gitignore、.env等檔案
