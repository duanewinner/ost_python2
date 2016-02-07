#!/usr/local/bin/python3

import glob
import os

def extcount():
	extlist = []
	for file in glob.glob("*"):
		if os.path.isfile(file):
			if os.path.splitext(file)[1] == '':
				extlist.append("No extension")
			else:
				extlist.append(os.path.splitext(file)[1])
	for i in extlist:
		print(i)
		
