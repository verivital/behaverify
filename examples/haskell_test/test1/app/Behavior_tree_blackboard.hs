module Behavior_tree_blackboard where
import SereneRandomizer
import System.Random

data BTreeBlackboard = BTreeBlackboard {
  sereneBoardGenerator :: StdGen
  , boardX :: Int
  , boardY :: Int
  }

instance Show BTreeBlackboard where
  show (BTreeBlackboard _ boardX boardY) = "Board = {" ++ "boardX: " ++ show boardX ++ ", boardY: " ++ show boardY ++ "}"


updateBoardGenerator :: BTreeBlackboard -> StdGen -> BTreeBlackboard
updateBoardGenerator blackboard newGen = blackboard { sereneBoardGenerator = newGen }
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
    initValX curGen = (localRandom0 (fst (getRandomInt curGen 1)), snd (getRandomInt curGen 1))
      where
        localRandom0 :: Int -> Int
        localRandom0 0 = 0
        localRandom0 _ = 1
    (newValX, tempGen1) = initValX tempGen0
    initValY :: StdGen -> (Int, StdGen)
    initValY curGen
      | (newValX == 1) = (localRandom0 (fst (getRandomInt curGen 1)), snd (getRandomInt curGen 1))
      | otherwise = (localRandom1 (fst (getRandomInt curGen 1)), snd (getRandomInt curGen 1))
      where
        localRandom0 :: Int -> Int
        localRandom0 0 = 4
        localRandom0 _ = 5
        localRandom1 :: Int -> Int
        localRandom1 0 = 10
        localRandom1 _ = 9
    (newValY, tempGen2) = initValY tempGen1

