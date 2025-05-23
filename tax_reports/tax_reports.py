import os

import pandas as pd

from loader.holding_loader import HoldingLoader
from loader.transaction_loader import TransactionLoader
from calculator.asset_calculator import AssetCalculator
from reporter.asset_reporter import AssetReporter
from reporter.summary_reporter import SummaryReporter

exclude_items = {}
include_items = {}
tax_year_from = 2024


def find_csv_filename(file_pattern: str):
    for filename in os.listdir('../data'):
        if file_pattern in filename.lower() and f"_{tax_year_from}_" in filename and filename.endswith('.csv'):
            return filename
    return None


def execute_tax_reports():
    df = get_dataframe_from_reports()
    df = filter_dataframe(df)
    asset_summary = AssetCalculator.calculate_asset_summary(df)
    SummaryReporter.generate_summary_for_assets(asset_summary)
    AssetReporter.generate_transaction_details_per_asset(df, asset_summary)
    SummaryReporter.generate_overall_summary(df)


def get_dataframe_from_reports():
    holdings_df = HoldingLoader.load_data(find_csv_filename('holdings_report'))
    transactions_df = TransactionLoader.load_data(find_csv_filename('capital_gains_report'))
    df = pd.concat([holdings_df, transactions_df], ignore_index=True)
    return df[transactions_df.columns]


def filter_dataframe(df):
    df = df.groupby('Asset').filter(lambda group: not group['Wallet Name'].str.startswith('@ ').all())
    for key, values in exclude_items.items():
        for value in values:
            df = df[df[key] != str(value).upper()]
    for key, values in include_items.items():
        for value in values:
            df = df[df[key] == str(value)]
    return df


if __name__ == "__main__":
    exclude_items = {'Wallet Name': [],
                     'Asset': []
                     }
    include_items = {'Wallet Name': ['Coinbase'],
                     'Asset': []
                     }
    execute_tax_reports()
