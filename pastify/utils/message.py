BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
PINK = '\033[95m'
CYAN = '\033[96m'

class message:
    '''Class for printing colored messages as output'''
    @staticmethod
    def blue(s):
        print(BLUE+s+ENDC) 
        
    @staticmethod
    def cyan(s):
        print(CYAN+s+ENDC) 

    @staticmethod
    def green(s):
        print(GREEN+s+ENDC)
    
    @staticmethod
    def yellow(s):
        print(YELLOW+s+ENDC)


    @staticmethod
    def red(s):
        print(RED+s+ENDC)

    @staticmethod
    def bold(s):
        print(BOLD+s+ENDC)


    @staticmethod
    def pink(s):
        print(PINK+s+ENDC)

    @staticmethod
    def color(s, col, anm=True):
        COL = ""
        if col == "blue":
            COL=BLUE
        elif col == "cyan":
            COL=CYAN
        elif col == "green":
            COL=GREEN
        elif col == "yellow":
            COL=YELLOW
        elif col == "red":
            COL=RED
        elif col == "pink":
            COL=PINK
        else:
            print(s)
            return None

        print(COL+s+ENDC)

        