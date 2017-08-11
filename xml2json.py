# -*- coding:utf-8 -*-

import optparse
from xml.etree import ElementTree
import json
import codecs
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def xml2json(xml):
    root = ElementTree.fromstring(xml)
    # 初始化
    result = {root.tag: _parse(root)}
    return json.dumps(result, indent=4).decode('unicode-escape')


def _parse(ele):
    result = None
    tags = []
    p_childs = []
    for child in ele.getchildren():
        # 统计子元素
        tags.append(child.tag)
        # 递归调用自身
        p_childs.append((child.tag, _parse(child)))

    if not tags:
        # 文本处理
        text = ele.text
        if text is not None:
            text = text.strip()
        else:
            text = ''
        return text

    if len(set(tags)) < len(tags):
        # 列表处理 子元素存在不同标签则为列表
        result = []
        result = [dict([x]) for x in p_childs]
    else:
        # 字典处理
        result = {}
        result = dict(p_childs)
    return result


def main():
    p = optparse.OptionParser(
        description='Converts XML to JSON ',
        prog='xml2json',
        usage='%prog -i xml.xml -o file.json'
    )
    p.add_option('--input', '-i', help="xml file")
    p.add_option('--out', '-o', help="Out json file name")
    options, arguments = p.parse_args()

    xml_string = ""
    with codecs.open(options.input, 'r', 'utf-8') as f:
        xml_string = f.read()
    out = xml2json(xml_string)
    with codecs.open(options.out, 'w', 'utf-8') as o:
        o.write(out)

if __name__ == "__main__":
    main()
