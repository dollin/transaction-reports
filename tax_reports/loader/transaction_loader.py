from pathlib import Path

from tax_reports.utils.common_util import *


def rename_columns(df: DataFrame):
    df.rename(columns={'Gain / loss': 'Gain/Loss', 'Cost (GBP)': 'Cost', 'Proceeds (GBP)': 'Proceeds', 'Amount': 'Qty'},
              inplace=True)


class TransactionLoader:

    @staticmethod
    def load_data(file_name=None):
        df = pd.read_csv(Path(__file__).resolve().parent.parent.parent / "data" / file_name, skiprows=2)
        rename_columns(df)
        convert_datetime_columns(df, ['Date Sold', 'Date Acquired'])
        convert_numeric_columns(df, ['Qty', 'Cost', 'Proceeds', 'Gain/Loss'])
        add_empty_columns(df, ['Date Acquired', 'Notes'])
        return df
