import interface

class control():
	def __init__(self, _keymap, _look):
		self.min_width = 10
		self.min_height = 10

		self.keymap = _keymap
		self.look = _look
		self.subs = []

		self.ui = interface.interface(self.event, self.look)
		self.ui.run()

	def event(self, key):
		global min_width
		global min_height

		if key == self.keymap["exit"] or key == "^[":
			pass
		if key == self.keymap["kill"]:
			self.ui.stop()

		if key == "KEY_RESIZE":
			if self.ui.stdscr.getmaxyx()[1] < self.min_width or \
				self.ui.stdscr.getmaxyx()[0] < self.min_height:
				self.ui.stdscr.clear()
				self.ui.stdscr.move(int(self.ui.stdscr.getmaxyx()[0] / 2),
					int(self.ui.stdscr.getmaxyx()[1] / 2) - 4)
				self.ui.stdscr.addstr("too small")
				return

			self.ui.headerBar.resize(5, self.ui.stdscr.getmaxyx()[1])
			self.ui.stdscr.refresh()
			self.ui.resize(self.ui.headerBar)
