import os
import xml.etree.ElementTree as ET
import requests
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables from your saved .env file
load_dotenv()

# Connect securely to your live Supabase cloud instance
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def fetch_general_news():
    """
    Fetches top headlines across International, Tech, and Nigerian sources
    using free public RSS feeds.
    """
    # Define your source mix map
    feeds = {
        "International (BBC)": "http://feeds.bbci.co.uk/news/world/rss.xml",
        "Tech (TechCrunch)": "https://techcrunch.com/feed/",
        "Nigerian/African (Premium Times)": "https://www.premiumtimesng.com/feed"
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
            
            # Parse the XML RSS response content
            root = ET.fromstring(response.content)
            
            # Loop through individual articles in the feed channel
            for item in root.findall(".//item")[:5]: # Grabbing top 5 per feed source
                title = item.find("title").text if item.find("title") is not None else "No Title"
                link = item.find("link").text if item.find("link") is not None else ""
                description = item.find("description").text if item.find("description") is not None else ""
                
                # Verify against cloud memory before adding to the dispatch batch
                if link and is_article_new(link):
                    combined_news.append({
                        "id": global_counter,
                        "source": source_name,
                        "title": title,
                        "link": link,
                        "description": description
                    })
                    global_counter += 1
                    
        except Exception as e:
            print(f"Error reading from {source_name}: {e}")
            
    return combined_news

def is_article_new(url: str) -> bool:
    """Checks the cloud database to see if an article url has already been processed."""
    try:
        response = supabase.table("processed_articles").select("article_url").eq("article_url", url).execute()
        if len(response.data) == 0:
            return True
        return False
    except Exception as e:
        print(f"Cloud database read error: {e}")
        return True # Fallback so your pipeline keeps moving

def mark_article_as_seen(url: str):
    """Saves a newly broadcasted article URL to the cloud database table."""
    try:
        supabase.table("processed_articles").insert({"article_url": url}).execute()
        print(f"Successfully saved article to cloud memory: {url}")
    except Exception as e:
        print(f"Cloud database write error: {e}")

          