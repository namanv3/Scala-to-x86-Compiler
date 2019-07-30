from sys import argv
import re
from semantics1504 import S
from nextUse import nextUseTable, liveTable, isLiteral
inputfile = argv[1][:-6] + "IR.txt"
handle = open(inputfile)
irCode = handle.read().split('\n')
handle.close()

print("------------------------------------------------------------------------------------")
currStrNumber = 0
dataSection = ".section .data\n"
for (i,line) in zip(range(len(irCode)), irCode):
	x = re.search("\".*\"",line)
	if not x:
		continue
	
	s = x.start()
	e = x.end()
	string = line[s:e]
	strLabel = "temp" + str(currStrNumber)
	irCode[i] = irCode[i][:s] + "temp" + str(currStrNumber) + irCode[i][e:]
	print(irCode[i])
	currStrNumber += (e - s)
	dataSection += "\t" + strLabel + ": .string " + string + "\n"

print("--------------------------------------------")
outputfile = argv[1][:-6] + "Assembly.s"
f = open(outputfile,"w+")
registers = ['%eax', '%ebx', '%ecx', '%edx', '%edi', '%esi']
regDesciptor = {reg : "" for reg in registers}

commands = {
	"int+" : "addl",
	"int-" : "subl",
	"int*" : "imul",
	"int/" : "idiv",
	"=="   : "jne",
	"!="   : "jeq",
	">="    : "jg",
	"<="    : "jl",
	"<"   : "jle",
	">"   : "jge",
	"<<"   : "shl",
	">>"   : "shr",
	"&&"  : "and",
	"||"   : "or",
	"&"    : "and",
	"|"	   : "or",
	"^"    : "xor"
}

oppositeOp = {
	">=" : "<=",
	"<=" : ">=",
	">" : "<",
	"<" : ">",
	"==" : "==",
	"!=" : "!="
}

scopeStack = []

class Scope:
	def __init__(self, name, distFromEBP):
		self.name = name
		self.distFromEBP = distFromEBP
		self.parameters = {}
		self.getParameters()
		self.localVariables = []
		self.getLocalVariables()
		self.sizeOflocalVariables = 0
		self.callerSavedRegisters = []
		self.addressDescriptor = {}
		self.assignStackLocation()

	def getParameters(self):
		if self.distFromEBP > 0:
			return
		for key in S.SymbolTable[self.name]["params"]:
			self.parameters[key] = S.SymbolTable[self.name]["params"][key]["tempName"]
		# print(self.name, self.parameters)

	def getLocalVariables(self):
		for var in S.SymbolTable[self.name]["variables"].keys():
			if var not in self.parameters:
				self.localVariables.append(var)

	def assignStackLocation(self):
		currOffset = self.distFromEBP
		for var in self.localVariables:
			currOffset += S.SymbolTable[self.name]["variables"][var]["size"]
			self.addressDescriptor[var] = (-1 * currOffset)
		self.sizeOflocalVariables = currOffset - self.distFromEBP 

		currOffset = 8
		for param in self.parameters:
			self.addressDescriptor[param] = currOffset
			currOffset += S.SymbolTable[self.name]["params"][param]["size"]

	def getLocationInStack(self, variable):
		if variable in self.parameters.values():
			for key in self.parameters:
				if self.parameters[key] == variable:
					variable = key
					break
		# print(self.name, variable)
		offset = self.addressDescriptor[variable]
		return str(offset) + "(%ebp)"

	def findCallerSavedRegs(self):
		global regDesciptor
		for reg in regDesciptor:
			if regDesciptor[reg] == "":
				continue
			self.callerSavedRegisters.append(reg)

	def addArrayToStack(self,src,dest):
		zerothAddress = int(self.addressDescriptor[dest])
		elements = src[6:-1].split(",")
		for e in elements:
			if isLiteral(e):
				f.write("\tmovl $" + e + ", " + str(zerothAddress) + "(%ebp)\n")
			else:
				location = findRegOrMemoryLocation(e)
				if location not in registers and "" in regDesciptor.values():
					newlocation = findRegLocation("")
					f.write("\tmovl " + location + ", " + newlocation + "\n")
					location = newlocation
				elif location not in registers:
					var = regDesciptor["%eax"]
					moveToStack(var)
					f.write("\tmovl " + location + ", %eax\n")
					location = "%eax"
					regDesciptor["%eax"] = e
				f.write("\tmovl " + location + ", " + str(zerothAddress) + "(%ebp)\n")
			zerothAddress += 4


