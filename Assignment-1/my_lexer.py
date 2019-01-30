
import lex as lex
from tokens import *
from reserved_words import *

lexer=lex.lex()

file = open(sys.argv[1],"r")
inp = file.read()
file.close()

file1 = open(sys.argv[1],"r")
in_lines = file1.readlines()
file1.close()

#to store all values of token as keys to their type
tok_store = {}
lex.input(inp)
while True:
        tok = lexer.token()
        if not tok: break
        print tok
        tok_store[tok.value] = tok.type

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

delimiters = []


with open("Coloured.html", "w") as htm_file:
		htm_file.write("<html> \n")
		htm_file.write("<title>\n")
		htm_file.write("Lexed_file")
		htm_file.write("</title>\n")
		htm_file.write("<body>\n")
		for i in in_lines:
			l1 = i.split()
			for i1 in l1:
				
			# (+text);
			# fl is final list with symbols added
			for f1 in fl:
				htm_file.write("<font color = %s>" % colors[tok_store[f1]])
				htm_file.write("%s" % f1)
				htm_file.write("</font">
				htm_file.write("\n")
				htm_file.write("&nbsp;")
			htm_file.write("</br>")
		htm_file.write("</body>\n")
		htm_file.write("</html>\n")
















