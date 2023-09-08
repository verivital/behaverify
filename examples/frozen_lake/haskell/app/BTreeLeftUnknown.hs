module BTreeLeftUnknown where
import BehaviorTreeCore
import BehaviorTreeBlackboard
import BehaviorTreeEnvironment
import SereneRandomizer
import SereneOperations



bTreeFunctionLeftUnknown :: [BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
bTreeFunctionLeftUnknown _ nodeLocation _ _ _ _ blackboard environment futureChanges
  | (("unknown" == (boardTiles ((max 0 ((envXLoc blackboard environment) - 1)) + (4 * (envYLoc blackboard environment))) blackboard)) && ((envXLoc blackboard environment) /= 0)) = (Success, [], [], blackboard, environment, futureChanges)
  | otherwise = (Failure, [], [], blackboard, environment, futureChanges)