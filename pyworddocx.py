# -*- coding:utf-8 -*-
import re
from docx import Document
import os


def list_dir_and_write(document, path):
    full_file_path = os.getcwd()+"\\"+path
    print full_file_path
    path_list = os.listdir(full_file_path)
    for dir_path in path_list:
        full_path = os.path.join(path, dir_path)
        if os.path.isfile(full_path):
            print os.path.abspath(full_path)
            write_java_file_to_document(document, dir_path, full_path)
        else:
            pt = os.path.abspath(full_path)
            print pt
            list_dir_and_write(document, pt)


def write_java_file_to_document(document, file_name, file_path):
    java_file = open(file_path, 'r')
    java_content = java_file.read()
    content = blank_line.sub("", comment_pattern.sub("", java_content))
    p_paragraph = document.add_paragraph("File: " + file_path.replace("\\", "/") + ": \n\n")
    p_paragraph.add_run(content)


doc = Document()
doc.styles['Normal'].font.name = u'宋体'
comment_pattern = re.compile("|".join({'/\*{1,2}[\s\S]*?\*/', '//[\s\S]*?\n' }))
blank_line = re.compile(r'^\n|\n+(?=\n)|\n$')
list_dir_and_write(doc, "src")
doc.save("out.docx")
