import ply.yacc as yacc
from myLexer import *
from sys import argv

precedence = (
				('left','OP_OR'),
				('left','OP_XOR'),
				('left','OP_AND'),          #changed order
				('left','LO_OR'),
				('left','LO_AND'),
				('left','EQ','NEQ'),
				('left','LEQ','LT','GT','GEQ'),       #?
				('left','OP_RSHIFT','OP_LSHIFT','OP_RRSHIFT'), #?
				('left','OP_ADD','OP_SUB'),
				('left','OP_MULT','OP_DIVIDE','OP_MOD')
)


def p_start(p):
	'''S : compilationUnit
	'''
	print("start")

def p_compilationUnit(p):
	'''compilationUnit 	: topStatSeq
	'''
	print("compilationUnit")

def p_topStatSeq(p):
	'''topStatSeq 	: topStat
					| topStatSeq sep topStat
					| topStatSeq topStat
	'''
	print("topStatSeq")

def p_topStat(p):
	'''topStat 	: tmplDef
	'''
	print("topStat")

def p_tmplDef(p):
	'''tmplDef 	: RESERVED_CLASS classDef
				| RESERVED_OBJECT objectDef
				| RESERVED_CASE RESERVED_CLASS classDef
				| RESERVED_CASE RESERVED_OBJECT objectDef
	'''
	print("tmplDef")

def p_classDef(p):
	'''classDef : IDENTIFIER classParamClauses
	'''
	print("classDef")

def p_classParamClauses(p):
	'''classParamClauses 	: classParamClause
							| classParamClauses classParamClause
	'''
	print("classParamClauses")

def p_classParamClause(p):
	'''classParamClause : LPARAN RPARAN
						| LPARAN classParams RPARAN
	'''
	print("classParamClause")

def p_classParams(p):
	'''classParams 	: classParam
					| classParams COMMA classParam
	'''
	print("classParams")

def p_classParam(p):
	'''classParam 	: IDENTIFIER
					| RESERVED_VAL IDENTIFIER
					| RESERVED_VAR IDENTIFIER
					| IDENTIFIER COLON paramType
					| RESERVED_VAL IDENTIFIER COLON paramType
					| RESERVED_VAR IDENTIFIER COLON paramType
					| IDENTIFIER EQ_ASGN expr
					| RESERVED_VAL IDENTIFIER EQ_ASGN expr
					| RESERVED_VAR IDENTIFIER EQ_ASGN expr
					| IDENTIFIER COLON paramType EQ_ASGN expr
					| RESERVED_VAL IDENTIFIER COLON paramType EQ_ASGN expr
					| RESERVED_VAR IDENTIFIER COLON paramType EQ_ASGN expr
	'''
	print("classParam")

def p_objectDef(p):
	'''objectDef 	: IDENTIFIER classTemplate
	'''
	print("objectDef")

def p_classTemplate(p):
	'''classTemplate 	: classParents
						| classParents templateBody
	'''
	print("classTemplate")

def p_classParents(p):
	'''classParents : type classParents1
					| epsilon
	'''
	print("classParents")

def p_classParents1(p):
	'''classParents1 	: LPARAN exprs RPARAN
						| LPARAN RPARAN
						| LPARAN exprs RPARAN classParents1
						| LPARAN RPARAN classParents1
	'''
	print("classParents1")

def p_templateBody(p):
	'''templateBody : LCURLYB templateStats RCURLYB
	'''
	print("templateBody")

def p_templateStats(p):
	'''templateStats 	: templateStat
						| templateStats templateStat
						| templateStats sep templateStat
	'''
	print("templateStats")

def p_templateStat(p):
	'''templateStat : def
					| dcl
					| expr
					| epsilon
	'''
	print("templateStat")

def p_expr(p):
	'''expr	: RESERVED_IF LPARAN expr RPARAN expr
			| RESERVED_IF LPARAN expr RPARAN expr RESERVED_ELSE expr
			| RESERVED_WHILE LPARAN expr RPARAN expr
			| RESERVED_DO expr RESERVED_WHILE LPARAN expr RPARAN
			| RESERVED_FOR LPARAN enumerators RPARAN expr
			| RESERVED_FOR LCURLYB enumerators RCURLYB expr
			| RESERVED_THROW expr
			| RESERVED_RETURN
			| RESERVED_RETURN expr
			| IDENTIFIER EQ_ASGN expr
			| simpleExpr DOT IDENTIFIER EQ_ASGN expr
			| simpleExpr1 argumentExprs EQ_ASGN expr
			| postfixExpr
			| postfixExpr RESERVED_MATCH LCURLYB caseClauses RCURLYB
	'''
	print("expr")


