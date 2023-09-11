module T15 where
import BehaviorTreeCore
import BTreeC1
import BTreeC2
bTreeNodeC2 = BTreeNode bTreeFunctionC2 [] 2
bTreeNodeC1 = BTreeNode bTreeFunctionC1 [] 3
bTreeNodePOne1 = BTreeNode (parallelCreator successOnOneFailureOne) [bTreeNodeC2, bTreeNodeC1] 1
bTreeNodeDecSf0 = BTreeNode (decoratorCreator (xISyCreator Success Failure)) [bTreeNodePOne1] 0
