import requests
import os
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin
import json
import argparse
import time
import progressbar


def get_response(url):
    response = requests.get(url)
    response.raise_for_status()
    return response


def download_txt(url, filename, path, folder='books'):
    os.makedirs(os.path.join(path, folder), exist_ok=True)
    filename = sanitize_filename(filename)
    filepath = os.path.join(os.path.join(path, folder), f'{filename}.txt')
    r = get_response(url)
    if url == r.url:
        response = r.text
        with open(os.path.join(path, filepath), 'w', encoding='utf-8') as f:
            f.write(response)
        return filepath


def download_image(url, path, folder='images'):
    os.makedirs(os.path.join(path, folder), exist_ok=True)
    filename = url.split('/')[-1]
    filepath = os.path.join(os.path.join(path, folder), filename)
    response = get_response(url).content
    with open(filepath, 'wb') as f:
        f.write(response)
    return filepath


def download_comments(soup):
    comments_soup = soup.select('div.texts')
    comments = [comment.select_one('span.black').text for comment in comments_soup]
    return comments


def download_genre(soup):
    genres_soup = soup.select('span.d_book a')
    genres = [genre.text for genre in genres_soup]
    return genres


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-sp', '--start_page', type=int)
    end_pages = 702
    parser.add_argument('-ep', '--end_page', type=int, default=end_pages)
    parser.add_argument('-df', '--dest_folder', default='D:\\books')
    parser.add_argument('-si', '--skip_imgs', action='store_const', const=True)
    parser.add_argument('-st', '--skip_txt', action='store_const', const=True)
    parser.add_argument('-jp', '--json_path', )
    return parser


def main():
    json_data = []
    parser = create_parser()
    namespace = parser.parse_args()
    os.makedirs(namespace.dest_folder, exist_ok=True)
    path = namespace.dest_folder

    for number in range(namespace.start_page, namespace.end_page):
        url = f'http://tululu.org/l55/{number}/'
        response = get_response(url)
        soup = BeautifulSoup(response.text, 'lxml')
        text_cards = soup.select('table.d_book')
        for card in text_cards:
            base_url = response.url
            link = card.select_one('a')['href']
            link_book = urljoin(base_url, link)
            r = get_response(link_book)
            response_text = r.text
            soup = BeautifulSoup(response_text, 'lxml')
            header = soup.select_one('div#content h1').text
            header = header.split('::')
            title = header[0].strip()
            author = header[1].strip()
            img_src = None
            if not namespace.skip_imgs:
                img_src_soup = soup.select_one('div.bookimage img')['src']
                img_url = urljoin(base_url, img_src_soup)
                img_src = download_image(img_url, path)
            book_path = None
            if not namespace.skip_txt:
                number = link.split('b')[1]
                book_url = urljoin('http://tululu.org', f'/txt.php?id={number}')
                book_path = download_txt(book_url, title, path)
            comments = download_comments(soup)
            genres = download_genre(soup)
            data = {
                "title": title,
                "author": author,
                "img_src": img_src,
                "book_path": book_path,
                "comments": comments,
                "genres": genres,
            }
            json_data.append(data)

    if namespace.json_path:
        great_folder(namespace.json_path)
        path = namespace.json_path

    with open(os.path.join(path, 'data.json'), 'w', encoding='utf8') as f:
        json.dump(json_data, f, ensure_ascii=False)


if __name__ == '__main__':
    main()
