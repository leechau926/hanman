import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0'
}

url = 'http://www.no-banana.com/chapter/25337'
# url = 'http://www.baidu.com'
print('requesting')
web_data = requests.get(url, headers=headers).content.decode('utf-8')
print('souping')
soup = BeautifulSoup(web_data, 'lxml')
with open('1.html', 'w', encoding='utf-8') as f:
    f.write(soup.prettify())
print('1.html saved.')