def p_enumerators(p):
	'''enumerators 	: generator
					| enumerators sep generator
	'''
	print("enumerators")

def p_generator(p):
	'''generator 	: pattern1 LEFTARROW expr
					| pattern1 LEFTARROW guards
	'''
	print("generator")

def p_guards(p):
	'''guards 	: sep pattern1 EQ_ASGN expr
				| guard
				| sep guard
				| sep pattern1 EQ_ASGN expr guards
				| guards guard
				| sep guards guard
	'''
	print("guards")

def p_pattern1(p):
	'''pattern1 : IDENTIFIER
	'''
	print("pattern1")

def p_guard(p):
	'''guard 	: RESERVED_IF postfixExpr
	'''
	print("guard")

def p_simpleExpr(p):
	'''simpleExpr 	: blockExpr
					| simpleExpr1
	'''
	print("simpleExpr")

def p_simpleExpr1(p):
	'''simpleExpr1 	: literal
					| path
					| UNDERSCORE
					| LPARAN RPARAN
					| LPARAN exprs RPARAN
					| simpleExpr DOT IDENTIFIER
					| simpleExpr1 argumentExprs
	'''
	print("simpleExpr1")

def p_blockExpr(p):
	'''blockExpr 	: LCURLYB caseClauses RCURLYB
					| LCURLYB block RCURLYB
	'''
	print("blockExpr")

def p_exprs(p):
	'''exprs 	: expr
				| exprs COMMA expr
	'''
	print("exprs")

def p_argumentExprs(p):
	'''argumentExprs 	: LPARAN RPARAN
						| LPARAN exprs RPARAN
	'''
	print("argumentExprs")

# PRAGYA
# def p_block(p):
# 	'''block 	: expr
# 				| block sep expr
# 				| block expr
# 	'''
# 	print("block")

def p_block(p):
	'''block 	: epsilon
				| expr
				| block sep expr
				| block expr
	'''
	print("block")


# PRAGYA
# def p_postfixExpr(p):
# 	'''postfixExpr 	: infixExpr
# 					| infixExpr IDENTIFIER
# 	'''
# 	print("postfixExpr")

def p_postfixExpr(p):
	'''postfixExpr 	: infixExpr
	'''
	print("postfixExpr")

def p_infixExpr(p):
	'''infixExpr 	: assign
					| orExpr
	'''
	print("infixExpr")

def p_assign(p):
	'''assign : simpleExpr1 EQ_ASGN orExpr
	'''
	print("assign")


def p_prefixExpr(p):
	'''prefixExpr 	: simpleExpr
					| OP_ADD simpleExpr
					| OP_SUB simpleExpr
					| OP_NOT simpleExpr
	'''
	print("prefixExpr")

def p_orExpr(p):
	'''orExpr 	: andExpr
				| orExpr OP_OR andExpr
	'''
	print("orExpr")


def p_andExpr(p):
	'''andExpr 	: bitOrExpr
				| andExpr OP_AND bitOrExpr
	'''
	print("andExpr")

def p_bitOrExpr(p):
	'''bitOrExpr	: xorExpr
					| bitOrExpr LO_OR xorExpr
	'''
	print("bitOrExpr")

def p_xorExpr(p):
	'''xorExpr	: bitAndExpr
				| xorExpr OP_XOR bitAndExpr
	'''
	print("xorExpr")


def p_bitAndExpr(p):
	'''bitAndExpr	: eqExpr
					| bitAndExpr LO_AND eqExpr
	'''
	print("bitAndExpr")

def p_eqExpr(p):
	'''eqExpr 	: compExpr
				| eqExpr EQ compExpr
				| eqExpr NEQ compExpr
	'''
	print("eqExpr")

def p_compExpr(p):
	'''compExpr : shiftExpr
				| compExpr LEQ shiftExpr
				| compExpr LT shiftExpr
				| compExpr GEQ shiftExpr
				| compExpr GT shiftExpr
	'''
	print("compExpr")

def p_shiftExpr(p):
	'''shiftExpr 	: addExpr
					| shiftExpr OP_RSHIFT addExpr
					| shiftExpr OP_LSHIFT addExpr
					| shiftExpr OP_RRSHIFT addExpr
	'''
	print("shiftExpr")

def p_addExpr(p):
	'''addExpr 	: multExpr
				| addExpr OP_ADD multExpr
				| addExpr OP_SUB multExpr
	'''
	print("addExpr")


def p_multExpr(p):
	'''multExpr	: unaryExpr
				| multExpr OP_MOD unaryExpr
				| multExpr OP_MULT unaryExpr
				| multExpr OP_DIVIDE unaryExpr
	'''
	print("multExpr")

