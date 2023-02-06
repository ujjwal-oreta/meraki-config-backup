import json
import datetime


def get_now(str_format = False):
    now = datetime.datetime.now()
    if str_format:
        return now.strftime("%Y%m%d%H%M%S")
    else:
        return now


def write_file(path, data):
    writer = open(path, 'w')
    writer.write(json.dumps(data))
    writer.close()
    