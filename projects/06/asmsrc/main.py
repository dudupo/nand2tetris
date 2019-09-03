
import sys
import inc.parser as parser
import inc.code as code

def outfilename( inputfile ):
    return inputfile.replace( ".asm" , "_out.hack")

if __name__ == '__main__':
    if ( len(sys.argv) > 1 ):
        inputfile = sys.argv[1]
        hackcode = parser.parse(open( inputfile, 'r' ).readlines())
        outpath = outfilename(inputfile)
        with open( outpath , "w" ) as output :
            output.write( hackcode )
            output.close()
