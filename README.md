# TitoNewsBriefingBot 

An automated, AI-powered daily news engine that scrapes tech and global news from multiple RSS feeds, processes and formats the context using Groq's Llama-3.3 engine, and broadcasts a beautifully structured briefing directly to Telegram.

## Features
- **Multi-Source Scraping:** Pulls latest headlines across International (BBC), Tech (TechCrunch), and African (Premium Times) sectors.
- **AI-Driven Categorization:** Leverages the Groq API (`llama-3.3-70b-versatile`) to summarize and group articles seamlessly.
- **Cloud Automation:** Runs 100% hands-off via GitHub Actions cron scheduling.
- **State Persistence:** Commits an internal SQLite database (`seen.db`) back to the repo at runtime to prevent duplicate article broadcasts.

## Architecture & Tech Stack
- **Language:** Python 3.10
- **LLM Engine:** Groq Cloud API 
- **Infrastructure:** GitHub Actions (Cron CI/CD Scheduler)
- **Database:** SQLite (Lightweight duplication filter)
- **API integrations:** Telegram Bot API & RSS Feed Parsers

##  Live Output Demo
![TitoNewsBriefingBot Live Preview](telegram_preview.jpg)

---

## Setup and Installation

### 1. Repository Secrets Configuration
To run this pipeline in the cloud, add the following securely under your GitHub Repo Settings (`Settings -> Secrets and variables -> Actions`):
- `GROQ_API_KEY`: Your production API key from Groq Console.
- `TELEGRAM_TOKEN`: Token from `@BotFather`.
- `TELEGRAM_CHAT_ID`: Your target Telegram channel or group chat ID.

### 2. Local Execution
If you want to run or test the pipeline locally:
```bash
# Clone the project
git clone [https://github.com/YOUR_USERNAME/week-02-news-bot.git](https://github.com/YOUR_USERNAME/week-02-news-bot.git)
cd week-02-news-bot

# Install requirements (excluding virtual environment files)
pip install -r requirements.txt

# Run the controller
python main.py
