# -*- coding: utf-8 -*-
from bow import *
from numpy import *
import warnings
import sys
import pickle
import itertools
from datetime import datetime


class multi_variate_bernoulli:
    """Multivariate Bernoulli class. バイナリの素性からクラス分類するモデル。"""
    def __init__(self, texts, labels, alpha):
        """
        :param texts: List[List[String]]. List[String]は一つの文.
        :param labels: List[Int]. クラスラベル。min(labels) = 0
        :param alpha: Double. > 1
        """
        self.texts = texts
        self.labels = labels
        self.classes = list(set(self.labels))
        self.num_classes = len(self.classes)
        meishi_list = []
        for text in texts:
            words = get_meishi(text)
            meishi_list.append(words)
        self.dictionary = corpora.Dictionary(meishi_list)
        self.dict_size = len(self.dictionary.token2id)
        self.pwc = zeros([self.dict_size, self.num_classes])
        self.pc = zeros(self.num_classes)
        self.alpha = alpha
        self.n_c = zeros(self.num_classes)
        self.n_wc = zeros([self.dict_size, self.num_classes])
        self.status = 'Initialized'

    def train(self):
        """
        :return: None
        """
        alpha = self.alpha
        num_classes = self.num_classes
        n_data = len(self.texts)
        n_c = self.n_c
        n_wc = self.n_wc
        for i_data in range(0, n_data):
            c = int(self.labels[i_data])
            n_c[c] += 1

        dictionary = self.dictionary
        dict_size = len(dictionary.token2id)
        for i_text in range(0, len(self.texts)):
            text = self.texts[i_text]
            words = get_meishi(text)
            feature = create_feature(words, dictionary)
            c = int(self.labels[i_text])
            for i_binary in range(0, dict_size):
                if feature[i_binary] == 1:
                    n_wc[i_binary, c] += 1

        for c in range(0, num_classes):
            self.pc[c] = (n_c[c] + alpha - 1) / (sum(n_c) + num_classes * (alpha - 1))
            for w in range(0, dict_size):
                self.pwc[w, c] = (n_wc[w, c] + alpha - 1) / (n_c[c] + 2 * (alpha - 1))
        self.n_wc = n_wc
        self.n_c = n_c
        self.status = 'Trained'

    def predict(self, text):
        """
        textのクラスを予測する。
        :param text: String
        :return predc: Int: 予測class
        """
        if self.status != 'Trained':
            warnings.warn('モデルは訓練されていません。trainを呼んで下さい。')
        words = get_meishi(text)
        feature = array(create_feature(words, self.dictionary) )
        logL_classes = []
        for c in range(0, self.num_classes):
            logL = log(self.pc[c])
            logL += sum(log(array(self.pwc)[:, c] ** feature)) + sum(log((1 - array(self.pwc[:, c]))**(1 - feature)))
            logL_classes.append(logL)

        predc = int(array(logL_classes).argmax())
        return predc

    def dump(self, destination):
        """
        モデルをdestination folderに保存。
        :param destination: String. フォルダの相対path。
        :return: String. pickleバイナリファイルのpath。
        """
        now = datetime.now()
        unixtime = int(now.timestamp())
        if destination[-1] != "/":
            destination += "/"
        filename = destination + str(unixtime) + ".pickle"
        with open(filename, "wb") as f:
            pickle.dump(self, f)
        return filename

    def featureSelection(self,featurenumber=8000):
        """
        素性選択して次元を削減する (work in progress)
        :return: None
        :param featurenumber: Int: dict_size*num_classes
        """
        if self.dict_size*self.num_classes < featurenumber:
            print('削除されて残る素性が元の素性より大きい！')
            sys.exit()
        # copied from train(self) #
        num_classes = self.num_classes
        n_data = len(self.texts)
        n_c = self.n_c
        n_wc = self.n_wc
        for i_data in range(0, n_data):
            c = int(self.labels[i_data])
            n_c[c] += 1

        dictionary = self.dictionary
        dict_size = len(dictionary.token2id)
        for i_text in range(0, len(self.texts)):
            text = self.texts[i_text]
            words = get_meishi(text)
            feature = create_feature(words, dictionary)
            c = int(self.labels[i_text])
            for i_binary in range(0, dict_size):
                if feature[i_binary] == 1:
                    n_wc[i_binary, c] += 1
        # copied from train(self) #

        n_w=n_wc.dot(n_c)
        mutual_info=zeros([self.dict_size, self.num_classes])  # 交互情報量
        for c, w in itertools.product(range(num_classes), range(dict_size)):
            mutual_info[w, c] = (n_c[c]/sum(n_c))*(log((n_wc[w, c]+1)/sum(n_c))-log(n_w[w]/sum(n_c))-log(n_c[c]/sum(n_c)))
        mutual_info_1d=mutual_info.flatten()
        idx_1d_all = mutual_info_1d.argsort()
        idx_1d = idx_1d_all[-int(featurenumber):]  # 最大な交互情報量を見つける
        x_idx, y_idx = unravel_index(idx_1d, mutual_info.shape)
#        bookkeeping = int(featurenumber)
#        while len(set(x_idx)) < int(featurenumber):
#            bookkeeping = bookkeeping + 1
#            idx_1d = mutual_info_1d.argsort()[-bookkeeping:] 
#            x_idx, y_idx = unravel_index(idx_1d, mutual_info.shape)
        self.dictionary.filter_tokens(good_ids=x_idx)
        self.dict_size = len(self.dictionary.token2id)
        self.pwc = zeros([self.dict_size, self.num_classes])
        self.status = 'dimensionReduced'
