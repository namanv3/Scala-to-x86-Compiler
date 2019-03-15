import sys
import operator
import reserved_words as R

global_scope_no = 0
class SymbolTable:

    def __init__(self):
        self.SymbolTable = {
                "main" : {
                            "scope_name" : "main",
                            "variables" : {},
                            "functions" :{},
                            "classes" :{},
                            "type" : "main",
                            "parent" : "None",
                            "offset" : 0,
                            "temp"  : 0,
                        }
                    }
        self.curr_scope = "main"

    def initialiseTable(self):
        for w in R.keywords:
            self.SymbolTable[self.curr_scope]["variables"][w.lower()] = {
                    "type" : "KEYWORD"
            }
            self.SymbolTable[self.curr_scope]["variables"][w.upper()] = {
                    "type" : "KEYWORD"
            }
        for w in R.data_types:
            self.SymbolTable[self.curr_scope]["variables"][w.upper()] = {
                    "type" : "KEYWORD"
            }
            self.SymbolTable[self.curr_scope]["variables"][w.lower()] = {
                    "type" : "KEYWORD"
            }

    def addVar(self, idVal, idType, lineno, idSize = 4, typeArray = None, objSize = None):
        scope = self.getScope("variables", idVal)
        if scope != self.curr_scope:
            self.SymbolTable[self.curr_scope]["variables"][idVal] = {
                "type" : idType,
                "size" : idSize,
            }
            if idType == "Array":
                size = reduce(operator.mul, self.SymbolTable[scope]["variables"][idVal]["size"], 1)
                w = self.getWidth(typeArray)
                self.SymbolTable[self.curr_scope]["offset"] += size * w
                self.SymbolTable[self.curr_scope]["variables"][idVal]["typeArray"] = typeArray
            elif objSize is not None:
                self.SymbolTable[self.curr_scope]["offset"] += objSize
            else:
                self.SymbolTable[self.curr_scope]["offset"] += idSize

            self.SymbolTable[self.curr_scope]["variables"][idVal]["offset"] = self.SymbolTable[self.curr_scope]["offset"]
        else:
            sys.exit("ERROR on line "+lineno+" : Variable "+idVal+"already declared in this scope")


    def addFunc(self, funcVal, lineno, returnType = None, def_c = 0):
        scope = self.getScope("functions", funcVal)
        if scope == self.curr_scope:
            if  self.SymbolTable[scope]["functions"][funcVal][fdef] == 1:
                sys.exit("ERROR on line "+lineno+" : Function "+funcVal+"already declared in this scope")
            else:
                if def_c == 0:
                    sys.exit("ERROR on line "+lineno+" : Function "+funcVal+"already declared in this scope")

        self.SymbolTable[funcVal] = {
                "name" : funcVal,
                "type" : "functions",
                "rType" : returnType,
                "variables" : {},
                "functions" : {},
                "parent" : self.curr_scope,
                "offset" : 4,
                "paramoffset" : -8,
                "temp"  : 0,
                }
        if def_c:                                                                 # adding entry corresponding to function body
            self.SymbolTable[self.curr_scope]["functions"][funcVal] = {
                    "fname" : funcVal,
                    "fdef" : 1,
                    }
            self.curr_scope = funcVal
            self.initialiseTable()
        else:                                                                   # adding entry corresponding to function declaration
            self.SymbolTable[self.curr_scope]["functions"][funcVal] = {
                    "fname" : funcVal,
                    "fdef" : 0,
                    }


    def addParamVar(self, idVal, idType,  lineno, idSize = 4, typeArray = None):
        scope = self.getScope("variables", idVal)
        if scope != self.curr_scope:
            self.SymbolTable[self.curr_scope]["variables"][idVal] = {
                    "type" : idType,
                    "size" : idSize,
                    }
            if idType == "Array":
                size = 4
                self.SymbolTable[self.curr_scope]["variables"][idVal]["typeArray"] = typeArray
                self.SymbolTable[self.curr_scope]["paramoffset"] -= size
                self.SymbolTable[self.curr_scope]["variables"][idVal]["offset"] = self.SymbolTable[self.curr_scope]["paramoffset"]
            else:
                self.SymbolTable[self.curr_scope]["paramoffset"] -= idSize
                self.SymbolTable[self.curr_scope]["variables"][idVal]["offset"] = self.SymbolTable[self.curr_scope]["paramoffset"]
        else:
            sys.exit("ERROR on line "+lineno+" : Variable "+idVal+"already declared in this scope")


    def addClass(self, classVal, parent="main"):
        self.SymbolTable[classVal]={
                "name" : classVal,
                "type" : "classes",
                "variables" : {},
                "functions" : {},
                "rType" : "undefined",
                "parent" : parent,
                "offset" : 0,
                "paramoffset": -8,
                "temp"  : 0,
                }
        self.curr_scope = classVal
        self.initialiseTable()

    def addObject(self, objVal, parent="main"):
        self.SymbolTable[objVal]={
                "name" : objVal,
                "type" : "OBJECT",
                "variables" : {},
                "functions" : {},
                "parent" : parent,
                "offset" : 0,
                "paramoffset": -8,
                "temp"  : 0,
                }
        self.curr_scope = objVal
        self.initialiseTable()


    def getScope(self, key, idVal):
        scope = self.curr_scope
        while scope != "None":
            if idVal in self.SymbolTable[scope][key]:
                return scope
            scope = self.SymbolTable[scope]["parent"]
        return scope

    def startScope(self):
        global global_scope_no
        scope = "scope_" + str(global_scope_no)
        global_scope_no += 1
        self.SymbolTable[scope] = {
                "name" : scope,
                "functions" : {},
                "variables" : {},
                "type" : "scope",
                "parent" : self.curr_scope,
                "offset" : self.SymbolTable[self.curr_scope]["offset"],
                "temp"  : 0,
                }
        self.curr_scope = scope
        self.initialiseTable()

    def endScope(self):
        self.curr_scope = self.SymbolTable[self.curr_scope]["parent"]

    def newtemp(self):
        self.SymbolTable[self.curr_scope]["temp"] += 1
        tempvar = "$t" + str(self.SymbolTable[self.curr_scope]["temp"])
        return tempvar

    def addtemptoST(self, idVal, idType, idSize):
        self.SymbolTable[self.curr_scope]["variables"][idVal] = {
                "type" : idType,
                "size" : idSize,
            }

    def getType(self, idVal, key = "variables"):
        scope = self.getScope(key, idVal)
        if scope != "None":
            return  self.SymbolTable[scope]["variables"][idVal]['type']
        else:
            return ""

    def getWidth(self,idType):
        if idType == "BOOL": return 1
        elif idType == "CHAR": return 1
        elif idType == "INT": return 4
        elif idType == "FLOAT": return 8
