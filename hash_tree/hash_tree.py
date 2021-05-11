import hashlib
from antlr4 import ParserRuleContext

class HashedNode():
    def __init__(self, ctx, parent=None, parser=None):
        if parser is None:
            parser=parent.parser
        self.parser=parser
        self.parent = parent
        self.children = []
        self.ctx = ctx
        self.hash_value = None
        self.rule_name = parser.ruleNames[ctx.getRuleIndex()]
        self.sub_tree_size = 1

    def __str__(self, level=0):
        """Print full subtree to terminal"""
        ret = "\t"*level+repr(f"{self.rule_name} => {self.hash_value}")+"\n"
        for child in self.children:
            ret += child.__str__(level+1)
        return ret

    def __repr__(self):
        return '<Hashed Node>'

    def add_child(self, ctx:ParserRuleContext):
        child = HashedNode(ctx, parent=self)
        self.children.append(child)
        return child

    def hash(self):
        tmp_hash = hashlib.md5(self.rule_name.encode()).hexdigest()
        for child in self.children:
            tmp_hash = hex(int(tmp_hash, 16) + int(child.hash_value, 16))[-32:]
        self.hash_value = tmp_hash

    def set_subtree_size(self):
        for child in self.children:
            self.sub_tree_size += child.sub_tree_size
        return self.sub_tree_size

    def get_file_location(self):
        return ((self.ctx.start.line, self.ctx.start.column), 
                (self.ctx.stop.line, self.ctx.stop.column))
