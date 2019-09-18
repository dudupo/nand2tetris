class Node():
    def __init__(self, streamer, hist=0):
        self.streamer = streamer
        self.children = []
        self.hist = hist

    def generate(self):
        ret = ""
        for child in self.children:
            # ~patch~
            if child != None:
                ret += child.generate()
        return ret

    def updatehist(self, _add):
        self.hist += _add
        for child in self.children:
            # ~patch~
            if child != None:
                child.updatehist(_add)

    def histline(self, line, addition=0):
        return (self.hist + addition) * "\t" + line + "\n"
class IdentifierNode(Node):
    def __init__(self, streamer, hist=0):
        super(IdentifierNode, self).__init__(streamer, hist)
        self.identifier = streamer.read()

    def generate(self):
        return self.histline("<identifier> {0} </identifier>".format(self.identifier))
class abcArgcClosure(Node):
    def __init__(self, streamer, lcloser='(', rcloser=")", hist=0):
        super(abcArgcClosure, self).__init__(streamer, hist = hist)
        self.lcloser = lcloser
        self.rcloser = rcloser

    def collect(self):

        _token = None
        while self.streamer.top() != self.rcloser :
            node = nextToken(self.streamer, hist=self.hist+1)
            if node != None :
                self.children.append( node )
class ArgcClosure(abcArgcClosure):
    def __init__(self, streamer, lcloser='(', rcloser=")", hist=0):
        super(ArgcClosure, self).__init__(streamer, lcloser='(', rcloser=")", hist = hist)
        self.lcloser = lcloser
        self.rcloser = rcloser

    def collect(self):
        self.children.append( nextToken(self.streamer, hist=self.hist+1) )
        super().collect()
        self.children.append( nextToken(self.streamer, hist=self.hist+1) )
class ArgcClosureStatements(abcArgcClosure):
    def __init__(self, streamer, lcloser='{', rcloser="}", hist=0):
        super(ArgcClosureStatements, self).__init__(streamer, lcloser='{', rcloser="}", hist=hist)
        #self.updatehist(1)

    def generate(self):
        return self.histline("<statements>") +\
         super().generate() + self.histline("</statements>")
class ClassNode(ArgcClosure):
    def __init__(self, streamer, hist=0):
        super(ClassNode, self).__init__(streamer, lcloser='{', rcloser="}", hist=hist)
        self.children.append( IdentifierNode(streamer, hist=self.hist + 1))

        super().collect()


    def generate(self):
        return self.histline("<class>") + \
                    self.histline("<keyword> class </keyword>", addition=1) + super().generate() + \
                    self.histline("</class>")
def createVarNode(vartype, _keyword):
    class VarNode(Node):
        def __init__(self, streamer, hist=0):
            super(VarNode, self).__init__(streamer, hist=hist)
            self.children.append( createKeyword(_keyword)( streamer, hist=hist+1) )
            self.children.append( Token_or_Identifier(streamer, hist=hist+1) ) # int
            self.children.append( Token_or_Identifier(streamer, hist=hist+1 ))

            while streamer.top() == ",":
                self.children.append( nextToken(streamer, hist=hist+1) )
                self.children.append( IdentifierNode(streamer, hist=hist+1 ))

            self.children.append( nextToken(streamer, hist=hist+1) )


        def generate(self):
            return self.histline("<{0}>".format(vartype)) +\
                        super().generate() + self.histline("</{0}>".format(vartype))

    return VarNode
class Term(Node):
    def __init__(self, streamer, node, minus=False, hist=0):
        super(Term, self).__init__(streamer, hist=hist)
        node.updatehist(1)
        self.children.append(node)
        if streamer.top() == ".":
            while streamer.top() == ".":
                self.children.append(nextToken(streamer, hist=hist+1))
                self.children.append(IdentifierNode(streamer, hist=hist+1))
            self.children.append(ExpressionList( streamer, hist=hist+1))
        elif streamer.top() == "[":
            self.children.append(Expression(streamer, lcloser="[", rcloser="]", hist=hist+1))
        if minus :
            self.children.append(\
             Term(streamer, IdentifierNode(streamer, hist=hist+1), hist=hist+1))
    def generate(self):
        return self.histline("<term>") +\
                    super().generate() + self.histline("</term>")
