import csv
import os
from create_directory import create_directory
from rich.console import Console
from output_styling import superpy_theme

console = Console(theme=superpy_theme)

def create_csv_report(report_type, report, report_date):
    '''formats and creates a csv report 
    inside reports directory'''
    dir_path = create_directory('reports')
    file_name = f'{report_type}-{report_date}.csv'
    file_path = os.path.join(dir_path, file_name)

    with open(file_path, 'w', newline='') as report_file:
        csv_writer = csv.writer(report_file)
        csv_writer.writerows(report)
    console.print(f'Success: [highlight]"{file_name}"[/highlight] report was saved to: [highlight]{dir_path}[/highlight]', style='success')

def save_report(report, default_date):
    '''saves a report to csv file '''
    if report:
        csv_report = report[2]
        report_type = report[1]
        report_date = default_date

        if len(report) > 3:
            if (report[3] != 'all'):
                report_date = report[3]

        create_csv_report(report_type, csv_report, report_date)
    else:
        console.print('Failure: could not create report', style='failure')
        return None
