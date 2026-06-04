import requests

def send_telegram_message(brief_text, bot_token, chat_id):
    if not brief_text or not bot_token or not chat_id:
        return False

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": brief_text,
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return True
        else:
            print(f"Telegram API Error: {response.text}")
            return False
    except Exception as e:
        print(f"Telegram Network Error: {e}")
        return False
