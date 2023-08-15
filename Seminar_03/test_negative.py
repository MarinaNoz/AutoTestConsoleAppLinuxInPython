from conftest import *



def test_negative1(get_bad_file, stat_file):
    assert checkout(f"cd {FOLDER_OUT}; 7z e arxbad.7z -o{FOLDER_TARG} -y", "Is not archive"), "negative_test1 FAIL"


def test_negative2(get_bad_file, stat_file):
    assert checkout(f"cd {FOLDER_OUT}; 7z t arxbad.7z", "Can not open the file as [7z] archive"), \
        "negative_test2 FAIL"



# def test_negative1():
#     assert checkout(f"cd {FOLDER_4BAD}; 7z e bad_arh.7z -o{FOLDER_TARG} -y", "Is not archive"), "negative_test1 FAIL"
#
#
# def test_negative2():
#     assert checkout(f"cd {FOLDER_4BAD}; 7z t bad_arh.7z", "Can not open the file as [7z] archive"), \
#         "negative_test2 FAIL"