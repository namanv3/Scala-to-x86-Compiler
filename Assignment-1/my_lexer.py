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
        tok_store[tok.value] = tok.type
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

delimiters1 = ['+', '-', '*', '/', '%', '&', '|', '^', '=', '!']
delimiters2 = ['<', '>']
delimiters3 = [')', '(', '[', ']', '{', '}', ':', ',', ';']
delimiter4 = ['.']
delimiters = delimiters1 + delimiters2 + delimiters3
normie_chars = list(string.uppercase) + list(string.lowercase) + list(string.digits)
normie_chars.append('_')

line_counter =0
tok_counter = 0
with open(outputfile, "w") as htm_file:
		htm_file.write("<html> \n")
		htm_file.write("<title>\n")
		htm_file.write("Lexed_file")
		htm_file.write("</title>\n")
		htm_file.write("<body>\n")
		for i in in_lines:
			for j in range(0, len(i)):
				if i[j] != ' ':
					break
				htm_file.write("&nbsp;\n")
			while tok_list[tok_counter] != '\n':
				htm_file.write("<font color = %s>" % colors[tok_store[tok_list[tok_counter]]])
					htm_file.write("%s" % tok_list[tok_counter])
					htm_file.write("</font">
					htm_file.write("\n")
					htm_file.write("&nbsp;")
					tok_counter += 1
			htm_file.write("</br>")
		htm_file.write("</body>\n")
		htm_file.write("</html>\n")