class abcExpression(ArgcClosure):
    def __init__(self, streamer, lcloser='(', rcloser=")",  hist=0):
        super(abcExpression, self).__init__(streamer, lcloser=lcloser, rcloser=rcloser, hist=hist)
        self.collect()

    def collect(self):

        def get_node(perent):
            _char = self.streamer.top()
            node = None
            if _char == "(" :
                node = Expression(perent.streamer, lcloser='(', rcloser=')', hist=perent.hist+1)
            elif check_int(_char) :
                node = IntConstantNode(perent.streamer, hist=perent.hist+1)
            else:
                node = Token_or_Identifier(perent.streamer, hist=perent.hist+1)
            if node != None and ( _char not in operator or _char == "\"") :
                return Term(perent.streamer,node, hist=perent.hist+1)
            elif len(perent.children) == 0 and _char in "-~":
                ret = Term(perent.streamer,node, hist=perent.hist+1)
                ret.children.append( get_node(ret) )
                return ret
            else :
                return node

        _token = None
        while self.notclosed():
            self.children.append( get_node(self) )
    def generate(self):
        return self.histline("<expression>") + \
                    super().generate() + \
                    self.histline("</expression>")

    def notclosed(self):
        return self.streamer.top() != self.rcloser
# decorator
class Expression(ArgcClosure):
    def __init__(self, streamer, lcloser='(', rcloser=")",  hist=0):
        super(Expression, self).__init__(streamer, lcloser=lcloser, rcloser=rcloser, hist=hist)
        #self.expression = abcExpression(streamer, lcloser='(', rcloser=")",   hist=hist)
        self.preExp = nextToken(self.streamer, hist=self.hist+1)
        self.expression = abcExpression(streamer, lcloser=lcloser, rcloser=rcloser,   hist=hist)
        self.endExp = nextToken(self.streamer, hist=self.hist+1)
        #self.collect()

        # self.preExp = self.children.pop(0) # =
        # self.endExp = self.children.pop(-1)

        # for debuging propuse :
        if self.preExp is None:
            self.preExp = Node(streamer)

        self.preExp.hist -= 1

        if self.endExp is None:
            self.endExp = Node(streamer)

        self.endExp.hist -= 1

    def collect(self):
        self.expression.collect()


    def generate(self):
        return self.preExp.generate() +\
                    self.expression.generate() + self.endExp.generate()

    def updatehist(self, _add):
        super().updatehist(_add)
        self.expression.updatehist(_add)
        self.preExp.updatehist(_add)
        self.endExp.updatehist(_add)
class ExpressionItem(abcExpression):
    def __init__(self, streamer, lcloser='(', rcloser=")",  hist=0):
        super(ExpressionItem, self).__init__(streamer, lcloser=lcloser, rcloser=rcloser, hist=hist)

    def notclosed(self):
        return self.streamer.top() != self.rcloser and self.streamer.top() != ','
class ExpressionList(Node):
    def __init__(self, streamer, hist=0):
        super(ExpressionList, self).__init__(streamer, hist=hist)

        self.preExp = nextToken(streamer,hist=hist)
        if streamer.top() != ")" :
            self.children.append( ExpressionItem(streamer, lcloser='(', rcloser=")",  hist=hist+1) )
        while streamer.top() == "," :
            self.children.append( nextToken(streamer,hist=hist+1))
            self.children.append( ExpressionItem(streamer, lcloser='(', rcloser=")",  hist=hist+1) )
        self.endExp = nextToken(streamer,hist=hist)

        if self.preExp is None:
            self.preExp = Node(streamer)

        # self.preExp.hist -= 1
        #
        if self.endExp is None:
            self.endExp = Node(streamer)

        # self.endExp.hist -= 1

    def generate(self):
        return self.preExp.generate() +\
                    self.histline("<expressionList>") + \
                    super().generate() + \
                    self.histline("</expressionList>") + \
                    self.endExp.generate()

    def updatehist(self, _add):
        super().updatehist(_add)
        self.preExp.updatehist(_add)
        self.endExp.updatehist(_add)
