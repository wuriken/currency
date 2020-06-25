from decimal import Decimal


def to_decimal(num) -> Decimal:
    return round(Decimal(num), 2)


def clean_td(td):
    return str(td).replace('<td>', '').replace('</td>', '')


def display(rate, attr):
    display_attr = f'get_{attr}_display'
    if hasattr(rate, display_attr):
        return getattr(rate, display_attr)()
    return getattr(rate, attr)
