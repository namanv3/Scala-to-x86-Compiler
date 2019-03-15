import ply.yacc as yacc
from my_lexer import *
from sys import argv


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
#Taken from https://www.scala-lang.org/files/archive/spec/2.11/13-syntax-summary.html

def typecheck(p):
	if p[1]['type'] == "INT" and p[3]['type'] == "INT":
		emit(p[0]['place'] '=' p[1]['place'] 'int' p[2] p[3]['place'])
		p[0]['type'] = "INT"
	elif p[1]['type'] == "FLOAT" and p[3]['type'] == "INT":
		u = S.newtemp()
		emit(u '=' inttofloat p[1]['place'])
		emit(p[0]['place'] '=' u 'float 'p[2] p[3]['place'])
		p[0]['type'] = "FLOAT"
		S.addtemptoST(u, p[0]['type'], S.getwidth(p[0]['type']))
	elif p[1]['type'] == "INT" and p[3]['type'] == "FLOAT":
		u = S.newtemp()
		emit(u '=' inttofloat p[3]['place'])
		emit(p[0]['place'] '=' p[1]['place'] 'float 'p[2] u)
		p[0]['type'] = "FLOAT"
		S.addtemptoST(u, p[0]['type'], S.getwidth(p[0]['type']))
	else:
		emit(p[0]['place'] '=' p[1]['place'] 'float 'p[2] p[3]['place'])
		p[0]['type'] = "FLOAT"
	return p


def p_start(p):
		'''S : compilation_unit'''


def p_compilation_unit(p):
		'''compilation_unit : compilation_unit_0 top_stat_seq
		'''

def p_compilation_unit_0(p):
		'''compilation_unit_0 : epsilon
							  | compilation_unit_0  RESERVED_PACKAGE qual_id sep
							  | compilation_unit_0  RESERVED_PACKAGE qual_id
		'''

def p_top_stat_seq(p):
		'''top_stat_seq :  epsilon
						| top_stat_seq top_stat sep
						| top_stat_seq top_stat
		'''

def p_top_stat(p):
		'''top_stat : local_modifier_0 tmpl_def
					| import
		'''

def p_import(p):
		''' import : RESERVED_IMPORT import_expr import_0
		'''

def p_import_0(p):
		''' import_0 : COMMA import_expr import_0
					 | epsilon
		'''

def p_import_expr(p):
		'''import_expr : path
		'''

def p_modifier_0(p):
		''' modifier_0 : modifier
						| modifier_0 modifier
		'''


def p_modifier(p):
		'''modifier :   local_modifier
					|   access_modifier'''

def p_local_modifier_0(p):
		'''local_modifier_0 : epsilon
							| local_modifier_0 local_modifier
		'''

def p_local_modifier(p):
		'''local_modifier   :   RESERVED_FINAL
							|   RESERVED_ABSTRACT'''


def p_access_modifier(p):
		'''access_modifier  :   RESERVED_PRIVATE
							|   RESERVED_PROTECTED'''

def p_tmpl_def(p):
		''' tmpl_def : RESERVED_CLASS class_def
					 | RESERVED_OBJECT object_def
		'''

def p_class_def(p):
		'''class_def : id cmark class_param_clause class_template_opt
		'''
		S.endScope()

def p_cmark(p):
	'''cmark : epsilon
	'''
	addClass(p[-1]['place'], S.curr_scope)

def p_class_param_clause(p):
		'''class_param_clause : LPARAN class_params RPARAN
		'''

def p_class_params(p) :
		''' class_params : epsilon
						 | class_param class_param_0
		'''

def p_class_param_0(p):
		''' class_param_0 : epsilon
						  | COMMA class_param class_param_0
		'''

def p_class_param(p):
		''' class_param : val_var_1 id COLON type eq_expr_1
		'''
		if type(p[4]['type']) == type([]):
			addParamVar(p[2]['place'], p[4]['type'][0], 4, p.lineno, p[4]['type'][1])
		else:
			addParamVar(p[2]['place'], p[4]['type'], S.getwidth(p[4]['type']), p.lineno, typeArray = None)

