from reserved_words import reserved

comp = ['GT', 'LT', 'GEQ', 'LEQ', 'EQ', 'NEQ']

brackets = ['LPARAN', 'RPARAN', 'LSQRB', 'RSQRB', 'LCURLYB', 'RCURLYB']

operations = [
	'OP_ADD', 'OP_SUB', 'OP_MULT', 'OP_DIVIDE', 'OP_MOD',
	'OP_NOT', 'OP_AND', 'OP_OR', 'OP_XOR',
	'OP_LSHIFT', 'OP_RSHIFT', 'OP_RRSHIFT']

logical_operations = ['LO_AND', 'LO_OR', 'LO_NOT']

assignment_symbols = [
	'EQ_ASGN', 'ADD_ASGN', 'SUB_ASGN', 'MULT_ASGN', 'DIV_ASGN', 'MOD_ASGN',
	'AND_ASGN', 'OR_ASGN', 'XOR_ASGN', 'LSHIFT_ASGN', 'RSHIFT_ASGN']

# above five arrays from https://www.tutorialspoint.com/scala/scala_operators.htm

characters = ['COLON', 'DOT', 'COMMA']

end_of_lines = ['SEMI_COLON', 'NEWLINE_CHAR']

named_tokens = ['ID','BOOL', 'CHAR', 'STRING', 'INT', 'FLOAT']	# should we just use NUM?


# These are left:
#'LEFTARROW' and the keywords