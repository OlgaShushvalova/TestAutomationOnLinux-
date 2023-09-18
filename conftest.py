import random
import string
import yaml
import pytest as pytest
from checks import checkout, getout
from datetime import datetime
from sshcheckers import ssh_checkout

with open('config.yaml') as fy:
    data = yaml.safe_load(fy)


@pytest.fixture()
def make_folder():
    return ssh_checkout(data["ip"], data["user"], data["passwd"],
        f'mkdir -p {data["folder_in"]} {data["folder_out"]} {data["folder_ext"]} {data["folder_ext3"]} {data["folder_bad"]}',
        "", True)


@pytest.fixture()
def clear_folder():
    return ssh_checkout(data["ip"], data["user"], data["passwd"],
        f'rm -rf {data["folder_in"]}/* {data["folder_out"]}/* {data["folder_ext"]}/* {data["folder_ext3"]}/* {data["folder_bad"]}/*',
        "", True)


@pytest.fixture()
def make_files():
    list_files = []
    for i in range(data['count']):
        file_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
        ssh_checkout(data["ip"], data["user"], data["passwd"], f'cd {data["folder_in"]}; dd if=/dev/urandom of={file_name} bs={data["bs"]} count=1 iflag=fullblock',
                 "", True)
        list_files.append(file_name)

    return list_files


@pytest.fixture()
def make_subfolder():
    subfolder_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfile_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
    if not ssh_checkout(data["ip"], data["user"], data["passwd"], f'cd {data["folder_in"]}; mkdir {subfolder_name}', "", True):
        return None, None
    if not ssh_checkout(data["ip"], data["user"], data["passwd"], f'cd {data["folder_in"]}/{subfolder_name}; '
                    f'dd if=/dev/urandom of={subfile_name} bs={data["bs"]} count=1 iflag=fullblock', "", True):
        return subfolder_name, None

    return subfolder_name, subfile_name


@pytest.fixture()
def create_bad_archive():
    ssh_checkout(data["ip"], data["user"], data["passwd"], f'cd {data["folder_in"]}; 7z a {data["folder_out"]}/arx2', "Everything is Ok", True)
    ssh_checkout(data["ip"], data["user"], data["passwd"], f'cp {data["folder_out"]}/arx2.7z {data["folder_bad"]}', "", True)
    ssh_checkout(data["ip"], data["user"], data["passwd"], f'truncate -s 1 {data["folder_bad"]}/arx2.7z', "", True)  # сделали битым


@pytest.fixture(autouse=True)
def speed():
    print(datetime.now().strftime('%H:%M:%S.%f'))
    yield
    print(datetime.now().strftime('%H:%M:%S.%f'))


@pytest.fixture(autouse=True)
def stat():
    yield
    stat = getout("cat /proc/loadavg")
    ssh_checkout(data["ip"], data["user"], data["passwd"], "echo 'time: {} count:{} size: {} load: {}'>> stat.txt".format(datetime.now().strftime("%H:%M:%S.%f"), data["count"], data["bs"], stat), "", True)


