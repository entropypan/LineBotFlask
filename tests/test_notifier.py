import pytest
from notifier import notify_reminders
from datetime import datetime, timedelta
from pytz import timezone

class DummyLineBotApi:
    def __init__(self):
        self.messages = []
    def push_message(self, user_id, text):
        self.messages.append((user_id, text))

def test_notify_reminders_push_and_remove():
    now = datetime.now(timezone('Asia/Taipei'))
    remind_time = (now + timedelta(minutes=9)).astimezone(timezone('UTC')).strftime("%Y-%m-%dT%H:%M:%S")
    reminders = [{"user_id": "u1", "time": remind_time, "event": "測試提醒"}]
    api = DummyLineBotApi()
    new_reminders = notify_reminders(reminders, api)
    assert len(api.messages) == 1
    assert "測試提醒" in api.messages[0][1]
    # 應該被移除
    assert new_reminders == []

def test_notify_reminders_not_yet():
    now = datetime.now(timezone('Asia/Taipei'))
    remind_time = (now + timedelta(minutes=20)).astimezone(timezone('UTC')).strftime("%Y-%m-%dT%H:%M:%S")
    reminders = [{"user_id": "u2", "time": remind_time, "event": "未到提醒"}]
    api = DummyLineBotApi()
    new_reminders = notify_reminders(reminders, api)
    assert len(api.messages) == 0
    assert new_reminders == reminders