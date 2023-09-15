module BehaviorTreeBlackboard where
import SereneRandomizer
import System.Random
import SereneOperations

data BTreeBlackboard = BTreeBlackboard {
  sereneBoardGenerator :: StdGen
  , boardPrevDestX :: Integer
  , boardPrevDestY :: Integer
  , boardCurX :: Integer
  , boardCurY :: Integer
  , boardDestX :: Integer
  , boardDestY :: Integer
  , boardDir :: Integer
  , boardVictory :: Bool
  }

fromBTreeBlackboardToString :: BTreeBlackboard -> String
fromBTreeBlackboardToString blackboard = "Board = {" ++ "boardPrevDestX: " ++ show (boardPrevDestX blackboard) ++ ", " ++ "boardPrevDestY: " ++ show (boardPrevDestY blackboard) ++ ", " ++ "boardCurX: " ++ show (boardCurX blackboard) ++ ", " ++ "boardCurY: " ++ show (boardCurY blackboard) ++ ", " ++ "boardDestX: " ++ show (boardDestX blackboard) ++ ", " ++ "boardDestY: " ++ show (boardDestY blackboard) ++ ", " ++ "boardDir: " ++ show (boardDir blackboard) ++ ", " ++ "boardVictory: " ++ show (boardVictory blackboard) ++ ", " ++ "boardXNet11: " ++ show (boardXNet11 blackboard) ++ ", " ++ "boardXNet12: " ++ show (boardXNet12 blackboard) ++ ", " ++ "boardXNet13: " ++ show (boardXNet13 blackboard) ++ ", " ++ "boardXNet14: " ++ show (boardXNet14 blackboard) ++ ", " ++ "boardXNet15: " ++ show (boardXNet15 blackboard) ++ ", " ++ "boardXNet21: " ++ show (boardXNet21 blackboard) ++ ", " ++ "boardXNet22: " ++ show (boardXNet22 blackboard) ++ ", " ++ "boardXNet23: " ++ show (boardXNet23 blackboard) ++ ", " ++ "boardXNet24: " ++ show (boardXNet24 blackboard) ++ ", " ++ "boardXNet31: " ++ show (boardXNet31 blackboard) ++ ", " ++ "boardXNet32: " ++ show (boardXNet32 blackboard) ++ ", " ++ "boardXNet33: " ++ show (boardXNet33 blackboard) ++ ", " ++ "boardXNet34: " ++ show (boardXNet34 blackboard) ++ ", " ++ "boardXNet41: " ++ show (boardXNet41 blackboard) ++ ", " ++ "boardXNet42: " ++ show (boardXNet42 blackboard) ++ ", " ++ "boardXNet43: " ++ show (boardXNet43 blackboard) ++ ", " ++ "boardXNetOutput1: " ++ show (boardXNetOutput1 blackboard) ++ ", " ++ "boardYNet11: " ++ show (boardYNet11 blackboard) ++ ", " ++ "boardYNet12: " ++ show (boardYNet12 blackboard) ++ ", " ++ "boardYNet13: " ++ show (boardYNet13 blackboard) ++ ", " ++ "boardYNet14: " ++ show (boardYNet14 blackboard) ++ ", " ++ "boardYNet15: " ++ show (boardYNet15 blackboard) ++ ", " ++ "boardYNet21: " ++ show (boardYNet21 blackboard) ++ ", " ++ "boardYNet22: " ++ show (boardYNet22 blackboard) ++ ", " ++ "boardYNet23: " ++ show (boardYNet23 blackboard) ++ ", " ++ "boardYNet24: " ++ show (boardYNet24 blackboard) ++ ", " ++ "boardYNet31: " ++ show (boardYNet31 blackboard) ++ ", " ++ "boardYNet32: " ++ show (boardYNet32 blackboard) ++ ", " ++ "boardYNet33: " ++ show (boardYNet33 blackboard) ++ ", " ++ "boardYNetOutput1: " ++ show (boardYNetOutput1 blackboard) ++ "}"

