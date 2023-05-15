module Can_move_side_file where
import Behavior_tree_core
import Behavior_tree_blackboard
import Behavior_tree_environment
import SereneRandomizer



can_move_side :: [BTreeNode] -> TreeLocation -> BTreeNodeStatus -> [BTreeStatusTree] -> BTreeNodeStatus -> [BTreeStatusTree] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
can_move_side nodeChildren nodeLocation memoryStatus memoryStorage partialStatus partialMemoryStorage blackboard environment futureChanges
  | ((((boardSide blackboard) + (envY environment)) >= 0) && (((boardSide blackboard) + (envY environment)) <= 2)) = (Success, [], [], blackboard, environment, futureChanges)
  | otherwise = (Failure, [], [], blackboard, environment, futureChanges)