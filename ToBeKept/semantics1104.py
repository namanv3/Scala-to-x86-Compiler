import ply.yacc as yacc
from my_lexer import *
from sys import argv
from symbolTable import SymbolTable
S = SymbolTable()

input_str = sys.argv[1:]
inputfile = ""

#taken from https://www.scala-lang.org/files/archive/spec/2.11/06-expressions.html#infix-operations
precedence = (
				('left','OP_OR'),
				('left','OP_XOR'),
				('left','OP_AND'),          #changed order
				('left','LO_OR'),
				('left','LO_AND'),
				('left','EQ','NEQ'),
				('left','LEQ','LT','GT','GEQ'),
				('left','OP_RSHIFT','OP_LSHIFT','OP_RRSHIFT'),
				('left','OP_ADD','OP_SUB'),
				('left','OP_MULT','OP_DIVIDE','OP_MOD')
)

nextstat = 1

for arg in input_str:
	inputfile = arg

#Taken from https://www.scala-lang.org/files/archive/spec/2.11/13-syntax-summary.html

begin_curr = []
after_curr = []
else_curr = []
begin_max = -1
after_max = -1
else_max = -1

return_curr = []
return_max = -1

for_begin_curr = []
for_begin_max = -1
for_after_curr = []
for_after_max = -1

upd_curr = []
upd_max = -1

L_curr = []
L_max = -1

f = open(inputfile[:-6] + "IR.txt", 'w+')

def typecheck(p):
	t1 = p[1]['type'][1]
	t3 = p[3]['type'][1]
	global nextstat

	if t1 == "INT" and t3 == "INT":
		f.write(str(nextstat) + ": " + str(p[0]['place']) + ' = ' + str(p[1]['place']) + ' int ' + p[2] + ' ' + str(p[3]['place'])+"\n")
		nextstat += 1
		p[0]['type'] = ["SIMPLE_TYPE", "INT"]
	if t1 == "FLOAT" and t3 == "INT":
		u = S.newtemp()
		f.write(str(nextstat) + ": " + u + ' = ' + 'inttofloat ' + str(p[3]['place'])+"\n")
		nextstat += 1
		f.write(str(nextstat) + ": " + str(p[0]['place']) + ' = ' + str(p[1]['place']) + ' float' + p[2] + ' '+ u +"\n")
		nextstat += 1
		p[0]['type'] = ["SIMPLE_TYPE", "FLOAT"]
		S.addtemptoST(u, p[0]['type'][1], S.getWidth(p[0]['type'][1]))
	if t1 == "INT" and t3 == "FLOAT":
		u = S.newtemp()
		f.write(str(nextstat) + ": " + u + ' = ' + 'inttofloat ' + str(p[1]['place'])+"\n")
		nextstat += 1
		f.write(str(nextstat) + ": " + str(p[0]['place']) + ' = ' + u + ' float' + p[2] + ' '+ str(p[3]['place']) +"\n")
		nextstat += 1
		p[0]['type'] = ["SIMPLE_TYPE", "FLOAT"]
		S.addtemptoST(u, p[0]['type'][1], S.getWidth(p[0]['type'][1]))
	if t1 == "FLOAT" and t3 == "FLOAT":
		f.write(str(nextstat) + ": " + str(p[0]['place']) + ' = ' + str(p[1]['place']) + ' float' + p[2] + ' ' +str(p[3]['place'])+"\n")
		nextstat += 1
		p[0]['type'] = ["SIMPLE_TYPE", "FLOAT"]
	return p

def typecheck2(p):
	t1 = p[1]['type'][1]
	t3 = p[3]['type'][1]
	global nextstat

	if t1 == "FLOAT" and t3 == "INT":
		u = S.newtemp()
		f.write(str(nextstat) + ": " + u + ' = ' + 'inttofloat ' + str(p[3]['place'])+"\n")
		nextstat += 1
		S.addtemptoST(u, p[0]['type'][1], S.getWidth(p[0]['type'][1]))
		if p[2]['place'] == '=':
			f.write(str(nextstat) + ": " + p[1]['place'] + " := " + u +"\n")
			nextstat += 1
		else:
			f.write(str(nextstat) + ": " + p[1]['place'] + " := " + p[1]['place'] + p[2]['place'][0] + u +"\n")
			nextstat += 1
	else:
		sys.exit("Incompatible type used in assignment" + str(p.lineno))


def intfloatboolcheck(a):
	if a["type"][0] == "SIMPLE_TYPE" :
		if a["type"][1] != "INT" and a["type"][1] != "BOOLEAN" and a["type"][1] != "FLOAT" :
			sys.exit("Operation performed on non-arithmetic expression")
	else:
		sys.exit("Operation performed on non-arithmetic expression")

def printp(p):
	print(":",)
	for i in range(1,len(p)):
		print((p.slice)[i])
	print("")

def p_start(p):
	'''S : compilationUnit
	'''
	print("start")
	printp(p)

def p_compilationUnit(p):
	'''compilationUnit 	: topStatSeq
	'''
	print("compilationUnit")
	printp(p)

def p_topStatSeq(p):
	'''topStatSeq 	: topStat
					| topStat sep topStatSeq
					| topStat topStatSeq
	'''
	print("topStatSeq")
	printp(p)

def p_topStat(p):
	'''topStat 	: tmplDef
	'''
	print("topStat")
	printp(p)

def p_tmplDef(p):
	'''tmplDef 	: RESERVED_CLASS classDef
				| RESERVED_OBJECT objectDef
				| RESERVED_CASE RESERVED_CLASS classDef
				| RESERVED_CASE RESERVED_OBJECT objectDef
				| RESERVED_TRAIT traitDef
	'''
	print("tmplDef")
	printp(p)

def p_classDef(p):
	'''classDef : IDENTIFIER class_m classParamClauses classTemplateOpt
	'''
	S.endscope()
	print("classDef")
	printp(p)

def p_class_m(p):
	'''class_m : epsilon
	'''
	S.addClass(p[-1]['place'], S.curr_scope)

def p_classParamClauses(p):
	'''classParamClauses 	: classParamClause
							| classParamClause classParamClauses
	'''
	print("classParamClauses")
	printp(p)

def p_classParamClause(p):
	'''classParamClause : LPARAN RPARAN
						| LPARAN classParams RPARAN
	'''
	print("classParamClause")
	printp(p)

def p_classParams(p):
	'''classParams 	: classParam
					| classParam COMMA classParams
	'''
	print("classParams")
	printp(p)

