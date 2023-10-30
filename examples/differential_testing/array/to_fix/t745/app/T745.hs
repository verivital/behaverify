module T745 where
import BehaviorTreeCore
import BTreeA3
import BTreeA4
bTreeNodeA4 = BTreeNode bTreeFunctionA4 [] 1
bTreeNodeA3 = BTreeNode bTreeFunctionA3 [] 2
bTreeNodeA3_1 = BTreeNode bTreeFunctionA3 [] 3
bTreeNodeSeq0 = BTreeNode sequencePartialMemoryFunc [bTreeNodeA4, bTreeNodeA3, bTreeNodeA3_1] 0