def p_unaryExpr(p):
	'''unaryExpr 	: prefixExpr
					| LPARAN infixExpr RPARAN
	'''
	print("unaryExpr")

def p_caseClauses(p):
	'''caseClauses 	: caseClause
					| caseClauses caseClause
	'''
	print("caseClauses")

def p_caseClause(p):
	'''caseClause 	: RESERVED_CASE
	'''
	print("caseClause")


def p_def(p):
	'''def 	: RESERVED_VAL valVarDef
			| RESERVED_VAR valVarDef
			| RESERVED_DEF funDef
			| RESERVED_TYPE typeDef
	'''
	print("def")

def p_valVarDef(p):
	'''valVarDef 	: IDENTIFIER COLON type EQ_ASGN expr
					| IDENTIFIER EQ_ASGN expr
	'''
	print("valVarDef")

# PRAGYA
# def p_funDef(p):
# 	'''funDef 	: funSig expr
# 				| funSig EQ_ASGN expr
# 				| funDcl expr
# 				| funDcl EQ_ASGN expr
# 	'''
# 	print("funDef")

def p_funDef(p):
	'''funDef 	: funSig templateBody
				| funSig EQ_ASGN templateBody
				| funDcl templateBody
				| funDcl EQ_ASGN templateBody
	'''
	print("funDef")

def p_typeDef(p):
	'''typeDef : IDENTIFIER EQ_ASGN type
	'''
	print("typeDef")

def p_dcl(p):
	'''dcl 	: RESERVED_VAR valVarDcl
			| RESERVED_DEF funDcl
			| RESERVED_TYPE typeDcl
	'''
	print("dcl")

def p_valVarDcl(p):
	'''valVarDcl 	: ids COLON type
	'''
	print("valVarDcl")

def p_funDcl(p):
	'''funDcl 	: funSig COLON type
	'''
	print("funDcl")

def p_funSig(p):
	'''funSig 	: IDENTIFIER paramClause
	'''
	print("funSig")

def p_paramClause(p):
	'''paramClause 	: LPARAN params RPARAN
					| LPARAN RPARAN
	'''
	print("paramClause")

def p_params(p):
	'''params 	: param
				| params COMMA param
	'''
	print("params")

def p_param(p):
	'''param 	: IDENTIFIER COLON paramType
	'''
	print("param")

def p_paramType(p):
	'''paramType	: type
					| type OP_MULT
	'''
	print("paramType")

def p_typeDcl(p):
	'''typeDcl : ids
	'''
	print("typeDcl")

def p_type(p):
	'''type : basicTypes
			| arrayType
			| listType
			| IDENTIFIER
	'''
	print("type")

def p_listType(p):
	'''listType 	: TYPE_LIST LSQRB type RSQRB
					| TYPE_LIST LSQRB type RSQRB LPARAN INT_LITERAL RPARAN
	'''
	print("listType")

def p_arrayType(p):
	'''arrayType 	: TYPE_ARRAY LSQRB type RSQRB
					| TYPE_ARRAY LSQRB type RSQRB LPARAN INT_LITERAL RPARAN
	'''
	print("arrayType")

def p_basicTypes(p):
	'''basicTypes 	: TYPE_CHAR
					| TYPE_BOOL
					| TYPE_BYTE
					| TYPE_SHORT
					| TYPE_INT
					| TYPE_LONG
					| TYPE_FLOAT
					| TYPE_DOUBLE
					| TYPE_STRING
					| TYPE_UNIT
					| TYPE_ANY
					| TYPE_ANYVAL
	'''
	print("basicTypes")

def p_path(p):
	'''path : IDENTIFIER
			| RESERVED_THIS
			| path DOT IDENTIFIER
	'''
	print("path")

def p_literal(p):
	'''literal	: INT_LITERAL
				| FLOAT_LITERAL
				| BOOL_LITERAL
				| CHAR_LITERAL
				| STRING_LITERAL
	'''
	print("literal")

def p_ids(p):
	'''ids	: IDENTIFIER
			| IDENTIFIER COMMA ids
	'''
	print("ids")

def p_sep(p):
	'''sep : SEMI_COLON
	'''
	print("sep")

def p_epsilon(p):
	'''epsilon :
	'''
	print("epsilon")


def p_error(p):
	CRED = '\033[91m'
	CEND = '\033[0m'
	print(CRED + "Syntax error at line number '%s'" % p.lineno + CEND)
	print(CRED + "Syntax error at token '%s'" % p.value + CEND)

parser = yacc.yacc(debug=True)

inputfile = argv[1]
with open(inputfile, 'r') as f:
	inputData = f.read()

print(inputData)

parser.parse(inputData)
