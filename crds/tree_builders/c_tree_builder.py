"""
Hashed Tree builder for the C parser.

This is an ANTLR generated parse tree listener, adapted to
walk a C parse tree, build our hashed AST and store
all its sub trees by size.
"""

from antlr4 import ParseTreeWalker
from antlr4.tree.Tree import TerminalNode
from parsers.C.CListener import CListener
from parsers.C.CParser import CParser
from ..hash_tree.hash_tree import HashedNode


class CTreeBuilder(CListener):
    """
    Parse Tree Listener for the C language.

    Enter- and exit functions generated by ANTLR.
    """
    def __init__(self, tree):
        super().__init__()
        self.tree = tree
        self.hashed_tree = None
        self.current = None
        self.sorted_trees = {}
        self.sub_tree_sizes = []

    def start(self):
        walker = ParseTreeWalker()
        walker.walk(self, self.tree)

    def print_tree(self, file_name=None):
        """Print the full tree, either to a file or to stdout."""
        try:
            with open(file_name, 'w') as file:
                file.write(str(self.hashed_tree))
        except TypeError:
            print(self.hashed_tree)

    def hash_node(self):
        """
        Hash the current node. Should be called on CTX exit,
        because it expects the children to be hashed already.
        """
        self.current.hash()

    def store_subtree(self):
        """
        Store the sub tree that has the current node as root.
        Sub trees are stored by size in a dictionary (for fast lookup) as follows:

        {
            <<size>>: [<<subtree>>, <<subtree>>],
            <<size>>: [<<subtree>>, <<subtree>>, <<subtree>>]
        }

        Should be called on CTX exit, because it expects the children to be stored already.
        """
        size = self.current.set_subtree_size()
        if size in self.sorted_trees:
            self.sorted_trees[size].append(self.current)
        else:
            self.sorted_trees.update({size: [self.current]})
            self.sub_tree_sizes.append(size)

    def enter_rule(self, ctx):
        """
        Function executed on entry of every CTX node (downward pass of traversal).
        Here we build the tree that will be hashed.
        """
        # Skip 'wrapper' nodes
        if ctx.getChildCount() == 1 and not isinstance(ctx.getChild(0), TerminalNode):
            return

        self.current = self.current.add_child(ctx)

    def exit_rule(self, ctx):
        """
        Function executed on exit of every CTX node (upward pass of traversal).
        Here we have the data of the children, so we can hash the current node
        and store it by sub tree size.
        """
        # Skip 'wrapper' nodes
        if ctx.getChildCount() == 1 and not isinstance(ctx.getChild(0), TerminalNode):
            return

        self.hash_node()
        self.store_subtree()
        self.current = self.current.parent

    def enterCompilationUnit(self, ctx:CParser.CompilationUnitContext):
        """
        Compilation Unit subtree, this is the root node.
        We add this ctx as the root of our hashed tree.
        """
        self.hashed_tree = HashedNode(ctx, parser=CParser)
        self.current = self.hashed_tree

    def exitCompilationUnit(self, ctx:CParser.CompilationUnitContext):
        self.hash_node()
        self.store_subtree()

    # --------------------------------------------------------------------
    # Below are all the enter- and exit methods for every ctx type
    # --------------------------------------------------------------------

    # Enter a parse tree produced by CParser#primaryExpression.
    def enterPrimaryExpression(self, ctx:CParser.PrimaryExpressionContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#primaryExpression.
    def exitPrimaryExpression(self, ctx:CParser.PrimaryExpressionContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#genericSelection.
    def enterGenericSelection(self, ctx:CParser.GenericSelectionContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#genericSelection.
    def exitGenericSelection(self, ctx:CParser.GenericSelectionContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#genericAssocList.
    def enterGenericAssocList(self, ctx:CParser.GenericAssocListContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#genericAssocList.
    def exitGenericAssocList(self, ctx:CParser.GenericAssocListContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#genericAssociation.
    def enterGenericAssociation(self, ctx:CParser.GenericAssociationContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#genericAssociation.
    def exitGenericAssociation(self, ctx:CParser.GenericAssociationContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#postfixExpression.
    def enterPostfixExpression(self, ctx:CParser.PostfixExpressionContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#postfixExpression.
    def exitPostfixExpression(self, ctx:CParser.PostfixExpressionContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#argumentExpressionList.
    def enterArgumentExpressionList(self, ctx:CParser.ArgumentExpressionListContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#argumentExpressionList.
    def exitArgumentExpressionList(self, ctx:CParser.ArgumentExpressionListContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#unaryExpression.
    def enterUnaryExpression(self, ctx:CParser.UnaryExpressionContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#unaryExpression.
    def exitUnaryExpression(self, ctx:CParser.UnaryExpressionContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#unaryOperator.
    def enterUnaryOperator(self, ctx:CParser.UnaryOperatorContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#unaryOperator.
    def exitUnaryOperator(self, ctx:CParser.UnaryOperatorContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#castExpression.
    def enterCastExpression(self, ctx:CParser.CastExpressionContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#castExpression.
    def exitCastExpression(self, ctx:CParser.CastExpressionContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#multiplicativeExpression.
    def enterMultiplicativeExpression(self, ctx:CParser.MultiplicativeExpressionContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#multiplicativeExpression.
    def exitMultiplicativeExpression(self, ctx:CParser.MultiplicativeExpressionContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#additiveExpression.
    def enterAdditiveExpression(self, ctx:CParser.AdditiveExpressionContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#additiveExpression.
    def exitAdditiveExpression(self, ctx:CParser.AdditiveExpressionContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#shiftExpression.
    def enterShiftExpression(self, ctx:CParser.ShiftExpressionContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#shiftExpression.
    def exitShiftExpression(self, ctx:CParser.ShiftExpressionContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#relationalExpression.
    def enterRelationalExpression(self, ctx:CParser.RelationalExpressionContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#relationalExpression.
    def exitRelationalExpression(self, ctx:CParser.RelationalExpressionContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#equalityExpression.
    def enterEqualityExpression(self, ctx:CParser.EqualityExpressionContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#equalityExpression.
    def exitEqualityExpression(self, ctx:CParser.EqualityExpressionContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#andExpression.
    def enterAndExpression(self, ctx:CParser.AndExpressionContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#andExpression.
    def exitAndExpression(self, ctx:CParser.AndExpressionContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#exclusiveOrExpression.
    def enterExclusiveOrExpression(self, ctx:CParser.ExclusiveOrExpressionContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#exclusiveOrExpression.
    def exitExclusiveOrExpression(self, ctx:CParser.ExclusiveOrExpressionContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#inclusiveOrExpression.
    def enterInclusiveOrExpression(self, ctx:CParser.InclusiveOrExpressionContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#inclusiveOrExpression.
    def exitInclusiveOrExpression(self, ctx:CParser.InclusiveOrExpressionContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#logicalAndExpression.
    def enterLogicalAndExpression(self, ctx:CParser.LogicalAndExpressionContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#logicalAndExpression.
    def exitLogicalAndExpression(self, ctx:CParser.LogicalAndExpressionContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#logicalOrExpression.
    def enterLogicalOrExpression(self, ctx:CParser.LogicalOrExpressionContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#logicalOrExpression.
    def exitLogicalOrExpression(self, ctx:CParser.LogicalOrExpressionContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#conditionalExpression.
    def enterConditionalExpression(self, ctx:CParser.ConditionalExpressionContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#conditionalExpression.
    def exitConditionalExpression(self, ctx:CParser.ConditionalExpressionContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#assignmentExpression.
    def enterAssignmentExpression(self, ctx:CParser.AssignmentExpressionContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#assignmentExpression.
    def exitAssignmentExpression(self, ctx:CParser.AssignmentExpressionContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#assignmentOperator.
    def enterAssignmentOperator(self, ctx:CParser.AssignmentOperatorContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#assignmentOperator.
    def exitAssignmentOperator(self, ctx:CParser.AssignmentOperatorContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#expression.
    def enterExpression(self, ctx:CParser.ExpressionContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#expression.
    def exitExpression(self, ctx:CParser.ExpressionContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#constantExpression.
    def enterConstantExpression(self, ctx:CParser.ConstantExpressionContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#constantExpression.
    def exitConstantExpression(self, ctx:CParser.ConstantExpressionContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#declaration.
    def enterDeclaration(self, ctx:CParser.DeclarationContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#declaration.
    def exitDeclaration(self, ctx:CParser.DeclarationContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#declarationSpecifiers.
    def enterDeclarationSpecifiers(self, ctx:CParser.DeclarationSpecifiersContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#declarationSpecifiers.
    def exitDeclarationSpecifiers(self, ctx:CParser.DeclarationSpecifiersContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#declarationSpecifiers2.
    def enterDeclarationSpecifiers2(self, ctx:CParser.DeclarationSpecifiers2Context):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#declarationSpecifiers2.
    def exitDeclarationSpecifiers2(self, ctx:CParser.DeclarationSpecifiers2Context):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#declarationSpecifier.
    def enterDeclarationSpecifier(self, ctx:CParser.DeclarationSpecifierContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#declarationSpecifier.
    def exitDeclarationSpecifier(self, ctx:CParser.DeclarationSpecifierContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#initDeclaratorList.
    def enterInitDeclaratorList(self, ctx:CParser.InitDeclaratorListContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#initDeclaratorList.
    def exitInitDeclaratorList(self, ctx:CParser.InitDeclaratorListContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#initDeclarator.
    def enterInitDeclarator(self, ctx:CParser.InitDeclaratorContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#initDeclarator.
    def exitInitDeclarator(self, ctx:CParser.InitDeclaratorContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#storageClassSpecifier.
    def enterStorageClassSpecifier(self, ctx:CParser.StorageClassSpecifierContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#storageClassSpecifier.
    def exitStorageClassSpecifier(self, ctx:CParser.StorageClassSpecifierContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#typeSpecifier.
    def enterTypeSpecifier(self, ctx:CParser.TypeSpecifierContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#typeSpecifier.
    def exitTypeSpecifier(self, ctx:CParser.TypeSpecifierContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#structOrUnionSpecifier.
    def enterStructOrUnionSpecifier(self, ctx:CParser.StructOrUnionSpecifierContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#structOrUnionSpecifier.
    def exitStructOrUnionSpecifier(self, ctx:CParser.StructOrUnionSpecifierContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#structOrUnion.
    def enterStructOrUnion(self, ctx:CParser.StructOrUnionContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#structOrUnion.
    def exitStructOrUnion(self, ctx:CParser.StructOrUnionContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#structDeclarationList.
    def enterStructDeclarationList(self, ctx:CParser.StructDeclarationListContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#structDeclarationList.
    def exitStructDeclarationList(self, ctx:CParser.StructDeclarationListContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#structDeclaration.
    def enterStructDeclaration(self, ctx:CParser.StructDeclarationContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#structDeclaration.
    def exitStructDeclaration(self, ctx:CParser.StructDeclarationContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#specifierQualifierList.
    def enterSpecifierQualifierList(self, ctx:CParser.SpecifierQualifierListContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#specifierQualifierList.
    def exitSpecifierQualifierList(self, ctx:CParser.SpecifierQualifierListContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#structDeclaratorList.
    def enterStructDeclaratorList(self, ctx:CParser.StructDeclaratorListContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#structDeclaratorList.
    def exitStructDeclaratorList(self, ctx:CParser.StructDeclaratorListContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#structDeclarator.
    def enterStructDeclarator(self, ctx:CParser.StructDeclaratorContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#structDeclarator.
    def exitStructDeclarator(self, ctx:CParser.StructDeclaratorContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#enumSpecifier.
    def enterEnumSpecifier(self, ctx:CParser.EnumSpecifierContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#enumSpecifier.
    def exitEnumSpecifier(self, ctx:CParser.EnumSpecifierContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#enumeratorList.
    def enterEnumeratorList(self, ctx:CParser.EnumeratorListContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#enumeratorList.
    def exitEnumeratorList(self, ctx:CParser.EnumeratorListContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#enumerator.
    def enterEnumerator(self, ctx:CParser.EnumeratorContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#enumerator.
    def exitEnumerator(self, ctx:CParser.EnumeratorContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#enumerationConstant.
    def enterEnumerationConstant(self, ctx:CParser.EnumerationConstantContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#enumerationConstant.
    def exitEnumerationConstant(self, ctx:CParser.EnumerationConstantContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#atomicTypeSpecifier.
    def enterAtomicTypeSpecifier(self, ctx:CParser.AtomicTypeSpecifierContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#atomicTypeSpecifier.
    def exitAtomicTypeSpecifier(self, ctx:CParser.AtomicTypeSpecifierContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#typeQualifier.
    def enterTypeQualifier(self, ctx:CParser.TypeQualifierContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#typeQualifier.
    def exitTypeQualifier(self, ctx:CParser.TypeQualifierContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#functionSpecifier.
    def enterFunctionSpecifier(self, ctx:CParser.FunctionSpecifierContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#functionSpecifier.
    def exitFunctionSpecifier(self, ctx:CParser.FunctionSpecifierContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#alignmentSpecifier.
    def enterAlignmentSpecifier(self, ctx:CParser.AlignmentSpecifierContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#alignmentSpecifier.
    def exitAlignmentSpecifier(self, ctx:CParser.AlignmentSpecifierContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#declarator.
    def enterDeclarator(self, ctx:CParser.DeclaratorContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#declarator.
    def exitDeclarator(self, ctx:CParser.DeclaratorContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#directDeclarator.
    def enterDirectDeclarator(self, ctx:CParser.DirectDeclaratorContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#directDeclarator.
    def exitDirectDeclarator(self, ctx:CParser.DirectDeclaratorContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#gccDeclaratorExtension.
    def enterGccDeclaratorExtension(self, ctx:CParser.GccDeclaratorExtensionContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#gccDeclaratorExtension.
    def exitGccDeclaratorExtension(self, ctx:CParser.GccDeclaratorExtensionContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#gccAttributeSpecifier.
    def enterGccAttributeSpecifier(self, ctx:CParser.GccAttributeSpecifierContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#gccAttributeSpecifier.
    def exitGccAttributeSpecifier(self, ctx:CParser.GccAttributeSpecifierContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#gccAttributeList.
    def enterGccAttributeList(self, ctx:CParser.GccAttributeListContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#gccAttributeList.
    def exitGccAttributeList(self, ctx:CParser.GccAttributeListContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#gccAttribute.
    def enterGccAttribute(self, ctx:CParser.GccAttributeContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#gccAttribute.
    def exitGccAttribute(self, ctx:CParser.GccAttributeContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#nestedParenthesesBlock.
    def enterNestedParenthesesBlock(self, ctx:CParser.NestedParenthesesBlockContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#nestedParenthesesBlock.
    def exitNestedParenthesesBlock(self, ctx:CParser.NestedParenthesesBlockContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#pointer.
    def enterPointer(self, ctx:CParser.PointerContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#pointer.
    def exitPointer(self, ctx:CParser.PointerContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#typeQualifierList.
    def enterTypeQualifierList(self, ctx:CParser.TypeQualifierListContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#typeQualifierList.
    def exitTypeQualifierList(self, ctx:CParser.TypeQualifierListContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#parameterTypeList.
    def enterParameterTypeList(self, ctx:CParser.ParameterTypeListContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#parameterTypeList.
    def exitParameterTypeList(self, ctx:CParser.ParameterTypeListContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#parameterList.
    def enterParameterList(self, ctx:CParser.ParameterListContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#parameterList.
    def exitParameterList(self, ctx:CParser.ParameterListContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#parameterDeclaration.
    def enterParameterDeclaration(self, ctx:CParser.ParameterDeclarationContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#parameterDeclaration.
    def exitParameterDeclaration(self, ctx:CParser.ParameterDeclarationContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#identifierList.
    def enterIdentifierList(self, ctx:CParser.IdentifierListContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#identifierList.
    def exitIdentifierList(self, ctx:CParser.IdentifierListContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#typeName.
    def enterTypeName(self, ctx:CParser.TypeNameContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#typeName.
    def exitTypeName(self, ctx:CParser.TypeNameContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#abstractDeclarator.
    def enterAbstractDeclarator(self, ctx:CParser.AbstractDeclaratorContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#abstractDeclarator.
    def exitAbstractDeclarator(self, ctx:CParser.AbstractDeclaratorContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#directAbstractDeclarator.
    def enterDirectAbstractDeclarator(self, ctx:CParser.DirectAbstractDeclaratorContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#directAbstractDeclarator.
    def exitDirectAbstractDeclarator(self, ctx:CParser.DirectAbstractDeclaratorContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#typedefName.
    def enterTypedefName(self, ctx:CParser.TypedefNameContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#typedefName.
    def exitTypedefName(self, ctx:CParser.TypedefNameContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#initializer.
    def enterInitializer(self, ctx:CParser.InitializerContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#initializer.
    def exitInitializer(self, ctx:CParser.InitializerContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#initializerList.
    def enterInitializerList(self, ctx:CParser.InitializerListContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#initializerList.
    def exitInitializerList(self, ctx:CParser.InitializerListContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#designation.
    def enterDesignation(self, ctx:CParser.DesignationContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#designation.
    def exitDesignation(self, ctx:CParser.DesignationContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#designatorList.
    def enterDesignatorList(self, ctx:CParser.DesignatorListContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#designatorList.
    def exitDesignatorList(self, ctx:CParser.DesignatorListContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#designator.
    def enterDesignator(self, ctx:CParser.DesignatorContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#designator.
    def exitDesignator(self, ctx:CParser.DesignatorContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#staticAssertDeclaration.
    def enterStaticAssertDeclaration(self, ctx:CParser.StaticAssertDeclarationContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#staticAssertDeclaration.
    def exitStaticAssertDeclaration(self, ctx:CParser.StaticAssertDeclarationContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#statement.
    def enterStatement(self, ctx:CParser.StatementContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#statement.
    def exitStatement(self, ctx:CParser.StatementContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#labeledStatement.
    def enterLabeledStatement(self, ctx:CParser.LabeledStatementContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#labeledStatement.
    def exitLabeledStatement(self, ctx:CParser.LabeledStatementContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#compoundStatement.
    def enterCompoundStatement(self, ctx:CParser.CompoundStatementContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#compoundStatement.
    def exitCompoundStatement(self, ctx:CParser.CompoundStatementContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#blockItemList.
    def enterBlockItemList(self, ctx:CParser.BlockItemListContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#blockItemList.
    def exitBlockItemList(self, ctx:CParser.BlockItemListContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#blockItem.
    def enterBlockItem(self, ctx:CParser.BlockItemContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#blockItem.
    def exitBlockItem(self, ctx:CParser.BlockItemContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#expressionStatement.
    def enterExpressionStatement(self, ctx:CParser.ExpressionStatementContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#expressionStatement.
    def exitExpressionStatement(self, ctx:CParser.ExpressionStatementContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#selectionStatement.
    def enterSelectionStatement(self, ctx:CParser.SelectionStatementContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#selectionStatement.
    def exitSelectionStatement(self, ctx:CParser.SelectionStatementContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#iterationStatement.
    def enterIterationStatement(self, ctx:CParser.IterationStatementContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#iterationStatement.
    def exitIterationStatement(self, ctx:CParser.IterationStatementContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#forCondition.
    def enterForCondition(self, ctx:CParser.ForConditionContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#forCondition.
    def exitForCondition(self, ctx:CParser.ForConditionContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#forDeclaration.
    def enterForDeclaration(self, ctx:CParser.ForDeclarationContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#forDeclaration.
    def exitForDeclaration(self, ctx:CParser.ForDeclarationContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#forExpression.
    def enterForExpression(self, ctx:CParser.ForExpressionContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#forExpression.
    def exitForExpression(self, ctx:CParser.ForExpressionContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#jumpStatement.
    def enterJumpStatement(self, ctx:CParser.JumpStatementContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#jumpStatement.
    def exitJumpStatement(self, ctx:CParser.JumpStatementContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#translationUnit.
    def enterTranslationUnit(self, ctx:CParser.TranslationUnitContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#translationUnit.
    def exitTranslationUnit(self, ctx:CParser.TranslationUnitContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#externalDeclaration.
    def enterExternalDeclaration(self, ctx:CParser.ExternalDeclarationContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#externalDeclaration.
    def exitExternalDeclaration(self, ctx:CParser.ExternalDeclarationContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#functionDefinition.
    def enterFunctionDefinition(self, ctx:CParser.FunctionDefinitionContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#functionDefinition.
    def exitFunctionDefinition(self, ctx:CParser.FunctionDefinitionContext):
        self.exit_rule(ctx)


    # Enter a parse tree produced by CParser#declarationList.
    def enterDeclarationList(self, ctx:CParser.DeclarationListContext):
        self.enter_rule(ctx)

    # Exit a parse tree produced by CParser#declarationList.
    def exitDeclarationList(self, ctx:CParser.DeclarationListContext):
        self.exit_rule(ctx)
