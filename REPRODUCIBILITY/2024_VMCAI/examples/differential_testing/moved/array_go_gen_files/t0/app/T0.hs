module T0 where
import BehaviorTreeCore
import BTreeC2
import BTreeA4
bTreeNodeA4 = BTreeNode bTreeFunctionA4 [] 2
bTreeNodeC2 = BTreeNode bTreeFunctionC2 [] 3
bTreeNodePOne1 = BTreeNode (parallelCreator successOnOneFailureOne) [bTreeNodeA4, bTreeNodeC2] 1
bTreeNodeDecSr0 = BTreeNode (decoratorCreator (xISyCreator Success Running)) [bTreeNodePOne1] 0
