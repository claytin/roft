
class control():
	def __init__(self, _keymap):
		self.keymap = _keymap
		self.subs = []
	
	def event(self, key):
		if key == self.keymap["exit"] or key == self.keymap["kill"]:
			piss
