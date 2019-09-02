import inc.code as code

def dex_parse(line):
    ret = format(int(line[1:]) , 'b')
    return "0" * (16 - len(ret)) + ret

symbol = {
    '@R0'  :    '0000000000000000',
    '@R1'  :    '0000000000000001',
    '@R2'  :    '0000000000000010',
    '@R3'  :    '0000000000000011',
    '@R4'  :    '0000000000000100',
    '@R5'  :    '0000000000000101',
    '@R6'  :    '0000000000000110',
    '@R7'  :    '0000000000000111',
    '@R8'  :    '0000000000001000',
    '@R9'  :    '0000000000001001',
    '@R10' :    '0000000000001010',
    '@R11' :    '0000000000001011',
    '@R12' :    '0000000000001100',
    '@R13' :    '0000000000001101',
    '@R14' :    '0000000000001110',
    '@R15' :    '0000000000001111',
    '@SCREEN' :  dex_parse('@16384'),
    '@KBD'    :  dex_parse('@24576'),
    '@SP'     :  dex_parse('@0'),
    '@LCL'    :  dex_parse('@1'),
    '@ARG'    :  dex_parse('@2'),
    '@THIS'   :  dex_parse('@3'),
    '@THAT'   :  dex_parse('@4')
}

def symbol_parse(line):
    pass



def binary_parse(line):
    return line +"\n"

def c_instruction(line):




    return "0" *16 + "\n"

def emptyline(line):
    return ""


def handle_spaces_and_commments(lines):

    def iscomment(line):
        return len(line) > 1 and line[0] == "/" and line[1] == "/"

    def stripcomment(line):
        return line[0:line.index("//")] if "//" in line else line

    retlines = []
    for line in lines:
        if not iscomment(line):
            templine = line.strip()
            if len(templine) > 0 :
                retlines.append( stripcomment(templine).strip() )
    return retlines

def assignment_var(lines):
    retlines = []
    for line in lines:
        if line[0] == "@":
            if line in symbol:
                retlines.append(symbol[line])
            else:
                retlines.append( dex_parse(line) )
        else:
            retlines.append("$" + line)
    return retlines

def add_symbols(lines):
    retlines = []
    hist = 0
    for number , line in enumerate(lines):
        if line[0] == "(" and line[-1] == ")":
            symbol[ "@" + line[1:-1] ] = dex_parse( "@{0}".format( number + hist) )
            hist -= 1
        else :
            retlines.append(line)
    #print(symbol)
    return retlines

def format_lines(lines):
    retlines = []
    for line in lines:
        templine = "" + line
        if line[0] == "$":
            templine = line[1:]
            if not "=" in line:
                templine = "null;" + templine
            else:
                templine = templine.replace('=' ,';')
            if not ";" in line:
                templine = templine +";null"
            templine = "$" + templine
        retlines.append(templine)
    return retlines

def parse(lines):

    lines = handle_spaces_and_commments(lines)
    lines = add_symbols(lines)
    lines = assignment_var(lines)
    lines = format_lines(lines)
    return code.generate(lines)
