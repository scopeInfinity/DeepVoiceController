import os

class Config():
    def __init__(self):
        self.HOME = '/home/scopeinfinity/OSS/DeepVoiceController/deepvoicecontroller'

    def getHome(self):
        return self.HOME

    def getDatasetDir(self):
        return os.path.join(self.getHome(), "dataset")

    def getModelFname(self):
    	return os.path.join(self.getHome(), "model")