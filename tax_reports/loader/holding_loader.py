from tax_reports.utils.common_util import *  # Keep for now, or list all specific imports
from tax_reports.utils.common_util import filter_by_wallet_prefix
from pandas import DataFrame
# Removed Path import as DATA_DIR from config will be a Path object
import pandas as pd
import tax_reports.config as config
import tax_reports.constants as const


def rename_columns(df: DataFrame) -> DataFrame:
    # inplace=False is default, so just ensure it's not True and return
    return df.rename(columns={const.RAW_QTY_HOLDING: const.QTY,
                              const.RAW_COST_GBP_HOLDING: const.COST,
                              const.DESCRIPTION: const.WALLET_NAME})


def convert_asset_name(df: DataFrame) -> DataFrame:
    new_df = df.copy()
    # Extract the first word of the asset name, assuming it's the primary ticker/identifier
    new_df[const.ASSET] = new_df[const.ASSET].apply(lambda x: str(x).strip().split(' ')[0])
    return new_df


def drop_unused_columns_and_rows(df: DataFrame) -> DataFrame:
    # filter_by_wallet_prefix uses const.WALLET_NAME and const.WALLET_PREFIX by default
    df = filter_by_wallet_prefix(df, exclude_prefix=False)
    return df.drop(columns=[const.VALUE_GBP])


class HoldingLoader:

    @staticmethod
    def load_data(file_name=None):
        # Construct the full path using DATA_DIR from config and the provided file_name
        full_path = config.DATA_DIR / file_name
        df = pd.read_csv(full_path, skiprows=config.HOLDING_REPORT_SKIP_ROWS)
        
        df = rename_columns(df)
        df = convert_asset_name(df)
        df = convert_numeric_columns(df, [const.QTY, const.COST]) # From common_util, returns new df
        df = add_empty_columns(df, [const.DATE_SOLD, const.DATE_ACQUIRED, const.NOTES]) # From common_util, returns new df
        df = drop_unused_columns_and_rows(df) # Already returns new df
        return df
