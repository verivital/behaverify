module Collatz where
import BehaviorTreeCore
import BTreeIsEven
import BTreeDivideBy2
import BTreeMultiplyAndAdd
bTreeNodeIsEven = BTreeNode bTreeFunctionIsEven [] 2
bTreeNodeDivideBy2 = BTreeNode bTreeFunctionDivideBy2 [] 3
bTreeNodeEvenCase = BTreeNode sequenceFunc [bTreeNodeIsEven, bTreeNodeDivideBy2] 1
bTreeNodeMultiplyAndAdd = BTreeNode bTreeFunctionMultiplyAndAdd [] 4
bTreeNodeCollatz = BTreeNode selectorFunc [bTreeNodeEvenCase, bTreeNodeMultiplyAndAdd] 0
