module BTreeUpBad where
import BehaviorTreeCore
import BehaviorTreeBlackboard
import BehaviorTreeEnvironment
import SereneRandomizer
import SereneOperations



upBad :: [BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
upBad _ nodeLocation _ _ _ _ blackboard environment futureChanges
  | (("hole" == (sereneIndexTiles ((envXLoc blackboard environment) + (4 * (max 0 ((envYLoc blackboard environment) - 1)))) blackboard)) || ((envYLoc blackboard environment) == 0)) = (Success, [], [], blackboard, environment, futureChanges)
  | otherwise = (Failure, [], [], blackboard, environment, futureChanges)