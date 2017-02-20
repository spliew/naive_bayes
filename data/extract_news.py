# -*- coding: utf-8 -*-
from scraping import get_articles

from urllib.request import urlretrieve
from numpy import arange


def extract_news(cat1, cat2, pages):
    """ 
Gunosyから記事htmlをtxtとして保存する
    :param cat1 (int),cat2 (int) pages (int ).カテゴリー cat1 から カテゴリー cat2 まで記事htmlをページ 1から ページ pages までtxtとして保存する
    保存先の例: data/1/Ru2WZ.txt
    :return None
    """
    for i in arange(cat1, cat2+1, pages):
        for j in arange(1, pages+1)[::-1]:
            print("\n Scraping page {} of category {}...\n".format(j, i))
            html = 'https://gunosy.com/categories/'+str(i)+'/?page='+str(j)
            articles = get_articles(html)
            for link in articles:
                primary_id = link.split('/')[-1]
                data = 'data/'+str(i)+'/'+primary_id+'.txt'
                urlretrieve(link, data)
    print("Scraped {} pages.".format(pages))

# title = getTitle(data)
# category=getCategories(data)[0]
# subcategory=getCategories(data)[1]
# content=getContent(data)
# source=getSource(data)
# sql = 'insert into news (id, title, category, subcategory, content, source) values (?,?,?,?,?,?)'
# news = (primary_id, title, category, subcategory, content, source)
# c.execute(sql,news)
# conn.commit()
# conn.close()

if __name__ == '__main__':
    extract_news(1, 2, 40)