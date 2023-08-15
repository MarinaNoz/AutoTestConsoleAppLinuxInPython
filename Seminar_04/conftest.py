import random
import string
from datetime import datetime
import pytest
import yaml
from checkout import *
import datetime
import paramiko
from sshcheckers import *

with open('config.yaml', 'r', encoding='utf-8') as f:
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
HOST = data['host']
PORT = data['port']
USER = data['user']
PWD = data['passwd']
COUNT = data['count']


@pytest.fixture()
def make_dir():
    return ssh_checkout(f'{HOST}', f'{USER}', f'{PWD}',
                        'mkdir {} {} {} {}'.format(FOLDER_TST, FOLDER_OUT, FOLDER_TARG, FOLDER_STAT), '')


@pytest.fixture()
def make_file():
    list_files = []
    for i in range(COUNT):
        filename = ''.join(random.choices(string.ascii_letters + string.digits, k=7))
        if ssh_checkout(f'{HOST}', f'{USER}', f'{PWD}',
                        f'cd {FOLDER_TST}; dd if=/dev/urandom of={filename} bs={data["size"]} '
                        f'count={COUNT} iflag=fullblock', ''):
            list_files.append(filename)
    return list_files

def save_log(start_time, name):
    with open(name, 'w', encoding='utf-8') as f:
        f.write(''.join(getout(f'journalctl --since "{start_time}"')[0]))

@pytest.fixture()
def clear_dir():
    return ssh_checkout(f'{HOST}', f'{USER}', f'{PWD}',
                        'rm -rf {FOLDER_TST} {FOLDER_OUT} {FOLDER_TARG} {FOLDER_X_TST} {FOLDER_X_OUT}'
                        '{FOLDER_X_TST} {FOLDER_4BAD}', '')


@pytest.fixture()
def get_list():
    return ssh_getout(f'{HOST}', f'{USER}', f'{PWD}', f'ls {FOLDER_TST[0]}')


@pytest.fixture()
def get_bad_file():
    ssh_checkout(f'{HOST}', f'{USER}', f'{PWD}',
                 f'cd {FOLDER_TST}; 7z a {FOLDER_OUT}/arxbad', "Everything is Ok")
    yield ssh_checkout(f'{HOST}', f'{USER}', f'{PWD}', f'truncate -s 1 {FOLDER_OUT}/arxbad.7z', '')



@pytest.fixture(autouse=True)
def stat_file():
    with open(f'{FOLDER_STAT}/stat.txt', 'w') as stat, open(f'{LOADAVG}/loadavg', 'r') as load:
        loadavg = load.readline()
        stat.write(datetime.datetime.now().ctime())
        datetime.datetime.now()
        stat.write(f'\t ' + f' Количество файлов: {str(data["count"])}' + ', ' + f'Размер файлов: {str(data["size"])}'
                   + f' Загрузка процессора: {loadavg}')


@pytest.fixture()
def start_time():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
