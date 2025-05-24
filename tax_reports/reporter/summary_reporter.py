from tax_reports.utils.table_generator import generate_table
from tax_reports.utils.common_util import as_currency
from tax_reports.utils.common_util import as_percentage


class SummaryReporter:

    @staticmethod
    def generate_summary_for_assets(assets):
        generate_table(assets, "1. Gain/Loss Summary For Assets")

    @staticmethod
    def generate_overall_summary(df):
        total_net = df['Gain/Loss'].sum()
        total_cost = df['Cost'].sum()
        total_proceeds = df['Proceeds'].sum()
        total_percent = (total_net / total_cost * 100) if total_cost > 0 else 0
        print("")
        print("4. Overall Summary:")
        print(f"    Total Cost: {as_currency(total_cost)}")
        print(f"    Total Proceeds: {as_currency(total_proceeds)}")
        print(f"    Total Gain/Loss: {as_currency(total_net)}")
        print(f"    Percentage Return: {as_percentage(total_percent)}")
