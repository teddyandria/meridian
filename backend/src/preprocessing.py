#nettoyage léger (HTML résiduel, doublons, articles vides ou tronqués)

# plain gratuit de NewsAPi limité à 200 carac environ, donc je dois tronqué.

import json
from pathlib import Path

def missing_data(news):
    articles = news["articles"]

    articles_clean = [] 

    for article in articles:
        description = article["description"]

        if description:
            articles_clean.append(article)
        else:
            print("paaaaas de descriptiiiiioon")
    print(len(articles_clean))
    return articles_clean


def main():
    base = Path(__file__).resolve().parent.parent
    news_path = base / "data" / "news.json"
    with open(news_path , "r", encoding='utf-8') as f:
        news = json.load(f)

    missing = missing_data(news)

if __name__ == "__main__":
    main()