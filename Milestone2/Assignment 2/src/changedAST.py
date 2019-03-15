import ply.yacc as yacc
from my_lexer import *
from sys import argv
import re

input_str = sys.argv[1:]

out_re = r'^--out.*'
help_re = r'^--help'

inputfile = ""
outputfile = ""

for arg in input_str:
	if re.match(out_re,arg):
		outputfile = arg[6:]
	elif re.match(help_re,arg):
		print("Usage: python ./src/myASTGenerator.py <inputfile> --output=<outputfile>")
		exit()
	else:
		inputfile = arg


#taken from https://www.scala-lang.org/files/archive/spec/2.11/06-expressions.html#infix-operations
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

#Taken from https://www.scala-lang.org/files/archive/spec/2.11/13-syntax-summary.html
def emit(out,in1,op,in2):

def typecheck(p):
	if p[1]['type'] == "INT" and p[3]['type'] == "INT":
		emit(p[0]['place'] '=' p[1]['place'] 'int' p[2] p[3]['place'])
		p[0]['type'] = "INT"
	elif p[1]['type'] == "FLOAT" and p[3]['type'] == "INT":
		u = newtemp
		emit(u '=' inttofloat p[1]['place'])
		emit(p[0]['place'] '=' u 'float 'p[2] p[3]['place'])
		p[0]['type'] = "FLOAT"
	elif p[1]['type'] == "INT" and p[3]['type'] == "FLOAT":
		u = newtemp
		emit(u '=' inttofloat p[3]['place'])
		emit(p[0]['place'] '=' p[1]['place'] 'float 'p[2] u)
		p[0]['type'] = "FLOAT"
	else:
		emit(p[0]['place'] '=' p[1]['place'] 'float 'p[2] p[3]['place'])
		p[0]['type'] = "FLOAT"
	return p


def label(name):

def temp():

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
		'''class_def : id class_param_clause class_template_opt
		'''
		p[0].place = p[1].place

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

def p_class_template_opt(p):
		''' class_template_opt : class_template_opt_1 template_body
		'''
		p[0].place = p[1].place

def p_class_template_opt_1(p):
		''' class_template_opt_1 : RESERVED_EXTENDS id
														 | epsilon
		'''
		if len(p) == 2:
			p[0].place = p[2].place
		elif len(p) == 1:
			p[0].place = ''

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
			emit(p[1].place ":=" p[3].place)
		elif len(p) == 6:
			emit(p[1].place ":=" p[5].place)

def p_array_size(p):
		''' array_size : LPARAN ints RPARAN
		'''
		p[0].place = p[2].place 	#array_size resolved

def p_ints(p):
		''' ints : INT
						 | INT COMMA ints
		'''
		if len(p) == 2:
			p[0].place = p[1].place
		elif len(p) == 4:
			p[0].place = p[1].place + p[3].place
def p_val_def(p):
		''' val_def : id COLON type EQ_ASGN val_var_init
					| id EQ_ASGN val_var_init
		'''
		if len(p) == 4:
			emit(p[1].place ":=" p[3].place)
		elif len(p) == 6:
			emit(p[1].place ":=" p[5].place)

def p_val_var_init(p):
		'''val_var_init : array_init
										| infix_expr
		'''
		if len(p) == 2:
			p[0].place = p[1].place

def p_array_init(p):
		''' array_init : LCURLYB epsilon RCURLYB
					   | LCURLYB array_init_0 RCURLYB
					   | TYPE_ARRAY LPARAN array_init_0 RPARAN
		'''
		if len(p) == 4:
			p[0].place = p[1].place
		elif len(p) == 5:
			p[0].place = p[1].place

def p_array_init_0(p):
		'''array_init_0 : val_var_init
										| array_init_0 COMMA val_var_init
		'''
		if len(p) == 2:
			p[0].place = p[1].place
		elif len(p) == 4:
			p[0].place = p[1].place + p[3].place

def p_fun_def(p):
		''' fun_def : fun_sig col_type_1 EQ_ASGN LCURLYB block RCURLYB
		'''


def p_col_type_1(p) :
		''' col_type_1 : COLON type
									 | epsilon
		'''

def p_fun_sig(p):           # function is named id@no.of args
		''' fun_sig : id param_clause
		'''

def p_param_clause(p):
		''' param_clause : LPARAN RPARAN
										 | LPARAN params RPARAN
		'''

def p_params(p):
		''' params : param
							 | params COMMA param
		'''

