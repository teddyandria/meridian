from dotenv import load_dotenv
import httpx
import os
import json
from pathlib import Path

load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def get_news():
    response = httpx.get(
        "https://newsapi.org/v2/top-headlines",
        params={
            "country": "us",
            "apiKey": NEWS_API_KEY,
        },
    )

    return response.json()

def store_news(news):
    location = Path("backend/data/news.json")
    
    with open(location, "w", encoding="utf-8") as fichier:
        json.dump(news, fichier, ensure_ascii=False, indent=4)

def main():
    news = get_news()
    store_news(news)


if __name__ == "__main__": 
    main()