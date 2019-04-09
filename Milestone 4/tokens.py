from reserved import reserved

tokens = [
	'ADD_ASGN', 'SUB_ASGN', 'MULT_ASGN', 'DIV_ASGN', 'MOD_ASGN',
	'AND_ASGN', 'OR_ASGN', 'XOR_ASGN', 'LSHIFT_ASGN', 'RSHIFT_ASGN',

	'OP_RRSHIFT', 'OP_RSHIFT', 'OP_LSHIFT',

	'LO_AND', 'LO_OR',

	'LEFTARROW', 'RIGHTARROW',

	'UPTBOUND', 'VIEWBOUND', 'LOTBOUND',

	'GEQ', 'LEQ', 'GT', 'LT', 'EQ', 'NEQ',

	'EQ_ASGN',

	'LPARAN', 'RPARAN', 'LSQRB', 'RSQRB', 'LCURLYB', 'RCURLYB',

	'OP_ADD', 'OP_SUB', 'OP_MULT', 'OP_DIVIDE', 'OP_MOD',
	'OP_NOT', 'OP_AND', 'OP_OR', 'OP_XOR',

	'COLON', 'DOT', 'COMMA', 'HASH', 'AT_SIGN', 'UNDERSCORE',

	'SEMI_COLON',

	'IDENTIFIER', 'BOOL_LITERAL', 'CHAR_LITERAL', 'INT_LITERAL', 'FLOAT_LITERAL',
	'STRING_LITERAL',
	# string_literal includes formar strings
	# no need to include ARRAY_LITERAL and LIST_LITERAL in here. They can be
	# handled during parsing

	'COMMENT'
] + list(reserved.values())