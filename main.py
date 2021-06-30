#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import re
import logging
import argparse

from gensim.models import word2vec
from luigi.format import Nop
import requests
import luigi

from utils import MecabSplitter, NoWakatiSplitter  # JumanPPSplitter,


class DownloadWikipediaDump(luigi.Task):
    """
    Wikipediaのダンプデータをダウンロードする
    """

    url = (
        "https://dumps.wikimedia.org/jawiki/latest/jawiki-latest-pages-articles.xml.bz2"
    )

    def output(self):
        return luigi.LocalTarget(
            "downloads/jawiki-latest-pages-articles.xml.bz2", format=Nop
        )

    def run(self):
        r = requests.get(self.url, stream=True)
        with self.output().open("wb") as f_out:
            for chunk in r.iter_content(chunk_size=1024):
                f_out.write(chunk)


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


class ParseWikipediaDump(luigi.Task):
    """
    ダウンロードしたWikipediaのデータをパースする
    参考 : http://taka-say.hateblo.jp/entry/2016/05/20/221817
    """

    def requires(self):
        return DecompressWikipediaDump()

    def output(self):
        return luigi.LocalTarget("var/wikipedia_extracted")

    def run(self):
        import os

        with self.output().temporary_path() as temp_output_path:
            args = [
                "python",
                "lib/wikiextractor-master/WikiExtractor.py",
                "-b",
                "20M",
                "-o",
                temp_output_path,
                self.input().path,
            ]
            os.system(" ".join(args))


class SplitWords(luigi.Task):
    """
    パースしたWikipediaの文章を分かち書きする
    """

    splitter = luigi.Parameter(default="mecab")

    def requires(self):
        return ParseWikipediaDump()

    def output(self):
        return luigi.LocalTarget("var/split_{}_wikipedia.txt".format(self.splitter))

    def run(self):
        pattern = re.compile("<doc.*>|<\\/doc>")
        if self.splitter == "mecab":
            splitter = MecabSplitter()
        # elif self.splitter == 'jumanpp':
        # splitter = JumanPPSplitter()
        else:
            splitter = NoWakatiSplitter()
        with self.output().open("w") as f_output:
            for source in glob.iglob(self.input().path + "/*/wiki*"):
                with open(source, "r") as f_input:
                    for line in f_input:
                        if pattern.match(line) or len(line) == 1:
                            continue
                        words = splitter.split(line)
                        f_output.write(" ".join(words) + "\n")


class TrainWord2VecModel(luigi.Task):
    """
    Word2Vecのモデルを学習する
    """

    splitter = luigi.Parameter(default="mecab")

    def requires(self):
        return SplitWords(splitter=self.splitter)

    def output(self):
        return luigi.LocalTarget("var/wikipedia_{}.model".format(self.splitter))

    def run(self):
        logging.basicConfig(
            format="%(asctime)s : %(levelname)s : %(message)s", level=logging.INFO
        )

        sentences = word2vec.Text8Corpus(self.input().path)
        model = word2vec.Word2Vec(sentences, size=200, min_count=20, window=15)
        model.save(self.output().path)


if __name__ == "__main__":
    luigi.run()
