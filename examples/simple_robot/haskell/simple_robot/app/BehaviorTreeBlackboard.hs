module BehaviorTreeBlackboard where
import SereneRandomizer
import System.Random

data BTreeBlackboard = BTreeBlackboard {
  sereneBoardGenerator :: StdGen
  , boardX :: Int
  , boardY :: Int
  , boardTargetX :: Int
  , boardTargetY :: Int
  , boardMission :: Bool
  }

instance Show BTreeBlackboard where
  show (BTreeBlackboard _ boardX boardY boardTargetX boardTargetY boardMission ) = "Board = {" ++ "boardX: " ++ show boardX ++ ", boardY: " ++ show boardY ++ ", boardTargetX: " ++ show boardTargetX ++ ", boardTargetY: " ++ show boardTargetY ++ ", boardMission: " ++ show boardMission ++ "}"






updateBoardGenerator :: BTreeBlackboard -> StdGen -> BTreeBlackboard
updateBoardGenerator blackboard newGen = blackboard { sereneBoardGenerator = newGen }
updateBoardX :: BTreeBlackboard -> Int -> BTreeBlackboard
updateBoardX blackboard value
  | 0 > value || value > 9 = error "x illegal value"
  | otherwise = blackboard { boardX = value }

updateBoardY :: BTreeBlackboard -> Int -> BTreeBlackboard
updateBoardY blackboard value
  | 0 > value || value > 9 = error "y illegal value"
  | otherwise = blackboard { boardY = value }

updateBoardTargetX :: BTreeBlackboard -> Int -> BTreeBlackboard
updateBoardTargetX blackboard value
  | 0 > value || value > 9 = error "target_x illegal value"
  | otherwise = blackboard { boardTargetX = value }

updateBoardTargetY :: BTreeBlackboard -> Int -> BTreeBlackboard
updateBoardTargetY blackboard value
  | 0 > value || value > 9 = error "target_y illegal value"
  | otherwise = blackboard { boardTargetY = value }

updateBoardMission :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateBoardMission blackboard value = blackboard { boardMission = value }



initialBlackboard :: Int -> BTreeBlackboard
initialBlackboard seed = BTreeBlackboard newSereneGenerator newValX newValY newValTargetX newValTargetY newValMission 
  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen5
    initValX :: StdGen -> (Int, StdGen)
    initValX curGen = (0, curGen)

    (newValX, tempGen1) = initValX tempGen0

    initValY :: StdGen -> (Int, StdGen)
    initValY curGen = (0, curGen)

    (newValY, tempGen2) = initValY tempGen1

    initValTargetX :: StdGen -> (Int, StdGen)
    initValTargetX curGen = (0, curGen)

    (newValTargetX, tempGen3) = initValTargetX tempGen2

    initValTargetY :: StdGen -> (Int, StdGen)
    initValTargetY curGen = (0, curGen)

    (newValTargetY, tempGen4) = initValTargetY tempGen3

    initValMission :: StdGen -> (Bool, StdGen)
    initValMission curGen = (False, curGen)

    (newValMission, tempGen5) = initValMission tempGen4


