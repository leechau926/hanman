import requests
from bs4 import BeautifulSoup
import shutil
import os
import time
from multiprocessing import Pool

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0'
}
proxies = {
    'http': 'socks5://192.168.131.1:10808',
    'https': 'socks5://192.168.131.1:10808'
}
http_prefix = 'http://www.no-banana.com'


def get_chapter_dict_list(book_url):
    web_data = requests.get(book_url, headers=headers, proxies=proxies).content.decode('utf-8')
    soup = BeautifulSoup(web_data, 'lxml')
    book_title = soup.find(name='h1').get_text().strip()
    chapterlistload = soup.find(attrs={'id': 'chapterlistload'})
    chapter_area = chapterlistload.find_all(attrs={'rel': 'nofollow'})
    chapter_dict_list = []
    for chapter in chapter_area:
        url = http_prefix + chapter['href']
        name = chapter.get_text().strip()
        chapter_dict = {'chapter_name': name, 'chapter_url': url}
        chapter_dict_list.append(chapter_dict)
    chapter_dict_list.pop()
    return chapter_dict_list


def get_img_list(chapter_url):
    web_data = requests.get(chapter_url, headers=headers, proxies=proxies).content.decode('utf-8')
    print('web_data got.')
    soup = BeautifulSoup(web_data, 'lxml')
    print('soup completed.')
    img_area = soup.find_all(name='img', attrs={'class': 'lazy img-responsive'})
    img_list = []
    for img in img_area:
        img_link = 'http://www.no-banana.com' + img['data-src']
        # print(img_link)
        # print('********')
        img_list.append(img_link)
    return img_list


def download_response(url, full_filename):
    r = requests.get(url, stream=True, headers=headers, proxies=proxies)
    with open(full_filename, 'wb') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)


def download(url, filename):
    full_filename = filename + '.jpg'
    download_response(url, full_filename)
    while (os.path.getsize(full_filename) < 201):
        download_response(url, full_filename)
    print('%s saved.' % filename)
    print('%s size is %d' % (filename, os.path.getsize(full_filename)))


def download_imgs(img_list, fileprefix):
    number = 1
    for img in img_list:
        download(img, fileprefix + str(number).zfill(2))
        number = number + 1
        #time.sleep(interval)


def main(chapter_dict):
    print('**** %s START' % chapter_dict['chapter_name'])
    img_list = get_img_list(chapter_dict['chapter_url'])
    download_imgs(img_list, chapter_dict['chapter_name'])
    print('**** %s COMPLETE' % chapter_dict['chapter_name'])


if __name__ == '__main__':
    book_url = 'http://www.no-banana.com/book/618'
    chapter_dict_list = get_chapter_dict_list(book_url)
    pool = Pool(4)
    for chapter_dict in chapter_dict_list:
        pool.apply_async(main,(chapter_dict,))
    pool.close()
    pool.join()
    
