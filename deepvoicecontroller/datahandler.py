from config import Config
from audio import load_and_preprocess_audio
CLASSES = 5

class DataHandler():
    """
    Handler for Dataset

    @ratio ratio of train, validation, test dataset
    """

    def __init__(self, ratio=[0.7, 0.15, 0.15]):
    	self.config = Config()
        # DataX : Preprocessed Audio
        # DataY : Class
        self.dataX = []
        self.dataY = []

        self.word2ind = dict()
        self.ind2word = []
        self.ratio = ratio
        assert(len(ratio)==3)
        assert(ratio[0]+ratio[1]+ratio[2]==1.0)
        self.load()
        print("Classes for Words. Found {}, Expected {}".format(len(self.ind2word), CLASSES))
        assert(len(self.ind2word)==CLASSES)

    # static
    def get_instance():
    	pass
    	
    def getClasses(self):
        return CLASSES

    def load(self):
        data_dir = self.config.getDatasetDir()
        # TODO : Load Data and call newDataElement
        pass

        self.dataskip = [0]                                             		# Train
        self.dataskip.append(int(self.ratio[0]*len(self.dataX)))                # Validation
        self.dataskip.append(int((self.ratio[0]+self.ratio[1])*len(self.dataX)))# Test
        self.dataskip.append(len(self.dataX))                            		# Full Dataset

    def newDataElement(self, audio_filename, word):
        x = load_and_preprocess_audio(audio_filename)
        if word not in self.ind2word:
            self.word2ind[word] = len(self.ind2word)
            self.ind2word.append(word)
        y = self.word2ind[word]
        self.dataX.append(x)
        self.dataX.append(y)

    

    def getSplitHalf(self, indx):
        content = [self.dataX[self.dataskip[indx]:self.dataskip[indx+1]], self.dataY[self.dataskip[indx]:self.dataskip[indx+1]]]
        print("Dataset for [{:7}] : {:3}".format(["Train","Validation","Test"][indx], len(content)))

    def getTrainSplit(self):
        return self.getSplitHalf(0)

    def getValidationSplit(self):
        return self.getSplitHalf(1)

    def getTestSplit(self):
        return self.getSplitHalf(2)


        


