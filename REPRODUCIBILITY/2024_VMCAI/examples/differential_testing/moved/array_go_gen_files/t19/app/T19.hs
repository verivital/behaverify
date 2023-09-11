module T19 where
import BehaviorTreeCore
import BTreeC1
import BTreeC2
import BTreeA1
bTreeNodeC1 = BTreeNode bTreeFunctionC1 [] 2
bTreeNodeC2 = BTreeNode bTreeFunctionC2 [] 4
bTreeNodeC1_1 = BTreeNode bTreeFunctionC1 [] 5
bTreeNodeA1 = BTreeNode bTreeFunctionA1 [] 6
bTreeNodePOne2 = BTreeNode (parallelCreator successOnOneFailureOne) [bTreeNodeC2, bTreeNodeC1_1, bTreeNodeA1] 3
bTreeNodeA1_1 = BTreeNode bTreeFunctionA1 [] 8
bTreeNodeC2_1 = BTreeNode bTreeFunctionC2 [] 9
bTreeNodePAll3 = BTreeNode (parallelPartialMemoryCreator successOnAllFailureOne) [bTreeNodeA1_1, bTreeNodeC2_1] 7
bTreeNodeSeq1 = BTreeNode sequencePartialMemoryFunc [bTreeNodeC1, bTreeNodePOne2, bTreeNodePAll3] 1
bTreeNodeC2_2 = BTreeNode bTreeFunctionC2 [] 11
bTreeNodeDecFr4 = BTreeNode (decoratorCreator (xISyCreator Failure Running)) [bTreeNodeC2_2] 10
bTreeNodePOne0 = BTreeNode (parallelCreator successOnOneFailureOne) [bTreeNodeSeq1, bTreeNodeDecFr4] 0
