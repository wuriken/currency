from bs4 import BeautifulSoup

from fake_useragent import UserAgent

from parse_workua import helper as hlp

import requests

BASE_URL = 'https://www.work.ua/ru/jobs/'
BASE_URL_DETAIL = 'https://www.work.ua'


ua = UserAgent()

page = 0
json_map = ''
while True:
    page += 1
    headers = {'User-Agent': ua.random}

    response = requests.get(BASE_URL, params={'page': page}, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    res = soup.find('div', {'id': 'pjax-job-list'})

    if res is None:
        break

    res = res.find_all('h2')
    for elem in res:
        href = elem.find('a').attrs['href']
        response = requests.get(f'{BASE_URL_DETAIL}{href}')
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        card = soup.find('div', {'class': 'card wordwrap'})
        tmp_tag = soup.find_all('p', {'class': 'text-indent text-muted add-top-sm'})
        firm = ''
        if len(tmp_tag) > 1:
            firm = hlp.clean_html(tmp_tag[1].
                                  find('span', {'class': 'glyphicon glyphicon-company text-black glyphicon-large'}).
                                  parent.__dict__['contents'][3].find('b'))
        else:
            firm = hlp.clean_html(tmp_tag[0].
                                  find('span', {'class': 'glyphicon glyphicon-company text-black glyphicon-large'}).
                                  parent.__dict__['contents'][3].find('b'))
        vacancy = hlp.clean_html(card.find('h1', {'id': 'h1-name'}).__dict__['contents'][0])
        is_hot = card.find('p', {'class': 'cut-bottom-print'})
        job_desc = hlp.clean_html(hlp.get_str_from_list(
            card.find('div', {'id': 'job-description'}).__dict__['contents']))
        addr = hlp.clean_space(soup.find('p', {'class': 'text-indent add-top-sm'}).__dict__['contents'][2])
        hlp.insert_data_into_db(firm, addr, vacancy, job_desc)
    json_map = {'company': '', 'vacancy': '', 'description': '', 'address': ''}
hlp.save_vacancy_to_json(json_map)
