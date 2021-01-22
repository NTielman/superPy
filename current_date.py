from datetime import date, timedelta

class Inventory_date():
    current_date = date.today()
    '''init current_date to date.fromisoformat ku tin den date.txt file
    first create txt file
    os find root_date.txt file, if it doesnt exist (initialise date to today) i write date den un txt file.
    else if it already exists open it. read the date i initialise date fromisofomat'''

    def advance_time(self, num_of_days):
        self.current_date += timedelta(days=num_of_days)
        print(f'advanced date by {num_of_days} days\nCurrent day: {self.current_date}')

    def reverse_time(self, num_of_days):
        self.current_date -= timedelta(days=num_of_days)
        print(f'reversed date by {num_of_days} days\nCurrent day: {self.current_date}')

    def reset_time():
        self.current_date = date.today()
        print(f'Date has been reset\nCurrent day: {self.current_date}')

current = Inventory_date()