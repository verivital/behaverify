module BTreeTargetReached where
import BehaviorTreeCore
import BehaviorTreeBlackboard
import BehaviorTreeEnvironment
import SereneRandomizer



targetReached :: [BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
targetReached _ nodeLocation _ _ _ _ blackboard environment futureChanges
  | (((boardX blackboard) == (boardTargetX blackboard)) && ((boardY blackboard) == (boardTargetY blackboard))) = (Success, [], [], blackboard, environment, futureChanges)
  | otherwise = (Failure, [], [], blackboard, environment, futureChanges)