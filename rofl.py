#!/usr/bin/env python

import configparser
#from os.path import expanduser
import os.path

#import interface
import control

#key map with a few things predifined
keymap = {"exit": "q", "kill": "Q"}

#appearance and stuff
look = {}

#read config and stuff
config_file = "./config"  #the temp test file

if os.path.isfile(config_file):
	config = configparser.ConfigParser()

	try:
		config.read(config_file)
	except configparser.ParsingError:
		print("config parse error, invalid config file syntax")
		exit()

	keymap = config['keys']
	look = config['look']

else:
	print("no config file")
	exit()

ctrl = control.control(keymap, look)
