import math

from pandas import DataFrame, Series


def as_percentage(value: str):
    return f"{value:.2f}%"


def as_currency(value: str):
    return f"£{value:,.2f}"


def as_number(value: str):
    return f"{value:,.8f}"


def calculate_max_width(df: DataFrame, col: str):
    if col == 'Qty':
        return df[col].apply(lambda x: len(as_number(x))).max()
    if col in ['Cost', 'Proceeds', 'Gain/Loss']:
        return df[col].apply(lambda x: len(as_currency(x))).max()
    if col == 'Gain/Loss %':
        return df[col].apply(lambda x: len(as_percentage(x))).max()
    return df[col].astype(str).str.len().max()


def calculate_value(row: Series, col: str):
    if col == 'Qty':
        return as_number(row[col])
    if col in ['Cost', 'Proceeds', 'Gain/Loss']:
        if math.isnan(row[col]):
            return ''
        return as_currency(row[col])
    if col == 'Gain/Loss %':
        return as_percentage(row[col])
    return str(row[col])
