#!/bin/sh

# mecab
./main.py --local-scheduler TrainWord2VecModel
# jumanpp
./main.py --local-scheduler TrainWord2VecModel --TrainWord2VecModel-splitter jumanpp

