# -*- coding: utf-8 -*-

from natto import MeCab
from numpy import array
from gensim import corpora, matutils

nm = MeCab('-F%m,%f[0],%h')


def get_meishi(sentence):
    """名詞だけを取り出す。
    :param sentence: String
    :return words: list of String.

    入力例) get_meishi("ピンチ、ピンチの時には必ずヒーローが現れる。")
    ==> ['ピンチ', 'ピンチ', '時', 'ヒーロー']
    """
    # -F / --node-format オプションでノードの出力フォーマットを指定する
    #
    # %m    ... 形態素の表層文
    # %f[0] ... 品詞
    # %h    ... 品詞 ID (IPADIC)
    # %f[8] ... 発音
    #
    words = []

    for n in nm.parse(sentence, as_nodes=True):
        node = n.feature.split(',')
        if len(node) != 3:
            continue
        if node[1] == '名詞':
            # if True:
            words.append(node[0])
    return words


def create_feature(words, dictionary):
    """文の特徴量を作る。

    :param words: List. get_meishi。
    :param dictio  nary: gensimのDictionary.
    :return feature : numpy.Array

    入力例: words = get_meishi("ピンチ、ピンチの時には必ずヒーローが現れる。")
    dictionary = corpora.Dictionary([words])
    create_feature(words, dictionary)
    出力： numpy.array([1,1,1])

    TODO: tf-idf, stop words等の工夫をする。
    """
    bow = dictionary.doc2bow(words)  # [(0, 1), (1, 1), (2, 2)]
    feature_list = list(matutils.corpus2dense([bow], num_terms=len(dictionary)).T[0])
    feature = array(feature_list)
    feature[feature > 0.5] = 1
    feature[feature <= 0.5] = 0
    return feature


if __name__ == '__main__':
    a = get_meishi("ピンチ、ピンチの時には必ずヒーローが現れる。")
    b1 = "コーパスとして使用した89個の文書を使って、SVMの学習とiPadとSochiのどちらのクラスに属するかの識別を行います"
    b2 = "コーパスの読み込み後、タイトルを単語に分割し、ストップワードの除去とステミング処理を行います。"
    c1 = get_meishi(b1)
    c2 = get_meishi(b2)
    print(c1)
    print(c2)
    dictionary = corpora.Dictionary([c1, c2])
    print(create_feature(c1, dictionary))
    print(create_feature(c2, dictionary))
