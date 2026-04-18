# Removed Path import as DATA_DIR from config will be a Path object
from tax_reports.utils.common_util import *
import tax_reports.config as config
import tax_reports.constants as const


def rename_columns(df: DataFrame) -> DataFrame:
    # inplace=False is default, so just ensure it's not True and return
    return df.rename(columns={const.RAW_GAIN_LOSS_TRANSACTION: const.GAIN_LOSS,
                              const.RAW_COST_GBP_TRANSACTION: const.COST,
                              const.RAW_PROCEEDS_TRANSACTION: const.PROCEEDS,
                              const.RAW_AMOUNT_TRANSACTION: const.QTY})


class TransactionLoader:

    @staticmethod
    def load_data(file_name=None):
        # Construct the full path using DATA_DIR from config and the provided file_name
        full_path = config.DATA_DIR / file_name
        df = pd.read_csv(full_path, skiprows=config.TRANSACTION_REPORT_SKIP_ROWS)

        df = rename_columns(df)
        df = convert_datetime_columns(df, [const.DATE_SOLD, const.DATE_ACQUIRED]) # From common_util
        df = convert_numeric_columns(df, [const.QTY, const.COST, const.PROCEEDS, const.GAIN_LOSS]) # From common_util
        df = add_empty_columns(df, [const.DATE_ACQUIRED, const.NOTES]) # From common_util
        return df
