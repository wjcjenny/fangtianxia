# -*- coding: utf-8 -*-

import sys

f = open(sys.argv[1])
# f = open("sun.json")
# i = open('sun_new.json', 'w')
# line = f.readlines()
line = f.readline()
while line:

	strip_line = line.replace('\n', ' ')
	# end = strip_line.find('\n')
	# print end
	# print strip_line
	id_str = strip_line.find('"_id"')
	if id_str >= 0:
		bracket = strip_line.find('"}', id_str+40)
		if bracket > 0:
			strip_line = strip_line
		else:
			next_line = f.readline()
			while next_line:
				strip_next_line = next_line.replace('\n', '')
				strip_line = strip_line + strip_next_line
				bracket_1 = next_line.find('"}')
				if bracket_1 > 0:
					break
				next_line = f.readline()
	print strip_line
	# i.write(strip_line + '\n')
	line = f.readline()

