# TODO: change date format of dlf date to yyyy-mm-dd
import os


def rename_directories(path):
    for filename in os.listdir(path):
        if os.path.isdir(os.path.join(path, filename)):
            split_name = filename.split('-')
            if len(split_name) > 1:
                date, title = split_name[0], '-'.join(split_name[1:])
                day, month, year = date.split('.')
                new_date = '-'.join([year, month, day])
                new_name = '-'.join([new_date, title])
                os.rename(os.path.join(path, filename), os.path.join(path, new_name))


rename_directories(os.getcwd())
