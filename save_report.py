import os
import csv
from rich.console import Console
from current_date import current
from create_directory import create_directory

console = Console()
current_day = current.current_date.isoformat()

def create_csv_report(report_type, report, report_date):
    '''creates and writes a csv report 
    inside reports directory'''
    dir_path = create_directory('reports')
    file_name = f'{report_type}-{report_date}.csv'
    file_path = os.path.join(dir_path, file_name)

    with open(file_path, 'w', newline='') as report_file:
        csv_writer = csv.writer(report_file)
        csv_writer.writerows(report)
    console.print(f'Success: "{file_name}" report was saved to: {dir_path}')

def save_report(report, default_date=current_day):
    if report:
        report_type = report[0]
        report_body = report[1]
        report_date = default_date

        #if user has passed in a report-date
        if (len(report) > 2) and (report[2] != '-'):
            report_date = report[2]

        create_csv_report(report_type, report_body, report_date)
    else:
        console.print('Failure: could not create report')
        return None