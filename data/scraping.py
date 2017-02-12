# -*- coding: utf-8 -*-

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re


def getArticles(link):
    """
    'https://gunosy.com/categories/i'から記事のリンクを読み込む。
    :param: link: Str. 例：'https://gunosy.com/categories/i' あるいは任意のhtml file
    :return list of Str: ['記事１','記事2']
    """
    articles = []
    try:
        html = urlopen(link)
    except:
        html = open(link,'r')
    bs0bj=BeautifulSoup(html.read(),"html.parser")
    for link in bs0bj.find("div",{"class":"main"}).findAll("a",href=re.compile("^(https://gunosy.com/articles/).*$")):
        if 'href' in link.attrs:
            articles.append(link.attrs['href'])
    return set(articles)

def getCategories(link):
    """
    記事のリンクからカテゴリーとサブカテゴリーを読み込む。
    :return list of Str: ['カテゴリー１','サブカテゴリー1']
    """
    categories = []
    try:
        html = urlopen(link)
    except:
        html = open(link,'r') 
    bs0bj=BeautifulSoup(html.read(),"html.parser")
    for link in bs0bj.find("div",{"class":"breadcrumb_inner"}).findAll("a",href=re.compile("^(https://gunosy.com/categories/).*$")):
        if 'href' in link.attrs:
            categories.append(int(link.attrs['href'].split('/')[-1]))
    return sorted(categories)

def getTitle(link):
    """
    記事のリンクからタイトルを読み込む。
    :return Str: タイトル
    """
    try:
        html = urlopen(link)
    except:
        html = open(link,'r')
    bs0bj=BeautifulSoup(html.read(),"html.parser")
    return bs0bj.find("h1").get_text()

def getContent(link):
    """
    記事のリンクからコンテンツを読み込む。
    :return Str: コンテンツ
    """
    try:
        html = urlopen(link)
    except:
        html = open(link,'r')
    bs0bj=BeautifulSoup(html.read(),"html.parser")
    return bs0bj.find("div",{"class":"article gtm-click"}).get_text()

def getSource(link):
    """
    記事のリンクから元記事を読み込む。
    :return Str: 元記事
    """
    OriginalArticle = []
    try:
        html = urlopen(link)
    except:
        html = open(link,'r')
    bs0bj=BeautifulSoup(html.read(),"html.parser")
    for link in bs0bj.find("div",{"class":"article_media clearfix gtm-click"}).findAll("a"):
        if 'href' in link.attrs:
            OriginalArticle.append(link.attrs['href'])
    return OriginalArticle[-1]
