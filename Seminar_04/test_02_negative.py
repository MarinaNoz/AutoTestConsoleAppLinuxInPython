from conftest import *
from sshcheckers import *



def test_negative1(start_time, clear_dir, make_dir, make_file, get_bad_file, stat_file):
    save_log(start_time, f'log_test_negative1')
    assert ssh_check_negative(f'{HOST}', f'{USER}', f'{PWD}',
                              f'cd {FOLDER_OUT}; 7z e arxbad.7z -o{FOLDER_TARG} -y',
                              'Is not archive'), 'negative_test1 FAIL'



def test_negative2(get_bad_file, stat_file):
    save_log(start_time, f'log_test_negative2')
    assert ssh_check_negative(f'{HOST}', f'{USER}', f'{PWD}',
                              f'cd {FOLDER_OUT}; 7z t arxbad.7z',
                              'Can not open the file as [7z] archive'), 'negative_test2 FAIL'


def test_undeploy(start_time, stat_file, clear_dir):
    res = []
    res.append(ssh_checkout(f'{HOST}', f'{USER}', f'{PWD}',
                            'echo "qwerty" | sudo -S dpkg -r p7zip-full', 'Удаляется p7zip-full'))
    res.append(ssh_checkout('0.0.0.0', 'usertest', 'qwerty',
                            'echo "qwerty" | sudo -S dpkg -s p7zip-full', 'deinstall ok config-files'))
    save_log(start_time, f'log_test_deploy')
    assert all(res), 'test_undeploy FAIL'


# def test_negative1():
#     assert checkout(f"cd {FOLDER_4BAD}; 7z e bad_arh.7z -o{FOLDER_TARG} -y", "Is not archive"), "negative_test1 FAIL"
#
#
# def test_negative2():
#     assert checkout(f"cd {FOLDER_4BAD}; 7z t bad_arh.7z", "Can not open the file as [7z] archive"), \
#         "negative_test2 FAIL"
