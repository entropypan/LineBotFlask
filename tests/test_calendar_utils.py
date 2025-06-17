import pytest
from calendar_utils import parse_reminder

def test_parse_reminder_tomorrow_afternoon():
    result = parse_reminder("明天下午2點開會")
    assert result is not None
    assert "time" in result and "event" in result
    assert "開會" in result["event"]

def test_parse_reminder_day_after_tomorrow():
    result = parse_reminder("後天8:30 meeting")
    assert result is not None
    assert "meeting" in result["event"]

def test_parse_reminder_mmdd():
    result = parse_reminder("6/4 14:00 報告")
    assert result is not None
    assert "報告" in result["event"]

def test_parse_reminder_afternoon():
    result = parse_reminder("下午3點 測試")
    assert result is not None
    assert "測試" in result["event"]

def test_parse_reminder_evening():
    result = parse_reminder("晚上8點 派對")
    assert result is not None
    assert "派對" in result["event"]

def test_parse_reminder_invalid():
    result = parse_reminder("這不是提醒格式")
    assert result is None