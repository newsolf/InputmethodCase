# -*- coding:UTF-8 -*-
# auth：NeWolf
# date 202107029

from urllib.request import urlopen

BD = 'http://www.baidu.com'
def request_baidu():
    for line in urlopen(BD):
        line = line.decode('utf-8')  # Decoding the binary data to text.
        print(line)
    if 'EST' in line or 'EDT' in line:  # look for Eastern Time
        print(line)


if __name__ == '__main__':
    request_baidu()