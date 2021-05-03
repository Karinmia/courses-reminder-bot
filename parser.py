import requests
from bs4 import BeautifulSoup

URL = 'https://dou.ua/calendar/'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36',
    'accept': '*/*'
}


def get_html(url):
    r = requests.get(url, headers=HEADERS)
    return r


def parser(url):
    page = 1
    while True:
        html = get_html(f'{url}page-{page}')
        print(f'{url}page-{page}')
        if html.status_code == 200:
            parce_events(html.text)
        elif html.status_code == 404:
            break
        else:
            print(f'error: parser - status_code: {html.status_code}')
        page = page + 1


def parce_events(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('article', class_='b-postcard')
    for item in items:
        name = item.find('a').get_text().rstrip().lstrip()
        date = item.find('span', class_='date').get_text()
        block = item.find('div', class_='when-and-where')
        if len(block.find_all('span')) == 2:
            price = block.find_all('span')[1].get_text().rstrip().lstrip()
        else:
            price = ''
        type = block.get_text().replace(date, '').replace(price, '').rstrip().lstrip()
        description = item.find('p', class_='b-typo').get_text().rstrip().lstrip()
        block = item.find('div', class_='more')
        if block.find('span') is not None:
            tags = block.get_text().replace(block.find('span').get_text(), '').rstrip().lstrip()
        else:
            tags = block.get_text().rstrip().lstrip()
        print(f'name: {name}')
        print(f'date: {date}')
        print(f'price: {price}')
        print(f'type: {type}')
        print(f'description: {description}')
        print(f'tags: {tags}')
        print()



parser(URL)
