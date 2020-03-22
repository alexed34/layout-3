import requests
import os
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin
import json



def get_response(url):
    response = requests.get(url)
    response.raise_for_status()
    return response


def great_folder(folder):
    path = os.getcwd()
    os.makedirs(path + folder, exist_ok=True)


def download_txt(url , filename , folder = 'books/'):
    path = os.getcwd()
    os.makedirs(os.path.join(path, folder), exist_ok=True)
    filename = sanitize_filename(filename)
    filepath = os.path.join(folder, f'{filename}.txt')
    if url == get_response(url).url:
        response = get_response(url).text
        with open(filepath, 'w') as f:
            f.write(response)
        return filepath
    else:
        return 'Нет книги'

def download_image(url , folder = 'images/'):
    path = os.getcwd()
    os.makedirs(os.path.join(path, folder), exist_ok=True)
    filename = url.split('/')[-1]
    filepath = os.path.join(folder, filename)
    response = get_response(url).content
    with open(filepath, 'wb') as f:
        f.write(response)
    return filepath

def download_comments(soup):
    comments_soup = soup.find_all('div', {'class' :'texts'})
    comments = [comment.find('span', {'class' :'black'}).text for comment in comments_soup]
    return comments

def download_genre(soup):
    genres_soup = soup.find('span', class_='d_book').find_all('a')
    genres = [genre.text for genre in genres_soup]
    return genres

def page(number):
    response = requests.get(f'http://tululu.org/l55/{number}/')
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    text_cards = soup.find_all('table', class_='d_book')
    for card in text_cards:
        link = card.find('a')['href']

        link = urljoin('http://tululu.org/', link)
        print(link)


def main():
    json_books = []
    for number in range(1,5):
        url = f'http://tululu.org/l55/{number}/'
        response = get_response(url)
        soup = BeautifulSoup(response.text, 'lxml')
        text_cards = soup.find_all('table', class_='d_book')
        for card in text_cards:
            link = card.find('a')['href']
            link_book = urljoin('http://tululu.org/', link)
            r = get_response(link_book)
            response_text = r.text
            soup = BeautifulSoup(response_text, 'lxml')
            header = soup.find('div', id='content').find('h1').text
            header = header.split('::')
            title = header[0].strip()
            author = header[1].strip()
            img_src_soup = soup.find('div', {'class': 'bookimage'}).find('img')['src']
            img_url = urljoin('http://tululu.org', img_src_soup)
            img_src = download_image(img_url)
            book_url = urljoin('http://tululu.org', f'/txt.php?id={number}')
            book_path = download_txt(book_url, title)
            comments = download_comments(soup)
            genres = download_genre(soup)
            data = {"title": title,
                    "author": author,
                    "img_src": img_src,
                    "book_path": book_path,
                    "comments": comments,
                    "genres": genres
                    }
            json_books.append(data)

    with open('data.json', 'w', encoding='utf8') as f:
        json.dump(json_books, f, ensure_ascii=False)














if __name__ == '__main__':
    main()
