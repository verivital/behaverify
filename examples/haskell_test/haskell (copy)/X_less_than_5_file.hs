module X_less_than_5_file where
import Behavior_tree_core
import Behavior_tree_environment


x_less_than_5 :: [Node] -> NodeStatus -> [MemoryTree] -> NodeStatus -> [MemoryTree] -> Environment -> Codes -> NodeOutput
x_less_than_5 children memoryStatus memoryTree partialStatus partialTree environment codes
  | (x environment < 5) = (Success, codes, environment, [], [])
  | otherwise = (Failure, codes, environment, [], [])