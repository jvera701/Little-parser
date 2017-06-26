#All the node classes are here
class PNode():
    def __init__(self, lNode, rNode):
        self.lNode = lNode
        self.rNode = rNode
    def evaluate(self):
        self.lNode.evaluate()
        self.rNode.evaluate()
    def __str__(self):
        return str(self.lNode) + str(self.rNode)
    __repr__ = __str__

class RNode():
    def __init__(self, lNode, rNode):
        self.lNode = lNode
        self.rNode = rNode
    def evaluate(self):
       self.lNode.evaluate()
       self.rNode.evaluate()
    def __str__(self):
        return str(self.lNode) + str(self.rNode)
    __repr__ = __str__

class TerminalNode():
    """This is a terminal symbol"""
    def __init__(self, element):
        self.element = element
    def evaluate(self):
        """This simply evaluates as the contained string (i.e. the terminal)"""
        return self.element
    def __str__(self):
        return self.element
    __repr__ = __str__

class OperationNode():
    """This corresponds to the rules O -> + | - | *"""
    def __init__(self, child):
        self.child = child
    def evaluate(self):
        return self.child.evaluate()
    def __str__(self):
        return str(self.child)
    __repr__ = __str__

class ValueNode():
    """This corresponds to the rules V -> 0 | 1 | 2| 3"""
    def __init__(self, child):
        self.child = child
    def evaluate(self):
        return int(self.child.evaluate())
    def __str__(self):
        return str(self.child)
    __repr__ = __str__

class TNode():
    def __init__(self, child):
        self.child = child
    def evaluate(self):
        return self.child.evaluate()
    def __str__(self):
        return str(self.child)
    __repr__ = __str__

class ValueExpressionNode():
    """This corresponds to the rule E -> V"""
    def __init__(self, child):
        self.child = child
    def evaluate(self):
        return self.child.evaluate()
    def __str__(self):
        return str(self.child)
    __repr__ = __str__

class RToLRNode():
    def __init__(self, lNode, rNode):
        self.lNode = lNode
        self.rNode = rNode

    def evaluate(self):
        self.lNode.evaluate()
        self.rNode.evaluate()
        return
    def __str__(self):
        return "LNode: " + str(self.lNode) + "RNode" + str(self.rNode)

class toEpsilon():
    def __init(self, child):
        self.child = TerminalNode("")
    def evaluate(self):
        return ""
    def __str__(self):
       return ""
    __repr__ = __str__

class LtoPrint():
    def __init__(self, printNode, bNode):
        self.bNode = bNode
        self.printNode = printNode
    def evaluate(self):
        print(self.bNode.evaluate())
    def __str__(self):
        return "print:" + str(self.bNode)
    __repr__ = __str__

class LtoC():
    def __init__(self, cNode):
        self.cNode = cNode
    def evaluate(self):
        return self.cNode.evaluate()
    def __str__(self):
        return str(self.cNode)
    __repr__ = __str__

class BinaryExpressionNode():
    """This corresponds to the rule E -> (EOE)"""
    def __init__(self, left_bracket, e1, operation, e2, right_bracket):
        self.left_bracket = left_bracket
        self.e1 = e1
        self.operation = operation
        self.e2 = e2
        self.right_bracket = right_bracket
    def evaluate(self):
        #apply the appropriate operation to the two evaluated expressions
        operation = self.operation.evaluate()
        lhs = self.e1.evaluate()
        rhs = self.e2.evaluate()
        if operation == '+':
            return lhs + rhs
        elif operation == '*':
            return lhs * rhs
        elif operation == '-':
            return lhs - rhs

    def me(self):
        return "BinaryExpressionNode"

    def __str__(self):
        return "{}{}{}{}{}".format(str(self.left_bracket), str(self.e1), str(self.operation), str(self.e2), str(self.right_bracket))
    __repr__ = __str__

class CtoIf():
    def __init__(self, ifNode, eNode, openBracket, pNode, closeBracket, aNode):
        self.ifNode = ifNode
        self.pNode = pNode
        self.eNode = eNode
        self.aNode = aNode
        self.openBracket = openBracket
        self.closeBracket = closeBracket

    def evaluate(self):
        if self.eNode.evaluate() != 0:
            self.pNode.evaluate()
        else:
            self.aNode.evaluate()

    def __str__(self):
        return str(self.eNode) + str(self.openBracket) + str(self.pNode) + str(self.closeBracket) + str(self.aNode)
    __repr__ = __str__

class AtoElse():
    def __init__(self, elseNode, leftBracket, pNode, rightBracket):
        self.elseNode = elseNode
        self.leftBracket = leftBracket
        self.pNode = pNode
        self.rightBacket = rightBracket
    def __str__(self):
        return str(self.elseNode) + str(self.leftBracket) + str(self.pNode) + str(self.rightBacket)
    def evaluate(self):
        return self.pNode.evaluate()
    __repr__ = __str__

class BtoE ():
    def __init__(self, eNode, semicolonNode):
        self.eNode = eNode
        self.semicolonNode = semicolonNode
    def evaluate(self):
        return self.eNode.evaluate()

    def __str__(self):
        return str(self.eNode) + str(self.semicolonNode)
    __repr__ = __str__

class BtoW ():
    def __init__(self, quotesNode, wNode, quotesNode2, semicolonNode):
        self.quotesNode = quotesNode
        self.wNode = wNode
        self.quotesNode2 = quotesNode2
        self.semicolonNode = semicolonNode

    def evaluate(self):
        return self.wNode.evaluate()

    def __str__(self):
        return str(self.quotesNode) + str(self.wNode) + str(self.quotesNode2) + str(self.semicolonNode)

    __repr__ = __str__

class WtoTW():
    def __init__(self, tNode, wNode):
        self.tNode = tNode
        self.wNode = wNode

    def evaluate(self):
        return str(self.tNode) + str(self.wNode)

    def __str__(self):
        return str(self.tNode) + str(self.wNode)

    __repr__ = __str__