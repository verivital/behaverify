module BTreeDownUnknown where
import BehaviorTreeCore
import BehaviorTreeBlackboard
import BehaviorTreeEnvironment
import SereneRandomizer
import SereneOperations



downUnknown :: [BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
downUnknown _ nodeLocation _ _ _ _ blackboard environment futureChanges
  | (("unknown" == (boardTiles ((envXLoc blackboard environment) + (4 * (min 3 ((envYLoc blackboard environment) + 1)))) blackboard)) && ((envYLoc blackboard environment) /= 3)) = (Success, [], [], blackboard, environment, futureChanges)
  | otherwise = (Failure, [], [], blackboard, environment, futureChanges)