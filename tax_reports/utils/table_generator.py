from tax_reports.utils import common_util


def generate_table(df, title=None):
    table_lines = []
    if title:
        table_lines.append(f"\n{title}\n")

    headers = df.columns.tolist()
    col_widths = {}
    for col in headers:
        data_width = common_util.calculate_max_width(df, col)
        col_widths[col] = max(len(str(col)), data_width) + 2

    header_line = "|"
    for col in headers:
        header_line += f" {col.ljust(col_widths[col])} |"

    separator = "|"
    for col in headers:
        separator += f"{'-' * (col_widths[col] + 2)}|"
    table_lines.append(separator)
    table_lines.append(header_line)
    table_lines.append(separator)
    for _, row in df.iterrows():
        row_line = "|"
        for col in headers:
            value = common_util.calculate_value(row, col)
            row_line += f" {value.ljust(col_widths[col])} |"
        table_lines.append(row_line)
    table_lines.append(separator)
    table_lines.append("")
    return "\n".join(table_lines)
