import requests
import os
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin


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

def download_image(url , folder = 'images/'):
    path = os.getcwd()
    os.makedirs(os.path.join(path, folder), exist_ok=True)
    filename = url.split('/')[-1]
    filepath = os.path.join(folder, filename)
    response = get_response(url).content
    with open(filepath, 'wb') as f:
        f.write(response)
    print(filename)





def main():
    for number in range(1,11):
        url = f'http://tululu.org/b{number}/'
        response = get_response(url)
        if url == response.url:
            response_text = response.text
            soup = BeautifulSoup(response_text, 'lxml')
            header = soup.find('div', id='content').find('h1').text
            header = header.split('::')
            book_title = header[0].strip()
            book_author = header[1].strip()
            link_img_find = soup.find('div', {'class': 'bookimage'}).find('img')['src']
            book_url_find = f'/txt.php?id={number}'
            if soup.find('a', href=book_url_find):
                # print('Заголовок: ', book_title)
                # print(urljoin('http://tululu.org', link_img_find), end='\n\n')
                book_url = urljoin('http://tululu.org', book_url_find)
                img_url = urljoin('http://tululu.org', link_img_find)
                download_image(img_url)
                # download_txt(book_url, book_title,)








if __name__ == '__main__':
    main()
