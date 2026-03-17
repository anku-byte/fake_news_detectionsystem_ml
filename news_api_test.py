import requests
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Get API key safely
API_KEY = os.getenv("NEWS_API_KEY")

query = "India election"

url = f"https://newsapi.org/v2/everything?q={query}&apiKey={API_KEY}"

response = requests.get(url)

data = response.json()

print("Total articles:", data["totalResults"])

for article in data["articles"][:5]:
    print(article["title"])
    print(article["source"]["name"])
    print(article["url"])
    print()