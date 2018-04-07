import argparse
import sys

from config import Config
from datahandler import DataHandler
from model import Model
from word_parser import word_parser

def main():
    config = Config()
    parser = argparse.ArgumentParser()
    parser.add_argument('-td', '--test-dataset', help='Walk through dataset \
        and test while preprocessing', action='store_true')
    parser.add_argument('-e', '--execute', help='Execute',  action='store_true')
    parser.add_argument('-t', '--train', help='Train Model', action='store_true')
    parser.add_argument('-wp', '--word-parser', help='Listen to microphone parse the word', action='store_true')
    parser.add_argument('-p', '--predict', help='Predict Audiofile', nargs='+')
   
    args = parser.parse_args()
    if args.test_dataset:
        datahandler = DataHandler()
        print("Test Passed")
        return
    if args.execute:
        from event_handler import EventHandler
        eh = EventHandler()
        word_parser(eh)
    if args.train:
        model = Model()
        model.train()
    if args.predict:
        model=Model()
        datahandler = DataHandler(noActualLoad = True)
        result_prob = model.predict(args.predict, datahandler.getClasses())
        for fname, rp in zip(args.predict, result_prob):
            print("%s\t%s\twith Probabity %f"%(fname,rp[0],rp[1])) 
    if args.word_parser:
        word_parser()

if __name__ == '__main__':
    main()

