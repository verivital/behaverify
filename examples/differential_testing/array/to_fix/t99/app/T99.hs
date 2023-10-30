module T99 where
import BehaviorTreeCore
import BTreeC2
import BTreeA1
import BTreeA2
import BTreeA3
bTreeNodeC2 = BTreeNode bTreeFunctionC2 [] 2
bTreeNodeA3 = BTreeNode bTreeFunctionA3 [] 3
bTreeNodeSel1 = BTreeNode selectorFunc [bTreeNodeC2, bTreeNodeA3] 1
bTreeNodeA2 = BTreeNode bTreeFunctionA2 [] 4
bTreeNodeA1 = BTreeNode bTreeFunctionA1 [] 6
bTreeNodeC2_1 = BTreeNode bTreeFunctionC2 [] 7
bTreeNodeC2_2 = BTreeNode bTreeFunctionC2 [] 8
bTreeNodeSel2 = BTreeNode selectorPartialMemoryFunc [bTreeNodeA1, bTreeNodeC2_1, bTreeNodeC2_2] 5
bTreeNodePAll0 = BTreeNode (parallelPartialMemoryCreator successOnAllFailureOne) [bTreeNodeSel1, bTreeNodeA2, bTreeNodeSel2] 0
