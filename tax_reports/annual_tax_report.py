import os

import pandas as pd

from loader.holding_loader import HoldingLoader
from loader.transaction_loader import TransactionLoader
from calculator.asset_calculator import AssetCalculator
from reporter.asset_reporter import AssetReporter
from reporter.summary_reporter import SummaryReporter

exclude_items = {}
include_items = {}
tax_year_files = {
    '2024-25': ['koinly_2024_beginning_of_year_holdings_report', 'koinly_2024_capital_gains_report'],
    '2025-26': ['koinly_2024_end_of_year_holdings_report', 'manual_2025_capital_gains_report']}


def find_csv_filename(file_pattern: str):
    for filename in os.listdir('../data'):
        if filename.startswith(file_pattern) and filename.endswith('.csv'):
            return filename
    return None


def execute_tax_reports(tax_year: str):
    df = get_dataframe_from_reports(tax_year)
    df = filter_dataframe(df)
    asset_summary = AssetCalculator.calculate_asset_summary(df)
    SummaryReporter.generate_summary_for_assets(asset_summary)
    AssetReporter.generate_transaction_details_per_asset(df, asset_summary)
    SummaryReporter.generate_overall_summary(df)


def get_dataframe_from_reports(tax_year: str):
    holdings_df = HoldingLoader.load_data(find_csv_filename(tax_year_files[tax_year][0]))
    transactions_df = TransactionLoader.load_data(find_csv_filename(tax_year_files[tax_year][1]))
    df = pd.concat([holdings_df, transactions_df], ignore_index=True)
    return df[transactions_df.columns]


def filter_dataframe(df):
    df = df.groupby('Asset').filter(lambda group: not group['Wallet Name'].str.startswith('@ ').all())
    for key, values in exclude_items.items():
        for value in values:
            df = df[df[key] != str(value).upper()]
    for key, values in include_items.items():
        for value in values:
            df = df[df[key].str.lower().fillna('') == str(value).lower()]
    return df


if __name__ == "__main__":
    exclude_items = {'Wallet Name': [],
                     'Asset': []
                     }
    include_items = {'Wallet Name': [],
                     'Asset': []
                     }
    execute_tax_reports('2024-25')
