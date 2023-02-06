import os


def check_path_exists(path, directory):
    path = join_path_name(path, directory)
    return os.path.exists(path)


def join_path_name(path, directory):
    path = os.path.join(path, directory)
    return path


def makedirs(dir_name):
    os.makedirs(dir_name)