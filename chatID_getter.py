import requests
import time

TOKEN = '<your_telegram_bot_token>'
URL = f"https://api.telegram.org/bot{TOKEN}/"

def get_updates(last_update_id=None):
    url = URL + "getUpdates?timeout=100"
    if last_update_id:
        url += f"&offset={last_update_id + 1}"
    response = requests.get(url)
    return response.json()['result']

def send_message(chat_id, text):
    url = URL + "sendMessage"
    payload = {'chat_id': chat_id, 'text': text}
    requests.post(url, data=payload)

def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        for update in updates:
            if 'message' in update and 'text' in update['message']:
                chat_id = update['message']['chat']['id']
                if update['message']['text'].lower() == '/chatid':
                    send_message(chat_id, f"Chat ID: {chat_id}")
                last_update_id = update['update_id']
        time.sleep(1)

if __name__ == '__main__':
    main()
