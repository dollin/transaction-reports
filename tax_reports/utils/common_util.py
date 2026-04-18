import math

import pandas as pd
from pandas import DataFrame, Series
import tax_reports.constants as const


def as_percentage(value: str):
    return f"{value:.2f}%"


def as_currency(value: str):
    return f"£{value:,.2f}"


def as_number(value: str):
    return f"{value:,.8f}"


def calculate_max_width(df: DataFrame, col: str):
    if col == const.QTY:
        return df[col].apply(lambda x: len(as_number(x))).max()
    if col in [const.COST, const.PROCEEDS, const.GAIN_LOSS]:
        return df[col].apply(lambda x: len(as_currency(x))).max()
    if col == const.GAIN_LOSS_PERCENT:
        return df[col].apply(lambda x: len(as_percentage(x))).max()
    return df[col].astype(str).str.len().max()


def calculate_value(row: Series, col: str):
    if col == const.QTY:
        return as_number(row[col])
    if col in [const.COST, const.PROCEEDS, const.GAIN_LOSS]:
        if math.isnan(row[col]):
            return ''
        return as_currency(row[col])
    if col == const.GAIN_LOSS_PERCENT:
        return as_percentage(row[col])
    return str(row[col])


def add_empty_columns(df: DataFrame, columns=None):
    if columns is None:
        return df.copy() # Or df if no modification means no copy needed
    return df.assign(**{col: '' for col in columns})


def convert_datetime_columns(df: DataFrame, columns=None):
    if columns is None:
        return df.copy()
    new_df = df.copy()
    for col in columns:
        # Attempt to convert, coercing errors will result in NaT
        date_series = pd.to_datetime(new_df[col], format='%d/%m/%Y %H:%M', errors='coerce')
        # If all are NaT after coercion (e.g., column was not in datetime format or empty)
        # fill with empty string or keep as NaT if appropriate for downstream.
        # Current logic fills with empty string.
        if not date_series.isna().all():
            new_df[col] = date_series.dt.date.fillna('')
        else:
            # If series was all NaNs/NaTs to begin with, or became all NaTs
            new_df[col] = date_series.fillna('') # Effectively makes it object type with empty strings or NaT
    return new_df


def convert_numeric_columns(df: DataFrame, columns=None):
    if columns is None:
        return df.copy()
    new_df = df.copy()
    new_df[columns] = new_df[columns].apply(pd.to_numeric, errors='coerce')
    return new_df


def filter_by_wallet_prefix(df: DataFrame, column_name: str = const.WALLET_NAME, prefix: str = const.WALLET_PREFIX, exclude_prefix: bool = True) -> DataFrame:
    """
    Filters a DataFrame based on whether a specified column starts with a given prefix.

    Args:
        df: The input DataFrame.
        column_name: The name of the column to filter on.
        prefix: The prefix string to check for.
        exclude_prefix: If True, returns rows where the column does NOT start with the prefix.
                        If False, returns rows where the column DOES start with the prefix.

    Returns:
        A new DataFrame with the filtered rows.
    """
    # Ensure the column exists
    if column_name not in df.columns:
        # Or raise an error, or return df unmodified
        return df

    # Handle NaN values by filling with an empty string for the startswith check
    col_series = df[column_name].fillna('')

    if exclude_prefix:
        return df[~col_series.astype(str).str.startswith(prefix)]
    else:
        return df[col_series.astype(str).str.startswith(prefix)]