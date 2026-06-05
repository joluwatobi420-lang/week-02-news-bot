import requests

def generate_ai_brief(raw_stories, groq_api_key):
    """ 
    Takes the multi-source stories list, builds a formattted text block,
    and uses Groq's Llama-3 model to structure a stylized news brief.
    """
    if not raw_stories or not groq_api_key:
        print("Missing stories or Grpq API Key!")
        return None
    
    # 1. Format the raw incoming articles into a text block for the prompt
    article_text = ""
    for story in raw_stories:
        article_text += f"Title: {story.get('title')}\nLink: {story.get('link')}\n\n"

    # 2. Setup the target endpoint URL and headers
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {groq_api_key}",
        "Content-Type": "application/json"
    }
    
    # 3. Setup the payload structure with ourclean multi-line system prompt
    payload = {
        "model": "llama-3-8b-8192",
        "messages": [
            {
                "role": "system",
                "content": "You are a tech news aggregator. Summarize the following news stories into a single, highly engaging daily brief matching a professional tech analyst tone."
            },
            {
                "role": "user",
                "content": f"Here is the multi-source breakdown:\n\n{article_text}"
            }
        ],
        "temperature": 0.7
    }

    # 4. Make the secure request to Groq's API
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]

    except Exception as e:
        print(f"Groq API Error: {e}")
        return None

    
    
    
    
    
    
