from tax_reports.utils.common_util import as_number
from tax_reports.utils.common_util import as_currency
from tax_reports.utils.common_util import as_percentage
from tax_reports.utils.table_generator import generate_table
import tax_reports.constants as const


class AssetReporter:

    @staticmethod
    def generate_transaction_details_per_asset(df, assets):
        report_lines = []
        report_lines.append("2. Transaction Details Per Asset")
        asset_names = sorted(df[const.ASSET].unique())
        for asset_name in asset_names:
            asset_transactions = df[df[const.ASSET] == asset_name].copy()
            asset_total = assets[assets[const.ASSET] == asset_name].iloc[0]
            report_lines.append(generate_table(asset_transactions, f"Asset: {asset_name}"))
            report_lines.append(AssetReporter.generate_aggregate_details_per_asset(asset_name, asset_total))
        return "\n".join(report_lines)

    @staticmethod
    def generate_aggregate_details_per_asset(asset, asset_total):
        asset_lines = []
        asset_lines.append(f"{asset} Qty: {as_number(asset_total[const.QTY])}")
        asset_lines.append(f"Cost: {as_currency(asset_total[const.COST])}")
        asset_lines.append(f"Proceeds: {as_currency(asset_total[const.PROCEEDS])}")
        asset_lines.append(f"Gain/Loss: {as_currency(asset_total[const.GAIN_LOSS])} "
                           f"({as_percentage(asset_total[const.GAIN_LOSS_PERCENT])})")
        asset_lines.append("=" * 80)
        return "\n".join(asset_lines)
