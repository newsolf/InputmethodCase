# -*- coding:UTF-8 -*-
# auth：NeWolf
# date 20210701

import datetime
import re
import time
import os

import xlwt as xlwt

# PKG_NAME = "com.baidu.input"
PKG_NAME = "com.huawei.ohos.inputmethod"


def log(out):
    print(out)


def execute(cmd):  # 执行adb命令，返回执行的结果
    adb = os.popen(cmd)
    line = adb.readlines()
    adb.close()
    return line


def get_pid(pkg_name):
    cmd = "adb shell ps | grep " + pkg_name
    info = execute(cmd)

    print("info = %s" % info)

    for i in range(len(info)):
        line = info[i].strip()
        print("line = %s" % line)
        if line.endswith(pkg_name):
            parts = re.split("\s+", line)
            print("parts = %s" % parts)
            return int(parts[1])

    return 0


def get_threads():
    pid = get_pid(PKG_NAME)
    if pid == 0:
        print('pid == 0,无法继续')
        return
    pre_pid = pid
    cmd = "adb shell cat proc/" + str(pid) + "/status"
    # print(cmd)
    list = execute(cmd)
    # print(list)

    file_name = "output/" + get_current_time() + "_" + str(pid) + ".txt"

    create_parent_folder(file_name)
    print('创建文件 %s ' % file_name)

    f = open(file_name, 'a+')
    result = xlwt.Workbook()
    result_sheet = result.add_sheet(str(pid))  # 写sheet name
    result_title = ['Time', 'Pid', 'threads', 'threadsName']
    result_cols = 0
    for row_result in range(len(result_title)):
        result_sheet.write(result_cols, row_result, result_title[row_result])  # 写标题
    # f.write(get_current_time() + "\n")
    # f.write("pid = %s \n" % pid)
    thread_max = 0
    thread_min = 0
    thread_avg = 0
    thread_total = 0
    thread_count = 0

    for i in range(len(list)):
        s = list[i]
        # print(s)
        if s.startswith('Threads'):
            parts = re.split("\s+", s)
            thread_count = int(parts[1].strip())
            thread_max = thread_count
            thread_min = thread_count
            thread_total = thread_count
            f.write("%s pid:%i %s" % (get_current_time(), pid, s))
    # f.close()
    retry_count = 0
    stats_count = 1

    while True:
        info = execute(cmd)
        # print (info)
        if len(info) == 0:
            pid = get_pid(PKG_NAME)
            retry_count += 1
            if pid == 0:
                print('pid == 0,无法继续')
                if retry_count > 3:
                    # set max min avg
                    thread_avg = thread_total / thread_count
                    out = "statsCount:%s max:%s min:%s avg: %s" % (stats_count, thread_max, thread_min, thread_avg)
                    print(out)
                    f.write(out)

                    result_cols += 1
                    result_sheet.write(result_cols, 0, "stats: %s, by NeWolf" % out)
                    result_file_name = "output/%s_%d_%d.xls" % (PKG_NAME, pre_pid, stats_count)
                    result.save(result_file_name)
                    break
                time.sleep(5)
                continue

            pre_pid = pid

            cmd = "adb shell cat proc/" + str(pid) + "/status"
            f.write("pid = %i \n" % pid)
            continue

        f = open(file_name, 'a+')
        # f.write(get_current_time() + "\n")
        # print (info)
        if pid == 0:
            continue
        stats_count += 1
        threads_name = get_threads_name(pid)

        for i in range(len(info)):
            item = info[i]
            if item.startswith('Threads'):
                out = "%s pid:%i %s" % (get_current_time(), pid, item)
                parts = re.split("\s+", item)
                thread_count = int(parts[1].strip())
                if thread_count > thread_max:
                    thread_max = thread_count
                if thread_count < thread_min:
                    thread_min = thread_count
                thread_total += thread_count
                print(out)
                f.write(out)

                threads_stats = [get_current_time(), pid, thread_count, threads_name]
                result_cols += 1
                for row_result in range(len(threads_stats)):
                    result_sheet.write(result_cols, row_result, threads_stats[row_result])
                break
        time.sleep(1)
    f.close()


def get_threads_name(pid):
    if pid == 0:
        return ""
    cmd_threads_name = "adb shell ps -T -p " + str(pid)
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
    # print(threads_name)

    return threads_name


def get_current_time():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def create_parent_folder(file):
    dir_path = get_dir(file)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def get_dir(path):
    p = path.rfind("/")
    if p != -1:
        return path[0: p]

    return path


if __name__ == '__main__':
    get_threads()