def p_classParam(p):
	'''classParam 	: IDENTIFIER COLON paramType
					| RESERVED_VAL IDENTIFIER COLON paramType
					| RESERVED_VAR IDENTIFIER COLON paramType
					| IDENTIFIER EQ_ASGN expr
					| RESERVED_VAL IDENTIFIER EQ_ASGN expr
					| RESERVED_VAR IDENTIFIER EQ_ASGN expr
					| IDENTIFIER COLON paramType EQ_ASGN expr
					| RESERVED_VAL IDENTIFIER COLON paramType EQ_ASGN expr
					| RESERVED_VAR IDENTIFIER COLON paramType EQ_ASGN expr
	'''

					# | IDENTIFIER
					# | RESERVED_VAL IDENTIFIER
					# | RESERVED_VAR IDENTIFIER

	if len(p) == 4:
		if p[3]["type"][0] == "SIMPLE_TYPE":
			S.addParamVar(p[1], p[3]["type"][1], p.lineno, S.getWidth(p[3]["type"][1]))
		else:
			S.addParamVar(p[1], p[3]["type"][0], p.lineno, 4, p[3]["type"][1])
	elif len(p) == 5:
		if p[4]["type"][0] == "SIMPLE_TYPE":
			S.addParamVar(p[2], p[4]["type"][1], p.lineno, S.getWidth(p[4]["type"][1]))
		else:
			S.addParamVar(p[2], p[4]["type"][0], p.lineno, 4, p[4]["type"][1])
	elif len(p) == 6:
		if p[3]["type"][0] == "SIMPLE_TYPE":
			S.addParamVar(p[1], p[3]["type"][1], p.lineno, S.getWidth(p[3]["type"][1]))
		else:
			S.addParamVar(p[1], p[3]["type"][0], p.lineno, 4, p[3]["type"][1])
	elif len(p) == 7:
		if p[4]["type"][0] == "SIMPLE_TYPE":
			S.addParamVar(p[2], p[4]["type"][1], p.lineno, S.getWidth(p[4]["type"][1]))
		else:
			S.addParamVar(p[2], p[4]["type"][0], p.lineno, 4, p[4]["type"][1])

	print("classParam")
	printp(p)

def p_objectDef(p):
	'''objectDef 	: IDENTIFIER object_mark classTemplate
	'''
	S.endScope()
	print("objectDef")
	printp(p)

def p_object_mark(p):
	'''object_mark : epsilon
	'''
	# S.startScope()
	S.addObject(p[-1], S.curr_scope)

def p_classTemplateOpt(p):
	'''classTemplateOpt : RESERVED_EXTENDS classTemplate
						| templateBody
						| RESERVED_EXTENDS templateBody
						| epsilon
	'''
	print("classTemplateOpt")
	printp(p)

def p_classTemplate(p):
	'''classTemplate 	: classParents
						| classParents templateBody
	'''
	print("classTemplate")
	printp(p)

def p_classParents(p):
	'''classParents : epsilon
					| type
	'''
	print("classParents")
	printp(p)

def p_traitDef(p):
	'''traitDef : IDENTIFIER traitTemplateOpt
	'''
	print("traitDef")
	printp(p)

def p_traitTemplateOpt(p):
	'''traitTemplateOpt : RESERVED_EXTENDS traitTemplate
						| templateBody
						| RESERVED_EXTENDS templateBody
						| epsilon
	'''
	print("traitTemplateOpt")
	printp(p)

def p_traitTemplate(p):
	'''traitTemplate 	: type templateBody
						| type
	'''
	print("traitTemplate")
	printp(p)

def p_templateBody(p):
	'''templateBody : LCURLYB templateStats RCURLYB
	'''
	print("templateBody")
	printp(p)

def p_templateStats(p):
	'''templateStats 	: templateStat
						| templateStat templateStats
						| templateStat sep templateStats
	'''
	print("templateStats")
	printp(p)

def p_templateStat(p):
	'''templateStat : dcl
					| def
					| modifier dcl
					| modifier def
					| expr
					| epsilon
	'''
	print("templateStat")
	printp(p)

def p_modifier(p):
	'''modifier : RESERVED_OVERRIDE
				| accessModifier
	'''
	print("modifier")
	printp(p)

def p_accessModifier(p):
	'''accessModifier 	: RESERVED_PRIVATE
						| RESERVED_PROTECTED
						| RESERVED_PUBLIC
	'''

def p_assign(p):
	'''assign 	: path assignOp postfixExpr
	'''
	global nextstat

	if type(p[1]['place']) == type([]):
		path_place = p[1]['place'][0]
		for i in p[1]['place'][1:]:
			path_place = path_place + "." + i
	else:
		path_place = p[1]['place']

	if p[1]["type"] == p[3]["type"] :
		if p[2]['place'] == '=':
			f.write(str(nextstat) + ": " + str(path_place) + " := " + str(p[3]['place'])+"\n")
			nextstat += 1
		else:
			f.write(str(nextstat) + ": " + str(path_place) + " := " + str(path_place) + p[2]['place'][0] + str(p[3]['place'])+"\n")
			nextstat += 1
	else:
		if p[1]["type"][0] != "SIMPLE_TYPE" and p[3]["type"][0] != "SIMPLE_TYPE" and p[1]["type"][0] == p[3]["type"][0]:
			if p[2]['place'] == '=':
				f.write(str(nextstat) + ": " + path_place + " := " + p[3]['place']+"\n")
				nextstat += 1
			else:
				sys.exit("Incorrect assignment to array or list")
		elif p[1]["type"][0] == "SIMPLE_TYPE" and p[3]["type"][0] == "SIMPLE_TYPE":
			typecheck2(p)
		else:
			sys.exit("Incompatible type used in assignment" + str(p.lineno))
	print("assign")
	printp(p)

def p_assignOp(p):
	'''assignOp : EQ_ASGN
				| ADD_ASGN
				| SUB_ASGN
				| MULT_ASGN
				| DIV_ASGN
				| MOD_ASGN
				| AND_ASGN
				| OR_ASGN
				| XOR_ASGN
				| LSHIFT_ASGN
				| RSHIFT_ASGN
	'''
	p[0] = {
				'place' : p[1]
			}
	print("assignOp")
	printp(p)


