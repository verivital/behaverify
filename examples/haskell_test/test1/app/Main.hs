module Main where
import Test1
import Behavior_tree_core
import Behavior_tree_environment
import Behavior_tree_blackboard
import X_less_than_5_file
import Action1_file
import Action2_file


main :: IO ()
main =
  do {
    print eachBoardEnv
  }
  where
    maxIteration = 100
    initBoard = initialBlackboard 0
    initEnv = initialEnvironment 0 initBoard
    treeRoot = root_sel__node
    executionChain :: Int -> MemoryStorage -> PartialMemoryStorage -> BTreeBlackboard -> BTreeEnvironment -> [(BTreeBlackboard, BTreeEnvironment)]
    executionChain count memory partial blackboard environment
      | count >= maxIteration = [(blackboard, environment)]
      | not (checkTickConditionTermination blackboard environment) = [(blackboard, environment)]
      | otherwise = (blackboard, environment) : (executionChain (count + 1) nextMemory nextPartial nextBoard nextEnv)
      where
        (_, nextMemory, nextPartial, nextBoard, tempEnv, futureChanges) = evaluateTree treeRoot memory partial blackboard environment
        nextEnv = betweenTickUpdate (applyFutureChanges tempEnv futureChanges)
    eachBoardEnv = executionChain 0 (allInvalid treeRoot) (allInvalid treeRoot) initBoard initEnv