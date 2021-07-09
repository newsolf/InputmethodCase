# -*- coding:UTF-8 -*-
# auth：NeWolf
# date 20210707
import os
import datetime
import time


def execute(cmd):  # 执行adb命令，返回执行的结果
    adb = os.popen(cmd)
    line = adb.readlines()
    adb.close()
    return line


def get_current_time():
    return datetime.datetime.now().strftime('%Y%m%d%H%M%S')


def get_dir_name():
    return datetime.datetime.now().strftime('%Y%m%d')


def create_parent_folder(file):
    dir_path = get_dir(file)
    print('dir_path %s' % dir_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print('make dir dir_path')


def get_dir(path):
    p = path.rfind("/")
    if p != -1:
        return path[0: p]

    return path


def picc():
    dir_name = get_dir_name()
    # 检查目录，创建目录 ~/Screencapture/{dir_name}
    dir_path = os.path.join('output', dir_name)
    dir_path = dir_name
    # print('dir_path is %s ' % dir_path)
    create_parent_folder(dir_name)
    picc_count = 0

    while True:
        if picc_count > 1200:
            break
        # 截图到手机
        cmd = 'adb shell /system/bin/screencap -p /sdcard/screenshot.png'
        execute(cmd)
        # 拉图到目录下
        file_name = '%s.png' % get_current_time()
        cmd = 'adb pull /sdcard/screenshot.png ' + dir_path + '/' + file_name
        print('cmd  %s ' % cmd)
        execute(cmd)
        picc_count += 1

        time.sleep(1)


if __name__ == '__main__':
    picc()
