#!/usr/bin/env python
# -*- coding: utf-8 -*-



import glob
import re
import logging
import argparse

from gensim.models import word2vec
import requests
import luigi
import luigi.contrib.external_program

from utils import split_to_words

class DownloadWikipediaDump(luigi.Task):
    """
    Wikipediaのダンプデータをダウンロードする
    """
    url = "https://dumps.wikimedia.org/jawiki/latest/jawiki-latest-pages-articles.xml.bz2"
    def output(self):
        return luigi.LocalTarget("downloads/jawiki-latest-pages-articles.xml.bz2")
    def run(self):
        r = requests.get(self.url)
        with self.output().open("w") as f_out:
            f_out.write(r.content)


class DecompressWikipediaDump(luigi.Task):
    """
    ダンプファイルの圧縮を展開
    """
    def requires(self):
        return DownloadWikipediaDump()
    def output(self):
        return luigi.LocalTarget("var/jawiki-latest-pages-articles.xml")
    def run(self):
        import os
        with self.output().temporary_path() as temp_output_path:
            args = ["bunzip2", "-c", self.input().path, ">", temp_output_path]
            os.system(" ".join(args))


class ParseWikipediaDump(luigi.contrib.external_program.ExternalProgramTask):
    """
    ダウンロードしたWikipediaのデータをパースする
    参考 : http://taka-say.hateblo.jp/entry/2016/05/20/221817
    """
    def requires(self):
        return DecompressWikipediaDump()
    def output(self):
        return luigi.LocalTarget("var/wikipedia_extracted")
    def program_args(self):
        args = [
            "python",
            "lib/wikiextractor-master/WikiExtractor.py",
            "-b",
            "20M",
            "-o",
            self.output().path,
            self.input().path
            ]
        print " ".join(args)
        return args


class SplitWords(luigi.Task):
    """
    パースしたWikipediaの文章を分かち書きする
    """
    def requires(self):
        return ParseWikipediaDump()
    def output(self):
        return luigi.LocalTarget("var/split_wikipedia.txt")
    def run(self):
        pattern = re.compile('<doc.*>|<\\/doc>')
        with self.output().open("w") as f_output:
            for source in glob.iglob(self.input().path + "/*/wiki*"):
                with open(source, "r") as f_input:
                    for line in f_input:
                        if pattern.match(line) or len(line) == 1:
                            continue
                        words = split_to_words(line)
                        print >> f_output, " ".join(words)


class TrainWord2VecModel(luigi.Task):
    """
    Word2Vecのモデルを学習する
    """
    def requires(self):
        return SplitWords()
    def output(self):
        return luigi.LocalTarget("var/wikipedia.model")
    def run(self):
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

        sentences = word2vec.Text8Corpus(self.input().path)
        model = word2vec.Word2Vec(sentences, size=200, min_count=20, window=15)
        model.save(self.output().path)


if __name__ == "__main__":
    luigi.run()
