from bs4 import BeautifulSoup
import logging
import requests

from sqlalchemy.dialects.postgresql import insert

from models import User, UserSubscription, Event
from database import session
from utils import log_time

logger = logging.getLogger(__name__)

URL = 'https://dou.ua/calendar/'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36',
    'accept': '*/*'
}


def get_html(url):
    r = requests.get(url, headers=HEADERS)
    return r


def parser(url=URL):
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
        name = item.find('a').get_text().strip()

        date = item.find('span', class_='date').get_text()
        block = item.find('div', class_='when-and-where')
        if len(block.find_all('span')) == 2:
            price = block.find_all('span')[1].get_text().strip()
        else:
            price = ''
        event_type = block.get_text().replace(date, '').replace(price, '').strip()
        description = item.find('p', class_='b-typo').get_text().strip()

        block = item.find('div', class_='more')
        if block.find('span') is not None:
            tags = block.get_text().replace(block.find('span').get_text(), '').strip()
        else:
            tags = block.get_text().strip()

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


@log_time(logger, 'clearing events table')
def delete_events():
    """
    Clear database from canceled events that no longer exist on the site
    :return: number of deleted events
    """
    i = 0
    events_to_delete = []
    for event in session.query(Event).all():
        html = get_html(URL + str(event.id_site))
        if html.status_code == 404:
            # session.delete(event)
            events_to_delete.append(event.id)
            i += 1

    session.query(Event).filter(
        Event.id.in_(events_to_delete)
    ).delete(synchronize_session=False)

    logger.debug(f'{i} events was deleted from db')

    session.commit()
    return i


# parser(URL)
