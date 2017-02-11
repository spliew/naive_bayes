# -*- coding: utf-8 -*-
from MultivariateBernoulli import *
import sqlite3, random
from numpy import *


def readData(trainvalidTestRatio):
    """data/gunosyInTextからテキストデータを読み込む。(../dataで sh selectData.shでテキストデータを作る)

    :param trainvalidTestRatio: List of length 3. train, validation, testデータの割合. 例:[0.6, 0.2, 0.2]
    :return dict(). data. N*, X*, y*を保存する（*はtrain, valid, test）
    """
    titleCategoryList = []
    classes = []
    for c in range(1, 9):
        f = open('../data/gunosyInText/' + str(c) + ".txt", encoding='euc-jp', errors='ignore')
        titleCategory = f.readlines()
        f.close()
        titleCategoryList += titleCategory
        classes += [c] * len(titleCategory)
    data = []
    for i in range(0, len(classes)):
        data.append([classes[i], titleCategoryList[i]])

    Ndata = len(data)
    Ntrain = int(Ndata * trainvalidTestRatio[0])
    Nvalid = int(Ndata * trainvalidTestRatio[1])
    Ntest= Ndata - Ntrain - Nvalid

    random.shuffle(data) # train, validate, test集合に分けるためにshuffle
    X = []
    classes = []
    for datum in data:
        text = datum[1]
        category = datum[0] - 1 # 学習機に入れるときはカテゴリーラベルが0から始まるようにする
        X.append(text)
        classes.append(category)

    Xtrain = X[0:Ntrain]
    Xvalid = X[Ntrain: Ntrain + Nvalid]
    Xtest = X[Ntrain + Nvalid: Ndata]
    ytrain = array(classes[0:Ntrain])
    yvalid = array(classes[Ntrain: Ntrain + Nvalid])
    ytest = array(classes[Ntrain + Nvalid: Ndata])
    data = {'Ntrain': Ntrain,'Nvalid': Nvalid,'Ntest': Ntest, 'Xtrain': Xtrain, 'Xvalid': Xvalid, 'Xtest': Xtest, 'ytrain': ytrain, 'yvalid': yvalid, 'ytest': ytest}
    return data

def validate(data, modelName, param):
    """
    validationする。
    :param data: readDataのreturn値。
    :param modelName: 今のところ"MB"にしか対応していない。
    :param param: モデルのパラメータ (alpha)。
    :return errorRatevalid: validation dataに対する誤分類率。
    """
    if modelName == 'MB':
        model = MultivariateBernoulli(data['Xtrain'], data['ytrain'], alpha=param['alpha'])
    else:
        raise RuntimeError('MB (Multivariate Bernoulli)以外は使えません。')

    model.train()
    predcList = []
    for x in data['Xvalid']:
        predc = model.predict(x)
        predcList.append(predc)

    predcArray = array(predcList)
    errorRatevalid = (data['Nvalid'] - sum(predcArray == data['yvalid'])) / data['Nvalid']
    return errorRatevalid

def trainWithAllData():
    """
    すべてのデータをtrainしてmodelをpickleフォーマットとして出力
    """
    trainvalidTestRatio = [1, 0, 0]
    data = readData(trainvalidTestRatio)
    model = MultivariateBernoulli(data['Xtrain'], data['ytrain'], alpha=2)
    model.train()
    model.dump("../model/")

if __name__ == '__main__':
#    trainvalidTestRatio = [0.6, 0.2, 0.2]
#    data = readData(trainvalidTestRatio)
#    errorRate = validate(data, 'MB', {'alpha': 2})
#    print(errorRate)
    trainWithAllData()
