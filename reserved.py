keywords = [
	'abstract',
	'break',
	'case',
	'catch',
	'class',
	'continue',
	'def',
	'default',
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
	'public',
	'return',
	'sealed',
	'switch',
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
# we need to ensure that only those keywords remain in this array which we'll actually use

data_types = [
	'Char', 'Boolean', 'Byte', 'Short', 'Int', 'Long', 'Float', 'Double',
	'Array', 'List', 'String',
	'Unit', 'Any', 'Anyval'
]
# Arrays aren't an explicit data type apparently. Argh.
# https://docs.scala-lang.org/tour/unified-types.html

reserved = { word:("RESERVED_" + word.upper()) for word in keywords }
for data_type in data_types:
	reserved[data_type] = "TYPE_" + data_type.upper()
