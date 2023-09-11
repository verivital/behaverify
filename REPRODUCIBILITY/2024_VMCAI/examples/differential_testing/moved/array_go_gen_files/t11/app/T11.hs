module T11 where
import BehaviorTreeCore
import BTreeA1
import BTreeA2
bTreeNodeA2 = BTreeNode bTreeFunctionA2 [] 1
bTreeNodeA2_1 = BTreeNode bTreeFunctionA2 [] 3
bTreeNodeA1 = BTreeNode bTreeFunctionA1 [] 4
bTreeNodePAll1 = BTreeNode (parallelPartialMemoryCreator successOnAllFailureOne) [bTreeNodeA2_1, bTreeNodeA1] 2
bTreeNodePAll0 = BTreeNode (parallelCreator successOnAllFailureOne) [bTreeNodeA2, bTreeNodePAll1] 0
