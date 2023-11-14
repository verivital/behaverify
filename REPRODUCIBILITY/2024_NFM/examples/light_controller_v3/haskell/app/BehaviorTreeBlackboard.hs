module BehaviorTreeBlackboard where
import SereneRandomizer
import System.Random
import SereneOperations

data BTreeBlackboard = BTreeBlackboard {
  sereneBoardGenerator :: StdGen
  , boardFairnessCounter :: Integer
  , boardDirection :: String
  , boardSignal :: Bool
  }

fromBTreeBlackboardToString :: BTreeBlackboard -> String
fromBTreeBlackboardToString blackboard = "Board = {" ++ "boardFairnessCounter: " ++ show (boardFairnessCounter blackboard) ++ ", " ++ "boardDirection: " ++ show (boardDirection blackboard) ++ ", " ++ "boardSignal: " ++ show (boardSignal blackboard) ++ "}"

-- START OF BLACKBOARD FUNCTIONS


-- START OF LOCAL BLACKBOARD FUNCTIONS


-- START OF GET FUNCTIONS FOR LOCAL VARIABLES


-- START OF GET FUNCTIONS FOR ARRAYS


-- START OF TYPE CHECKING FUNCTIONS

checkValueBoardFairnessCounter :: Integer -> Integer
checkValueBoardFairnessCounter value
  | 0 > value || value > 4 = error "boardFairnessCounter illegal value"
  | otherwise = value

checkValueBoardDirection :: String -> String
checkValueBoardDirection "east_to_west" = "east_to_west"
checkValueBoardDirection "west_to_east" = "west_to_east"
checkValueBoardDirection _ = error "boardDirection illegal value"

checkValueBoardSignal :: Bool -> Bool
checkValueBoardSignal value = value


-- START OF SET FUNCTIONS

updateBoardGenerator :: BTreeBlackboard -> StdGen -> BTreeBlackboard
updateBoardGenerator blackboard newGen = blackboard { sereneBoardGenerator = newGen }
updateBoardFairnessCounter :: BTreeBlackboard -> Integer -> BTreeBlackboard
updateBoardFairnessCounter blackboard value = blackboard { boardFairnessCounter = (checkValueBoardFairnessCounter value)}
updateBoardDirection :: BTreeBlackboard -> String -> BTreeBlackboard
updateBoardDirection blackboard value = blackboard { boardDirection = (checkValueBoardDirection value)}
updateBoardSignal :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateBoardSignal blackboard value = blackboard { boardSignal = (checkValueBoardSignal value)}

-- START OF SET FUNCTIONS FOR ARRAYS


-- START OF INITIAL BLACKBOARD VALUE

initialBlackboard :: Integer -> BTreeBlackboard
initialBlackboard seed = BTreeBlackboard newSereneGenerator newValFairnessCounter newValDirection newValSignal  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen3
    partialBlackboardFairnessCounter = BTreeBlackboard newSereneGenerator 0 " " True
    initValFairnessCounter :: StdGen -> (Integer, StdGen)
    initValFairnessCounter curGen = (0, curGen)
      where
        blackboard = partialBlackboardFairnessCounter

    (newValFairnessCounter, tempGen1) = initValFairnessCounter tempGen0

    partialBlackboardDirection = BTreeBlackboard newSereneGenerator newValFairnessCounter " " True
    initValDirection :: StdGen -> (String, StdGen)
    initValDirection curGen = ("west_to_east", curGen)
      where
        blackboard = partialBlackboardDirection

    (newValDirection, tempGen2) = initValDirection tempGen1

    partialBlackboardSignal = BTreeBlackboard newSereneGenerator newValFairnessCounter newValDirection True
    initValSignal :: StdGen -> (Bool, StdGen)
    initValSignal curGen = (False, curGen)
      where
        blackboard = partialBlackboardSignal

    (newValSignal, tempGen3) = initValSignal tempGen2


