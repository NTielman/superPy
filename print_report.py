from rich.console import Console
from prettytable import PrettyTable
from output_styling import superpy_theme

console = Console(theme=superpy_theme)

def create_terminal_report(report_type, report):
    '''formats and prints report to terminal'''
    #add report title and headers
    title=f'{report_type.upper()} REPORT'
    table = PrettyTable()
    table.field_names = report.pop(0)

    reports_with_footers = ['purchases', 'sales', 'profit']
    if report_type in reports_with_footers:
        footer = report.pop()
    #add report body to table
    for line in report:
        table.add_row(line)
    table.align = 'r'

    console.print('\n')
    console.print(title, style='success')
    console.print(table, style='success')
    #print report footer if available
    if report_type in reports_with_footers:
        footer_padding = (3 * (len(table.field_names) - 1))
        table_width = sum(table._widths)
        console.print('| ' + (' ' * (table_width - len(footer[0])) + ' ' * footer_padding) + footer[0] + ' |', style='success')
        console.print('+-' + '-' * table_width + '-' * footer_padding + '-+', style='success')

def print_report(report):
    '''prints a report to terminal'''
    if report:
        terminal_report = report[2]
        report_type = report[1]
        create_terminal_report(report_type, terminal_report)
    else:
        console.print('Failure: could not create report', style='failure')
        return None