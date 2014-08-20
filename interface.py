import curses
from curses import wrapper

#ui stuff
import headerBar
import infoBar
import sub

class interface():
	def __init__(self, _event, _look):
		self.event = _event
		self.look = _look

	def run(self):
		wrapper(self.init)

	#set everything up then take input and send it to control
	def init(self, _stdscr):
		self.stdscr = _stdscr
		self.stdscr.clear()
		self.stdscr.refresh()

		curses.curs_set(False)

		#create color pairs
		curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLACK)
		curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)

		#first load message
		firstLoad = True
		if firstLoad:
			pass

		#sub stuff
		self.subWindow = curses.newwin(_stdscr.getmaxyx()[0] - 4,
			self.stdscr.getmaxyx()[1], 4, 0)
		self.sub = sub.sub(self.subWindow, self.look, "test_sub")

		testitem0 = sub.subItem("test item 1's title", 420, "poster name",
			420, 0, 69)
		testitem1 = sub.subItem("abcabcabcabcabcabcabcabcabcabcabcabcabcabc" \
			"abcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabcab" \
			"cabcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabca" \
			"bcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabc" \
			"abcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabcab" \
			"cabcabcabc", 1337, "another poster", 1339, 2, 69)
		testitem2 = sub.subItem("post title", -101, "yep...", 1, 102, 69)
		testitem3 = sub.subItem("some item", 1, "poster name", 420, 0, 5)
		testitem4 = sub.subItem("breaking news?", 12, "ass", 1339, 5, 12)
		testitem5 = sub.subItem("idk...", 12234, "piss", 1, 0, 1)

		self.sub.items = [testitem0, testitem1, testitem2, testitem3,
			testitem4, testitem5]

		#set this test sub as the current
		self.curSub = self.sub

		#header bar stuff
		self.headerBarWindow = curses.newwin(4, self.stdscr.getmaxyx()[1],
			1, 0)
		self.headerBar = headerBar.headerBar(self.headerBarWindow, self.look,
			self.drawTab)
		self.headerBar.sublist = self.headerBar.sublist + [self.sub]

		#infobar stuff
		if self.look['infobar_pos'] == "top":
			infobar_pos = 0
		else:
			infobar_pos = self.stdscr.getmaxyx()[0] - 4

		self.infoBarWindow = curses.newwin(1, self.stdscr.getmaxyx()[1],
			infobar_pos, 0)
		self.infoBar = infoBar.infoBar(self.infoBarWindow, self.look)
		self.infoBar.setString("status", "starting up")

		self.headerBar.draw()
		self.sub.draw()

		while True:
			key = self.stdscr.getkey()
			self.infoBar.setString("key", "key: " + repr(key))

			self.event(key)

	def resize(self):
		self.stdscr.refresh()

		self.headerBarWindow.resize(5, self.stdscr.getmaxyx()[1])
		self.headerBar.draw()

		self.infoBarWindow.resize(1, self.stdscr.getmaxyx()[1])
		self.infoBar.draw()

		self.subWindow.resize(self.stdscr.getmaxyx()[0] - 4,
			self.stdscr.getmaxyx()[1])
		self.sub.draw()

	def drawTab(self, window, x, y, selected = False, string = "", w = False,
		roundr = False, roundl = False, paddingr = False, paddingl = False,
		padding = True):
		pos = x
		if not w:
			w = len(string)
			if self.look['tab_padding'] == "true":
				#if padding add a space for each side
				w += 2

		draw_string = "xxxxxx"
		if self.look['use_special_characters'] == "true":
			if selected and self.look['thicken_selected'] == "true":
				draw_string = self.look['special_characters_bold']
			else:
				draw_string = self.look['special_characters']
		else:
			draw_string = self.look['ascii_characters']

		#left side
		window.move(y, pos)
		if self.look['thicken_selected'] == "true":
			if selected:
				window.addch(draw_string[1])
			else:
				window.addch(self.look['special_characters_bold'][6])
		else:
			if selected:
				window.addch(draw_string[1])
			else:
				window.addch(draw_string[6])
		window.move(y - 1, pos)
		window.addch(draw_string[2])
		window.move(y - 2, pos)
		if roundl and self.look['use_special_characters'] == "true":
			window.addch(self.look['special_characters_round'][0])
		else:
			if paddingl or padding:
				window.addch(draw_string[3])
			else:
				window.addch(draw_string[7])

		#middle... ish
		if self.look['tab_padding'] == "true":
			window.move(y - 1, pos + 2)
		else:
			window.move(y - 1, pos + 1)

		window.addstr(string)
		for part in range(w):
			window.move(y - 2, pos + part + 1)
			window.addch(draw_string[0])
			if selected:
				window.move(y - 0, pos + part + 1)
				window.addch(" ")

		pos += w + 1

		#right side
		window.move(y, pos)
		if self.look['thicken_selected'] == "true":
			if selected:
				window.addch(draw_string[5])
			else:
				window.addch(self.look['special_characters_bold'][6])
		else:
			if selected:
				window.addch(draw_string[5])
			else:
				window.addch(draw_string[6])

		window.move(y - 1, pos)
		window.addch(draw_string[2])
		window.move(y - 2, pos)
		if roundr and self.look['use_special_characters'] == "true":
			window.addch(self.look['special_characters_round'][1])
		else:
			if paddingr or padding:
				window.addch(draw_string[4])
			else:
				window.addch(draw_string[8])

		return pos

	def stop(self):
		exit()