def findRegLocation(variable):
	global regDesciptor
	for reg,var in regDesciptor.items():
		if var == variable:
			return reg

def findMemoryLocation(variable):
	global scopeStack
	j = -1
	while variable not in scopeStack[j].addressDescriptor:
		j -= 1
	return scopeStack[j].getLocationInStack(variable)

def findRegOrMemoryLocation(variable):
	global regDesciptor
	global scopeStack
	if variable in regDesciptor.values():
		return findRegLocation(variable)
	else:
		j = len(scopeStack) - 1
		while variable not in scopeStack[j].addressDescriptor:
			j -= 1
		return scopeStack[j].getLocationInStack(variable)

def furthestNextUse(lineNo):
	global regDesciptor
	furthest = lineNo
	chosenReg = ""
	for reg, var in regDesciptor.items():
		if nextUseTable[(var,lineNo)] > furthest:
			furthest = nextUseTable[(var,lineNo)]
			chosenReg = reg

	return chosenReg

def moveToStack(variable):
	global scopeStack
	# print(">>>>", variable)
	j = len(scopeStack) - 1
	while variable not in scopeStack[j].addressDescriptor:
		j -= 1
	stackLocation = scopeStack[j].getLocationInStack(variable)
	f.write("\tmovl " + findRegLocation(variable) + ", " + stackLocation + "\n")

def findDest(lineNo, line):
	# := $t4 $t2 int+ 9
	# := $t4 $t2 int+ $t9
	global regDesciptor
	global scopeStack

	var = line[1]
	tuple0 = (var,lineNo)
	arg1 = line[2]
	tuple1 = (arg1, lineNo)

	if arg1 in regDesciptor.values() and nextUseTable[tuple1] == -1:
		return findRegLocation(arg1)
	elif "" in regDesciptor.values():
		return findRegLocation("")
	elif nextUseTable[tupl0] != -1:
		chosenReg = furthestNextUse(lineNo)
		moveToStack(regDesciptor[chosenReg])
		return chosenReg
	else:
		return findRegOrMemoryLocation(var)



