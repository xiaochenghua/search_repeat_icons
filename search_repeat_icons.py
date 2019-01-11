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


def search_repeat_icon():
    icon_path = ''
    output_file = ''

    if len(sys.argv) > 1:
        # 解析命令行
        try:
            opts, args = getopt.getopt(sys.argv[1:], 'hp:o:h:')
        except getopt.GetoptError as e:
            print(e.msg)
            sys.exit(-1)

        for opt, arg in opts:
            if opt == '-p':
                if not os.path.exists(arg):
                    print('Path=%s is not exists!' % arg)
                    sys.exit(-2)
                icon_path = arg
            elif opt == '-o':
                if os.path.isdir(arg):
                    print('Path=%s is not ALLOW a dir!' % arg)
                    sys.exit(-3)
                elif not os.path.exists(os.path.dirname(arg)):
                    print('Path=%s is not exists!' % os.path.dirname(arg))
                    sys.exit(-4)

                # 如果已经存在文件，将其重命名备份
                if os.path.exists(arg):
                    os.rename(arg, '%s_bak_%s%s' % (os.path.splitext(arg)[-2], random.randint(1, 100), os.path.splitext(arg)[-1]))
                output_file = arg
            elif opt == '-h':
                print('Usage: python3 %s -p path -o outfile' % os.path.basename(sys.argv[0]))
                sys.exit(0)
    else:
        # 根据控制台输入得到数据
        icon_path = input('Please type search path: \n').strip()
        output_file = input('Please type out file path: \n').strip()

    # 找出给定目录下所有扩展名为.png和.jpg的文件
    total_icons_path = []
    for parent, dirnames, filenames in os.walk(icon_path):
        for filename in filenames:
            if os.path.splitext(filename)[-1] not in ['.png', '.jpg']:
                continue
            total_icons_path.append(os.path.join(parent, filename))

    # 获取每个icon文件的md5
    icons_info = {}
    for icon_path in total_icons_path:
        md5_string = hashlib.md5(open(icon_path, 'rb').read()).hexdigest()

        if md5_string in icons_info.keys() and isinstance(icons_info[md5_string], list):
            icons_info[md5_string].append(os.path.basename(icon_path))
        else:
            icons_info[md5_string] = [os.path.basename(icon_path)]

    # 将字典写入文件
    try:
        with open(output_file, 'w') as f:
            # 过滤掉字典值数组个数为1个的(取出的就是有重复的图片)
            repeat_icon_info = {i: icons_info[i] for i in icons_info if len(icons_info[i]) > 1}
            format_string = json.dumps(repeat_icon_info, indent=4)
            f.write(format_string)
            print('-'*80)
            print('🎁🎁🎁 Successfully!! Output file path is: %s' % output_file)
    except IOError as e:
        print(e.msg)
        sys.exit(-5)

if __name__ == "__main__":
    search_repeat_icon()
    sys.exit(0)
