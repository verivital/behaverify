module T14 where
import BehaviorTreeCore
import BTreeC2
import BTreeA1
bTreeNodeA1 = BTreeNode bTreeFunctionA1 [] 2
bTreeNodeC2 = BTreeNode bTreeFunctionC2 [] 3
bTreeNodePOne1 = BTreeNode (parallelCreator successOnOneFailureOne) [bTreeNodeA1, bTreeNodeC2] 1
bTreeNodeDecRf0 = BTreeNode (decoratorCreator (xISyCreator Running Failure)) [bTreeNodePOne1] 0
