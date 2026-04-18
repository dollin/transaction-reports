# Column Names
ASSET = "Asset"
WALLET_NAME = "Wallet Name"
QTY = "Qty"
COST = "Cost"
PROCEEDS = "Proceeds"
GAIN_LOSS = "Gain/Loss"
GAIN_LOSS_PERCENT = "Gain/Loss %"
DATE_SOLD = "Date Sold"
DATE_ACQUIRED = "Date Acquired"
NOTES = "Notes"
DESCRIPTION = "Description"  # Original name in holding report for 'Wallet Name'
VALUE_GBP = "Value (GBP)"    # Original name in holding report, used for dropping

# Raw CSV Column Names (examples, add more if needed for consistent renaming)
# Holding report specific raw names
RAW_QTY_HOLDING = "Quantity" # Renamed to QTY
RAW_COST_GBP_HOLDING = "Cost (GBP)" # Renamed to COST
# Transaction report specific raw names
RAW_GAIN_LOSS_TRANSACTION = "Gain / loss" # Renamed to GAIN_LOSS
RAW_COST_GBP_TRANSACTION = "Cost (GBP)" # Renamed to COST
RAW_PROCEEDS_TRANSACTION = "Proceeds (GBP)" # Renamed to PROCEEDS
RAW_AMOUNT_TRANSACTION = "Amount" # Renamed to QTY

# Special Values
WALLET_PREFIX = "@ "
