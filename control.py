import interface

class control():
	def __init__(self, _keymap, _look):
		self.keymap = _keymap
		self.look = _look
		self.subs = []

		self.ui = interface.interface(self.event, self.look)
		self.ui.run()

	def event(self, key):
		if key == self.keymap["exit"] or key == "^[":
			pass
		if key == self.keymap["kill"]:
			self.ui.stop()

		if key == "KEY_RESIZE":
			self.ui.headerBar.resize(5, self.ui.stdscr.getmaxyx()[1])
			self.ui.stdscr.refresh()
			self.ui.resize(self.ui.headerBar)
