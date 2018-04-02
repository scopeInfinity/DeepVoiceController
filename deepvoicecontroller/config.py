import os

class Config():
    def __init__(self):
        self.HOME = '/home/gagan.cs14/DeepVoiceController/deepvoicecontroller'

    def getHome(self):
        return self.HOME

    def getDatasetDir(self):
        return os.path.join(self.getHome(), "dataset")

    def getModelFname(self):
    	w_dir = os.path.join(self.getHome(), "Weights")
    	list_of_files=[os.path.join(w_dir, x) for x in os.listdir(w_dir)]
        latest_file = max(list_of_files, key=os.path.getctime)
        print("Using %s as model"%latest_file)
        return latest_file