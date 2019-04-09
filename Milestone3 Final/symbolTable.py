import sys
import operator
import reserved_words as R
import json

global_scope_no = 0
scopelist = []
class SymbolTable:

    def __init__(self):
        self.SymbolTable = {
                "none" : {
                            "scope_name" : "none",
                            "variables" : {},
                            "functions" :{},
                            "classes" :{},
                            "type" : "none",
                            "parent" : "None",
                            "offset" : 0,
                            "temp"  : 0,
                        }
                    }
        self.curr_scope = "none"
        global scopelist
        scopelist.append("none")

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
            if  self.SymbolTable[scope]["functions"][funcVal]["fdef"] == 1:
                sys.exit("ERROR on line "+str(lineno)+" : Function "+str(funcVal)+"already declared in this scope")
            else:
                if def_c == 0:
                    sys.exit("ERROR on line "+str(lineno)+" : Function "+str(funcVal)+"already declared in this scope")

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
            global scopelist
            scopelist.append(funcVal)
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


    def addClass(self, classVal, parent="none"):
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
        global scopelist
        scopelist.append(classVal)

    def addObject(self, objVal, parent="none"):
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
        global scopelist
        scopelist.append(objVal)


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
        global scopelist
        scopelist.append(scope)

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
            return  self.SymbolTable[scope][key][idVal]['type']
        else:
            return ""

    def getWidth(self,idType):
        if idType == "BOOL": return 1
        elif idType == "CHAR": return 1
        elif idType == "INT": return 4
        elif idType == "FLOAT": return 8

    def printSymbolTable(self, filename):
        f = open(filename, "w+")
        global scopelist
        for s in scopelist:
            # print(self.SymbolTable[s])
            f.write(json.dumps(self.SymbolTable[s], indent=4))

            # f.write("SCOPE NAME : " + self.SymbolTable[s]['parent'] + "." + s + ":\n")

            # if 'variables' in self.SymbolTable[s]:
            #     f.write("-> Variables : \n")
            #     for v in self.SymbolTable[s]['variables']:
            #         f.write("  - Var name : " + str(v) + "\n")
            #         f.write("    Type : " + str(self.SymbolTable[s]["variables"][v]['type']))
            #         # if self.SymbolTable[s]["variables"][v]['type'] == 'ARRAY':
            #         #     f.write("["+ self.SymbolTable[s]["variables"][v]['typeArray'] +"]")
            #         f.write("\n")
            #         f.write("    Size : " + str(self.SymbolTable[s]["variables"][v]['size']) + "\n")

            # if 'functions' in self.SymbolTable[s]:
            #     f.write("-> Functions : \n")
            #     for v in self.SymbolTable[s]['functions']:
            #         f.write("  - Func name : " + str(v) + "\n")
            #         f.write("    Return type : " + str(self.SymbolTable[v]['rType']) + "\n")

            # if 'classes' in self.SymbolTable[s]:
            #     f.write("-> Classes : \n")
            #     for v in self.SymbolTable[s]['classes']:
            #         f.write("  - Class name : " + str(v) + "\n")
            # f.write("\n-----------------------------------------------------\n\n")

        f.close()
