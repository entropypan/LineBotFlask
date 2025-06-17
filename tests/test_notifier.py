import pytest
from notifier import notify_reminders, REMIND_BEFORE_MINUTES
from datetime import datetime, timedelta
from pytz import timezone

class DummyLineBotApi:
    def __init__(self, fail=False):
        self.messages = []
        self.fail = fail
    def push_message(self, user_id, text):
        if self.fail:
            raise Exception("推播失敗")
        self.messages.append((user_id, text))

def test_notify_reminders_push_and_remove():
    now = datetime.now(timezone('Asia/Taipei'))
    remind_time = (now + timedelta(minutes=REMIND_BEFORE_MINUTES-1)).astimezone(timezone('UTC')).strftime("%Y-%m-%dT%H:%M:%S")
    reminders = [{"user_id": "u1", "time": remind_time, "event": "測試提醒"}]
    api = DummyLineBotApi()
    new_reminders = notify_reminders(reminders, api)
    assert len(api.messages) == 1
    assert "測試提醒" in api.messages[0][1]
    # 應該被移除
    assert new_reminders == []

def test_notify_reminders_not_yet():
    now = datetime.now(timezone('Asia/Taipei'))
    remind_time = (now + timedelta(minutes=REMIND_BEFORE_MINUTES+10)).astimezone(timezone('UTC')).strftime("%Y-%m-%dT%H:%M:%S")
    reminders = [{"user_id": "u2", "time": remind_time, "event": "未到提醒"}]
    api = DummyLineBotApi()
    new_reminders = notify_reminders(reminders, api)
    assert len(api.messages) == 0
    assert new_reminders == reminders

def test_notify_reminders_push_fail():
    now = datetime.now(timezone('Asia/Taipei'))
    remind_time = (now + timedelta(minutes=REMIND_BEFORE_MINUTES-1)).astimezone(timezone('UTC')).strftime("%Y-%m-%dT%H:%M:%S")
    reminders = [{"user_id": "u3", "time": remind_time, "event": "推播失敗提醒"}]
    api = DummyLineBotApi(fail=True)
    new_reminders = notify_reminders(reminders, api)
    # 推播失敗時提醒應保留
    assert new_reminders