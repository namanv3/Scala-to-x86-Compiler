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


fdot = open(outputfile, 'w+')
fdot.write('digraph G { \n')
count = -1

def print_node(v, p_count):
		global count
		if p_count != -1:
				count += 1
				fdot.write('\"%d\" [label=\"%s\"];\n'%(count,v[0]))
				fdot.write('\"%d\" -> \"%d\";\n'%(p_count,count))
		else:
				count += 1
				fdot.write('\"%d\" [label=\"%s\"];\n'%(count,v[0]))
		p_count = count
		for i in range(1, len(v)):
				if type(v[i]) is tuple:
						print_node(v[i], p_count)
				else:
						count += 1
						fdot.write('\"%d\" [label=\"%s\"];\n'%(count,v[i]))
						fdot.write('\"%d\" -> \"%d\";\n'%(p_count,count))

#Taken from https://www.scala-lang.org/files/archive/spec/2.11/13-syntax-summary.html

def p_start(p):
		'''S : compilation_unit'''
		p[0] = ("S",p[1])
		print(p[0])
		print_node(p[0],-1)

def p_compilation_unit(p):
		'''compilation_unit : compilation_unit_0 top_stat_seq
		'''
		p[0] = ("compilation_unit",p[1],p[2])
		print("p_compilation_unit")

def p_compilation_unit_0(p):
		'''compilation_unit_0 : epsilon
													| compilation_unit_0  RESERVED_PACKAGE qual_id sep
													| compilation_unit_0  RESERVED_PACKAGE qual_id
		'''
		if len(p) >= 4:
			p[0] = ("compilation_unit_0",p[1],p[2],p[3])
		else:
			p[0] = ("compilation_unit_0")

		print("p_compilation_unit_0")

# removed packaging object

def p_top_stat_seq(p):
		'''top_stat_seq :  epsilon
											| top_stat_seq top_stat sep
											| top_stat_seq top_stat
		'''
		if len(p) >= 3:
			p[0] = ("top_stat_seq",p[1],p[2])
		else:
			p[0] = ("top_stat_seq")
		print("p_top_stat_seq")

def p_top_stat(p):
		'''top_stat : local_modifier_0 tmpl_def
								| import
		'''
		if len(p) > 2:
			p[0] = ("top_stat",p[1],p[2])
		else:
			p[0] = ("top_stat",p[1])
		print("p_top_stat")

def p_import(p):
		''' import : RESERVED_IMPORT import_expr import_0
		'''

		p[0] = ("import", p[1], p[2], p[3])
		print("p_import")

def p_import_0(p):
		''' import_0 : COMMA import_expr import_0
								 | epsilon
		'''
		if len(p) > 2:
			p[0] = ("import_0", p[1], p[2], p[3])
		else:
			p[0] = ("import_0")

		print("p_import_0")

def p_import_expr(p):
		'''import_expr : path
		'''
		p[0] = ("import_expr", p[1])
		print("p_import_expr")

def p_modifier_0(p):
		''' modifier_0 : modifier
									 | modifier_0 modifier
		'''
		if len(p) > 2:
			p[0] = ("modifier_0", p[1], p[2])
		else:
			p[0] = ("modifier_0", p[1])
		print("p_modifier_0")


def p_modifier(p):
		'''modifier :   local_modifier
								|   access_modifier'''

		p[0] = ("modifier", p[1])
		print("p_modifier")

def p_local_modifier_0(p):
		'''local_modifier_0 : epsilon
												| local_modifier_0 local_modifier
		'''
		if len(p) > 2:
			p[0] = ("local_modifier_0", p[1],p[2])
		else:
			p[0] = ("local_modifier_0")
		print("p_local_modifier_0")

def p_local_modifier(p):
		'''local_modifier   :   RESERVED_FINAL
												|   RESERVED_ABSTRACT'''

		p[0]  = ("local_modifier", p[1])
		print("p_local_modifier")

def p_access_modifier(p):
		'''access_modifier  :   RESERVED_PRIVATE
												|   RESERVED_PROTECTED'''

		p[0]  = ("access_modifier", p[1])
		print("p_access_modifier")


