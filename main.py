import requests
import os
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


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
    response = get_response(url).text
    with open(filepath, 'w') as f:
        f.write(response)
    return filepath




def main():
    for number in range(1,3):
        url = f'http://tululu.org/b{number}/'
        response = get_response(url)
        if url == response.url:
            response_text = response.text
            soup = BeautifulSoup(response_text, 'lxml')
            header = soup.find('div', id='content').find('h1').text
            header = header.split('::')
            book_title = header[0].strip()
            book_author = header[1].strip()
            book_url_find = f'/txt.php?id={number}'
            if soup.find('a', href=book_url_find):
                book_url = f'http://tululu.org{book_url_find}'
                download_txt(book_url, book_title,)








if __name__ == '__main__':
    main()