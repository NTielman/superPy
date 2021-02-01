import os
from datetime import date, timedelta
from rich.console import Console
from create_directory import create_directory

console = Console()

class Inventory_date():

    def __init__(self):
        dir_path = create_directory('root_files')
        file_name = "root_date.txt"
        self.file_path = os.path.join(dir_path, file_name)
        try:
            with open(self.file_path, 'r') as text_file:
                root_date = text_file.readline()
                self.current_date = date.fromisoformat(root_date)
        except FileNotFoundError:
            self.current_date = date.today()
            self.update_root_date()
            console.print(
                f'Created "{file_name}" file at {self.file_path}')
        console.print(f'\nCurrent date is: {self.current_date}')

    def advance_time(self, num_of_days):
        self.current_date += timedelta(days=num_of_days)
        self.update_root_date()
        console.print(
            f'Success: advanced date by {num_of_days} days\nCurrent day is: {self.current_date}')

    def reverse_time(self, num_of_days):
        self.current_date -= timedelta(days=num_of_days)
        self.update_root_date()
        console.print(
            f'Success: reversed date by {num_of_days} days\nCurrent day is: {self.current_date}')

    def reset_time(self):
        self.current_date = date.today()
        self.update_root_date()
        console.print(
            f'Success: Date has been reset\nCurrent day is: {self.current_date}')

    def update_root_date(self):
        with open(self.file_path, 'w') as text_file:
            text_file.write(self.current_date.isoformat())

current = Inventory_date()