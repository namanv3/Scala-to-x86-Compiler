#!/usr/bin/python

import lex as lex
import string
from tokens import *
from reserved_words import *
import regex
import sys, getopt

inputfile = ''
outputfile = ''

def GetArgs(argv):
	global inputfile, outputfile
	try:
      		opts, args = getopt.getopt(argv,"i:o:",["cfg=","out="])
   	except getopt.GetoptError:
      		print 'Error'
      		sys.exit(2)
   	for opt, arg in opts:
      		if opt in ("-i", "--cfg"):
         		inputfile = arg
      		elif opt in ("-o", "--out"):
         		outputfile = arg

GetArgs(sys.argv[1:])
lexer=lex.lex()

file = open(inputfile,"r")
inp = file.read()
file.close()

file1 = open(inputfile,"r")
in_lines = file1.readlines()
file1.close()

#to store all values of token as keys to their type
tok_store = {}
tok_list = []
lex.input(inp)
while True:
        tok = lexer.token()
        if not tok: break
        print tok
        tok_store[tok.value] = tok
        tok_list.append(tok.value)
f = open('Config_file1.txt', "r")
# use readlines to read all lines in the file
# The variable "lines" is a list containing all lines in the file
colors = {}
lines = f.readlines()

# make dictionary of all colours of tokens with token.type as key
for i in lines:
	for j in range(0,len(i)):
		if i[j] == ":":
			break
	colors[i[0:j]] = i[(j+1):len(i)-1]
print colors

tok_counter = 0
no_tok = len(tok_list)
max_row = tok_store[tok_list[no_tok - 1]][2]
curr_row = 0 
curr_col = 0
max_col = tok_store[tok_list[no_tok - 1]][3] + len(tok_store[tok_list[no_tok - 1]][1])
with open("Coloured.html", "w") as htm_file:
		htm_file.write("<html> \n")
		htm_file.write("<title>\n")
		htm_file.write("Lexed_file")
		htm_file.write("</title>\n")
		htm_file.write("<body>\n")
		while curr_col != max_col:
			if tok_store[tok_list[no_tok - 1]][3] == curr_col:
				htm_file.write("<font color = %s>" % colors[tok_store[tok_list[tok_counter]][0]])
				htm_file.write("%s" % tok_list[tok_counter])
				htm_file.write("</font">
				htm_file.write("\n")
				curr_col += len(tok_store[tok_list[no_tok - 1]][1])
			else:
				htm_file.write(" &nbsp; ")
				curr_col += 1
		htm_file.write("</body>\n")
		htm_file.write("</html>\n")
