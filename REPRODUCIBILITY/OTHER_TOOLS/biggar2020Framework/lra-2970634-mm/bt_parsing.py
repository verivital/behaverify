# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 10:24:15 2019

Parsing module for a BT

@author: Oliver Biggar
"""

from pyparsing import infixNotation, opAssoc, Word, alphas

# define classes to be built at parse time, as each matching
# expression type is parsed
    
class BehaviourOperand(object):
    
    def __init__(self,t):
        self.token = t[0]
        
    def __str__(self):
        return self.token

class BinOp(object):
    def __init__(self,t):
        self.args = t[0][0::2]
        self.left = t[0][0]
        self.right = t[0][2]
    def __str__(self):
        sep = " %s " % self.reprsymbol
        return "(" + sep.join(map(str,self.args)) + ")"
    __repr__ = __str__

class Sequence(BinOp):
    reprsymbol = '->'

class Fallback(BinOp):
    reprsymbol = '?'
    
class BoolAnd(BinOp):
    reprsymbol = '&'
    
class PrlSequence(BinOp):
    reprsymbol = '=>>'
    
class BoolOr(BinOp):
    reprsymbol = '|'
    
class BoolNot(object):
    def __init__(self,t):
        self.arg = t[0][1]
    def __str__(self):
        return "!" + str(self.arg)
    __repr__ = __str__

#TRUE = Keyword("True")
#FALSE = Keyword("False")
behOperand = Word(alphas,max=20)
behOperand.setParseAction(BehaviourOperand)

# define expression, based on expression operand and
# list of operations in precedence order
btExpr = infixNotation( behOperand,
    [
    ("!", 1, opAssoc.RIGHT, BoolNot),
    ('&',2,opAssoc.RIGHT, BoolAnd),
    ('|',2,opAssoc.RIGHT, BoolOr),
    ("->", 2, opAssoc.RIGHT, Sequence),
    ("?", 2, opAssoc.RIGHT,  Fallback),
    ("=>>",2,opAssoc.RIGHT,PrlSequence)
    ])

def parse_bt(bt_exp):
    
    return btExpr.parseString(bt_exp)

if __name__ == "__main__":
    
    tests = ["p -> q",
             "p ? q",
             "p ? (q -> r)",
             "a ? b ? c ? d",
             "a -> (b ? a)",
             "a ? b -> c",
             "!a -> b",
             "!(a-> b)",
             "a -> b ? c",
             "a ? b -> c",
             "(a&b) | c",
             "a -> b -> c",
             "a =>> b"]
    
    for t in tests:
        
        print(btExpr.parseString(t),type(btExpr.parseString(t)[0]))

