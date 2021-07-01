#!/sr/bin/env python
# -*- coding: utf-8 -*-
from gensim.models import word2vec

model = word2vec.Word2Vec.load("var/wikipedia_mecab.model")
# model = word2vec.Word2Vec.load("var/wikipedia_jumanpp.model")

print("ジンギスカン - 北海道 + 大阪")
for x in model.wv.most_similar(positive=["ジンギスカン", "大阪"], negative=["北海道"]):
    print(x[0], x[1])

print("人生 - お金")
for x in model.wv.most_similar(positive=["人生"], negative=["お金"]):
    print(x[0], x[1])
