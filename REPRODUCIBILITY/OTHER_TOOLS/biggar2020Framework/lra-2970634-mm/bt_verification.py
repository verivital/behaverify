"""
Created on Thu Jan 17 08:25:41 2019

Behaviour Tree verification module

@author: Oliver Biggar
"""

import spot
from bt_parsing import parse_bt , BehaviourOperand, Sequence,Fallback,BoolNot,PrlSequence
spot.setup()

#False constant
FALSE = spot.formula.ff()
#True constant
TRUE = spot.formula.tt()

class Behaviour(object):
    
    """Class representing a behaviour"""
    
    def __init__(self,name,succ,fail,guar,inv=[],varying=None,r_o_e = set()):
        """name is a string, and all other arguments are strings representing
        formulas."""
        self.name = name
        self.success = spot.formula(succ)
        self.failure = spot.formula(fail)
        self.guarantee = spot.formula(guar)
        self.eventually = set()
        self.region_of_effect = r_o_e
        self.varying = set(spot.atomic_prop_collect(self.guarantee))
        if varying:
            self.varying |= {spot.formula(s) for s in varying}
        self.inv = {spot.formula(x) for x in inv}
        self.add_invariance()
        self._get_eventually()
        
    def __repr__(self):
        return self.name
    
    def _get_eventually(self):
        
        self.eventually.clear()
        self._rec_get_eventually(self.guarantee.simplify(),spot.formula.tt())
            
    def _rec_get_eventually(self,formula,path):
        if formula.is_literal():
            return
        elif formula.kind() is spot.op_Or:
            for child in formula:
                other_not = [spot.formula.Not(x) for x in formula if not x == child ]
                other_not.append(path)
                self._rec_get_eventually(child,spot.formula.And(other_not))
        elif formula.kind() is spot.op_F:
            self.eventually.add((formula.get_child_of(spot.op_F),path))
            return
        else:
            for child in formula:
                self._rec_get_eventually(child,path)
                
    def add_invariance(self,vbls=None):
        """Makes invariance conditions explicit in guarantee"""
        if vbls:
            self.inv |= vbls
            vs = vbls
        else:
            vs = self.inv
        current = self.guarantee
    
        for v in vs:
            tmp = spot.formula.Or((spot.formula.And((v,spot.formula.X(v))),
                                   spot.formula.And((spot.formula.Not(v),spot.formula.X(spot.formula.Not(v))))))
            current = spot.formula.And((current,tmp))
        self.guarantee = current
                
    def variables(self):
        
        return set(spot.atomic_prop_collect(self.guarantee)) | set(spot.atomic_prop_collect(self.success)) | set(spot.atomic_prop_collect(self.failure))
               
    def act(state):
        pass

class Condition(Behaviour):
    """Shortcut for creating a condition behaviour."""
    
    def __init__(self,name,condition=None):
        if condition:
            cond = spot.formula(condition)
        else:
            cond = spot.formula(name)
        Behaviour.__init__(self,str(name),cond,spot.formula.Not(cond),FALSE)

def idle():
    
    return Behaviour('idle',FALSE,FALSE,TRUE)

IDLE = idle() #singleton


def get_behaviour_from_tree(expr_string,bhvr_dict):
    """Parses tree given by expr_string and returns a behaviour representing
    the tree. All names of behaviours in expr_string must be in bhvr_dict."""
    ast = parse_bt(expr_string)[0]
    return _rec_eval(ast,bhvr_dict)


def _rec_eval(tree,bhvr_dict):
    
    #Recursively constructs the tree from its parse tree.
    if isinstance(tree,BehaviourOperand):
        if tree.token in bhvr_dict:
            return bhvr_dict[tree.token]
        else:
            return Condition(str(tree))
    
    if isinstance(tree,Sequence):
        #print("a sequence")
        b_left = _rec_eval(tree.left,bhvr_dict)
        b_right = _rec_eval(tree.right,bhvr_dict)
        b = sequence(b_left,b_right)
        
        #print_behaviour(b)
        return b
    
    if isinstance(tree,Fallback):
        #print("a fallback")
        b_left = _rec_eval(tree.left,bhvr_dict)
        b_right = _rec_eval(tree.right,bhvr_dict)
        b = fallback(b_left,b_right)
        
        #print_behaviour(b)
        return b
    
    if isinstance(tree,BoolNot):
        #print("a negation")
        b = _rec_eval(tree.arg,bhvr_dict)
        new_b = negate(b)
        
        #print_behaviour(new_b)
        return new_b
    if isinstance(tree,PrlSequence):
        b_left = _rec_eval(tree.left,bhvr_dict)
        b_right = _rec_eval(tree.right,bhvr_dict)
        b = parallel_sequence(b_left,b_right)
        
        #print_behaviour(b)
        return b
    else:
        return Condition(str(tree))


