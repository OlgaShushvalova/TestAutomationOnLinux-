# Задание 1.
# Переделать все шаги позитивных тестов на выполнение по SSH. Проверить работу.

import yaml
from checks import checkout, check_hash_crc32
from sshcheckers import ssh_checkout
import pytest

with open('config.yaml') as fy:
    data = yaml.safe_load(fy)


class TestPositive:

    def test_add_archive(self, make_folder, clear_folder, make_files):  # a создали архив
        res = list()
        res.append(ssh_checkout(data["ip"], data["user"], data["passwd"],
                                f'cd {data["folder_in"]}; 7z a {data["folder_out"]}/arx2', "Everything is Ok"))
        res.append(ssh_checkout(data["ip"], data["user"], data["passwd"], f'ls {data["folder_out"]}', "arx2.7z"))
        assert all(res)

    def test_check_e_extract(self, clear_folder, make_files):  #
        res = list()
        res.append(ssh_checkout(data["ip"], data["user"], data["passwd"], f'cd {data["folder_in"]}; 7z a {data["folder_out"]}/arx2', "Everything is Ok", True))
        res.append(ssh_checkout(data["ip"], data["user"], data["passwd"], f'cd {data["folder_out"]}; 7z e arx2.7z -o{data["folder_ext"]} -y', "Everything is Ok", True))
        for item in make_files:
            res.append(ssh_checkout(data["ip"], data["user"], data["passwd"], f'ls {data["folder_ext"]}', item, True))

        assert all(res)

    def test_check_e_extract_subfolder(self, clear_folder, make_files, make_subfolder):
        res = list()
        res.append(ssh_checkout(data["ip"], data["user"], data["passwd"], f'cd {data["folder_in"]}; 7z a {data["folder_out"]}/arx2', "Everything is Ok", True))
        res.append(ssh_checkout(data["ip"], data["user"], data["passwd"], f'cd {data["folder_out"]}; 7z e arx2.7z -o{data["folder_ext"]} -y', "Everything is Ok", True))
        for item in make_files:
            res.append(ssh_checkout(data["ip"], data["user"], data["passwd"], f'ls {data["folder_ext"]}', item, True))
        for item in make_subfolder:
            res.append(ssh_checkout(data["ip"], data["user"], data["passwd"], f'ls {data["folder_ext"]}', item, True))

        assert all(res)

    def test_check_x_extract_subfolder(self, clear_folder, make_files, make_subfolder):
        res = list()
        res.append(ssh_checkout(data["ip"], data["user"], data["passwd"], f'cd {data["folder_in"]}; 7z a {data["folder_out"]}/arx2', "Everything is Ok", True))
        res.append(ssh_checkout(data["ip"], data["user"], data["passwd"], f'cd {data["folder_out"]}; 7z x arx2.7z -o{data["folder_ext"]} -y', "Everything is Ok", True))
        for item in make_files:
            res.append(ssh_checkout(data["ip"], data["user"], data["passwd"], f'ls {data["folder_ext"]}', item, True))

        res.append(ssh_checkout(data["ip"], data["user"], data["passwd"], f'ls {data["folder_ext"]}', make_subfolder[0], True))
        res.append(ssh_checkout(data["ip"], data["user"], data["passwd"], f'ls {data["folder_ext"]}/{make_subfolder[0]}', make_subfolder[1], True))

        assert all(res)

    def test_check_x_files(self, clear_folder, make_files):  # only files
        res = list()
        res.append(ssh_checkout(data["ip"], data["user"], data["passwd"], f'cd {data["folder_in"]}; 7z a {data["folder_out"]}/arx2', "Everything is Ok", True))
        res.append(ssh_checkout(data["ip"], data["user"], data["passwd"], f'cd {data["folder_out"]}; 7z x arx2.7z -o{data["folder_ext"]} -y', "Everything is Ok", True))
        for item in make_files:
            res.append(ssh_checkout(data["ip"], data["user"], data["passwd"], f'ls {data["folder_ext"]}', item, True))
        assert all(res)

    def test_totality(self, clear_folder, make_files):  # t проверка целостности архива
        res = list()
        res.append(ssh_checkout(data["ip"], data["user"], data["passwd"], f'cd {data["folder_in"]}; 7z a {data["folder_out"]}/arx2', "Everything is Ok", True))
        res.append(ssh_checkout(data["ip"], data["user"], data["passwd"], f'cd {data["folder_out"]}; 7z t arx2.7z', "Everything is Ok", True))

        assert all(res)

    def test_delete(self, clear_folder, make_files, make_subfolder):  # d удаление из архива
        res = list()
        res.append(ssh_checkout(data["ip"], data["user"], data["passwd"], f'cd {data["folder_in"]}; 7z a {data["folder_out"]}/arx2', "Everything is Ok", True))
        res.append(ssh_checkout(data["ip"], data["user"], data["passwd"], f'cd {data["folder_out"]}; 7z d arx2.7z', "Everything is Ok", True))

        assert all(res)

    def test_update(self):  # u - обновление архива
        assert ssh_checkout(data["ip"], data["user"], data["passwd"], f'cd {data["folder_in"]}; 7z u {data["folder_out"]}/arx2.7z', "Everything is Ok", True), 'NO update'

    def test_nonempty_archive(self, clear_folder, make_files):
        res = list()
        res.append(ssh_checkout(data["ip"], data["user"], data["passwd"], f'cd {data["folder_in"]}; 7z a {data["folder_out"]}/arx2', "Everything is Ok", True))
        res.append(ssh_checkout(data["ip"], data["user"], data["passwd"], f'cd {data["folder_out"]}; 7z l arx2.7z', f'{len(make_files)} files', True))

    def test_check_hash(self):
        hash_crc32 = check_hash_crc32(f'cd {data["folder_out"]}; crc32 arx2.7z')
        res_upper = ssh_checkout(data["ip"], data["user"], data["passwd"], f'cd {data["folder_out"]}; 7z h arx2.7z', hash_crc32.upper(), True)
        res_lower = ssh_checkout(data["ip"], data["user"], data["passwd"], f'cd {data["folder_out"]}; 7z h arx2.7z', hash_crc32.lower(), True)
        assert res_lower or res_upper, 'NO equal hash'


if __name__ == '__main__':
    pytest.main(['-vv'])