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

		#header bar stuff
		self.headerBar = curses.newwin(10, stdscr.getmaxyx()[1], 0, 0)
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
		subs = ["all", "linux", "unixporn", "programmerhumor"]
		cursub = 0

		logins = ["fucko"]
		curlogin = 0

		window.clear()
		window.box(0, 0)

		#draw bottom line
		bottomBar = ""
		for pos in range(0, w):
			bottomBar = bottomBar + "━"
		window.move(h - 2, 0)
		window.addstr(bottomBar)

		#left align
		#draw subs
		pos = 1
		for sub in range(len(subs)):
			pos = self.drawTab(window, pos, h - 2, (sub == cursub), subs[sub])
			pos += 1

		#right align
		#draw search box
		drawTab(window, 
		#draw logins

		window.refresh()
	def drawTab(self, window, x, y, selected, string):
		pos = x
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
			for part in range(len(string)):
				window.move(y - 2, pos + part + 1)
				window.addch("━")
				window.move(y, pos + part + 1)
				window.addch(" ")

			pos += len(string) + 1

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
			window.addch("┌")

			#middle
			window.move(y - 1, pos + 1)
			window.addstr(string)
			for part in range(len(string)):
				window.move(y - 2, pos + part + 1)
				window.addch("─")

			pos += len(string) + 1

			#right side
			window.move(y, pos)
			window.addch("┷")
			window.move(y - 1, pos)
			window.addch("│")
			window.move(y - 2, pos)
			window.addch("┐")
		return pos

ui = interface()
ui.start()
