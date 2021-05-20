from bs4 import BeautifulSoup
import requests
from sqlalchemy.dialects.postgresql import insert
# from lxml.html import fromstring as lxml_fromstring
# from lxml.html.clean import Cleaner

from models import User, UserSubscription, Event
from database import session
# from bot_object import bot

# cleaner = Cleaner(style=True)

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
            parse_events(html.text)
        elif html.status_code == 404:
            break
        else:
            print(f'error: parser - status_code: {html.status_code}')
        page = page + 1


def parse_events(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('article', class_='b-postcard')
    
    events = []
    for item in items:
        url = item.find('h2', class_='title')
        id_site = str(url.find('a').get('href')).split('/')[4]
        name = item.find('a').get_text().rstrip().lstrip()
        # cleaned_ = cleaner.clean_html(lxml_fromstring(name))
        # name = cleaned_.text_content()

        date = item.find('span', class_='date').get_text()
        block = item.find('div', class_='when-and-where')
        if len(block.find_all('span')) == 2:
            price = block.find_all('span')[1].get_text().rstrip().lstrip()
        else:
            price = ''
        event_type = block.get_text().replace(date, '').replace(price, '').rstrip().lstrip()
        description = item.find('p', class_='b-typo').get_text().rstrip().lstrip()

        block = item.find('div', class_='more')
        if block.find('span') is not None:
            tags = block.get_text().replace(block.find('span').get_text(), '').rstrip().lstrip()
        else:
            tags = block.get_text().rstrip().lstrip()

        tags = str(tags).split(', ')
        event_type = str(event_type).split(', ')

        events.append(
            {
                'id_site': id_site, 
                'name': name, 
                'date': date, 
                'price': price, 
                'type': event_type,
                'description': description, 
                'tags': tags
            })
        
    session.execute(insert(Event).values(events).on_conflict_do_nothing())
    session.commit()


parser(URL)


def delete_event():
    events = session.query(Event).all()
    for event in events:
        html = get_html(URL+str(event.id_site))
        if html.status_code == 404:
            print(f'delete event: {event.id_site}')
            session.delete(event)


# delete_event()

