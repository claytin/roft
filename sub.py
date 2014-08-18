class sub():
	def __init__(self, _window, _look, _name):
		self.name = _name
		self.curItem = 0
		self.items = []

		self.window = _window
		self.look = _look

	def draw(self):
		self.window.clear()

		rightAlignWidth = 0
		#find longest
		for item in self.items:
			if len(str(item.score)) > rightAlignWidth:
				rightAlignWidth = len(str(item.score))

		voteCenter = int(rightAlignWidth / 2) + 2
		rightAlignWidth += 2
		itemOffset = 1
		itemLeftPad = 1
		itemRightPad = 1

		curitem = 0
		for item in self.items:
			if curitem == self.curItem:
				#draw border top part
				self.window.move(itemOffset - 1, 0)
				self.window.addstr(self.look['special_characters'][3])
				self.window.move(itemOffset - 1 + 4, 0)
				self.window.addstr(self.look['special_characters'][5])
				self.window.move(itemOffset - 1 + 4, self.window.getmaxyx()[1] - 1)
				self.window.addstr(self.look['special_characters'][1])
				for i in range(1, self.window.getmaxyx()[1] - 1):
					self.window.move(itemOffset - 1, i)
					self.window.addstr(self.look['special_characters'][0])
					self.window.move(itemOffset - 1 + 4, i)
					self.window.addstr(self.look['special_characters'][0])
				self.window.move(itemOffset - 1, self.window.getmaxyx()[1] - itemLeftPad)
				self.window.addstr(self.look['special_characters'][4])
				for i in range(1, 4):
					self.window.move(itemOffset - 1 + i, self.window.getmaxyx()[1] - itemLeftPad)
					self.window.addstr(self.look['special_characters'][2])
					self.window.move(itemOffset - 1 + i, 0)
					self.window.addstr(self.look['special_characters'][2])


			itemTextOffset = 0

			self.window.move(itemOffset, voteCenter + itemLeftPad)
			self.window.addstr(self.look['up_char'])
			self.window.move(itemOffset, rightAlignWidth + 1 + itemLeftPad)

			if len(item.title) < self.window.getmaxyx()[1] - (8 + itemRightPad):
				self.window.addstr(item.title)
			else:
				lastPos = 0
				while lastPos < len(item.title):
					self.window.move(itemOffset + itemTextOffset, rightAlignWidth + 1 + itemLeftPad)
					self.window.addstr(item.title[lastPos:(self.window.getmaxyx()[1] - (9 + itemRightPad)) + lastPos])
					lastPos = (self.window.getmaxyx()[1] - (9 + itemRightPad)) + lastPos
					itemTextOffset += 1

			itemOffset += 1
			self.window.move(itemOffset, 0 + itemLeftPad)
			self.window.addstr(str(curitem + 1))
			self.window.move(itemOffset, voteCenter -
				int(len(str(item.score)) / 2) + itemLeftPad)
			self.window.addstr(str(item.score))

			itemOffset += 1
			self.window.move(itemOffset, voteCenter + itemLeftPad)
			self.window.addstr(self.look['down_char'])

			itemOffset += int(self.look['post_pad']) + 1
			if itemTextOffset > 3:
				itemOffset += itemTextOffset - 3

			curitem += 1

		self.window.refresh()


class subItem():
	def __init__(self, _title, _score, _user, _upScore, _downScore, _comments):
		self.title = _title
		self.score = _score
		self.user = _user
		self.upScore = _upScore
		self.downScore = _downScore
		self.comments = _comments
