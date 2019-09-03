




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
    def __init__(self, streamer, hist=0):
        super(ArgcCosure, self).__init__(streamer, hist)

        _token = None
        while _token != ")":
            pass


    def generate(self):
        return self.histline("<symbol> ( </symbol>") + \
                    self.histline("<keyword> class </keyword>", addition=1) + super().generate()


class ClassNode(Node):
    def __init__(self, streamer, hist=0):
        super(ClassNode, self).__init__(streamer, hist=hist)
        self.children.append( IdentifierNode(streamer, hist=self.hist + 1))

    def generate(self):
        return self.histline("<class>") + \
                    self.histline("<keyword> class </keyword>", addition=1) + super().generate()




tokens = {
    "class" : ClassNode,
    "function" : 0,
    "method" : 0,
    "if" : 0,
    "let" : 0,
    "do" : 0
}




def nextToken(streamer):
    _token = streamer.read()

    if _token in tokens:
        return tokens[_token]( streamer )

def generateRoot(streamer):
    return nextToken(streamer)