def p_val_var_1(p):
		''' val_var_1 : val_var
					  | epsilon
		'''

def p_val_var(p):
		''' val_var : RESERVED_VAL
					| RESERVED_VAR
		'''

def p_eq_expr_1(p):
		''' eq_expr_1 : EQ_ASGN expr
					  | epsilon
		'''
		if len(p) == 3:
			emit(p[-3]['place'] ':=')

def p_class_template_opt(p):
		''' class_template_opt : class_template_opt_1 template_body
		'''

def p_class_template_opt_1(p):
		''' class_template_opt_1 : RESERVED_EXTENDS id
								 | epsilon
		'''

def p_template_body(p):
		''' template_body : LCURLYB template_body_0 RCURLYB
		'''

def p_template_body_0(p):
		''' template_body_0 : epsilon
							| template_body_0 template_stat sep
							| template_body_0 template_stat
		'''

def p_template_stat(p):
		''' template_stat : def
							| dcl
							| modifier_0 def
							| modifier_0 dcl
		'''

def p_def(p):
		''' def : path_var_def
				| RESERVED_DEF fun_def
				| tmpl_def
		'''

def p_path_var_def(p):
		''' path_var_def : RESERVED_VAR var_def
						 | RESERVED_VAL val_def
		'''

def p_var_def(p):
		''' var_def : id COLON type EQ_ASGN val_var_init
					| id EQ_ASGN val_var_init
		'''
		if len(p) == 4:
			p[1]['type'] = p[3]['type']
			emit(p[1]['place'] ":=" p[3]['place'])
		elif len(p) == 6:
			p[1]['type'] = p[3]['type']
			emit(p[1]['place'] ":=" p[5]['place'])
			if type(p[1]['type']) == type([]):
				addVar(p[1]['place'], p[3]['type'][0], p.lineno, 4, p[3]['type'][1])
			else:
				addVar(p[1]['place'], p[3]['type'], p.lineno, S.getWidth(p[3]['type']))

def p_array_size(p):
		''' array_size : LPARAN ints RPARAN
		'''
		p[0] = {
				'place' : p[2]
				}

def p_ints(p):
		''' ints : INT
				 | INT COMMA ints
		'''
		if len(p) == 2:
			p[0] = [p[1]]
		elif len(p) == 4:
			p[0] = [p[1]] + p[3]

def p_val_def(p):
		''' val_def : id COLON type EQ_ASGN val_var_init
					| id EQ_ASGN val_var_init
		'''
		if len(p) == 4:
			p[1]['type'] = p[3]['type']
			emit(p[1]['place'] ":=" p[3]['place'])
		elif len(p) == 6:
			p[1]['type'] = p[3]['type']
			emit(p[1]['place'] ":=" p[5]['place'])
			if type(p[1]['type']) == type([]):
				addVar(p[1]['place'], p[3]['type'][0], p.lineno, 4, p[3]['type'][1])
			else:
				addVar(p[1]['place'], p[3]['type'], p.lineno, S.getWidth(p[3]['type']))

def p_val_var_init(p):
		'''val_var_init : array_init
						| infix_expr
		'''
		if p.slice[1].type == 'infix_expr':
			p[0] = p[1]
		else:
			p[0] = {
						'place' : p[1]
					}

def p_array_init(p):
		''' array_init : LCURLYB epsilon RCURLYB
					   | LCURLYB array_init_0 RCURLYB
					   | TYPE_ARRAY LPARAN array_init_0 RPARAN
		'''
		if len(p) == 4:
			p[0] = p[2]
		elif len(p) == 5:
			p[0] = p[3]

def p_array_init_0(p):
		'''array_init_0 : val_var_init
						| array_init_0 COMMA val_var_init
		'''
		if len(p) == 2:
			p[0] = [p[1]]
		elif len(p) == 4:
			p[0] = p[1] + [p[3]]

def p_fun_def(p):
		''' fun_def : fun_sig col_type_1 EQ_ASGN LCURLYB block RCURLYB
		'''
		emit('END FUNCTION')
		S.endScope()

