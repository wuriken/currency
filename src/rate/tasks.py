from bs4 import BeautifulSoup

from celery import shared_task

from rate import model_choices as mch
from rate.models import Rate
from rate.utils import clean_td, to_decimal

import requests


@shared_task
def parse_privatbank():
    url = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'
    response = requests.get(url)
    currency_type_mapper = {
        'USD': mch.CURRENCY_TYPE_USD,
        'EUR': mch.CURRENCY_TYPE_EUR,
    }
    for item in response.json():
        if item['ccy'] not in currency_type_mapper:
            continue

        currency_type = currency_type_mapper[item['ccy']]
        amount = to_decimal(item['buy'])

        last = Rate.objects.filter(
            source=mch.SOURCE_PRIVATBANK,
            currency_type=currency_type,
            type=mch.RATE_TYPE_BUY,
        ).last()
        if last is None or last.amount != amount:
            Rate.objects.create(
                amount=amount,
                source=mch.SOURCE_PRIVATBANK,
                currency_type=currency_type,
                type=mch.RATE_TYPE_BUY,
            )

        # sale
        amount = to_decimal(item['sale'])

        last = Rate.objects.filter(
            source=mch.SOURCE_PRIVATBANK,
            currency_type=currency_type,
            type=mch.RATE_TYPE_SALE,
        ).last()
        if last is None or last.amount != amount:
            Rate.objects.create(
                amount=amount,
                source=mch.SOURCE_PRIVATBANK,
                currency_type=currency_type,
                type=mch.RATE_TYPE_SALE,
            )


@shared_task
def parse_monobank():
    url = 'https://api.monobank.ua/bank/currency'
    response = requests.get(url)
    CURRENCY_CODE_UAH = 980
    currency_type_mapper = {
        840: mch.CURRENCY_TYPE_USD,
        978: mch.CURRENCY_TYPE_EUR,
    }
    for item in response.json():
        if item['currencyCodeA'] not in currency_type_mapper:
            continue
        if item['currencyCodeB'] != CURRENCY_CODE_UAH:
            continue
        currency_type = currency_type_mapper[item['currencyCodeA']]
        amount = to_decimal(item['rateBuy'])

        last = Rate.objects.filter(
            source=mch.SOURCE_MONOBANK,
            currency_type=currency_type,
            type=mch.RATE_TYPE_BUY,
        ).last()
        if last is None or last.amount != amount:
            Rate.objects.create(
                amount=amount,
                source=mch.SOURCE_MONOBANK,
                currency_type=currency_type,
                type=mch.RATE_TYPE_BUY,
            )

        # sale
        amount = to_decimal(item['rateSell'])

        last = Rate.objects.filter(
            source=mch.SOURCE_MONOBANK,
            currency_type=currency_type,
            type=mch.RATE_TYPE_SALE,
        ).last()
        if last is None or last.amount != amount:
            Rate.objects.create(
                amount=amount,
                source=mch.SOURCE_MONOBANK,
                currency_type=currency_type,
                type=mch.RATE_TYPE_SALE,
            )


@shared_task
def parse_nationalbank():
    url = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json'
    response = requests.get(url)
    currency_type_mapper = {
        'USD': mch.CURRENCY_TYPE_USD,
        'EUR': mch.CURRENCY_TYPE_EUR,
    }
    for item in response.json():
        if item['cc'] not in currency_type_mapper:
            continue

        currency_type = currency_type_mapper[item['cc']]
        amount = to_decimal(item['rate'])

        last = Rate.objects.filter(
            source=mch.SOURCE_NATIONALBANK,
            currency_type=currency_type,
            type=mch.RATE_TYPE_BUY,
        ).last()
        if last is None or last.amount != amount:
            Rate.objects.create(
                amount=amount,
                source=mch.SOURCE_NATIONALBANK,
                currency_type=currency_type,
                type=mch.RATE_TYPE_BUY,
            )


@shared_task
def parse_vkurse():
    url = 'http://vkurse.dp.ua/course.json'
    response = requests.get(url)
    currency_type_mapper = {
        'Dollar': mch.CURRENCY_TYPE_USD,
        'Euro': mch.CURRENCY_TYPE_EUR,
    }
    for key, value in response.json().items():
        if key not in currency_type_mapper.keys():
            continue

        amount = to_decimal(value['buy'])

        last = Rate.objects.filter(
            source=mch.SOURCE_VKURSE,
            currency_type=currency_type_mapper[key],
            type=mch.RATE_TYPE_BUY,
        ).last()
        if last is None or last.amount != amount:
            Rate.objects.create(
                amount=amount,
                source=mch.SOURCE_VKURSE,
                currency_type=currency_type_mapper[key],
                type=mch.RATE_TYPE_BUY,
            )

        # sale
        amount = to_decimal(value['sale'])

        last = Rate.objects.filter(
            source=mch.SOURCE_VKURSE,
            currency_type=currency_type_mapper[key],
            type=mch.RATE_TYPE_SALE,
        ).last()
        if last is None or last.amount != amount:
            Rate.objects.create(
                amount=amount,
                source=mch.SOURCE_VKURSE,
                currency_type=currency_type_mapper[key],
                type=mch.RATE_TYPE_SALE,
            )


@shared_task
def parse_pumb():
    url = 'https://www.pumb.ua/ru'
    response = requests.get(url)
    currency_type_mapper = {
        'USD': mch.CURRENCY_TYPE_USD,
        'EUR': mch.CURRENCY_TYPE_EUR,
    }
    soup = BeautifulSoup(response.text)
    exchange_rate = soup.find('div', {'class': 'exchange-rate'})
    tr_list = exchange_rate.find('table').findAll('tr')
    for tr in tr_list:
        td_list = tr.findAll('td')
        if len(td_list) > 0:
            if clean_td(td_list[0]) not in currency_type_mapper:
                continue

            amount = to_decimal(clean_td(td_list[1]))

            last = Rate.objects.filter(
                source=mch.SOURCE_PUMB,
                currency_type=currency_type_mapper[clean_td(td_list[0])],
                type=mch.RATE_TYPE_BUY,
            ).last()
            if last is None or last.amount != amount:
                Rate.objects.create(
                    amount=amount,
                    source=mch.SOURCE_PUMB,
                    currency_type=currency_type_mapper[clean_td(td_list[0])],
                    type=mch.RATE_TYPE_BUY,
                )

            # sale
            amount = to_decimal(clean_td(td_list[2]))

            last = Rate.objects.filter(
                source=mch.SOURCE_PUMB,
                currency_type=currency_type_mapper[clean_td(td_list[0])],
                type=mch.RATE_TYPE_SALE,
            ).last()
            if last is None or last.amount != amount:
                Rate.objects.create(
                    amount=amount,
                    source=mch.SOURCE_PUMB,
                    currency_type=currency_type_mapper[clean_td(td_list[0])],
                    type=mch.RATE_TYPE_SALE,
                )
