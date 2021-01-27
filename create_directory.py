import os
from rich.console import Console
from output_styling import superpy_theme

console = Console(theme=superpy_theme)

def create_directory(dir_name):
    '''creates a folder in current directory'''
    full_path = os.path.realpath(__file__)
    file_dir = os.path.dirname(full_path)
    dir_path = os.path.join(file_dir, dir_name)

    try:
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)
            console.print(f'Created "{dir_name}" folder at {dir_path}', style='process_info')
        return dir_path
    except Exception as e:
            console.print(e, style='error')