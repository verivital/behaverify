module BTreeYStrategy where
import BehaviorTreeCore
import BehaviorTreeBlackboard
import BehaviorTreeEnvironment
import SereneRandomizer
import SereneOperations



yStrategy :: [BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
yStrategy _ nodeLocation _ _ _ _ blackboard environment futureChanges
  | ((boardStrategy blackboard) == "y_first") = (Success, [], [], blackboard, environment, futureChanges)
  | otherwise = (Failure, [], [], blackboard, environment, futureChanges)