import py_trees
import operator

def create_root(print_pic=False):


    seq = py_trees.composites.Sequence('CookiePlan')
    sel = py_trees.composites.Selector('AcquireCookies')
    eat = py_trees.behaviours.SetBlackboardVariable("cookies", 0, name="EatCookie")    
    buy = py_trees.behaviours.SetBlackboardVariable("cookies", 1, name="BuyCookies")
    check = py_trees.behaviours.CheckBlackboardVariableValue(py_trees.common.ComparisonExpression("cookies", 0, operator.gt), "CheckCookies")
    seq.add_children([sel, eat])
    sel.add_children([check, buy])
                                                             
    if print_pic:
        py_trees.display.render_dot_tree(seq, with_blackboard_variables=True, target_directory = '../pictures')#works
    return seq

create_root(True)
