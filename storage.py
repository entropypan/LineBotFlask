import os
import json

REMINDER_FILE = "reminders.json"

def load_reminders():
    if not os.path.exists(REMINDER_FILE):
        return []
    with open(REMINDER_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_reminders(reminders):
    with open(REMINDER_FILE, "w", encoding="utf-8") as f:
        json.dump(reminders, f, ensure_ascii=False, indent=2)