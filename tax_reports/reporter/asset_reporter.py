import common_util
import table_generator


class AssetReporter:

    @staticmethod
    def generate_transaction_details_per_asset(df, assets):
        print("2. Transaction Details Per Asset")
        asset_names = sorted(df['Asset'].unique())
        for asset_name in asset_names:
            asset_transactions = df[df['Asset'] == asset_name].copy()
            asset_total = assets[assets['Asset'] == asset_name].iloc[0]
            table_generator.generate_table(asset_transactions, f"Asset: {asset_name}")
            AssetReporter.generate_aggregate_details_per_asset(asset_name, asset_total)

    @staticmethod
    def generate_aggregate_details_per_asset(asset, asset_total):
        print(f"{asset} Qty: {common_util.as_number(asset_total['Qty'])}")
        print(f"Cost: {common_util.as_currency(asset_total['Cost'])}")
        print(f"Proceeds: {common_util.as_currency(asset_total['Proceeds'])}")
        print(f"Gain/Loss: {common_util.as_currency(asset_total['Gain/Loss'])} "
              f"({common_util.as_percentage(asset_total['Gain/Loss %'])})")
        print("=" * 80)
