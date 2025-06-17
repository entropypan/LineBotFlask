from flask import Flask, request, abort
import os
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler

from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from calendar_utils import parse_reminder
from storage import load_reminders, save_reminders
from notifier import notify_reminders

load_dotenv()

app = Flask(__name__)

LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
CHANNEL_ACCESS_TOKEN = os.getenv("CHANNEL_ACCESS_TOKEN")
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    body = request.get_data(as_text=True)
    signature = request.headers.get('X-Line-Signature', '')
    try:
        events = parser.parse(body, signature)
    except Exception:
        abort(400)

    reminders = load_reminders()
    for event in events:
        if isinstance(event, MessageEvent) and isinstance(event.message, TextMessage):
            user_id = event.source.user_id
            message_text = event.message.text.strip()

            if message_text == "OK":
                reminders = [
                    r for r in reminders
                    if r.get("user_id") != user_id
                ]
                save_reminders(reminders)
                reply = "提醒已取消"
            else:
                reminder = parse_reminder(message_text)
                if reminder:
                    reminder["user_id"] = user_id
                    reminders.append(reminder)
                    save_reminders(reminders)
                    reply = f"提醒已設定：{reminder['event']}，時間：{reminder['time']}"
                else:
                    reply = "格式錯誤，請輸入：明天下午2點開會 或 6/4 14:00 開會"
            try:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=reply)
                )
            except Exception as e:
                print("回覆失敗：", e)
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