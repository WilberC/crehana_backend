from random import randint, uniform
from decimal import Decimal


def random_from_list(options_list, index_start=1):
    return randint(index_start, (len(options_list) - 1))


def random_decimal_number(min_number=1, max_number=100, decimals=2):
    return Decimal(round(uniform(min_number, max_number), decimals))


def random_int(min_number=1, max_number=100):
    return randint(min_number, max_number)
