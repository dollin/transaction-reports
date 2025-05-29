from tax_reports.utils.common_util import filter_by_wallet_prefix
import tax_reports.constants as const

class AssetCalculator:

    @staticmethod
    def calculate_asset_summary(df):
        # filter_by_wallet_prefix uses const.WALLET_NAME and const.WALLET_PREFIX by default
        filtered_df = filter_by_wallet_prefix(df, exclude_prefix=True)
        sum_columns = {const.QTY: 'sum', const.COST: 'sum', const.PROCEEDS: 'sum', const.GAIN_LOSS: 'sum'}
        asset_summary = filtered_df.groupby(const.ASSET).agg(sum_columns).reset_index()
        asset_summary[const.GAIN_LOSS_PERCENT] = (asset_summary[const.GAIN_LOSS] / asset_summary[const.COST] * 100).round(2)
        return asset_summary.sort_values(const.GAIN_LOSS, ascending=False)
