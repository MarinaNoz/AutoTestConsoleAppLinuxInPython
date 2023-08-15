from checkout import *


def test_negative1():
    assert checkout(f"cd {FOLDER_OUT}; 7z e bad_arh.7z -o{FOLDER_1} -y", "Is not archive"), "negative_test1 FAIL"



def test_negative2():
    assert checkout(f"cd {FOLDER_OUT}; 7z t bad_arh.7z", "Can not open the file as [7z] archive"), \
        "negative_test2 FAIL"
