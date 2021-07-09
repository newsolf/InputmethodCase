# -*- coding:UTF-8 -*-
# auth：NeWolf
# date 20210701

import datetime
import glob
import re
import time
import os

import xlwt as xlwt
import xlrd
from xlutils.copy import copy

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


def restart_process():
    # 其他输入法的时候，需要重写这个方法
    cmd = 'adb shell am start -n %s/com.appstore.view.activity.PrimaryActivity' % PKG_NAME
    execute(cmd)


def get_threads():
    pid = get_pid(PKG_NAME)
    if pid == 0:
        print('pid == 0,无法继续')
        return
    pre_pid = pid
    cmd = "adb shell cat proc/" + str(pid) + "/status"
    # print(cmd)
    list_info = execute(cmd)
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

    result_file_name = "output/%s_%d.xls" % (PKG_NAME, pre_pid)
    result.save(result_file_name)

    # f.write(get_current_time() + "\n")
    # f.write("pid = %s \n" % pid)
    thread_max = 0
    thread_min = 0
    thread_avg = 0
    thread_total = 0
    thread_count = 0

    for i in range(len(list_info)):
        s = list_info[i]
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
            if retry_count == 0:
                retry_start_time = time.time()
            restart_process()
            pid = get_pid(PKG_NAME)
            retry_count += 1
            if pid == 0:
                print('pid == 0,无法继续 retry %d time:%s' % (retry_count, datetime.datetime.now()))
                if retry_count > 3:
                    retry_end_time = time.time()
                    retry_use_time = retry_end_time - retry_start_time
                    print('retry_use_time %.2f s,and retry finished!!' % retry_use_time)
                    # set max min avg
                    thread_avg = thread_total / stats_count
                    out = "statsCount:%s max:%s min:%s avg: %s" % (stats_count, thread_max, thread_min, thread_avg)
                    print(out)
                    f.write(out)
                    try:
                        new_file = switch_to_append_model(result_file_name, result_sheet)
                        result_sheet = new_file[0]
                        new_work_book = new_file[1]

                        result_cols += 1
                        result_sheet.write(result_cols, 0, "stats: %s, by NeWolf" % out)
                        new_work_book.save(result_file_name)
                    except Exception as e:
                        print(e)
                    break
                else:
                    time.sleep(5)
                    continue

            # pre_pid = pid
            retry_count = 0
            print("retry get pid %d " % pid)
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
                new_file = switch_to_append_model(result_file_name, result_sheet)
                result_sheet = new_file[0]
                new_work_book = new_file[1]
                result_cols += 1
                for row_result in range(len(threads_stats)):
                    result_sheet.write(result_cols, row_result, threads_stats[row_result])
                new_work_book.save(result_file_name)
                break
        time.sleep(1)
    f.close()


def switch_to_append_model(result_file_name, result_sheet):
    word_book = xlrd.open_workbook(result_file_name)
    # 获取所有的sheet表单。
    sheets = word_book.sheet_names()
    # 获取第一个表单
    work_sheet = word_book.sheet_by_name(sheets[0])
    # 获取已经写入的行数
    # old_rows = work_sheet.nrows
    # 获取表头信息
    # heads = work_sheet.row_values(0)
    # 将xlrd对象变成xlwt
    new_work_book = copy(word_book)
    # 添加内容
    result_sheet = new_work_book.get_sheet(0)
    new_file = [result_sheet, new_work_book]
    return new_file


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
