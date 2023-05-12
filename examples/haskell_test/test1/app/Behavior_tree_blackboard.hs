module Behavior_tree_blackboard where
import SereneRandomizer
import System.Random

data BTreeBlackboard = BTreeBlackboard {
  sereneGenerator :: StdGen
  , boardX :: Int
  , boardY :: Int
  } deriving (Show)

updateBoardX :: BTreeBlackboard -> Int -> BTreeBlackboard
updateBoardX blackboard value
  | 0 > value || value > 10 = error "x illegal value"
  | otherwise = blackboard { boardX = value }

updateBoardY :: BTreeBlackboard -> Int -> BTreeBlackboard
updateBoardY blackboard value
  | 0 > value || value > 10 = error "y illegal value"
  | otherwise = blackboard { boardY = value }



initialBlackboard :: Int -> BTreeBlackboard
initialBlackboard seed = BTreeBlackboard newSereneGenerator newValX newValY
  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen2
    initValX :: StdGen -> (Int, StdGen)
    initValX curGen = (0, curGen)
    (newValX, tempGen1) = initValX tempGen0
    initValY :: StdGen -> (Int, StdGen)
    initValY curGen = (10, curGen)
    (newValY, tempGen2) = initValY tempGen1

