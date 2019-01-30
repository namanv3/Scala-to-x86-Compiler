from reserved_words import reserved

comp = ['GEQ', 'LEQ', 'GT', 'LT', 'EQ', 'NEQ']

brackets = ['LPARAN', 'RPARAN', 'LSQRB', 'RSQRB', 'LCURLYB', 'RCURLYB']

operations = [
	'OP_ADD', 'OP_SUB', 'OP_MULT', 'OP_DIVIDE', 'OP_MOD',
	'OP_NOT', 'OP_AND', 'OP_OR', 'OP_XOR',
	'OP_LSHIFT', 'OP_RSHIFT', 'OP_RRSHIFT']

logical_operations = ['LO_AND', 'LO_OR', 'LO_NOT']

assignment_symbols = [
	'EQ_ASGN', 'ADD_ASGN', 'SUB_ASGN', 'MULT_ASGN', 'DIV_ASGN', 'MOD_ASGN',
	'AND_ASGN', 'OR_ASGN', 'XOR_ASGN', 'LSHIFT_ASGN', 'RSHIFT_ASGN']

'''
above five arrays from: 
https://www.tutorialspoint.com/scala/scala_operators.htm
'''

characters = ['COLON', 'DOT', 'COMMA']

end_of_lines = ['SEMI_COLON', 'NEWLINE_CHAR']

named_tokens = ['ID','BOOL', 'CHAR', 'STRING', 'INT', 'FLOAT']

miscellaneous = ['LEFTARROW']					# added

# tokens = list(reserved.values()) + comp + brackets + operations 
#	 + logical_operations + assignment_symbols + characters 
#	 + end_of_lines + named_tokens + miscellaneous

"""
Section 4.3 of https://www.dabeaz.com/ply/ply.html says that we need to have
the string tokens in decreasing order of length

Restarting now
"""

tokens = [
	'ADD_ASGN', 'SUB_ASGN', 'MULT_ASGN', 'DIV_ASGN', 'MOD_ASGN',
	'AND_ASGN', 'OR_ASGN', 'XOR_ASGN', 'LSHIFT_ASGN', 'RSHIFT_ASGN',

	'OP_RRSHIFT', 'OP_RSHIFT', 'OP_LSHIFT', 

	'LO_AND', 'LO_OR',

	'LEFTARROW',

	'GEQ', 'LEQ', 'GT', 'LT', 'EQ', 'NEQ',

	'EQ_ASGN',

	'LPARAN', 'RPARAN', 'LSQRB', 'RSQRB', 'LCURLYB', 'RCURLYB',

	'OP_ADD', 'OP_SUB', 'OP_MULT', 'OP_DIVIDE', 'OP_MOD',
	'OP_NOT', 'OP_AND', 'OP_OR', 'OP_XOR',

	'COLON', 'DOT', 'COMMA',

	'SEMI_COLON',

	'ID', 'CHAR', 'STRING', 'INT', 'FLOAT',

	'MCOMMENT', 'SCOMMENT'
] + list(reserved.values())