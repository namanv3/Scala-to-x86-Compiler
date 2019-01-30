from tokens import *
from reserved_words import *

colour = {}
for d in data_types:
	colour[reserved[d]] = 'Tomato'
for k in keywords:
	colour[reserved[k]] = 'Violet'
for n in named_tokens:
	colour[n] = 'White'
for c in characters:
	colour[c] = 'Yellow'
for b in brackets:
	colour[b] = 'SlateBlue'
for m in comp:
	colour[m] = 'Pink'
for m in operations:
	colour[m] = 'Pink'
for m in logical_operations:
	colour[m] = 'Pink'
for m in assignment_symbols:
	colour[m] = 'Pink'
for m in end_of_lines:
	colour[m] = 'Pink'
for m in miscellaneous:
	colour[m] = 'Pink'

print colour

with open("Config_file1.txt", "w") as text_file:
	for i in colour.keys():
	    text_file.write("%s:%s\n" % (i,colour[i]))
