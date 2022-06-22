#!/bin/sh

## for Ubuntu
sudo apt-get install -y mecab libmecab-dev mecab-ipadic-utf8
sudo apt-get install -y python-mecab gensim
pip install -r requirements.txt

mkdir -p downloads

(cd downloads && wget http://nlp.ist.i.kyoto-u.ac.jp/nl-resource/knp/pyknp-0.3.tar.gz && tar xvf pyknp-0.3.tar.gz && cd pyknp-0.3 && sudo python setup.py install)

