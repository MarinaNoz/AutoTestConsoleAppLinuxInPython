from conftest import *


def test_positive1(clear_dir, get_dir, make_file, stat_file):
    res1 = checkout(f"cd {FOLDER_TST}; 7z a {FOLDER_OUT}/{FILE_INPUT}", "Everything is Ok")
    res2 = checkout(f"ls {FOLDER_OUT}", f"{FILE_INPUT}.7z")
    assert res1 and res2, "positive_test1 FAIL"


def test_positive2(clear_dir, get_dir, make_file, stat_file):
    res = [checkout(f"cd {FOLDER_TST}; 7z a {FOLDER_OUT}/{FILE_INPUT}", "Everything is Ok"),
           checkout(f"cd {FOLDER_OUT}; 7z e {FILE_INPUT}.7z -o{FOLDER_TARG} -y", "Everything is Ok")]
    for i in make_file:
        res.append(checkout(f'ls {FOLDER_TARG}', i))
    assert all(res), "positive_test2 FAIL"


def test_positive3(stat_file):
    assert checkout(f"cd {FOLDER_OUT}; 7z t {FILE_INPUT}.7z", "Everything is Ok"), "positive_test3 FAIL"


def test_positive4(get_list, stat_file):
    print(get_list)
    assert checkout(f"cd {FOLDER_OUT}; 7z d {FILE_INPUT}.7z {get_list[0]}", "Everything is Ok"), "positive_test4 FAIL"


def test_positive5(get_list, stat_file):
    assert checkout(f"cd {FOLDER_TST}; echo 'hello' >> {get_list[1]}; cd {FOLDER_OUT}; "
                    f"7z u {FOLDER_TST}/{FILE_INPUT}.7z", "Everything is Ok"), "positive_test5 FAIL"


def test_positive6(stat_file):
    res1 = checkout(f"cd {FOLDER_OUT}; 7z l {FILE_INPUT}.7z", "Physical Size"),
    res2 = checkout(f"cd {FOLDER_OUT}; 7z l {FILE_INPUT}.7z", f"{FILE_INPUT}.7z")
    assert res1 and res2, "positive_test6 FAIL"


def test_positive7(stat_file):

    res1 = checkout(f"cd {FOLDER_X_TST}; 7z a {FOLDER_X_OUT}/{FILE_INPUT}", "Everything is Ok")
    res2 = checkout(f"cd {FOLDER_X_OUT}; 7z x {FILE_INPUT}.7z -o{FOLDER_X_OUT} -y", "Everything is Ok")
    res3 = checkout(f"ls {FOLDER_OUT}", f"{FILE_INPUT}")
    assert res1 and res2 and res3, "positive_test7 FAIL"


def test_positive8(stat_file):
    def crc_32(cmd):
        crc = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        return crc
    crc_str = crc_32(f"cd {FOLDER_OUT}; crc32 {FILE_INPUT}.7z")
    crc_up = str(crc_str).upper()
    crc = crc_up[-23:-15]
    res_txt = checkout(f"cd {FOLDER_OUT}; 7z h {FILE_INPUT}.7z", "CRC32  for data")
    res_crc = checkout(f"cd {FOLDER_OUT}; 7z h {FILE_INPUT}.7z", crc)
    assert res_txt and res_crc, "positive_test8 FAIL"
