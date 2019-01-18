#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# @Author: xiaochenghua
# @Date: 2019/01/11

import os
import hashlib
import sys
import getopt
import random
import json


def __check_icon_path(path):
    if not os.path.isdir(path):
        print('Path:[%s] is not a dir!' % path)
        sys.exit(-2)
    elif not os.path.exists(path):
        print('Path:[%s] is not exists!' % path)
        sys.exit(-3)
    return path


def __check_export_file(file):
    if os.path.isdir(file):
        print('File:[%s] is not ALLOW a dir!' % file)
        sys.exit(-4)
    elif not os.path.exists(os.path.dirname(file)):
        print('Path:[%s] is not exists!' % os.path.dirname(file))
        sys.exit(-5)

    # 如果已经存在文件，将其重命名备份
    if os.path.exists(file):
        # 不确保重新命名是唯一，有重复概率
        os.rename(file, '%s%s%s' % (os.path.splitext(file)[-2], random.randint(1, 100), os.path.splitext(file)[-1]))
    return file


# 找出给定目录下所有扩展名为.png和.jpg的文件
def __icons_paths(icon_path):
    icons_paths = []
    for parent, dirnames, filenames in os.walk(icon_path):
        for filename in filenames:
            if os.path.splitext(filename)[-1] not in ('.png', '.jpg'):
                continue
            icons_paths.append(os.path.join(parent, filename))
    return icons_paths


def __md5_dict(*args):
    md5_dict = {}
    for icon_path in args:
        md5_string = hashlib.md5(open(icon_path, 'rb').read()).hexdigest()
        if md5_string in md5_dict.keys() and isinstance(md5_dict[md5_string], list):
            md5_dict[md5_string].append(os.path.basename(icon_path))
        else:
            md5_dict[md5_string] = [os.path.basename(icon_path)]
    return md5_dict


def __write_to_file(file, **kwargs):
    # 过滤掉字典值数组个数为1个的(取出的就是有重复的图片)
    repeat_icon_dict = {}
    repeat_icons = [kwargs[i] for i in kwargs if len(kwargs[i]) > 1]
    repeat_icon_dict['count'] = len(repeat_icons)
    repeat_icon_dict['icons'] = repeat_icons

    try:
        with open(file, 'w') as f:
            f.write(json.dumps(repeat_icon_dict, indent=4))
    except IOError as e:
        print(e.msg)
        sys.exit(-6)


def __search_repeat_icon():
    icon_path = ''
    export_file = ''

    if len(sys.argv) > 1:
        # 解析命令行
        try:
            opts, args = getopt.getopt(sys.argv[1:], 'hp:e:h:')
        except getopt.GetoptError as e:
            print(e.msg)
            sys.exit(-1)

        # -p -e -h
        for opt, arg in opts:
            if opt == '-p':
                icon_path = __check_icon_path(arg)
            elif opt == '-e':
                export_file = __check_export_file(arg)
            elif opt == '-h':
                print('Usage: python3 %s -p iconPath -e exportFile' % os.path.basename(sys.argv[0]))
                exit()
    else:
        # 根据控制台输入得到数据
        icon_path = __check_icon_path(input('Please type out path: \n').strip())
        export_file = __check_export_file(input('Please type out file: \n').strip())

    # 获取每个icon文件的md5
    icons_info = __md5_dict(*__icons_paths(icon_path))

    # 将字典写入文件
    __write_to_file(export_file, **icons_info)

    # 打印日志
    print('%s\n🎁🎁🎁 Successfully!! Export file is:[%s]' % ('-'*80, export_file))

if __name__ == "__main__":
    __search_repeat_icon()
    exit()
