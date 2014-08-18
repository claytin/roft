class sub():
	def __init__(self, _window, _look, _name):
		self.name = _name
		self.curItem = 0
		self.items = []

		self.window = _window
		self.look = _look

	def draw(self):
		rightAlignWidth = 0
		#find longest
		for item in self.items:
			if len(str(item.score)) > rightAlignWidth:
				rightAlignWidth = len(str(item.score))

		voteCenter = int(rightAlignWidth / 2) + 2
		rightAlignWidth += 2

		curitem = 0
		for item in self.items:
			itemOffset = curitem * (3 + int(self.look['post_pad']))

			self.window.move(itemOffset, voteCenter)
			self.window.addstr(self.look['up_char'])
			self.window.move(itemOffset, rightAlignWidth + 1)
			self.window.addstr(item.title)

			self.window.move(itemOffset + 1, 0)
			self.window.addstr(str(curitem + 1))
			self.window.move(itemOffset + 1, voteCenter -
				int(len(str(item.score)) / 2))
			self.window.addstr(str(item.score))

			self.window.move(itemOffset + 2, voteCenter)
			self.window.addstr(self.look['down_char'])
			curitem += 1

		self.window.refresh()

		self.window.move(0, 0)
		self.window.addstr(".")
		self.window.move(self.window.getmaxyx()[0] - 1, 0)
		self.window.addstr(".")
		self.window.move(self.window.getmaxyx()[0] - 1, self.window.getmaxyx()[1] - 2)
		self.window.addstr(".")
		self.window.move(0, self.window.getmaxyx()[1] - 2)
		self.window.addstr(".")

class subItem():
	def __init__(self, _title, _score, _user, _upScore, _downScore, _comments):
		self.title = _title
		self.score = _score
		self.user = _user
		self.upScore = _upScore
		self.downScore = _downScore
		self.comments = _comments
