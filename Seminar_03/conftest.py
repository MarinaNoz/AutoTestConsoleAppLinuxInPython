import random
import string
import datetime
import pytest
import yaml
from checkout import *


with open('config.yml', 'r', encoding='utf-8') as f:
    data = yaml.safe_load(f)
FOLDER_TST = data['FOLDER_TST']
FOLDER_OUT = data['FOLDER_OUT']
FOLDER_TARG = data['FOLDER_TARG']
FOLDER_X_TST = data['FOLDER_X_TST']
FOLDER_X_OUT = data['FOLDER_X_OUT']
FILE_INPUT = data['FILE_INPUT']
FOLDER_STAT = data['FOLDER_STAT']
FOLDER_4BAD = data['FOLDER_4BAD']
FILE_STAT = data['FILE_STAT']
LOADAVG = data['LOADAVG']

@pytest.fixture()
def get_dir():
    return checkout(f'mkdir {FOLDER_OUT} {FOLDER_TST} {FOLDER_TARG}')

@pytest.fixture()
def make_file():
    list_files = []
    for i in range(data['count']):
        filename = ''.join(random.choices(string.ascii_letters + string.digits, k=7))
        if checkout(
                f'cd {FOLDER_TST}; dd if=/dev/urandom of={filename} bs={data["size"]} '
                f'count={data["count"]} iflag=fullblock'):
            list_files.append(filename)
    return list_files

@pytest.fixture()
def clear_dir():
    return checkout(f'rm -rf {FOLDER_OUT} {FOLDER_TST} {FOLDER_TARG}')

@pytest.fixture()
def get_list():
    return getout(f'ls {FOLDER_TST}')[0]

@pytest.fixture()
def get_bad_file():
    checkout(f'cd {FOLDER_TST}; 7z a {FOLDER_OUT}/arxbad', "Everything is Ok")
    checkout(f'truncate -s 1 {FOLDER_OUT}/arxbad.7z')
    yield 'arxbad'
    checkout(f'rm -f {FOLDER_OUT}/arxbad')

@pytest.fixture()
def stat_file():

    with open(f"{FOLDER_STAT}/stat.txt", 'a') as stat, open(f"{LOADAVG}/loadavg", 'r') as load:
    loadavg = load.readline()
    stat.write(datetime.datetime.now().ctime())
    datetime.datetime.now()
    stat.write(f"\t " + f" Количество файлов: {str(data['count'])}" + ', ' + f" Размер файлов: {str(data['size'])}"
               + f" Загрузка процессора: {loadavg}")
