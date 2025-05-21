import pandas as pd

from loader.holding_loader import HoldingLoader
from loader.transaction_loader import TransactionLoader
from calculator.asset_calculator import AssetCalculator
from reporter.asset_reporter import AssetReporter
from reporter.summary_reporter import SummaryReporter


def execute_tax_reports(transactions_filename=None, holdings_filename=None):
    holdings_df = HoldingLoader.load_data(transactions_filename)
    transactions_df = TransactionLoader.load_data(holdings_filename)
    df = pd.concat([transactions_df, holdings_df])
    asset_summary = AssetCalculator.calculate_asset_summary(df)
    SummaryReporter.generate_summary_for_assets(asset_summary)
    AssetReporter.generate_transaction_details_per_asset(df, asset_summary)
    SummaryReporter.generate_overall_summary(df)


if __name__ == "__main__":
    execute_tax_reports()
