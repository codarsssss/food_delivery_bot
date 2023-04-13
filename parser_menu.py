import requests
from bs4 import BeautifulSoup


URL = 'https://kubanskiypovar.ru/'


def get_html(url):
    response = requests.get(url)
    return response


def get_main_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='item x3 md4 sm6 xs12')
    ready_list = []

    for card in items:
        ready_list.append({
            'name': card.find('div', class_='title').get_text(strip=True),
            'description': card.find('div', class_='text').get_text(strip=True).split('Состав:')[1],
            'volume': card.find('div', class_='text').get_text(strip=True).split('Состав')[0],
            'img': 'https://kubanskiypovar.ru' + card.find('img').get('src')
        })
    return ready_list


def get_new_year_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('a', class_='item')
    info = soup.find_all('p')
    des_list = []
    number = 1
    flag = True
    for i in info:
        if i.text.strip().startswith(f'{number}.') or i.text.strip().startswith(f'{number}'):
            if flag:
                flag = False
                continue
            i = i.text.replace('\n', '').replace('\t', '').replace('\xa0', '')
            des_list.append(f'Объём: {i.split("-")[1].strip() if i.split("-")[1].strip() != "деревенски" else i.split("-")[2].strip()}\nСостав: {i.split("Состав:")[1].strip()}')
            number += 1
    ready_list = []
    a = 0
    for card in items:
        ready_list.append({
            'name': card.get('alt'),
            'img': 'https://kubanskiypovar.ru' + card.get('href'),
            'description': des_list[a]
        })
        a += 1
    return ready_list


def get_from_site():
    html = get_html(URL)
    if html.status_code == 200:
        answer = get_main_content(html.text)
        new_year = get_new_year_content(html.text)
        return answer, new_year
    else:
        print('Ошибка! Код:', html.status_code)


