from decimal import Decimal


def to_decimal(num) -> Decimal:
    return round(Decimal(num), 2)


def clean_td(td):
    return str(td).replace('<td>', '').replace('</td>', '')
