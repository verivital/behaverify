module T1 where
import BehaviorTreeCore
import BTreeC1
import BTreeA1
import BTreeA3
import BTreeA4
bTreeNodeA3 = BTreeNode bTreeFunctionA3 [] 1
bTreeNodeC1 = BTreeNode bTreeFunctionC1 [] 3
bTreeNodeDecSf1 = BTreeNode (decoratorCreator (xISyCreator Success Failure)) [bTreeNodeC1] 2
bTreeNodeA1 = BTreeNode bTreeFunctionA1 [] 6
bTreeNodeA4 = BTreeNode bTreeFunctionA4 [] 7
bTreeNodeC1_1 = BTreeNode bTreeFunctionC1 [] 8
bTreeNodePOne3 = BTreeNode (parallelCreator successOnOneFailureOne) [bTreeNodeA1, bTreeNodeA4, bTreeNodeC1_1] 5
bTreeNodeDecSr2 = BTreeNode (decoratorCreator (xISyCreator Success Running)) [bTreeNodePOne3] 4
bTreeNodePOne0 = BTreeNode (parallelCreator successOnOneFailureOne) [bTreeNodeA3, bTreeNodeDecSf1, bTreeNodeDecSr2] 0
