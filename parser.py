import sys
import tree
#Class that defines the action token
class ActionToken:
    def __init__(self, variable, result, realResult):
        self.variable = variable
        self.result = result
        self.realResult = realResult

    def __str__(self):
        return self.variable + "->" + self.result
    def __repr__(self):
        return self.variable + "->" + self.result
def identify_terminals (word):
    if word.startswith("print"):
        return "print"
    elif word.startswith("if"):
        return "if"
    elif word.startswith("else"):
        return "else"
    else:
        return ""
#Function that only does the parsing of the input
def parsing(stack, input):
    while len(stack) > 0:
        print (input + "  " + "".join(stack))
        T = stack[0]
        c = identify_terminals(input)
        if c == "":
            c =input[0]
        if c == "$" == T:
            print("ACCEPTED")
            stack.pop(0)
        elif T in terminals or T == "$":
            if T == c:
                stack.pop(0)
                input = input[len(T):]
            else:
                print("REJECTED")
                break
        elif table.get(T, None) is not None and table[T].get(c, None) is not None:
            result = table[T][c]
            stack.pop(0)
            result = result.replace("print", "#")
            result = result.replace("if", "&")
            result = result.replace("else", "%")
            for character in reversed(result):
                if character == "#":
                    stack.insert(0, "print")
                elif character == "&":
                    stack.insert(0, "if")
                elif character == "%":
                    stack.insert(0, "else")
                else:
                    stack.insert(0, character)
        else:
            print("REJECTED")
            break

#Function that evaluates the input. It assumes that the input is correct
def evaluating (stack, input, expressionStack):
    while len(stack) > 0:
        if "->" in str(stack[0]):
            # Action token
            # Correspinding object
            me = stack[0]
            if me.variable == "V":
                child = expressionStack.pop(0)
                toInsert = tree.ValueExpressionNode(child)
                expressionStack.insert(0, toInsert)
            elif me.variable == "C":
                aNode = expressionStack.pop(0)
                closeBracket = expressionStack.pop(0)
                pNode = expressionStack.pop(0)
                openBracket = expressionStack.pop(0)
                eNode = expressionStack.pop(0)
                ifNode = expressionStack.pop(0)
                toInsert = tree.CtoIf(ifNode, eNode, openBracket, pNode, closeBracket, aNode)
                expressionStack.insert(0, toInsert)

            elif me.variable == "W":
                if me.realResult == "":
                    expressionStack.insert(0, tree.toEpsilon())
                else:
                    wNode = expressionStack.pop(0)
                    tNode = expressionStack.pop(0)
                    toInsert = tree.WtoTW(tNode, wNode)
                    expressionStack.insert(0, toInsert)
            elif me.variable == "R":
                if me.realResult == "":
                    expressionStack.insert(0, tree.toEpsilon())
                else:
                    rNode = expressionStack.pop(0)
                    lNode = expressionStack.pop(0)
                    toInsert = tree.RNode(lNode, rNode)
                    expressionStack.insert(0, toInsert)
            elif me.variable == "B":
                if me.realResult == '"W";':
                    semicolonNode = expressionStack.pop(0)
                    quotesNode2 = expressionStack.pop(0)
                    wNode = expressionStack.pop(0)
                    quotesNode = expressionStack.pop(0)
                    toInsert = tree.BtoW(quotesNode, wNode, quotesNode2, semicolonNode)
                    expressionStack.insert(0, toInsert)
                else:
                    semicolonNode = expressionStack.pop(0)
                    eNode = expressionStack.pop(0)
                    toInsert = tree.BtoE(eNode, semicolonNode)
                    expressionStack.insert(0, toInsert)

            elif me.variable == "L":
                if me.realResult == "C":
                    cNode = expressionStack.pop(0)
                    toInsert = tree.LtoC(cNode)
                    expressionStack.insert(0, toInsert)
                else:
                    bNode = expressionStack.pop(0)
                    printNode = expressionStack.pop(0)
                    toInsert = tree.LtoPrint(printNode, bNode)
                    expressionStack.insert(0, toInsert)

            elif me.variable == "P":
                rNode = expressionStack.pop(0)
                lNode = expressionStack.pop(0)
                toInsert = tree.PNode(lNode, rNode)
                expressionStack.insert(0,toInsert)
            elif me.variable == "T":
                child = expressionStack.pop(0)
                toInsert = tree.TNode(child)
                expressionStack.insert(0, toInsert)
            elif me.variable == "A":
                if me.realResult == "":
                    expressionStack.insert(0, tree.toEpsilon())
                else:
                    rightBracket = expressionStack.pop(0)
                    pNode = expressionStack.pop(0)
                    leftBracket = expressionStack.pop(0)
                    elseNode = expressionStack.pop(0)
                    toInsert = tree.AtoElse(elseNode, leftBracket, pNode, rightBracket)
                    expressionStack.insert(0, toInsert)

            elif me.variable == "O":
                expressionStack.insert(0,  expressionStack.pop(0))
            elif me.variable == "E":
                if me.realResult == "(EOE)":
                    rightBracket = expressionStack.pop(0)
                    lastExpression = expressionStack.pop(0)
                    operation = expressionStack.pop(0)
                    firstExpression = expressionStack.pop(0)
                    leftBracket = expressionStack.pop(0)
                    toInsert = tree.BinaryExpressionNode(leftBracket, firstExpression,
                                                         operation, lastExpression, rightBracket)
                    expressionStack.insert(0, toInsert)
                else:
                    toInsert = tree.ValueExpressionNode(expressionStack.pop(0))
                    expressionStack.insert(0, toInsert)

            stack.pop(0)

        else:
            T = stack[0]
            c = identify_terminals(input)
            if c == "":
                c = input[0]
            if c == "$" == T:
                #ACCEPT
                stack.pop(0)
            elif T in terminals or T == "$":
                if T == c:
                    stack.pop(0)
                    #Pop a terminal, push single tree node
                    expressionStack.insert(0, terminalToObject[T])
                    input = input[len(T):]
                else:
                    print("ERROR")
                    break
            elif table.get(T, None) is not None and table[T].get(c, None) is not None:
                result = table[T][c]
                stack.pop(0)
                #Push Action token onto stack first
                stack.insert(0, ActionToken(T, c, result))
                result = result.replace("print", "#")
                result = result.replace("if", "&")
                result = result.replace("else", "%")
                for character in reversed(result):
                    if character == "#":
                        stack.insert(0, "print")
                    elif character == "&":
                        stack.insert(0, "if")
                    elif character == "%":
                        stack.insert(0, "else")
                    else:
                        stack.insert(0, character)
            else:
                print("ERROR_INVALID_SYMBOL")
                break
    return expressionStack[0].evaluate()

