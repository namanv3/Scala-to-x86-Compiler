import ply.lex as lex
from sys import argv
from reserved import reserved
from tokens import tokens
from regex import *


lexer = lex.lex()

handle = open(argv[1])
lex.input(handle.read())

curr_line = 1
while True:
	tok = lexer.token()
	if not tok:
		break
	else:
		if tok.lineno > curr_line:
			curr_line = tok.lineno
			print(f"-->{curr_line}")
		print(tok.type)