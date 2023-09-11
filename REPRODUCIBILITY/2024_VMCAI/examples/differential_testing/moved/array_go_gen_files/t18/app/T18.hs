module T18 where
import BehaviorTreeCore
import BTreeC1
import BTreeA1
import BTreeA4
bTreeNodeA4 = BTreeNode bTreeFunctionA4 [] 3
bTreeNodeC1 = BTreeNode bTreeFunctionC1 [] 4
bTreeNodeA1 = BTreeNode bTreeFunctionA1 [] 5
bTreeNodePOne2 = BTreeNode (parallelCreator successOnOneFailureOne) [bTreeNodeA4, bTreeNodeC1, bTreeNodeA1] 2
bTreeNodeA4_1 = BTreeNode bTreeFunctionA4 [] 6
bTreeNodePAll1 = BTreeNode (parallelCreator successOnAllFailureOne) [bTreeNodePOne2, bTreeNodeA4_1] 1
bTreeNodeDecRf0 = BTreeNode (decoratorCreator (xISyCreator Running Failure)) [bTreeNodePAll1] 0