#Terminals
terminals = [";", "print", '"' , "if" , "else", "{" , "}" ,
             "(" , ")", "+", "-", "*", "0", "1", "2", "3", "a", "b", "c", "d"]

#Stack
stack = ["P", "$"]

#Table
table = {"P" : {"print" : "LR", "if" : "LR"},
         "R" : {"print" : "LR", "if" : "LR", "$" : "", "}" : ""},
         "L" : {"print" : "printB", "if" : "C"},
         "B" : {'"' : '"W";', "(" : "E;", "0" : "E;", "1" : "E;", "2" : "E;", "3": "E;"} ,
         "N" : {"print" : "printE"},
         "M" : {"print" : 'print"W"'},
         "W" : {'"' : "", "a" : "TW", "b": "TW", "c": "TW", "d":"TW"},
         "C" : {"if": "ifE{P}A"},
         "A" : {"else": "else{P}" , "$": "", "print": "" , "if": "", "}" : ""},
         "E" : {"(": "(EOE)", "0": "V", "1" : "V", "2" : "V", "3" : "V"},
         "O" : {"+":"+", "-":"-", "*":"*"},
         "V" : {"0": "0", "1":"1", "2":"2", "3":"3"},
         "T" : {"a": "a", "b":"b", "c":"c", "d":"d"}
        }

#Action Token table
terminalToObject = {
    "0": tree.ValueNode(tree.TerminalNode("0")),
    "1": tree.ValueNode(tree.TerminalNode("1")),
    "2": tree.ValueNode(tree.TerminalNode("2")),
    "3": tree.ValueNode(tree.TerminalNode("3")),
    "a" : tree.TNode(tree.TerminalNode("a")),
    "b" : tree.TNode(tree.TerminalNode("b")),
    "c" : tree.TNode(tree.TerminalNode("c")),
    "d" : tree.TNode(tree.TerminalNode("d")),
    "+": tree.OperationNode(tree.TerminalNode("+")),
    "-": tree.OperationNode(tree.TerminalNode("-")),
    "*": tree.OperationNode(tree.TerminalNode("*")),
    "(": tree.TerminalNode("("),
    ")": tree.TerminalNode(")"),
    "print" : tree.TerminalNode("else"),
    "if" : tree.TerminalNode("if"),
    "else" : tree.TerminalNode("else"),
    "{": tree.TerminalNode("{"),
    "}": tree.TerminalNode("}"),
    '"': tree.TerminalNode('"'),
    ";": tree.TerminalNode(";"),
}

file = open(sys.argv[1], "r")
eval = False
if len (sys.argv) == 3:
    if sys.argv[2] == "eval":
        eval = True

#removing whitespace
input = ""
for line in file:
    input += line.replace(" ", "").strip()
input += "$"

#Dectecting invalid symbols
input2 = input
input2 = input2.replace("print", "")
input2 = input2.replace("if", "")
input2 = input2.replace("else", "")
finish = False
for character in input2:
    if character not in terminals and character != "$":
        print("ERROR_INVALID_SYMBOL")
        finish = True
        break

if(finish):
    sys.exit()

if(eval == False):
    parsing(stack, input)
else:
    expressionStack = []
    evaluating(stack, input, expressionStack)