def p_col_type_1(p) :
		''' col_type_1 : COLON type
						| epsilon
		'''
		if len(p) == 2:
			S.SymbolTable[S.curr_scope]["rType"] = 'VOID'
		else:
			S.SymbolTable[S.curr_scope]["rType"] = p[2]['type']

def p_fun_sig(p):
		''' fun_sig : id fmark param_clause
		'''

def p_fmark(p):
		'''fmark: epsilon
		'''
		emit('BEGIN FUNCTION' + S.curr_scope + "." + p[-1]['place'] + ":")
		S.addFunc(p[-1]['place'], returnType = None, def_c = 1)

def p_param_clause(p):
		''' param_clause : LPARAN epsilon RPARAN
						 | LPARAN params RPARAN
		'''
		p[0] = p[2]

def p_params(p):
		''' params : param
				   | params COMMA param
		'''
		if len(p) == 2:
			p[0] = [p[1]]
		else:
			p[0] = p[1] + [p[3]]

def p_param(p):
		''' param : RESERVED_VAR id COLON type EQ_ASGN val_var_init
				  | RESERVED_VAR id COLON type
				  | id COLON type EQ_ASGN val_var_init
				  | id COLON type
		'''
		if len(p) == 7:
			emit(p[1]['place'] ":=" p[5]['place'])
			if type(p[4]['type'] == type([])):
				addVar(p[2]['place'], p[4]['type'][0], p.lineno, 4, p[4]['type'][1])
			else:
				addVar(p[2]['place'], p[4]['type'], p.lineno, S.getWidth(p[4]['type']))
		if len(p) == 6:
			emit(p[1]['place'] ":=" p[5]['place'])
			if type(p[3]['type'] == type([])):
				addVar(p[1]['place'], p[3]['type'][0], p.lineno, 4, p[3]['type'][1])
			else:
				addVar(p[1]['place'], p[3]['type'], p.lineno, S.getWidth(p[3]['type']))


def p_dcl(p):
		'''dcl  :   RESERVED_VAL val_dcl
				|   RESERVED_VAR var_dcl
				|   RESERVED_DEF fun_dcl'''

def p_val_dcl(p):
		'''val_dcl : id COLON type val_dcl_0
		'''
		p[1]['type'] = p[3]['type']
		if type(p[3]['type']) == type([]):
			S.addVar(p[1]['place'], p[3]['type'][0], p.lineno, 4, p[3]['place'][1])
		else:
			S.addVar(p[1]['place'], p[3]['type'], p.lineno, S.getWidth(p[3]['type']))


def p_val_dcl_0(p):
		'''val_dcl_0    :   epsilon
						|   COMMA val_dcl
		'''

def p_var_dcl(p):
		'''var_dcl  :   id COLON type
		'''
		p[1]['type'] = p[3]['type']
		if type(p[3]['type']) == type([]):
			S.addVar(p[1]['place'], p[3]['type'][0], p.lineno, 4, p[3]['place'][1])
		else:
			S.addVar(p[1]['place'], p[3]['type'], p.lineno, S.getWidth(p[3]['type']))


def p_fun_dcl(p):
		'''fun_dcl  :   id f_dcl_mark param_clause LCURLYB COLON type RCURLYB'''

def p_fun_dcl(p):
	S.addFunc(p[-1]['place'], def_c = 0)

def p_path(p):
		'''path :   id
				|   RESERVED_THIS
				|   path DOT id
		'''
		if len(p) == 2:
			p[0] = {
						'place' : p[1]['place']
						'type' : p[1]['type']
				   }
		else:
			p[0] = {
						'place' : p[3]['place']
						'type' : "OBJECT"
				   }

def p_block_stat(p):
		'''block_stat   :   def
						|   dcl
						|   expr
		'''

def p_block(p):
		'''block    :   epsilon
					|   block_stat sep block
		'''

def p_simple_expr(p):
		'''simple_expr  :   RESERVED_NEW class_template
						|   simple_expr1
		'''
		if len(p) == 3:
			p[0] = p[2]
		else:
			p[0] = p[1]