-- START OF BLACKBOARD FUNCTIONS

boardXNet11 :: BTreeBlackboard -> Integer
boardXNet11 blackboard = (max (boardDestX blackboard) 0)
boardXNet12 :: BTreeBlackboard -> Integer
boardXNet12 blackboard = (max ((boardDestX blackboard) - (boardPrevDestX blackboard)) 0)
boardXNet13 :: BTreeBlackboard -> Integer
boardXNet13 blackboard = (max ((boardPrevDestX blackboard) - (boardDestX blackboard)) 0)
boardXNet14 :: BTreeBlackboard -> Integer
boardXNet14 blackboard = (max ((boardDestX blackboard) - (quot (0 + 6) 2)) 0)
boardXNet15 :: BTreeBlackboard -> Integer
boardXNet15 blackboard = (max ((quot (0 + 6) 2) - (boardDestX blackboard)) 0)
boardXNet21 :: BTreeBlackboard -> Integer
boardXNet21 blackboard = (max (boardXNet11 blackboard) 0)
boardXNet22 :: BTreeBlackboard -> Integer
boardXNet22 blackboard = (max ((- (boardXNet12 blackboard)) + ((- (boardXNet13 blackboard)) + 1)) 0)
boardXNet23 :: BTreeBlackboard -> Integer
boardXNet23 blackboard = (max (1 - (boardXNet14 blackboard)) 0)
boardXNet24 :: BTreeBlackboard -> Integer
boardXNet24 blackboard = (max (1 - (boardXNet15 blackboard)) 0)
boardXNet31 :: BTreeBlackboard -> Integer
boardXNet31 blackboard = (max ((boardXNet21 blackboard) - ((boardXNet22 blackboard) * 6)) 0)
boardXNet32 :: BTreeBlackboard -> Integer
boardXNet32 blackboard = (max (1 - (boardXNet22 blackboard)) 0)
boardXNet33 :: BTreeBlackboard -> Integer
boardXNet33 blackboard = (max (boardXNet23 blackboard) 0)
boardXNet34 :: BTreeBlackboard -> Integer
boardXNet34 blackboard = (max (boardXNet24 blackboard) 0)
boardXNet41 :: BTreeBlackboard -> Integer
boardXNet41 blackboard = (max (boardXNet31 blackboard) 0)
boardXNet42 :: BTreeBlackboard -> Integer
boardXNet42 blackboard = (max ((6 * (boardXNet33 blackboard)) - (6 * (boardXNet32 blackboard))) 0)
boardXNet43 :: BTreeBlackboard -> Integer
boardXNet43 blackboard = (max ((0 * (boardXNet34 blackboard)) - (6 * (boardXNet32 blackboard))) 0)
boardXNetOutput1 :: BTreeBlackboard -> Integer
boardXNetOutput1 blackboard = (max ((boardXNet41 blackboard) + ((boardXNet42 blackboard) + (boardXNet43 blackboard))) 0)
boardYNet11 :: BTreeBlackboard -> Integer
boardYNet11 blackboard = (max (boardDestY blackboard) 0)
boardYNet12 :: BTreeBlackboard -> Integer
boardYNet12 blackboard = (max ((boardDestY blackboard) - (boardPrevDestY blackboard)) 0)
boardYNet13 :: BTreeBlackboard -> Integer
boardYNet13 blackboard = (max ((boardPrevDestY blackboard) - (boardDestY blackboard)) 0)
boardYNet14 :: BTreeBlackboard -> Integer
boardYNet14 blackboard = (max (boardDir blackboard) 0)
boardYNet15 :: BTreeBlackboard -> Integer
boardYNet15 blackboard = (max (- (boardDir blackboard)) 0)
boardYNet21 :: BTreeBlackboard -> Integer
boardYNet21 blackboard = (max (boardYNet11 blackboard) 0)
boardYNet22 :: BTreeBlackboard -> Integer
boardYNet22 blackboard = (max ((- (boardYNet12 blackboard)) + ((- (boardYNet13 blackboard)) + 1)) 0)
boardYNet23 :: BTreeBlackboard -> Integer
boardYNet23 blackboard = (max (boardYNet14 blackboard) 0)
boardYNet24 :: BTreeBlackboard -> Integer
boardYNet24 blackboard = (max (boardYNet15 blackboard) 0)
boardYNet31 :: BTreeBlackboard -> Integer
boardYNet31 blackboard = (max (boardYNet21 blackboard) 0)
boardYNet32 :: BTreeBlackboard -> Integer
boardYNet32 blackboard = (max ((boardYNet22 blackboard) + ((boardYNet23 blackboard) + (-1))) 0)
boardYNet33 :: BTreeBlackboard -> Integer
boardYNet33 blackboard = (max ((boardYNet22 blackboard) + ((boardYNet24 blackboard) + (-1))) 0)
boardYNetOutput1 :: BTreeBlackboard -> Integer
boardYNetOutput1 blackboard = (max ((boardYNet31 blackboard) + ((2 * (boardYNet32 blackboard)) + ((-1) * (2 * (boardYNet33 blackboard))))) 0)

