from parsers.python3.Python3Listener import Python3Listener
from parsers.python3.Python3Parser import Python3Parser

class ASTListener(Python3Listener):
    def enterFuncdef(self, ctx:Python3Parser.FuncdefContext):
        print("FUNCTION FOUND")
        # Get position in original code:
        print("POSITION IN CODE: {}:{}".format(ctx.DEF().getPayload().line, ctx.DEF().getPayload().column))