def p_expr(p):
	'''expr	: RESERVED_IF LPARAN infixExpr RPARAN if_b_m expr if_s_m if_i1_m if_e_m
			| RESERVED_IF LPARAN infixExpr RPARAN if_b_m expr if_s_m RESERVED_ELSE if_i_m expr if_is_m if_e_m
			| RESERVED_WHILE LPARAN wh_i_m infixExpr RPARAN wh_b_m expr wh_s_m wh_e_m
			| RESERVED_DO do_b_m expr do_i_m RESERVED_WHILE LPARAN infixExpr RPARAN do_s_m
			| RESERVED_FOR for_s_m LPARAN initExpr sep for_b_m condExpr sep for_i_m updExpr RPARAN for_is_m expr for_e_m
			| RESERVED_THROW expr
			| RESERVED_RETURN
			| RESERVED_RETURN infixExpr
			| assign
			| simpleExpr DOT IDENTIFIER EQ_ASGN expr
			| simpleExpr1 argumentExprs EQ_ASGN expr
			| postfixExpr
			| postfixExpr RESERVED_MATCH match_b_m LCURLYB caseClauses RCURLYB match_e_m
	'''
	global nextstat
	if p.slice[1].type == "RESERVED_RETURN":
		if len(p) == 2:
			f.write(str(nextstat) + ": return" +"\n")
			nextstat += 1
		elif len(p) == 3:
			f.write(str(nextstat) + ": return " + str(p[2]['place']) +"\n")
			nextstat += 1
	elif len(p) == 2 and p.slice[1].type == "postfixExpr":
		p[0] = p[1]
	print("expr")
	printp(p)

def p_match_b_m(p):
	'''match_b_m : epsilon
	'''
	global nextstat
	global begin_max
	global begin_curr
	begin_max += 1
	begin_curr.append(begin_max)
	f.write(str(nextstat) + ": " + "goto " + "BEGIN" + str(begin_curr[-1]) +"\n")
	nextstat += 1
	S.startScope()
	global for_after_max
	for_after_max += 1
	for_after_curr.append(for_after_max)

def p_match_e_m(p):
	'''match_e_m : epsilon
	'''
	global nextstat
	global begin_curr
	global for_after_curr
	f.write(str(nextstat) + ": " + "BEGIN" + str(begin_curr[-1]) +"\n")
	begin_curr.pop(-1)
	nextstat += 1

	for i in p[-2]:
		if(i['place'][0] != "_"):
			f.write(str(nextstat) + ": " + "if " + str(p[-6]['place']) + " = " + str(i['place'][0]) + " goto " + str(i['place'][1]) + "\n")
			nextstat += 1
		else:
			f.write(str(nextstat) + ": " + "goto " + str(i['place'][1]) + "\n")
			nextstat += 1

	f.write(str(nextstat) + ": " +  "AFTER_F" + str(for_after_curr[-1]) + ":" + "\n")
	nextstat += 1
	for_after_curr.pop(-1)
	S.endScope()

def p_initExpr(p):
	'''initExpr : epsilon
				| subInitExpr
				| initExpr COMMA subInitExpr
				'''

def p_subInitExpr(p):
	'''subInitExpr : infixExpr
				   | RESERVED_VAL valVarDef
				   | RESERVED_VAR valVarDef
				   | RESERVED_VAR valVarDcl
	'''

def p_condExpr(p):
	'''condExpr : epsilon
				| infixExpr
				| infixExpr COMMA condExpr
	'''
	global nextstat
	if p.slice[1].type != "epsilon":
		global for_after_curr
		f.write(str(nextstat) + ": " + "if " + p[-2]['place'] + " = 0 goto " + "AFTER_F" + str(for_after_curr[-1]) +"\n")
		nextstat += 1

	# AFTER_F is exit label, i.e. label taking you outside for loop

def p_updExpr(p):
	'''updExpr : epsilon
				| infixExpr
				| updExpr COMMA infixExpr
	'''

def p_for_s_m(p):
	'''for_s_m : epsilon
	'''
	S.startScope()

def p_for_b_m(p):
	'''for_b_m : epsilon
	'''
	global nextstat
	global for_begin_curr
	global for_begin_max
	for_begin_max += 1
	for_begin_curr.append(for_begin_max)
	f.write(str(nextstat) + ": " + "BEGIN_F" + str(for_begin_curr[-1]) + ":"+"\n")
	nextstat += 1

	global for_after_curr
	global for_after_max
	for_after_max += 1
	for_after_curr.append(for_after_max)

def p_for_i_m(p):
	'''for_i_m : epsilon
	'''
	global nextstat
	global after_curr
	global after_max
	after_max += 1
	after_curr.append(after_max)
	f.write(str(nextstat) + ": " + "goto " + "AFTER" + str(after_curr[-1]) +"\n")
	# This AFTER label takes you to the beginning of for-loop body
	nextstat += 1

	global upd_curr
	global upd_max
	upd_max += 1
	upd_curr.append(upd_max)
	f.write(str(nextstat) + ": " + "UPD" + str(upd_curr[-1]) +"\n")
	nextstat += 1

def p_for_is_m(p):
	'''for_is_m : epsilon
	'''
	global for_begin_curr
	f.write(str(nextstat) + ": " + "goto " + "BEGIN_F" + str(for_begin_curr[-1]) +"\n")
	for_begin_curr.pop(-1)
	nextstat += 1

	global after_curr
	f.write(str(nextstat) + ": " + "AFTER:" + str(after_curr[-1]) +"\n")
	# This AFTER label indicates the beginning of for-loop body
	after_curr.pop(-1)
	nextstat += 1

def p_for_e_m(p):
	'''for_e_m : epsilon
	'''
	global nextstat
	global upd_curr
	f.write(str(nextstat) + ": " + "goto " + "UPD" + str(upd_curr[-1]) +"\n")
	upd_curr.pop(-1)
	nextstat += 1

	global for_after_curr
	f.write(str(nextstat) + ": " + "AFTER_F:" + str(for_after_curr[-1]) +"\n")
	for_after_curr.pop(-1)
	nextstat += 1
	S.endScope()


def p_wh_i_m(p):
	'''wh_i_m : epsilon
	'''
	global nextstat
	global begin_curr
	global begin_max
	begin_max += 1
	begin_curr.append(begin_max)
	f.write(str(nextstat) + ": " + "BEGIN" + str(begin_curr[-1]) + ":"+"\n")
	nextstat += 1

def p_wh_b_m(p):
	'''wh_b_m : epsilon
	'''
	global nextstat
	global after_curr
	global after_max
	after_max += 1
	after_curr.append(after_max)
	f.write(str(nextstat) + ": " + "if " + str(p[-2]['place']) + " = 0 goto " + "AFTER" + str(after_curr[-1]) + "\n")
	nextstat += 1
	S.startScope()

def p_wh_s_m(p):
	'''wh_s_m : epsilon
	'''
	global nextstat
	global begin_curr
	f.write(str(nextstat) + ": " + "goto BEGIN" + str(begin_curr[-1]) +"\n")
	begin_curr.pop(-1)
	nextstat += 1
	S.endScope()

