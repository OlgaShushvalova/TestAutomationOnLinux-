from sshcheckers import ssh_checkout, upload_files
import yaml

with open('config.yaml') as fy:
    data = yaml.safe_load(fy)


def deploy():
    res = []
    upload_files(data["ip"], data["user"], data["passwd"], data["local-path"], data["remote-path"])
    res.append(ssh_checkout(data["ip"], data["user"], data["passwd"],
                            f"echo {data['passwd']} | sudo -S dpkg -i {data['remote-path']}",
                            "Настраивается пакет"))
    res.append(ssh_checkout(data["ip"], data["user"], data["passwd"],
                            f"echo {data['passwd']} | sudo -S dpkg -s {data['package']}",
                            "Status: install ok installed"))
    return all(res)


if deploy():
    print("Деплой успешен")
else:
    print("Ошибка деплоя")
