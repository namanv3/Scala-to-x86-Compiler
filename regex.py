from reserved import reserved
from tokens import tokens

# for t in tokens:
# 	print(f"t_{t} = ")

t_ADD_ASGN = r'\+='
t_SUB_ASGN = r'-='
t_MULT_ASGN = r'\*='
t_DIV_ASGN = r'/='
t_MOD_ASGN = r'%='
t_AND_ASGN = r'&='
t_OR_ASGN = r'\|='
t_XOR_ASGN = r'\^='
t_LSHIFT_ASGN = r'<<='
t_RSHIFT_ASGN = r'>>='

t_OP_RRSHIFT = r'>>>'
t_OP_RSHIFT = r'>>'
t_OP_LSHIFT = r'<<'

t_LO_AND = r'&&'
t_LO_OR = r'\|\|'

t_LEFTARROW = r'<-'
t_RIGHTARROW = r'=>'

t_UPTBOUND = r'<:'
t_VIEWBOUND = r'<%'
t_LOTBOUND = r'>:'

t_GEQ = r'>='
t_LEQ = r'<='
t_GT = r'>'
t_LT = r'<'
t_EQ = r'=='
t_NEQ = r'!='

t_EQ_ASGN = r'='

t_LPARAN = r'\('
t_RPARAN = r'\)'
t_LSQRB = r'\['
t_RSQRB = r'\]'
t_LCURLYB = r'\{'
t_RCURLYB = r'\}'

t_OP_ADD = r'\+'
t_OP_SUB = r'-'
t_OP_MULT = r'\*'
t_OP_DIVIDE = r'/'
t_OP_MOD = r'%'
t_OP_NOT = r'!'

t_OP_AND = r'&'
t_OP_OR = r'\|'
t_OP_XOR = r'\^'

t_COLON = r':'
t_DOT = r'\.'
t_COMMA = r'\,'
t_HASH = r'\#'
t_AT_SIGN = r'\@'
t_UNDERSCORE = r'_'
t_SEMI_COLON = r';'
# t_NEWLINE = r'\n'

def t_BOOL_LITERAL(t):
	r'true|false'
	if t.value == 'true':
		t.value = True
	else:
		t.value = False
	return t


def t_FLOAT_LITERAL(t):
	r'(([0-9]+(\.[0-9]+)|\.[0-9]+)([Ee][+-]?[0-9]+)?)|([0-9]+[Ee][+-]?[0-9]+)([FfDd])?'
	if (t.value[-1]=='F' or t.value[-1]=='f' or t.value[-1]=='D' or t.value[-1]=='d'):
		t.value = t.value[:-1]
	t.value = float(t.value)
	return t

def t_INT_LITERAL(t):
	r'((0[xX][0-9a-fA-F]+)|0|([1-9][0-9]*))([lL]?)'
	if len(t.value) > 1 and (t.value[1] == 'x' or t.value[1] == 'X'):
		return t
	if t.value[-1] == 'L' or t.value[-1] == 'l':
		t.value=t.value[:-1]
	t.value = int(t.value)
	return t

def t_CHAR_LITERAL(t):
	r'\'([^\\\'\r\n\\[^\r\n]|\\u[0-9A-Fa-f][0-9A-Fa-f][0-9A-Fa-f][0-9A-Fa-f])(\'|\\)'
	return t

def t_STRING_LITERAL(t):
	r'(raw|s|f)?\"(\\.|[^\\"]| )*\"'
	if t.value[0] == 'r':
		t.value = (t.value[4:-1],'raw')
	elif t.value[0] == 's':
		t.value = (t.value[2:-1],'interpolated')
	elif t.value[0] == 'f':
		t.value = (t.value[2:-1],'formatted')
	else:
		t.value = (t.value[1:-1],'normal')
	return t

def t_IDENTIFIER(t):
	r'([A-Za-z][0-9_A-Za-z]*)|(_[A-Za-z][0-9_A-Za-z]+)'
	t.type = reserved.get(t.value,'IDENTIFIER')    # Check for reserved words
	return t

t_ignore = ' \t'

def t_COMMENT(t):
	r'//.*'
	pass

# Define a rule so we can track line numbers
def t_NEWLINE(t):
	r'\n+'
	t.lexer.lineno += len(t.value)
	pass

# error handling
def t_error(t):
	print ("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)
	pass
