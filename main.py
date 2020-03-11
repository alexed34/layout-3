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

def download_comments(soup):
    comments = soup.find_all('div', {'class' :'texts'})
    for comment in comments:
        text = comment.find('span', {'class' :'black'}).text
        print(text)

def download_genre(soup):
    genres = soup.find('span', class_='d_book').find_all('a')
    genre = [genre.text for genre in genres]
    print(genre)




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
            img_url = urljoin('http://tululu.org', link_img_find)
            book_url = urljoin('http://tululu.org', f'/txt.php?id={number}')
            print('Заголовок: ',book_title)
            download_genre(soup)
            #download_comments(soup)
            print(end='\n\n')


            # download_image(img_url)
            # download_txt(book_url, book_title,)

            # if soup.find('a', href=book_url_find): если есть ссылка на скачивание книги









if __name__ == '__main__':
    main()
