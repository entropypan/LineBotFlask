from datetime import datetime, timedelta
from pytz import timezone
import logging

REMIND_BEFORE_MINUTES = 10

def notify_reminders(reminders, line_bot_api):
    now = datetime.now(timezone('Asia/Taipei'))
    new_reminders = []
    for reminder in reminders:
        remind_time_utc = datetime.strptime(reminder["time"], "%Y-%m-%dT%H:%M:%S")
        remind_time_taipei = remind_time_utc.astimezone(timezone('Asia/Taipei'))
        if now >= remind_time_taipei - timedelta(minutes=REMIND_BEFORE_MINUTES) and now < remind_time_taipei:
            try:
                line_bot_api.push_message(
                    reminder["user_id"],
                    f"提醒：{reminder['event']}，時間：{remind_time_taipei.strftime('%Y-%m-%d %H:%M:%S')}"
                )
            except Exception as e:
                logging.error(f"推播失敗：{e}")
                # 推播失敗時保留該提醒
                new_reminders.append(reminder)
        else:
            new_reminders.append(reminder)
    return new_reminders