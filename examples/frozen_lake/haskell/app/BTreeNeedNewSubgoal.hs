module BTreeNeedNewSubgoal where
import BehaviorTreeCore
import BehaviorTreeBlackboard
import BehaviorTreeEnvironment
import SereneRandomizer
import SereneOperations



bTreeFunctionNeedNewSubgoal :: [BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
bTreeFunctionNeedNewSubgoal _ nodeLocation _ _ _ _ blackboard environment futureChanges
  | (("hole" == (boardTiles ((boardXSubgoal blackboard) + (4 * (boardYSubgoal blackboard))) blackboard)) || ((envLoc environment) == (boardSubgoal blackboard))) = (Success, [], [], blackboard, environment, futureChanges)
  | otherwise = (Failure, [], [], blackboard, environment, futureChanges)