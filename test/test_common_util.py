import unittest
import pandas as pd
from pandas import DataFrame
import numpy as np # For NaN
from tax_reports.utils.common_util import filter_by_wallet_prefix
import tax_reports.constants as const

class TestCommonUtil(unittest.TestCase):

    def test_exclude_prefix_default(self):
        data = {
            const.WALLET_NAME: ['Coinbase', const.WALLET_PREFIX + 'Staked BTC', 'Kraken', const.WALLET_PREFIX + 'Yield ETH']
        }
        test_df = DataFrame(data)
        # Default is exclude_prefix=True, column_name=const.WALLET_NAME, prefix=const.WALLET_PREFIX
        filtered_df = filter_by_wallet_prefix(test_df) 
        
        self.assertEqual(filtered_df.shape[0], 2)
        self.assertNotIn(const.WALLET_PREFIX + 'Staked BTC', filtered_df[const.WALLET_NAME].tolist())
        self.assertIn('Coinbase', filtered_df[const.WALLET_NAME].tolist())

    def test_include_prefix(self):
        data = {
            const.WALLET_NAME: ['Coinbase', const.WALLET_PREFIX + 'Staked BTC', 'Kraken', const.WALLET_PREFIX + 'Yield ETH']
        }
        test_df = DataFrame(data)
        filtered_df = filter_by_wallet_prefix(test_df, column_name=const.WALLET_NAME, prefix=const.WALLET_PREFIX, exclude_prefix=False)
        
        self.assertEqual(filtered_df.shape[0], 2)
        self.assertIn(const.WALLET_PREFIX + 'Staked BTC', filtered_df[const.WALLET_NAME].tolist())
        self.assertNotIn('Coinbase', filtered_df[const.WALLET_NAME].tolist())

    def test_different_column_and_prefix(self):
        custom_col = 'Transaction Type'
        custom_prefix = 'Fee_'
        data = {
            const.WALLET_NAME: ['Coinbase', const.WALLET_PREFIX + 'Staked BTC'],
            custom_col: [custom_prefix + 'Trade', 'Deposit', custom_prefix + 'Withdrawal', 'Transfer']
        }
        test_df = DataFrame(data)
        
        # Test include prefix
        filtered_df_include = filter_by_wallet_prefix(test_df, column_name=custom_col, prefix=custom_prefix, exclude_prefix=False)
        self.assertEqual(filtered_df_include.shape[0], 2)
        self.assertTrue(all(w.startswith(custom_prefix) for w in filtered_df_include[custom_col]))
        
        # Test exclude prefix
        filtered_df_exclude = filter_by_wallet_prefix(test_df, column_name=custom_col, prefix=custom_prefix, exclude_prefix=True)
        self.assertEqual(filtered_df_exclude.shape[0], 2)
        self.assertTrue(all(not w.startswith(custom_prefix) for w in filtered_df_exclude[custom_col]))

    def test_column_with_nan_values(self):
        data = {
            const.WALLET_NAME: ['Coinbase', np.nan, const.WALLET_PREFIX + 'Staked BTC', None, 'Kraken']
        }
        test_df = DataFrame(data)
        
        # Exclude prefix (default)
        filtered_df_exclude = filter_by_wallet_prefix(test_df)
        self.assertEqual(filtered_df_exclude.shape[0], 3) # Coinbase, NaN, None (Kraken)
        self.assertIn('Coinbase', filtered_df_exclude[const.WALLET_NAME].tolist())
        self.assertIn('Kraken', filtered_df_exclude[const.WALLET_NAME].tolist())
        # NaNs are effectively not matching the prefix, so they are included when exclude_prefix=True
        self.assertTrue(any(pd.isna(val) for val in filtered_df_exclude[const.WALLET_NAME]))


        # Include prefix
        filtered_df_include = filter_by_wallet_prefix(test_df, exclude_prefix=False)
        self.assertEqual(filtered_df_include.shape[0], 1)
        self.assertIn(const.WALLET_PREFIX + 'Staked BTC', filtered_df_include[const.WALLET_NAME].tolist())

    def test_empty_dataframe_input_for_filter(self):
        empty_df = DataFrame(columns=[const.WALLET_NAME, 'Another Column'])
        filtered_df = filter_by_wallet_prefix(empty_df)
        self.assertTrue(filtered_df.empty)
        pd.testing.assert_frame_equal(filtered_df, empty_df, check_dtype=False)

    def test_non_existent_column(self):
        data = {const.WALLET_NAME: ['Coinbase', const.WALLET_PREFIX + 'Wallet']}
        test_df = DataFrame(data)
        # Function should return df unmodified if column_name doesn't exist
        filtered_df = filter_by_wallet_prefix(test_df, column_name="NonExistentCol")
        pd.testing.assert_frame_equal(test_df, filtered_df)


if __name__ == '__main__':
    unittest.main()
