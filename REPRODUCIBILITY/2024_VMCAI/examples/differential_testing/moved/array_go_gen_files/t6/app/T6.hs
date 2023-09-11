module T6 where
import BehaviorTreeCore
import BTreeC2
import BTreeA1
import BTreeA2
import BTreeA4
bTreeNodeA2 = BTreeNode bTreeFunctionA2 [] 2
bTreeNodeC2 = BTreeNode bTreeFunctionC2 [] 3
bTreeNodeA4 = BTreeNode bTreeFunctionA4 [] 5
bTreeNodeA1 = BTreeNode bTreeFunctionA1 [] 6
bTreeNodePOne2 = BTreeNode (parallelCreator successOnOneFailureOne) [bTreeNodeA4, bTreeNodeA1] 4
bTreeNodePAll1 = BTreeNode (parallelCreator successOnAllFailureOne) [bTreeNodeA2, bTreeNodeC2, bTreeNodePOne2] 1
bTreeNodeDecSf0 = BTreeNode (decoratorCreator (xISyCreator Success Failure)) [bTreeNodePAll1] 0
