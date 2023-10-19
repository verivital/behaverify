module BehaviorTreeBlackboard where
import SereneRandomizer
import System.Random
import SereneOperations

data BTreeBlackboard = BTreeBlackboard {
  sereneBoardGenerator :: StdGen
  , boardX :: Integer
  , boardY :: Integer
  , boardTargetX :: Integer
  , boardTargetY :: Integer
  , boardMission :: Bool
  }

fromBTreeBlackboardToString :: BTreeBlackboard -> String
fromBTreeBlackboardToString blackboard = "Board = {" ++ "boardX: " ++ show (boardX blackboard) ++ ", " ++ "boardY: " ++ show (boardY blackboard) ++ ", " ++ "boardTargetX: " ++ show (boardTargetX blackboard) ++ ", " ++ "boardTargetY: " ++ show (boardTargetY blackboard) ++ ", " ++ "boardMission: " ++ show (boardMission blackboard) ++ "}"

-- START OF BLACKBOARD FUNCTIONS


-- START OF LOCAL BLACKBOARD FUNCTIONS


-- START OF GET FUNCTIONS FOR LOCAL VARIABLES


-- START OF GET FUNCTIONS FOR ARRAYS


-- START OF TYPE CHECKING FUNCTIONS

checkValueBoardX :: Integer -> Integer
checkValueBoardX value
  | 0 > value || value > 7 = error "boardX illegal value"
  | otherwise = value

checkValueBoardY :: Integer -> Integer
checkValueBoardY value
  | 0 > value || value > 7 = error "boardY illegal value"
  | otherwise = value

checkValueBoardTargetX :: Integer -> Integer
checkValueBoardTargetX value
  | 0 > value || value > 7 = error "boardTargetX illegal value"
  | otherwise = value

checkValueBoardTargetY :: Integer -> Integer
checkValueBoardTargetY value
  | 0 > value || value > 7 = error "boardTargetY illegal value"
  | otherwise = value

checkValueBoardMission :: Bool -> Bool
checkValueBoardMission value = value

checkValueLocalBoardSawTarget :: Bool -> Bool
checkValueLocalBoardSawTarget value = value


-- START OF SET FUNCTIONS

updateBoardGenerator :: BTreeBlackboard -> StdGen -> BTreeBlackboard
updateBoardGenerator blackboard newGen = blackboard { sereneBoardGenerator = newGen }
updateBoardX :: BTreeBlackboard -> Integer -> BTreeBlackboard
updateBoardX blackboard value = blackboard { boardX = (checkValueBoardX value)}
updateBoardY :: BTreeBlackboard -> Integer -> BTreeBlackboard
updateBoardY blackboard value = blackboard { boardY = (checkValueBoardY value)}
updateBoardTargetX :: BTreeBlackboard -> Integer -> BTreeBlackboard
updateBoardTargetX blackboard value = blackboard { boardTargetX = (checkValueBoardTargetX value)}
updateBoardTargetY :: BTreeBlackboard -> Integer -> BTreeBlackboard
updateBoardTargetY blackboard value = blackboard { boardTargetY = (checkValueBoardTargetY value)}
updateBoardMission :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateBoardMission blackboard value = blackboard { boardMission = (checkValueBoardMission value)}

-- START OF SET FUNCTIONS FOR ARRAYS


-- START OF INITIAL BLACKBOARD VALUE

initialBlackboard :: Integer -> BTreeBlackboard
initialBlackboard seed = BTreeBlackboard newSereneGenerator newValX newValY newValTargetX newValTargetY newValMission  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen5
    partialBlackboardX = BTreeBlackboard newSereneGenerator 0 0 0 0 True
    initValX :: StdGen -> (Integer, StdGen)
    initValX curGen = (0, curGen)
      where
        blackboard = partialBlackboardX

    (newValX, tempGen1) = initValX tempGen0

    partialBlackboardY = BTreeBlackboard newSereneGenerator newValX 0 0 0 True
    initValY :: StdGen -> (Integer, StdGen)
    initValY curGen = (0, curGen)
      where
        blackboard = partialBlackboardY

    (newValY, tempGen2) = initValY tempGen1

    partialBlackboardTargetX = BTreeBlackboard newSereneGenerator newValX newValY 0 0 True
    initValTargetX :: StdGen -> (Integer, StdGen)
    initValTargetX curGen = (0, curGen)
      where
        blackboard = partialBlackboardTargetX

    (newValTargetX, tempGen3) = initValTargetX tempGen2

    partialBlackboardTargetY = BTreeBlackboard newSereneGenerator newValX newValY newValTargetX 0 True
    initValTargetY :: StdGen -> (Integer, StdGen)
    initValTargetY curGen = (0, curGen)
      where
        blackboard = partialBlackboardTargetY

    (newValTargetY, tempGen4) = initValTargetY tempGen3

    partialBlackboardMission = BTreeBlackboard newSereneGenerator newValX newValY newValTargetX newValTargetY True
    initValMission :: StdGen -> (Bool, StdGen)
    initValMission curGen = (False, curGen)
      where
        blackboard = partialBlackboardMission

    (newValMission, tempGen5) = initValMission tempGen4


