module Test1 where
import Behavior_tree_core
import X_less_than_5_file
import Action1_file
import Action2_file
x_less_than_5__node = BTreeNode x_less_than_5 [] 2
action1__node = BTreeNode action1 [] 3
default_attempt__node = BTreeNode sequenceFunc [x_less_than_5__node, action1__node] 1
action2__node = BTreeNode action2 [] 4
root_sel__node = BTreeNode selectorFunc [default_attempt__node, action2__node] 0
