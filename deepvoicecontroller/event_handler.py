class EventHandler():
	def __init__(self):
		self.active = False
		print("Give command followed by 'marvin'")

 	def command_stop(self):
 		print("COMMAND STOP")

	def gotWord(self,word):
		if word == "marvin":
			self.active = True
			print("Command Mode")
			return
		elif self.active:
			self.active = False
			if word == "stop":
				self.command_stop()
				return
			print("Command Failed")


		