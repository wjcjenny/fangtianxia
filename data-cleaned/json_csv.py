# -*- coding: utf-8 -*-

import logging
from itertools import chain
import json
import csv
from io import StringIO
import sys
from six import string_types

# f = open('dongcheng_22029_new.json')

f = open(sys.argv[1], 'r')
json_value = f.read()



def to_keyvalue_pairs(source, ancestors=[], key_delimeter='_'):
    def is_sequence(arg):
        return (not isinstance(arg, string_types)) and (hasattr(arg, "__getitem__") or hasattr(arg, "__iter__"))

    def is_dict(arg):
        return isinstance(arg, dict)

    if is_dict(source):
        result = [to_keyvalue_pairs(source[key], ancestors + [key]) for key in source.keys()]
        return list(chain.from_iterable(result))
    elif is_sequence(source):
        result = [to_keyvalue_pairs(item, ancestors + [str(index)]) for (index, item) in enumerate(source)]
        return list(chain.from_iterable(result))
    else:
        return [(key_delimeter.join(ancestors), source)]

def json_to_dicts(json_str):
    try:
      objects = json.loads(json_str)
    except:
      objects = [json.loads(l) for l in json_str.split('\n') if l.strip()]

    return [dict(to_keyvalue_pairs(obj)) for obj in objects]

dicts = json_to_dicts(json_value) 

def remove_comma(line, name):
    name_num = line.find(name)
    if name_num >= 0:
        if name == '年代：':
            return line[name_num + len(name): len(line)-1]
        elif name == '参考首付：':
            return line[name_num + len(name): len(line)-2]
        else:
            return line[name_num + len(name): len(line)]
    else:
        return line

def dicts_to_csv(source, output_file):
    def build_row(dict_obj, keys):
        return [dict_obj.get(k, "") for k in keys]

    keys = sorted(set(chain.from_iterable([o.keys() for o in source])))
    rows = [build_row(d, keys) for d in source]

    cw = csv.writer(output_file)
    cw.writerow(keys)
    for row in rows:
        # print (row)
        each = []
        for c_new in row:
            c_new = remove_comma(c_new, "建筑类别：")
            c_new = remove_comma(c_new, "年代：")
            c_new = remove_comma(c_new, "装修：")
            c_new = remove_comma(c_new, "朝向：")
            c_new = remove_comma(c_new, "参考首付：")
            c_new = remove_comma(c_new, "户型：")
            c_new = remove_comma(c_new, "住宅类别：")
            c_new = remove_comma(c_new, "产权性质：")
            c_new = remove_comma(c_new, "结构：")
            c_new = remove_comma(c_new, "发布时间：")
            c_new = remove_comma(c_new, "楼层：")
            c_new = remove_comma(c_new, "装修程度：")
            # print(c_new)
            each.append(c_new)
        cw.writerow(each)
        #     end = c.find('\n')
        #     if end >= 0:
        #         c_new = c.replace('\n', '')
        #         c_new = remove_comma(c_new, "建筑类别：")
        #         c_new = remove_comma(c_new, "年代：")
        #         c_new = remove_comma(c_new, "装修：")
        #         c_new = remove_comma(c_new, "朝向：")
        #         c_new = remove_comma(c_new, "参考首付：")
        #         c_new = remove_comma(c_new, "户型：")
        #         c_new = remove_comma(c_new, "住宅类别：")
        #         c_new = remove_comma(c_new, "产权性质：")
        #         c_new = remove_comma(c_new, "结构：")
        #         c_new = remove_comma(c_new, "发布时间：")
        #         c_new = remove_comma(c_new, "楼层：")

        #         print(c_new)
        #         each.append(c_new)
        #     else:
        #         print(c)
        #         each.append(c)
        # cw.writerow(each)




                

        # cw.writerow([c if isinstance(c, string_types) else c for c in row])


with open(sys.argv[2], "w") as output_file:
    dicts_to_csv(dicts, output_file)

