import argparse
import sys

from config import Config
from datahandler import DataHandler
from word_parser import word_parser

def save_img(fname,tfname):
    from audio import load_and_preprocess_audio
    from PIL import Image
    mat= load_and_preprocess_audio(fname, False)
    img = Image.fromarray(mat, 'L')
    img.save(tfname)

def main():
    config = Config()
    parser = argparse.ArgumentParser()
    parser.add_argument('-td', '--test-dataset', help='Walk through dataset \
        and test while preprocessing', action='store_true')
    parser.add_argument('-e', '--execute', help='Execute',  action='store_true')
    parser.add_argument('-d', '--dry', help='Dry Run',  action='store_true')
    parser.add_argument('-t', '--train', help='Train Model', action='store_true')
    parser.add_argument('-wp', '--word-parser', help='Listen to microphone parse the word', action='store_true')
    parser.add_argument('-p', '--predict', help='Predict Audiofile', nargs='+')
    parser.add_argument('-si', '--save_image', help='Save Image from wav')
    parser.add_argument('-ti', '--target_image', help='Save Image target file')

   
    args = parser.parse_args()
    if args.test_dataset:
        datahandler = DataHandler()
        print("Test Passed")
        return
    if args.save_image and args.target_image:
        save_img(args.save_image,args.target_image)
    if args.execute:
        from event_handler import EventHandler
        eh = EventHandler(args.dry)
        word_parser(eh)
    if args.train:
        from model import Model
        model = Model()
        model.train()
    if args.predict:
        from model import Model
        model=Model()
        datahandler = DataHandler(noActualLoad = True)
        result = model.predict(args.predict, datahandler.getClasses(),whole = True)
        for fname, res in zip(args.predict, result):
            print("%s\t%s"%(fname,str(res))) 
    if args.word_parser:
        word_parser()

if __name__ == '__main__':
    main()