-- START OF LOCAL BLACKBOARD FUNCTIONS


-- START OF GET FUNCTIONS FOR LOCAL VARIABLES


-- START OF GET FUNCTIONS FOR ARRAYS


-- START OF TYPE CHECKING FUNCTIONS

checkValueBoardPrevDestX :: Integer -> Integer
checkValueBoardPrevDestX value
  | 0 > value || value > 6 = error "boardPrevDestX illegal value"
  | otherwise = value

checkValueBoardPrevDestY :: Integer -> Integer
checkValueBoardPrevDestY value
  | 0 > value || value > 6 = error "boardPrevDestY illegal value"
  | otherwise = value

checkValueBoardCurX :: Integer -> Integer
checkValueBoardCurX value
  | 0 > value || value > 6 = error "boardCurX illegal value"
  | otherwise = value

checkValueBoardCurY :: Integer -> Integer
checkValueBoardCurY value
  | 0 > value || value > 6 = error "boardCurY illegal value"
  | otherwise = value

checkValueBoardDestX :: Integer -> Integer
checkValueBoardDestX value
  | 0 > value || value > 6 = error "boardDestX illegal value"
  | otherwise = value

checkValueBoardDestY :: Integer -> Integer
checkValueBoardDestY value
  | 0 > value || value > 6 = error "boardDestY illegal value"
  | otherwise = value

checkValueBoardDir :: Integer -> Integer
checkValueBoardDir (-1) = (-1)
checkValueBoardDir 1 = 1
checkValueBoardDir _ = error "boardDir illegal value"

checkValueBoardVictory :: Bool -> Bool
checkValueBoardVictory value = value


-- START OF SET FUNCTIONS

updateBoardGenerator :: BTreeBlackboard -> StdGen -> BTreeBlackboard
updateBoardGenerator blackboard newGen = blackboard { sereneBoardGenerator = newGen }
updateBoardPrevDestX :: BTreeBlackboard -> Integer -> BTreeBlackboard
updateBoardPrevDestX blackboard value = blackboard { boardPrevDestX = (checkValueBoardPrevDestX value)}
updateBoardPrevDestY :: BTreeBlackboard -> Integer -> BTreeBlackboard
updateBoardPrevDestY blackboard value = blackboard { boardPrevDestY = (checkValueBoardPrevDestY value)}
updateBoardCurX :: BTreeBlackboard -> Integer -> BTreeBlackboard
updateBoardCurX blackboard value = blackboard { boardCurX = (checkValueBoardCurX value)}
updateBoardCurY :: BTreeBlackboard -> Integer -> BTreeBlackboard
updateBoardCurY blackboard value = blackboard { boardCurY = (checkValueBoardCurY value)}
updateBoardDestX :: BTreeBlackboard -> Integer -> BTreeBlackboard
updateBoardDestX blackboard value = blackboard { boardDestX = (checkValueBoardDestX value)}
updateBoardDestY :: BTreeBlackboard -> Integer -> BTreeBlackboard
updateBoardDestY blackboard value = blackboard { boardDestY = (checkValueBoardDestY value)}
updateBoardDir :: BTreeBlackboard -> Integer -> BTreeBlackboard
updateBoardDir blackboard value = blackboard { boardDir = (checkValueBoardDir value)}
updateBoardVictory :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateBoardVictory blackboard value = blackboard { boardVictory = (checkValueBoardVictory value)}

