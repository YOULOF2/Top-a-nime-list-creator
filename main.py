import csv
from time import sleep

from bs4 import BeautifulSoup
from requests_html import HTMLSession
from tqdm.contrib import tzip

URL = "https://myanimelist.net/topanime.php"
CSV_FILE_NAME = "top_anime.csv"
COLUMN_NAMES = ["title", "rating", "link"]


def main():
    session = HTMLSession()
    website_obj = session.get(URL)

    soup = BeautifulSoup(website_obj.content, 'html.parser')

    all_titles = soup.find_all("h3", class_="anime_ranking_h3")
    all_ratings = soup.find_all("td", class_="score")
    all_ratings.pop(0)

    data_list = []

    for title_element, rating_element in tzip(all_titles, all_ratings):
        title_text = title_element.text
        element_link = title_element.find("a", href=True)["href"]
        rating_text = rating_element.find("span", class_="score-label").text

        data_list.append(
            {
                "title": title_text,
                "link": element_link,
                "rating": rating_text,
            }
        )
        sleep(0.1)

    with open(CSV_FILE_NAME, 'w') as file:
        writer = csv.DictWriter(file, fieldnames=COLUMN_NAMES)
        writer.writeheader()
        for row_data in data_list:
            writer.writerow(row_data)


if __name__ == "__main__":
    main()
