#nettoyage léger (HTML résiduel, doublons, articles vides ou tronqués)

# plan gratuit de NewsAPi limité à 200 carac environ, donc je dois tronqué.

import json
from pathlib import Path
from bs4 import BeautifulSoup
import re

def missing_data(news):
    articles = news["articles"]

    articles_clean = [] 

    for article in articles:
        description = article["description"]
        content = article["content"]

        if not description or not content:
            print("La description ou le contenu est vide.")
            continue 

        articles_clean.append(article)

    # print(len(articles_clean))
    return articles_clean

def remove_html(news)-> list:

    articles_clean = []

    for article in news:
        description = article["description"]
        content = article["content"]

        soup_content = BeautifulSoup(content, "html.parser")
        soup_description = BeautifulSoup(description, "html.parser")

        article["content"] = soup_content.get_text()
        article["description"] = soup_description.get_text()

        articles_clean.append(article)

    return articles_clean

def remove_truncate(news)-> list:
    regex = r"\s*…?\s*\[\+\d+ chars\]\s*$"
    regex_unclosed_balise = r"\s*</?[a-zA-Z][^>]*$"

    articles_clean = []

    for article in news:
        content = article["content"]
        description = article["description"]

        content_char_removed = re.sub(regex, "", content)
        remove_unclosed__content_balise = re.sub(regex_unclosed_balise, "", content_char_removed)

        description_char_removed = re.sub(regex, "", description)
        remove_unclosed_description_balise = re.sub(regex_unclosed_balise, "", description_char_removed)

        article["content"] = " ".join(remove_unclosed__content_balise.split())
        article["description"] = " ".join(remove_unclosed_description_balise.split())

        articles_clean.append(article)
    return articles_clean

def remove_duplication(news)->list:
    articles_clean = []
    urls = set()

    for article in news:
        url = article["url"]

        if url in urls:
            print("url déjà vue")
        else:
            urls.add(url)
            articles_clean.append(article)

    return articles_clean





def main():
    base = Path(__file__).resolve().parent.parent
    news_path = base / "data" / "news.json"
    news_clean_path = base / "data" / "news_clean.json"
    with open(news_path , "r", encoding='utf-8') as f:
        news = json.load(f)


    news_without_empty_values = missing_data(news)
    # print(clean_news)

    html_removed = remove_html(news_without_empty_values)
    # print(len(html_removed))
    # print(html_removed[0])

    char_removed = remove_truncate(html_removed)
    print(char_removed[0]["content"])

    duplicate_removed = remove_duplication(char_removed)

    with open(news_clean_path, "w", encoding="utf-8") as f:
        json.dump(duplicate_removed, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()