if __name__ == '__main__':
    print("HalfAdder(a=a[0],b=b[0],sum=out[0],carry=carry0);");
    for i in range(1,16):
        print("FullAdder(a=a[{1}],b=b[{1}],c=carry{0},sum=out[{1}],carry=carry{1});".format(i-1,i))

    print("...")

    for i in range(1,16):
        print("Xor(a=in[{1}],b=carry{0},out=out[{1}]);".format(i-1,i))
        print("And(a=in[{1}],b=carry{0},out=carry{1});".format(i-1,i))

    print("...")

    for x , flag in [("x" ,"zx") ,("y" ,"zy")]:
        for i in range(0,16):
            print("And(a={0}[{2}],b={1},out=z{0}out{2});".format(x,flag,i))