def p_class_template(p):
		'''class_template   :   id class_template_1
		'''
		p[0] = p[1]

def p_class_template_1(p):
		'''class_template_1 :   LPARAN id class_template_0 RPARAN
							|   LPARAN literal class_template_0 RPARAN
							|   LPARAN RPARAN
		'''

def p_class_template_0(p):
		'''class_template_0 :   COMMA id class_template_0
							|   COMMA literal class_template_0
							|   epsilon
		'''

def p_simple_expr1(p):
		'''simple_expr1 :   literal
						|   id LSQRB access RSQRB
						|   path
						|   LPARAN exprs_1 RPARAN
						|   simple_expr1 argument_exprs
						|   id RESERVED_MATCH switch_block
		'''
		if len(p) == 2:
			p[0] = p[1]
		elif len(p) == 3:
			p[0] = {
						'type' : p[1]['type'],
						'place' : p[1]['place']
					}
			p[0]['place'] += "("
			for i in p[2]:
				p[0]['place'] += i['place']
				p[0]['place'] += ","
			p[0]['place'] += ")"

		elif len(p) == 4:
			if p[1] == "(":
				p[0] = p[2]
		elif len(p) == 5:
			if p.slice[2].type == "LSQRB":
				p[0] = {
							'place' : p[1]['place'],
							'type' : p[1]['type'][1]
						}
				p[0]['place'] += "["
			for i in p[3]:
				p[0]['place'] += i['place']
				p[0]['place'] += ","
			p[0]['place'] += "]"


def p_prefix_expr(p):
		'''prefix_expr  :   simple_expr
						|   OP_SUB infix_expr
						|   OP_ADD infix_expr
						|   OP_NOT infix_expr'''

		if len(p) == 2:
			p[0] = p[1]
		elif len(p) == 3:
			u = S.newtemp()
			p[0] = {
					'place' : u,
					'type' : p[2]['type']
					}
			emit(p[0]['place'] ":=" p[1] p[2]['place'])

def p_type(p):
		''' type : basic_type
				 | array_type
		'''
		p[0] = {
					'type' : p[1]['type']
				}

def p_array_type(p):
		''' array_type : TYPE_ARRAY LSQRB type RSQRB array_size
						| TYPE_ARRAY LSQRB type RSQRB
		'''
		if len(p) == 6:
			p[0] = {
						'type' : ['ARRAY', p[3]['type']],
						'arraysize' : p[5]['place']
					}
		else:
			p[0] = {
						'type' : p[3]['type']
					}

def p_sep(p):
		''' sep : SEMI_COLON
				| epsilon
		'''

def p_qual_id(p):
		''' qual_id : id
					| qual_id DOT id
		'''
		if len(p) == 2:
			p[0] = p[1]
		else:
			p[0] = {
					'place' : p[1]['place'] + "." + p[3]['place']
					}

def p_object_def(p):
		''' object_def : id objmark class_template_opt
		'''
		p[1]['type'] = "OBJECT"
		p[0] = p[1]

def p_objmark(p):
		S.addObject(p[-1]['place'], S.curr_scope)

def p_for_logic(p):
		''' for_logic : LPARAN for_b_m for_init sep infix_expr sep for_upd
		'''
		emit('')

def p_for_init(p):
		''' for_init : epsilon
					 | path_var_def for_inits
					 | var_dcl for_inits
					 | infix_expr for_inits
		'''



def p_for_inits(p):
		'''for_inits : COMMA for_inits
					 | for_init
		'''

def p_for_upd(p):           # to be done later, the for case
		''' for_upd : RPARAN
								| infix_expr RPARAN
		'''

def p_switch_labels(p):
		''' switch_labels : RESERVED_CASE literal RIGHTARROW
						  | RESERVED_DEFAULT RIGHTARROW
						  | RESERVED_CASE RESERVED__ RIGHTARROW
		'''

def p_switch_block_statements(p):
		''' switch_block_statements : switch_labels LCURLYB block RCURLYB sep
									| switch_labels LCURLYB block RCURLYB
									| switch_labels val_var_init
		'''

