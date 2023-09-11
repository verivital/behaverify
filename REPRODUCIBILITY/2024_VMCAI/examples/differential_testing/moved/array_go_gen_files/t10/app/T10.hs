module T10 where
import BehaviorTreeCore
import BTreeC1
import BTreeA3
bTreeNodeC1 = BTreeNode bTreeFunctionC1 [] 1
bTreeNodeA3 = BTreeNode bTreeFunctionA3 [] 3
bTreeNodeDecSf1 = BTreeNode (decoratorCreator (xISyCreator Success Failure)) [bTreeNodeA3] 2
bTreeNodePOne0 = BTreeNode (parallelCreator successOnOneFailureOne) [bTreeNodeC1, bTreeNodeDecSf1] 0
