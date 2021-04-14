# Creates an AST from python3.6 code using the ANTLR parser.

import sys
from antlr4 import *
from parsers.python3.Python3Lexer import Python3Lexer
from parsers.python3.Python3Parser import Python3Parser
from listener import ASTListener
 
def main(argv):
    input_stream = FileStream(argv[1])
    lexer = Python3Lexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = Python3Parser(stream)
    tree = parser.file_input()
    listener = ASTListener()
    walker = ParseTreeWalker()
    walker.walk(listener, tree)
 
if __name__ == '__main__':
    main(sys.argv)
