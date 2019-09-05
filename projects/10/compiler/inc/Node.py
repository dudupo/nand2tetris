class Node():
    def __init__(self, streamer, hist=0):
        self.streamer = streamer
        self.children = []
        self.hist = hist

    def generate(self):
        ret = ""
        for child in self.children:
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

class ArgcCosure(Node):
    def __init__(self, streamer, lcloser='(', rcloser=")", hist=0):
        super(ArgcCosure, self).__init__(streamer, hist = hist)
        self.lcloser = lcloser
        self.rcloser = rcloser

    def collect(self):
        print(" i was here")

        if self.streamer.top() != self.lcloser:
            raise Exception("shit")

        self.children.append( nextToken(self.streamer, hist=self.hist+1) )


        _token = None
        while self.streamer.top() != self.rcloser :
            node = nextToken(self.streamer, hist=self.hist+1)
            if node != None :
                self.children.append( node )

        self.children.append( nextToken(self.streamer, hist=self.hist+1) )


class ClassNode(ArgcCosure):
    def __init__(self, streamer, hist=0):
        super(ClassNode, self).__init__(streamer, lcloser='{', rcloser="}", hist=hist)
        self.children.append( IdentifierNode(streamer, hist=self.hist + 1))

        super().collect()

    def generate(self):
        return self.histline("<class>") + \
                    self.histline("<keyword> class </keyword>", addition=1) + super().generate() + \
                    self.histline("</class>")

def createSymbol(_symbol):
    class SymbolNode(Node):

        def __init__(self, streamer, hist=0):
            super(SymbolNode, self).__init__(streamer, hist)

        def generate(self):
            return self.histline("<symbol>{0}</symbol>".format(_symbol))

    return SymbolNode




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
    "if" : 0,
    "let" : 0,
    "do" : 0,
    "{" : createSymbol("{"),
    "}" : createSymbol("}")
}


print("load..")
