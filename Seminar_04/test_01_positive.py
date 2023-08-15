from conftest import *
from sshcheckers import *


def save_log(start_time, name):
    with open(name, 'w', encoding='utf-8') as f:
        f.write(''.join(getout(f'journalctl --since "{start_time}"')[0]))


def test_deploy(start_time):
    res = []
    upload_files('0.0.0.0', 'usertest', 'qwerty', 'test_ssh/p7zip-full.deb',
                 '/home/usertest/p7zip-full.deb')
    res.append(ssh_checkout('0.0.0.0', 'usertest', 'qwerty',
                            'echo "qwerty" | sudo -S dpkg -i /home/usertest/p7zip-full.deb', 'Настраивается пакет'))
    res.append(ssh_checkout('0.0.0.0', 'usertest', 'qwerty',
                            'echo "qwerty" | sudo -S dpkg -s p7zip-full', 'Status: install ok installed'))
    save_log(start_time, f'log_test_deploy')
    assert all(res), 'test_deploy FAIL'


def test_positive1(start_time, clear_dir, make_dir, make_file, stat_file):
    res = []
    res.append(ssh_checkout(f'{HOST}', f'{USER}', f'{PWD}',
                            f'cd {FOLDER_TST}; 7z a {FOLDER_OUT}/{FILE_INPUT}', 'Everything is Ok'))
    res.append(ssh_checkout(f'{HOST}', f'{USER}', f'{PWD}',
                            f'ls {FOLDER_OUT}', f'{FILE_INPUT}.7z'))
    save_log(start_time, f'log_test_positive1')
    assert all(res), 'positive_test1 FAIL'


def test_positive2(start_time, clear_dir, make_dir, make_file, stat_file):
    res = [ssh_checkout(f'{HOST}', f'{USER}', f'{PWD}',
                        f'cd {FOLDER_TST}; 7z a {FOLDER_OUT}/{FILE_INPUT}', 'Everything is Ok'),
           ssh_checkout(f'{HOST}', f'{USER}', f'{PWD}',
                        f'cd {FOLDER_OUT}; 7z e {FILE_INPUT}.7z -o{FOLDER_TARG} -y', 'Everything is Ok')]
    for i in make_file:
        res.append(ssh_checkout(f'{HOST}', f'{USER}', f'{PWD}',
                                f'ls {FOLDER_TARG}', i))
    save_log(start_time, f'log_test_positive2')
    assert all(res), 'positive_test2 FAIL'


def test_positive3(start_time, stat_file):
    save_log(start_time, f'log_test_positive3')
    assert ssh_checkout(f'{HOST}', f'{USER}', f'{PWD}',
                        f'cd {FOLDER_OUT}; 7z t {FILE_INPUT}.7z', 'Everything is Ok'), 'positive_test3 FAIL'


def test_positive4(start_time, stat_file):
    # print(get_list)
    save_log(start_time, f'log_test_positive4')
    assert ssh_checkout(f'{HOST}', f'{USER}', f'{PWD}',
                        f'cd {FOLDER_OUT}; 7z u {FILE_INPUT}.7z',
                        'Everything is Ok'), 'positive_test4 FAIL'


def test_positive5(start_time, get_list, stat_file):
    save_log(start_time, f'log_test_positive5')
    assert ssh_checkout(f'{HOST}', f'{USER}', f'{PWD}',
                        f'cd {FOLDER_TST}; echo "hello" >> {get_list[1]}; cd {FOLDER_OUT};'
                        f'7z u {FOLDER_TST}/{FILE_INPUT}.7z', 'Everything is Ok'), 'positive_test5 FAIL'


def test_positive6(start_time, stat_file):
    res = [ssh_checkout(f'{HOST}', f'{USER}', f'{PWD}',
                        f'cd {FOLDER_OUT}; 7z l {FILE_INPUT}.7z', 'Physical Size'),
           ssh_checkout(f'{HOST}', f'{USER}', f'{PWD}',
                        f'cd {FOLDER_OUT}; 7z l {FILE_INPUT}.7z', f'{FILE_INPUT}.7z')]
    save_log(start_time, f'log_test_positive6')
    assert all(res), 'positive_test6 FAIL'


def test_positive7(start_time, stat_file):
    res = [ssh_checkout(f'{HOST}', f'{USER}', f'{PWD}',
                        f'cd {FOLDER_X_TST}; 7z a {FOLDER_X_OUT}/{FILE_INPUT}', 'Everything is Ok'),
           ssh_checkout(f'{HOST}', f'{USER}', f'{PWD}',
                        f'cd {FOLDER_X_OUT}; 7z x {FILE_INPUT}.7z -o{FOLDER_X_OUT} -y', 'Everything is Ok'),
           ssh_checkout(f'{HOST}', f'{USER}', f'{PWD}',
                        f'ls {FOLDER_OUT}', f'{FILE_INPUT}')]
    save_log(start_time, f'log_test_positive7')
    assert all(res), 'positive_test7 FAIL'


def test_positive8(start_time, make_file, stat_file):
    res = []
    for i in make_file:
        res.append(ssh_checkout(f'{HOST}', f'{USER}', f'{PWD}',
                                f'cd {FOLDER_TST}; 7z h i', "Everything is Ok"))
        crc = ssh_getout(f'{HOST}', f'{USER}', f'{PWD}',
                          f'cd {FOLDER_TST}; crc32 {i}').upper()
        res.append(ssh_checkout(f'{HOST}', f'{USER}', f'{PWD}',
                                f'cd {FOLDER_TST}; 7z h {i}', crc))
    save_log(start_time, 'log_test_positive8')
    assert all(res), "positive_test8 FAIL"

    # def crc_32(cmd):
    #     crc = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    #     return crc
    # crc_str = crc_32(f'cd {FOLDER_OUT}; crc32 {FILE_INPUT}.7z')
    # crc_up = str(crc_str).upper()
    # crc = crc_up[-23:-15]
    # res_txt = checkout(f'cd {FOLDER_OUT}; 7z h {FILE_INPUT}.7z', 'CRC32  for data')
    # res_crc = checkout(f'cd {FOLDER_OUT}; 7z h {FILE_INPUT}.7z', crc)
    # save_log(start_time, f'log_test_positive8')
    # assert res_txt and res_crc, ''
