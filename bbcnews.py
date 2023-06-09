import requests
import json
import os
from bs4 import BeautifulSoup

def scrape_bbc_articles(section):
    url = f"https://www.bbc.com/news/{section}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    articles = soup.find_all("article")

    downloaded_articles = get_downloaded_articles(section)

    for article in articles:
        title_element = article.find("h3")
        body_element = article.find("p")

        if title_element and body_element:
            title = title_element.text.strip()
            body = body_element.text.strip()

            remove_elements = article.find_all(
                ["figure", "a", "script", "style", "noscript", "video"]
            )
            for element in remove_elements:
                element.extract()

            article_data = {"title": title, "body": body}
            filename = f"{section}_{title}.json".replace("/", "-")

            if filename not in downloaded_articles:
                with open(filename, "w") as file:
                    json.dump(article_data, file, indent=4)
                downloaded_articles.append(filename)

    update_downloaded_articles(section, downloaded_articles)


def get_downloaded_articles(section):
    filename = f"downloaded_{section}_articles.txt"
    if os.path.exists(filename):
        with open(filename, "r") as file:
            return [line.strip() for line in file.readlines()]
    return []


def update_downloaded_articles(section, articles):
    filename = f"downloaded_{section}_articles.txt"
    with open(filename, "w") as file:
        file.write("\n".join(articles))


scrape_bbc_articles("business")
scrape_bbc_articles("technology")