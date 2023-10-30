module T700 where
import BehaviorTreeCore
import BTreeC2
import BTreeA2
import BTreeA3
bTreeNodeC2 = BTreeNode bTreeFunctionC2 [] 2
bTreeNodeA3 = BTreeNode bTreeFunctionA3 [] 3
bTreeNodeA2 = BTreeNode bTreeFunctionA2 [] 4
bTreeNodePOne1 = BTreeNode (parallelCreator successOnOneFailureOne) [bTreeNodeC2, bTreeNodeA3, bTreeNodeA2] 1
bTreeNodeDecInv0 = BTreeNode (decoratorCreator inverterCreator) [bTreeNodePOne1] 0
