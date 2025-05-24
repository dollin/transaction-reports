from tax_reports.utils.common_util import as_number
from tax_reports.utils.common_util import as_currency
from tax_reports.utils.common_util import as_percentage
from tax_reports.utils.table_generator import generate_table


class AssetReporter:

    @staticmethod
    def generate_transaction_details_per_asset(df, assets):
        print("2. Transaction Details Per Asset")
        asset_names = sorted(df['Asset'].unique())
        for asset_name in asset_names:
            asset_transactions = df[df['Asset'] == asset_name].copy()
            asset_total = assets[assets['Asset'] == asset_name].iloc[0]
            generate_table(asset_transactions, f"Asset: {asset_name}")
            AssetReporter.generate_aggregate_details_per_asset(asset_name, asset_total)

    @staticmethod
    def generate_aggregate_details_per_asset(asset, asset_total):
        print(f"{asset} Qty: {as_number(asset_total['Qty'])}")
        print(f"Cost: {as_currency(asset_total['Cost'])}")
        print(f"Proceeds: {as_currency(asset_total['Proceeds'])}")
        print(f"Gain/Loss: {as_currency(asset_total['Gain/Loss'])} "
              f"({as_percentage(asset_total['Gain/Loss %'])})")
        print("=" * 80)
