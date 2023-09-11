module T7 where
import BehaviorTreeCore
import BTreeC1
import BTreeA1
import BTreeA2
import BTreeA4
bTreeNodeA4 = BTreeNode bTreeFunctionA4 [] 2
bTreeNodeA2 = BTreeNode bTreeFunctionA2 [] 3
bTreeNodeA4_1 = BTreeNode bTreeFunctionA4 [] 4
bTreeNodeSel1 = BTreeNode selectorPartialMemoryFunc [bTreeNodeA4, bTreeNodeA2, bTreeNodeA4_1] 1
bTreeNodeA1 = BTreeNode bTreeFunctionA1 [] 5
bTreeNodeC1 = BTreeNode bTreeFunctionC1 [] 6
bTreeNodeSel0 = BTreeNode selectorFunc [bTreeNodeSel1, bTreeNodeA1, bTreeNodeC1] 0