def p_wh_e_m(p):
	'''wh_e_m : epsilon
	'''
	global nextstat
	global after_curr
	f.write(str(nextstat) + ": " + "AFTER" + str(after_curr[-1]) +":\n")
	after_curr.pop(-1)
	nextstat += 1

def p_if_b_m(p):
	'''if_b_m : epsilon
	'''
	global nextstat
	global else_max
	global else_curr
	else_max += 1
	else_curr.append(else_max)
	f.write(str(nextstat) + ": " + "if " + p[-2]['place'] + " = 0 goto " + " ELSE" + str(else_curr[-1]) +"\n")
	nextstat += 1
	S.startScope()

def p_if_s_m(p):
	'''if_s_m : epsilon
	'''
	global nextstat
	global after_max
	global after_curr
	after_max += 1
	after_curr.append(after_max)
	f.write(str(nextstat) + ": " + "goto AFTER" + str(after_curr[-1]) +"\n")
	nextstat += 1
	S.endScope()

def p_if_i_m(p):
	'''if_i_m : epsilon
	'''
	global nextstat
	global else_curr
	S.startScope()
	f.write(str(nextstat) + ": " + 'ELSE' + str(else_curr[-1]) +":\n")
	else_curr.pop(-1)
	nextstat += 1

def p_if_i1_m(p):
	'''if_i1_m : epsilon
	'''
	global nextstat
	global else_curr
	f.write(str(nextstat) + ": " + 'ELSE' + str(else_curr[-1]) +":\n")
	else_curr.pop(-1)
	nextstat += 1

def p_if_is_m(p):
	'''if_is_m : epsilon
	'''
	S.endScope()

def p_if_e_m(p):
	'''if_e_m : epsilon
	'''
	global nextstat
	global after_curr
	f.write(str(nextstat) + ": " + "AFTER" + str(after_curr[-1]) +":\n")
	after_curr.pop(-1)
	nextstat += 1

def p_do_b_m(p):
	'''do_b_m : epsilon
	'''
	global nextstat
	global begin_curr
	global begin_max
	begin_max += 1
	begin_curr.append(begin_max)
	f.write(str(nextstat) + ": " + "BEGIN" + str(begin_curr[-1]) + ":"+"\n")
	S.startScope()

def p_do_i_m(p):
	'''do_i_m : epsilon
	'''
	S.endScope()

def p_do_s_m(p):
	'''do_s_m : epsilon
	'''
	global nextstat
	global begin_curr
	global after_curr
	global after_max

	after_max += 1
	after_curr.append(after_max)
	f.write(str(nextstat) + ": " + "if " + p[-2]['place'] + " = 0 goto " + "AFTER" + str(after_curr[-1]) +"\n")
	nextstat += 1


	f.write(str(nextstat) + ": " + "goto BEGIN" + str(begin_curr[-1]) +"\n")
	nextstat += 1
	begin_curr.pop(-1)

	f.write(str(nextstat) + ": " + "AFTER" + str(after_curr[-1]) +":\n")
	after_curr.pop(-1)
	nextstat += 1

# def p_enumerators(p):
# 	'''enumerators 	: generator
# 	'''
# 	print("enumerators")
# 	printp(p)
#
# def p_generator(p):
# 	'''generator 	: pattern1 LEFTARROW expr
# 					| pattern1 LEFTARROW expr guards
# 	'''
# 	print("generator")
# 	printp(p)
#
# def p_guards(p):
# 	'''guards 	: sep pattern1 EQ_ASGN expr
# 				| guard
# 				| sep guard
# 				| sep pattern1 EQ_ASGN expr guards
# 				| guard guards
# 				| sep guard guards
# 	'''
# 	print("guards")
# 	printp(p)
#
# def p_pattern1(p):
# 	'''pattern1 : IDENTIFIER
# 	'''
# 	p[0] = {
# 		'place' : p[1],
# 		'type' : S.getType(p[1], "variables")
# 	}
# 	print("pattern1")
# 	printp(p)

def p_guard(p):
	'''guard 	: RESERVED_IF postfixExpr
	'''
	print("guard")
	printp(p)

def p_simpleExpr(p):
	'''simpleExpr 	: RESERVED_NEW classTemplate
					| RESERVED_NEW templateBody
					| blockExpr
					| simpleExpr1
	'''
	if len(p) == 2:
		if p.slice[1].type == "simpleExpr1":
			p[0] = p[1]

			# PASS for blockExpr

	# PASS for len(p) = 3

	print("simpleExpr")
	printp(p)

def p_simpleExpr1(p):
	'''simpleExpr1 	: literal
					| path
					| UNDERSCORE
					| LPARAN epsilon RPARAN
					| LPARAN exprs RPARAN
					| simpleExpr DOT IDENTIFIER
					| simpleExpr1 argumentExprs
	'''
	global nextstat
	global return_curr
	global return_max
	if p[1] == "_":
		p[0] = {
			"place" : "_",
			"type" : ["", ""]
		}
	elif len(p) == 2:
		p[0] = p[1]
	elif len(p) == 3:
		# for array(1D);
		if S.getScope("variables", p[1]['place']) != "none":
			u = S.newtemp()
			Arraytype = S.getType(p[1]['place'], "variables")
			elemSize = S.getWidth(Arraytype[1][1])

			# Error checking for index while accessing array element
			if p[2][0]['type'] != ["SIMPLE_TYPE", "INT"]:
				sys.exit('Array index not an integer')

			# scope = S.getScope("variables", p[1]['place'])
			# if (p[2][0]['place'] > S.SymbolTable[scope]["variables"][p[1]['place']]['Arraysize']):
			# 	sys.exit('Array index greater than size accessed')


			f.write(str(nextstat) + ": " + u + " := " + str(elemSize) +" * " + str(p[2][0]["place"]) +"\n")
			nextstat += 1
			u2 = S.newtemp()
			f.write(str(nextstat)+ ": " + u2 + " := " + str(p[1]["place"]) + " + " + u +"\n")
			p[0] = {
				'place' : u2,
				'type' : S.getType(p[1]['place'], "variables")
			}
			nextstat += 1
		else:
			# else, it's a function call
			for i in p[2]:
				if i['type'][0] == "SIMPLE_TYPE":
					f.write(str(nextstat) + ": param " + str(i['place']) +"\n")
					nextstat += 1
				else:
					f.write(str(nextstat) + ": refparam " + str(i['place']) +"\n")
					nextstat += 1
			# 3AC of result = function return statement
			if type(p[1]['place']) == type([]):
				place = p[1]['place'][-1]
			else:
				place = p[1]['place']
			if (S.SymbolTable[place]["rType"][0] != 'VOID'):
				return_max += 1
				return_curr.append(return_max)
				f.write(str(nextstat) + ": " + "refparam $result" + str(return_curr[-1]) + "\n")
				nextstat += 1
				p[0] = {
					'place' : '$result' + str(return_curr[-1]),
					'type' : S.SymbolTable[place]["rType"]
				}
				return_curr.pop(-1)
			f.write(str(nextstat) + ": " + "call " + str(p[1]['place']) + ", " + str(len(p[2])) + "\n")
			nextstat += 1
	else:
		if p.slice[1].type == "LPARAN":
			p[0] = p[2]

		# PASS for simpleExpr DOT IDENTIFIER
	print("simpleExpr1")
	printp(p)

