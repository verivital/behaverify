module Can_move_forward_file where
import Behavior_tree_core
import Behavior_tree_blackboard
import Behavior_tree_environment
import SereneRandomizer



can_move_forward :: [BTreeNode] -> TreeLocation -> BTreeNodeStatus -> [BTreeStatusTree] -> BTreeNodeStatus -> [BTreeStatusTree] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
can_move_forward nodeChildren nodeLocation memoryStatus memoryStorage partialStatus partialMemoryStorage blackboard environment futureChanges
  | ((((boardForward blackboard) + (envX environment)) >= 0) && (((boardForward blackboard) + (envX environment)) <= 18) && (|| ((envActive_hole blackboard environment) == -1) ((envActive_hole blackboard environment) == (envY environment)))) = (Success, [], [], blackboard, environment, futureChanges)
  | otherwise = (Failure, [], [], blackboard, environment, futureChanges)