def p_tmpl_def(p):
		''' tmpl_def : RESERVED_CLASS class_def
								 | RESERVED_OBJECT object_def
		'''
		p[0] = ("tmpl_def", p[1], p[2])
		print("p_tmpl_def")

def p_class_def(p):
		'''class_def : id class_param_clause class_template_opt
		'''
		p[0] = ("class_def", p[1], p[2], p[3])
		print("p_class_def")


def p_class_param_clause(p):
		'''class_param_clause : LPARAN class_params RPARAN
		'''
		p[0] = ("class_param_clause", p[1], p[2], p[3])
		print("p_class_param_clause")

def p_class_params(p) :
		''' class_params : epsilon
										 | class_param class_param_0
		'''
		if len(p) > 2:
			p[0] = ("class_params", p[1], p[2])
		else:
			p[0] = ("class_params")
		print("p_class_param")

def p_class_param_0(p):
		''' class_param_0 : epsilon
											| COMMA class_param class_param_0
		'''
		if len(p) > 2:
			p[0] = ("class_params", p[1], p[2],p[3])
		else:
			p[0] = ("class_params")

		print("p_class_param_0")

def p_class_param(p):
		''' class_param : val_var_1 id COLON type eq_expr_1
		'''
		p[0] = ("class_param",p[1], p[2], p[3], p[4], p[5])
		print("p_class_param")

def p_val_var_1(p):
		''' val_var_1 : val_var
									| epsilon
		'''
		p[0] = ("val_var_1", p[1])

		print("p_val_var_1")

def p_val_var(p):
		''' val_var : RESERVED_VAL
								| RESERVED_VAR
		'''
		p[0] = ("val_var", p[1])

		print("p_val_var")

def p_eq_expr_1(p):
		''' eq_expr_1 : EQ_ASGN expr
									| epsilon
		'''
		if len(p) > 2:
			p[0] = ("eq_expr_1", p[1],p[2])
		else:
			p[0] = ("eq_expr_1")
		print("p_eq_expr_1")

def p_class_template_opt(p):
		''' class_template_opt : class_template_opt_1 template_body
		'''
		p[0] = ("class_template_opt", p[1], p[2])
		print("p_class_template_opt")

def p_class_template_opt_1(p):
		''' class_template_opt_1 : RESERVED_EXTENDS id
														 | epsilon
		'''
		if len(p) > 2:
			 p[0] = ("class_template_opt_1", p[1], p[2])
		else:
			p[0] = ("class_template_opt_1")
		print("p_class_template_opt_1")

def p_template_body(p):
		''' template_body : LCURLYB template_body_0 RCURLYB
		'''
		p[0] = ("template_body", p[1], p[2], p[3])
		print("p_template_body")

def p_template_body_0(p):
		''' template_body_0 : epsilon
												| template_body_0 template_stat sep
												| template_body_0 template_stat
		'''
		if len(p) == 2:
			p[0] = ("template_body_0")
		else:
			p[0] = ("template_body_0", p[1], p[2])
		print("p_template_body_0")

def p_template_stat(p):
		''' template_stat : def
											| dcl
											| modifier_0 def
											| modifier_0 dcl
		'''

		if len(p) > 2:
			p[0] = ("template_stat", p[1], p[2])
		else:
			p[0] = ("template_stat", p[1])
		print("p_template_stat")


def p_def(p):
		''' def : path_var_def
						| RESERVED_DEF fun_def
						| tmpl_def
		'''
		if len(p) > 2:
			p[0] = ("def", p[1], p[2])
		else:
			p[0] = ("def", p[1])
		print("p_def")

def p_path_var_def(p):
		''' path_var_def : RESERVED_VAR var_def
										 | RESERVED_VAL val_def
		'''
		p[0] = ("path_var_def", p[1], p[2])
		print("p_path_var_def")

def p_var_def(p):
		''' var_def : id COLON type EQ_ASGN val_var_init
								| id EQ_ASGN val_var_init
		'''
		if len(p) > 4:
			p[0] = ("var_def", p[1], p[2], p[3], p[4], p[5])
		else:
			p[0] = ("var_def", p[1], p[2], p[3])
		print("p_var_def")

