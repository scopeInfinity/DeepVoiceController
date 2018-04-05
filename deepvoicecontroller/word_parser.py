from datahandler import DataHandler
from model import Model
from audio import capture_audio
import numpy as np
import time
import threading

lastword=[None,time.time(),0]
lastrecords = []
current_word_prob = dict()
def newword(word,prob):
    # if word=="go":
    #     if prob<0.95:
    #         return
    # if word=="stop":
    #     if prob<0.99:
    #         return
    lastrecords.append((word,prob))
    # print(lastrecords)
    if len(lastrecords)>5:
        current_word_prob[lastrecords[0][0]]-=lastrecords[0][1]
        lastrecords.pop(0)
    current_word_prob[word]+=prob
    if len(lastrecords) == 10:
        best_word = max(current_word_prob, key=current_word_prob.get)
    if current_word_prob[word]<1.0 or prob<0.85:
        return
    # print(">>>>>>>>>>>>>>>>>>>>>> New Word : %s\tProb: %f"%(word,prob))
    print(">>>>> \t"+str(current_word_prob[word])+" : "+str(word) +":"+str(prob))
    # exit()

def callback_word(callback_free, fname):
    result = None
    now = time.time()
    # if fname is not None:
    if True:#callback_free[0]:
        result_prob = model.predict([fname], datahandler.getClasses())
        # print("Caluculating %s"%str(np.shape(result_prob)))
        lastword[1]=now
        lastword[0]=result_prob[0][0]
        lastword[2]=result_prob[0][1]

        newword(lastword[0],lastword[2])
        # print(result)
   
        callback_free[0]=True
    # if callback_free is not None:

    # lasttime = lastword[1]
    # if (now - lasttime )*1000 > 100:
    #     if lastword[0] is not None:
    #         newword(lastword[0],lastword[2])
    #     lastword[0]=None

def word_parser():
    global model
    global datahandler
    model=Model()
    datahandler = DataHandler(noActualLoad = True)
    for i,word in enumerate( datahandler.getClasses()):
        current_word_prob[word]=0
    capture_audio(callback_word)

