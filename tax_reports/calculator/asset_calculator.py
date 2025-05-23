class AssetCalculator:

    @staticmethod
    def calculate_asset_summary(df):
        filtered_df = df[~df['Wallet Name'].str.startswith('@ ')]
        sum_columns = {'Qty': 'sum', 'Cost': 'sum', 'Proceeds': 'sum', 'Gain/Loss': 'sum'}
        asset_summary = filtered_df.groupby('Asset').agg(sum_columns).reset_index()
        asset_summary['Gain/Loss %'] = (asset_summary['Gain/Loss'] / asset_summary['Cost'] * 100).round(2)
        return asset_summary.sort_values('Gain/Loss', ascending=False)
