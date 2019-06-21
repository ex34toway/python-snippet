import string

from googletrans import Translator

import MySQLdb

conn = MySQLdb.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='soc', charset='utf8')

cursor = conn.cursor()

cursor.execute("select id,name from asset_category")

rs = cursor.fetchall()

sql_list = []
if len(rs) > 0:
    translator = Translator(proxies={"http": "http://127.0.0.1:23599",
                                     "https": "http://127.0.0.1:23599"})
    for row in rs:
        value = string.capwords(translator.translate(row[1]).text)
        sql_list.append("update asset_category set name = '"+value+"' where id = "+str(row[0])+"; \n")

with open('update.sql', 'w') as configfile:
    configfile.writelines(sql_list)

