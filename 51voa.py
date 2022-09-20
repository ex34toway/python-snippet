#!/bin/env python

from bs4 import BeautifulSoup
import re
try:
    from urllib import urlopen
except Exception:
    from urllib.request import urlopen
import sqlite3
import atexit

import unicodedata
import re

db_file = 'voa.db'

host_prefix = 'https://www.51voa.com'
host_prefix_with_ctx = '/VOA_Standard_English/'
writer_dir = './voa/'


def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')

def ProgramList(url, tb_name, cur):

    reg_document = re.compile('<!DOCTYPE.*?>')

    #html_data = open('Health_Report_1.html').read()
    html_data = urlopen(url).read().decode('utf-8')
    html_data = reg_document.sub('', html_data)

    soup = BeautifulSoup(html_data)
    span = soup.find('div', {"class":"list"})

    ii = 0
    # Get the Program List
    Health_Report_List = []
    for i in span.findAll('li'):
        for a in i.find_all('a'):
            # How could be setup the Dict quickly?
            # tmp = {}
            # tmp['title'] = a.string
            # tmp['href'] = 'http://www.51voa.com' + a['href']
            if 1 - a.has_attr('class'):
                title = a.string
                url = host_prefix + a['href']
                print(title)
                GetProgramContent(title, tb_name, url, cur)
                #Health_Report_List.append(tmp)
                if ii > 5: break
                ii += 1

    return Health_Report_List

def GetProgramContent(title, tb_name, url, cur):
    """This function use to get the content of the program,
    contain origin material text, mp3, lrc, translation.

    title           the title of the program
    url             the url of page
    """
    reg_document = re.compile('<!DOCTYPE.*?>')
    html_data = urlopen(url).read().decode('utf-8')
    html_data = reg_document.sub('', html_data)

    soup = BeautifulSoup(html_data)

    valid_title = slugify(title)

    div_menubar = soup.find('div', {'class':'menubar'})
    mp3_a = div_menubar.find('a', {'id': 'mp3'})
    if mp3_a :
        savefile(mp3_a['href'], valid_title + '.mp3', flags=2)
    lrc_a = div_menubar.find('a', {'id': 'lrc'})
    if lrc_a :
        savefile(lrc_a['href'], valid_title + '.lrc', flags=2)
    trans_a = div_menubar.find('a', {'id': 'EnPage'})
    if trans_a :
        getTrans(trans_a['href'], valid_title + '.trans')
    text = purifyContent(soup)
    savefile(text.decode("utf-8"), [tb_name, title,'',''], cur)

def getTrans(url, filename):
    """This function use to get the translation content.
    And no return value.

    url             the url of trans page
    filename        the name of file use to save translation
    """

    # Delete The Tag <!DOCTYPE ......>
    reg_document = re.compile('<!DOCTYPE.*?>')
    data = urlopen(host_prefix + host_prefix_with_ctx + url).read().decode('utf-8')
    data = reg_document.sub('', data)

    soup = BeautifulSoup(data)
    text = purifyContent(soup)
    savefile(text, filename, flags=1)

def purifyContent(soup):
    """This function use to purify the Program text content
    which contain some HTML sybaml.

    soup            the BeautifulSoup object content the text content
    """

    div_content = soup.find('div', {'class':'content'})
    if div_content:
        return bytes(div_content.extract().text, 'utf-8')
    return bytearray()
    """
    if cur != '':
        artical = [title, content, '', '']
        #Insert2DB(artical, 'economics', cur)
    else:
        artical = content
    """

def savefile(url, other_data, cur='', flags=0):
    """This function use to save the download file.
    url             the url of media file or text file
    other_data      a list contain [tbname,filetype,pubtime]
    cur             the name of file use to save the download content
    """

    if flags == 2 and (1 - (url.startswith('http') or url.startswith('https'))):
        url = host_prefix + url

    if flags == 0:
        # Save material into Database
        data = url.replace("'", "''").replace('"','""')
        v1 = other_data[0].replace("'", "''").replace('"','""')
        v2 = other_data[1].replace("'", "''").replace('"','""')

        sql_insert = "INSERT INTO %s VALUES('%s', '%s', '%s', '%s')"%(v1, v2, data, other_data[2], other_data[3])
        cur.execute(sql_insert)
        return 0
    elif flags == 1:
        # Save trans
        data = url
        f = open(writer_dir + other_data, 'wb')
        f.write(data)
        f.close()
    else:
        data = urlopen(url).read()
        f = open(writer_dir + other_data, 'wb')
        f.write(data)
        f.close()

def CreateTable(db, tbname):
    """
    """
    # --------- Create DataBase ----------
    create_DB = "CREATE TABLE %s (title text,content text, ftype varchar(3), publish date)" %(tbname)
    try:
        db.execute(create_DB)
    except sqlite3.Error:
        pass

def Insert2DB(item, tname, cur):
    """
    """
    #print(item)
    insert_DB = 'INSERT INTO %s VALUES("%s", "%s", "%s","%s")' % (tname, item[0], item[1], item[2], item[3])
    # Escape "
    #print insert_DB
    cur.execute(insert_DB)

conn = ''

def exit_handler():
    conn.commit()
    cur.close()

if __name__ == '__main__':

    education_db = 'education'
    standard_1_db = 'standard_1_db'
    technology_report_1 = 'technology_report_1_db'

    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    CreateTable(cur, technology_report_1)

    economics_report_url = 'http://www.51voa.com/Economics_Report_1.html'
    Education_report_url = 'http://www.51voa.com/Education_Report_1.html'
    Standard_1_url = 'https://www.51voa.com/VOA_Standard_1.html'
    Technology_Report_1 = 'https://www.51voa.com/Technology_Report_1.html'
    
    atexit.register(exit_handler)

    host_prefix_with_ctx = '/VOA_Special_English/'
    ProgramList(Technology_Report_1, technology_report_1, cur)

