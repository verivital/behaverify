module T13 where
import BehaviorTreeCore
import BTreeC1
import BTreeA3
import BTreeA4
bTreeNodeA3 = BTreeNode bTreeFunctionA3 [] 1
bTreeNodeC1 = BTreeNode bTreeFunctionC1 [] 2
bTreeNodeA4 = BTreeNode bTreeFunctionA4 [] 3
bTreeNodePAll0 = BTreeNode (parallelCreator successOnAllFailureOne) [bTreeNodeA3, bTreeNodeC1, bTreeNodeA4] 0
