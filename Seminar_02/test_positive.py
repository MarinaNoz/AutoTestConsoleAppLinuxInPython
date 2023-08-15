from checkout import *



def test_positive1():
    res1 = checkout(f"cd {FOLDER_TST}; 7z a ../out/{FILE_INPUT}", "Everything is Ok")
    res2 = checkout(f"ls {FOLDER_OUT}", f"{FILE_INPUT}.7z")
    assert res1 and res2, "positive_test1 FAIL"


def test_positive2():
    res1 = checkout(f"cd {FOLDER_OUT}; 7z e {FILE_INPUT}.7z -o{FOLDER_1} -y", "Everything is Ok")
    res2 = checkout(f"ls {FOLDER_1}", "nod")
    assert res1 and res2, "positive_test2 FAIL"


def test_positive3():
    assert checkout(f"cd {FOLDER_OUT}; 7z t {FILE_INPUT}.7z", "Everything is Ok"), "positive_test3 FAIL"


def test_positive4():
    assert checkout(f"cd {FOLDER_OUT}; 7z d {FILE_INPUT}.7z", "Everything is Ok"), "positive_test4 FAIL"


def test_positive5():
    assert checkout(f"cd {FOLDER_OUT}; 7z u {FILE_INPUT}.7z", "Everything is Ok"), "positive_test5 FAIL"


def test_positive6():
    res1 = checkout(f"cd {FOLDER_OUT}; 7z l {FILE_INPUT}.7z", "Physical Size"),
    res2 = checkout(f"cd {FOLDER_OUT}; 7z l {FILE_INPUT}.7z", f"{FILE_INPUT}.7z")
    assert res1 and res2, "positive_test6 FAIL"


def test_positive7():
    res1 = checkout(f"cd {FOLDER_OUT}; 7z x {FILE_INPUT}.7z -o{FOLDER_X} -y", "Everything is Ok")
    res2 = checkout(f"ls {FOLDER_1}", "nod")
    assert res1 and res2, "positive_test7 FAIL"


def test_positive8():
    def crc_32(cmd):
        crc = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        return crc
    crc = crc_32(f"cd {FOLDER_OUT}; crc32 {FILE_INPUT}.7z")
    crc2 = str(crc).upper()
    crc3 = crc2[-23:-15]
    res1 = checkout(f"cd {FOLDER_OUT}; 7z h {FILE_INPUT}.7z", "CRC32  for data")
    res2 = checkout(f"cd {FOLDER_OUT}; 7z h {FILE_INPUT}.7z", crc3)
    assert res1 and res2, "positive_test8 FAIL"
