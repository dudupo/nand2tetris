
def handle_spaces_and_commments(text):



    while text.find( "/*" ) > 0 :
        i = text.find( "/*" )
        j = text.find( "*/" )
        text = text[:i] + text[j+3:]

    def iscomment(line):
        return len(line) > 1 and line[0] == "/" and line[1] == "/"

    def stripcomment(line):
        return line[0:line.index("//")] if "//" in line else line

    def ismultiline(line):
        return len(line>1)

    multiline = False

    rettext = ""
    for line in text.split("\n"):
        if not iscomment(line):
            templine = line.strip()
            if len(templine) > 0 :
                rettext += stripcomment(templine).strip() + "\n"
    return rettext


class Streamer():
    """docstring for Streamer."""

    def __init__(self, inputfile):
        super(Streamer, self).__init__()
        self.text =  handle_spaces_and_commments(open(inputfile, 'r').read())
        self.cursor = 0

        print(self.text)

    def read(self):
        pass
