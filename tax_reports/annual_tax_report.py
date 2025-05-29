import os
import pandas as pd

from calculator.asset_calculator import AssetCalculator
from loader.holding_loader import HoldingLoader
from loader.transaction_loader import TransactionLoader
from reporter.asset_reporter import AssetReporter
from reporter.summary_reporter import SummaryReporter
import tax_reports.config as config
from tax_reports.utils.common_util import filter_by_wallet_prefix # Added import
import tax_reports.constants as const


def find_csv_filename(file_pattern: str, data_directory: str):
    for filename in os.listdir(data_directory):
        if filename.startswith(file_pattern) and filename.endswith('.csv'):
            return os.path.join(data_directory, filename)
    return None


def execute_tax_reports(tax_year: str):
    df = get_dataframe_from_reports(tax_year)
    df = filter_dataframe(df)
    asset_summary = AssetCalculator.calculate_asset_summary(df)

    summary_report_string = SummaryReporter.generate_summary_for_assets(asset_summary)
    print(summary_report_string)

    asset_details_string = AssetReporter.generate_transaction_details_per_asset(df, asset_summary)
    print(asset_details_string)

    overall_summary_string = SummaryReporter.generate_overall_summary(df)
    print(overall_summary_string)


def get_dataframe_from_reports(tax_year: str):
    holding_file_pattern = config.tax_year_files[tax_year][0]
    transaction_file_pattern = config.tax_year_files[tax_year][1]

    holding_report_path = find_csv_filename(holding_file_pattern, config.DATA_DIR)
    if holding_report_path is None:
        raise FileNotFoundError(
            f"Holding report matching pattern '{holding_file_pattern}' not found in {config.DATA_DIR}"
        )

    transaction_report_path = find_csv_filename(transaction_file_pattern, config.DATA_DIR)
    if transaction_report_path is None:
        raise FileNotFoundError(
            f"Transaction report matching pattern '{transaction_file_pattern}' not found in {config.DATA_DIR}"
        )

    holdings_df = HoldingLoader.load_data(os.path.basename(holding_report_path))
    transactions_df = TransactionLoader.load_data(os.path.basename(transaction_report_path))
    df = pd.concat([holdings_df, transactions_df], ignore_index=True)
    # Ensure final DataFrame conforms to the column structure of transaction reports.
    return df[transactions_df.columns]


def filter_dataframe(df):
    # This filters out entire asset groups if *all* their associated wallet names start with the WALLET_PREFIX.
    # The filter_by_wallet_prefix utility is not used here due to the .all() condition on the group
    df = df.groupby(const.ASSET).filter(lambda group: not group[const.WALLET_NAME].fillna('').str.startswith(const.WALLET_PREFIX).all())
    for key, values in config.exclude_items.items(): # keys are now constants from config.py
        for value in values:
            df = df[df[key] != str(value).upper()]
    for key, values in config.include_items.items(): # keys are now constants from config.py
        for value in values:
            df = df[df[key].str.lower().fillna('') == str(value).lower()]
    return df


if __name__ == "__main__":
    # exclude_items and include_items are now accessed via config (which uses constants for keys)
    # No changes needed here if they are used as config.exclude_items directly in functions
    execute_tax_reports('2024-25')
