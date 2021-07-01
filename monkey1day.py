# -*- coding:UTF-8 -*-
# auth：NeWolf
# date 20210701
import os
import subprocess

PKG_NAME = "com.huawei.ohos.inputmethod"


def execute(cmd):  # 执行adb命令，返回执行的结果
    adb = os.popen(cmd)
    # subprocess.run(cmd)



def run_monkey(pkg_name):
    cmd = 'adb shell monkey -p com.huawei.ohos.inputmethod  -v --throttle 300 --ignore-crashes --ignore-timeouts --monitor-native-crashes 10000000'
    print(cmd)
    execute(cmd)


if __name__ == '__main__':
    run_monkey(PKG_NAME)