class LetNode(Node):
    def __init__(self, streamer, hist=0):
        super(LetNode, self).__init__(streamer, hist=hist)
        self.children.append( createKeyword("let")( streamer, hist=hist+1) )
        self.children.append( IdentifierNode(streamer, hist=hist+1 ))
        if streamer.top() == "[":
            self.children.append(  Expression(streamer, lcloser = "[", rcloser = "]", hist=hist+1 ) )
        self.children.append(  Expression(streamer, lcloser = "=", rcloser = ";", hist=hist+1 ) )

    def generate(self):
        return self.histline("<letStatement>") + \
            super().generate() + \
            self.histline("</letStatement>")
class doNode(Node):
    def __init__(self, streamer, hist=0):
        super(doNode, self).__init__(streamer, hist=hist)
        self.children.append( createKeyword("do")( streamer, hist=hist+1))

        self.children.append( IdentifierNode(streamer, hist=hist+1) )
        while streamer.top() == ".":
            self.children.append( nextToken(streamer, hist=hist+1) )
            self.children.append(   IdentifierNode(streamer, hist=hist+1) )
        #self.children.append( nextToken(streamer, hist=hist+1) )
        self.children.append( ExpressionList(streamer, hist=hist+1) )
        self.children.append( nextToken(streamer, hist=hist+1) )
    def generate(self):
        return self.histline("<doStatement>") + \
            super().generate() + \
            self.histline("</doStatement>")
class ReturnNode(Node):
    def __init__(self, streamer, hist=0):
        super(ReturnNode, self).__init__(streamer, hist)
        self.children.append( createKeyword("return")( streamer, hist=hist+1)  )
        if streamer.top() != ";":
            self.children.append( abcExpression(streamer, rcloser=";", hist=hist+1) )
        self.children.append( nextToken(streamer , hist=hist+1) )

    def generate(self):
        return self.histline("<returnStatement>") + \
            super().generate() + \
            self.histline("</returnStatement>")
class StringConstantNode(Node):
    def __init__(self, streamer, hist=0):
        super(StringConstantNode, self).__init__(streamer, hist)
        self.value = ""
        #streamer.read()
        while streamer.top() != "\"":
            self.value += streamer.read() +" "
        streamer.read()

    def generate(self):
        return self.histline("<stringConstant> {0} </stringConstant>".format(self.value))
class IntConstantNode(Node):
    def __init__(self, streamer, hist=0):
        super(IntConstantNode, self).__init__(streamer, hist)
        self.value =  int(streamer.read())

    def generate(self):
        return self.histline("<integerConstant> {0} </integerConstant>".format(self.value))
class parameterListNode(Node):
    def __init__(self, streamer, hist=0):
        super(parameterListNode, self).__init__( streamer, hist=hist )

        self.preExp = nextToken( streamer, hist=hist )
        while streamer.top() != ")" :
            self.children.append( Token_or_Identifier(streamer, hist=hist+1) )
        self.endExp = nextToken( streamer, hist=hist )

    def generate(self):
        return self.preExp.generate() +\
            self.histline("<parameterList>") + \
            super().generate() + \
            self.histline("</parameterList>") +\
            self.endExp.generate()
class BodySubRotNode(ArgcClosureStatements):
    def __init__(self, streamer, hist=0):
        super(BodySubRotNode, self).__init__( streamer, lcloser='{', rcloser="}", hist=hist)
        super().collect()
class Warper(Node):
    def __init__(self, streamer, nodes, _tag, hist=0):
        super(Warper, self).__init__(streamer, hist)
        self.children = nodes
        self.updatehist(1)
        self._tag = _tag

    def generate(self):
        return self.histline("<{0}>".format(self._tag)) + \
             super().generate() +  self.histline("</{0}>".format(self._tag))
def createSubRot(_keyword):
    class SubRotNode(Node):
        def __init__(self, streamer, hist=0):
            super(SubRotNode, self).__init__( streamer, hist=hist)
            self.children.append(createKeyword(_keyword)(streamer, hist=hist+1))
            self.children.append( Token_or_Identifier(streamer, hist=hist+1) )
            self.children.append( Token_or_Identifier(streamer, hist=hist+1) )
            self.children.append( parameterListNode(streamer, hist=hist+1) )

            nodes = [ ]
            nodes.append( Token_or_Identifier(streamer, hist=hist+1) )
            while streamer.top() == "var":
                nodes.append( Token_or_Identifier(streamer, hist=hist+1) )
            nodes.append( BodySubRotNode(streamer, hist=hist+1) )
            nodes.append( Token_or_Identifier(streamer, hist=hist+1) )
            self.children.append( Warper( streamer, nodes, "subroutineBody", hist=hist+1) )


        def generate(self):
            return self.histline("<subroutineDec>") +\
                super().generate() +\
                self.histline("</subroutineDec>")

    return SubRotNode
