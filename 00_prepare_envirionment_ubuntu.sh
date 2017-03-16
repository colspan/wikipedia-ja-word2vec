#!/bin/sh

## for Ubuntu
sudo apt-get install -y mecab libmecab-dev mecab-ipadic-utf8
sudo apt-get install -y python-mecab
sudo pip install -r requirements.txt
sudo easy_install gensim

mkdir -p downloads
wget https://github.com/attardi/wikiextractor/archive/master.zip -O downloads/wikiextractor.zip
(mkdir -p lib && cd lib && unzip ../downloads/wikiextractor.zip)

(cd downloads && wget http://nlp.ist.i.kyoto-u.ac.jp/nl-resource/knp/pyknp-0.3.tar.gz && tar xvf pyknp-0.3.tar.gz && cd pyknp-0.3 && sudo python setup.py install)

