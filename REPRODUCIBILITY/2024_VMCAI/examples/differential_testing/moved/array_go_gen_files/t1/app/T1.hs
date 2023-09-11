module T1 where
import BehaviorTreeCore
import BTreeC1
bTreeNodeC1 = BTreeNode bTreeFunctionC1 [] 1
bTreeNodeDecSf0 = BTreeNode (decoratorCreator (xISyCreator Success Failure)) [bTreeNodeC1] 0