-- START OF SET FUNCTIONS FOR ARRAYS


-- START OF INITIAL BLACKBOARD VALUE

initialBlackboard :: Integer -> BTreeBlackboard
initialBlackboard seed = BTreeBlackboard newSereneGenerator newValPrevDestX newValPrevDestY newValCurX newValCurY newValDestX newValDestY newValDir newValVictory  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen8
    partialBlackboardPrevDestX = BTreeBlackboard newSereneGenerator 0 0 0 0 0 0 0 True
    initValPrevDestX :: StdGen -> (Integer, StdGen)
    initValPrevDestX curGen = (0, curGen)
      where
        blackboard = partialBlackboardPrevDestX

    (newValPrevDestX, tempGen1) = initValPrevDestX tempGen0

    partialBlackboardPrevDestY = BTreeBlackboard newSereneGenerator newValPrevDestX 0 0 0 0 0 0 True
    initValPrevDestY :: StdGen -> (Integer, StdGen)
    initValPrevDestY curGen = ((0 + 1), curGen)
      where
        blackboard = partialBlackboardPrevDestY

    (newValPrevDestY, tempGen2) = initValPrevDestY tempGen1

    partialBlackboardCurX = BTreeBlackboard newSereneGenerator newValPrevDestX newValPrevDestY 0 0 0 0 0 True
    initValCurX :: StdGen -> (Integer, StdGen)
    initValCurX curGen = (0, curGen)
      where
        blackboard = partialBlackboardCurX

    (newValCurX, tempGen3) = initValCurX tempGen2

    partialBlackboardCurY = BTreeBlackboard newSereneGenerator newValPrevDestX newValPrevDestY newValCurX 0 0 0 0 True
    initValCurY :: StdGen -> (Integer, StdGen)
    initValCurY curGen = (0, curGen)
      where
        blackboard = partialBlackboardCurY

    (newValCurY, tempGen4) = initValCurY tempGen3

    partialBlackboardDestX = BTreeBlackboard newSereneGenerator newValPrevDestX newValPrevDestY newValCurX newValCurY 0 0 0 True
    initValDestX :: StdGen -> (Integer, StdGen)
    initValDestX curGen = (0, curGen)
      where
        blackboard = partialBlackboardDestX

    (newValDestX, tempGen5) = initValDestX tempGen4

    partialBlackboardDestY = BTreeBlackboard newSereneGenerator newValPrevDestX newValPrevDestY newValCurX newValCurY newValDestX 0 0 True
    initValDestY :: StdGen -> (Integer, StdGen)
    initValDestY curGen = (0, curGen)
      where
        blackboard = partialBlackboardDestY

    (newValDestY, tempGen6) = initValDestY tempGen5

    partialBlackboardDir = BTreeBlackboard newSereneGenerator newValPrevDestX newValPrevDestY newValCurX newValCurY newValDestX newValDestY 0 True
    initValDir :: StdGen -> (Integer, StdGen)
    initValDir curGen = (1, curGen)
      where
        blackboard = partialBlackboardDir

    (newValDir, tempGen7) = initValDir tempGen6

    partialBlackboardVictory = BTreeBlackboard newSereneGenerator newValPrevDestX newValPrevDestY newValCurX newValCurY newValDestX newValDestY newValDir True
    initValVictory :: StdGen -> (Bool, StdGen)
    initValVictory curGen = (False, curGen)
      where
        blackboard = partialBlackboardVictory

    (newValVictory, tempGen8) = initValVictory tempGen7


