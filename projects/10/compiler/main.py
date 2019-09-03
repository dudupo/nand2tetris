
import sys
import inc.Node as Node
import inc.Streamer as Streamer

def outfilename( inputfile ):
    return inputfile.replace( ".jack" , "_out.xml")

if __name__ == '__main__':
    if ( len(sys.argv) > 1 ):
        inputfile = sys.argv[1]

        xmlcode =  Node.Node(Streamer.Streamer( inputfile )).generate()  #parser.parse(open( inputfile, 'r' ).readlines())
        outpath = outfilename(inputfile)
        with open( outpath , "w" ) as output :
            output.write( xmlcode )
            output.close()
