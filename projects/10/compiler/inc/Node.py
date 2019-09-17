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

    def histline(self, line, addition=0):
        return (self.hist + addition) * "\t" + line + "\n"

class IdentifierNode(Node):
    def __init__(self, streamer, hist=0):
        super(IdentifierNode, self).__init__(streamer, hist)
        self.identifier = streamer.read()

    def generate(self):
        return self.histline("<identifier> {0} </identifier>".format(self.identifier))

class ArgcClosure(Node):
    def __init__(self, streamer, lcloser='(', rcloser=")", hist=0):
        super(ArgcClosure, self).__init__(streamer, hist = hist)
        self.lcloser = lcloser
        self.rcloser = rcloser

    def collect(self):
        self.children.append( nextToken(self.streamer, hist=self.hist+1) )


        _token = None
        while self.streamer.top() != self.rcloser :
            node = nextToken(self.streamer, hist=self.hist+1)
            if node != None :
                self.children.append( node )

        self.children.append( nextToken(self.streamer, hist=self.hist+1) )


class ClassNode(ArgcClosure):
    def __init__(self, streamer, hist=0):
        super(ClassNode, self).__init__(streamer, lcloser='{', rcloser="}", hist=hist)
        self.children.append( IdentifierNode(streamer, hist=self.hist + 1))

        super().collect()


    def generate(self):
        return self.histline("<class>") + \
                    self.histline("<keyword> class </keyword>", addition=1) + super().generate() + \
                    self.histline("</class>")

class VarNode(Node):
    def __init__(self, streamer, hist=0):
        super(VarNode, self).__init__(streamer, hist=hist)
        self.children.append( createKeyword("var")( streamer, hist=hist+1) )
        self.children.append( nextToken(streamer, hist=hist+1) ) # int
        self.children.append( IdentifierNode(streamer, hist=hist+1 ))

        while streamer.top() == ",":
            self.children.append( nextToken(streamer, hist=hist+1) )
            self.children.append( IdentifierNode(streamer, hist=hist+1 ))

        self.children.append( nextToken(streamer, hist=hist+1) )


    def generate(self):
        return self.histline("<varDec>") +\
                    super().generate() + self.histline("</varDec>")


class Term(Node):
    def __init__(self, streamer, node, hist=0):
        super(Term, self).__init__(streamer, hist=hist)
        self.node = node;
        self.node.hist += 1

    def generate(self):
        return self.histline("<term>") +\
                    self.node.generate() + self.histline("</term>")

class Expression(ArgcClosure):
    def __init__(self, streamer, lcloser='(', rcloser=")", hist=0):
        super(Expression, self).__init__(streamer, lcloser=lcloser, rcloser=rcloser, hist=hist+1)
        self.collect()

        # self.preExp = self.children.pop(0) # =
        # self.endExp = self.children.pop(-1)

        # for debuging propuse :
        if self.preExp is None:
            self.preExp = Node(streamer)

        if self.endExp is None:
            self.endExp = Node(streamer)

        self.preExp.hist -= 1
        self.endExp.hist -= 1

    def collect(self):
        self.preExp = nextToken(self.streamer, hist=self.hist+1)

        _token = None
        while self.streamer.top() != self.rcloser :
            if self.streamer.top() == "(" :
                self.children.append(Expression(self.streamer, lcloser='(', rcloser=')', hist=self.hist+1))
            else :
                node = Token_or_Identifier(self.streamer, hist=self.hist+1)
                if node != None :
                    self.children.append( Term(self.streamer,node, hist=self.hist+1) )

        self.endExp = nextToken(self.streamer, hist=self.hist+1)

    def generate(self):
        return self.preExp.generate() +\
                    self.histline("<expression>") + \
                    super().generate() + \
                    self.histline("</expression>") +\
                    self.endExp.generate()


class LetNode(Node):
    def __init__(self, streamer, hist=0):
        super(LetNode, self).__init__(streamer, hist=hist)
        self.children.append( createKeyword("let")( streamer, hist=hist+1) )
        self.children.append( IdentifierNode(streamer, hist=hist+1 ))
        self.children.append(  Expression(streamer, lcloser = "=", rcloser = ";", hist=hist+1 ) )

    def generate(self):
        return self.histline("<lateStatement>") + \
            super().generate() + \
            self.histline("</lateStatement>")

class doNode(Node):
    def __init__(self, streamer, hist=0):
        super(doNode, self).__init__(streamer, hist=hist)
        self.children.append( createKeyword("do")( streamer, hist=hist+1))

        self.children.append( IdentifierNode(streamer, hist=hist+1) )
        while streamer.top() == ".":
            self.children.append( nextToken(streamer, hist=hist+1) )
            self.children.append( IdentifierNode(streamer, hist=hist+1) )
        self.children.append( nextToken(streamer, hist=hist+1) )

    def generate(self):
        return self.histline("<doStatement>") + \
            super().generate() + \
            self.histline("</doStatement>")

class parameterListNode(Node):
    def __init__(self, streamer, hist=0):
        super(parameterListNode, self).__init__( streamer, hist=hist )

        self.children.append( nextToken( streamer, hist=hist+1 ))
        while streamer.top() != ")" :
            self.children.append( Token_or_Identifier(streamer, hist=hist+1) )
        self.children.append( nextToken( streamer, hist=hist+1 ))

    def generate(self):
        return self.histline("<parameterList>") + \
            super().generate() + \
            self.histline("</parameterList>")

class BodySubRotNode(ArgcClosure):
    def __init__(self, streamer, hist=0):
        super(BodySubRotNode, self).__init__( streamer, lcloser='{', rcloser="}", hist=hist)
        super().collect()

    def generate(self):
        return self.histline("<subroutineBody>") + \
            super().generate() + \
            self.histline("</subroutineBody>")

def createSubRot(_keyword):
    class SubRotNode(Node):
        def __init__(self, streamer, hist=0):
            super(SubRotNode, self).__init__( streamer, hist=hist)
            self.children.append(createKeyword(_keyword)(streamer, hist=hist+1))
            self.children.append( nextToken(streamer, hist=hist+1) )
            self.children.append( IdentifierNode(streamer, hist=hist+1) )
            self.children.append( parameterListNode(streamer, hist=hist+1) )
            self.children.append( BodySubRotNode(streamer, hist=hist+1) )

        def generate(self):
            return self.histline("<subroutineDec>") +\
                super().generate() +\
                self.histline("</subroutineDec>")

    return SubRotNode

def createCondition(_keyword, _statement):
    class conditionNode(ArgcClosure):
        def __init__(self, streamer, hist=0):
            super(conditionNode, self).__init__(streamer, lcloser='{', rcloser="}", hist=hist)

            self.children.append(Expression(streamer, hist=hist+1))
            super().collect()


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

tokens = {
    "class" : ClassNode,
    "function" : createSubRot("function"),
    "method" : createSubRot("method"),
    "if" : createCondition("if" , "ifStatement"),
    "let" : LetNode,
    "while" : createCondition("while" , "whileStatement"),
    "do" : doNode ,
    "{" : createSymbol("{"),
    "}" : createSymbol("}"),
    "," : createSymbol(","),
    "=" : createSymbol("="),
    "+" : createSymbol("+"),
    "-" : createSymbol("-"),
    ";" : createSymbol(";"),
    "." : createSymbol("."),
    "var" : VarNode,
    "int" : createKeyword("int"),
    "void" : createKeyword("void")
}

print("load..")
