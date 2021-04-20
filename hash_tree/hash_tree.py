import hashlib
from antlr4 import ParserRuleContext
from parsers.python3.Python3Parser import Python3Parser

class HashedNode():
    def __init__(self, ctx, parent=None):
        self.parent = parent
        self.children = []
        self.ctx = ctx
        self.hash_value = None
        self.rule_name = Python3Parser.ruleNames[ctx.getRuleIndex()]

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
        # QUESTION: is the rule name a good value to hash?
        tmp_hash = hashlib.md5(self.rule_name.encode()).hexdigest()
        for child in self.children:
            tmp_hash = hex(int(tmp_hash, 16) + int(child.hash_value, 16))[-32:]
        self.hash_value = tmp_hash
