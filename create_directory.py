import os

def create_directory(dir_name):
    '''creates a folder in current directory'''
    full_path = os.path.realpath(__file__)
    file_dir = os.path.dirname(full_path)
    dir_path = os.path.join(file_dir, dir_name)

    try:
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)
        return dir_path
    except OSError:
        print(f'Error: Creating folder "{dir_name}"')