#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MeCab
from pyknp import Jumanpp

class MecabSplitter():
    """
    Mecabを使って単語列(原形)を取得する
    https://github.com/katryo/tfidf_with_sklearn/blob/master/utils.py
    """
    def __init__(self):
        self.m = MeCab.Tagger('mecabrc')

    def split(self, sentence):
        try:
            info_of_words = self.m.parse(sentence).split('\n')
            words = []
            for info in info_of_words:
                # macabで分けると、文の最後に’’が、その手前に'EOS'が来る
                if info == 'EOS' or info == '':
                    break
                # info => 'な\t助詞,終助詞,*,*,*,*,な,ナ,ナ'
                info_elems = info.split(',')
                if info_elems[6] == '*':
                    # 6番目に、無活用系の単語が入る。もし6番目が'*'だったら0番目を入れる
                    words.append(info_elems[0].split('\t')[0])
                elif info_elems[0][-6:] == "名詞":
                    # よみがなが得られる名詞
                    words.append(info_elems[6])
                else:
                    # info_elems[0] => 'ヴァンロッサム\t名詞'
                    # よみがなが得られない名詞、その他すべて
                    words.append(info_elems[0].split('\t')[0])
            return words
        except:
            print "Exception :".format(sentence)
            return []

class JumanPPSplitter():
    """
    Juman++を使って単語列(原形)を取得する
    """
    def __init__(self):
        self.jumanpp = Jumanpp()

    def split(self, sentence):
        try:
            result = self.jumanpp.analysis(sentence.decode('utf-8'))
            return [x.genkei.encode('utf-8') for x in result.mrph_list()]
        except:
            print "Exception :".format(sentence)
            return []


class NoWakatiSplitter():
    """
    分かち書きをしない
    """
    def split(self, sentence):
        return [sentence]

