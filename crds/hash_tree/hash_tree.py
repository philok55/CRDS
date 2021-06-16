"""HashedNode is a language independent node in the hashed Abstract Syntax Tree."""

from parsers.python3.Python3Parser import Python3Parser
from parsers.C.CParser import CParser
import hashlib
from antlr4 import ParserRuleContext


class HashedNode():
    """HashedNode is a node in the hashed Abstract Syntax Tree."""
    def __init__(self, ctx, parent=None, parser=None):
        """
        To define which language to expect, pass either
        a parent node or an ANTLR generated parser.
        """
        if parser is None:
            parser=parent.parser
        self.parser=parser
        self.parent = parent
        self.children = []
        self.ctx = ctx
        self.hash_value = None
        self.exact_hash = None
        self.names_hash_exact = None
        self.rule_name = parser.ruleNames[ctx.getRuleIndex()]
        self.sub_tree_size = 1

    def __str__(self, level=0):
        """
        Build a printable string of the full subtree
        below this node, including hash values.
        """
        ret = "\t"*level+repr(f"{self.rule_name} => {self.hash_value}")+"\n"
        for child in self.children:
            ret += child.__str__(level+1)
        return ret

    def __repr__(self):
        return f'<Hashed Node>'

    def add_child(self, ctx:ParserRuleContext):
        """Add a new child to this node."""
        child = HashedNode(ctx, parent=self)
        self.children.append(child)
        return child

    def hash(self):
        """
        Hash the current node.

        hash_value is an MD5 hash of the CTX type, summed with the hash
        value of all children (invariant over reorderings).

        hash_exact is an MD5 hash of the CTX type, appended to the hash
        values of all children and then re-hashed (not invariant over reorderings).

        This function expects the child nodes to already have a hash value
        (call in upwards pass of tree traversal).
        """
        hashable = self.rule_name
        if type(self.ctx) == Python3Parser.TfpdefContext:
            hashable = self.rule_name + self.ctx.NAME().getText()

        if type(self.ctx) == CParser.DirectDeclaratorContext:
            if type(self.parent.ctx) == CParser.ParameterDeclarationContext:
                hashable = self.rule_name + self.ctx.Identifier().getText()

        tmp_hash = tmp_hash_exact = hashlib.md5(self.rule_name.encode()).hexdigest()
        names = names_exact = hashlib.md5(hashable.encode()).hexdigest()

        for child in self.children:
            # Remove Python-prepended '0x' and clip to 32 characters (mod 2^128)
            tmp_hash = hex(int(tmp_hash, 16) + int(child.hash_value, 16))[2:][-32:]
            tmp_hash = tmp_hash.rjust(32, '0')  # Fill with leading zeros to match md5 length
            names = hex(int(names, 16) + int(child.names_hash, 16))[2:][-32:]
            names = names.rjust(32, '0')  # Fill with leading zeros to match md5 length
            tmp_hash_exact += child.exact_hash  # string append
            names_exact += child.names_hash_exact  # string append
        self.hash_value = tmp_hash
        self.names_hash = names
        self.exact_hash = hashlib.md5(tmp_hash_exact.encode()).hexdigest()
        self.names_hash_exact = hashlib.md5(names_exact.encode()).hexdigest()

    def set_subtree_size(self):
        """
        Set size of sub tree (sum of sizes of children + 1).

        This function expects the child nodes to already have a size
        (call in upwards pass of tree traversal).
        """
        self.sub_tree_size = 1
        for child in self.children:
            self.sub_tree_size += child.sub_tree_size
        return self.sub_tree_size

    def get_file_location(self):
        """Returns the file location of the subtree below this node."""
        return ((self.ctx.start.line, self.ctx.start.column),
                (self.ctx.stop.line, self.ctx.stop.column))

    def get_children(self):
        return self.children
