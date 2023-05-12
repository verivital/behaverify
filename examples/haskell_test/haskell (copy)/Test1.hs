module Test1 where
import Behavior_tree_core
import X_less_than_5_file
import Action1_file
import Action2_file
x_less_than_5__node = Node x_less_than_5 []
action1__node = Node action1 []
default_attempt__node = Node sequenceFunc [x_less_than_5__node, action1__node]
action2__node = Node action2 []
root_sel__node = Node selectorFunc [default_attempt__node, action2__node]
