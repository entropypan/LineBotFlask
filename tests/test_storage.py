import os
import json
import pytest
from storage import load_reminders, save_reminders, REMINDER_FILE

def test_save_and_load_reminders(tmp_path):
    test_file = tmp_path / "reminders.json"
    test_data = [{"user_id": "abc", "time": "2025-06-17T10:00:00", "event": "test"}]
    # Patch REMINDER_FILE
    import storage
    storage.REMINDER_FILE = str(test_file)
    save_reminders(test_data)
    loaded = load_reminders()
    assert loaded == test_data

def test_load_reminders_file_not_exist(tmp_path):
    import storage
    storage.REMINDER_FILE = str(tmp_path / "not_exist.json")
    assert load_reminders() == []