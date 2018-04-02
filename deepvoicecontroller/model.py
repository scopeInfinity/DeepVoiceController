import os
import numpy as np
from config import Config
from datahandler import DataHandler
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Activation
from keras.layers import LSTM 
from keras.callbacks import ModelCheckpoint
from keras.layers import TimeDistributed
from audio import no_of_mels as frequencies
from audio import msg_width as timestamps

class Model():
	"""Model Voice to Text Classification"""
	def __init__(self):
		self.config = Config()
		self.fname = self.config.getModelFname()
		self.build_model()
		self.load_model()

	def build_model(self):
		self.model = Sequential()
		self.model.add(TimeDistributed( Dense(1000),
					 					input_shape=(timestamps,frequencies)))
		self.model.add(LSTM(1000,
						 activation='tanh',  
						 kernel_initializer='glorot_uniform', 
						 return_sequences=False))
		self.model.add(Dense(30, 
						 activation='softmax'))
		self.model.compile(optimizer='rmsprop', 
			              loss='categorical_crossentropy',
			              metrics=['accuracy'])


	def load_model(self):
		if os.path.exists(self.fname):
			# TODO : Load weights from self.fname
			print("Loading Weights from %s"%self.fname)
			self.model.load_weights(self.fname)
			print("Weights Loaded")

	def train(self):
		datah=DataHandler()
		train_data=datah.getTrainSplit()
		print(type(train_data))
		print(np.shape(train_data[0]))
		print(np.shape(train_data[1]))
		print(train_data[1])
		# test_data=datah.getTestSplit()
		# validation_data=datah.getValidationSplit()
		saved = ModelCheckpoint("Weights/weights.{epoch:02d}-{val_loss:.2f}.hdf5", monitor='val_loss', verbose=0, save_best_only=False, save_weights_only=False, mode='auto', period=1)			
		self.model.fit(np.array(train_data[0]), 
					train_data[1],
					validation_split=0.8,
					epochs=1000, 
					batch_size=200,
					verbose=2,
					callbacks=[saved])

	def predict(self,file_names, classes_names):
		from audio import load_and_preprocess_audio
		x = []
		for fname in file_names:
			x.append( load_and_preprocess_audio(fname) )	
		y=self.model.predict(np.array(x))
		results = []
		for _y in y:
			results.append(classes_names[ np.argmax(_y) ] )
		return results