def p_blockExpr(p):
	'''blockExpr 	: LCURLYB caseClauses RCURLYB
					| LCURLYB block RCURLYB
	'''
	print("blockExpr")
	printp(p)

def p_exprs(p):
	'''exprs 	: expr
				| expr COMMA exprs
	'''
	if len(p) == 2:
		p[0] = [p[1]]
	else:
		p[0] = [p[1]] + p[3]
	print("exprs")
	printp(p)

def p_argumentExprs(p):
	'''argumentExprs 	: LPARAN RPARAN
						| LPARAN exprs RPARAN
	'''
	if len(p) == 2:
		p[0] = []
	else:
		p[0] = p[2]
	print("argumentExprs")
	printp(p)

def p_block(p):
	'''block 	: epsilon
				| expr
				| def
				| dcl
				| expr sep block
				| expr block
				| def sep block
				| def block
				| dcl sep block
				| dcl block
	'''
	print("block")
	printp(p)

def p_postfixExpr(p):
	'''postfixExpr 	: infixExpr
	'''
	p[0] = p[1]
	print("postfixExpr")
	printp(p)

def p_infixExpr(p):
	'''infixExpr 	: assign
					| orExpr
	'''
	if p.slice[1].type == 'assign':
		p[0] = {}
		p[0]['place'] = S.newtemp()
		p[0]['type'] = ["", ""]
	else:
		p[0] = p[1]
	print("infixExpr")
	printp(p)

def p_prefixExpr(p):
	'''prefixExpr 	: simpleExpr
					| OP_ADD simpleExpr
					| OP_SUB simpleExpr
					| OP_NOT simpleExpr
	'''
	global nextstat
	if len(p) == 2:
		p[0] = p[1]
	else:
		u = S.newtemp()
		if p[2]['type'][0] == "SIMPLE_TYPE":
			if p.slice[1].type == "OP_ADD" or p.slice[1].type == "OP_SUB":
				if p[2]['type'][1] != "INT" and p[2]['type'][1] != "FLOAT":
					sys.exit("Incompatible data type error in prefix_expression" + " in line " + str(p.lineno))
			else:
				if p[2]['type'][1] != "BOOLEAN":
					sys.exit("Incompatible data type error in prefix_expression" + " in line " + str(p.lineno))
		else:
			 sys.exit("Incompatible data type error in prefix_expression" + " in line " + str(p.lineno))


		p[0] = {
				'place' : u,
				'type' : p[2]['type']
				}
		f.write(str(nextstat) + ": " + str(p[0]['place']) + " := " + str(p[1]) + str(p[2]['place'])+"\n")
		nextstat += 1

	print("prefixExpr")
	printp(p)

def p_orExpr(p):
	'''orExpr 	: andExpr
				| orExpr OP_OR andExpr
	'''
	global nextstat
	if len(p)==2:
			p[0] = p[1]
	else:
		intfloatboolcheck(p[1])
		intfloatboolcheck(p[3])

		if p[1]['type'][1] == "INT" and p[3]['type'][1] == "INT":
			p[0]['place'] = S.newtemp()
			p[0]['type'] = ["SIMPLE_TYPE", "INT"]
			S.addtemptoST(p[0]['place'], p[0]['type'][1], S.getWidth(p[0]['type'][1]))
			f.write(str(nextstat) + ": " + p[0]['place'] + ':=' + p[1]['place'] + '|' + p[2]['place']+"\n")
			nextstat += 1
		else:
			sys.exit("Incompatible data type error in and_expression" + " in line " + str(p.lineno))
	# print("orExpr")
	# printp(p)

def p_andExpr(p):
	'''andExpr 	: bitOrExpr
				| andExpr OP_AND bitOrExpr
	'''
	global nextstat
	if len(p)==2:
			p[0] = p[1]
	else:
		intfloatboolcheck(p[1])
		intfloatboolcheck(p[3])

		if p[1]['type'][1] == "INT" and p[3]['type'][1] == "INT":
			p[0]['place'] = S.newtemp()
			p[0]['type'] = ["SIMPLE_TYPE", "INT"]
			S.addtemptoST(p[0]['place'], p[0]['type'][1], S.getWidth(p[0]['type'][1]))
			f.write(str(nextstat) + ": " + p[0]['place'] + ':=' + p[1]['place'] + '&' + p[2]['place']+"\n")
			nextstat += 1
		else:
			sys.exit("Incompatible data type error in and_expression" + " in line " + str(p.lineno))
	# print("andExpr")
	# printp(p)

def p_bitOrExpr(p):
	'''bitOrExpr	: xorExpr
					| bitOrExpr LO_OR xorExpr
	'''
	global nextstat
	if len(p)==2:
		p[0] = p[1]
	else:
		intfloatboolcheck(p[1])
		intfloatboolcheck(p[3])
		if p[1]['type'][1] == "BOOLEAN" and p[3]['type'][1] == "BOOLEAN":
			p[0] = {}
			p[0]['place'] = S.newtemp()
			p[0]['type'] = ["SIMPLE_TYPE", "BOOLEAN"]
			S.addtemptoST(p[0]['place'], p[0]['type'][1], S.getWidth(p[0]['type'][1]))
			f.write(str(nextstat) + ": " + str(p[0]['place']) + ':=' + str(p[1]['place']) + ' or ' + str(p[3]['place'])+"\n")
			nextstat += 1
		else:
			sys.exit("Incompatible data type error in bit_or_expression" + " in line " + str(p.lineno))
	# print("bitOrExpr")
	# printp(p)

