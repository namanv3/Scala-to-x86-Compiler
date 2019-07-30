#!/usr/bin/python

import ply.lex as lex
import string
from tokens import *
from reserved_words import *
from regex import *
import sys, getopt
import re

# inputfile = ''
# outputfile = ''
#
# def GetArgs(argv):
# 	global inputfile, outputfile
# 	try:
# 		opts, args = getopt.getopt(argv,"i:o:",["cfg=","out="])
# 	except getopt.GetoptError:
# 		print 'Error'
# 		sys.exit(2)
# 	for opt, arg in opts:
# 		if opt in ("-i", "--cfg"):
# 			cfgfile = arg
# 		elif opt in ("-o", "--out"):
# 			outputfile = arg
#
# inputfile = sys.argv[2]
#
# GetArgs(sys.argv[1:])

# input_str = sys.argv[1:]
#
# out_re = r'^--out.*'
# cfg_re = r'^--cfg.*'
#
# inputfile = ""
# cfg_file = ""
# outputfile = ""
#
# for arg in input_str:
# 	if re.match(out_re,arg):
# 		outputfile = arg[6:]
# 	elif re.match(cfg_re,arg):
# 		cfg_file = arg[6:]
# 	else:
# 		inputfile = arg

lexer = lex.lex()
# file = open('inp',"r")
# inp = file.read()
# file.close()

# #to store all values of token as keys to their type
# tok_list = []
# lex.input(inp)
# while True:
# 	tok = lexer.token()
# 	if not tok:
# 		break
# 	print tok
# 	tok_list.append(tok)

# # cfgfile = "./Config_file1.txt"
# f = open(cfg_file, "r")
# # use readlines to read all lines in the file
# # The variable "lines" is a list containing all lines in the file
# colors = {}
# lines = f.readlines()
#
# # make dictionary of all colours of tokens with token.type as key
# for i in lines:
# 	for j in range(0,len(i)):
# 		if i[j] == ":":
# 			break
# 	colors[i[0:j]] = i[(j+1):len(i)-1]
# # print colors
#
# inp1 = inp
# tok_counter = 0
# no_tok = len(tok_list)
# curr_col = 0
# curr_row = 1
# with open(outputfile, "w+") as htm_file:
# 	htm_file.write("<html> \n")
# 	htm_file.write("<title>\n")
# 	htm_file.write("Lexed_file")
# 	htm_file.write("</title>\n")
# 	htm_file.write("<body>\n")
# 	while tok_counter != no_tok:
# 		curr_token = tok_list[tok_counter]
#
# 		if curr_token.lineno == curr_row:
# 			start_col = curr_token.lexpos
# 			no_of_spaces = start_col - curr_col
# 			print curr_token.value, "noofspaces",no_of_spaces
# 			for i in range(no_of_spaces):
# 				htm_file.write(" &nbsp; ")	# print (start_col - curr_col) no of spaces
#
# 			htm_file.write("<font color = %s>" % colors[tok_list[tok_counter].type])
# 			if curr_token.type == "STRING":
# 				htm_file.write("\"%s\"" % curr_token.value)
# 			elif curr_token.type == "CHAR":
# 				htm_file.write("\'%s\'" % curr_token.value)
# 			else:
# 				htm_file.write("%s" % curr_token.value)
# 			htm_file.write("</font>")
# 			curr_col = start_col + len(str(curr_token.value))
# 		elif curr_token.lineno == (curr_row + 1):
# 			htm_file.write("<br>")	# add new line
# 			curr_row += 1
# 			start_col = curr_token.lexpos
# 			no_of_spaces = start_col - curr_col
# 			print no_of_spaces
# 			for i in range(no_of_spaces):
# 				htm_file.write(" &nbsp; ")	# print (start_col - curr_col) no of spaces
# 			# now print the token
# 			htm_file.write("<font color = %s>" % colors[tok_list[tok_counter].type])
# 			if curr_token.type == "STRING":
# 				htm_file.write("\"%s\"" % curr_token.value)
# 			elif curr_token.type == "CHAR":
# 				htm_file.write("\'%s\'" % curr_token.value)
# 			else:
# 				htm_file.write("%s" % curr_token.value)
# 			htm_file.write("</font>")
# 			curr_col = start_col + len(str(curr_token.value))
# 		else:
# 			htm_file.write("<br>")	# add new line
# 			curr_row += 1
# 			continue
#
# 		tok_counter += 1
# 		# print "tok_counter has been made", tok_counter
#
#
# 	htm_file.write("</body>\n")
# 	htm_file.write("</html>\n")
