from pathlib import Path

import pandas as pd

from pandas import DataFrame


def rename_columns(df: DataFrame):
    df.rename(columns={'Gain / loss': 'Gain/Loss', 'Cost (GBP)': 'Cost', 'Proceeds (GBP)': 'Proceeds', 'Amount': 'Qty'},
              inplace=True)


def convert_datetime_columns(df: DataFrame):
    for col in ['Date Sold', 'Date Acquired']:
        date_series = pd.to_datetime(df[col], format='%d/%m/%Y %H:%M', errors='coerce')
        if not date_series.isna().all():
            df[col] = date_series.dt.date.fillna('')
        else:
            df[col] = date_series.fillna('')


def convert_numeric_columns(df: DataFrame):
    numeric_columns = ['Qty', 'Cost', 'Proceeds', 'Gain/Loss']
    df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')


class TransactionLoader:

    @staticmethod
    def load_data(file_name=None):
        df = pd.read_csv(Path(__file__).resolve().parent.parent.parent / "data" / file_name, skiprows=2)
        rename_columns(df)
        convert_datetime_columns(df)
        convert_numeric_columns(df)
        return df
