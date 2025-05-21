import table_generator
import common_util


class SummaryReporter:

    @staticmethod
    def generate_summary_for_assets(assets):
        table_generator.generate_table(assets, "1. Gain/Loss Summary For Assets")

    @staticmethod
    def generate_overall_summary(df):
        total_net = df['Gain/Loss'].sum()
        total_cost = df['Cost'].sum()
        total_proceeds = df['Proceeds'].sum()
        total_percent = (total_net / total_cost * 100) if total_cost > 0 else 0
        print("")
        print("4. Overall Summary:")
        print(f"    Total Cost: {common_util.as_currency(total_cost)}")
        print(f"    Total Proceeds: {common_util.as_currency(total_proceeds)}")
        print(f"    Total Gain/Loss: {common_util.as_currency(total_net)}")
        print(f"    Percentage Return: {common_util.as_percentage(total_percent)}")
