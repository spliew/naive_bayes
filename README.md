# naive_bayes
記事URLを入れると記事カテゴリを返す、ナイーブベイズを使った教師あり文書分類器ウェブアプリを実装

## アプリ(ローカルサーバー)の起動

```
cd django
./manage.py runserver
```

## ウェブアプリ
https://fierce-island-51792.herokuapp.com/

## 必要なLibrary
- bs4
- gensim
- natto
- numpy
- sqlite3


# Steps
- 記事をscrapeして、databaseを作る
  * data/extract_news.py, data/insert_database.py を使う
- 記事を形態素解析して、ナイーブベイズを使って訓練させる
  * main/constructModelForGunosy.py　を使う
- Djangoを使ってウェブアプリを実装する
- Herokuでアプリをデプロイする	
  * https://fierce-island-51792.herokuapp.com/