def combine(t1,bhvrs):
    """Simplified version of get_behaviour_from_tree. bhvrs is now a list not
    a dictionary."""
    bhvr_dict = {bh.name : bh for bh in bhvrs}
    return get_behaviour_from_tree(t1,bhvr_dict)

def preconditions(tree, subtree, bhvrs):
    
    bhvr_dict = {bh.name : bh for bh in bhvrs}
    ast = parse_bt(tree)[0]
    found, prec = _rec_prec(ast,bhvr_dict,subtree)
    if found:
        return prec
    return False

def _rec_prec(tree, bhvr_dict, subtree):
    
    if isinstance(tree,BehaviourOperand):
        if tree.token == subtree:
            return (True, spot.formula.tt())
        else:
            return (False, spot.formula.ff())
    
    if isinstance(tree,Sequence):
        #print("a sequence")
        is_q_left, L_cond = _rec_prec(tree.left,bhvr_dict, subtree)
        is_q_right, R_cond = _rec_prec(tree.right,bhvr_dict, subtree)
        if is_q_left:
            return (True, L_cond)
        if is_q_right:
            return (True, spot.formula.And((_rec_eval(tree.right,bhvr_dict).success,R_cond)))
        return (False, spot.formula.ff())
    
    if isinstance(tree,Fallback):
        #print("a fallback")
        is_q_left, L_cond = _rec_prec(tree.left,bhvr_dict, subtree)
        is_q_right, R_cond = _rec_prec(tree.right,bhvr_dict, subtree)
        if is_q_left:
            return (True, L_cond)
        if is_q_right:
            return (True, spot.formula.And((_rec_eval(tree.left,bhvr_dict).failure,R_cond)))
        return (False, spot.formula.ff())
    
    if isinstance(tree,BoolNot):
        return (False, spot.formula.ff())
    
    if isinstance(tree,PrlSequence):
        return (False, spot.formula.ff())

def are_equivalent_behaviour(behaviours,t1,t2):
    """Checks if two BTs represent the same behaviour, and provides counter
    examples if not. Args:
        behaviours:: list of behaviours
        t1 :: string repr. of first tree
        t2 :: string repr. of second tree"""
    
    bhvr_dict = {bh.name : bh for bh in behaviours}
    
    b1 = get_behaviour_from_tree(t1,bhvr_dict)
    b2 = get_behaviour_from_tree(t2,bhvr_dict)
    
    is_equiv = True
    print("Success:")
    if not b1.success.equivalent_to(b2.success):
        print(str(b1.success)+" is not equivalent to "+str(b2.success))
        print(b1.success.translate().exclusive_run(b2.success.translate()))
        is_equiv = False
    else:
        print(str(b1.success)+" is equivalent to "+str(b2.success))
    print("Failure:")
    if not b1.failure.equivalent_to(b2.failure):
        print(str(b1.failure)+" is not equivalent to "+str(b2.failure))
        print(b1.failure.translate().exclusive_run(b2.failure.translate()))
        is_equiv = False
    else:
        print(str(b1.failure)+" is equivalent to "+str(b2.failure))
        
    print("Guarantee:")
    if not b1.guarantee.equivalent_to(b2.guarantee):
        print(str(b1.guarantee)+" is not equivalent to "+str(b2.guarantee))
        print(b1.guarantee.translate().exclusive_run(b2.guarantee.translate()))
        is_equiv = False
    else:
        print(str(b1.guarantee)+" is equivalent to "+str(b2.guarantee))
    return is_equiv

def convert_reduce_and(conjuncts):
    formulas = map(spot.formula,conjuncts)
    return spot.formula.And(formulas).simplify()

