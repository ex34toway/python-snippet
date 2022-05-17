# -*- coding:utf-8 -*-
#!/bin/env python3

# 处理 PuTTY Color Themes 适配 KiTTY 配置器

from functools import reduce

color_schema = """
"Colour0"="185,188,186"
"Colour1"="254,255,178"
"Colour2"="31,31,31"
"Colour3"="31,31,31"
"Colour4"="248,62,25"
"Colour5"="185,188,186"
"Colour6"="58,61,67"
"Colour7"="136,137,135"
"Colour8"="190,63,72"
"Colour9"="251,0,31"
"Colour10"="135,154,59"
"Colour11"="15,114,47"
"Colour12"="197,166,53"
"Colour13"="196,112,51"
"Colour14"="79,118,161"
"Colour15"="24,109,227"
"Colour16"="133,92,141"
"Colour17"="251,0,103"
"Colour18"="87,143,164"
"Colour19"="46,112,109"
"Colour20"="185,188,186"
"Colour21"="253,255,185"
"""

def pair_handle(kv):
    pair = kv.split("=")
    key = pair[0].lstrip('\"').rstrip('\"')
    val = pair[1].lstrip('\"').rstrip('\"')
    return f"{key}\{val}\\"


if __name__ == '__main__':
    color_list = map(pair_handle, filter(lambda x: len(x) > 0, color_schema.split("\n")))
    print(reduce((lambda a,x: a + '\n' + x), color_list))
