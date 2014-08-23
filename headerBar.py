import urwid

class headerBar(urwid.WidgetWrap):
	def __init__(self, _look):
		self.look = _look
		self.curSub = 0
		self.sublist = []

	def draw(self):
		#window w/h
		w = self.window.getmaxyx()[1]
		#h = self.window.getmaxyx()[0]

		#tmp data
		subs = []
		for sub in self.sublist:
			subs = subs + [sub.name]
		cursub = self.curSub

		logins = ["curly", "booster", "sue", "balrog", "quote", "jack",
			"kazuma", "king"]
		curlogin = 1

		self.window.clear()

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
		self.window.move(2, 0)
		self.window.addstr(bottomBar)

		#hide tabs when space is limited
		#each "+" tab takes up three plus spaces between leftside, logs/subs,
		#and logs/seach, and search box padding
		number_of_spacers = 3 + 3 + 3 + 2
		if self.look['tab_spacing'] == "true":
			tab_padding_amount = 2
		else:
			tab_padding_amount = 1

		search_box_with = int(self.look['search_box_max'])

		bar_total = search_box_with + number_of_spacers
		for sub in subs:
			bar_total += len(sub) + tab_padding_amount
		for log in logins:
			bar_total += len(log) + tab_padding_amount

		#if a continue arrow needs to be added
		cont_subs = False
		cont_logs = False
		remove_search = False

		#shorten everything down untile there is enough space
		#order:
		#search -> search_min -> remove log -> remove sub -> remove search ->
		#shorten log -> shorten sub
		#THIS
		#IS
		#(ass)PISS
		#i should really optomize it
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
		curpos = 0
		for sub in range(len(subs)):
			if self.look['tab_spacing'] == "false" and sub == cursub:
				curpos = pos
			pos = self.drawTab(self.window, pos, 2, (sub == cursub), subs[sub],
				padding = not (self.look['tab_spacing'] == "false" and sub is not 0))
			if self.look['tab_spacing'] == "true":
				pos += 1
		if cont_subs:
			pos = self.drawTab(self.window, pos, 2,
				False, self.look['special_character_cont'],
				padding = (self.look['tab_spacing'] == "true"))
			if self.look['tab_spacing'] == "true":
				pos += 1
		if self.look['tab_spacing'] == "false" and cursub <= len(subs) - 1:
			self.drawTab(self.window, curpos, 2, True,
				subs[cursub], padding = False, paddingr = False,
				paddingl = (cursub == 0))

		pos = self.drawTab(self.window, pos, 2, False, "+",
			roundl = (self.look['left_new_tab_rounding'] == "true"),
			roundr = (self.look['right_new_tab_rounding'] == "true"),
			padding = (self.look['tab_spacing'] == "true"))

		#--> right align
		#draw search box
		if not remove_search:
			self.drawTab(self.window, w - 2 - search_box_with, 2, False,
			"Search...", search_box_with)
			pos = w - 4 - search_box_with
		else:
			pos = w - 2

		#draw logins
		pos -= 2
		self.drawTab(self.window, pos, 2, False, "+",
			roundl = (self.look['left_new_tab_rounding'] == "true"),
			roundr = (self.look['right_new_tab_rounding'] == "true"),
			padding = (self.look['tab_spacing'] == "true"))
		if cont_logs:
			if self.look['tab_spacing'] == "true":
				pos -= 1
			pos -= 2
			self.drawTab(self.window, pos, 2,
				False, self.look['special_character_cont'],
				padding = (self.look['tab_spacing'] == "true"))
		for login in range(len(logins)):
			revlog = len(logins) - login - 1
			if self.look['tab_spacing'] == "true":
				pos = pos - len(logins[revlog]) - 2
			else:
				pos = pos - len(logins[revlog]) - 1

			if revlog == curlogin:
				curpos = pos
			self.drawTab(self.window, pos, 2, (revlog == curlogin),
				logins[revlog],
				padding = not (self.look['tab_spacing'] == "false"
				and login is not len(logins) - 1))

		if self.look['tab_spacing'] == "false":
			self.drawTab(self.window, curpos, 2, True,
				logins[curlogin], padding = False, paddingr = False,
				paddingl = (cursub == 0))

		self.window.refresh()
