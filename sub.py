import urwid

class sub(urwid.WidgetWrap):
	def __init__(self, _look, _name):
		self.name = _name
		self.curItem = 0
		self.items = []

		self.look = _look

		self.scroll = 0
		#create initla pad (will resize later)
		#self.itemPad = curses.newpad(self.window.getmaxyx()[0],
		#self.window.getmaxyx()[1])

		urwid.WidgetWrap.__init__(self, self.main_window())

	def moveUp(self):
		if self.curItem > 0:
			self.curItem -= 1
		self.draw()

	def moveDown(self):
		if self.curItem < len(self.items) - 1:
			self.curItem += 1
		self.draw()

	def draw(self):
		self.itemPad.clear()
		self.itemPad.resize(1000, self.window.getmaxyx()[1])

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
			itemTextOffset = 0

			self.itemPad.move(itemOffset, voteCenter + itemLeftPad)
			self.itemPad.addstr(self.look['up_char'])
			self.itemPad.move(itemOffset, rightAlignWidth + 1 + itemLeftPad)

			if len(item.title) < self.itemPad.getmaxyx()[1] - (8 + itemRightPad):
				self.itemPad.addstr(item.title)
			else:
				lastPos = 0
				while lastPos < len(item.title):
					self.itemPad.move(itemOffset + itemTextOffset,
						rightAlignWidth + 1 + itemLeftPad)
					self.itemPad.addstr(item.title[
						lastPos:(self.itemPad.getmaxyx()[1] -
						(9 + itemRightPad)) + lastPos])
					lastPos = (self.itemPad.getmaxyx()[1] -
						(9 + itemRightPad)) + lastPos
					itemTextOffset += 1

			itemOffset += 1
			self.itemPad.move(itemOffset, 0 + itemLeftPad)
			self.itemPad.addstr(str(curitem + 1))
			self.itemPad.move(itemOffset, voteCenter -
				int(len(str(item.score)) / 2) + itemLeftPad)
			self.itemPad.addstr(str(item.score))

			itemOffset += 1
			self.itemPad.move(itemOffset, voteCenter + itemLeftPad)
			self.itemPad.addstr(self.look['down_char'])

			itemOffset += int(self.look['post_pad']) + 1
			if itemTextOffset > 3:
				itemOffset += itemTextOffset - 3

			if curitem == self.curItem:
				borderOffset = 0
				borderHeight = 0
				if itemTextOffset > 0:
					borderOffset = itemOffset - itemTextOffset - 1
					borderHeight = itemTextOffset + 1
				else:
					borderOffset = itemOffset - 4
					borderHeight = 4

				#draw border top part
				self.itemPad.move(borderOffset - 1, 0)
				self.itemPad.addstr(self.look['special_characters'][3])
				self.itemPad.move(borderOffset - 1 + borderHeight, 0)
				self.itemPad.addstr(self.look['special_characters'][5])
				self.itemPad.move(borderOffset - 1 + borderHeight,
					self.itemPad.getmaxyx()[1] - 1)
				self.itemPad.addstr(self.look['special_characters'][1])
				for i in range(1, self.itemPad.getmaxyx()[1] - 1):
					self.itemPad.move(borderOffset - 1, i)
					self.itemPad.addstr(self.look['special_characters'][0])
					self.itemPad.move(borderOffset - 1 + borderHeight, i)
					self.itemPad.addstr(self.look['special_characters'][0])
				self.itemPad.move(borderOffset - 1, self.itemPad.getmaxyx()[1] -
					itemLeftPad)
				self.itemPad.addstr(self.look['special_characters'][4])
				for i in range(1, borderHeight):
					self.itemPad.move(borderOffset - 1 + i,
						self.itemPad.getmaxyx()[1] - itemLeftPad)
					self.itemPad.addstr(self.look['special_characters'][2])
					self.itemPad.move(borderOffset - 1 + i, 0)
					self.itemPad.addstr(self.look['special_characters'][2])

			curitem += 1

		self.itemPad.refresh(self.scroll, 0, self.window.getbegyx()[0], 0,
			self.window.getmaxyx()[0], self.window.getmaxyx()[1])

class subItem():
	def __init__(self, _title, _score, _user, _upScore, _downScore, _comments):
		self.title = _title
		self.score = _score
		self.user = _user
		self.upScore = _upScore
		self.downScore = _downScore
		self.comments = _comments
