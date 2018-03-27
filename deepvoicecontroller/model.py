import os

from config import Config
from datahandler import DataHandler

class Model():
	"""Model Voice to Text Classification"""
	def __init__(self):
		self.config = Config()
		self.fname = self.config.getModelFname()
		self.build_model()
		self.load_model()
		self.datahandler = None

	def build_model(self):
		# TODO : Assign DNN Model
		self.model = None

	def load_model(self):
		if os.path.exists(self.fname):
			# TODO : Load weights from self.fname
			pass

	def train(self):
