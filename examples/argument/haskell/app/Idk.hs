module Idk where
import BehaviorTreeCore
import BTreeCheckEnum
import BTreeCheckInt
import BTreeCheckBoolean
import BTreeCheckAll
bTreeNodeCheckEnum = BTreeNode (bTreeFunctionCreatorCheckEnum ("yes")) [] 1
bTreeNodeCheckEnum_1 = BTreeNode (bTreeFunctionCreatorCheckEnum ("Hello")) [] 2
bTreeNodeCheckInt = BTreeNode (bTreeFunctionCreatorCheckInt (55)) [] 3
bTreeNodeCheckInt_1 = BTreeNode (bTreeFunctionCreatorCheckInt (1)) [] 4
bTreeNodeCheckBoolean = BTreeNode (bTreeFunctionCreatorCheckBoolean (True)) [] 5
bTreeNodeCheckBoolean_1 = BTreeNode (bTreeFunctionCreatorCheckBoolean (False)) [] 6
bTreeNodeCheckAll = BTreeNode (bTreeFunctionCreatorCheckAll ("yes") ("Hello") (55) (1) (True) (False)) [] 7
bTreeNodeRootNode = BTreeNode (parallelCreator successOnAllFailureOne) [bTreeNodeCheckEnum, bTreeNodeCheckEnum_1, bTreeNodeCheckInt, bTreeNodeCheckInt_1, bTreeNodeCheckBoolean, bTreeNodeCheckBoolean_1, bTreeNodeCheckAll] 0
