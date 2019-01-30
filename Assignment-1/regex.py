from tokens import tokens
from lex import TOKEN

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
t_SEMI_COLON = r';'

def t_FLOAT(t):
	r'[-+]?([0-9]+(\.[0-9]+)?|\.[0-9]+)([Ee][+-]?[0-9]+)?([FfDd])?'
	if (t.value[-1]=='F' or t.value[-1]=='f' or t.value[-1]=='D' or t.value[-1]=='d'):
        t.value = t.value[:-1]
    t.value = float(t.value)
    return t

# def t_FLOAT(t):
#     r'((\d+)?(\.)(\d+)([Ee][+-]?(\d+))?([FfDd])?) | ((\d)+([Ee][+-]?(\d+))?([FfDd]))|((\d)+([Ee][+-](\d+))([FfDd])?)'
#     if (t.value[-1]=='F' or t.value[-1]=='f' or t.value[-1]=='D' or t.value[-1]=='d'):
#         t.value = t.value[:-1]
#     t.value = float(t.value)
#     return t

def t_INT(t):
    r'((0[xX][0-9a-fA-F]+)|([+-]?[1-9][0-9]*))([lL]?)'
    if len(t.value) > 1 and (t.value[1] == 'x' or t.value[1] == 'X'):
        return t
    if t.value[-1] == 'L' or t.value[-1] == 'l':
        t.value=t.value[:-1]
    t.value = int(t.value)
    return t

# def t_INT(t):
#     r'(((((0x)|(0X))[0-9a-fA-F]+)|(\d+))([uU]|[lL]|[uU][lL]|[lL][uU])?)'
#     # r'(0|[1-9](\d+)|(((0x)|(0X))[0-9A-Fa-f]+))[lL]?'
#     #print t.value
#     if len(t.value) > 1 and (t.value[1]=='x' or t.value[1]=='X'):
#       #  print t 
#         return t
#     if t.value[-1]=='L' or t.value[-1]=='l':
#         t.value=t.value[:-1]
#     t.value = int(t.value)
#     return t

def t_CHAR(t):
    r'\'([^\\\'\r\n\\[^\r\n]|\\u[0-9A-Fa-f][0-9A-Fa-f][0-9A-Fa-f][0-9A-Fa-f])(\'|\\)'
    return t 

def t_STRING(t):
   # r'\"([^\"]|\"|\\|\n|\b)*\"'
    r'\"(\\.|[^\\"]| )*\"'
    t.value = t.value[1:-1]
    return t


digit            = r'([0-9])'
nondigit         = r'([_A-Za-z])'
identifier = r'(' + nondigit + r'(' + digit + r'|' + nondigit + r')*)'

@TOKEN(identifier)
def t_ID(t):
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    pass

t_ignore = ' \t'

#handling nested comments and single line comments
def t_MCOMMENT(t):
    r'(/\*(\n|.)*?\*/)'
    t.lexer.lineno += t.value.count('\n')

def t_SCOMMENT(t):
    r'(//.*?\n)'
    t.lexer.lineno += t.value.count('\n')

# error handling 
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)
    pass