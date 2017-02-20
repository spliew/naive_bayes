# -*- coding: utf-8 -*-

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re


def get_articles(link):
    """
    'https://gunosy.com/categories/i'から記事のリンクを読み込む。
    :param: link: Str. 例：'https://gunosy.com/categories/i' あるいは任意のhtml file
    :return list of Str: ['記事１','記事2']
    """
    articles = []
    try:
        html = urlopen(link)
    except:
        html = open(link, 'r')
    bs0bj = BeautifulSoup(html.read(), "html.parser")
    for link in bs0bj.find("div", {"class": "main"}).find_all("a", href=re.compile("^(https://gunosy.com/articles/).*$")):
        if 'href' in link.attrs:
            articles.append(link.attrs['href'])
    return set(articles)


def get_categories(link):
    """
    記事のリンクからカテゴリーとサブカテゴリーを読み込む。
    :return list of Str: ['カテゴリー１','サブカテゴリー1']
    """
    categories = []
    try:
        html = urlopen(link)
    except:
        html = open(link, 'r')
    bs0bj = BeautifulSoup(html.read(), "html.parser")
    for link in bs0bj.find("div", {"class": "breadcrumb_inner"}).find_all("a", href=re.compile("^(https://gunosy.com/categories/).*$")):
        if 'href' in link.attrs:
            categories.append(int(link.attrs['href'].split('/')[-1]))
    return sorted(categories)


def get_title(link):
    """
    記事のリンクからタイトルを読み込む。
    :return Str: タイトル
    """
    try:
        html = urlopen(link)
    except:
        html = open(link, 'r')
    bs0bj = BeautifulSoup(html.read(), "html.parser")
    return bs0bj.find("h1").get_text()


def get_content(link):
    """
    記事のリンクからコンテンツを読み込む。
    :return Str: コンテンツ
    """
    try:
        html = urlopen(link)
    except:
        html = open(link, 'r')
    bs0bj = BeautifulSoup(html.read(), "html.parser")
    return bs0bj.find("div", {"class": "article gtm-click"}).get_text()


def get_source(link):
    """
    記事のリンクから元記事を読み込む。
    :return Str: 元記事
    """
    original_articles = []
    try:
        html = urlopen(link)
    except:
        html = open(link, 'r')
    bs0bj = BeautifulSoup(html.read(), "html.parser")
    for link in bs0bj.find("div", {"class": "article_media clearfix gtm-click"}).find_all("a"):
        if 'href' in link.attrs:
            original_articles.append(link.attrs['href'])
    return original_articles[-1]
