module T5 where
import BehaviorTreeCore
import BTreeA1
import BTreeA2
import BTreeA3
bTreeNodeA1 = BTreeNode bTreeFunctionA1 [] 2
bTreeNodeA2 = BTreeNode bTreeFunctionA2 [] 3
bTreeNodeA3 = BTreeNode bTreeFunctionA3 [] 4
bTreeNodeSel1 = BTreeNode selectorFunc [bTreeNodeA1, bTreeNodeA2, bTreeNodeA3] 1
bTreeNodeDecRs0 = BTreeNode (decoratorCreator (xISyCreator Running Success)) [bTreeNodeSel1] 0
