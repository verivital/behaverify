module BTreeLeftBad where
import BehaviorTreeCore
import BehaviorTreeBlackboard
import BehaviorTreeEnvironment
import SereneRandomizer
import SereneOperations



leftBad :: [BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
leftBad _ nodeLocation _ _ _ _ blackboard environment futureChanges
  | (("hole" == (sereneIndexTiles ((max 0 ((envXLoc blackboard environment) - 1)) + (4 * (envYLoc blackboard environment))) blackboard)) || ((envXLoc blackboard environment) == 0)) = (Success, [], [], blackboard, environment, futureChanges)
  | otherwise = (Failure, [], [], blackboard, environment, futureChanges)