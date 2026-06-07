import requests

def send_telegram_message(ai_brief, telegram_token, chat_id):
    url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
    
    payload = {
        "chat_id": chat_id,
        "text": ai_brief,
        "parse_mode": "HTML"
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
