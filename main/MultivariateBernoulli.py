# -*- coding: utf-8 -*-
from bow import *
from numpy import *
import warnings, sys, pickle, itertools
from datetime import datetime

class MultivariateBernoulli:
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
        self.numClasses = len(self.classes)
        meishiList = []
        for text in texts:
            words = getMeishi(text)
            meishiList.append(words)
        self.dictionary  = corpora.Dictionary(meishiList)
        self.dictSize = len(self.dictionary.token2id)
        self.pwc = zeros([self.dictSize, self.numClasses])
        self.pc = zeros(self.numClasses)
        self.alpha = alpha
        self.Nc = zeros(self.numClasses)
        self.Nwc = zeros([self.dictSize, self.numClasses])
        self.status = 'Initialized'

    def train(self):
        """
        :return: None
        """
        alpha = self.alpha
        numClasses = self.numClasses
        Ndata = len(self.texts)
        Nc = self.Nc
        Nwc = self.Nwc
        for iData in range(0, Ndata):
            c = int(self.labels[iData])
            Nc[c] += 1

        dictionary = self.dictionary
        dictSize = len(dictionary.token2id)
        for iText in range(0, len(self.texts)):
            text = self.texts[iText]
            words = getMeishi(text)
            feature = createFeature(words, dictionary)
            c = int(self.labels[iText])
            for iBinary in range(0, dictSize):
                if feature[iBinary] == 1:
                    Nwc[iBinary, c] += 1

        for c in range(0, numClasses):
            self.pc[c] = (Nc[c] + alpha - 1) / (sum(Nc) + numClasses * (alpha - 1))
            for w in range(0, dictSize):
                self.pwc[w, c] = (Nwc[w, c] + alpha - 1) / (Nc[c] + 2 * (alpha - 1))
        self.Nwc = Nwc
        self.Nc = Nc
        self.status = 'Trained'

    def predict(self, text):
        """
        textのクラスを予測する。
        :param text: String
        :return predc: Int: 予測class
        """
        if self.status != 'Trained':
            warnings.warn('モデルは訓練されていません。trainを呼んで下さい。')
        words = getMeishi(text)
        feature = array( createFeature(words, self.dictionary) )
        logL_classes = []
        for c in range(0, self.numClasses):
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
        :param featurenumber: Int: dictSize*numClasses
        """
        if self.dictSize*self.numClasses < featurenumber:
            print('削除されて残る素性が元の素性より大きい！')
            sys.exit()
        # copied from train(self) #
        numClasses = self.numClasses
        Ndata = len(self.texts)
        Nc = self.Nc
        Nwc = self.Nwc
        for iData in range(0, Ndata):
            c = int(self.labels[iData])
            Nc[c] += 1

        dictionary = self.dictionary
        dictSize = len(dictionary.token2id)
        for iText in range(0, len(self.texts)):
            text = self.texts[iText]
            words = getMeishi(text)
            feature = createFeature(words, dictionary)
            c = int(self.labels[iText])
            for iBinary in range(0, dictSize):
                if feature[iBinary] == 1:
                    Nwc[iBinary, c] += 1
        # copied from train(self) #

        Nw=Nwc.dot(Nc)
        mutual_info=zeros([self.dictSize, self.numClasses]) # 交互情報量
        for c, w in itertools.product(range(numClasses),range(dictSize)):
            mutual_info[w, c] = (Nc[c]/sum(Nc))*(log((Nwc[w,c]+1)/sum(Nc))-log(Nw[w]/sum(Nc))-log(Nc[c]/sum(Nc)))
        mutual_info_1d=mutual_info.flatten()
        idx_1d_all = mutual_info_1d.argsort()
        idx_1d = idx_1d_all[-int(featurenumber):] #最大な交互情報量を見つける
        x_idx, y_idx = unravel_index(idx_1d, mutual_info.shape)
#        bookkeeping = int(featurenumber)
#        while len(set(x_idx)) < int(featurenumber):
#            bookkeeping = bookkeeping + 1
#            idx_1d = mutual_info_1d.argsort()[-bookkeeping:] 
#            x_idx, y_idx = unravel_index(idx_1d, mutual_info.shape)
        self.dictionary.filter_tokens(good_ids=x_idx)
        self.dictSize = len(self.dictionary.token2id)
        self.pwc = zeros([self.dictSize, self.numClasses])
        self.status = 'dimensionReduced'