def p_xorExpr(p):
	'''xorExpr	: bitAndExpr
				| xorExpr OP_XOR bitAndExpr
	'''
	global nextstat
	if len(p)==2:
			p[0] = p[1]
	else:
		intfloatboolcheck(p[1])
		intfloatboolcheck(p[3])

		if p[1]['type'][1] == "INT" and p[3]['type'][1] == "INT":
			p[0]['place'] = S.newtemp()
			p[0]['type'] = ["SIMPLE_TYPE", "INT"]
			S.addtemptoST(p[0]['place'], p[0]['type'][1], S.getWidth(p[0]['type'][1]))
			f.write(str(nextstat) + ": " + p[0]['place'] + ':=' + p[1]['place'] + '^' + p[2]['place']+"\n")
			nextstat += 1
		else:
			sys.exit("Incompatible data type error in xor_expression" + " in line " + str(p.lineno))
	# print("xorExpr")
	# printp(p)

def p_bitAndExpr(p):
	'''bitAndExpr	: eqExpr
					| bitAndExpr LO_AND eqExpr
	'''
	global nextstat
	if len(p)==2:
		p[0] = p[1]
	else:
		intfloatboolcheck(p[1])
		intfloatboolcheck(p[3])
		if p[1]['type'][1] == "BOOLEAN" and p[3]['type'][1] == "BOOLEAN":
			p[0] = {}
			p[0]['place'] = S.newtemp()
			p[0]['type'] = ["SIMPLE_TYPE", "BOOLEAN"]
			S.addtemptoST(p[0]['place'], p[0]['type'][1], S.getWidth(p[0]['type'][1]))
			f.write(str(nextstat) + ": " + str(p[0]['place']) + ':=' + str(p[1]['place']) + ' and ' + str(p[3]['place'])+"\n")
			nextstat += 1
		else:
			sys.exit("Incompatible data type error in bit_and_expression" + " in line " + str(p.lineno))
	# print("bitAndExpr")
	# printp(p)

def p_eqExpr(p):
	'''eqExpr 	: compExpr
				| eqExpr EQ compExpr
				| eqExpr NEQ compExpr
	'''
	global nextstat
	if len(p)==2:
		p[0] = p[1]
	else:
		intfloatboolcheck(p[1])
		intfloatboolcheck(p[3])

		t1 = p[1]['type'][1]
		t3 = p[3]['type'][1]
		if t1 == t3:
			p[0] = {}
			p[0]['place'] = S.newtemp()
			p[0]['type'] = ["SIMPLE_TYPE", "BOOLEAN"]
			S.addtemptoST(p[0]['place'], p[0]['type'][1], S.getWidth(p[0]['type'][1]))
			f.write(str(nextstat) + ": " + 'if ' + str(p[1]['place']) + str(p[2]) + str(p[3]['place']) + ' goto ' + str(nextstat+3)+"\n")
			nextstat += 1
			f.write(str(nextstat) + ": " + str(p[0]['place']) + " = 0"+"\n")
			nextstat += 1
			f.write(str(nextstat) + ": " + "goto " + str(nextstat+2)+"\n")
			nextstat += 1
			f.write(str(nextstat) + ": " + str(p[0]['place']) + " = 1"+"\n")
			nextstat += 1
		else:
			sys.exit("Comparison operation performed on incompatible data types in eq_expression" + " in line " + str(p.lineno))
	# print("eqExpr")
	# printp(p)

def p_compExpr(p):
	'''compExpr : shiftExpr
				| compExpr LEQ shiftExpr
				| compExpr LT shiftExpr
				| compExpr GEQ shiftExpr
				| compExpr GT shiftExpr
	'''
	global nextstat
	#global variable nextstat
	if len(p)==2:
		p[0] = p[1]
	else:
		intfloatboolcheck(p[1])
		intfloatboolcheck(p[3])

		t1 = p[1]['type'][1]
		t3 = p[3]['type'][1]
		if (t1 == "INT" or t1 == "FLOAT") and (t3 == "INT" or t3 == "FLOAT"):
			p[0] = {}
			p[0]['place'] = S.newtemp()
			p[0]['type'] = ["SIMPLE_TYPE", "BOOLEAN"]
			S.addtemptoST(p[0]['place'], p[0]['type'][1], S.getWidth(p[0]['type'][1]))
			nextstat += 1
			f.write(str(nextstat) + ": " + 'if ' + str(p[1]['place']) + ' ' + str(p[2]) + ' ' + str(p[3]['place']) + ' goto ' + str(nextstat+3)+"\n")
			nextstat += 1
			f.write(str(nextstat) + ": " + p[0]['place'] + " = 0"+"\n")
			nextstat += 1
			f.write(str(nextstat) + ": " + "goto " + str(nextstat+2)+"\n")
			nextstat += 1
			f.write(str(nextstat) + ": " + str(p[0]['place']) + " = 1"+"\n")
			nextstat += 1
		else:
			sys.exit("Comparison operation performed on incompatible data types in comp_expression" + " in line " + str(p.lineno))
	# print("compExpr")
	# printp(p)

def p_shiftExpr(p):
	'''shiftExpr 	: addExpr
					| shiftExpr OP_RSHIFT addExpr
					| shiftExpr OP_LSHIFT addExpr
					| shiftExpr OP_RRSHIFT addExpr
	'''
	global nextstat
	if len(p)==2:
		p[0] = p[1]
	else:
		intfloatboolcheck(p[1])
		intfloatboolcheck(p[3])

		if p[1]['type'][1] == "INT" and p[3]['type'][1] == "INT":
			p[0] = {}
			p[0]['place'] = S.newtemp()
			f.write(str(nextstat) + ": " + str(p[0]['place']) + ' = ' + str(p[1]['place']) + str(p[2]) + str(p[3]['place']) +"\n")
			nextstat += 1
			p[0]['type'] = ["SIMPLE_TYPE", "INT"]
			S.addtemptoST(p[0]['place'], p[0]['type'][1], S.getWidth(p[0]['type'][1]))
		else:
			sys.exit("Shift operation on non-integers not allowed. Error in line " + str(p.lineno))
	# print("shiftExpr")
	# printp(p)

def p_addExpr(p):
	'''addExpr 	: multExpr
				| addExpr OP_ADD multExpr
				| addExpr OP_SUB multExpr
	'''
	global nextstat
	#type conversion for short, int,long and float
	if len(p)==2:
		p[0] = p[1]
	else:
		intfloatboolcheck(p[1])
		intfloatboolcheck(p[3])

		p[0] = {}
		p[0]['place'] = S.newtemp()
		p = typecheck(p)
		S.addtemptoST(p[0]['place'], p[0]['type'][1], S.getWidth(p[0]['type'][1]))
	# print("addExpr")
	# printp(p)

