import json
import subprocess

def fetch_general_news(api_key):
    """
    Fetches the top global headlines across all categories using NewsAPI.
    """
    print("Pulling latest global headlines via NewsAPI...")

    # 1. Hit the NewsAPI endpoint
    url = f"https://newsapi.org/v2/top-headlines?language=en&apiKey={api_key}"

    try:
        response = requests.get(url)
        response.raise_status()      # Check for HTTP errors
        data = response.json()

        # 2. Extract the articles array
        articles = data.get("articles", [])

        # 3. Format them preciselyinto standard structured dictionaries for main.py
        news_list = []
        for index, art in enumerate(articles[:10], 1):  # Grab top 10 items
            if art.get("title"):
                clean_story = {
                    "number": index,
                    "title": art.get("title"),
                    "link": art.get("url", "No link available")
                }
                news_list.append(clean_story)

        return news_list

    except Exception as e:
        print(f"News Fetcher Error: {e}")
        return []            
   