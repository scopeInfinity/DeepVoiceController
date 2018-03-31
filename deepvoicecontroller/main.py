import argparse
import sys

from config import Config
from datahandler import DataHandler
from model import Model

def main():
    config = Config()
    parser = argparse.ArgumentParser()
    parser.add_argument('-td', '--test-dataset', help='Walk through dataset \
        and test while preprocessing', action='store_true')
    parser.add_argument('-t', '--train', help='Train Model', action='store_true')
    parser.add_argument('-wp', '--word-parser', help='Listen to microphone parse the word', action='store_true')
    args = parser.parse_args()
    if args.test_dataset:
        datahandler = DataHandler()
        print("Test Passed")
        return
    if args.train:
        model = Model()
        

if __name__ == '__main__':
    main()
