import string

from googletrans import Translator

import MySQLdb

import configparser

conn = MySQLdb.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='soc', charset='utf8')

cursor = conn.cursor()

cursor.execute("select id,name from asset_category")

rs = cursor.fetchall()

i18n = configparser.ConfigParser()

i18n.add_section('AssetCategory')

if len(rs) > 0:
    translator = Translator(proxies={"http": "http://127.0.0.1:23599",
                                     "https": "http://127.0.0.1:23599"})
    for row in rs:
        value = string.capwords(translator.translate(row[1]).text)
        i18n.set('AssetCategory', "AssetCategory."+str(row[0]), value)

# Writing our configuration file to 'example.cfg'
with open('example.properties', 'w') as configfile:
    i18n.write(configfile)

