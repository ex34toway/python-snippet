# -*- coding:utf-8 -*-
import re
from docx import Document
import os
import codecs


def list_dir_and_write(document, path):
    cwd = os.getcwd()
    full_file_path = cwd+"\\"+path
    print(full_file_path)
    path_list = os.listdir(full_file_path)
    for dir_path in path_list:
        full_path = os.path.join(full_file_path, dir_path)
        if os.path.isfile(full_path):
            print(os.path.abspath(full_path))
            write_java_file_to_document(document, dir_path, full_path)
        else:
            pt = os.path.abspath(full_path)
            print(pt)
            list_dir_and_write(document, full_path.replace(cwd+"\\", ""))


def write_java_file_to_document(document, file_name, file_path):
    java_file = codecs.open(filename=file_path, mode='r', encoding='utf-8')
    tem_file = comment_pattern.sub("", java_file.read())
    java_file.close()
    java_file = codecs.open(filename=file_path, mode='w', encoding='utf-8')
    java_file.write(tem_file)
    java_file = codecs.open(filename=file_path, mode='r', encoding='utf-8')
    content = ""
    first_line = 1
    for line in java_file.readlines():
        if line != '\r\n' and len(line.strip()) != 0 :
            if first_line:
                content = '\n'
                content += line.strip()
                first_line = 0
            else:
                content += '\n'
                content += line.rstrip()
    java_file.close()
    p_paragraph = document.add_paragraph(text="File: " + file_name.replace("\\", "/") + ": \n\n", style='Normal')
    p_paragraph.text = content


doc = Document()
doc.styles['Normal'].font.name = u'宋体'
comment_pattern = re.compile("|".join({'/\*{1,2}[\s\S]*?\*/', '//[\s\S]*?\n'}))
list_dir_and_write(doc, "src")
doc.save("out.docx")