def createCondition(_keyword, _statement):
    class conditionNode(Node):
        def __init__(self, streamer, hist=0):
            super(conditionNode, self).__init__(streamer, hist=hist)
            self.children.append(Expression(streamer, hist=hist+1))

            def create_block():
                self.children.append( Token_or_Identifier(streamer, hist=hist+1) )
                node = ArgcClosureStatements(streamer, lcloser='{', rcloser="}",hist=hist+1)
                node.collect()
                self.children.append(node)
                self.children.append( Token_or_Identifier(streamer, hist=hist+1) )

            create_block()
            if streamer.top() == "else" and _keyword == "if" :
                self.children.append( Token_or_Identifier(streamer, hist=hist+1) )
                create_block()

        def generate(self):
            return self.histline("<{0}>".format(_statement)) + \
                        self.histline("<keyword> {0} </keyword>".format(_keyword), addition=1) + super().generate() + \
                        self.histline("</{0}>".format(_statement))

    return conditionNode
def createSymbol(_symbol):
    class SymbolNode(Node):

        def __init__(self, streamer, hist=0):
            super(SymbolNode, self).__init__(streamer, hist)

        def generate(self):
            return self.histline("<symbol> {0} </symbol>".format(_symbol))

    return SymbolNode
def createKeyword(keyword):
    class KeywordNode(Node):
        def __init__(self, streamer, hist=0):
            super(KeywordNode, self).__init__(streamer, hist)

        def generate(self):
            return self.histline("<keyword> {0} </keyword>".format(keyword))

    return KeywordNode
def Token_or_Identifier(streamer, hist=0):
    if streamer.top() in tokens:
        return nextToken(streamer, hist=hist)
    else:
        return IdentifierNode(streamer, hist=hist)
def nextToken(streamer, hist=0):
    _token = streamer.read()

    if _token in tokens:
        return tokens[_token]( streamer, hist=hist )
def generateRoot(streamer):
    return nextToken(streamer)
# stack-over-flow !!!
def check_int(s):
    if s[0] in ('-', '+'):
        return s[1:].isdigit()
    return s.isdigit()


operator = {
    "+" : createSymbol("+"),
    "-" : createSymbol("-"),
    "*" : createSymbol("*"),
    "/" : createSymbol("/"),
    "|" : createSymbol("|"),
    "=" : createSymbol("="),
    "<" : createSymbol("&lt;"),
    ">" : createSymbol("&gt;"),
    "&" : createSymbol("&amp;"),
    "~" : createSymbol("~")
}


symbols = {
    "{" : createSymbol("{"),
    "}" : createSymbol("}"),
    "(" : createSymbol("("),
    ")" : createSymbol(")"),
    "[" : createSymbol("["),
    "]" : createSymbol("]"),
    "," : createSymbol(","),
    **operator,
    ";" : createSymbol(";"),
    "." : createSymbol(".")

}


tokens = {
    "class" : ClassNode,
    "function" : createSubRot("function"),
    "method" : createSubRot("method"),
    "constructor" : createSubRot("constructor"),
    "if" : createCondition("if" , "ifStatement"),
    "let" : LetNode,
    "while" : createCondition("while" , "whileStatement"),
    "do" : doNode ,
    **symbols,
    "\"" : StringConstantNode,
    "var" : createVarNode("varDec" , "var"),
    "field" :createVarNode("classVarDec" , "field"),
    "static" :createVarNode("classVarDec" , "static"),
    "int" : createKeyword("int"),
    "char" : createKeyword("char"),
    "boolean" : createKeyword("boolean"),
    "true" : createKeyword("true"),
    "false" : createKeyword("false"),
    # "Array" : createKeyword("Array"),
    "void" : createKeyword("void"),
    "return" : ReturnNode,
    "this" : createKeyword("this"),
    "null" : createKeyword("null"),
    "else" : createKeyword("else")
}

print("load..")
