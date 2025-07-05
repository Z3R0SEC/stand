from flask import Flask, request
import requests
import os
from threading import Thread

app = Flask(__name__)

PAGE_ACCESS_TOKEN = 'EAAPRPyHULIABPB2H0R38nEwXKUZAXN437uMa40iIdIZCgVZCDwRZCJZAuvdZB5Gu4PIok9sHTY97vnn3gUMVZCHuDyjFnH3THl2GcRenolCpPv2yuAi93XuUGJ40djpeBS5H7BV0BuTjBCeQOwdAKDNiuWLzMT4rfhv99AN4C55ZB8qxoZAXtyJr8cdqBF5smItdTYZB3pNRwiWwZDZD'
VERIFY_TOKEN = 'standby'

FB_URL = 'https://graph.facebook.com/v17.0/me/messages'


def send_message(recipient_id, message_text):
    payload = {
        'recipient': {'id': recipient_id},
        'message': {
            'attachment': {
                'type': 'template',
                'payload': {
                    'template_type': 'button',
                    'text': message_text,
                    'buttons': [
                        {
                            "type": "web_url",
                            "url": "https://example.com",
                            "title": "Visit Website"
                        },
                        {
                            "type": "web_url",
                            "url": "https://example.com/store",
                            "title": "Shop Now"
                        },
                        {
                            "type": "web_url",
                            "url": "https://example.com/support",
                            "title": "Get Support"
                        }
                    ]
                }
            }
        }
    }
    params = {'access_token': PAGE_ACCESS_TOKEN}
    response = requests.post(FB_URL, params=params, json=payload)
    return response.json()


@app.route('/', methods=['GET'])
def verify():
    if request.args.get('hub.verify_token') == VERIFY_TOKEN:
        return request.args.get('hub.challenge')
    return 'Invalid verification token'


@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    if data.get('object') == 'page':
        for entry in data.get('entry', []):
            for messaging_event in entry.get('messaging', []):
                sender_id = messaging_event['sender']['id']

                if 'message' in messaging_event:
                    msg = messaging_event['message']
                    if 'text' in msg:
                        user_msg = msg['text']
                        reply = f"You said: {user_msg}"
                    elif 'attachments' in msg:
                        reply = "You sent an attachment. I can’t read it yet, my developer is working on it."

                    send_message(sender_id, reply)
    return 'ok'


if __name__ == "__main__":
   def run():
       app.run(host='0.0.0.0', port=5001)

   def keep_alive():
       import os
       os.system("clear")
       print("[›] UPTIME ROBOT: ALIVE!")
       t = Thread(target=run)
       t.start()

   keep_alive()
