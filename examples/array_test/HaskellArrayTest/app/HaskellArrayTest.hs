module HaskellArrayTest where
import BehaviorTreeCore
import BTreeAdditionMore
import BTreeMoveIndex
import BTreeActionOne
import BTreeActionTwo
bTreeNodeMoveIndex = BTreeNode moveIndex [] 1
bTreeNodeAdditionMore = BTreeNode additionMore [] 3
bTreeNodeActionOne = BTreeNode actionOne [] 4
bTreeNodeTryOption = BTreeNode sequenceFunc [bTreeNodeAdditionMore, bTreeNodeActionOne] 2
bTreeNodeActionTwo = BTreeNode actionTwo [] 5
bTreeNodeController = BTreeNode selectorFunc [bTreeNodeMoveIndex, bTreeNodeTryOption, bTreeNodeActionTwo] 0
