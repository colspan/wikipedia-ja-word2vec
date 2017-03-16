#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gensim.models import word2vec

model = word2vec.Word2Vec.load("var/wikipedia_mecab.model")
#model = word2vec.Word2Vec.load("var/wikipedia_jumanpp.model")

print u'ジンギスカン - 北海道 + 大阪'
for x in model.most_similar(positive=[u'ジンギスカン', u'大阪'], negative=[u'北海道']):
    print x[0], x[1]

print u'人生 - お金'
for x in model.most_similar(positive=[u'人生'], negative=[u'お金']):
    print x[0], x[1]
