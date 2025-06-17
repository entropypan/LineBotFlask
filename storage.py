import os
import json
import logging

REMINDER_FILE = "reminders.json"

def load_reminders():
    if not os.path.exists(REMINDER_FILE):
        return []
    try:
        with open(REMINDER_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"讀取提醒檔案失敗: {e}")
        return []

def save_reminders(reminders):
    try:
        with open(REMINDER_FILE, "w", encoding="utf-8") as f:
            json.dump(reminders, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logging.error(f"儲存提醒檔案失敗: {e}")