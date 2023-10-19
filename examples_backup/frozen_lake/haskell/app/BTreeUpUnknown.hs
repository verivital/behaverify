module BTreeUpUnknown where
import BehaviorTreeCore
import BehaviorTreeBlackboard
import BehaviorTreeEnvironment
import SereneRandomizer
import SereneOperations



bTreeFunctionUpUnknown :: [BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
bTreeFunctionUpUnknown _ nodeLocation _ _ _ _ blackboard environment futureChanges
  | (("unknown" == (boardTiles ((envXLoc blackboard environment) + (4 * (max 0 ((envYLoc blackboard environment) - 1)))) blackboard)) && ((envYLoc blackboard environment) /= 0)) = (Success, [], [], blackboard, environment, futureChanges)
  | otherwise = (Failure, [], [], blackboard, environment, futureChanges)