def p_array_size(p):
		''' array_size : LPARAN ints RPARAN
		'''
		p[0] = ("array_size", p[1], p[2], p[3])
		print("p_array_size")

def p_ints(p):
		''' ints : INT
						 | INT COMMA ints
		'''
		if len(p) > 2:
			p[0] = ("ints", p[1],p[2],p[3])
		else:
			p[0] = ("ints", p[1])
		print("p_ints")

def p_val_def(p):
		''' val_def : id COLON type EQ_ASGN val_var_init
								| id EQ_ASGN val_var_init
		'''
		if len(p) > 4:
			p[0] = ("val_def", p[1], p[2], p[3], p[4], p[5])
		else:
			p[0] = ("val_def", p[1], p[2], p[3])
		print("p_val_def")

def p_val_var_init(p):
		'''val_var_init : array_init
										| infix_expr
		'''
		p[0] = (p[1])
		print("p_val_var_init")

def p_array_init(p):
		''' array_init : LCURLYB epsilon RCURLYB
									 | LCURLYB array_init_0 RCURLYB
									 | TYPE_ARRAY LPARAN array_init_0 RPARAN
		'''
		if len(p)==4:
				p[0] = ("array_init", p[1], p[2], p[3])
		else:
				p[0] = ("array_init", p[1],p[2],p[3],p[4])
		print("p_array_init")

def p_array_init_0(p):
		'''array_init_0 : val_var_init
										| array_init_0 COMMA val_var_init
		'''
		if len(p) > 2:
			p[0] = ("array_init_0", p[1], p[2], p[3])
		else:
			p[0] = ("array_init_0", p[1])
#some ambiguity here ???
		print("p_array_init_0")

def p_fun_def(p):
		''' fun_def : fun_sig col_type_1 EQ_ASGN LCURLYB block RCURLYB
		'''
		p[0] = ("fun_def", p[1], p[2], p[3], p[4], p[5], p[6])
		print("p_fun_def")

def p_col_type_1(p) :
		''' col_type_1 : COLON type
									 | epsilon
		'''
		if len(p) > 2:
			p[0] = ("col_type_1", p[1], p[2])
		else:
			p[0] = ("col_type_1")

		print("p_col_type_")

def p_fun_sig(p):           # function is named id@no.of args
		''' fun_sig : id param_clause
		'''
		p[0] = ("fun_sig", p[1], p[2])
		print("p_fun_sig")

def p_param_clause(p):
		''' param_clause : LPARAN RPARAN
										 | LPARAN params RPARAN
		'''
		if len(p) > 3:
			p[0] = ("param_clause", p[1], p[2], p[3])
		else:
			p[0] = ("param_clause", p[1], p[2])
		print("p_param_clause")

def p_params(p):
		''' params : param
							 | params COMMA param
		'''
		if len(p) >2:
			p[0] = ("params", p[1], p[2], p[3])
		else:
			p[0] = ("params", p[1])
		print("p_params")

def p_param(p):
		''' param : RESERVED_VAR id COLON type EQ_ASGN val_var_init
							| RESERVED_VAR id COLON type
							| id COLON type EQ_ASGN val_var_init
							| id COLON type
		'''
		if len(p) == 7:
			p[0] = ("param", p[1], p[2], p[3],p[4], p[5], p[6])
		elif len(p) == 6:
			p[0] = ("param", p[1], p[2], p[3],p[4], p[5])
		elif len(p) == 5:
			p[0] = ("param", p[1], p[2], p[3],p[4])
		else:
			p[0] = ("param", p[1], p[2], p[3])

		print("p_param")

def p_eq_expr(p):
		''' eq_expr : epsilon
								| EQ_ASGN expr
		'''
		if len(p) > 2:
			p[0] = ("eq_expr", p[1], p[2])
		else:
			p[0] = ("eq_expr")
		print("p_eq_expr")

def p_param_type(p):
		''' param_type : type
		'''
		p[0] = ("param_type", p[1])
		print("p_param_type")

def p_dcl(p):
		'''dcl  :   RESERVED_VAL val_dcl
						|   RESERVED_VAR var_dcl
						|   RESERVED_DEF fun_dcl'''

		p[0] = ("dcl", p[1], p[2])
		print("p_dcl")

