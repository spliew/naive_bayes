# -*- coding: utf-8 -*-

from scraping import *
import sqlite3, os


def insert_database(cat):
''' 保存されたtxtから記事id、タイトル、カテゴリー、サブカテゴリー、内容と元記事リンクをデータベース('database.db')に入れる
    :param cat: Int. 例：エンタメなら1
    :return None
'''
    dbname = 'database.db'
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    ''''''
    #create_table = '''create table news (id char(5) NOT NULL UNIQUE, title varchar, category int NOT NULL, subcategory int NOT NULL,
     #                 content varchar, source varchar)'''
    #c.execute(create_table)
    path='data/'+str(cat)+'/'
    htmls=[s for s in os.listdir(path) if '.txt' in s]

    for link in htmls:
        primary_id=link.split('.')[0]
        link= path+link
        title = getTitle(link)
        try:
            category=getCategories(link)[0]
            subcategory=getCategories(link)[1]
        except: #カテゴリーのない記事もある#
            category=0
            subcategory=0
        content=getContent(link)
        source=getSource(link)
        sql = 'insert into news (id, title, category, subcategory, content, source) values (?,?,?,?,?,?)'
        news = (primary_id, title, category, subcategory, content, source)
        c.execute(sql,news)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    for i in range(1,9):
        insert_database(i)

