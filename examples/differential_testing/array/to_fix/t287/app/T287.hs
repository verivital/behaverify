module T287 where
import BehaviorTreeCore
import BTreeC1
import BTreeA1
import BTreeA2
import BTreeA4
bTreeNodeA1 = BTreeNode bTreeFunctionA1 [] 2
bTreeNodeA2 = BTreeNode bTreeFunctionA2 [] 4
bTreeNodeDecInv2 = BTreeNode (decoratorCreator inverterCreator) [bTreeNodeA2] 3
bTreeNodeA4 = BTreeNode bTreeFunctionA4 [] 6
bTreeNodeDecRf3 = BTreeNode (decoratorCreator (xISyCreator Running Failure)) [bTreeNodeA4] 5
bTreeNodePOne1 = BTreeNode (parallelCreator successOnOneFailureOne) [bTreeNodeA1, bTreeNodeDecInv2, bTreeNodeDecRf3] 1
bTreeNodeC1 = BTreeNode bTreeFunctionC1 [] 7
bTreeNodePOne0 = BTreeNode (parallelCreator successOnOneFailureOne) [bTreeNodePOne1, bTreeNodeC1] 0
