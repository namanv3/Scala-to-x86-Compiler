from reserved_words import reserved

comp = ['GT', 'LT', 'GEQ', 'LEQ', 'EQ', 'NEQ']

brackets = ['LPARAN', 'RPARAN', 'LSQRB', 'RSQRB', 'LCURLYB', 'RCURLYB'] ## 'BLOCKBEGIN' AND 'BLOCKEND' 

operations = [
	'OP_ADD', 'OP_SUB', 'OP_MULT', 'OP_DIVIDE', 'OP_MOD', 				# + - * / %
	'OP_NOT', 'OP_AND', 'OP_OR', 'OP_XOR', 								# ~ & | ^
	'OP_LSHIFT', 'OP_RSHIFT', 'OP_RRSHIFT']								# << >> >>>

logical_operations = ['LO_AND', 'LO_OR', 'LO_NOT']						# && || !

assignment_symbols = [
	'EQ_ASGN', 'ADD_ASGN', 'SUB_ASGN', 'MULT_ASGN', 'DIV_ASGN', 'MOD_ASGN',
	'AND_ASGN', 'OR_ASGN', 'XOR_ASGN', 'LSHIFT_ASGN', 'RSHIFT_ASGN']

# above five arrays from https://www.tutorialspoint.com/scala/scala_operators.htm


# These are left:
#'BOOL', 'LEFTARROW', 'XOR', 'COLON', 'SEMICOLON', 'DOT', 'COMMA', 'ID', 'CHAR', 'STRING', 'INT', 'FLOAT'