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
    parser.add_argument('--predict', help='Predict Audiofile', nargs='+')
   
    args = parser.parse_args()
    if args.test_dataset:
        datahandler = DataHandler()
        print("Test Passed")
        return
    if args.train:
        model = Model()
        model.train()
    if args.predict:
        model=Model()
        datahandler = DataHandler(noActualLoad = True)
        result = model.predict(args.predict, datahandler.getClasses())
        for fname, res in zip(args.predict, result):
            print("%s\t%s"%(fname,res)) 

if __name__ == '__main__':
    main()

