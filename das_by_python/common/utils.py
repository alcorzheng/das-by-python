#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
@auth: alcorzheng<alcor.zheng@gmail.com>
@file: utils.py
@time: 2018/4/39:58
@desc: 通用工具类
"""


def obj2oth(val, datatype, model, defval, **kwargs):
    if datatype == 'I':
        if model == 'replaces':
            return obj2int(str_replaces(val, kwargs['oldchars'], kwargs['newchars']), defval)
        elif model == 'maketrans':
            return obj2int(str_maketrans(val, kwargs['oldchars'], kwargs['newchars']), defval)
        else:
            return obj2int(val, defval)
    elif datatype == 'S':
        if model == 'replaces':
            return str_replaces(val, kwargs['oldchars'], kwargs['newchars'])
        elif model == 'maketrans':
            return str_maketrans(val, kwargs['oldchars'], kwargs['newchars'])
        else:
            return val
    else:
        return val


def obj2int(val, defval):
    """整数转换处理，空值转为默认值"""
    if val:
        return int(val)
    else:
        return defval


def str_maketrans(text, intab, outtab):
    """字符串按映射替换"""
    return text.translate(str.maketrans(intab, outtab))


def str_replaces(text, oldchars, newchar):
    """字符串批量替换成指定字符"""
    if oldchars:
        for c in oldchars:
            text = text.replace(c, newchar)
    return text
