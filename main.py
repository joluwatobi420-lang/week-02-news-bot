import os
from dotenv import load_dotenv
from news_fetcher import fetch_general_news
from ai_styler import generate_ai_brief
from telegram_sender import send_telegram_message 

# 1. Load local .env configuration securely if it exists
base_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(base_dir, '.env')
if os.path.exists(env_path):
    load_dotenv(dotenv_path=env_path, override=True)
else:
    # If no .env file exists, look natively at the system context (Githun Actions)
    load_dotenv()

def main():
    print("==STARTING DAILY BRIEFING PIPELINE ===")

    # 1. Fetch credentials securely
    groq_key = os.environ.get("GROQ_API_KEY")
    telegram_token = os.environ.get("TELEGRAM_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    
    if not groq_key:
        print("Error: Missing GROQ_API_KEY in .env file!")
        print(f"DEBUG: Checked file at path -> {env_path}")
        return

    # 2. Run scraping engine
    raw_stories = fetch_general_news(groq_key)
    if not raw_stories:
        print("Pipeline stopped: Could not crape new items.")
        return
    
    # 3. Format with Groq Llama-3
    print("Sending data to Groq AI Engine for styling...")
    ai_brief = generate_ai_brief(raw_stories, groq_key)
    if not ai_brief:
        print("Pipeline stopped: Groq AI failed to generate brief.")
        return
    
    # 4. Ship to phone!
    print("Shipping structured briefing block to Telegram...")
    success = send_telegram_message(ai_brief, telegram_token, chat_id)
    if success:
        print("Success! Check your TitoNewsBriefingBot chat window on your phone.")
    else:
        print("Pipeline failed at final delivery step.")

if __name__ == "__main__":
    main()    



    