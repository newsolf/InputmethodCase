# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import re
import os


def execute(cmd):  # 执行adb命令，返回执行的结果
    adb = os.popen(cmd)
    line = adb.readlines()
    adb.close()
    return line


def print_hi(name):
    cmd_threads_name = "adb shell ps -T -p " + str(18442)
    threads_info = execute(cmd_threads_name)
    threads_name = ''
    size = len(threads_info)
    for i in range(1, size):
        line = threads_info[i].strip()
        parts = re.split("\s+", line)
        if i == size - 1:
            threads_name += parts[9]
        else:
            threads_name += parts[9] + "\n"

    print(threads_name)
    print("end")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
