import unittest
import pandas as pd
from pandas import DataFrame
from tax_reports.calculator.asset_calculator import AssetCalculator
import tax_reports.constants as const

class TestAssetCalculator(unittest.TestCase):

    def test_calculate_summary_basic(self):
        data = {
            const.ASSET: ['BTC', 'BTC', 'ETH', 'ETH', 'SOL'],
            const.WALLET_NAME: ['Coinbase', 'Binance', 'Kraken', 'Coinbase', 'Phantom'],
            const.QTY: [1, 0.5, 10, 5, 100],
            const.COST: [20000, 10000, 1500, 800, 2000],
            const.PROCEEDS: [25000, 12000, 1800, 1000, 2500],
            const.GAIN_LOSS: [5000, 2000, 300, 200, 500]
        }
        test_df = DataFrame(data)
        
        # Expected summary for non-@ wallets
        # BTC: Qty=1.5, Cost=30000, Proceeds=37000, Gain/Loss=7000. Gain/Loss % = (7000/30000)*100 = 23.33
        # ETH: Qty=15, Cost=2300, Proceeds=2800, Gain/Loss=500. Gain/Loss % = (500/2300)*100 = 21.74
        # SOL: Qty=100, Cost=2000, Proceeds=2500, Gain/Loss=500. Gain/Loss % = (500/2000)*100 = 25.00
        
        summary_df = AssetCalculator.calculate_asset_summary(test_df)
        
        self.assertEqual(summary_df.shape[0], 3) # Should have 3 assets
        
        btc_summary = summary_df[summary_df[const.ASSET] == 'BTC'].iloc[0]
        self.assertAlmostEqual(btc_summary[const.QTY], 1.5)
        self.assertAlmostEqual(btc_summary[const.COST], 30000)
        self.assertAlmostEqual(btc_summary[const.PROCEEDS], 37000)
        self.assertAlmostEqual(btc_summary[const.GAIN_LOSS], 7000)
        self.assertAlmostEqual(btc_summary[const.GAIN_LOSS_PERCENT], 23.33, places=2)

        eth_summary = summary_df[summary_df[const.ASSET] == 'ETH'].iloc[0]
        self.assertAlmostEqual(eth_summary[const.QTY], 15)
        self.assertAlmostEqual(eth_summary[const.COST], 2300)
        self.assertAlmostEqual(eth_summary[const.PROCEEDS], 2800)
        self.assertAlmostEqual(eth_summary[const.GAIN_LOSS], 500)
        self.assertAlmostEqual(eth_summary[const.GAIN_LOSS_PERCENT], 21.74, places=2) # (500/2300)*100

        sol_summary = summary_df[summary_df[const.ASSET] == 'SOL'].iloc[0]
        self.assertAlmostEqual(sol_summary[const.GAIN_LOSS_PERCENT], 25.00, places=2)


    def test_filter_out_at_wallets(self):
        data = {
            const.ASSET: ['BTC', 'BTC', 'ETH', 'ETH', 'ADA'],
            const.WALLET_NAME: ['Coinbase', const.WALLET_PREFIX + 'Staked BTC', const.WALLET_PREFIX + 'ETH Yield', 'Kraken', const.WALLET_PREFIX + 'Cardano Staking'],
            const.QTY: [1, 0.5, 10, 5, 200],
            const.COST: [20000, 10000, 1500, 800, 300],
            const.PROCEEDS: [25000, 12000, 1800, 1000, 400],
            const.GAIN_LOSS: [5000, 2000, 300, 200, 100]
        }
        test_df = DataFrame(data)
        summary_df = AssetCalculator.calculate_asset_summary(test_df)
        
        # Expected: Only BTC (from Coinbase) and ETH (from Kraken) should be present. ADA should be filtered out.
        # BTC (Coinbase): Qty=1, Cost=20000, Proceeds=25000, Gain/Loss=5000
        # ETH (Kraken): Qty=5, Cost=800, Proceeds=1000, Gain/Loss=200
        
        self.assertEqual(summary_df.shape[0], 2) 
        self.assertNotIn('ADA', summary_df[const.ASSET].tolist())
        
        btc_summary = summary_df[summary_df[const.ASSET] == 'BTC'].iloc[0]
        self.assertAlmostEqual(btc_summary[const.QTY], 1)
        self.assertAlmostEqual(btc_summary[const.COST], 20000)

        eth_summary = summary_df[summary_df[const.ASSET] == 'ETH'].iloc[0]
        self.assertAlmostEqual(eth_summary[const.QTY], 5)
        self.assertAlmostEqual(eth_summary[const.COST], 800)


    def test_empty_dataframe_input(self):
        empty_df = DataFrame(columns=[
            const.ASSET, const.WALLET_NAME, const.QTY, 
            const.COST, const.PROCEEDS, const.GAIN_LOSS
        ])
        summary_df = AssetCalculator.calculate_asset_summary(empty_df)
        self.assertTrue(summary_df.empty)
        # Check for expected columns in an empty summary
        expected_summary_cols = [const.ASSET, const.QTY, const.COST, const.PROCEEDS, const.GAIN_LOSS, const.GAIN_LOSS_PERCENT]
        pd.testing.assert_frame_equal(
            summary_df, 
            DataFrame(columns=expected_summary_cols), 
            check_dtype=False # Empty DFs might have object dtype
        )

    def test_all_at_wallets_input(self):
        data = {
            const.ASSET: ['BTC', 'ETH'],
            const.WALLET_NAME: [const.WALLET_PREFIX + 'Staked BTC', const.WALLET_PREFIX + 'ETH Yield'],
            const.QTY: [0.5, 10],
            const.COST: [10000, 1500],
            const.PROCEEDS: [12000, 1800],
            const.GAIN_LOSS: [2000, 300]
        }
        test_df = DataFrame(data)
        summary_df = AssetCalculator.calculate_asset_summary(test_df)
        self.assertTrue(summary_df.empty)
        expected_summary_cols = [const.ASSET, const.QTY, const.COST, const.PROCEEDS, const.GAIN_LOSS, const.GAIN_LOSS_PERCENT]
        pd.testing.assert_frame_equal(
            summary_df, 
            DataFrame(columns=expected_summary_cols), 
            check_dtype=False
        )

if __name__ == '__main__':
    unittest.main()
