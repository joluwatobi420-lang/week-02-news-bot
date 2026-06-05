import xml.etree.ElementTree as ET
import requests

def fetch_general_news():
    """
    Fetches top headlines across International, Tech, and Nigerian sources.
     using free public RSS feeds.
    """
    # Defien your source mix map
    feeds = {
        "International (BBC)": "http://feeds.bbci.co.uk/news/world/rss.xml",
        "Tech (TechCrunch)": "https://techcrunch.com/feed/",
        "Nigerian/African (Premium Times)": "https://www.premiumtimesng.com/feed",
    }

    combined_news = []
    global_counter = 1

    for source_name, url in feeds.items():
        print(f"Pulling from {source_name}...")
        try:
            response = requests.get(url, timeout=10, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            })
            response.raise_for_status()

            root = ET.fromstring(response.content)
            items = root.findall(".//item")

            # Grab the top 3 frehest stories per source to keep the bundle tight
            for item in items[:3]:
                title = item.find("title")
                link = item.find("link")

                if title is not None:
                    clean_story = {
                        "number": global_counter,
                        "source": source_name,
                        "title": f"[{source_name}] {title.text.strip()}",
                        "link": link.text.strip() if link is not None else "No link",
                    }
                    combined_news.append(clean_story)
                    global_counter +=1

        except Exception as e:
            print(f"Failed to pull from {source_name}: {e}")

    return combined_news                   