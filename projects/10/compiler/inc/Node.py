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


class Expression(ArgcClosure):
    def __init__(self, streamer, hist=0):
        super(Expression, self).__init__(streamer, lcloser='(', rcloser=")", hist=hist)
        super().collect()


    def generate(self):
        return self.histline("<Expression>") + \
                    super().generate() + \
                    self.histline("</Expression>")


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


def nextToken(streamer, hist=0):
    _token = streamer.read()

    if _token in tokens:
        return tokens[_token]( streamer, hist=hist )

def generateRoot(streamer):
    return nextToken(streamer)

tokens = {
    "class" : ClassNode,
    "function" : 0,
    "method" : 0,
    "if" : createCondition("if" , "ifStatement"),
    "let" : 0,
    "while" : createCondition("while" , "whileStatement"),
    "do" : 0,
    "{" : createSymbol("{"),
    "}" : createSymbol("}"),
    "," : createSymbol(","),
    "=" : createSymbol("="),
    ";" : createSymbol(";"),
    "var" : VarNode,
    "int" : createKeyword("int")
}

print("load..")
