import os

import pandas as pd

from loader.holding_loader import HoldingLoader
from loader.transaction_loader import TransactionLoader
from calculator.asset_calculator import AssetCalculator
from reporter.asset_reporter import AssetReporter
from reporter.summary_reporter import SummaryReporter


def find_csv_filename(file_pattern: str):
    for filename in os.listdir('../data'):
        if file_pattern in filename.lower() and filename.endswith('.csv'):
            return filename
    return None


def execute_tax_reports():
    holdings_df = HoldingLoader.load_data(find_csv_filename('holdings_report'))
    transactions_df = TransactionLoader.load_data(find_csv_filename('capital_gains_report'))
    df = pd.concat([holdings_df, transactions_df], ignore_index=True)
    combined_df = df[transactions_df.columns]
    asset_summary = AssetCalculator.calculate_asset_summary(combined_df)
    SummaryReporter.generate_summary_for_assets(asset_summary)
    AssetReporter.generate_transaction_details_per_asset(combined_df, asset_summary)
    SummaryReporter.generate_overall_summary(combined_df)


if __name__ == "__main__":
    execute_tax_reports()
