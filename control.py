import urwid
import interface

import headerBar
import infoBar
import sub

class control():
	def __init__(self, _keymap, _look):
		self.min_width = 10
		self.min_height = 10

		self.keymap = _keymap
		self.look = _look
		self.subs = []

		#create all the widgets
		info = infoBar.infoBar(self.look)
		header = headerBar.headerBar(self.look)

		#different content views
		cursub = sub.sub(self.look, "test_sub")
		#comments = urwid.Text('comments')
		#link = urwid.Text('view of link')
		#sidebar = urwid.Text('sidebar')
		#settings = urwid.Text('settings')

		#use sub for now
		content = urwid.Columns([cursub])

		#create a pile with status bar, headerbar, and content
		pile = urwid.Pile([info, header, content])

		self.ui = interface.interface(pile, valign = 'top')

	def start(self):
		#filler = urwid.Filler('test', 'top')
		self.loop = urwid.MainLoop(self.ui, unhandled_input = self.event)
		self.loop.run()

	def event(self, key):
		if key in ('q', 'Q'):
			raise urwid.ExitMainLoop()

		#global min_width
		#global min_height

		#if key == self.keymap["exit"] or key == "^[":
			#pass
		#elif key == self.keymap["kill"]:
			#self.ui.stop()
		#elif key == self.keymap['move_up'] or key == 'KEY_UP':
			#self.ui.curSub.moveUp()
		#elif key == self.keymap['move_down'] or key == 'KEY_DOWN':
			#self.ui.curSub.moveDown()

		#elif key == "KEY_RESIZE":
			#if self.ui.stdscr.getmaxyx()[1] < self.min_width or \
				#self.ui.stdscr.getmaxyx()[0] < self.min_height:
				#self.ui.stdscr.clear()
				#self.ui.stdscr.move(int(self.ui.stdscr.getmaxyx()[0] / 2),
					#int(self.ui.stdscr.getmaxyx()[1] / 2) - 4)
				#self.ui.stdscr.addstr("too small")
				#return

			#self.ui.resize()
