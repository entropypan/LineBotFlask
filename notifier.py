from datetime import datetime, timedelta
from pytz import timezone

def notify_reminders(reminders, line_bot_api):
    now = datetime.now(timezone('Asia/Taipei'))
    new_reminders = []
    for reminder in reminders:
        remind_time_utc = datetime.strptime(reminder["time"], "%Y-%m-%dT%H:%M:%S")
        remind_time_taipei = remind_time_utc.astimezone(timezone('Asia/Taipei'))
        if now >= remind_time_taipei - timedelta(minutes=10) and now < remind_time_taipei:
            try:
                line_bot_api.push_message(
                    reminder["user_id"],
                    # 這裡直接用 f-string
                    f"提醒：{reminder['event']}，時間：{remind_time_taipei.strftime('%Y-%m-%d %H:%M:%S')}"
                )
            except Exception as e:
                print("推播失敗：", e)
        else:
            new_reminders.append(reminder)
    return new_reminders