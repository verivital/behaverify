import py_trees
import operator

def create_root(print_pic=False):


    par = py_trees.composites.Parallel('Root')
    eat = py_trees.behaviours.SetBlackboardVariable("var", 0, name="Set0") 
    check1 = py_trees.behaviours.CheckBlackboardVariableValue(py_trees.common.ComparisonExpression("var", 0, operator.gt), "IsVar0")   
    buy = py_trees.behaviours.SetBlackboardVariable("var", 1, name="Set1")
    check2 = py_trees.behaviours.CheckBlackboardVariableValue(py_trees.common.ComparisonExpression("var", 0, operator.gt), "IsVar1")   
    par.add_children([eat, check1, buy, check2])
                                                             
    if print_pic:
        py_trees.display.render_dot_tree(par, with_blackboard_variables=True, target_directory = '../pictures')#works
    return par

create_root(True)
