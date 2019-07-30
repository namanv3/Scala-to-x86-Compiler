from sys import argv
print("-----------------nextUse------------------")

inputfile = argv[1][:-6] + "IR.txt"
handle = open(inputfile)
irCode = handle.read().split('\n')
handle.close()

nextUseTable = {}
nextUse = {}
liveTable = {}

def isLiteral(arg):
	try:
		x = int(arg)
		return True
	except:
		try:
			x = float(arg)
			return True
		except:
			if arg == "True" or arg == "False":
				return True
			elif arg[:5] == "ARRAY":
				return True
			elif arg[:4] == "temp":
				return True
			return False


irCode.reverse()
for lineStr in irCode:
	print(lineStr)
	if len(lineStr) == 0:
		continue
	line = lineStr.strip().split()[2:]
	lineNo = int(lineStr.strip().split()[0])
	
	if line[0] == ":=" and len(line) == 5:
		# := $t1 2 int* 4
		# := $t1 $t0 int+ $t4
		dest = line[1]
		arg1 = line[2]
		arg2 = line[4]

		if not isLiteral(arg1):
			liveTable[(arg1,lineNo)] = True
			if arg1 in nextUse:
				nextUseTable[(arg1,lineNo)] = nextUse[arg1]
				nextUse[arg1] = lineNo
			else:
				nextUseTable[(arg1,lineNo)] = -1
				nextUse[arg1] = lineNo

		if not isLiteral(arg2):
			liveTable[(arg2,lineNo)] = True
			if arg2 in nextUse:
				nextUseTable[(arg2,lineNo)] = nextUse[arg2]
				nextUse[arg2] = lineNo
			else:
				nextUseTable[(arg2,lineNo)] = -1
				nextUse[arg2] = lineNo
			
		liveTable[(dest,lineNo)] = False
		if dest in nextUse:
			nextUseTable[(dest,lineNo)] = nextUse[dest]
		else:
			nextUseTable[(dest,lineNo)] = -1

	elif line[0] == ":=" and len(line) == 3:
		# := $t4 $t2

		dest = line[1]
		src  = line[2]

		if not isLiteral(src):
			liveTable[(src,lineNo)] = True
			if src in nextUse:
				nextUseTable[(src,lineNo)] = nextUse[src]
				nextUse[src] = lineNo
			else:
				nextUseTable[(src,lineNo)] = -1
				nextUse[src] = lineNo

		liveTable[(dest,lineNo)] = False
		if dest in nextUse:
			nextUseTable[(dest,lineNo)] = nextUse[dest]
		else:
			nextUseTable[(dest,lineNo)] = -1

	elif line[0] == "if":
		# 2: if $t5 < $t9 goto 5

		arg1 = line[1]
		arg2 = line[3]

		if not isLiteral(arg1):
			liveTable[(arg1,lineNo)] = True
			if arg1 in nextUse:
				nextUseTable[(arg1,lineNo)] = nextUse[arg1]
				nextUse[arg1] = lineNo
			else:
				nextUseTable[(arg1,lineNo)] = -1
				nextUse[arg1] = lineNo

		if not isLiteral(arg2):
			liveTable[(arg2,lineNo)] = True
			if arg2 in nextUse:
				nextUseTable[(arg2,lineNo)] = nextUse[arg2]
				nextUse[arg2] = lineNo
			else:
				nextUseTable[(arg2,lineNo)] = -1
				nextUse[arg2] = lineNo

	elif line[0] == "param" and not isLiteral(line[1]):
		# param $t2

		arg1 = line[1]
		liveTable[(arg1,lineNo)] = True
		if arg1 in nextUse:
			nextUseTable[(arg1,lineNo)] = nextUse[arg1]
			nextUse[arg1] = lineNo
		else:
			nextUseTable[(arg1,lineNo)] = -1
			nextUse[arg1] = lineNo

	elif line[0] == "refparam":
		# refparam $res
		arg1 = line[1]
		liveTable[(arg1,lineNo)] = True
		if arg1 in nextUse:
			nextUseTable[(arg1,lineNo)] = nextUse[arg1]
			nextUse[arg1] = lineNo
		else:
			nextUseTable[(arg1,lineNo)] = -1
			nextUse[arg1] = lineNo

print("------")
for entry in nextUseTable:
	print(entry, nextUseTable[entry])