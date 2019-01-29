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