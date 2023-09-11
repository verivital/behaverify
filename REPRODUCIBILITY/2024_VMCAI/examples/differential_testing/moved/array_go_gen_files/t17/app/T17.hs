module T17 where
import BehaviorTreeCore
import BTreeC1
import BTreeC2
import BTreeA1
import BTreeA4
bTreeNodeA1 = BTreeNode bTreeFunctionA1 [] 2
bTreeNodeC2 = BTreeNode bTreeFunctionC2 [] 3
bTreeNodeA4 = BTreeNode bTreeFunctionA4 [] 4
bTreeNodeSel1 = BTreeNode selectorFunc [bTreeNodeA1, bTreeNodeC2, bTreeNodeA4] 1
bTreeNodeA4_1 = BTreeNode bTreeFunctionA4 [] 6
bTreeNodeA1_1 = BTreeNode bTreeFunctionA1 [] 7
bTreeNodePAll2 = BTreeNode (parallelCreator successOnAllFailureOne) [bTreeNodeA4_1, bTreeNodeA1_1] 5
bTreeNodeC1 = BTreeNode bTreeFunctionC1 [] 8
bTreeNodeSel0 = BTreeNode selectorPartialMemoryFunc [bTreeNodeSel1, bTreeNodePAll2, bTreeNodeC1] 0
