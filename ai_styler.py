import requests

def generate_ai_brief(raw_stories, groq_api_key):
    if not raw_stories or not groq_api_key:
        return None

    article_text = ""
    for a in raw_stories:
        article_text += f"Title: {a['title']}\nLink: {a['link']}\n\n"

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {groq_api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {
                "role": "system",
                "content": "You are a tech news aggregator. Summarize the following news stories into a single, highly engaging daily brief matching a professional tech analyst tone."
            },
            {
                "role": "user",
                "content": f"Here are today's tech news articles:\n\n{article_text}"
            }
        ],
        "temperature": 0.7
    }

    try:
        # No 'verify=False' here because GitHub's cloud environment has perfect native SSL!
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Groq API Error: {e}")
        return None

    
    
    
    
    
    
