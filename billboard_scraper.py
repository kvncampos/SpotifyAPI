from bs4 import BeautifulSoup
import datetime
import requests
from util import timeit


@timeit
def validate_date(date_text: str) -> str:
    """
    User Validation of Correct Format for Billboard Endpoint YYYY-MM-DD.
    :param date_text: User Date: Expected YYYY-MM-DD.
    :return: Validated Date Format: str
    """
    not_validated = True
    while not_validated:
        try:
            datetime.date.fromisoformat(date_text)
            not_validated = False
            return date_text
        except ValueError:
            date_text = input("What Date do you want the Top 100 Songs from? YYYY-MM-DD ")


@timeit
def get_billboard100(date: str) -> list:
    """
    Get Billboards Top 100 Based on date.

    :param date: YYYY-MM-DD
    :return: List of Songs from date
    """
    # Billboard Endpoint for Top 100
    billboard_100 = f'https://www.billboard.com/charts/hot-100/{date}'

    response = requests.get(billboard_100)

    billboard_html = response.text

    soup = BeautifulSoup(billboard_html, 'html.parser')

    chart = soup.find_all(name='div', class_="o-chart-results-list-row-container")
    song_list = [each.h3.string.strip() for each in chart]

    return song_list


def main():
    # Test Functionality
    print("-------------------- TEST...TEST...TEST --------------------")
    print("Running Directly from File.")
    date = validate_date('2005-03-05')
    chart = get_billboard100(date)
    print(chart)


if __name__ == '__main__':
    main()
