import sys
import operator
import reserved_words as R
import json

global_scope_no = 0
scopelist = []
global_temp_count = 0
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

    def Linking(self):
        # Linking
        self.addFunc("printf", 0, ["VOID", "VOID"], 0)
        self.endScope()
        self.addFunc("malloc", 0, ["VOID", "VOID"], 0)
        self.endScope()
        self.addFunc("scanf", 0, ["VOID", "VOID"], 0)
        self.endScope()


    def addVar(self, idVal, idType, lineno, idSize, idtempName, typeArray = None, objSize = None, Arraysize = None):
        scope = self.getScope("variables", idVal)
        if scope != self.curr_scope:
            self.SymbolTable[self.curr_scope]["variables"][idVal] = {
                "type" : idType,
                "size" : idSize,
                "Arraysize" : 0,
                'tempName' : idtempName
            }
            if idType[0] == "ARRAY":
                if Arraysize == None:
                    self.SymbolTable[self.curr_scope]["offset"] += 4
                else:
                    self.SymbolTable[self.curr_scope]["variables"][idVal]["Arraysize"] = Arraysize
                    if not any(not isinstance(y,(int)) for y in Arraysize):
                        self.SymbolTable[self.curr_scope]["offset"] += 4 * eval("*".join(str(item) for item in Arraysize))
                    # Arrays defined using 'new' go to heap
                    self.SymbolTable[self.curr_scope]["variables"][idVal]["size"] = self.SymbolTable[self.curr_scope]["offset"]

                self.SymbolTable[self.curr_scope]["variables"][idVal]["typeArray"] = typeArray
            elif objSize is not None:
                # self.SymbolTable[self.curr_scope]["offset"] += objSize
                self.SymbolTable[self.curr_scope]["offset"] += 4
            else:
                self.SymbolTable[self.curr_scope]["offset"] += idSize

            self.SymbolTable[self.curr_scope]["variables"][idVal]["offset"] = self.SymbolTable[self.curr_scope]["offset"]
        else:
            sys.exit("ERROR on line "+ str(lineno) +" : Variable "+ str(idVal) +"already declared in this scope")


    def addFuncParamVar(self, idVal, idType, lineno, idSize, idtempName, typeArray = None, objSize = None, Arraysize = None):
        scope = self.getScope("variables", idVal)
        if scope != self.curr_scope:
            self.SymbolTable[self.curr_scope]["variables"][idVal] = {
                "type" : idType,
                "size" : idSize,
                "Arraysize" : 0,
                'tempName' : idtempName
            }
            if idType[0] == "ARRAY":
                self.SymbolTable[self.curr_scope]["offset"] += 4
            elif objSize is not None:
                # self.SymbolTable[self.curr_scope]["offset"] += objSize
                self.SymbolTable[self.curr_scope]["offset"] += 4
            else:
                self.SymbolTable[self.curr_scope]["offset"] += idSize

            self.SymbolTable[self.curr_scope]["variables"][idVal]["offset"] = self.SymbolTable[self.curr_scope]["offset"]
        else:
            sys.exit("ERROR on line "+ str(lineno) +" : Variable "+ str(idVal) +"already declared in this scope")

        self.SymbolTable[self.curr_scope]["params"][idVal] = self.SymbolTable[self.curr_scope]["variables"][idVal]


    def addFunc(self, funcVal, lineno, returnType = None, def_c = 0):
        scope = self.getScope("functions", funcVal)
        if scope == self.curr_scope and self.curr_scope != "none":
            if self.SymbolTable[funcVal]["fdef"] == 1:
                sys.exit("ERROR on line "+str(lineno)+" : Function "+str(funcVal)+" already declared in this scope")
            else:
                if def_c == 0:
                    sys.exit("ERROR on line "+str(lineno)+" : Function "+str(funcVal)+" already declared in this scope")

        self.SymbolTable[funcVal] = {
                "name" : funcVal,
                "type" : "functions",
                "rType" : returnType,
                "variables" : {},
                "functions" : {},
                "params" : {},
                "parent" : self.curr_scope,
                "offset" : 4,
                "paramoffset" : -8,
                "temp"  : 0,
                "fdef" : 0
                }
        self.SymbolTable[self.curr_scope]["functions"][funcVal] = {
                "fname" : funcVal,
                "rType" : returnType
                }

        self.curr_scope = funcVal
        if def_c == 1:
            self.SymbolTable[self.curr_scope]["fdef"] = 1
        global scopelist
        scopelist.append(funcVal)


    def addParamVar(self, idVal, idType,  lineno, idSize, idtempName, typeArray = None):
        scope = self.getScope("variables", idVal)
        if scope != self.curr_scope:
            self.SymbolTable[self.curr_scope]["variables"][idVal] = {
                    "type" : idType,
                    "size" : idSize,
                    "tempName" : idtempName
                    }
            if idType[0] == "Array":
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
                "parent" : parent,
                "offset" : 0,
                "paramoffset": -8,
                "temp"  : 0,
                }
        self.curr_scope = classVal
        global scopelist
        scopelist.append(classVal)
        self.Linking()

    def addObject(self, objVal, parent="none"):
        self.SymbolTable[objVal]={
                "name" : objVal,
                "type" : "objects",
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
        self.Linking()


    def getScope(self, key, idVal):
        scope = self.curr_scope
        while scope != "none":
            print(scope)
            if idVal in self.SymbolTable[scope][key].keys():
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
        global global_temp_count
        tempvar = "$t" + str(global_temp_count)
        global_temp_count += 1
        return tempvar

    def addtemptoST(self, idVal, idType, idSize):
        self.SymbolTable[self.curr_scope]["variables"][idVal] = {
                "type" : idType,
                "size" : idSize,
            }

    def getType(self, idVal, key = "variables"):
        scope = self.getScope(key, idVal)
        if scope != "none":
            if key == "variables":
                return  self.SymbolTable[scope][key][idVal]['type']
            elif key == "functions":
                return self.SymbolTable[idVal]['rType']
        else:
            return ""
            # sys.exit('Identifier \'' + str(idVal) + '\' not declared in scope')

    def getWidth(self,idType):
        # if idType == "BOOLEAN": return 1
        # elif idType == "CHAR": return 1
        # elif idType == "INT": return 4
        # elif idType == "FLOAT": return 8
        return 4

    def printSymbolTable(self, filename):
        f = open(filename, "w+")
        global scopelist
        for s in scopelist:
            f.write(json.dumps(self.SymbolTable[s], indent=4))
        f.close()
