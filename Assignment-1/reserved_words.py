keywords = [
	'abstract',
	'case',
	'catch',
	'class',
	'def',
	'do',
	'else',
	'extends',
	'false',
	'final',
	'finally',
	'for',
	'forSome',
	'if',
	'implicit',
	'import',
	'lazy',
	'match',
	'new',
	'null',
	'object',
	'override',
	'package',
	'private',
	'protected',
	'return',
	'sealed',
	'super',
	'this',
	'throw',
	'trait',
	'true',
	'try',
	'type',
	'val',
	'var',
	'while',
	'with',
	'yield'
]			# from https://www.scala-lang.org/docu/files/ScalaReference.pdf, Page 4
# how should we handle the non english reserved characters?

data_types = [
	'Byte',
	'Short',
	'Int',
	'Long',
	'Float',
	'Double',
	'Char',
	'String',
	'Boolean',
	'Unit',
	'Null',
	'Nothing',
	'Any',
	'AnyRef'
]			# from https://www.tutorialspoint.com/scala/scala_data_types.htm

reserved = { word:("R_" + word.upper()) for word in keywords }
for data_type in data_types:
	reserved[data_type] = "TYPE_" + data_type.upper() 

# for key in reserved:
# 	print(key,reserved[key])