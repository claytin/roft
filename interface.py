import curses
from curses import wrapper

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

		#first load message
		firstLoad = True
		if firstLoad:
			pass

		#header bar stuff
		self.headerBar = curses.newwin(5, self.stdscr.getmaxyx()[1], 0, 0)
		self.drawHeader(self.headerBar)

		while True:
			key = self.stdscr.getkey()
			self.stdscr.move(0, 0)
			self.stdscr.addstr("key " + str(key))

			self.event(key)

	def resize(self, window):
		self.drawHeader(window)

	def drawHeader(self, window):
		#window w/h
		w = window.getmaxyx()[1]
		h = window.getmaxyx()[0]

		#tmp data
		#subs = ["Lorem", "ipsum", "dolor", "sit", "amet", "consectetur",
		#	"adipisicing", "elit", "sed", "do", "eiusmod", "tempor"]
		#	"Lorem", "ipsum", "dolor", "sit", "amet", "consectetur",
		#	"adipisicing", "elit", "sed", "do", "eiusmod", "tempor"]
		subs = ["aaa", "bbb", "ccc", "ddd", "eee"]
		cursub = 0

		#logins = ["curly", "booster", "sue", "balrog", "quote", "jack",
		#	"kazuma", "king"]
		logins = ["a", "b", "c", "d", "e"]
		curlogin = 1

		window.clear()
		#window.box(0, 0)

		#draw bottom line
		bottomBar = ""
		barchar = "x"
		if self.look['use_special_characters'] == "true":
			if self.look['thicken_selected'] == "true":
				barchar = self.look['special_characters_bold'][0]
			else:
				barchar = self.look['special_characters'][0]
		else:
			barchar = self.look['ascii_characters'][0]

		for pos in range(0, w):
			bottomBar = bottomBar + barchar
		window.move(h - 2, 0)
		window.addstr(bottomBar)

		#hide tabs when space is limited
		#each "+" tab takes up three plus spaces between leftside, logs/subs,
		#and logs/seach, and search box padding
		number_of_spacers = 3 + 3 + 3 + 2
		tab_padding_amount = 2
		search_box_with = int(self.look['search_box_max'])

		bar_total = search_box_with + number_of_spacers
		for sub in subs:
			bar_total += len(sub) + tab_padding_amount
		for log in logins:
			bar_total += len(log) + tab_padding_amount
		window.move(0, 0)
		window.addstr("bar_total:" + str(bar_total) + ", winwidth:" + str(w))

		#if a continue arrow needs to be added
		cont_subs = False
		cont_logs = False
		remove_search = False

		#shorten everything down untile there is enough space
		#order:
		#search -> search_min -> remove log -> remove sub -> remove search ->
		#shorten log -> shorten sub
		while bar_total > w:
			#search box intial shorten from max to med
			while bar_total > w and \
				search_box_with > int(self.look['search_box_med']):
				search_box_with -= 1
				bar_total -= 1

			#check if fits
			if not bar_total > w:
				break

			#remove logins
			if len(logins) > 1 and len(logins) >= len(subs) / 2:
				if len(logins) - 1 == curlogin:
					bar_total -= len(logins[len(logins) - 2]) + tab_padding_amount
					logins[curlogin - 1] = logins[curlogin]
					curlogin -= 1
				else:
					bar_total -= len(logins[len(logins) - 1]) + tab_padding_amount
				if not cont_logs:
					cont_logs = True
					bar_total += 3
				logins = logins[0: len(logins) - 1]

			#check if fits (again)
			if not bar_total > w:
				break

			#remove subs
			if len(subs) > 1 and len(subs) > len(logins):
				if len(subs) - 1 == cursub:
					bar_total -= len(subs[len(subs) - 2]) + tab_padding_amount
					subs[cursub - 1] = subs[cursub]
					cursub -= 1
				else:
					bar_total -= len(subs[len(subs) - 1]) + tab_padding_amount
				if not cont_subs:
					cont_subs = True
					bar_total += 3
				subs = subs[0: len(subs) - 1]
				cont_subs = True
			if not bar_total > w:
				break

			#change search box down to min width
			if search_box_with > int(self.look['search_box_min']):
				search_box_with -= 1
				bar_total -= 1

			if not bar_total > w:
				break

			#remove characters as a last resort
			if len(logins) <= 1 and len(subs) <= 1 and \
				search_box_with <= int(self.look['search_box_min']):
				#remove search box compleatly
				if not remove_search:
					remove_search = True
					bar_total -= int(self.look['search_box_min']) + 2

				if not bar_total > w:
					break

				if len(logins[0]) > 1 and len(logins[0]) >= len(subs[0]) / 2:
					logins[0] = logins[0][0:-1]
					bar_total -= 1

				if not bar_total > w:
					break

				if len(subs[0]) > 1 and len(subs[0]) > len(logins[0]):
					subs[0] = subs[0][0:-1]
					bar_total -= 1
				if len(logins[0]) <= 1 and len(subs[0]) <= 1:
					break

		#left align <--
		#draw subs (starting one space over)
		pos = 1
		for sub in range(len(subs)):
			pos = self.drawTab(window, pos, h - 2, (sub == cursub), subs[sub])
			pos += 1
		if cont_subs:
			pos = self.drawTab(window, pos, h - 2,
				False, self.look['special_character_cont'])
			pos += 1

		pos = self.drawTab(window, pos, h - 2, False, "+",
			roundl = (self.look['left_new_tab_rounding'] == "true"),
			roundr = (self.look['right_new_tab_rounding'] == "true"))

		#--> right align
		#draw search box
		if not remove_search:
			self.drawTab(window, w - 2 - search_box_with, h - 2, False, "Search...",
				search_box_with)
			pos = w - 4 - search_box_with
		else:
			pos = w - 2

		#draw logins
		pos -= 2
		self.drawTab(window, pos, h - 2, False, "+",
			roundl = (self.look['left_new_tab_rounding'] == "true"),
			roundr = (self.look['right_new_tab_rounding'] == "true"))
		if cont_logs:
			pos -= 3
			self.drawTab(window, pos, h - 2,
				False, self.look['special_character_cont'])
		for login in range(len(logins)):
			revlog = len(logins) - login - 1
			pos = pos - len(logins[revlog]) - 2
			self.drawTab(window, pos, h - 2, (revlog == curlogin), logins[revlog])

		window.refresh()

	def drawTab(self, window, x, y, selected, string, w = False,
		roundr = False, roundl = False):
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
			window.addch(draw_string[3])

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
			window.addch(draw_string[4])

		return pos

	def stop(self):
		exit()
