# Дополнить проект тестами, проверяющими команды вывода списка файлов (l) и
# разархивирования с путями (x).

import subprocess


def checkout(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    if text in result.stdout and result.returncode == 0:
        return True
    else:
        return False


folderin = "/home/olga/tst"
folderout = "/home/olga/out"


def test_step1():
    assert checkout(f"cd {folderin}; 7z a {folderout}/arx2", "Everything is Ok"), "test1 FAIL"
    assert test_step2(), "test2 FAIL"
    assert test_step3(), "test3 FAIL"


def test_step2():
    cmd = f"cd {folderin}; 7z l {folderout}/arx2"
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    if "test1.txt" in result.stdout and "test2.txt" in result.stdout and result.returncode == 0:
        return True
    else:
        return False


def test_step3():
    cmd = f"cd {folderin}; 7z x {folderout}/arx2"
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    if "Everything is Ok" in result.stdout and result.returncode == 0:
        return True
    else:
        return False