def p_param(p):
		''' param : RESERVED_VAR id COLON type EQ_ASGN val_var_init
							| RESERVED_VAR id COLON type
							| id COLON type EQ_ASGN val_var_init
							| id COLON type
		'''


def p_eq_expr(p):
		''' eq_expr : epsilon
								| EQ_ASGN expr
		'''

def p_param_type(p):
		''' param_type : type
		'''

def p_dcl(p):
		'''dcl  :   RESERVED_VAL val_dcl
						|   RESERVED_VAR var_dcl
						|   RESERVED_DEF fun_dcl'''


def p_val_dcl(p):
		'''val_dcl   :   id COLON type val_dcl_0'''


def p_val_dcl_0(p):
		'''val_dcl_0    :   epsilon
										|   COMMA val_dcl'''

def p_var_dcl(p):
		'''var_dcl  :   id COLON type
		'''
		symtab.addVar(idVal, idType, offset, lineno, idSize = 4, typeArray = None, objSize = None):

def p_fun_dcl(p):
		'''fun_dcl  :   id param_clause LCURLYB COLON type RCURLYB'''
			 #        |   id param_clause'''


def p_path(p):
		'''path :   id
						|   RESERVED_THIS
						|   path DOT id
						|   RESERVED_SUPER DOT path
						'''


def p_block_stat(p):
		'''block_stat   :   def
										|   dcl
										|   expr'''



def p_block(p):
		'''block    :   epsilon
								|   block_stat sep block'''


def p_simple_expr(p):
		'''simple_expr  :   RESERVED_NEW class_template
										|   simple_expr1'''
		if len(p) == 3:
			p[0].place = p[2].place
		else:
			p[0].place = p[1].place

def p_class_template(p):
		'''class_template   :   id class_template_1'''


def p_class_template_1(p):
		'''class_template_1 :   LPARAN id class_template_0 RPARAN
												|   LPARAN literal class_template_0 RPARAN
												|   LPARAN RPARAN '''


def p_class_template_0(p):
		'''class_template_0 :   COMMA id class_template_0
												|   COMMA literal class_template_0
												|   epsilon'''


def p_simple_expr1(p):
		'''simple_expr1 :   literal
						|   ID LSQRB access RSQRB
						|   path
						|   LPARAN exprs_1 RPARAN
						|   simple_expr1 argument_exprs
						|   id RESERVED_MATCH switch_block
		'''
		if len(p) == 2:
			p[0].place = p[1].place
		if len(p) == 4:
			if p[1] == "(":
				p[0].place = p[2].place
		#doubt simple_expr1

def p_prefix_expr(p):
		'''prefix_expr  :   simple_expr
										|   OP_SUB infix_expr
										|   OP_ADD infix_expr
										|   OP_NOT infix_expr'''
		if len(p) == 2:
			p[0].place = p[1].place
		elif len(p) == 3:
			p[0].place = newtemp
			if p[1].place == "+":
				emit(p[0].place ":=" "+" p[2].place)
			elif p[1].place == "-":
				emit(p[0].place ":=" "-" p[2].place)
			elif p[1].place == "!":
				emit(p[0].place ":=" "!" p[2].place)

def p_type(p):                      # look at <T>
		''' type : basic_type
						 | array_type
						 | id
		'''
		p[0].place = p[1].place

def p_array_type(p):
		''' array_type : TYPE_ARRAY LSQRB type RSQRB array_size
										| TYPE_ARRAY LSQRB type RSQRB
		'''
		p[0].place = p[3].place


def p_sep(p):
		''' sep : SEMI_COLON
						| epsilon
		'''


def p_qual_id(p):
		''' qual_id : id
								| qual_id DOT id
		'''


def p_object_def(p):
		''' object_def : id class_template_opt
		'''


def p_catch_params(p):
		''' catch_params : type id
		'''


def p_catch_clause(p):
		''' catch_clause : RESERVED_CATCH LPARAN catch_params LPARAN LCURLYB block RCURLYB catch_clause_1
		'''


def p_catch_clause_1(p):
		''' catch_clause_1 : catch_clause
											 | epsilon
		'''


def p_for_logic(p):
		''' for_logic : LPARAN for_b_m for_init sep infix_expr sep for_upd
										| LPARAN ID LEFTARROW ID RPARAN	#doubt wth is this
		'''

def for_b_m(p):
	emit(for_init.place)
	#S.begin (new label)
	#if infix expr is false goto S.after
	#goto S.inter
	#S.update (new label)
	#for_update
	#goto S.begin

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


