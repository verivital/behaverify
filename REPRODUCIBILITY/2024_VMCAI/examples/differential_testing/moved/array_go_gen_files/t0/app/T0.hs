module T0 where
import BehaviorTreeCore
import BTreeA1
bTreeNodeA1 = BTreeNode bTreeFunctionA1 [] 1
bTreeNodeDecFs0 = BTreeNode (decoratorCreator (xISyCreator Failure Success)) [bTreeNodeA1] 0
