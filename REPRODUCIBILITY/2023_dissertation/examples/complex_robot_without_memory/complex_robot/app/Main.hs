module Main where
import Complex_robot
import Behavior_tree_core
import Behavior_tree_environment
import Behavior_tree_blackboard
import System.Environment (getArgs)
import In_home_file
import In_maze_file
import In_target_file
import Flag_found_file
import Need_side_file
import Success_node_file
import Change_side_file
import Go_forward_file
import Go_side_file
import Never_need_side_file
import Search_tile_file
import Set_zone_file
import Flag_not_returned_file
import Can_move_forward_file
import Can_move_side_file


formatPrint :: [(BTreeBlackboard, BTreeEnvironment)] -> String
formatPrint [] = []
formatPrint boardEnvs = curString ++ formatPrint (tail boardEnvs)
  where
    (board, env) = head boardEnvs
    curString = "_______________________________\n" ++ coreString ++ "_______________________________\n"
    charsAt :: Int -> Int -> String
    charsAt x y = char1 ++ char2 ++ char3
      where
        char1
          | x == envX env && y == envY env = "R"
          | x == envFlag_x env && y == envFlag_y env && boardHave_flag board = "f"
          | x == envFlag_x env && y == envFlag_y env = "F"
          | x < 4 || x > 12 = "-"
          | otherwise = ""
        char2
          | x < 4 || x > 12 = ""
          | x == envX env && y == envY env = ""
          | otherwise = " "
        char3
          | x < 4 || x > 12 = ""
          | x == 4 && y == envHole_1 env = " "
          | x == 5 && y == envHole_2 env = " "
          | x == 6 && y == envHole_3 env = " "
          | x == 7 && y == envHole_4 env = " "
          | x == 8 && y == envHole_5 env = " "
          | x == 9 && y == envHole_6 env = " "
          | x == 10 && y == envHole_7 env = " "
          | x == 11 && y == envHole_8 env = " "
          | x == 12 && y == envHole_9 env = " "
          | otherwise = "|"
    buildRow :: Int -> Int -> String
    buildRow 18 y = charsAt 18 y
    buildRow x y = charsAt x y ++ (buildRow (x + 1) y)
    buildBoard :: Int -> String
    buildBoard 2 = buildRow 0 2 ++ "\n"
    buildBoard y = buildRow 0 y ++ "\n" ++ (buildBoard (y + 1))
    coreString = buildBoard 0


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
        (_, nextMemory, nextPartial, tempBoard, tempEnv, futureChanges) = evaluateTree treeRoot memory partial blackboard environment
        (nextBoard, nextEnv) = betweenTickUpdate (applyFutureChanges futureChanges (tempBoard, tempEnv))
    eachBoardEnv = executionChain 0 (allInvalid treeRoot) (allInvalid treeRoot) initBoard initEnv

main :: IO ()
main =
  do {
    args <- getArgs
    --; let (seed1, seed2) = seedFromArgs args in mapM_ print (executeFromSeeds seed1 seed2 10)
    ; let (seed1, seed2) = seedFromArgs args in putStr (formatPrint (executeFromSeeds seed1 seed2 100))
  }
  where
    seedFromArgs :: [String] -> (Int, Int)
    seedFromArgs [] = (0, 0)
    seedFromArgs curArgs
      | null (tail curArgs) = (read (head curArgs), 0)
      | otherwise = (read (head curArgs), read (head (tail curArgs)))
