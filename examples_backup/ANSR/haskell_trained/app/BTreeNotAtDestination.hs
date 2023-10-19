module BTreeNotAtDestination where
import BehaviorTreeCore
import BehaviorTreeBlackboard
import BehaviorTreeEnvironment
import SereneRandomizer
import SereneOperations



bTreeFunctionNotAtDestination :: [BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
bTreeFunctionNotAtDestination _ nodeLocation _ _ _ _ blackboard environment futureChanges
  | (not (((boardCurX blackboard) == (boardDestX blackboard)) && ((boardCurY blackboard) == (boardDestY blackboard)))) = (Success, [], [], blackboard, environment, futureChanges)
  | otherwise = (Failure, [], [], blackboard, environment, futureChanges)