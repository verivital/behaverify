module T12 where
import BehaviorTreeCore
import BTreeA1
import BTreeA4
bTreeNodeA4 = BTreeNode bTreeFunctionA4 [] 1
bTreeNodeA1 = BTreeNode bTreeFunctionA1 [] 2
bTreeNodePAll0 = BTreeNode (parallelPartialMemoryCreator successOnAllFailureOne) [bTreeNodeA4, bTreeNodeA1] 0
