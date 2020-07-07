import datetime

from django.core.management import BaseCommand

from rate import model_choices as mch
from rate.models import Rate

import requests


class Command(BaseCommand):
    help = 'Generate rates with param'  # noqa builtin name from python
    BASE_URL = 'https://api.privatbank.ua/p24api/exchange_rates'

    def get_rates_from_json(self, json_str):
        date_time = datetime.datetime.strptime(json_str['date'], '%d.%m.%Y')
        for item in json_str['exchangeRate']:
            if item.get('currency'):
                if 'EUR' in item['currency']:
                    rate_buy = Rate.objects.create(source=mch.SOURCE_PRIVATBANK, currency_type=mch.CURRENCY_TYPE_EUR, type=mch.RATE_TYPE_SALE, amount=item['purchaseRate'])
                    rate_buy.created = date_time
                    rate_buy.save()
                    rate_sale = Rate.objects.create(source=mch.SOURCE_PRIVATBANK, currency_type=mch.CURRENCY_TYPE_EUR, type=mch.RATE_TYPE_BUY, amount=item['saleRate'])
                    rate_sale.created = date_time
                    rate_sale.save()
                if 'USD' in item['currency']:
                    rate_buy = Rate.objects.create(source=mch.SOURCE_PRIVATBANK, currency_type=mch.CURRENCY_TYPE_USD, type=mch.RATE_TYPE_SALE, amount=item['purchaseRate'])
                    rate_buy.created = date_time
                    rate_buy.save()
                    rate_sale = Rate.objects.create(source=mch.SOURCE_PRIVATBANK, currency_type=mch.CURRENCY_TYPE_USD, type=mch.RATE_TYPE_BUY, amount=item['saleRate'])
                    rate_sale.created = date_time
                    rate_sale.save()

    def add_arguments(self, parser):
        parser.add_argument('-c', '--count', type=str, help='Create rates count',)  # noqa

    def handle(self, *args, **options):
        count = 5
        if options.get('count'):
            if options.get('count').isdigit():
                count = int(options.get('count'))
        date_now = datetime.datetime.now()

        date_from = date_now - datetime.timedelta(days=count)
        while date_from.day != date_now.day & date_from.month != date_now.month & date_from.year != date_now.year:
            response = requests.get(self.__class__.BASE_URL,
                                    params={'json': '', 'date': date_from.strftime('%d.%m.%Y')})
            date_from = date_from + datetime.timedelta(days=1)
            if response.status_code == 200:
                self.get_rates_from_json(response.json())
