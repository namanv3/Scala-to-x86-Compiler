import ply.lex as lex
from regex import *
from sys import argv

handle = open(argv[1])
content = handle.read()
print(content)

lex.lex()

lex.input(content)

while True:
	tok = lex.token()
	if not tok: break
	print (tok)
	# tok_store[tok.value] = tok.type