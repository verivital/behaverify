module Main where
import Haskellfrozenlake
import BehaviorTreeCore
import BehaviorTreeEnvironment
import BehaviorTreeBlackboard
import System.Environment (getArgs)
import BTreeXStrategy
import BTreeYStrategy
import BTreeGetInfo
import BTreeRequestHold
import BTreeRequestReset
import BTreeRequestUp
import BTreeRequestDown
import BTreeRequestLeft
import BTreeRequestRight
import BTreeSetNewSubgoal
import BTreeChangeStrategy
import BTreeSometimesChangeStrategy
import BTreeFellInHole
import BTreeUpBad
import BTreeDownBad
import BTreeLeftBad
import BTreeRightBad
import BTreeUpUnknown
import BTreeDownUnknown
import BTreeLeftUnknown
import BTreeRightUnknown
import BTreeNeedNewSubgoal
import BTreeNeedUp
import BTreeNeedDown
import BTreeNeedLeft
import BTreeNeedRight
import BTreeReachedGoal
import BTreeSubgoalUnreachable


executeFromSeeds :: Int -> Int -> Int -> [(BTreeBlackboard, BTreeEnvironment)]
executeFromSeeds seed1 seed2 maxIteration = eachBoardEnv
  where
    initBoard = initialBlackboard seed1
    initEnv = initialEnvironment seed2 initBoard
    treeRoot = bTreeNodeExecutionSequence
    executionChain :: Int -> TrueMemoryStorage -> PartialMemoryStorage -> BTreeBlackboard -> BTreeEnvironment -> [(BTreeBlackboard, BTreeEnvironment)]
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
    ; let (seed1, seed2) = seedFromArgs args in mapM_ print (executeFromSeeds seed1 seed2 11)
  }
  where
    seedFromArgs :: [String] -> (Int, Int)
    seedFromArgs [] = (0, 0)
    seedFromArgs curArgs
      | null (tail curArgs) = (read (head curArgs), 0)
      | otherwise = (read (head curArgs), read (head (tail curArgs)))
