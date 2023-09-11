module T2 where
import BehaviorTreeCore
import BTreeC1
import BTreeA4
bTreeNodeC1 = BTreeNode bTreeFunctionC1 [] 2
bTreeNodeDecRs1 = BTreeNode (decoratorCreator (xISyCreator Running Success)) [bTreeNodeC1] 1
bTreeNodeA4 = BTreeNode bTreeFunctionA4 [] 5
bTreeNodeC1_1 = BTreeNode bTreeFunctionC1 [] 6
bTreeNodeC1_2 = BTreeNode bTreeFunctionC1 [] 7
bTreeNodeSel3 = BTreeNode selectorFunc [bTreeNodeA4, bTreeNodeC1_1, bTreeNodeC1_2] 4
bTreeNodeDecRf2 = BTreeNode (decoratorCreator (xISyCreator Running Failure)) [bTreeNodeSel3] 3
bTreeNodeSeq0 = BTreeNode sequencePartialMemoryFunc [bTreeNodeDecRs1, bTreeNodeDecRf2] 0
