module T9 where
import BehaviorTreeCore
import BTreeC1
import BTreeA1
import BTreeA4
bTreeNodeC1 = BTreeNode bTreeFunctionC1 [] 1
bTreeNodeA1 = BTreeNode bTreeFunctionA1 [] 3
bTreeNodeA4 = BTreeNode bTreeFunctionA4 [] 4
bTreeNodePAll1 = BTreeNode (parallelCreator successOnAllFailureOne) [bTreeNodeA1, bTreeNodeA4] 2
bTreeNodePOne0 = BTreeNode (parallelCreator successOnOneFailureOne) [bTreeNodeC1, bTreeNodePAll1] 0
