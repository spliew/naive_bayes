# -*- coding: utf-8 -*-
from multi_variate_bernoulli import *
# import sqlite3, random
from numpy import *
import random
import time


def read_data(train_valid_test_ratio):
    """data/gunosyInTextからテキストデータを読み込む。(../dataで sh selectData.shでテキストデータを作る)

    :param train_valid_test_ratio: List of length 3. train, validation, testデータの割合. 例:[0.6, 0.2, 0.2]
    :return dict(). data. N*, X*, y*を保存する（*はtrain, valid, test）
    """
    title_category_list = []
    classes = []
    for c in range(1, 9):
        # f = open('../data/gunosyInText/' + str(c) + ".txt", encoding='euc-jp', errors='ignore')
        f = open('../data/gunosyInText/' + str(c) + ".txt", errors='ignore')
        title_category = f.readlines()
        f.close()
        title_category_list += title_category
        classes += [c] * len(title_category)
    data = []
    for i in range(0, len(classes)):
        data.append([classes[i], title_category_list[i]])

    n_data = len(data)
    n_train = int(n_data * train_valid_test_ratio[0])
    n_valid = int(n_data * train_valid_test_ratio[1])
    n_test= n_data - n_train - n_valid

    random.shuffle(data)  # train, validate, test集合に分けるためにshuffle
    X = []
    classes = []
    for datum in data:
        text = datum[1]
        category = datum[0] - 1  # 学習機に入れるときはカテゴリーラベルが0から始まるようにする
        X.append(text)
        classes.append(category)

    x_train = X[0:n_train]
    x_valid = X[n_train: n_train + n_valid]
    x_test = X[n_train + n_valid: n_data]
    y_train = array(classes[0:n_train])
    y_valid = array(classes[n_train: n_train + n_valid])
    y_test = array(classes[n_train + n_valid: n_data])
    data = {'n_train': n_train, 'n_valid': n_valid, 'n_test': n_test, 'x_train': x_train, 'x_valid': x_valid, 'x_test': x_test, 'y_train': y_train, 'y_valid': y_valid, 'y_test': y_test}
    return data


def validate(data, modelName, param):
    """
    validationする。
    :param data: read_dataのreturn値。
    :param modelName: Str. 今のところ"MB"にしか対応していない。
    :param param: Str. モデルのパラメータ (alpha)。
    :return [error_rate_valid,error_rate_test]: validation, test dataに対する誤分類率。
    """
    if modelName == 'MB':
        model = multi_variate_bernoulli(data['x_train'], data['y_train'], alpha = param['alpha'])
    else:
        raise RuntimeError('MB (Multivariate Bernoulli)以外は使えません。')

    model.train()
    predcList = []
    for x in data['x_valid']:
        predc = model.predict(x)
        predcList.append(predc)

    predc_array = array(predcList)
    error_rate_valid = (data['n_valid'] - sum(predc_array == data['y_valid'])) / data['n_valid']

    predcList2 = []
    for x in data['x_test']:
        predc2 = model.predict(x)
        predcList2.append(predc2)

    predc_array2 = array(predcList2)
    error_rate_test = (data['n_test'] - sum(predc_array2 == data['y_test'])) / data['n_test']

    return [error_rate_valid, error_rate_test]


def grid_search(data, modelName, para, gridRange):
    """
    grid search する。
    :param data: read_dataのreturn値。
    :param modelName: String. 今のところ"MB"にしか対応していない。
    :param para: String. grid search するモデルのパラメータ (今のところ'alpha'にしか対応してない)。
    :return None: 結果がterminalに出力される。
    """
    for i in arange(gridRange[0], gridRange[1], gridRange[2]):
        error_rate = validate(data, 'MB', {para: i})
        print("alpha = {}, error_rate_valid = {}, error_rate_test = {}".format(i, error_rate[0], error_rate[1]))


def train_with_all_data():
    """
    すべてのデータをtrainしてmodelをpickleフォーマットとして出力
    """
    train_valid_test_ratio = [1, 0, 0]
    data = read_data(train_valid_test_ratio)
    model = multi_variate_bernoulli(data['x_train'], data['y_train'], alpha=1.001)
    model.train()
    model.dump("../model/")

if __name__ == '__main__':
    train_valid_test_ratio = [0.8, 0.1, 0.1]

    # alphaのtuningをする
    # data = read_data(train_valid_test_ratio)
    # grid_search(data,'MB','alpha',[1.001,1.002,0.1])

    # error_rateを計算する

# data = read_data(train_valid_test_ratio)
    # error_rate = validate(data, 'MB', {'alpha': 2})
    # print(error_rate)
    # start_time = time.time()
    # train_with_all_data()
    # print("--- %s seconds ---" % (time.time() - start_time))
