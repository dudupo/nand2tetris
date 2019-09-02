import inc.code as code

def symbol_parse(line):
    pass

def dex_parse(line):
    ret = format(int(line[1:]) , 'b')
    return "0" * (16 - len(ret)) + ret

def binary_parse(line):
    return line +"\n"

def c_instruction(line):




    return "0" *16 + "\n"

def emptyline(line):
    return ""


def handle_spaces_and_commments(lines):

    def iscomment(line):
        return len(line) > 1 and line[0] == "/" and line[1] == "/"

    retlines = []
    for line in lines:
        if not iscomment(line):
            templine = line.strip()
            if len(templine) > 0 :
                retlines.append(templine)
    return retlines

def assignment_var(lines):
    retlines = []
    for line in lines:
        if line[0] == "@":
            retlines.append( dex_parse(line) )
        else:
            retlines.append(line)
    return retlines

def format_lines(lines):
    retlines = []
    for line in lines:
        templine = "" + line
        if line[0] != "@":
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
    lines = format_lines(lines)
    lines = assignment_var(lines)
    return code.generate(lines)
