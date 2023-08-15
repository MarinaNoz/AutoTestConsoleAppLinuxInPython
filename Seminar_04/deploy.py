from sshcheckers import ssh_checkout, upload_files


def deploy():
    res = []
    upload_files('0.0.0.0', 'usertest', 'qwerty', 'test_ssh/p7zip-full.deb',
                 '/home/usertest/p7zip-full.deb')
    res.append(ssh_checkout('0.0.0.0', 'usertest', 'qwerty',
                            'echo "qwerty" | sudo -S dpkg -i /home/usertest/p7zip-full.deb', 'Настраивается пакет'))
    res.append(ssh_checkout('0.0.0.0', 'usertest', 'qwerty',
                            'echo "qwerty" | sudo -S dpkg -s p7zip-full', 'Status: install ok installed'))
    return all(res)


if __name__ == '__main__':
    if deploy():
        print('Деплой успешен')
    else:
        print('Ошибка деплоя')
