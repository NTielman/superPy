from rich.console import Console
from prettytable import PrettyTable

console = Console()

def create_terminal_report(report_type, report):
    '''formats and prints a table report to terminal'''
    table = PrettyTable()
    title = f'{report_type.upper()} REPORT'
    table.field_names = report.pop(0)  # table headers

    reports_with_footers = ['purchases', 'sales', 'profit']
    if report_type in reports_with_footers:
        # remove footer before adding report body to table
        footer = report.pop()

    table.add_rows(report)
    table.align = 'r'
    console.print('\n')
    console.print(title)
    console.print(table)

    # print report footer if available
    if report_type in reports_with_footers:
        footer_padding = (3 * (len(table.field_names) - 1))
        table_width = sum(table._widths)
        console.print('| ' + (' ' * (table_width -
                                     len(footer[0])) + ' ' * footer_padding) + footer[0] + ' |')
        console.print('+-' + '-' * table_width + '-' * footer_padding + '-+')

def print_report(report):
    if report:
        report_type = report[0]
        report_body = report[1]
        create_terminal_report(report_type, report_body)
    else:
        console.print('Failure: could not create report')
        return None