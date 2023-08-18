module BTreeNeedUp where
import BehaviorTreeCore
import BehaviorTreeBlackboard
import BehaviorTreeEnvironment
import SereneRandomizer
import SereneOperations



needUp :: [BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
needUp _ nodeLocation _ _ _ _ blackboard environment futureChanges
  | ((envYLoc blackboard environment) > (boardYSubgoal blackboard)) = (Success, [], [], blackboard, environment, futureChanges)
  | otherwise = (Failure, [], [], blackboard, environment, futureChanges)