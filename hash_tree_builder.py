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

    # # Enter a parse tree produced by Python3Parser#eval_input.
    # def enterEval_input(self, ctx:Python3Parser.Eval_inputContext):
    #     self.enter_rule(ctx)

    # # Exit a parse tree produced by Python3Parser#eval_input.
    # def exitEval_input(self, ctx:Python3Parser.Eval_inputContext):
    #     self.exit_rule()


    # Enter a parse tree produced by Python3Parser#decorator.
    def enterDecorator(self, ctx:Python3Parser.DecoratorContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#decorator.
    def exitDecorator(self, ctx:Python3Parser.DecoratorContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#decorators.
    def enterDecorators(self, ctx:Python3Parser.DecoratorsContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#decorators.
    def exitDecorators(self, ctx:Python3Parser.DecoratorsContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#decorated.
    def enterDecorated(self, ctx:Python3Parser.DecoratedContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#decorated.
    def exitDecorated(self, ctx:Python3Parser.DecoratedContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#async_funcdef.
    def enterAsync_funcdef(self, ctx:Python3Parser.Async_funcdefContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#async_funcdef.
    def exitAsync_funcdef(self, ctx:Python3Parser.Async_funcdefContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#funcdef.
    def enterFuncdef(self, ctx:Python3Parser.FuncdefContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#funcdef.
    def exitFuncdef(self, ctx:Python3Parser.FuncdefContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#parameters.
    def enterParameters(self, ctx:Python3Parser.ParametersContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#parameters.
    def exitParameters(self, ctx:Python3Parser.ParametersContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#typedargslist.
    def enterTypedargslist(self, ctx:Python3Parser.TypedargslistContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#typedargslist.
    def exitTypedargslist(self, ctx:Python3Parser.TypedargslistContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#tfpdef.
    def enterTfpdef(self, ctx:Python3Parser.TfpdefContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#tfpdef.
    def exitTfpdef(self, ctx:Python3Parser.TfpdefContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#varargslist.
    def enterVarargslist(self, ctx:Python3Parser.VarargslistContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#varargslist.
    def exitVarargslist(self, ctx:Python3Parser.VarargslistContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#vfpdef.
    def enterVfpdef(self, ctx:Python3Parser.VfpdefContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#vfpdef.
    def exitVfpdef(self, ctx:Python3Parser.VfpdefContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#stmt.
    def enterStmt(self, ctx:Python3Parser.StmtContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#stmt.
    def exitStmt(self, ctx:Python3Parser.StmtContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#simple_stmt.
    def enterSimple_stmt(self, ctx:Python3Parser.Simple_stmtContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#simple_stmt.
    def exitSimple_stmt(self, ctx:Python3Parser.Simple_stmtContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#small_stmt.
    def enterSmall_stmt(self, ctx:Python3Parser.Small_stmtContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#small_stmt.
    def exitSmall_stmt(self, ctx:Python3Parser.Small_stmtContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#expr_stmt.
    def enterExpr_stmt(self, ctx:Python3Parser.Expr_stmtContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#expr_stmt.
    def exitExpr_stmt(self, ctx:Python3Parser.Expr_stmtContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#annassign.
    def enterAnnassign(self, ctx:Python3Parser.AnnassignContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#annassign.
    def exitAnnassign(self, ctx:Python3Parser.AnnassignContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#testlist_star_expr.
    def enterTestlist_star_expr(self, ctx:Python3Parser.Testlist_star_exprContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#testlist_star_expr.
    def exitTestlist_star_expr(self, ctx:Python3Parser.Testlist_star_exprContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#augassign.
    def enterAugassign(self, ctx:Python3Parser.AugassignContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#augassign.
    def exitAugassign(self, ctx:Python3Parser.AugassignContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#del_stmt.
    def enterDel_stmt(self, ctx:Python3Parser.Del_stmtContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#del_stmt.
    def exitDel_stmt(self, ctx:Python3Parser.Del_stmtContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#pass_stmt.
    def enterPass_stmt(self, ctx:Python3Parser.Pass_stmtContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#pass_stmt.
    def exitPass_stmt(self, ctx:Python3Parser.Pass_stmtContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#flow_stmt.
    def enterFlow_stmt(self, ctx:Python3Parser.Flow_stmtContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#flow_stmt.
    def exitFlow_stmt(self, ctx:Python3Parser.Flow_stmtContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#break_stmt.
    def enterBreak_stmt(self, ctx:Python3Parser.Break_stmtContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#break_stmt.
    def exitBreak_stmt(self, ctx:Python3Parser.Break_stmtContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#continue_stmt.
    def enterContinue_stmt(self, ctx:Python3Parser.Continue_stmtContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#continue_stmt.
    def exitContinue_stmt(self, ctx:Python3Parser.Continue_stmtContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#return_stmt.
    def enterReturn_stmt(self, ctx:Python3Parser.Return_stmtContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#return_stmt.
    def exitReturn_stmt(self, ctx:Python3Parser.Return_stmtContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#yield_stmt.
    def enterYield_stmt(self, ctx:Python3Parser.Yield_stmtContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#yield_stmt.
    def exitYield_stmt(self, ctx:Python3Parser.Yield_stmtContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#raise_stmt.
    def enterRaise_stmt(self, ctx:Python3Parser.Raise_stmtContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#raise_stmt.
    def exitRaise_stmt(self, ctx:Python3Parser.Raise_stmtContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#import_stmt.
    def enterImport_stmt(self, ctx:Python3Parser.Import_stmtContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#import_stmt.
    def exitImport_stmt(self, ctx:Python3Parser.Import_stmtContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#import_name.
    def enterImport_name(self, ctx:Python3Parser.Import_nameContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#import_name.
    def exitImport_name(self, ctx:Python3Parser.Import_nameContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#import_from.
    def enterImport_from(self, ctx:Python3Parser.Import_fromContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#import_from.
    def exitImport_from(self, ctx:Python3Parser.Import_fromContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#import_as_name.
    def enterImport_as_name(self, ctx:Python3Parser.Import_as_nameContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#import_as_name.
    def exitImport_as_name(self, ctx:Python3Parser.Import_as_nameContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#dotted_as_name.
    def enterDotted_as_name(self, ctx:Python3Parser.Dotted_as_nameContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#dotted_as_name.
    def exitDotted_as_name(self, ctx:Python3Parser.Dotted_as_nameContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#import_as_names.
    def enterImport_as_names(self, ctx:Python3Parser.Import_as_namesContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#import_as_names.
    def exitImport_as_names(self, ctx:Python3Parser.Import_as_namesContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#dotted_as_names.
    def enterDotted_as_names(self, ctx:Python3Parser.Dotted_as_namesContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#dotted_as_names.
    def exitDotted_as_names(self, ctx:Python3Parser.Dotted_as_namesContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#dotted_name.
    def enterDotted_name(self, ctx:Python3Parser.Dotted_nameContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#dotted_name.
    def exitDotted_name(self, ctx:Python3Parser.Dotted_nameContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#global_stmt.
    def enterGlobal_stmt(self, ctx:Python3Parser.Global_stmtContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#global_stmt.
    def exitGlobal_stmt(self, ctx:Python3Parser.Global_stmtContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#nonlocal_stmt.
    def enterNonlocal_stmt(self, ctx:Python3Parser.Nonlocal_stmtContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#nonlocal_stmt.
    def exitNonlocal_stmt(self, ctx:Python3Parser.Nonlocal_stmtContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#assert_stmt.
    def enterAssert_stmt(self, ctx:Python3Parser.Assert_stmtContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#assert_stmt.
    def exitAssert_stmt(self, ctx:Python3Parser.Assert_stmtContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#compound_stmt.
    def enterCompound_stmt(self, ctx:Python3Parser.Compound_stmtContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#compound_stmt.
    def exitCompound_stmt(self, ctx:Python3Parser.Compound_stmtContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#async_stmt.
    def enterAsync_stmt(self, ctx:Python3Parser.Async_stmtContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#async_stmt.
    def exitAsync_stmt(self, ctx:Python3Parser.Async_stmtContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#if_stmt.
    def enterIf_stmt(self, ctx:Python3Parser.If_stmtContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#if_stmt.
    def exitIf_stmt(self, ctx:Python3Parser.If_stmtContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#while_stmt.
    def enterWhile_stmt(self, ctx:Python3Parser.While_stmtContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#while_stmt.
    def exitWhile_stmt(self, ctx:Python3Parser.While_stmtContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#for_stmt.
    def enterFor_stmt(self, ctx:Python3Parser.For_stmtContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#for_stmt.
    def exitFor_stmt(self, ctx:Python3Parser.For_stmtContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#try_stmt.
    def enterTry_stmt(self, ctx:Python3Parser.Try_stmtContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#try_stmt.
    def exitTry_stmt(self, ctx:Python3Parser.Try_stmtContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#with_stmt.
    def enterWith_stmt(self, ctx:Python3Parser.With_stmtContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#with_stmt.
    def exitWith_stmt(self, ctx:Python3Parser.With_stmtContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#with_item.
    def enterWith_item(self, ctx:Python3Parser.With_itemContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#with_item.
    def exitWith_item(self, ctx:Python3Parser.With_itemContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#except_clause.
    def enterExcept_clause(self, ctx:Python3Parser.Except_clauseContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#except_clause.
    def exitExcept_clause(self, ctx:Python3Parser.Except_clauseContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#suite.
    def enterSuite(self, ctx:Python3Parser.SuiteContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#suite.
    def exitSuite(self, ctx:Python3Parser.SuiteContext):
        self.exit_rule()

    # XXX: this one causes a weird invalid hash value
    # # Enter a parse tree produced by Python3Parser#test.
    # def enterTest(self, ctx:Python3Parser.TestContext):
    #     self.enter_rule(ctx)

    # # Exit a parse tree produced by Python3Parser#test.
    # def exitTest(self, ctx:Python3Parser.TestContext):
    #     self.exit_rule()


    # Enter a parse tree produced by Python3Parser#test_nocond.
    def enterTest_nocond(self, ctx:Python3Parser.Test_nocondContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#test_nocond.
    def exitTest_nocond(self, ctx:Python3Parser.Test_nocondContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#lambdef.
    def enterLambdef(self, ctx:Python3Parser.LambdefContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#lambdef.
    def exitLambdef(self, ctx:Python3Parser.LambdefContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#lambdef_nocond.
    def enterLambdef_nocond(self, ctx:Python3Parser.Lambdef_nocondContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#lambdef_nocond.
    def exitLambdef_nocond(self, ctx:Python3Parser.Lambdef_nocondContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#or_test.
    def enterOr_test(self, ctx:Python3Parser.Or_testContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#or_test.
    def exitOr_test(self, ctx:Python3Parser.Or_testContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#and_test.
    def enterAnd_test(self, ctx:Python3Parser.And_testContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#and_test.
    def exitAnd_test(self, ctx:Python3Parser.And_testContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#not_test.
    def enterNot_test(self, ctx:Python3Parser.Not_testContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#not_test.
    def exitNot_test(self, ctx:Python3Parser.Not_testContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#comparison.
    def enterComparison(self, ctx:Python3Parser.ComparisonContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#comparison.
    def exitComparison(self, ctx:Python3Parser.ComparisonContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#comp_op.
    def enterComp_op(self, ctx:Python3Parser.Comp_opContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#comp_op.
    def exitComp_op(self, ctx:Python3Parser.Comp_opContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#star_expr.
    def enterStar_expr(self, ctx:Python3Parser.Star_exprContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#star_expr.
    def exitStar_expr(self, ctx:Python3Parser.Star_exprContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#expr.
    def enterExpr(self, ctx:Python3Parser.ExprContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#expr.
    def exitExpr(self, ctx:Python3Parser.ExprContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#xor_expr.
    def enterXor_expr(self, ctx:Python3Parser.Xor_exprContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#xor_expr.
    def exitXor_expr(self, ctx:Python3Parser.Xor_exprContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#and_expr.
    def enterAnd_expr(self, ctx:Python3Parser.And_exprContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#and_expr.
    def exitAnd_expr(self, ctx:Python3Parser.And_exprContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#shift_expr.
    def enterShift_expr(self, ctx:Python3Parser.Shift_exprContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#shift_expr.
    def exitShift_expr(self, ctx:Python3Parser.Shift_exprContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#arith_expr.
    def enterArith_expr(self, ctx:Python3Parser.Arith_exprContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#arith_expr.
    def exitArith_expr(self, ctx:Python3Parser.Arith_exprContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#term.
    def enterTerm(self, ctx:Python3Parser.TermContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#term.
    def exitTerm(self, ctx:Python3Parser.TermContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#factor.
    def enterFactor(self, ctx:Python3Parser.FactorContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#factor.
    def exitFactor(self, ctx:Python3Parser.FactorContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#power.
    def enterPower(self, ctx:Python3Parser.PowerContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#power.
    def exitPower(self, ctx:Python3Parser.PowerContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#atom_expr.
    def enterAtom_expr(self, ctx:Python3Parser.Atom_exprContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#atom_expr.
    def exitAtom_expr(self, ctx:Python3Parser.Atom_exprContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#atom.
    def enterAtom(self, ctx:Python3Parser.AtomContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#atom.
    def exitAtom(self, ctx:Python3Parser.AtomContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#testlist_comp.
    def enterTestlist_comp(self, ctx:Python3Parser.Testlist_compContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#testlist_comp.
    def exitTestlist_comp(self, ctx:Python3Parser.Testlist_compContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#trailer.
    def enterTrailer(self, ctx:Python3Parser.TrailerContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#trailer.
    def exitTrailer(self, ctx:Python3Parser.TrailerContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#subscriptlist.
    def enterSubscriptlist(self, ctx:Python3Parser.SubscriptlistContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#subscriptlist.
    def exitSubscriptlist(self, ctx:Python3Parser.SubscriptlistContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#subscript.
    def enterSubscript(self, ctx:Python3Parser.SubscriptContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#subscript.
    def exitSubscript(self, ctx:Python3Parser.SubscriptContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#sliceop.
    def enterSliceop(self, ctx:Python3Parser.SliceopContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#sliceop.
    def exitSliceop(self, ctx:Python3Parser.SliceopContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#exprlist.
    def enterExprlist(self, ctx:Python3Parser.ExprlistContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#exprlist.
    def exitExprlist(self, ctx:Python3Parser.ExprlistContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#testlist.
    def enterTestlist(self, ctx:Python3Parser.TestlistContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#testlist.
    def exitTestlist(self, ctx:Python3Parser.TestlistContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#dictorsetmaker.
    def enterDictorsetmaker(self, ctx:Python3Parser.DictorsetmakerContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#dictorsetmaker.
    def exitDictorsetmaker(self, ctx:Python3Parser.DictorsetmakerContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#classdef.
    def enterClassdef(self, ctx:Python3Parser.ClassdefContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#classdef.
    def exitClassdef(self, ctx:Python3Parser.ClassdefContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#arglist.
    def enterArglist(self, ctx:Python3Parser.ArglistContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#arglist.
    def exitArglist(self, ctx:Python3Parser.ArglistContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#argument.
    def enterArgument(self, ctx:Python3Parser.ArgumentContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#argument.
    def exitArgument(self, ctx:Python3Parser.ArgumentContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#comp_iter.
    def enterComp_iter(self, ctx:Python3Parser.Comp_iterContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#comp_iter.
    def exitComp_iter(self, ctx:Python3Parser.Comp_iterContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#comp_for.
    def enterComp_for(self, ctx:Python3Parser.Comp_forContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#comp_for.
    def exitComp_for(self, ctx:Python3Parser.Comp_forContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#comp_if.
    def enterComp_if(self, ctx:Python3Parser.Comp_ifContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#comp_if.
    def exitComp_if(self, ctx:Python3Parser.Comp_ifContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#encoding_decl.
    def enterEncoding_decl(self, ctx:Python3Parser.Encoding_declContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#encoding_decl.
    def exitEncoding_decl(self, ctx:Python3Parser.Encoding_declContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#yield_expr.
    def enterYield_expr(self, ctx:Python3Parser.Yield_exprContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#yield_expr.
    def exitYield_expr(self, ctx:Python3Parser.Yield_exprContext):
        self.exit_rule()


    # Enter a parse tree produced by Python3Parser#yield_arg.
    def enterYield_arg(self, ctx:Python3Parser.Yield_argContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by Python3Parser#yield_arg.
    def exitYield_arg(self, ctx:Python3Parser.Yield_argContext):
        self.exit_rule()