def p_val_dcl(p):
		'''val_dcl   :   id COLON type val_dcl_0'''
		p[0] = ("val_dcl", p[1], p[2], p[3], p[4])
		print("p_val_dcl")

def p_val_dcl_0(p):
		'''val_dcl_0    :   epsilon
										|   COMMA val_dcl'''

		if len(p) > 2:
			p[0] = ("val_dcl_0", p[1], p[2])
		else:
			p[0] = ("val_dcl_0")
		print("p_val_dcl_0")

def p_var_dcl(p):
		'''var_dcl  :   id COLON type
		'''
		p[0] = ("var_dcl", p[1], p[2],p[3])
		print("p_var_dcl")

def p_fun_dcl(p):
		'''fun_dcl  :   id param_clause LCURLYB COLON type RCURLYB'''
			 #        |   id param_clause'''

		p[0] = ("fun_dcl",p[1], p[2], p[3],p[4], p[5], p[6])
		print("p_fun_dcl")


def p_path(p):
		'''path :   id
						|   RESERVED_THIS
						|   path DOT id
						|   RESERVED_SUPER DOT path
						'''
		if len(p) > 2:
			p[0] = ("path",p[1],p[2],p[3])
		else:
			p[0] = ("path",p[1])
		print("p_path")

def p_block_stat(p):
		'''block_stat   :   def
										|   dcl
										|   expr'''

		p[0] = ("block_stat",p[1])
		print("p_block_stat")

def p_block(p):
		'''block    :   epsilon
								|   block_stat sep block'''
		if len(p) > 2:
			p[0] = ("block", p[1], p[2], p[3])
		else:
			p[0] = ("block")
		print("p_block")

def p_simple_expr(p):
		'''simple_expr  :   RESERVED_NEW class_template
										|   simple_expr1'''
		if len(p) > 2:
			p[0] = (p[1], p[2])
		else:
			p[0] = (p[1])
		print("p_simple_expr")

def p_class_template(p):
		'''class_template   :   id class_template_1'''

		p[0] = ("class_template", p[1], p[2])
		print("p_class_template")

def p_class_template_1(p):
		'''class_template_1 :   LPARAN id class_template_0 RPARAN
												|   LPARAN literal class_template_0 RPARAN
												|   LPARAN RPARAN '''

		if len(p) > 3:
			p[0] = ("class_template_1",p[1],p[2],p[3],p[4])
		else:
			p[0] = ("class_template_1",p[1],p[2])
		print("p_class_template_1")

def p_class_template_0(p):
		'''class_template_0 :   COMMA id class_template_0
												|   COMMA literal class_template_0
												|   epsilon'''
		if len(p) > 2:
			p[0] = ("class_template_0",p[1],p[2],p[3])
		else:
			p[0] = ("class_template_0")

		print("p_class_template_0")

def p_simple_expr1(p):
		'''simple_expr1 :   literal
										|   ID LSQRB access RSQRB
										|   path
										|   LPARAN exprs_1 RPARAN
										|   simple_expr1 argument_exprs
										|   id RESERVED_MATCH switch_block
		'''
		if len(p) == 2:
			p[0] = (p[1])
		elif len(p) == 3:
			p[0] = (p[1], p[2])
		elif len(p) == 4:
			p[0] = (p[1], p[2], p[3])
		else:
			p[0] = (p[1], p[2], p[3], p[4])
		print("p_simple_expr1")

def p_prefix_expr(p):
		'''prefix_expr  :   simple_expr
										|   OP_SUB infix_expr
										|   OP_ADD infix_expr
										|   OP_NOT infix_expr'''

		if len(p)>2:
			p[0] = (p[1],p[2])
		else:
			p[0] = (p[1])

		print("p_prefix_expr")

def p_type(p):                      # look at <T>
		''' type : basic_type
						 | array_type
						 | id
		'''
		p[0] = ("type",p[1])
		print("p_type")

def p_array_type(p):
		''' array_type : TYPE_ARRAY LSQRB type RSQRB array_size
										| TYPE_ARRAY LSQRB type RSQRB
		'''
		if len(p) > 5:
			p[0] = ("array_type",p[1], p[2], p[3], p[4], p[5])
		else:
			p[0] = ("array_type",p[1], p[2], p[3], p[4])
		print("p_array_type")