def p_switch_block(p):
		''' switch_block : LCURLYB switch_block_statements_0 RCURLYB
		'''

def p_switch_block_statements_0(p):
		''' switch_block_statements_0 : switch_block_statements
									  | switch_block_statements_0 switch_block_statements
		'''
		if len(p)==2:
	        p[0] = [p[1]]
	    else:
	        p[0] = p[1]+[p[2]]

def p_expr(p):
		''' expr : RESERVED_IF LPARAN postfix_expr RPARAN if_b_m LCURLYB block RCURLYB if_s_m else_expression if_e_m
				 | RESERVED_WHILE LPARAN postfix_expr RPARAN wh_b_m LCURLYB block wh_s_m RCURLYB wh_e_m
			   	 | RESERVED_DO LCURLYB do_b_m block RCURLYB do_i_m RESERVED_WHILE LPARAN postfix_expr RPARAN do_s_m
				 | RESERVED_FOR for_logic LCURLYB for_i_m block RCURLYB
				 | RESERVED_RETURN postfix_expr
				 | RESERVED_RETURN
			   	 | RESERVED_BREAK
				 | RESERVED_CONTINUE
				 | postfix_expr
				 | id RESERVED_MATCH ms_b_m switch_block
		'''
	if (len(p) == 3 and p[1] == "return"):
		emit('return' p[2]['place'])
	elif p[1] == "return":
		emit('return')
	elif p[1] == "break":
		emit("goto" [loop end])
	elif p[1] == "continue":
		emit("goto" [loop begin])
	elif len(p) == 2:
		p[0] = p[1]


def p_wh_b_m(p):
	'''wh_b_m : epsilon
	'''
	emit("BEGIN:")
	emit(if p[-2]['place'] = 0 goto "AFTER")
	S.startScope()

def p_wh_s_m(p):
	'''wh_s_m : epsilon
	'''
	emit("goto BEGIN")
	S.endScope()

def p_wh_e_m(p):
	'''wh_e_m : epsilon
	'''
	emit("AFTER:")

def p_if_b_m(p):
	'''if_b_m : epsilon
	'''
	emit(if p[-2]['place'] = 0 goto "ELSE")
	S.startScope()

def p_if_s_m(p):
	'''if_s_m : epsilon
	'''
	S.endScope()

def p_if_i_m(p):
	'''if_i_m : epsilon
	'''
	S.startScope()
	emit('ELSE:')

def p_if_i1_m(p):
	'''if_i1_m : epsilon
	'''
	emit('ELSE:')

def p_if_e_m(p):
	'''if_e_m : epsilon
	'''
	emit("goto AFTER")
	emit("AFTER:")

def p_do_b_m(p):
	'''do_b_m : epsilon
	'''
	emit("BEGIN:")
	S.startScope()

def p_do_i_m(p):
	'''do_i_m : epsilon
	'''
	S.endScope()

def p_do_s_m(p):
	'''do_s_m : epsilon
	'''
	emit("if" p[-2]['place'] = 0 goto "AFTER")
	emit("goto BEGIN")
	emit("AFTER:")

# def p_for_i_m(p):
# 	#S.inter (new label)
# 	#block
# 	#goto S.update


def p_else_expression(p):
	''' else_expression : RESERVED_ELSE if_i_m LCURLYB block RCURLYB if_is_m
							| if_i1_m
	'''

def p_if_is_m(p):
	'''if_is_m : epsilon
	'''
	S.endScope()

def p_argument_exprs(p):
		''' argument_exprs : LPARAN exprs_1 RPARAN
		'''
		p[0] = p[2]

def p_exprs_1(p):
		''' exprs_1 : postfix_expr
					| epsilon
					| exprs_1 COMMA postfix_expr
		'''
		if len(p)==2:
			p[0] = [p[1]]
		else:
			p[0] = p[1] + [p[3]]

def p_postfix_expr(p):
		''' postfix_expr : infix_expr id_1
						 | infix_expr
		'''
		p[0]= p[1]

def p_id_1(p):
		''' id_1 : id
				| id_1 id
		'''
		if len(p)==3:
				p[0] = p[1] + [p[2]]
		else:
				p[0] = [p[1]]

