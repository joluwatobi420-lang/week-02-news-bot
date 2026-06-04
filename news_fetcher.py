import json
import subprocess

def fetch_top_tech_news():
    print("Pulling latest tech briefs via System Bridge..." )
    feed_url = "https://api.rss2json.com/v1/api.json?rss_url=https://techcrunch.com/feed/"

    cmd = ["curl", "-s", feed_url]
   
    try:
        result = subprocess.run(cmd, capture_output=True, text=True,check=True)

        if not result.stdout.strip():
            print("Scraper Bridge Error: Recieved empty textresponse from network.")
            return[]

        data = json.loads(result.stdout)

        if data.get("status") == "ok":
            articles = data.get("items", [][:3]) # Grab the top 3 items
            news_list = []

            for index, item in enumerate(articles, 1):
                clean_story = {
                    "number": index,
                    "title": item.get("title"),
                    "link": item.get("link")
                }
                news_list.append(clean_story)
            return news_list
        else:
            print("Scraper Bridge Error: API response status wasn't 'ok'.")
            return []

    except json.JSONDecodeError:
        print("Scraper Bridge Error: Could not parse response. Network might be unstable or blocked.")
        return[]
    except Exception as e:
        print(f"Scraper Bridge Error: {e}")
        return []   