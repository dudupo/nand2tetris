

class OperationGate:

    id = 0

    def __init__(self, Gate="Or"):
        self.id = OperationGate.id
        OperationGate.id += 1
        self.out = Gate.lower() + str(self.id)
        self.Gate = Gate+"(a={0},b={1},out=" + self.out + " );"

    def feed(self, gate1, gate2):
        return self.Gate.format(gate1.out , gate2.out );

    def endcase(self, index):
        inp = "in[{0}]"
        return self.Gate.format( inp.format(index) , inp.format(index+1) );

    @staticmethod
    def recursiveinit(n, hist=0,  op="Or"):
        g = OperationGate()
        if n > 2:
            gate1 , gate2 = OperationGate.recursiveinit(n//2, hist, op), \
              OperationGate.recursiveinit(n//2, hist + n//2, op)
            print( g.feed(gate1, gate2) )
        else:
            print(g.endcase(hist))
        return g

    @staticmethod
    def sequentialinit(n, op="Or"):
        for i in range(n):
            defline =  "(a={0},b={1}," + { False : "" ,True : "sel=sel," }[op=="Mux"] + "out={2});"
            Gate = op + defline.format("a[{0}]".format(i), \
             "b[{0}]".format(i) , "out[{0}]".format(i))
            print( Gate );

    @staticmethod
    def unarisequentialinit(n, op="Not"):
        for i in range(n):
            Gate = op + "(in={0},out={1});".format("in[{0}]".format(i), \
             "out[{0}]".format(i))
            print( Gate );

if __name__ == '__main__':
    n = 16

    #OperationGate.recursiveinit(n)
    OperationGate.sequentialinit(n, op="And")
    #OperationGate.unarisequentialinit(n)
