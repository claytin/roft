#!/usr/bin/env python

import curses
from curses import wrapper

import threading
import praw

class interface(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		wrapper(self.init)

	def init(self, stdscr):
		stdscr.clear()
		stdscr.refresh()

		curses.curs_set(False)

		#create color pairs
		curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLACK)

		#first load message
		firstLoad = True
		if firstLoad:
			pass

		#header bar stuff
		self.headerBar = curses.newwin(5, stdscr.getmaxyx()[1], 0, 0)
		self.drawHeader(self.headerBar)

		while True:
			key = stdscr.getch()
			stdscr.move(0, 0)
			stdscr.addstr("key " + str(key))

			if key == ord("q"):
				break

	def drawHeader(self, window):
		#window w/h
		w = window.getmaxyx()[1]
		h = window.getmaxyx()[0]

		#tmp data
		subs = ["sub1", "sub2", "sub3", "sub4"]
		cursub = 0

		logins = ["log1", "log2", "log3"]
		curlogin = 0

		window.clear()
		#window.box(0, 0)

		#draw bottom line
		bottomBar = ""
		for pos in range(0, w):
			bottomBar = bottomBar + "━"
		window.move(h - 2, 0)
		window.addstr(bottomBar)

		#left align --
		#draw subs
		pos = 1
		for sub in range(len(subs)):
			pos = self.drawTab(window, pos, h - 2, (sub == cursub), subs[sub])
			pos += 1
		self.drawTab(window, pos, h - 2, False, "+", roundr = True)

		#-- right align
		#draw search box
		self.drawTab(window, w - 22, h - 2, False, "Search...", 20)

		#draw logins
		pos = w - 22 - 2
		pos -= 2
		self.drawTab(window, pos, h - 2, False, "+", roundr = True)
		for login in range(len(logins)):
			revlog = len(logins) - login - 1
			pos = pos - len(logins[revlog]) - 2
			self.drawTab(window, pos, h - 2, (revlog == curlogin), logins[revlog])

		window.refresh()
	def drawTab(self, window, x, y, selected, string, w = False,
		roundr = False, roundl = False):
		pos = x
		if w == False:
			w = len(string)

		if selected:
			#left side
			window.move(y, pos)
			window.addch("┛")
			window.move(y - 1, pos)
			window.addch("┃")
			window.move(y - 2, pos)
			window.addch("┏")

			#middle
			window.move(y - 1, pos + 1)
			window.addstr(string)
			for part in range(w):
				window.move(y - 2, pos + part + 1)
				window.addch("━")
				window.move(y, pos + part + 1)
				window.addch(" ")

			pos += w + 1

			#right side
			window.move(y, pos)
			window.addch("┗")
			window.move(y - 1, pos)
			window.addch("┃")
			window.move(y - 2, pos)
			window.addch("┓")
		else:
			#left side
			window.move(y, pos)
			window.addch("┷")
			window.move(y - 1, pos)
			window.addch("│")
			window.move(y - 2, pos)
			if roundl:
				window.addch("╭")
			else:
				window.addch("┌")

			#middle
			window.move(y - 1, pos + 1)
			window.addstr(string)
			for part in range(w):
				window.move(y - 2, pos + part + 1)
				window.addch("─")

			pos += w + 1

			#right side
			window.move(y, pos)
			window.addch("┷")
			window.move(y - 1, pos)
			window.addch("│")
			window.move(y - 2, pos)
			if roundr:
				window.addch("╮")
			else:
				window.addch("┐")

		return pos
#testing praw
#user_agent = ("test stuff... i'm just learning...")
#reddit = praw.Reddit(user_agent=user_agent)

#submissions = reddit.get_subreddit('linux').get_hot(limit=25)

#for sub in submissions:
#	print(sub)

ui = interface()
ui.start()
