import os
import Tkinter as tk
import tkMessageBox
import pyautogui

class EventHandler():
	def __init__(self, dry = False):
		self.active = False
		print("Give command followed by 'marvin'")
		self.list = ["BAD"]
		self.dry = dry

 	def command_sleep(self):
 		print("Command Sleep")
 		if self.dry:
			root = tk.Tk()
			root.withdraw()
			tkMessageBox.showwarning('Dry Run', 'Suspend Command')
		else:
 			os.system("systemctl suspend")

 	def clean(self):
 		self.list = []

 	def command_scroll(self,up):
 		print("Scroll, Mode UP : "+str(up))
 		if up:
 			pyautogui.press('pgup')
 		else:
 			pyautogui.press('pgdn')

 	def command_key(self,key):
 		print("Key stroke : "+key)
 		pyautogui.press(key)

	def gotWord(self,word):
		if word == "marvin":
			self.active = True
			print("Marvin Active")
			self.clean()
		elif self.active:
			self.list.append(word)
			if self.list == ["tree","stop"] or self.list == ["three","stop"]:
				self.command_sleep()
				self.clean()
			if self.list == ["sheila","up"]:
				self.command_key("volumeup")
				self.clean()
			if self.list == ["sheila","down"]:
				self.command_key("volumemute")
				self.clean()
			if self.list == ["bird", "up"]:
				self.command_scroll(up=True)
				self.clean()
			if self.list == ["bird", "down"]:
				self.command_scroll(up=False)
				self.clean()
			if self.list == ["yes"]:
				self.command_key("enter")
				self.clean()
			if self.list == ["no"]:
				self.command_key("esc")
				self.clean()
			if self.list == ["wow"]:
				self.command_key("prtscr")
				self.clean()
			if self.list == ["stop"]:
				self.active = False
				self.clean()






		