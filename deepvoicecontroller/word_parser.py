from datahandler import DataHandler
from model import Model
from audio import capture_audio
import numpy as np
import time
import threading

lastword=[None,time.time(),0]
lastrecords = []
current_word_prob = dict()
def getitem(list_,key):
    # print list_
    for a,b in list_:
        if a==key:
            return b
    assert False

lastoccurance = time.time()-10000
def newword(result_whole, final_callback):
    # if word=="go":
    #     if prob<0.95:
    #         return
    # if word=="stop":
    #     if prob<0.99:
    #         return
    # lastrecords.append((word,prob))
    # if len(lastrecords)>5:
    #     # current_word_prob[lastrecords[0][0]]-=lastrecords[0][1]
    #     lastrecords.pop(0)
    # print(lastrecords)
    # print(word)
    for k in current_word_prob.keys():
        current_word_prob[k]=0.6*current_word_prob[k] + 0.4*getitem(result_whole, k) 
    
    # if len(lastrecords) == 5:
    best_word = max(current_word_prob, key=current_word_prob.get)
    if current_word_prob[best_word]<0.22:
        return
    # print(">>>>>>>>>>>>>>>>>>>>>> New Word : %s\tProb: %f"%(word,prob))
    now = time.time()
    global lastoccurance

    if now - lastoccurance > 1 : #1sec
        print(">>>>> \t"+str(current_word_prob[best_word])+" : "+str(best_word))
        lastoccurance = now
        if final_callback is not None:
            final_callback.gotWord(best_word)
    # exit()

def callback_word(callback_free, fname,final_callback=None):
    result = None
    now = time.time()
    # if fname is not None:
    if True:#callback_free[0]:
        # result_prob = model.predict([fname], datahandler.getClasses())
        result_whole = model.predict([fname], datahandler.getClasses(), whole = True)[0]
        # print("Caluculating %s"%str(np.shape(result_prob)))
        # lastword[1]=now
        # lastword[0]=result_prob[0][0]
        # lastword[2]=result_prob[0][1]

        newword(result_whole,final_callback)
        # print(result)
   
        callback_free[0]=True
    # if callback_free is not None:

    # lasttime = lastword[1]
    # if (now - lasttime )*1000 > 100:
    #     if lastword[0] is not None:
    #         newword(lastword[0],lastword[2])
    #     lastword[0]=None

def word_parser(final_callback=None):
    global model
    global datahandler
    model=Model()
    datahandler = DataHandler(noActualLoad = True)
    for i,word in enumerate( datahandler.getClasses()):
        current_word_prob[word]=0
    capture_audio(callback_word,final_callback)