def entails_fast(f,g):
    """Same as entails, but more efficient and does not print a counterexample"""
    return spot.formula.contains(g,f)

def entails(f, g):
    """Checks if one LTL formula entails another, and producse a counterexample
        if not."""
    if spot.formula.contains(g,f):
        return True
    print("Not satisfied. One counterexample is")
    a_f = spot.translate(f)
    a_ng = spot.translate(spot.formula.Not(g))
    prod = spot.product(a_f,a_ng)
    print(prod.accepting_run())
    return False

def satisfies_fast(sf, sg):
    """Same as entails_fast, but takes strings as arguments"""
    return entails_fast(spot.formula(sf),spot.formula(sg))

def satisfies(sf, sg):
    """Same as entails, but takes strings as arguments"""
    return entails(spot.formula(sf),spot.formula(sg))

def succ(behaviour):
    return behaviour.success

def fail(behaviour):
    return behaviour.failure

def guar(behaviour):
    return behaviour.guarantee

def sequence(A,B):
    """returns sequence composition of A and B"""
    success = spot.formula.And((A.success,B.success)).simplify()
    failure = spot.formula.Or((A.failure,spot.formula.And((A.success,B.failure)))).simplify()
    guarantee = spot.formula.Or((spot.formula.And((spot.formula.Not(A.failure),
                                                   spot.formula.Not(A.success),
                                                   A.guarantee)),
                                 spot.formula.And((A.success,
                                                   spot.formula.Not(B.failure),
                                                   spot.formula.Not(B.success),B.guarantee)))).simplify()
    
    return Behaviour("("+A.name+") -> ("+B.name+")",success,failure,guarantee)


def fallback(A,B):
    """returns fallback composition of A and B"""
    success = spot.formula.Or((A.success,spot.formula.And((A.failure,B.success)))).simplify()
    failure = spot.formula.And((A.failure,B.failure)).simplify()
    guarantee = spot.formula.Or((spot.formula.And((spot.formula.Not(A.failure),
                                                   spot.formula.Not(A.success),
                                                   A.guarantee)),
                                 spot.formula.And((A.failure,
                                                   spot.formula.Not(B.failure),
                                                   spot.formula.Not(B.success),B.guarantee)))).simplify()
    
    return Behaviour("("+A.name+") ? ("+B.name+")",success,failure,guarantee)

def negate(B):
    """returns negation of B"""
    success = spot.formula.Not(B.success)
    failure = spot.formula.Not(B.failure)
    
    return Behaviour("!"+B.name,success,failure,B.guarantee)

def parallel_sequence(A,B):
    """returns parallel sequence composition of A and B"""
    success = spot.formula.And((A.success,B.success)).simplify()
    failure = spot.formula.Or((A.failure,B.failure)).simplify()
        
    guarantee = spot.formula.And((spot.formula.Not(A.failure),
                                  spot.formula.Not(B.failure),
                                  spot.formula.Or((spot.formula.And((spot.formula.Not(A.success),
                                                                     B.success,
                                                                     A.guarantee)),
                                                   spot.formula.And((A.success,
                                                                     spot.formula.Not(B.success),
                                                                     B.guarantee)),
                                                   spot.formula.And((spot.formula.Not(A.success),
                                                                     spot.formula.Not(B.success),
                                                                     A.guarantee,
                                                                     B.guarantee))
                                                 ))
                                  ))
    
    return Behaviour("("+A.name+") =>> ("+B.name+")",success,failure,guarantee)

def parallel_fallback(A,B):
    
    b = negate(parallel_sequence(negate(A),negate(B)))
    return Behaviour("("+A.name+") ?? ("+B.name+")",b.success,b.failure,b.guarantee)

def parallelizable(b,bs):
    s = set()
    for x in bs:
        if b.varying.isdisjoint(x.varying):
            s.add(x)
    
    return s

def always(formula):
    return spot.formula.G(formula)

def eventually(formula):
    return spot.formula.F(formula)
    
def printif(prop,*string):
    if prop:
        print(*string)

def is_contradiction(formula):
    return FALSE.equivalent_to(formula)

#helper function for debugging
def print_behaviour(b):
    
    print("BEHAVIOR "+b.name)
    print("--SUCC "+str(b.success))
    print("--FAIL "+str(b.failure))
    print("--GUAR "+str(b.guarantee))
