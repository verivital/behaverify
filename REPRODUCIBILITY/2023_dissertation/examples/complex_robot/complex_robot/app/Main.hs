module Main where
import Complex_robot
import Behavior_tree_core
import Behavior_tree_environment
import Behavior_tree_blackboard
import System.Environment (getArgs)
import In_maze_file
import In_target_file
import Flag_found_file
import Change_side_file
import Go_forward_file
import Go_side_file
import Search_tile_file
import Set_zone_file
import Flag_not_returned_file
import Can_move_forward_file
import Can_move_side_file


executeFromSeeds :: Int -> Int -> Int -> [(BTreeBlackboard, BTreeEnvironment)]
executeFromSeeds seed1 seed2 maxIteration = eachBoardEnv
  where
    initBoard = initialBlackboard seed1
    initEnv = initialEnvironment seed2 initBoard
    treeRoot = control__node
    executionChain :: Int -> MemoryStorage -> PartialMemoryStorage -> BTreeBlackboard -> BTreeEnvironment -> [(BTreeBlackboard, BTreeEnvironment)]
    executionChain count memory partial blackboard environment
      | count >= maxIteration = [(blackboard, environment)]
      | not (checkTickConditionTermination blackboard environment) = [(blackboard, environment)]
      | otherwise = (blackboard, environment) : executionChain (count + 1) nextMemory nextPartial nextBoard nextEnv
      where
        (_, nextMemory, nextPartial, nextBoard, tempEnv, futureChanges) = evaluateTree treeRoot memory partial blackboard environment
        nextEnv = betweenTickUpdate (applyFutureChanges tempEnv futureChanges)
    eachBoardEnv = executionChain 0 (allInvalid treeRoot) (allInvalid treeRoot) initBoard initEnv

main :: IO ()
main =
  do {
    args <- getArgs
    ; let (seed1, seed2) = seedFromArgs args in mapM_ print (executeFromSeeds seed1 seed2 10)
  }
  where
    seedFromArgs :: [String] -> (Int, Int)
    seedFromArgs [] = (0, 0)
    seedFromArgs curArgs
      | null (tail curArgs) = (read (head curArgs), 0)
      | otherwise = (read (head curArgs), read (head (tail curArgs)))
