# Wikipediaのダンプイメージを用いたWord2Vecモデル学習パイプライン

ダウンロード、前処理、モデル生成と手間がかかる一連のモデル学習作業をパイプラインとして再現可能な形にまとめました。

## 依存OSS

 - コーパス : [Wikipedia](https://ja.wikipedia.org/wiki/Wikipedia:%E3%83%87%E3%83%BC%E3%82%BF%E3%83%99%E3%83%BC%E3%82%B9%E3%83%80%E3%82%A6%E3%83%B3%E3%83%AD%E3%83%BC%E3%83%89)
 - コーパス切り出し : [WikiExtractor](https://github.com/attardi/wikiextractor)
 - 日本語分かち書き
    - [mecab](http://taku910.github.io/mecab/)
    - [Juman++](https://github.com/ku-nlp/jumanpp)
 - モデル生成 : [gensim](https://radimrehurek.com/gensim/)
 - パイプライン記述 : [Luigi](https://github.com/spotify/luigi)

## 動作確認環境

Ubuntu 14.04 LTS

## 使用方法

```bash
# Ubuntu向け環境構築
./00_prepare_envirionment_ubuntu.bash
# データダウンロード及び学習
./01_download_and_train.sh
# 学習結果を用いて類似度等を計算する
## 北海道の市町村同士の類似度を計算する
./02_calc_similarity_of_hokkaido_communes.sh
## なんとなく楽しそうな加減算をしてみる
./03_operate_words.py
```

## 参考文献

 - [【Python】日本語Wikipediaのダンプデータから本文を抽出する](http://taka-say.hateblo.jp/entry/2016/05/20/221817)
 - [katryo/tfidf_with_sklearn](https://github.com/katryo/tfidf_with_sklearn/blob/master/utils.py)
