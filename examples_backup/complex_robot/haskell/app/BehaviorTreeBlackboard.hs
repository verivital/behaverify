module BehaviorTreeBlackboard where
import SereneRandomizer
import System.Random
import SereneOperations

data BTreeBlackboard = BTreeBlackboard {
  sereneBoardGenerator :: StdGen
  , boardZone :: String
  , boardSide :: Integer
  , boardHaveFlag :: Bool
  , boardNeedSideReached :: Bool
  , localBoardTileSearchedLocation47 :: Bool
  }

fromBTreeBlackboardToString :: BTreeBlackboard -> String
fromBTreeBlackboardToString blackboard = "Board = {" ++ "boardZone: " ++ show (boardZone blackboard) ++ ", " ++ "boardSide: " ++ show (boardSide blackboard) ++ ", " ++ "boardHaveFlag: " ++ show (boardHaveFlag blackboard) ++ ", " ++ "boardNeedSideReached: " ++ show (boardNeedSideReached blackboard) ++ ", " ++ "localBoardTileSearchedLocation47: " ++ show (localBoardTileSearched 47blackboard) ++ ", " ++ "boardForward: " ++ show (boardForward blackboard) ++ "}"

-- START OF BLACKBOARD FUNCTIONS

boardForward :: BTreeBlackboard -> Integer
boardForward blackboard
  | (boardHaveFlag blackboard) = (-1)
  | otherwise = 1

-- START OF LOCAL BLACKBOARD FUNCTIONS


-- START OF GET FUNCTIONS FOR LOCAL VARIABLES

localBoardTileSearched :: Integer -> BTreeBlackboard -> Bool
localBoardTileSearched 47 = localBoardTileSearchedLocation47
localBoardTileSearched _ = error "tile_searched illegal local reference"

-- START OF GET FUNCTIONS FOR ARRAYS


-- START OF TYPE CHECKING FUNCTIONS

checkValueBoardZone :: String -> String
checkValueBoardZone "home" = "home"
checkValueBoardZone "maze" = "maze"
checkValueBoardZone "target" = "target"
checkValueBoardZone _ = error "boardZone illegal value"

checkValueBoardSide :: Integer -> Integer
checkValueBoardSide (-1) = (-1)
checkValueBoardSide 1 = 1
checkValueBoardSide _ = error "boardSide illegal value"

checkValueBoardHaveFlag :: Bool -> Bool
checkValueBoardHaveFlag value = value

checkValueBoardNeedSideReached :: Bool -> Bool
checkValueBoardNeedSideReached value = value

checkValueLocalBoardTileSearched :: Bool -> Bool
checkValueLocalBoardTileSearched value = value

checkValueLocalBoardWillCollide :: Bool -> Bool
checkValueLocalBoardWillCollide value = value


-- START OF SET FUNCTIONS

updateBoardGenerator :: BTreeBlackboard -> StdGen -> BTreeBlackboard
updateBoardGenerator blackboard newGen = blackboard { sereneBoardGenerator = newGen }
updateLocalBoardTileSearched :: Integer -> BTreeBlackboard -> Bool -> BTreeBlackboard
updateLocalBoardTileSearched 47 = updateLocalBoardTileSearchedLocation47
updateLocalBoardTileSearched _ = error "localBoardTileSearched illegal local reference"
updateBoardZone :: BTreeBlackboard -> String -> BTreeBlackboard
updateBoardZone blackboard value = blackboard { boardZone = (checkValueBoardZone value)}
updateBoardSide :: BTreeBlackboard -> Integer -> BTreeBlackboard
updateBoardSide blackboard value = blackboard { boardSide = (checkValueBoardSide value)}
updateBoardHaveFlag :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateBoardHaveFlag blackboard value = blackboard { boardHaveFlag = (checkValueBoardHaveFlag value)}
updateBoardNeedSideReached :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateBoardNeedSideReached blackboard value = blackboard { boardNeedSideReached = (checkValueBoardNeedSideReached value)}
updateLocalBoardTileSearchedLocation47 :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateLocalBoardTileSearchedLocation47 blackboard value = blackboard { localBoardTileSearchedLocation47 = (checkValueLocalBoardTileSearched value)}

-- START OF SET FUNCTIONS FOR ARRAYS


-- START OF INITIAL BLACKBOARD VALUE

initialBlackboard :: Integer -> BTreeBlackboard
initialBlackboard seed = BTreeBlackboard newSereneGenerator newValZone newValSide newValHaveFlag newValNeedSideReached localNewValTileSearchedLocation47  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen5
    partialBlackboardZone = BTreeBlackboard newSereneGenerator " " 0 True True True
    initValZone :: StdGen -> (String, StdGen)
    initValZone curGen = ("home", curGen)
      where
        blackboard = partialBlackboardZone

    (newValZone, tempGen1) = initValZone tempGen0

    partialBlackboardSide = BTreeBlackboard newSereneGenerator newValZone 0 True True True
    initValSide :: StdGen -> (Integer, StdGen)
    initValSide curGen = (1, curGen)
      where
        blackboard = partialBlackboardSide

    (newValSide, tempGen2) = initValSide tempGen1

    partialBlackboardHaveFlag = BTreeBlackboard newSereneGenerator newValZone newValSide True True True
    initValHaveFlag :: StdGen -> (Bool, StdGen)
    initValHaveFlag curGen = (False, curGen)
      where
        blackboard = partialBlackboardHaveFlag

    (newValHaveFlag, tempGen3) = initValHaveFlag tempGen2

    partialBlackboardNeedSideReached = BTreeBlackboard newSereneGenerator newValZone newValSide newValHaveFlag True True
    initValNeedSideReached :: StdGen -> (Bool, StdGen)
    initValNeedSideReached curGen = (True, curGen)
      where
        blackboard = partialBlackboardNeedSideReached

    (newValNeedSideReached, tempGen4) = initValNeedSideReached tempGen3

    partialBlackboardTileSearchedLocation47 = BTreeBlackboard newSereneGenerator newValZone newValSide newValHaveFlag newValNeedSideReached True
    localInitValTileSearchedLocation47 :: StdGen -> (Bool, StdGen)
    localInitValTileSearchedLocation47 curGen = (False, curGen)
      where
        blackboard = partialBlackboardTileSearchedLocation47
        nodeLocation = 47

    (localNewValTileSearchedLocation47, tempGen5) = localInitValTileSearchedLocation47 tempGen4


