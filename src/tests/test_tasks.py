import os

from django.conf import settings

from rate.models import Rate
from rate.tasks import parse_monobank, parse_nationalbank, parse_privatbank, parse_pumb, parse_vkurse


class Response:
    pass


def test_privat(mocker):
    def mock():
        res = [
            {
                "ccy": "RUR",
                "base_ccy": "UAH",
                "buy": "0.28000",
                "sale": "0.32000"
            },
            {
                "ccy": "EUR",
                "base_ccy": "UAH",
                "buy": "19.20000",
                "sale": "20.00000"
            },
            {
                "ccy": "USD",
                "base_ccy": "UAH",
                "buy": "15.50000",
                "sale": "15.85000"
            }
        ]
        response = Response()
        response.json = lambda: res
        return response

    requests_get_patcher = mocker.patch('requests.get')
    requests_get_patcher.return_value = mock()
    rate_initial_count = Rate.objects.count()
    parse_privatbank()
    assert Rate.objects.count() == rate_initial_count + 4
    parse_privatbank()
    assert Rate.objects.count() == rate_initial_count + 4


def test_mono(mocker):
    def mock():
        res = [
            {
                "currencyCodeA": 840,
                "currencyCodeB": 980,
                "date": 1596834607,
                "rateBuy": 27.55,
                "rateSell": 27.8552
            },
            {
                "currencyCodeA": 978,
                "currencyCodeB": 980,
                "date": 1596834607,
                "rateBuy": 32.3,
                "rateSell": 32.7869
            },
            {
                "currencyCodeA": 643,
                "currencyCodeB": 980,
                "date": 1596834607,
                "rateBuy": 0.36,
                "rateSell": 0.385
            }
        ]
        response = Response()
        response.json = lambda: res
        return response

    requests_get_patcher = mocker.patch('requests.get')
    requests_get_patcher.return_value = mock()
    rate_initial_count = Rate.objects.count()
    parse_monobank()
    assert Rate.objects.count() == rate_initial_count + 4
    parse_monobank()
    assert Rate.objects.count() == rate_initial_count + 4


def test_vkurse(mocker):
    def mock():
        res = {"Dollar": {
                "buy": "27.55",
                "sale": "27.75"
            },
            "Euro":
                {
                    "buy": "32.40",
                    "sale": "32.60"
                },
            "Rub":
                {
                    "buy": "0.375",
                    "sale": "0.380"
                }
        }
        response = Response()
        response.json = lambda: res
        return response

    requests_get_patcher = mocker.patch('requests.get')
    requests_get_patcher.return_value = mock()
    rate_initial_count = Rate.objects.count()
    parse_vkurse()
    assert Rate.objects.count() == rate_initial_count + 4
    parse_vkurse()
    assert Rate.objects.count() == rate_initial_count + 4


def test_national(mocker):
    def mock():
        res = [
            {
                "r030": 840,
                "txt": "Долар США",
                "rate": 27.6486,
                "cc": "USD",
                "exchangedate": "10.08.2020"
            },
            {
                "r030": 643,
                "txt": "Російський рубль",
                "rate": 0.37553,
                "cc": "RUB",
                "exchangedate": "10.08.2020"
            },
            {
                "r030": 978,
                "txt": "Євро",
                "rate": 32.6848,
                "cc": "EUR",
                "exchangedate": "10.08.2020"
            }
        ]
        response = Response()
        response.json = lambda: res
        return response

    requests_get_patcher = mocker.patch('requests.get')
    requests_get_patcher.return_value = mock()
    parse_nationalbank()


def test_pumb(mocker):
    def mock():
        path = os.path.join(settings.BASE_DIR, 'tests', 'html', 'pumb.html')
        with open(path, encoding="UTF-8") as file:
            content = file.read()

        response = Response()
        response.status_code = 200
        response.text = content
        return response

    requests_get_patcher = mocker.patch('requests.get')
    requests_get_patcher.return_value = mock()
    parse_pumb()
