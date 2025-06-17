from flask import Flask, request, abort
import os
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
import logging

from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from calendar_utils import parse_reminder
from storage import load_reminders, save_reminders, REMINDER_FILE
from notifier import notify_reminders, REMIND_BEFORE_MINUTES

load_dotenv()

app = Flask(__name__)

LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
CHANNEL_ACCESS_TOKEN = os.getenv("CHANNEL_ACCESS_TOKEN")
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(LINE_CHANNEL_SECRET)

logging.basicConfig(level=logging.INFO)

@app.route("/callback", methods=['POST'])
def callback():
    body = request.get_data(as_text=True)
    signature = request.headers.get('X-Line-Signature', '')
    try:
        events = parser.parse(body, signature)
    except Exception as e:
        logging.error(f"Webhook 驗證失敗: {e}")
        abort(400)

    reminders = load_reminders()
    for event in events:
        if isinstance(event, MessageEvent) and isinstance(event.message, TextMessage):
            user_id = event.source.user_id
            message_text = event.message.text.strip()

            if message_text == "OK":
                # 只刪除最近一筆未來提醒
                now = datetime.now(timezone('Asia/Taipei'))
                user_reminders = [r for r in reminders if r.get("user_id") == user_id]
                if user_reminders:
                    # 找最近一筆未來提醒
                    user_reminders = sorted(
                        user_reminders,
                        key=lambda r: datetime.strptime(r["time"], "%Y-%m-%dT%H:%M:%S")
                    )
                    for r in user_reminders:
                        remind_time = datetime.strptime(r["time"], "%Y-%m-%dT%H:%M:%S").astimezone(timezone('Asia/Taipei'))
                        if remind_time > now:
                            reminders.remove(r)
                            save_reminders(reminders)
                            reply = f"已刪除您最近一筆提醒：{r['event']}，時間：{remind_time.strftime('%Y-%m-%d %H:%M:%S')}"
                            break
                    else:
                        reply = "您目前沒有未來的提醒。"
                else:
                    reply = "您目前沒有提醒。"
            else:
                reminder = parse_reminder(message_text)
                if reminder:
                    reminder["user_id"] = user_id
                    reminders.append(reminder)
                    save_reminders(reminders)
                    remind_time_utc = datetime.strptime(reminder["time"], "%Y-%m-%dT%H:%M:%S")
                    remind_time_taipei = remind_time_utc.astimezone(timezone('Asia/Taipei'))
                    reply = f"提醒已設定：{reminder['event']}，時間：{remind_time_taipei.strftime('%Y-%m-%d %H:%M:%S')}"
                else:
                    reply = "格式錯誤，請輸入：明天下午2點開會 或 6/4 14:00 開會"
            try:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=reply)
                )
            except Exception as e:
                logging.error(f"回覆失敗：{e}")
    return 'OK'

def scheduled_notify():
    reminders = load_reminders()
    new_reminders = notify_reminders(reminders, line_bot_api)
    save_reminders(new_reminders)

scheduler = BackgroundScheduler()
scheduler.add_job(func=scheduled_notify, trigger="interval", minutes=1)
scheduler.start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)