import os

class Config():
    def __init__(self):
        self.HOME = os.path.dirname(os.path.realpath(__file__))

    def getHome(self):
        return self.HOME

    def getDatasetDir(self):
        return os.path.join(self.getHome(), "dataset")

    def getModelFname(self):
    	w_dir = os.path.join(self.getHome(), "Weights")
    	list_of_files=[os.path.join(w_dir, x) for x in os.listdir(w_dir)]
        if len(list_of_files) == 0:
            return None,0
        latest_file = max(list_of_files, key=os.path.getctime)
        print("Using %s as model"%latest_file)
        start_epoch = int(latest_file.split("-")[-2].split(".")[-1])
        return latest_file,start_epoch