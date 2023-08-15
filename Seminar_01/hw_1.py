# Задание 1.
# Условие: Написать функцию на Python, которой передаются в качестве параметров команда и текст.
# Функция должна возвращать True, если команда успешно выполнена и текст найден в её выводе и False в противном случае.
# Передаваться должна только одна строка, разбиение вывода использовать не нужно.

import subprocess

def execute_command(command, text):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, stdout=subprocess.PIPE)
        output = result.stdout
        if text in output:
            return True
        else:
            return False
    except Exception as e:
        print("Error: ", e)
        return False


if __name__ == '__main__':
    command = 'cat /etc/os-relase'
    text = "VERSION = '22.04.2 LTS (Jammy Jellyfish)'"
    if execute_command(command, text):
        print("Команда выполнена успешно, и текст найден")
    else:
        print("Команда не выполнена успешно или текст не найден")

