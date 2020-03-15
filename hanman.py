import requests
from bs4 import BeautifulSoup
import shutil
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0'
}
proxies = {
    'http': 'socks5://192.168.2.105:10808',
    'https': 'socks5://192.168.2.105:10808'
}


def get_img_list(url):
    web_data = requests.get(url, headers=headers, proxies=proxies).content.decode('utf-8')
    print('web_data got.')
    soup = BeautifulSoup(web_data, 'lxml')
    print('soup completed.')
    img_area = soup.find_all(name='img', attrs={'class': 'lazy img-responsive'})
    url_list = []
    for img in img_area:
        img_link = 'http://www.no-banana.com' + img['data-src']
        # print(img_link)
        # print('********')
        url_list.append(img_link)
    return url_list


def download(url, filename):
    full_filename = filename + '.jpg'
    r = requests.get(url, stream=True, headers=headers, proxies=proxies)
    with open(full_filename, 'wb') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)
    print('%s saved.' % filename)
    print('%s size is %d' % (filename, os.path.getsize(full_filename)))


if __name__ == '__main__':
    url = 'http://www.no-banana.com/chapter/25338'
    print('starting...')
    img_list = get_img_list(url)
    print('img list got.')
    number = 1
    for img in img_list:
        download(img, 'test-' + str(number).zfill(3))
        number = number + 1
