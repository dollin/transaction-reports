from pathlib import Path
import tax_reports.constants as const

# Assuming config.py is in the 'tax_reports' directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

# Configuration for tax year files
tax_year_files = {
    '2024-25': ['koinly_2024_beginning_of_year_holdings_report', 'koinly_2024_capital_gains_report'],
    '2025-26': ['koinly_2024_end_of_year_holdings_report', 'manual_2025_capital_gains_report']
}

# Configuration for excluding items from reports
exclude_items = {
    const.WALLET_NAME: [],  # List of wallet names to exclude
    const.ASSET: []         # List of asset symbols to exclude
}

# Configuration for including items in reports (currently unused but defined for future use)
include_items = {
    const.WALLET_NAME: [],  # List of wallet names to include (if filtering by inclusion)
    const.ASSET: []         # List of asset symbols to include (if filtering by inclusion)
}

# Configuration for skipping rows in holding and transaction reports
HOLDING_REPORT_SKIP_ROWS = 2
TRANSACTION_REPORT_SKIP_ROWS = 2
