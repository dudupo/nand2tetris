

comp = {
    "0"   : "0101010",
    "1"   : "0111111",
    "-1"  : "0111010",
    "D"   : "0001100",
    "A"   : "0110000",
    "M"   : "1110000",
    "!D"  : "0001101",
    "!A"  : "0110001",
    "!M"  : "1110001",
    "-D"  : "0001111",
    "-A"  : "0110011",
    "-M"  : "1110011",
    "D+1" : "0011111",
    "A+1" : "0110111",
    "M+1" : "1110111",
    "D-1" : "0001110",
    "A-1" : "0110010",
    "M-1" : "1110010",
    "D+A" : "0000010",
    "D+M" : "1000010",
    "D-A" : "0010011",
    "D-M" : "1010011",
    "A-D" : "0000111",
    "M-D" : "1000111",
    "D&A" : "0000000",
    "D&M" : "1000000",
    "D|A" : "0010101",
    "D|M" : "1010101"
}

dest = {
    "null"  : "000",
    "M"     : "001",
    "D"     : "010",
    "MD"    : "011",
    "A"     : "100",
    "AM"    : "101",
    "AD"    : "110",
    "AMD"   : "111"
}

jump = {
    "null"  : "000",
    "JGT"   : "001",
    "JEQ"   : "010",
    "JGE"   : "011",
    "JLT"   : "100",
    "JNE"   : "110",
    "JMP"   : "111"
}
#
# def extract_comp(line):
#     compLit = ""
#
#     def _search(char, compLit):
#         return char == "=" , compLit
#
#     def _accumulate(char, compLit):
#         if char != ";":
#             compLit += char
#             return False, compLit
#         return True, compLit
#
#     def _none(char, compLit):
#         return False
#
#     states = [ _search, _accumulate, _none]
#     stateindex = 0
#     for char in line:
#         _nextstate , compLit = states[stateindex](char , compLit)
#         if _nextstate :
#             stateindex += 1
#
# def decompose(line):
#     destLit, compLit, jumpLit = "", "", ""
#     destInd, compInd, jumpInd = 0,0,0






def generate(lines):

    code = ""

    for line in lines:
        if line[0] == "$":
            destLit, compLit, jumpLit = line[1:].split(";")
            code += "111" + comp[compLit] + dest[destLit] + jump[jumpLit] +"\n"
        else:
            code += line + "\n"
    return code