def p_infix_expr(p):
		''' infix_expr : assign
					   | or_expression
		'''
		if p.slice[1].type == 'assign':
			p[0] = {}
			p[0]['place'] = S.newtemp()
			p[0]['type'] = 'BOOL'
		else:
			p[0] = p[1]

def p_assign(p):														# ----------------- remaining -------------------
		''' assign : simple_expr1 asgn or_expression
		'''
	#type error of assignment

	if (p[1]['type'] == type([])):
		if p[1]['type'][0] == 'literal':
			sys.exit("Value cannot be assigned to constant")
		elif p[3]['type'] == type([]):
			if p[3]['type'][0] == 'ARRAY':
				if p[1]['type'][1] == "FLOAT" and p[3]['type'][1] == "INT":
					u1 = S.newtemp()
					emit(u1 '=' inttofloat p[3]['place'])
				elif p[1]['type'][1] != p[3]['type'][1]:
					sys.exit("Incompatible data types")
				# x[i] = y[i] form
				u = S.newtemp()
				S.addtemptoST(u, p[3]['type'], S.getwidth(p[3]['type']))
				emit(u ':=' p[3]['place'])
				if p[2] == '=':
					emit(p[1]['place'] ":=" p[3]['place'])
				else:
					emit(p[1]['place'] ":=" p[1]['place'] p[2][0] p[3]['place'])
		else:
			if p[1]['type'][1] == "FLOAT" and p[3]['type'] == "INT":
				u1 = S.newtemp()
				emit(u1 '=' inttofloat p[3]['place'])
			elif p[1]['type'][1] != p[3]['type']:
				sys.exit("Incompatible data types")
			if p[2] == '=':
				emit(p[1]['place'] ":=" p[3]['place'])
			else:
				emit(p[1]['place'] ":=" p[1]['place'] p[2][0] p[3]['place'])
	else:
		u1 = p[3]['place']
		if p[3]['type'] == type([]):
			if p[3]['type'][0] == 'ARRAY':
				if p[1]['type'] == "FLOAT" and p[3]['type'][1] == "INT":
					u1 = S.newtemp()
					emit(u1 '=' inttofloat p[3]['place'])
				elif p[1]['type'] != p[3]['type'][1]:
					sys.exit("Incompatible data types")
		elif p[1]['type'] == "FLOAT" and p[3]['type'] == "INT":
			u1 = S.newtemp()
			emit(u1 '=' inttofloat p[3]['place'])
		elif p[1]['type'] != p[3]['type']:
			sys.exit("Incompatible data types")
		if p[2] == '=':
			emit(p[1]['place'] ":=" u1)
		else:
			emit(p[1]['place'] ":=" p[1]['place'] p[2][0] u1)



def p_or_expression(p):
		''' or_expression : and_expression
						  | or_expression OP_OR and_expression
		'''
		if len(p)==2:
				p[0] = p[1]
		else:
			if p[1]['type'] == "INT" and p[3]['type'] == "INT":
				p[0]['place'] = S.newtemp()
				p[0]['type'] = "INT"
				S.addtemptoST(p[0]['place'], p[0]['type'], S.getwidth(p[0]['type']))
				emit(p[0]['place'] ':=' p[1]['place'] '|' p[2]['place'])
			else:
				sys.exit("Incompatible data type error")

def p_xor_expression(p):
		''' xor_expression : and_expression
							| xor_expression OP_XOR and_expression
		'''
		if len(p)==2:
				p[0] = p[1]
		else:
			if p[1]['type'] == "INT" and p[3]['type'] == "INT":
				p[0]['place'] = S.newtemp()
				p[0]['type'] = "INT"
				S.addtemptoST(p[0]['place'], p[0]['type'], S.getwidth(p[0]['type']))
				emit(p[0]['place'] ':=' p[1]['place'] '^' p[2]['place'])
			else:
				sys.exit("Incompatible data type error")