def p_expr(p):
		''' expr : RESERVED_IF LPARAN postfix_expr RPARAN LCURLYB if_s_m block RCURLYB expression1 if_e_m
							| RESERVED_WHILE LPARAN wh_b_m postfix_expr RPARAN LCURLYB wh_s_m block RCURLYB wh_e_m
							| RESERVED_TRY LCURLYB block RCURLYB catch_clause_1 expression2
							| RESERVED_DO LCURLYB do_b_m block RCURLYB RESERVED_WHILE LPARAN do_s_m postfix_expr RPARAN do_e_m
							| RESERVED_FOR for_logic LCURLYB for_i_m block RCURLYB
							| RESERVED_RETURN postfix_expr
							| RESERVED_RETURN
							| RESERVED_BREAK
							| RESERVED_CONTINUE
							| postfix_expr
							| RESERVED_SWITCH LPARAN s_b_m postfix_expr RPARAN switch_block
							| id RESERVED_MATCH ms_b_m switch_block
		'''
	if (len(p) == 3 and p[1] == "return"):
		#doubt function return
	elif p[1] == "return":
		#doubt function return
	elif p[1] == "break":
		emit("goto" [loop end])
	elif p[1] == "continue":
		emit("goto" [loop begin])
	elif len(p) == 2:
		p[0].place = p[1].place


def wh_b_m(p):
	#create new label S.begin

def wh_s_m(p):
	#if false goto S.after
	#S1.code (block)
	#goto S.begin

def wh_e_m(p):
	#S.after

def if_s_m(p):
	#if false goto S.else
	#S1.code (block)
	#goto S.after
	#S.else (new label)

def if_i_m(p):
	#block
	#goto S.after

def if_i1_m(p):
	#goto S.after

def if_e_m(p):
	#S.after (new label)

def do_b_m(p):
	#S.begin (new label)
	#block

def do_s_m(p):
	#if true goto S.begin
	#goto S.after

def do_e_m(p):
	#S.after (new label)	#might not be needed

def for_i_m(p):
	#S.inter (new label)
	#block
	#goto S.update


def p_expression1(p):
		''' expression1 : RESERVED_ELSE if_i_m LCURLYB block RCURLYB
						| if_i1_m
		'''

def p_expression2(p):
		''' expression2 : RESERVED_FINALLY LCURLYB block RCURLYB
						| epsilon
		'''

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
		if len(p) == 2:
			p[0]= p[1]
		else:
			p[0] = [p[1]] + [p[2]]

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
		p[0] = p[1]

def p_assign(p):														# ----------------- remaining -------------------
		''' assign : simple_expr1 asgn or_expression
		'''
	#type error of assignment
		p[1].place = p[3].place
		emit(p[1].place ':=' p[3].place)

		if (p[1]['type'] == type([])):
			if p[1]['type'][0] == 'literal':
				sys.exit("Value cannot be assigned to constant")

def p_or_expression(p):
		''' or_expression : and_expression
						  | or_expression OP_OR and_expression
		'''
		if len(p)==2:
				p[0] = p[1]
		else:
			if p[1]['type'] == "INT" and p[3]['type'] == "INT":
				p[0]['place'] = newtemp
				p[0]['type'] = "INT"
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
				p[0]['place'] = newtemp
				p[0]['type'] = "INT"
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
				p[0]['place'] = newtemp
				p[0]['type'] = "INT"
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
			p[0]['place'] = newtemp
			p[0]['type'] = "BOOL"
			if p[1]['type'] == "BOOL":
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
			p[0]['place'] = newtemp
			p[0]['type'] = "BOOL"
			if p[1]['type'] == "BOOL":
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
				p[0]['place'] = newtemp
				p[0]['type'] = "BOOL"
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
				p[0]['place'] = newtemp
				p[0]['type'] = "BOOL"
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
			if p[1]['type'] == "INT and p[3]['type'] == "INT":
				p[0]['place'] = newtemp
				emit(p[0]['place'] '=' p[1]['place'] p[2] p[3]['place'])
				p[0]['type'] = "INT"
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
			p[0]['place'] = newtemp
			p = typecheck(p)

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
			p[0]['place'] = newtemp
			if p[2] == "%":
				if p[1]['type'] == "INT" and p[3]['type'] == "INT":
					p[0]['place'] = newtemp
					p[0]['type'] = "INT"
					emit(p[0]['place'] '=' p[1]['place'] '%' p[3]['place'])
				else:
					sys.exit("Modulous operation attempted on non-integer values")
			else:
				p = typecheck(p)

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
				'place' : p[1].upper()
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
