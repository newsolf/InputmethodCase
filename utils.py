# -*- coding: utf-8 -*-
import os
import os.path
import shutil


def get_filename(path):
    p = path.rfind("/")
    if (p != -1):
        return path[p + 1:len(path)]

    return path


def get_dir(path):
    p = path.rfind("/")
    if (p != -1):
        return path[0: p]

    return path


def copy_file(srcFile, targetFile):
    create_parent_folder(targetFile)
    shutil.copy(srcFile, targetFile)


def create_parent_folder(file):
    dir = get_dir(file)
    if (os.path.exists(dir) == False):
        os.makedirs(dir)


def create_folder(dir):
    if (os.path.exists(dir) == False):
        os.makedirs(dir)


def read_values_from_file(file):
    print(file)
    values = {}
    fo = open(file, "r")
    lines = fo.readlines()
    for line in lines:
        parts = line.split(":")
        if len(parts) == 2:
            key = parts[0].strip()
            value = parts[1].strip()
            if len(key) > 0 and len(value) > 0:
                values[key] = value
    fo.close()
    return values