def p_and_expression(p):
		''' and_expression : bit_or_expression
							| and_expression OP_AND bit_or_expression
		'''
		if len(p)==2:
				p[0] = p[1]
		else:
			if p[1]['type'] == "INT" and p[3]['type'] == "INT":
				p[0]['place'] = S.newtemp()
				p[0]['type'] = "INT"
				S.addtemptoST(p[0]['place'], p[0]['type'], S.getwidth(p[0]['type']))
				emit(p[0]['place'] ':=' p[1]['place'] '&' p[2]['place'])
			else:
				sys.exit("Incompatible data type error")

def p_bit_or_expression(p):
		''' bit_or_expression : bit_and_expression
							  | bit_or_expression LO_OR bit_and_expression
		'''
		if len(p)==2:
			p[0] = p[1]
		else:
			if p[1]['type'] == "BOOL":
				p[0]['place'] = S.newtemp()
				p[0]['type'] = "BOOL"
				S.addtemptoST(p[0]['place'], p[0]['type'], S.getwidth(p[0]['type']))
				emit(p[0]['place'] ':=' p[1]['place'] 'or' p[2]['place'])
			else:
				sys.exit("Incompatible data type error")

def p_bit_and_expression(p):
		'''bit_and_expression : eq_expression
							  | bit_and_expression LO_AND eq_expression
		'''
		if len(p)==2:
			p[0] = p[1]
		else:
			if p[1]['type'] == "BOOL":
				p[0]['place'] = S.newtemp()
				p[0]['type'] = "BOOL"
				S.addtemptoST(p[0]['place'], p[0]['type'], S.getwidth(p[0]['type']))
				emit(p[0]['place'] ':=' p[1]['place'] 'and' p[2]['place'])
			else:
				sys.exit("Incompatible data type error")

def p_eq_expression(p):
		'''eq_expression : comp_expression
						 | eq_expression EQ comp_expression
						 | eq_expression NEQ comp_expression
		'''
		if len(p)==2:
				p[0] = p[1]
		else:
			if p[1]['type'] == p[3]['type']:
				p[0]['place'] = S.newtemp()
				p[0]['type'] = "BOOL"
				S.addtemptoST(p[0]['place'], p[0]['type'], S.getwidth(p[0]['type']))
				emit('if' p[1]['place'] p[2] p[3]['place'] 'goto' nextstat+3)
				emit(p[0]['place'] = 0)
				emit(goto nextstat+2)
				emit(p[0]['place'] = 1)
			else:
				sys.exit("Comparison operation performed on incompatible data types")

def p_comp_expression(p):
		'''comp_expression : shift_expression
							| comp_expression LEQ shift_expression
							| comp_expression LT shift_expression
							| comp_expression GEQ shift_expression
							| comp_expression GT shift_expression
		'''
		#global variable nextstat
		if len(p)==2:
				p[0] = p[1]
		else:
			if (p[1]['type'] == "INT" or p[1]['type'] == "FLOAT") and (p[3]['type'] == "INT" or p[3]['type'] == "FLOAT"):
				p[0]['place'] = S.newtemp()
				p[0]['type'] = "BOOL"
				S.addtemptoST(p[0]['place'], p[0]['type'], S.getwidth(p[0]['type']))
				emit('if' p[1]['place'] p[2] p[3]['place'] 'goto' nextstat+3)
				emit(p[0]['place'] = 0)
				emit(goto nextstat+2)
				emit(p[0]['place'] = 1)
			else:
				sys.exit("Comparison operation performed on incompatible data types")


def p_shift_expression(p):
		'''shift_expression : add_expression
							| shift_expression OP_RSHIFT add_expression
							| shift_expression OP_LSHIFT add_expression
							| shift_expression OP_RRSHIFT add_expression
		'''
		if len(p)==2:
				p[0] = p[1]
		else:
			if p[1]['type'] == "INT" and p[3]['type'] == "INT":
				p[0]['place'] = S.newtemp()
				emit(p[0]['place'] '=' p[1]['place'] p[2] p[3]['place'])
				p[0]['type'] = "INT"
				S.addtemptoST(p[0]['place'], p[0]['type'], S.getwidth(p[0]['type']))
			else:
				sys.exit("Shift operations on non-integers are not allowed")


