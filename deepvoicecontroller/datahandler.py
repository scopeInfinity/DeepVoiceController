from config import Config
from audio import load_and_preprocess_audio
import os
import random
import numpy as np

CLASSES = 30

class DataHandler():
    """
    Handler for Dataset

    @ratio ratio of train, validation, test dataset
    """

    def __init__(self, ratio=[0.85, 0.0, 0.15], noActualLoad = False):
        self.config = Config()
        # DataX : Preprocessed Audio
        # DataY : Class
        self.dataX = []
        self.dataY = []

        self.word2ind = dict()
        self.ind2word = ["bed","bird","cat","dog","down","eight","five","four","go","happy","house","left","marvin","nine","no","off","on","one","right","seven","sheila","six","stop","three","tree","two","up","wow","yes","zero"]
	for i,w in enumerate(self.ind2word):
		self.word2ind[w]=i
        self.ratio = ratio
        assert(len(ratio)==3)
        assert(ratio[0]+ratio[1]+ratio[2]==1.0)
	if not noActualLoad:
        	self.load()
        print("Classes for Words. Found {}, Expected {}".format(len(self.ind2word), CLASSES))
        assert(len(self.ind2word)==CLASSES)

    # static
    def get_instance(self):
    	pass
    	
    def getClasses(self):
        return self.ind2word

    def load(self):
        data_dir = self.config.getDatasetDir()
        # MX_PERCLASS = 100
        # TODO : Load Data and call newDataElement
        list_dir=os.listdir(data_dir)
        for classno, directory in enumerate(list_dir):
            if directory not in self.getClasses():
                continue
            directory_path=os.path.join(data_dir,directory)
            if os.path.isdir(directory_path):
                if directory[0]!="_":
                    files=os.listdir(directory_path)
                    for i,file in enumerate(files):
                        self.newDataElement(os.path.join(directory_path,file),directory)
                        print("Class Number %d, %.3f%% loaded"%(classno,(i*100.0/len(files))))
        self.getClasses()

        random.seed(17)
        train = zip(self.dataX,self.dataY)
        np.random.shuffle(train)
        [self.dataX, self.dataY] = [list(t) for t in zip(*train)]

        
        self.dataskip = [0]                                                     # Train
        self.dataskip.append(int(self.ratio[0]*len(self.dataX)))                # Validation
        self.dataskip.append(int((self.ratio[0]+self.ratio[1])*len(self.dataX)))# Test
        self.dataskip.append(len(self.dataX))                                   # Full Dataset

    def newDataElement(self, audio_filename, word, noActualLoad = False):
        x = load_and_preprocess_audio(audio_filename)
        y = self.word2ind[word]
        array_y=[0]*30
        array_y[y]=1
        self.dataX.append(x)
        self.dataY.append(array_y)
        # print(self.dataX)

    

    def getSplitHalf(self, indx):
        content = [self.dataX[self.dataskip[indx]:self.dataskip[indx+1]], self.dataY[self.dataskip[indx]:self.dataskip[indx+1]]]
        print("Dataset for [{:7}] : {:3}".format(["Train","Validation","Test"][indx], len(content)))
        return content

    def getTrainSplit(self):
        return self.getSplitHalf(0)

    def getValidationSplit(self):
        return self.getSplitHalf(1)

    def getTestSplit(self):
        return self.getSplitHalf(2)


        


