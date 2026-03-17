import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("NEWS_API_KEY")

def verify_news(query):

    if not API_KEY:
        return False, []

    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={API_KEY}"

    try:
        response = requests.get(url)
        data = response.json()

        if data.get("totalResults", 0) > 0:
            return True, data.get("articles", [])[:3]
        else:
            return False, []

    except Exception as e:
        print("Error:", e)
        return False, []