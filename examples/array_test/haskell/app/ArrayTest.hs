module ArrayTest where
import BehaviorTreeCore
import BTreeAdditionMore
import BTreeMoveIndex
import BTreeActionOne
import BTreeActionTwo
bTreeNodeMoveIndex = BTreeNode bTreeFunctionMoveIndex [] 1
bTreeNodeAdditionMore = BTreeNode bTreeFunctionAdditionMore [] 3
bTreeNodeActionOne = BTreeNode bTreeFunctionActionOne [] 4
bTreeNodeTryOption = BTreeNode sequenceFunc [bTreeNodeAdditionMore, bTreeNodeActionOne] 2
bTreeNodeActionTwo = BTreeNode bTreeFunctionActionTwo [] 5
bTreeNodeController = BTreeNode selectorFunc [bTreeNodeMoveIndex, bTreeNodeTryOption, bTreeNodeActionTwo] 0