def p_sep(p):
		''' sep : SEMI_COLON
						| epsilon
		'''
		p[0] = ("sep")
		print("p_sep")

def p_qual_id(p):
		''' qual_id : id
								| qual_id DOT id
		'''
		if len(p) > 2:
			p[0] = ("qual_id",p[1],p[2],p[3])
		else:
			p[0] = ("qual_id",p[1])
		print("p_qual_id")

def p_object_def(p):
		''' object_def : id class_template_opt
		'''
		p[0] = ("object_def",p[1],p[2])
		print("p_object_def")

def p_catch_params(p):
		''' catch_params : type id
		'''
		p[0] = ("catch_params",p[1],p[2])
		print("p_catch_params")

def p_catch_clause(p):
		''' catch_clause : RESERVED_CATCH LPARAN catch_params LPARAN LCURLYB block RCURLYB catch_clause_1
		'''
		p[0] = ("catch_clause", p[1],p[2],p[3],p[4],p[5],p[6],p[7],p[8])
		print("p_catch_clause")

def p_catch_clause_1(p):
		''' catch_clause_1 : catch_clause
											 | epsilon
		'''
		p[0] = ("catch_clause_1",p[1])
		print("p_catch_clause_1")

def p_for_logic(p):
		''' for_logic : LPARAN for_init sep infix_expr sep for_upd
										| LPARAN ID LEFTARROW ID RPARAN
		'''

		if len(p) == 7:
			p[0] = ("for_logic",p[1],p[2],p[3],p[4],p[5],p[6])
		else:
			p[0] = ("for_logic",p[1],p[2],p[3],p[4],p[5])
		print("p_for_logic")

def p_for_init(p):
		''' for_init : epsilon
								 | path_var_def for_inits
								 | var_dcl for_inits
								 | infix_expr for_inits
		'''
		if len(p) > 2:
			p[0] = ("for_init", p[1],p[2])
		else:
			p[0] = ("for_init", p[1])

		print("p_for_init")

def p_for_inits(p):
		'''for_inits : COMMA for_inits
								 | for_init
		'''
		if len(p) > 2:
			p[0] = ("for_inits", p[1], p[2])
		else:
			p[0] = ("for_inits", p[1])
		print("p_for_inits")

def p_for_upd(p):           # to be done later, the for case
		''' for_upd : RPARAN
								| infix_expr RPARAN
		'''
		if len(p) > 2:
			p[0] = ("for_upd", p[1], p[2])
		else:
			p[0] = ("for_upd", p[1])
		print("p_for_upd")

def p_switch_labels(p):
		''' switch_labels : RESERVED_CASE literal RIGHTARROW
											| RESERVED_DEFAULT RIGHTARROW
											| RESERVED_CASE RESERVED__ RIGHTARROW
		'''
		if len(p) > 3:
			p[0] = ("switch_labels", p[1], p[2], p[3])
		else:
			p[0] = ("switch_labels", p[1], p[2])
		print("p_switch_labels")

def p_switch_block_statements(p):
		''' switch_block_statements : switch_labels LCURLYB block RCURLYB sep
																| switch_labels LCURLYB block RCURLYB
																| switch_labels val_var_init
		'''
		if len(p) >= 5:
			p[0] = ("switch_block_statements", p[1],p[2],p[3],p[4])
		else:
			p[0] = ("switch_block_statements", p[1],p[2])
		print("p_switch_block_statements")

def p_switch_block(p):
		''' switch_block : LCURLYB switch_block_statements_0 RCURLYB
		'''
		p[0] = ("switch_block", p[1],p[2],p[3])
		print("p_switch_block")

def p_switch_block_statements_0(p):
		''' switch_block_statements_0 : switch_block_statements
																	| switch_block_statements_0 switch_block_statements
		'''
		if len(p) > 2:
			p[0] = ("switch_block_statements_0", p[1],p[2])
		else:
			p[0] = ("switch_block_statements_0", p[1])
		print("p_switch_block_statements_0")

