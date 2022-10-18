import sys

import getopt

import os
dir_path = sys.argv[1:]
optlist, args = getopt.getopt(sys.argv[1:],'r:', ['dir_path='])

if optlist:
	for o, a in optlist:
		if o == "-r":
			files = []
			for (a, dir_names, file_names) in os.walk(a):
				files.extend(file_names)
			print("Files - ",files)
else:
	print(os.listdir(dir_path[0]))
