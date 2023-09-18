# Задание 2. (дополнительное задание)
# Переделать все шаги негативных тестов на выполнение по SSH. Проверить работу.

import pytest
from sshcheckers import ssh_checkout
import yaml

with open('config.yaml') as fy:
    data = yaml.safe_load(fy)


class TestNegative:
    def test_negative1(self, make_folder, clear_folder, make_files, create_bad_archive):  # e извлекли из архива

        assert ssh_checkout(data["ip"], data["user"], data["passwd"], f'cd {data["folder_bad"]}; 7z e arx2.7z -o{data["folder_ext"]} -y', "ERRORS", False)

    def test_negative2(self, make_folder, clear_folder, make_files,
                       create_bad_archive):  # t проверка целостности архива
        assert ssh_checkout(data["ip"], data["user"], data["passwd"], f'cd {data["folder_bad"]}; 7z t arx2.7z', "Is not", False)



if __name__ == '__main__':
    pytest.main(['-vv'])