f.write(".section .text" + "\n")
f.write(".globl main\n" + "\n")
linesToSkip = 0
for i,lineStr in zip(range(len(irCode)), irCode):
	if linesToSkip > 0:
		linesToSkip -= 1
		continue

	if lineStr == "":
		continue

	line = lineStr.strip().split()[2:]
	lineNo = int(lineStr.strip().split()[0])

	print("// " + str(lineNo) + " " + str(line) + "\n")
	# f.write("// " + str(lineNo) + " " + str(line) + "\n")

	if line[0] == ":=" and len(line) == 5 and line[2][0] != "&":
		# := $t4 3 int+ 8
		# := $t4 $t2 int+ 9
		# := $t4 2 int+ $t9
		# := $t4 $t2 int+ $t9

		dest = line[1]
		arg1 = line[2]
		op   = line[3]
		arg2 = line[4]

		command = commands[op]
		if isLiteral(arg1) and isLiteral(arg2):
			src = eval(arg1 + op[-1] + arg2)
			L = findRegOrMemoryLocation(dest)
			f.write("\tmovl $" + str(src) + ", " + L + "\n")

		elif isLiteral(arg2):
			src = "$" + arg2
			L = findDest(lineNo,line)
			Y_curr = findRegOrMemoryLocation(arg1)
			if L != Y_curr:
				f.write("\tmovl " + Y_curr + ", " + L + "\n")
			f.write("\t" + command + " " + src + ", " + L + "\n")
			while dest in regDesciptor.values():
				toBeEmptied = findRegLocation(dest)
				regDesciptor[toBeEmptied] = ""
			if L in registers:
				regDesciptor[L] = dest

		elif isLiteral(arg1):
			newline = [line[0], line[1], line[4], line[3], line[2]]
			src = "$" + arg1

			L = findDest(lineNo,newline)
			Y_curr = findRegOrMemoryLocation(arg2)
			f.write("\tmovl " + Y_curr + ", " + L + "\n")
			f.write("\t" + command + " " + src + ", " + L + "\n")
			while dest in regDesciptor.values():
				toBeEmptied = findRegLocation(dest)
				regDesciptor[toBeEmptied] = ""
			if L in registers:
				regDesciptor[L] = dest

		else:
			L = findDest(lineNo,line)
			Y_curr = findRegOrMemoryLocation(arg1)
			if L != Y_curr:
				f.write("\tmovl " + Y_curr + ", " + L + "\n")
			Z_curr = findRegOrMemoryLocation(arg2)
			f.write("\t" + command + " " + Z_curr + ", " + L + "\n")
			while dest in regDesciptor.values():
				toBeEmptied = findRegLocation(dest)
				regDesciptor[toBeEmptied] = ""
			if L in registers:
				regDesciptor[L] = dest
		
		if arg1 in regDesciptor.values() and nextUseTable[(arg1,lineNo)] == -1:
			toBeEmptied = findRegLocation(arg1)
			regDesciptor[toBeEmptied] = ""
		if arg2 in regDesciptor.values() and nextUseTable[(arg2,lineNo)] == -1:
			toBeEmptied = findRegLocation(arg2)
			regDesciptor[toBeEmptied] = ""

	elif line[0] == ":=" and len(line) == 5:
		# := $t4 &$t2 int+ $t9
		if irCode[i+1].strip().split()[3][0] == "*":
			print("***************************")
			continue

		dest = line[1]
		arg1 = line[2]
		op   = line[3]
		arg2 = line[4]
		command = commands[op]

		arrStart = findMemoryLocation(arg1[1:])
		# print(scopeStack[-1].name, arrStart)

		if int(arrStart[:-6]) > 0:
			# it is a parameter, that is, we already have the address
			reg1 = ""
			if "" in regDesciptor.values():
				reg1 = findRegLocation("")
				regDesciptor[reg1] =  "occupied"
			else:
				var = regDesciptor["%eax"]
				moveToStack(var)
				reg1 = "%eax"
				regDesciptor["%eax"] = "occupied"
			f.write("\tmovl " + arrStart + ", " + reg1 + "\n")
			f.write("\taddl " + findRegOrMemoryLocation(arg2) + ", " + reg1 + "\n")
			destreg = ""
			if "" in regDesciptor.values():
				destreg = findRegLocation("")
				regDesciptor[destreg] = dest
			elif regDesciptor["%eax"] == "occupied":
				var = regDesciptor["%ebx"]
				moveToStack(var)
				destreg = "%ebx"
				regDesciptor["%ebx"] = dest
			f.write("\tmovl 0(" + reg1 + "), " + destreg + "\n")
			regDesciptor[reg1] =  ""
			
		else:
			reg = ""
			if "" in regDesciptor.values():
				reg = findRegLocation("")
				regDesciptor[reg] =  "occupied"
			else:
				var = regDesciptor["%eax"]
				moveToStack(var)
				reg = "%eax"
				regDesciptor["%eax"] = "occupied"
			f.write("\tmovl %ebp, " + reg + "\n")
			f.write("\taddl $" + arrStart[:-6] + ", " + reg + "\n")
			f.write("\taddl " + findRegOrMemoryLocation(arg2) + ", " + reg + "\n")

			destreg = ""
			if "" in regDesciptor.values():
				destreg = findRegLocation("")
				regDesciptor[destreg] = dest
			elif regDesciptor["%eax"] == "occupied":
				var = regDesciptor["%ebx"]
				moveToStack(var)
				destreg = "%ebx"
				regDesciptor["%ebx"] = dest
			f.write("\tmovl 0(" + reg + "), " + destreg + "\n")
			regDesciptor[reg] =  ""

	elif line[0] == ":=" and len(line) == 3 and line[1][0] != "*":
		# := $t4 5
		# := $t4 ARRAY{2,6,1}
		# := $t4 $t8

		src  = line[2]
		dest = line[1]

		if isLiteral(src):
			if src[:5] == "ARRAY":
				scopeStack[-1].addArrayToStack(src,dest)
			else:
				dest = findRegOrMemoryLocation(dest)
				f.write("\tmovl $" + src + ", " + dest + "\n")
			continue

		src_curr  = findRegOrMemoryLocation(src)
		if src_curr in registers:
			f.write("\tmovl " + src_curr + ", " + findRegOrMemoryLocation(dest) + "\n")
		else:
			dest_curr = findDest(lineNo, line)
			f.write("\tmovl " + src_curr + ", " + dest_curr + "\n")
			while dest in regDesciptor.values():
				toBeEmptied = findRegLocation(dest)
				regDesciptor[toBeEmptied] = ""
			if dest_curr in registers:
				regDesciptor[dest_curr] = dest

	elif line[0] == ":=" and len(line) == 3:
		# := $t4 &$t2 int+ $t3
		# := *$t4 $t1
		prevLine = irCode[i - 1].strip().split()[2:]
		print("****", prevLine)

		arrOffset = prevLine[-1]
		arrTempName = prevLine[2][1:]
		arrStart = findMemoryLocation(arrTempName)

		if int(arrStart[:-6]) < 0:
			reg = ""
			if "" in regDesciptor.values():
				reg = findRegLocation("")
				regDesciptor[reg] = "occupied"
			else:
				var = regDesciptor["%eax"]
				moveToStack(var)
				regDesciptor["%eax"] = "occupied"
				reg = "%eax"
			f.write("\tmovl $" + arrStart[:-6] + ", " + reg + "\n")
			f.write("\taddl %ebp, " + reg + "\n")
			f.write("\taddl " + findRegOrMemoryLocation(arrOffset) + ", " + reg + "\n")
			# now, reg has the address of the place where we have to put $t1

			src = line[-1]
			srcmemLoc = findRegOrMemoryLocation(src)
			srcreg = ""
			if srcmemLoc in registers:
				srcreg = srcmemLoc
			elif "" in regDesciptor.values():
				srcreg = findRegLocation("")
			else:
				var = regDesciptor["%ebx"]
				moveToStack(var)
				regDesciptor["%ebx"] = "occupied"
				srcreg = "%ebx"
			if srcreg != srcmemLoc:
				f.write("\tmovl " + srcmemLoc + ", " + srcreg + "\n")
			f.write("\tmovl " + srcreg + ", 0(" + reg + ")\n")
			regDesciptor[reg] = ""
			regDesciptor[srcreg] = ""
		else:
			reg = ""
			if "" in regDesciptor.values():
				reg = findRegLocation("")
				regDesciptor[reg] = "occupied"
			else:
				var = regDesciptor["%eax"]
				moveToStack(var)
				regDesciptor["%eax"] = "occupied"
				reg = "%eax"
			f.write("\tmovl " + arrStart + ", " + reg + "\n")
			f.write("\taddl " + findRegOrMemoryLocation(arrOffset) + ", " + reg + "\n")
			# now reg has the address that we have to add the value of $t1 to
			
			src = line[-1]
			srcmemLoc = findRegOrMemoryLocation(src)
			srcreg = ""
			if srcmemLoc in registers:
				srcreg = srcmemLoc
			elif "" in regDesciptor.values():
				srcreg = findRegLocation("")
			else:
				var = regDesciptor["%ebx"]
				moveToStack(var)
				regDesciptor["%ebx"] = "occupied"
				srcreg = "%ebx"
			if srcreg != srcmemLoc:
				f.write("\tmovl " + srcmemLoc + ", " + srcreg + "\n")
			f.write("\tmovl " + srcreg + ", 0(" + reg + ")\n")
			regDesciptor[reg] = ""
			regDesciptor[srcreg] = ""



	elif line[0] == "BEGIN_FUNCTION":
		scopeName = line[1][:-1]
		newScope = Scope(scopeName, 0)

		f.write(scopeName + ":" + "\n")													# 	factorial:
		f.write("\tpush %ebp" + "\n")													#		push %ebp	
		f.write("\tmovl %esp, %ebp" + "\n")												#		mov %ebp, %esp
		f.write("\tsubl $" + str(newScope.sizeOflocalVariables) + ", %esp" + "\n") 		#		sub %esp, $32

		scopeStack.append(newScope)

	elif line[0] == "BEGIN":
		scopeName = line[1]
		distFromEBP = scopeStack[-1].sizeOflocalVariables
		newScope = Scope(scopeName, distFromEBP)
		# print("added scope", newScope.name)

		f.write("\tsubl $" + str(newScope.sizeOflocalVariables) + ", %esp" + "\n")		#		sub %esp, $32

		scopeStack.append(newScope)
		
	elif line[0][:5] == "BEGIN":
		f.write("." + line[0] + "\n")

	elif line[0][:-2] == "ELSE":
		f.write("." + line[0] + "\n")

	elif line[0][:5] == "AFTER":
		f.write("." + line[0] + "\n")

	elif line[0][:3] == "UPD":
		f.write("." + line[0] + "\n")

	elif line[0] == "END":
		for reg in regDesciptor:
			if regDesciptor[reg] == "":
				continue
			if regDesciptor[reg] in scopeStack[-1].addressDescriptor:
				moveToStack(regDesciptor[reg])
				regDesciptor[reg] = ""
		scopeSize = scopeStack[-1].sizeOflocalVariables
		scopeStack.pop()
		f.write("\taddl $" + str(scopeSize) + ", %esp" + "\n")

	elif line[0] == "END_FUNCTION":
		# for reg in regDesciptor:
		# 	if regDesciptor[reg] == "":
		# 		continue
		# 	memLoc = scopeStack[-1].getLocationInStack(regDesciptor[reg])
		# 	f.write("\tmovl " + reg + ", " + memLoc + "\n")
		f.write("\tleave" + "\n")
		f.write("\tret" + "\n")

		regDesciptor = {reg : "" for reg in registers}
		scopeStack.pop()

	elif line[0] == "param":
		# first, save the caller saved registers that are in use
		for reg in regDesciptor:
			if regDesciptor[reg] == "":
				continue
			moveToStack(regDesciptor[reg])
			regDesciptor[reg] = ""

		j = i
		paramStack = []
		while irCode[j].strip().split()[2] == "param":
			parameter = irCode[j].strip().split()[3]
			paramStack.append(parameter)
			j += 1

		paramStack.reverse()
		for param in paramStack:
			if isLiteral(param):
				f.write("\tpush $" + param + "\n")
			elif param[0] == "&":
				print(">>>>param[0] == \"&\"")
				arrStart = findMemoryLocation(param[1:])
				print(arrStart)
				if int(arrStart[:-6]) > 0:
					p = param[1:]
					f.write("\tpush " + findRegOrMemoryLocation(p) + "\n")
				else:
					reg = ""
					if "" in regDesciptor.values():
						reg = findRegLocation("")
						regDesciptor[reg] =  "occupied"
					else:
						var = regDesciptor["%eax"]
						moveToStack(var)
						reg = "%eax"
						regDesciptor["%eax"] = "occupied"
					f.write("\tmovl %ebp, " + reg + "\n")
					f.write("\taddl $" + arrStart[:-6] + ", " + reg + "\n")
					f.write("\tpush " + reg + "\n")
					regDesciptor[reg] = ""
				print(">>>>param[0] == \"&\"\n")
			else:
				f.write("\tpush " + findRegOrMemoryLocation(param) + "\n")

		linesToSkip = j - i - 1

	elif line[0] == "call":
		f.write("\tcall " + line[1][:-1] + "\n")
		sizeOfParams = line[2]
		f.write("\taddl $" + str(sizeOfParams) + ", %esp" + "\n")

	elif line[0] == "refparam":
		# find the size of all the parameters combined. Assuming its 8 rn
		dest = findRegOrMemoryLocation(line[1])
		f.write("\tmovl %eax, " + dest + "\n")
		regDesciptor["%eax"] = line[1]

	elif line[0] == "goto":
		# print(line)
		# print(regDesciptor)
		# [print("!!",s.name) for s in scopeStack]
		for reg in regDesciptor:
			if regDesciptor[reg] == "":
				continue
			moveToStack(regDesciptor[reg])
			regDesciptor[reg] = ""

		f.write("\tjmp ." + line[1] + "\n")

	elif line[0] == "return":
		if len(line) > 1:
			returnVal = line[1]
			if isLiteral(returnVal):
				returnVal = "$" + returnVal
			else:
				returnVal = findRegOrMemoryLocation(returnVal)
			f.write("\tmovl " + returnVal + ", %eax" + "\n")
		f.write("\tleave" + "\n")
		f.write("\tret" + "\n")

	elif line[0] == "if":
		# f.write("//aa gya if\n")
		# 2: if $t1 < $t5 goto 5

		leftArg  = line[1]
		compop   = line[2]
		rightArg = line[3]

		if isLiteral(leftArg):
			leftArg = "$" + leftArg
		else:
			leftArgLoc  = findRegOrMemoryLocation(leftArg)
			if leftArgLoc not in registers and isLiteral(line[3]):
				mem = leftArgLoc
				if "" in regDesciptor.values():
					leftArgLoc = findRegLocation("")
					regDesciptor[leftArgLoc] = leftArg
				else:
					var = regDesciptor["%eax"]
					moveToStack(var)
					leftArgLoc = "%eax"
					regDesciptor["%eax"] = leftArg
				f.write("\tmovl " + mem + ", " + leftArgLoc + "\n")
			leftArg = leftArgLoc
		if isLiteral(rightArg):
			rightArg = "$" + rightArg
		else:
			rightArgLoc  = findRegOrMemoryLocation(rightArg)
			if rightArgLoc not in registers and (isLiteral(line[1]) or leftArg not in registers):
				mem = rightArgLoc
				if "" in regDesciptor.values():
					rightArgLoc = findRegLocation("")
					regDesciptor[rightArgLoc] = rightArg
				else:
					var = regDesciptor["%eax"]
					if var == line[1]:
						var = regDesciptor["%ebx"]
						moveToStack(var)
						rightArgLoc = "%ebx"
						regDesciptor["%ebx"] = rightArg
					else:
						moveToStack(var)
						rightArgLoc = "%eax"
						regDesciptor["%eax"] = rightArg
				f.write("\tmovl " + mem + ", " + rightArgLoc + "\n")
			rightArg = rightArgLoc

		for reg in regDesciptor:
			if regDesciptor[reg] == "":
				continue

			moveToStack(regDesciptor[reg])

		if isLiteral(rightArg[1:]):
			f.write("\tcmpl " + rightArg + ", " + leftArg + "\n")		# 	cmp eax, ebx
			compop = oppositeOp[compop]
		else:
			f.write("\tcmpl " + leftArg + ", " + rightArg + "\n")		# 	cmp eax, ebx

		elseToken = irCode[i + 4].split()[-1]
		command = commands[compop]
		
		f.write("\t" + command + " ." + elseToken + "\n")			#	jge .ELSE0
		regDesciptor = {reg : "" for reg in registers}
		linesToSkip = 4

	# print(str(regDesciptor))
	# f.write("" + "\n")
f.write(dataSection)