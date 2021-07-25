from decimal import Decimal


def to_bytes(value) -> bytes:
    return bytes(str(value), 'utf-8')


def format_dai_to_decimals(value: int):
    return format(value / Decimal(10 ** 18), 'f')
