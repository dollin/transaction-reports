from tax_reports.utils.common_util import *
from pandas import DataFrame
from pathlib import Path
import pandas as pd


def rename_columns(df: DataFrame):
    df.rename(columns={'Quantity': 'Qty', 'Cost (GBP)': 'Cost', 'Description': 'Wallet Name'},
              inplace=True)


def convert_asset_name(df: DataFrame):
    df['Asset'] = df['Asset'].apply(lambda x: x.strip().split(' ')[0])


def drop_unused_columns_and_rows(df: DataFrame):
    df = df[df['Wallet Name'].str.startswith("@ ")]
    return df.drop(columns=['Value (GBP)'])


class HoldingLoader:

    @staticmethod
    def load_data(file_name=None):
        df = pd.read_csv(Path(__file__).resolve().parent.parent.parent / "data" / file_name, skiprows=2)
        rename_columns(df)
        convert_asset_name(df)
        convert_numeric_columns(df, ['Qty', 'Cost'])
        add_empty_columns(df, ['Date Sold', 'Date Acquired', 'Notes'])
        df = drop_unused_columns_and_rows(df)
        return df
