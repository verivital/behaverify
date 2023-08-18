module BTreeFellInHole where
import BehaviorTreeCore
import BehaviorTreeBlackboard
import BehaviorTreeEnvironment
import SereneRandomizer
import SereneOperations



fellInHole :: [BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
fellInHole _ nodeLocation _ _ _ _ blackboard environment futureChanges
  | ((boardTiles (envLoc environment) blackboard) == "hole") = (Success, [], [], blackboard, environment, futureChanges)
  | otherwise = (Failure, [], [], blackboard, environment, futureChanges)