def p_add_expression(p):
		'''add_expression : mul_expression
							| add_expression OP_ADD mul_expression
							| add_expression OP_SUB mul_expression
		'''
		#type conversion for short, int,long and float
		if len(p)==2:
				p[0] = p[1]
		else:
			p[0]['place'] = S.newtemp()
			p = typecheck(p)
			S.addtemptoST(p[0]['place'], p[0]['type'], S.getwidth(p[0]['type']))

def p_mul_expression(p):
		'''mul_expression : unary_expression
						  | mul_expression OP_MOD unary_expression
						  | mul_expression OP_MULT unary_expression
						  | mul_expression OP_DIVIDE unary_expression
		'''
		# Type conversion for int, long and float
		if len(p) == 2:
				p[0] = p[1]
		else:
			p[0]['place'] = S.newtemp()
			if p[2] == "%":
				if p[1]['type'] == "INT" and p[3]['type'] == "INT":
					p[0]['type'] = "INT"
					emit(p[0]['place'] '=' p[1]['place'] '%' p[3]['place'])
					S.addtemptoST(p[0]['place'], p[0]['type'], S.getwidth(p[0]['type']))
				else:
					sys.exit("Modulous operation attempted on non-integer values")
			else:
				p = typecheck(p)
				S.addtemptoST(p[0]['place'], p[0]['type'], S.getwidth(p[0]['type']))

def p_unary_expression(p):
		'''unary_expression : prefix_expr
							| LPARAN infix_expr RPARAN
		'''
		if len(p) == 2:
			p[0] = p[1]
		elif len(p) == 4:
			p[0] = p[2]

def p_asgn(p):
		''' asgn : EQ_ASGN
				 | ADD_ASGN
				 | SUB_ASGN
				 | MULT_ASGN
				 | DIV_ASGN
				 | MOD_ASGN
				 | LSHIFT_ASGN
				 | RSHIFT_ASGN
				 | AND_ASGN
				 | OR_ASGN
				 | XOR_ASGN
		'''
		p[0] = {
					'place' : p[1]
				}

def p_basic_type(p):
		''' basic_type : TYPE_INT
						| TYPE_FLOAT
						| TYPE_CHAR
						| TYPE_STRING
						| TYPE_BOOLEAN
						| RESERVED_NULL
		'''
	p[0] = {
				'place' : p[1].upper(),
				'type' : p[1].upper()
			}

def p_id(p):
		''' id : ID
		'''
		p[0] = {
					'place' : p[1]
			   }

def p_access(p):
		''' access : ID
				   | literal
				   | access COMMA ID
				   | access  COMMA literal
		'''
	if len(p) == 2:
		if type(p[1]) == type({}):
			if p[1]['type'] != "INT":
				sys.exit("Array index not an integer")
		else:
			if p.slice[1].type != "INT":
				sys.exit("Array index not an integer")

        p[0] = [{
            'place' : p[1],
            'type' : "INT"
            }]
	else:
		if type(p[3]) == type({}):
			if p[1]['type'] != "INT":
				sys.exit("Array index not an integer")
		else:
			if p.slice[3].type != "INT":
				sys.exit("Array index not an integer")
		p[0] = p[1]
		p[0].append({
				'place' : p[3],
				'type' : "INT"
			})

def p_literal(p):
		''' literal : BOOL
					| INT
					| CHAR
					| STRING
					| FLOAT
		'''
	p[0] = {
			'place'	: p[1],
			'type' : ['literal', p.slice[1].type]
			}


def p_epsilon(p):
		''' epsilon :
		'''
	#doubt
	p[0] = {
			'place' : ""
			}

def p_error(p):
		CRED = '\033[91m'
		CEND = '\033[0m'
		print(CRED+"Syntax error at line number'%s'" % p.lineno + CEND)
		print(CRED+"Syntax error at the token '%s'" % p.value +CEND)

parser = yacc.yacc(debug=True)

with open(inputfile, 'r') as f:
	input_data = f.read()

parser.parse(input_data)
