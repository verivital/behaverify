module BTreeCanMoveForward where
import BehaviorTreeCore
import BehaviorTreeBlackboard
import BehaviorTreeEnvironment
import SereneRandomizer
import SereneOperations



bTreeFunctionCanMoveForward :: [BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
bTreeFunctionCanMoveForward _ nodeLocation _ _ _ _ blackboard environment futureChanges
  | ((((boardForward blackboard) + (envX environment)) >= 0) && ((((boardForward blackboard) + (envX environment)) <= 18) && (((envActiveHole blackboard environment) == (-1)) || ((envActiveHole blackboard environment) == (envY environment))))) = (Success, [], [], blackboard, environment, futureChanges)
  | otherwise = (Failure, [], [], blackboard, environment, futureChanges)