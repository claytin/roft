#!/usr/bin/env python

import curses
from curses import wrapper

import threading
import praw
import configparser
from os.path import expanduser
import os.path

import interface
import control

#key map with a few things predifined
keymap = { "exit" : "q", "kill" : "Q"}

#read config and stuff
config_file = "./config"	#the temp test file

if os.path.isfile(config_file):
	config = configparser.ConfigParser()

	try:
		config.read(config_file)
	except configparser.ParsingError:
		print("config parse error, invalid config file syntax")
		exit()

	keys = config['keys']

	for key in keys:
		try:
			keymap[key] = ord(keys[key])
		except TypeError:
			print("config parse error, invalid keymap format")
			exit()
else:
	print("no config file")
	exit()

ctrl = control.control(keymap)

ui = interface.interface(ctrl)
ui.start()
