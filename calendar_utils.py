import re
from datetime import datetime, timedelta
from pytz import timezone

def parse_reminder(text: str):
    now = datetime.now(timezone('Asia/Taipei'))
    if "明天" in text:
        base_date = now + timedelta(days=1)
        text = text.replace("明天", "")
    elif "後天" in text:
        base_date = now + timedelta(days=2)
        text = text.replace("後天", "")
    else:
        base_date = now

    # 支援「下午」「晚上」
    time_match = re.search(r'(下午|晚上)?(\d{1,2})[:點](\d{2})?', text)
    if time_match:
        hour = int(time_match.group(2))
        minute = int(time_match.group(3)) if time_match.group(3) else 0
        if time_match.group(1):  # 有「下午」或「晚上」
            if hour < 12:
                hour += 12
        event_time = base_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
        event = text[time_match.end():].strip()
    else:
        date_time_match = re.search(r'(\d{1,2})/(\d{1,2})\s*(\d{1,2}):(\d{2})', text)
        if date_time_match:
            month = int(date_time_match.group(1))
            day = int(date_time_match.group(2))
            hour = int(date_time_match.group(3))
            minute = int(date_time_match.group(4))
            year = now.year
            event_time = datetime(year, month, day, hour, minute, tzinfo=timezone('Asia/Taipei'))
            event = text[date_time_match.end():].strip()
        else:
            return None

    if event_time.tzinfo is None:
        event_time = timezone('Asia/Taipei').localize(event_time)

    event_time_utc = event_time.astimezone(timezone('UTC'))
    return {
        "time": event_time_utc.strftime("%Y-%m-%dT%H:%M:%S"),
        "event": event.strip()
    }