def p_multExpr(p):
	'''multExpr	: unaryExpr
				| multExpr OP_MOD unaryExpr
				| multExpr OP_MULT unaryExpr
				| multExpr OP_DIVIDE unaryExpr
	'''
	global nextstat
	if len(p) == 2:
		p[0] = p[1]
	else:
		intfloatboolcheck(p[1])
		intfloatboolcheck(p[3])

		p[0] = {}
		p[0]["place"] = S.newtemp()
		if p[2] == "%":
			if p[1]["type"][1] == "INT" and p[3]["type"][1] == "INT":
				p[0]["type"] = ["SIMPLE_TYPE", "INT"]
				f.write(str(nextstat) + ": " + str(p[0]["place"]) + ' = ' + str(p[1]["place"]) + ' % ' + str(p[3]["place"]) +"\n")
				nextstat += 1
				S.addtemptoST(p[0]['place'], p[0]['type'][1], S.getWidth(p[0]['type'][1]))
			else:
				sys.exit("Modulous operation attempted on non-integer values")
		else:
			p = typecheck(p)
			S.addtemptoST(p[0]['place'], p[0]['type'][1], S.getWidth(p[0]['type'][1]))
	# print("multExpr")
	# printp(p)

def p_unaryExpr(p):
	'''unaryExpr 	: prefixExpr
					| LPARAN infixExpr RPARAN
	'''
	if len(p) == 2:
		p[0] = p[1]
	elif len(p) == 4:
		p[0] = p[2]

	# print("unaryExpr")
	# printp(p)

def p_caseClauses(p):
	'''caseClauses 	: caseClause
					| caseClause caseClauses
	'''
	if len(p) == 2:
		p[0] = [p[1]]
	else:
		p[0] = [p[1]] + p[2]
	print("caseClauses")
	printp(p)

def p_caseClause(p):
	'''caseClause 	: RESERVED_CASE pattern RIGHTARROW caseClause_b_m block
	'''
	# | RESERVED_CASE pattern guard RIGHTARROW block
	p[0] = {
		'place' : (p[2]['place'], p[4]['place'])
	}
	global nextstat
	global for_after_curr
	f.write(str(nextstat) + ": goto AFTER_F" + str(for_after_curr[-1]) +"\n")
	nextstat += 1
	print("caseClause")
	printp(p)

def p_caseClause_b_m(p):
	'''caseClause_b_m : epsilon
	'''
	global nextstat
	global L_curr
	global L_max
	L_max += 1
	L_curr.append(L_max)
	f.write(str(nextstat) + ": " + "L" + str(L_curr[-1]) + ":" +"\n")
	nextstat += 1
	p[0] = {
		'place' : "L" + str(L_curr[-1])
	}

def p_pattern(p):
	'''pattern 	: literal
				| IDENTIFIER
				| UNDERSCORE
	'''
	if p.slice[1].type == "literal":
		p[0] = {
		'place' : p[1]['place']
		}
	else:
		p[0] = {
		'place' : p[1]
		}
	print("pattern")
	printp(p)

def p_def(p):
	'''def 	: RESERVED_VAL valVarDef
			| RESERVED_VAR valVarDef
			| RESERVED_DEF funDef
			| RESERVED_TYPE typeDef
	'''
	print("def")
	printp(p)

def p_valVarDef(p):
	'''valVarDef 	: IDENTIFIER COLON type EQ_ASGN expr
					| IDENTIFIER EQ_ASGN expr
	'''
	global nextstat
	if len(p) == 6:
		if p[3]['type'] != p[5]['type']:
			sys.exit("Incompatible type assignment to variable")
		f.write(str(nextstat) + ": " + str(p[1]) + " := " + str(p[5]['place'])+"\n")
	else:
		f.write(str(nextstat) + ": " + str(p[1]) + " := " + str(p[3]['place'])+"\n")
	nextstat += 1

	if p[3]["type"][0] == "SIMPLE_TYPE":
		S.addVar(p[1], p[3]["type"], p.lineno, S.getWidth(p[3]["type"][1]))
	else:
		if 'Arraysize' in p[3].keys():
			S.addVar(p[1], p[3]["type"], p.lineno, 4, p[3]["type"][1], None, p[3]['Arraysize'])
		else:
			S.addVar(p[1], p[3]["type"], p.lineno, 4, p[3]["type"][1], None)
	print("valVarDef")
	printp(p)

def p_funDef(p):
	'''funDef 	: funSig fun_mark1 templateBody
				| funSig fun_mark1 EQ_ASGN templateBody
				| funSig COLON type fun_mark templateBody
				| funSig COLON type fun_mark EQ_ASGN templateBody
	'''
	global nextstat
	f.write(str(nextstat) + ": " + 'END FUNCTION'+"\n")
	nextstat += 1
	S.endScope()
	print("funDef")
	printp(p)

def p_fun_mark(p):
	'''fun_mark : epsilon
	'''
	S.SymbolTable[S.curr_scope]["rType"] = p[-1]['type']

def p_fun_mark1(p):
	'''fun_mark1 : epsilon
	'''
	S.SymbolTable[S.curr_scope]["rType"] = ['VOID', 'VOID']

def p_typeDef(p):
	'''typeDef : IDENTIFIER EQ_ASGN type
	'''
	print("typeDef")
	printp(p)

def p_dcl(p):
	'''dcl 	: RESERVED_VAR valVarDcl
			| RESERVED_DEF funDcl
			| RESERVED_TYPE typeDcl
	'''
	print("dcl")
	printp(p)

def p_valVarDcl(p):
	'''valVarDcl 	: ids COLON type
	'''
	for id in p[1]["place"]:
		if p[3]["type"][0] == "SIMPLE_TYPE":
			S.addVar(id, p[3]["type"], p.lineno, S.getWidth(p[3]["type"][1]))
		else:
			S.addVar(id, p[3]["type"], p.lineno, 4, p[3]["type"][1])
	print("valVarDcl")
	printp(p)

def p_funDcl(p):
	'''funDcl 	: funSig1 COLON type
	'''
	S.SymbolTable[S.curr_scope]["rType"] = p[3]['type']
	S.endScope()
	print("funDcl")
	printp(p)

def p_funSig(p):
	'''funSig 	: IDENTIFIER fmark paramClause
	'''
	p[0] = {
		'place' : p[1]
	}
	print("funSig")
	printp(p)

def p_funSig1(p):
	'''funSig1 	: IDENTIFIER fmark1 paramClause
	'''
	p[0] = {
		'place' : p[1]
	}
	print("funSig1")
	printp(p)

def p_fmark(p):
		'''fmark : epsilon
		'''
		global nextstat
		f.write(str(nextstat) + ": " + "BEGIN FUNCTION " + str(S.curr_scope) + "." + str(p[-1]) + ":"+ "\n")
		S.addFunc(p[-1], p.lineno, returnType = None, def_c = 1)
		nextstat += 1

