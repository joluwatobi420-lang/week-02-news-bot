import requests
import json
def generate_ai_brief(raw_stories, groq_api_key):
    """
    Takes the multi-source stories list, formats them, and calls Groq's API
    via raw requests to generate a styled news briefing.
    """
    if not raw_stories or not groq_api_key:
        print(" Missing stories or Groq API Key!")
        return None
    
    # 1. Loop through your raw stories and format them into a single string
    article_text = ""
    for story in raw_stories:
        title = story.get('title', 'No Title')
        link = story.get('link', 'No Link')
        article_text += f"Title: {title}\nLink: {link}\n\n"

      # 2. Setup your raw requests parameters exactly as specified
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {groq_api_key}",
        "Content-Type": "application/json" # Fixed the missing quote here
    }

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are an elite, multi-domain news editor. Structure today's "
                    "briefing into distinct, stylized categories based on the articles "
                    "provided (e.g., Global Affairs, Tech & Innovations, African Markets "
                    "& Perspectives). Keep the brief engaging, punchy, and professional."
                )
            },
            {
                "role": "user",
                "content": f"Here is the multi-source breakdown:\n\n{article_text}"
            }
        ],
        "temperature": 0.7
    }

    # 3. Fire the POST request to Groq
    print("Sending data to Groq AI Engine for styling...")
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        
        # Parse the JSON response        
        result = response.json()
        return result["choices"][0]["message"]["content"]
    
    except Exception as e:
        print(f" Groq API Error: {e}")
        if 'response' in locals() and response is not None:
            print(f"Details from Groq: {response.text}")
        return None

