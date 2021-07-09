# -*- coding:UTF-8 -*-
# auth：NeWolf
# date 20210701
import os
import subprocess
import datetime

PKG_NAME = "com.huawei.ohos.inputmethod"




class monkey(object):
    def __init__(self, whitelist, appname, s, count, t, filename):
        self.whitelist = whitelist
        self.pack = appname
        self.seed = s
        self.count = count
        self.time = t
        self.storage = filename

    def test(self):
        # cmd = 'adb shell monkey ' + self.pack + ' ' + '-s ' + self.seed \
        #       + '--ignore-timeouts --ignore-security-exceptions --kill-process-after-error --pct-trackball 0 ' \
        #         '--pct-nav 0 --pct-anyevent 0 --pct-flip 0 --pct-pinchzoom 0 --pct-syskeys 0 --ignore-crashes -v ' \
        #       + self.count + ' ' + self.time + ' ' + self.storage

        cmd = 'adb shell CLASSPATH=/sdcard/monkey.jar:/sdcard/framework.jar exec app_process ' \
              '/system/bin tv.panda.test.monkey.Monkey ' \
              '-p com.newolf.watchinput -p com.huawei.ohos.inputmethod ' \
              '--running-minutes 60 --throttle 100 --act-whitelist-file ' \
              '/sdcard/awl.strings --uiautomatormix -v -v --output-directory /sdcard/max-output'
        test_monkey = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
        return test_monkey.stdout.read()

def run_monkey(pkg_name):
    # 1200000000
    # 2880000 = 8h
    run = monkey('--pkg-whitelist-file /sdcard/MonkeyLog.txt', '-p com.huawei.ohos.inputmethod', '2880000', '450',
                 '--throttle 500', '>> output/monkey_log.txt')

    start_time = datetime.datetime.now()
    print("run monkey time %s" % start_time)
    print(run.test())

    end_time = datetime.datetime.now()

    run_time = end_time - start_time
    print("monkey end , run time %s " %run_time)


if __name__ == '__main__':
    run_monkey(PKG_NAME)