def p_fmark1(p):
	'''fmark1 : epsilon
	'''
	S.addFunc(p[-1], p.lineno, returnType = None, def_c = 0)

def p_paramClause(p):
	'''paramClause 	: LPARAN params RPARAN
					| LPARAN RPARAN
	'''
	print("paramClause")
	printp(p)

def p_params(p):
	'''params 	: param
				| param COMMA params
	'''
	print("params")
	printp(p)

def p_param(p):
	'''param 	: IDENTIFIER COLON paramType
				| IDENTIFIER COLON paramType EQ_ASGN literal
	'''
	if (S.SymbolTable[S.curr_scope]["fdef"] == 1):
		if p[3]["type"][0] == "SIMPLE_TYPE":
			S.addVar(p[1], p[3]["type"], p.lineno, S.getWidth(p[3]["type"][1]))
		else:
			S.addVar(p[1], p[3]["type"], p.lineno, 4, p[3]["type"][1])

	# emit missing
	print("param")
	printp(p)

def p_paramType(p):
	'''paramType	: type
	'''
					# | type OP_MULT
	p[0] = p[1]
	print("paramType")
	printp(p)

def p_typeDcl(p):
	'''typeDcl : ids
	'''
	p[0] = p[1]
	print("typeDcl")
	printp(p)

def p_type(p):
	'''type : basicTypes
			| arrayType
			| listType
			| IDENTIFIER
	'''
	if p.slice[1].type == "IDENTIFIER":
		p[0] = {
			"place" : ["OBJECT", p[1]],
			"type" : ["OBJECT", p[1]]
		}
	else:
		p[0] = p[1]
	print("type")
	printp(p)

def p_listType(p):
	'''listType 	: TYPE_LIST LSQRB type RSQRB
					| TYPE_LIST LSQRB type RSQRB LPARAN INT_LITERAL RPARAN
	'''
	if len(p) == 5:
		p[0] = {
			"place" : ["LIST", p[3]["type"]],
			"type" : ["LIST", p[3]["type"]]
		}
	else:
		p[0] = {
			"place" : ["LIST", p[3]["type"]],
			"type" : ["LIST", p[3]["type"]],
			"arrayDim" : p[6]
		}
	print("listType")
	printp(p)

def p_arrayType(p):
	'''arrayType 	: TYPE_ARRAY LSQRB type RSQRB
					| TYPE_ARRAY LSQRB type RSQRB LPARAN INT_LITERAL RPARAN
	'''
	if len(p) == 5:
		p[0] = {
			"place" : ["ARRAY", p[3]["type"]],
			"type" : ["ARRAY", p[3]["type"]]
		}
	else:
		p[0] = {
			"place" : ["ARRAY", p[3]["type"]],
			"type" : ["ARRAY", p[3]["type"]],
			"arrayDim" : p[6]
		}
	print("arrayType")
	printp(p)

def p_basicTypes(p):
	'''basicTypes 	: TYPE_CHAR
					| TYPE_BOOLEAN
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
	p[0] = {
			"place" : ["SIMPLE_TYPE", p[1].upper()],
			"type" : ["SIMPLE_TYPE", p[1].upper()]
	}
	print("basicTypes")
	printp(p)

def p_path(p):
	'''path : path DOT IDENTIFIER
			| RESERVED_THIS
			| IDENTIFIER
	'''
	global nextstat
	if(len(p) == 2):
		if p[1] == "this":
			p[0] = {
				"place" : [p[1]],
				"type" : ["", ""]
			}
		else:
			type = S.getType(p[1], "variables")
			if type == "":
				type = S.getType(p[1], "functions")
			if type == "":
				sys.exit('Identifier \'' + str(p[1]) + '\' not declared in scope')

			p[0] = {
				"place" : p[1],
				"type" : type
			}
	else:
		type = S.getType(p[1], "variables")
		if type == "":
			type = S.getType(p[1], "functions")
		if type == "":
			sys.exit('Identifier \'' + str(idVal) + '\' not declared in scope')

		if type(p[1]['place']) == type([]):
			place = p[1]['place'] + [p[3]]
		else:
			place = [p[1]['place']] + [p[3]]
		p[0] = {
			"place" : place,
			"type" : type
		}

	print("path")
	printp(p)

def p_literal(p):
	'''literal	: INT_LITERAL
				| FLOAT_LITERAL
				| BOOL_LITERAL
				| CHAR_LITERAL
				| STRING_LITERAL
				| TYPE_ARRAY argumentExprs
	'''
	if (len(p) == 2):
		p[0] = {
			"place"	: p[1],
			"type" : ["SIMPLE_TYPE", p.slice[1].type[:-8]],
			"literal" : "True"
		}
		if(p.slice[1].type == "BOOL_LITERAL"):
			p[0]['type'][1] = "BOOLEAN"
	else:
		p[0] = {
			"place" : "",
			"type" : [ "ARRAY", ""],
			"literal" : "True",
			"Arraysize" : len(p[2])
		}
		p[0]['place'] = "ARRAY{"
		p[0]['place'] += str(p[2][0]['place'])
		for i in p[2][1:]:
			p[0]['place'] += ","
			p[0]['place'] += str(i['place'])
		p[0]['place'] += "}"
		p[0]['type'][1] = str(p[2][0]['type'])

	print("literal")
	printp(p)

#ids are present in dcl only and they are not present in 3ac
def p_ids(p):
	'''ids	: IDENTIFIER
			| IDENTIFIER COMMA ids
	'''
	if len(p) == 2:
		p[0] = {
			"place" : p[1]
		}
	else:
		if type(p[3]['place']) == type([]):
			place = p[3]['place']
		else:
			place = [p[3]['place']]
		p[0] = {
			"place" : [p[1]] + place
		}
	print("ids")
	printp(p)


def p_sep(p):
	'''sep 	: SEMI_COLON
	'''
	print("sep")
	printp(p)

def p_epsilon(p):
	'''epsilon :
	'''
	print("epsilon")
	printp(p)
	p[0] = {
		"place" : ""
	}

def p_error(p):
	CRED = '\033[91m'
	CEND = '\033[0m'
	print(CRED + "Syntax error at line number '%s'" % p.lineno + CEND)
	print(CRED + "Syntax error at token '%s'" % p.value + CEND)

parser = yacc.yacc(debug=True)
inputfile = argv[1]
with open(inputfile, 'r') as f1:
	inputData = f1.read()
print(inputData)
parser.parse(inputData)
