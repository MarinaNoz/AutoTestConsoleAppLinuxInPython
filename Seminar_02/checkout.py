import subprocess

FOLDER_TST = "/home/marina/tst"
FOLDER_OUT = "/home/marina/out"
FOLDER_X = "/home/marina/folder_x"
FOLDER_1 = "/home/marina/folder1"
# FILE_INPUT = "arh_1"
FILE_INPUT = "arx2"

def checkout(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    if text in result.stdout and result.returncode == 0 or text in result.stderr:
        return True
    else:
        return False
