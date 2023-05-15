module In_maze_file where
import Behavior_tree_core
import Behavior_tree_blackboard
import Behavior_tree_environment
import SereneRandomizer



in_maze :: [BTreeNode] -> TreeLocation -> BTreeNodeStatus -> [BTreeStatusTree] -> BTreeNodeStatus -> [BTreeStatusTree] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
in_maze nodeChildren nodeLocation memoryStatus memoryStorage partialStatus partialMemoryStorage blackboard environment futureChanges
  | ((boardZone blackboard) == "maze") = (Success, [], [], blackboard, environment, futureChanges)
  | otherwise = (Failure, [], [], blackboard, environment, futureChanges)