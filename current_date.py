from datetime import date, timedelta
from create_directory import create_directory
import os
from rich.console import Console
from output_styling import superpy_theme

console = Console(theme=superpy_theme)

class Inventory_date():
    def __init__(self):
        #find root folder path
        dir_path = create_directory('root_files')
        file_name = "root_date.txt"
        self.file_path = os.path.join(dir_path, file_name)
        #store file path for future use
        # self.file_path = file_path

        try:
            #if root_date.txt file doesn't exist yet
            if not os.path.isfile(file_path):
                #initialise date to today
                self.current_date = date.today()
                update_root_date()
                # with open(file_path, 'w') as text_file:
                #     text_file.write(today.isoformat())
                console.print(f'Created "{file_name}" file at {self.file_path}', style='process_info')
            else:
                #initialise date to root_date
                with open(file_path, 'r') as text_file:
                    root_date = text_file.readline()
                    self.current_date = date.fromisoformat(root_date)
            console.print(f'Current date is: {self.current_date}', style='process_info')
        except Exception as e:
            console.print(e, style='error')

    def advance_time(self, num_of_days):
        self.current_date += timedelta(days=num_of_days)
        update_root_date()
        console.print(f'Success: advanced date by [highlight]{num_of_days}[/highlight] days\nCurrent day is: [highlight]{self.current_date}[/highlight]', style='success')

    def reverse_time(self, num_of_days):
        self.current_date -= timedelta(days=num_of_days)
        update_root_date()
        console.print(f'Success: reversed date by [highlight]{num_of_days}[/highlight] days\nCurrent day is: [highlight]{self.current_date}[/highlight]', style='success')

    def reset_time(self):
        self.current_date = date.today()
        update_root_date()
        console.print(f'Success: Date has been reset\nCurrent day is: [highlight]{self.current_date}[/highlight]', style='success')
        
    def update_root_date(self):
        with open(self.file_path, 'w') as text_file:
            text_file.write(self.current_date.isoformat())

current = Inventory_date()