"""HashedNode is a language independent node in the hashed Abstract Syntax Tree."""

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
        self.rule_name = parser.ruleNames[ctx.getRuleIndex()]
        self.sub_tree_size = 1

    def __str__(self, level=0):
        """Print full subtree to terminal with hash values."""
        ret = "\t"*level+repr(f"{self.rule_name} => {self.hash_value}")+"\n"
        for child in self.children:
            ret += child.__str__(level+1)
        return ret

    def __repr__(self):
        return '<Hashed Node>'

    def add_child(self, ctx:ParserRuleContext):
        """Add a child to this node."""
        child = HashedNode(ctx, parent=self)
        self.children.append(child)
        return child

    def hash(self):
        """
        Hash the current node.

        hash_value is an MD5 hash of the CTX type, summed with the hash
        value of all children (invariant over reorderings).

        hash_exact is an MD5 hash of the CTX type, appended to the hash
        values of all children and then hashed again (variant over reorderings).

        This function expects the child nodes to already have a hash value
        (call in upwards pass of tree traversal).
        """
        tmp_hash = tmp_hash_exact = hashlib.md5(self.rule_name.encode()).hexdigest()
        for child in self.children:
            tmp_hash = hex(int(tmp_hash, 16) + int(child.hash_value, 16))
            tmp_hash_exact += child.exact_hash  # string append
        self.hash_value = tmp_hash
        self.exact_hash = hashlib.md5(tmp_hash_exact.encode()).hexdigest()

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
