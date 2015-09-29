# -*- coding: UTF-8 -*-
__author__ = 'jxs'

import threading
import os
import os.path
import datetime as datetime

NEXT_TIMES = 1.0
ROOT_PATH = '/Users/jxs/Desktop/app/'
RENAME_PATH = '/Users/jxs/Desktop/rename.txt'
TOGGER_MODE = ('SCAN', 'RENAME')
LIMITED_FILE_NAME_LEN = 1
mode = TOGGER_MODE[0]


def timer():
    if mode == TOGGER_MODE[0]:
        scan_file()  # 扫描文件
    elif mode == TOGGER_MODE[1]:
        read_file()
    global next_thd  # Notice: use global variable!
    next_thd = threading.Timer(NEXT_TIMES, timer)
    next_thd.start()


def scan_file():
    for parent, dirnames, filenames in os.walk(ROOT_PATH):  # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
        for filename in filenames:  # 输出文件信息
            if filename.__len__() > LIMITED_FILE_NAME_LEN:
                abspath = os.path.join(parent, filename)  # 输出文件路径信息
                src = abspath.replace(ROOT_PATH, '')
                ac = os.path.splitext(src)
                if ac.__len__() == 2:
                    print ac
                    if ac[1].strip().__len__() > 0:
                        print 'filename is [%s] %s ' % (ac[0], filename)
                        dst_name = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f') + ac[1];
                        dst = abspath.replace(ROOT_PATH, '').replace(filename, dst_name)
                        rename_file(src, dst)
                        append_file(src, dst)


def append_file(src, dst):
    # if os.path.exists(FILE_PATH):
    fp = open(RENAME_PATH, 'a')
    line = src + ';' + dst + '\n'
    print 'line is: %s' % line
    fp.write(line)
    fp.close()


'''读文件 '''


def read_file():
    print 'come in ...' + mode
    if os.path.exists(RENAME_PATH):
        fp = open(RENAME_PATH, 'r')
        file_list = fp.readlines()
        for file_line in file_list:
            splits = file_line.split(';')
            if splits.__len__() == 2:
                rename_file(splits[0], splits[1]);
        fp.close()


def rename_file(src, dst):
    src = ROOT_PATH + src
    dst = ROOT_PATH + dst
    if os.path.exists(src) and not os.path.exists(dst):
        os.rename(src, dst)


if __name__ == "__main__":
    # scan_file()
    next_thd = threading.Timer(NEXT_TIMES, timer)
    next_thd.start()
