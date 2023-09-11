module T16 where
import BehaviorTreeCore
import BTreeA2
bTreeNodeA2 = BTreeNode bTreeFunctionA2 [] 1
bTreeNodeDecSf0 = BTreeNode (decoratorCreator (xISyCreator Success Failure)) [bTreeNodeA2] 0
