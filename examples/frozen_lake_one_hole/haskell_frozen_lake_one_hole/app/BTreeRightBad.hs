module BTreeRightBad where
import BehaviorTreeCore
import BehaviorTreeBlackboard
import BehaviorTreeEnvironment
import SereneRandomizer
import SereneOperations



rightBad :: [BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
rightBad _ nodeLocation _ _ _ _ blackboard environment futureChanges
  | (("hole" == (boardTiles ((min 3 ((envXLoc blackboard environment) + 1)) + (4 * (envYLoc blackboard environment))) blackboard)) || ((envXLoc blackboard environment) == 3)) = (Success, [], [], blackboard, environment, futureChanges)
  | otherwise = (Failure, [], [], blackboard, environment, futureChanges)