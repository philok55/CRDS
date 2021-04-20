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

    def print_tree(self, file_name=None):
        try:
            with open(file_name, 'w') as file:
                file.write(str(self.hashed_tree))
        except TypeError:
            print(self.hashed_tree)

    def hash_node(self):
        self.current.hash()

    def enter_rule(self, ctx):
        self.current = self.current.add_child(ctx)

    def exit_rule(self):
        self.hash_node()
        self.current = self.current.parent

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
        self.enter_rule(ctx)

    def exitFuncdef(self, ctx:Python3Parser.FuncdefContext):
        self.exit_rule()

    def enterIf_stmt(self, ctx:Python3Parser.If_stmtContext):
        self.enter_rule(ctx)

    def exitIf_stmt(self, ctx:Python3Parser.If_stmtContext):
        self.exit_rule()

    def enterWhile_stmt(self, ctx:Python3Parser.While_stmtContext):
        self.enter_rule(ctx)

    def exitWhile_stmt(self, ctx:Python3Parser.While_stmtContext):
        self.exit_rule()

    def enterFor_stmt(self, ctx:Python3Parser.For_stmtContext):
        self.enter_rule(ctx)

    def exitFor_stmt(self, ctx:Python3Parser.For_stmtContext):
        self.exit_rule()

    def enterTry_stmt(self, ctx:Python3Parser.Try_stmtContext):
        self.enter_rule(ctx)

    def exitTry_stmt(self, ctx:Python3Parser.Try_stmtContext):
        self.exit_rule()

    def enterExcept_clause(self, ctx:Python3Parser.Except_clauseContext):
        self.enter_rule(ctx)

    def exitExcept_clause(self, ctx:Python3Parser.Except_clauseContext):
        self.exit_rule()

    def enterSliceop(self, ctx:Python3Parser.SliceopContext):
        self.enter_rule(ctx)

    def exitSliceop(self, ctx:Python3Parser.SliceopContext):
        self.exit_rule()

    def enterClassdef(self, ctx:Python3Parser.ClassdefContext):
        self.enter_rule(ctx)

    def exitClassdef(self, ctx:Python3Parser.ClassdefContext):
        self.exit_rule()

    def enterAugassign(self, ctx:Python3Parser.AugassignContext):
        self.enter_rule(ctx)  # += or -=

    def exitAugassign(self, ctx:Python3Parser.AugassignContext):
        self.exit_rule()

    def enterBreak_stmt(self, ctx:Python3Parser.Break_stmtContext):
        self.enter_rule(ctx)

    def exitBreak_stmt(self, ctx:Python3Parser.Break_stmtContext):
        self.exit_rule()

    def enterContinue_stmt(self, ctx:Python3Parser.Continue_stmtContext):
        self.enter_rule(ctx)

    def exitContinue_stmt(self, ctx:Python3Parser.Continue_stmtContext):
        self.exit_rule()

    def enterReturn_stmt(self, ctx:Python3Parser.Return_stmtContext):
        self.enter_rule(ctx)

    def exitReturn_stmt(self, ctx:Python3Parser.Return_stmtContext):
        self.exit_rule()

    def enterYield_stmt(self, ctx:Python3Parser.Yield_stmtContext):
        self.enter_rule(ctx)

    def exitYield_stmt(self, ctx:Python3Parser.Yield_stmtContext):
        self.exit_rule()

    def enterTerm(self, ctx:Python3Parser.TermContext):
        self.enter_rule(ctx)

    def exitTerm(self, ctx:Python3Parser.TermContext):
        self.exit_rule()

    def enterStmt(self, ctx:Python3Parser.StmtContext):
        self.enter_rule(ctx)

    def exitStmt(self, ctx:Python3Parser.StmtContext):
        self.exit_rule()