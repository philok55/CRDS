"""
TODO description

NOTE:
Get position in original code:
print("POSITION IN CODE: {}:{}".format(ctx.DEF().getPayload().line, ctx.DEF().getPayload().column))

Get literally the text of the code:
ctx.getText()
"""

from antlr4 import ParseTreeWalker
from parsers.python3.Python3Listener import Python3Listener
from parsers.python3.Python3Parser import Python3Parser
from hash_tree import HashedNode


class HashTreeBuilder(Python3Listener):
    def __init__(self, tree):
        super().__init__()
        self.tree = tree
        self.hashed_tree = None
        self.current = None

    def start(self):
        walker = ParseTreeWalker()
        walker.walk(self, self.tree)

    def print_tree(self):
        print(self.hashed_tree)

    def hash_node(self):
        self.current.hash()

    def enterFile_input(self, ctx:Python3Parser.File_inputContext):
        """
        File input subtree, this is the root node.
        We add this ctx as the root of our hashed tree.
        """
        self.hashed_tree = HashedNode(ctx)
        self.current = self.hashed_tree

    def exitFile_input(self, ctx:Python3Parser.File_inputContext):
        self.hash_node()

    # --------------------------------------------------------------------
    # Below are all the enter- and exit methods for every ctx type we want to hash
    # --------------------------------------------------------------------

    def enterFuncdef(self, ctx:Python3Parser.FuncdefContext):
        self.current = self.current.add_child(ctx)

    def exitFuncdef(self, ctx:Python3Parser.FuncdefContext):
        self.hash_node()
        self.current = self.current.parent

    def enterStmt(self, ctx:Python3Parser.StmtContext):
        self.current = self.current.add_child(ctx)

    def exitStmt(self, ctx:Python3Parser.StmtContext):
        self.hash_node()
        self.current = self.current.parent
