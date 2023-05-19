module BTreeCanMoveSide where
import BehaviorTreeCore
import BehaviorTreeBlackboard
import BehaviorTreeEnvironment
import SereneRandomizer



canMoveSide :: [BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
canMoveSide _ nodeLocation _ _ _ _ blackboard environment futureChanges
  | ((((boardSide blackboard) + (envY environment)) >= 0) && (((boardSide blackboard) + (envY environment)) <= 2)) = (Success, [], [], blackboard, environment, futureChanges)
  | otherwise = (Failure, [], [], blackboard, environment, futureChanges)