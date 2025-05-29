from tax_reports.utils.table_generator import generate_table
from tax_reports.utils.common_util import as_currency
from tax_reports.utils.common_util import as_percentage
import tax_reports.constants as const


class SummaryReporter:

    @staticmethod
    def generate_summary_for_assets(assets):
        return generate_table(assets, "1. Gain/Loss Summary For Assets")

    @staticmethod
    def generate_overall_summary(df):
        summary_lines = []
        total_net = df[const.GAIN_LOSS].sum()
        total_cost = df[const.COST].sum()
        total_proceeds = df[const.PROCEEDS].sum()
        total_percent = (total_net / total_cost * 100) if total_cost > 0 else 0
        summary_lines.append("")  # For the initial empty line print
        summary_lines.append("4. Overall Summary:")
        summary_lines.append(f"    Total Cost: {as_currency(total_cost)}")
        summary_lines.append(f"    Total Proceeds: {as_currency(total_proceeds)}")
        summary_lines.append(f"    Total Gain/Loss: {as_currency(total_net)}")
        summary_lines.append(f"    Percentage Return: {as_percentage(total_percent)}")
        return "\n".join(summary_lines)
