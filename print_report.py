def create_terminal_report(report_type, report):
    '''formats and prints report to terminal'''
    line_length = 90
    header_lines = '#' * line_length
    division_line = '_' * line_length

    # print report title and header
    print('\n')
    print(header_lines)
    print(f'{report_type.upper() + " REPORT":^90}')
    print(header_lines)

    # print report body
    for line in report:
        print(line)
        print(division_line)

def print_report(report):
    '''prints a report to terminal'''
    terminal_report = report[0]
    report_type = report[1]
    create_terminal_report(report_type, terminal_report)