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
		itemOffset = 0

		curitem = 0
		for item in self.items:
			itemTextOffset = 0

			self.window.move(itemOffset, voteCenter)
			self.window.addstr(self.look['up_char'])
			self.window.move(itemOffset, rightAlignWidth + 1)

			if len(item.title) < self.window.getmaxyx()[1] - 7:
				self.window.addstr(item.title)
			else:
				lastPos = 0
				while lastPos < len(item.title):
					self.window.move(itemOffset + itemTextOffset, rightAlignWidth + 1)
					self.window.addstr(item.title[lastPos:(self.window.getmaxyx()[1] - 8) + lastPos])
					lastPos = (self.window.getmaxyx()[1] - 8) + lastPos
					itemTextOffset += 1

			itemOffset += 1
			self.window.move(itemOffset, 0)
			self.window.addstr(str(curitem + 1))
			self.window.move(itemOffset, voteCenter -
				int(len(str(item.score)) / 2))
			self.window.addstr(str(item.score))

			itemOffset += 1
			self.window.move(itemOffset, voteCenter)
			self.window.addstr(self.look['down_char'])
			curitem += 1

			itemOffset += int(self.look['post_pad']) + 1
			if itemTextOffset > 0:
				itemOffset += itemTextOffset - 3

		self.window.refresh()


class subItem():
	def __init__(self, _title, _score, _user, _upScore, _downScore, _comments):
		self.title = _title
		self.score = _score
		self.user = _user
		self.upScore = _upScore
		self.downScore = _downScore
		self.comments = _comments
