
class infoBar():
	def __init__(self, _window, _look):
		self.window = _window
		self.look = _look
		self.progress = False
		self.strings = {}

	def setString(self, _name, _string, _color = False):
		self.strings[_name] = {'string': _string, 'color': _color}
		self.draw()

	def setProgress(self, _progress = False):
		self.progress = _progress
		if self.progress > 100:
			self.progress = False
		self.draw()

	def draw(self):
		self.window.clear()
		self.window.move(0, 0)

		for item in self.strings:
			self.window.addstr(self.strings[item]['string'] + " ")

		progress_chars = 0
		if self.progress is not False:
			progress_chars = int((self.progress / 100) *
				self.window.getmaxyx()[1]) - 1
			for char in range(progress_chars):
				self.window.move(0, char)
				self.window.addch("#")
			self.window.move(0, int(self.window.getmaxyx()[1] / 2) - 2)
			self.window.addstr(str(self.progress) + "%")

		self.window.refresh()
