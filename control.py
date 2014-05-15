import threading
import curses
import interface

class control():
	def __init__(self, _keymap):
		self.keymap = _keymap
		self.subs = []

		self.ui = interface.interface(self.event)
		self.ui.start()

	def event(self, key):
		if key == self.keymap["exit"] or key == self.keymap["kill"]:
			self.ui.stop()