def p_expr(p):
		''' expr : RESERVED_IF LPARAN postfix_expr RPARAN LCURLYB block RCURLYB expression1
							| RESERVED_WHILE LPARAN postfix_expr RPARAN LCURLYB block RCURLYB
							| RESERVED_TRY LCURLYB block RCURLYB catch_clause_1 expression2
							| RESERVED_DO LCURLYB block RCURLYB RESERVED_WHILE LPARAN postfix_expr RPARAN
							| RESERVED_FOR for_logic  LCURLYB block RCURLYB
							| RESERVED_RETURN postfix_expr
							| RESERVED_RETURN
							| RESERVED_BREAK
							| RESERVED_CONTINUE
							| postfix_expr
							| RESERVED_SWITCH LPARAN postfix_expr RPARAN switch_block
							| id RESERVED_MATCH switch_block
		'''
		if len(p) == 9:
				p[0] = ("expr", p[1],p[2],p[3],p[4],p[5],p[6],p[7],p[8])
		elif len(p) == 8:
				p[0] = ("expr", p[1],p[2],p[3],p[4],p[5],p[6],p[7])
		elif len(p) == 7:
				p[0] = ("expr", p[1],p[2],p[3],p[4],p[5],p[6])
		elif len(p) == 6:
				p[0] = ("expr", p[1],p[2],p[3],p[4],p[5])
		elif len(p) == 3:
				p[0] = ("expr", p[1],p[2])
		elif len(p) == 2:
				p[0] = ("expr", p[1])
		else:
				p[0] = ("expr", p[1],p[2],p[3])

		print("p_expr")

def p_expression1(p):
		''' expression1 : RESERVED_ELSE LCURLYB block RCURLYB
										| epsilon
		'''
		if len(p) == 5:
				p[0] = ("expression1", p[1],p[2],p[3],p[4])
		else:
				p[0] = ("expression1")

		print("p_expression1")

def p_expression2(p):
		''' expression2 : RESERVED_FINALLY LCURLYB block RCURLYB
										| epsilon
		'''

		if len(p) == 5:
				p[0] = ("expression2", p[1],p[2],p[3],p[4])
		else:
				p[0] = ("expression2")

		print("p_expression2")

def p_argument_exprs(p):
		''' argument_exprs : LPARAN exprs_1 RPARAN
		'''
		p[0] = ("argument_exprs",p[1],p[2],p[3])
		print("p_argument_exprs")

def p_exprs_1(p):
		''' exprs_1 : postfix_expr
								| epsilon
								| exprs_1 COMMA postfix_expr
		'''
		if len(p)==2:
				p[0] = (p[1])
		else:
				p[0] = (p[1],p[2],p[3])

		print("p_exprs_1")

def p_postfix_expr(p):
		''' postfix_expr : infix_expr id_1
										 | infix_expr
		'''
		if len(p)==3:
				p[0] = (p[1],p[2])
		else:
				p[0] = (p[1])

		print("p_postfix_expr")

def p_id_1(p):
		''' id_1 : id
						 | id_1 id
		'''
		if len(p)==2:
				p[0] = (p[1])
		else:
				p[0] = (p[1],p[2])

		print("p_id_1")

def p_infix_expr(p):
		''' infix_expr : assign
									 | or_expression
		'''
		p[0] = (p[1])

		print("p_infix_expr")

def p_assign(p):
		''' assign : simple_expr1  asgn or_expression
		'''
		p[0] = ("assign",p[1],p[2],p[3])

		print("p_assign")

def p_or_expression(p):
		''' or_expression : and_expression
											| or_expression OP_OR and_expression
		'''
		if len(p)==2:
				p[0] = (p[1])
		else:
				p[0] = (p[1],p[2],p[3])
		print("p_or_expression")

def p_xor_expression(p):
		''' xor_expression : and_expression
											 | xor_expression OP_XOR and_expression
		'''
		if len(p)==2:
				p[0] = (p[1])
		else:
				p[0] = (p[1],p[2],p[3])
		print("p_xor_expression")

def p_and_expression(p):
		''' and_expression : bit_or_expression
											 | and_expression OP_AND bit_or_expression
		'''
		if len(p)==2:
				p[0] = (p[1])
		else:
				p[0] = (p[1],p[2],p[3])
		print("p_and_expression")

