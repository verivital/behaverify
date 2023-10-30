module Main where
import T745
import BehaviorTreeCore
import BehaviorTreeEnvironment
import BehaviorTreeBlackboard
import System.Environment (getArgs)


executeFromSeeds :: Integer -> Integer -> Integer -> [(BTreeBlackboard, BTreeEnvironment)]
executeFromSeeds seed1 seed2 maxIteration = eachBoardEnv
  where
    initBoard = initialBlackboard seed1
    initEnv = initialEnvironment seed2 initBoard
    treeRoot = bTreeNodeSeq0
    executionChain :: Integer -> TrueMemoryStorage -> PartialMemoryStorage -> BTreeBlackboard -> BTreeEnvironment -> [(BTreeBlackboard, BTreeEnvironment)]
    executionChain count memory partial blackboard environment
      | count >= maxIteration = [(blackboard, environment)]
      | not (checkTickConditionTermination blackboard environment) = [(blackboard, environment)]
      | otherwise = (blackboard, environment) : executionChain (count + 1) nextMemory nextPartial nextBoard nextEnv
      where
        (_, nextMemory, nextPartial, tempBoard, tempEnv, futureChanges) = evaluateTree treeRoot memory partial blackboard environment
        (nextBoard, nextEnv) = betweenTickUpdate (applyFutureChanges futureChanges (tempBoard, tempEnv))
    eachBoardEnv = executionChain 0 (allInvalid treeRoot) (allInvalid treeRoot) initBoard initEnv

boardEnvToString :: (BTreeBlackboard, BTreeEnvironment) -> String
boardEnvToString (blackboard, environment) = "(" ++ fromBTreeBlackboardToString blackboard ++ ", " ++ fromBTreeEnvironmentToString blackboard environment ++ ")"

main :: IO ()
main =
  do {
    args <- getArgs
    ; let (seed1, seed2) = seedFromArgs args in mapM_ putStrLn (map boardEnvToString (executeFromSeeds seed1 seed2 11))
  }
  where
    seedFromArgs :: [String] -> (Integer, Integer)
    seedFromArgs [] = (0, 0)
    seedFromArgs curArgs
      | null (tail curArgs) = (read (head curArgs), 0)
      | otherwise = (read (head curArgs), read (head (tail curArgs)))
