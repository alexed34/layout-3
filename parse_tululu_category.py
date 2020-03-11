import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def page(number):
    response = requests.get(f'http://tululu.org/l55/{number}/')
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    text_cards = soup.find_all('table', class_='d_book')
    for card in text_cards:
        link = card.find('a')['href']

        link = urljoin('http://tululu.org/', link)
        print(link)

for number in range(1,11):
    page(number)