def p_bit_or_expression(p):
		''' bit_or_expression : bit_and_expression
													| bit_or_expression LO_OR bit_and_expression
		'''
		if len(p)==2:
				p[0] = (p[1])
		else:
				p[0] = (p[1],p[2],p[3])
		print("p_bit_or_expression")

def p_bit_and_expression(p):
		'''bit_and_expression : eq_expression
													| bit_and_expression LO_AND eq_expression
		'''
		if len(p)==2:
				p[0] = (p[1])
		else:
				p[0] = (p[1],p[2],p[3])
		print("p_bit_and_expression")

def p_eq_expression(p):
		'''eq_expression : comp_expression
											| eq_expression EQ comp_expression
											| eq_expression NEQ comp_expression
		'''
		if len(p)==2:
				p[0] = (p[1])
		else:
				p[0] = (p[1],p[2],p[3])

		print("p_eq_expression")

def p_comp_expression(p):
		'''comp_expression : shift_expression
											| comp_expression LEQ shift_expression
											| comp_expression LT shift_expression
											| comp_expression GEQ shift_expression
											| comp_expression GT shift_expression
		'''
		if len(p)==2:
				p[0] = (p[1])
		else:
				p[0] = (p[1],p[2],p[3])

		print("p_comp_expression")

def p_shift_expression(p):
		'''shift_expression : add_expression
											| shift_expression OP_RSHIFT add_expression
											| shift_expression OP_LSHIFT add_expression
											| shift_expression OP_RRSHIFT add_expression
		'''
		if len(p)==2:
				p[0] = (p[1])
		else:
				p[0] = (p[1],p[2],p[3])

		print("p_shift_expression")

def p_add_expression(p):
		'''add_expression : mul_expression
											| add_expression OP_ADD mul_expression
											| add_expression OP_SUB  mul_expression
		'''
		if len(p)==2:
				p[0] = (p[1])
		else:
				p[0] = (p[1],p[2],p[3])
		print("p_add_expression")

def p_mul_expression(p):
		'''mul_expression : unary_expression
											| mul_expression OP_MOD unary_expression
											| mul_expression OP_MULT  unary_expression
											| mul_expression OP_DIVIDE  unary_expression
		'''
		if len(p)==2:
				p[0] = (p[1])
		else:
				p[0] = (p[1],p[2],p[3])
		print("p_mul_expression")

def p_unary_expression(p):
		'''unary_expression : prefix_expr
												| LPARAN infix_expr RPARAN
		'''
		if len(p)==2:
				p[0] = (p[1])
		else:
				p[0] = (p[1],p[2],p[3])
		print("p_unary_expression")

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
		p[0] = (p[1])
		print("p_asgn")

def p_basic_type(p):
		''' basic_type : TYPE_INT
									 | TYPE_FLOAT
									 | TYPE_CHAR
									 | TYPE_STRING
									 | TYPE_BOOLEAN
									 | RESERVED_NULL
		'''
		p[0] = (p[1])
		print("p_basic_type")

def p_id(p):
		''' id : ID
		'''
		p[0] = (p[1])
		print("p_id")

def p_access(p):
		''' access : ID
							 | literal
							 | access COMMA ID
							 | access  COMMA literal
		'''
		if len(p)==2:
				p[0] = (p[1])
		else:
				p[0] = (p[1],p[2],p[3])
		print("p_access")

def p_literal(p):
		''' literal : BOOL
								| INT
								| CHAR
								| STRING
								| FLOAT
		'''
		p[0] = (p[1])
		print("p_literal")

def p_epsilon(p):
		''' epsilon :
		'''
		p[0] = ("epsilon")
		print("epsilon")

def p_error(p):
		CRED = '\033[91m'
		CEND = '\033[0m'
		print(CRED+"Syntax error at line number'%s'" % p.lineno + CEND)
		print(CRED+"Syntax error at the token '%s'" % p.value +CEND)

parser = yacc.yacc(debug=True)

with open(inputfile, 'r') as f:
	input_data = f.read()

parser.parse(input_data)
fdot.write('}\n')
