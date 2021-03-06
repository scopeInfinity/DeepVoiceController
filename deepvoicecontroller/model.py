import os
import numpy as np
from config import Config
from datahandler import DataHandler
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Activation
from keras.layers import LSTM 
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dropout
from keras.layers import ELU
from keras.layers.normalization import BatchNormalization
from keras.callbacks import ModelCheckpoint
from keras.layers import TimeDistributed
from audio import no_of_mels as frequencies
from audio import msg_width as timestamps

class Model():
	"""Model Voice to Text Classification"""
	def __init__(self):
		self.config = Config()
		self.build_model()
		self.load_model()

	def build_model(self):
		self.model = Sequential()
		self.model.add(Conv2D(32, kernel_size=(3, 3),
		                 input_shape=(timestamps,frequencies,1),
                                 data_format="channels_last"))
		self.model.add(BatchNormalization(axis=1, mode=0))
		self.model.add(Activation('relu'))
		self.model.add(MaxPooling2D(pool_size=(2, 2)))
		self.model.add(Dropout(0.3))
		self.model.add(Conv2D(32, (3, 3)))
		self.model.add(BatchNormalization(axis=1, mode=0))
		self.model.add(ELU())
		self.model.add(MaxPooling2D(pool_size=(2, 2)))
		self.model.add(Dropout(0.3))
		self.model.add(Conv2D(32, (3, 3)))
		self.model.add(BatchNormalization(axis=1, mode=0))
		self.model.add(ELU())
		self.model.add(MaxPooling2D(pool_size=(2, 2)))
		self.model.add(Dropout(0.3))
		self.model.add(Conv2D(32, (3, 3)))
		self.model.add(BatchNormalization(axis=1, mode=0))
		self.model.add(ELU())
		self.model.add(MaxPooling2D(pool_size=(2, 2)))
		self.model.add(Dropout(0.3))
		
		# self.model.add(Conv2D(64, (3, 3), activation='relu'))
		# self.model.add(MaxPooling2D(pool_size=(2, 2)))
		# self.model.add(Dropout(0.25))
		self.model.add(Flatten())
		self.model.add(Dense(64, activation='relu'))
		self.model.add(Dropout(0.5))
		self.model.add(Dense(30, 
						 activation='softmax'))
		self.model.compile(optimizer='rmsprop', 
			              loss='categorical_crossentropy',
			              metrics=['accuracy'])


	def load_model(self):
		fname,self.start_epoch = self.config.getModelFname()
		if fname is not None and os.path.exists(fname):
			# TODO : Load weights from fname
			print("Loading Weights from %s"%fname)
			self.model.load_weights(fname)
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
					initial_epoch=self.start_epoch,
					validation_split=0.8,
					epochs=10000, 
					batch_size=500,
					verbose=1,
					callbacks=[saved])

	def predict(self,file_names, classes_names, whole = False):
		from audio import load_and_preprocess_audio
		x = []
		for fname in file_names:
			x.append( load_and_preprocess_audio(fname, True) )	
		y=self.model.predict(np.array(x))
		results = []
		for _y in y:
			_ind = np.argmax(_y)
			_max = np.max(_y)
			assert _max == _y[_ind]
			assert abs(np.sum(_y) - 1.0)<1e-5
			whole = []
			for j in range(len(_y)):
				whole.append((classes_names[j], _y[j] ))
			if whole:
				results.append(whole)
			else:
				results.append((classes_names[_ind  ],_max) )
		return results
