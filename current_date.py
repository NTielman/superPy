from datetime import date, timedelta
from create_directory import create_directory
import os

class Inventory_date():
    def __init__(self):
        #find root folder path
        dir_path = create_directory('root_files')
        file_name = "root_date.txt"
        file_path = os.path.join(dir_path, file_name)

        try:
            #if root_date.txt file doesn't exist yet
            if not os.path.isfile(file_path):
                #initialise date to today
                today = date.today()
                self.current_date = today
                with open(file_path, 'w') as text_file:
                    text_file.write(today.isoformat())
            else:
                #initialise date to root_date
                with open(file_path, 'r') as text_file:
                    root_date = text_file.readline()
                    self.current_date = date.fromisoformat(root_date)
            #store file path for future use
            self.file_path = file_path
        except OSError:
            print(f'Error: Creating file "{file_name}"')

    def advance_time(self, num_of_days):
        self.current_date += timedelta(days=num_of_days)
        with open(self.file_path, 'w') as text_file:
            text_file.write(self.current_date.isoformat())
        print(f'advanced date by {num_of_days} days\nCurrent day: {self.current_date}')

    def reverse_time(self, num_of_days):
        self.current_date -= timedelta(days=num_of_days)
        with open(self.file_path, 'w') as text_file:
            text_file.write(self.current_date.isoformat())
        print(f'reversed date by {num_of_days} days\nCurrent day: {self.current_date}')

    def reset_time(self):
        self.current_date = date.today()
        with open(self.file_path, 'w') as text_file:
            text_file.write(self.current_date.isoformat())
        print(f'Date has been reset\nCurrent day: {self.current_date}')

current = Inventory_date()