from datahandler import DataHandler
from model import Model
from audio import capture_audio
import time
import threading

lastword=[None,time.time()]

def newword(word):
    print(">>>>>>>>>>>>>>>>>>>>>> New Word : %s"%word)
    # exit()

def callback_word(callback_free, fname):
    result = None
    now = time.time()
    if fname is not None:
        result = model.predict([fname], datahandler.getClasses())
        lastword[1]=now
        lastword[0]=result
        # print(result)
   
    if callback_free is not None:
        callback_free[0]=True

    lasttime = lastword[1]
    if (now - lasttime )*1000 > 1000:
        if lastword[0] is not None:
            newword(lastword[0])
        lastword[0]=None

def word_parser():
    global model
    global datahandler
    model=Model()
    datahandler = DataHandler(noActualLoad = True)
    capture_audio(callback_word)

