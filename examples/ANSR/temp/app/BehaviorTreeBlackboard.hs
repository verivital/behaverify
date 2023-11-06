module BehaviorTreeBlackboard where
import SereneRandomizer
import System.Random
import SereneOperations

data BTreeBlackboard = BTreeBlackboard {
    boardGenerator :: StdGen
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
fromBTreeBlackboardToString blackboard = "board = {" ++ "boardPrevDestX: " ++ (show (boardPrevDestX blackboard)) ++ ", " ++ "boardPrevDestY: " ++ (show (boardPrevDestY blackboard)) ++ ", " ++ "boardCurX: " ++ (show (boardCurX blackboard)) ++ ", " ++ "boardCurY: " ++ (show (boardCurY blackboard)) ++ ", " ++ "boardDestX: " ++ (show (boardDestX blackboard)) ++ ", " ++ "boardDestY: " ++ (show (boardDestY blackboard)) ++ ", " ++ "boardDir: " ++ (show (boardDir blackboard)) ++ ", " ++ "boardVictory: " ++ (show (boardVictory blackboard)) ++ ", " ++ "boardXNet11: " ++ (show (boardXNet11 blackboard)) ++ ", " ++ "boardXNet12: " ++ (show (boardXNet12 blackboard)) ++ ", " ++ "boardXNet13: " ++ (show (boardXNet13 blackboard)) ++ ", " ++ "boardXNet14: " ++ (show (boardXNet14 blackboard)) ++ ", " ++ "boardXNet15: " ++ (show (boardXNet15 blackboard)) ++ ", " ++ "boardXNet21: " ++ (show (boardXNet21 blackboard)) ++ ", " ++ "boardXNet22: " ++ (show (boardXNet22 blackboard)) ++ ", " ++ "boardXNet23: " ++ (show (boardXNet23 blackboard)) ++ ", " ++ "boardXNet24: " ++ (show (boardXNet24 blackboard)) ++ ", " ++ "boardXNet31: " ++ (show (boardXNet31 blackboard)) ++ ", " ++ "boardXNet32: " ++ (show (boardXNet32 blackboard)) ++ ", " ++ "boardXNet33: " ++ (show (boardXNet33 blackboard)) ++ ", " ++ "boardXNet34: " ++ (show (boardXNet34 blackboard)) ++ ", " ++ "boardXNet41: " ++ (show (boardXNet41 blackboard)) ++ ", " ++ "boardXNet42: " ++ (show (boardXNet42 blackboard)) ++ ", " ++ "boardXNet43: " ++ (show (boardXNet43 blackboard)) ++ ", " ++ "boardXNetOutput: " ++ (show (boardXNetOutput blackboard)) ++ ", " ++ "boardYNet11: " ++ (show (boardYNet11 blackboard)) ++ ", " ++ "boardYNet12: " ++ (show (boardYNet12 blackboard)) ++ ", " ++ "boardYNet13: " ++ (show (boardYNet13 blackboard)) ++ ", " ++ "boardYNet14: " ++ (show (boardYNet14 blackboard)) ++ ", " ++ "boardYNet15: " ++ (show (boardYNet15 blackboard)) ++ ", " ++ "boardYNet21: " ++ (show (boardYNet21 blackboard)) ++ ", " ++ "boardYNet22: " ++ (show (boardYNet22 blackboard)) ++ ", " ++ "boardYNet23: " ++ (show (boardYNet23 blackboard)) ++ ", " ++ "boardYNet24: " ++ (show (boardYNet24 blackboard)) ++ ", " ++ "boardYNet31: " ++ (show (boardYNet31 blackboard)) ++ ", " ++ "boardYNet32: " ++ (show (boardYNet32 blackboard)) ++ ", " ++ "boardYNet33: " ++ (show (boardYNet33 blackboard)) ++ ", " ++ "boardYNetOutput: " ++ (show (boardYNetOutput blackboard)) ++ "}"

-- START OF GET FUNCTIONS FOR LOCAL VARIABLES


-- START OF BLACKBOARD FUNCTIONS

boardXNet11 :: BTreeBlackboard  -> Integer
boardXNet11 blackboard = newVal
  where
    newVal = (max (boardDestX blackboard) 0)
boardXNet12 :: BTreeBlackboard  -> Integer
boardXNet12 blackboard = newVal
  where
    newVal = (max ((boardDestX blackboard) - (boardPrevDestX blackboard)) 0)
boardXNet13 :: BTreeBlackboard  -> Integer
boardXNet13 blackboard = newVal
  where
    newVal = (max ((boardPrevDestX blackboard) - (boardDestX blackboard)) 0)
boardXNet14 :: BTreeBlackboard  -> Integer
boardXNet14 blackboard = newVal
  where
    newVal = (max ((boardDestX blackboard) - (quot (0 + 10) 2)) 0)
boardXNet15 :: BTreeBlackboard  -> Integer
boardXNet15 blackboard = newVal
  where
    newVal = (max ((quot (0 + 10) 2) - (boardDestX blackboard)) 0)
boardXNet21 :: BTreeBlackboard  -> Integer
boardXNet21 blackboard = newVal
  where
    newVal = (max (boardXNet11 blackboard) 0)
boardXNet22 :: BTreeBlackboard  -> Integer
boardXNet22 blackboard = newVal
  where
    newVal = (max ( (- (boardXNet12 blackboard))+((- (boardXNet13 blackboard)) + 1)) 0)
boardXNet23 :: BTreeBlackboard  -> Integer
boardXNet23 blackboard = newVal
  where
    newVal = (max (1 - (boardXNet14 blackboard)) 0)
boardXNet24 :: BTreeBlackboard  -> Integer
boardXNet24 blackboard = newVal
  where
    newVal = (max (1 - (boardXNet15 blackboard)) 0)
boardXNet31 :: BTreeBlackboard  -> Integer
boardXNet31 blackboard = newVal
  where
    newVal = (max ((boardXNet21 blackboard) - ((boardXNet22 blackboard) * 10)) 0)
boardXNet32 :: BTreeBlackboard  -> Integer
boardXNet32 blackboard = newVal
  where
    newVal = (max (1 - (boardXNet22 blackboard)) 0)
boardXNet33 :: BTreeBlackboard  -> Integer
boardXNet33 blackboard = newVal
  where
    newVal = (max (boardXNet23 blackboard) 0)
boardXNet34 :: BTreeBlackboard  -> Integer
boardXNet34 blackboard = newVal
  where
    newVal = (max (boardXNet24 blackboard) 0)
boardXNet41 :: BTreeBlackboard  -> Integer
boardXNet41 blackboard = newVal
  where
    newVal = (max (boardXNet31 blackboard) 0)
boardXNet42 :: BTreeBlackboard  -> Integer
boardXNet42 blackboard = newVal
  where
    newVal = (max ((10 * (boardXNet33 blackboard)) - (10 * (boardXNet32 blackboard))) 0)
boardXNet43 :: BTreeBlackboard  -> Integer
boardXNet43 blackboard = newVal
  where
    newVal = (max ((0 * (boardXNet34 blackboard)) - (10 * (boardXNet32 blackboard))) 0)
boardXNetOutput :: BTreeBlackboard  -> Integer
boardXNetOutput blackboard = newVal
  where
    newVal = (max ( (boardXNet41 blackboard)+((boardXNet42 blackboard) + (boardXNet43 blackboard))) 0)
boardYNet11 :: BTreeBlackboard  -> Integer
boardYNet11 blackboard = newVal
  where
    newVal = (max (boardDestY blackboard) 0)
boardYNet12 :: BTreeBlackboard  -> Integer
boardYNet12 blackboard = newVal
  where
    newVal = (max ((boardDestY blackboard) - (boardPrevDestY blackboard)) 0)
boardYNet13 :: BTreeBlackboard  -> Integer
boardYNet13 blackboard = newVal
  where
    newVal = (max ((boardPrevDestY blackboard) - (boardDestY blackboard)) 0)
boardYNet14 :: BTreeBlackboard  -> Integer
boardYNet14 blackboard = newVal
  where
    newVal = (max (boardDir blackboard) 0)
boardYNet15 :: BTreeBlackboard  -> Integer
boardYNet15 blackboard = newVal
  where
    newVal = (max (- (boardDir blackboard)) 0)
boardYNet21 :: BTreeBlackboard  -> Integer
boardYNet21 blackboard = newVal
  where
    newVal = (max (boardYNet11 blackboard) 0)
boardYNet22 :: BTreeBlackboard  -> Integer
boardYNet22 blackboard = newVal
  where
    newVal = (max ( (- (boardYNet12 blackboard))+((- (boardYNet13 blackboard)) + 1)) 0)
boardYNet23 :: BTreeBlackboard  -> Integer
boardYNet23 blackboard = newVal
  where
    newVal = (max (boardYNet14 blackboard) 0)
boardYNet24 :: BTreeBlackboard  -> Integer
boardYNet24 blackboard = newVal
  where
    newVal = (max (boardYNet15 blackboard) 0)
boardYNet31 :: BTreeBlackboard  -> Integer
boardYNet31 blackboard = newVal
  where
    newVal = (max (boardYNet21 blackboard) 0)
boardYNet32 :: BTreeBlackboard  -> Integer
boardYNet32 blackboard = newVal
  where
    newVal = (max ( (boardYNet22 blackboard)+((boardYNet23 blackboard) + (-1))) 0)
boardYNet33 :: BTreeBlackboard  -> Integer
boardYNet33 blackboard = newVal
  where
    newVal = (max ( (boardYNet22 blackboard)+((boardYNet24 blackboard) + (-1))) 0)
boardYNetOutput :: BTreeBlackboard  -> Integer
boardYNetOutput blackboard = newVal
  where
    newVal = (max ( (boardYNet31 blackboard)+((2 * (boardYNet32 blackboard)) + ( (-1)*(2 * (boardYNet33 blackboard))))) 0)

-- START OF LOCAL BLACKBOARD FUNCTIONS


-- START OF INDEX FUNCTIONS FOR ARRAYS


-- START OF NEW ARRAY FUNCTIONS


-- START OF UPDATES

boardUpdate :: BTreeBlackboard -> StdGen -> BTreeBlackboard
boardUpdate blackboard newGen = blackboard { boardGenerator = newGen }
boardUpdatePrevDestX :: BTreeBlackboard -> StdGen -> Integer -> BTreeBlackboard
boardUpdatePrevDestX blackboard newGen newVal = blackboard { boardGenerator = newGen, boardPrevDestX = newVal }
boardUpdatePrevDestY :: BTreeBlackboard -> StdGen -> Integer -> BTreeBlackboard
boardUpdatePrevDestY blackboard newGen newVal = blackboard { boardGenerator = newGen, boardPrevDestY = newVal }
boardUpdateCurX :: BTreeBlackboard -> StdGen -> Integer -> BTreeBlackboard
boardUpdateCurX blackboard newGen newVal = blackboard { boardGenerator = newGen, boardCurX = newVal }
boardUpdateCurY :: BTreeBlackboard -> StdGen -> Integer -> BTreeBlackboard
boardUpdateCurY blackboard newGen newVal = blackboard { boardGenerator = newGen, boardCurY = newVal }
boardUpdateDestX :: BTreeBlackboard -> StdGen -> Integer -> BTreeBlackboard
boardUpdateDestX blackboard newGen newVal = blackboard { boardGenerator = newGen, boardDestX = newVal }
boardUpdateDestY :: BTreeBlackboard -> StdGen -> Integer -> BTreeBlackboard
boardUpdateDestY blackboard newGen newVal = blackboard { boardGenerator = newGen, boardDestY = newVal }
boardUpdateDir :: BTreeBlackboard -> StdGen -> Integer -> BTreeBlackboard
boardUpdateDir blackboard newGen newVal = blackboard { boardGenerator = newGen, boardDir = newVal }
boardUpdateVictory :: BTreeBlackboard -> StdGen -> Bool -> BTreeBlackboard
boardUpdateVictory blackboard newGen newVal = blackboard { boardGenerator = newGen, boardVictory = newVal }

-- START OF INITIAL BLACKBOARD VALUE

initialBlackboard :: Integer -> BTreeBlackboard
initialBlackboard seed = newBlackboard
  where
    -- START OF UDPATE FROZENVAR (for internal use only)
    -- START OF CREATING
    firstGen = getGenerator seed
    dummy = BTreeBlackboard firstGen 0 0 0 0 0 0 0 True
    statement0 :: BTreeBlackboard -> BTreeBlackboard
    statement0 blackboard = boardUpdatePrevDestX blackboard newGenerator newVal
      where
        randomPair0 = (-1, boardGenerator blackboard)
        newGenerator = snd randomPair0
        newVal = 0
    statement1 :: BTreeBlackboard -> BTreeBlackboard
    statement1 blackboard = boardUpdatePrevDestY blackboard newGenerator newVal
      where
        randomPair0 = (-1, boardGenerator blackboard)
        newGenerator = snd randomPair0
        newVal = (0 + 1)
    statement2 :: BTreeBlackboard -> BTreeBlackboard
    statement2 blackboard = boardUpdateCurX blackboard newGenerator newVal
      where
        randomPair0 = (-1, boardGenerator blackboard)
        newGenerator = snd randomPair0
        newVal = 0
    statement3 :: BTreeBlackboard -> BTreeBlackboard
    statement3 blackboard = boardUpdateCurY blackboard newGenerator newVal
      where
        randomPair0 = (-1, boardGenerator blackboard)
        newGenerator = snd randomPair0
        newVal = 0
    statement4 :: BTreeBlackboard -> BTreeBlackboard
    statement4 blackboard = boardUpdateDestX blackboard newGenerator newVal
      where
        randomPair0 = (-1, boardGenerator blackboard)
        newGenerator = snd randomPair0
        newVal = 0
    statement5 :: BTreeBlackboard -> BTreeBlackboard
    statement5 blackboard = boardUpdateDestY blackboard newGenerator newVal
      where
        randomPair0 = (-1, boardGenerator blackboard)
        newGenerator = snd randomPair0
        newVal = 0
    statement6 :: BTreeBlackboard -> BTreeBlackboard
    statement6 blackboard = boardUpdateDir blackboard newGenerator newVal
      where
        randomPair0 = (-1, boardGenerator blackboard)
        newGenerator = snd randomPair0
        newVal = 1
    statement7 :: BTreeBlackboard -> BTreeBlackboard
    statement7 blackboard = boardUpdateVictory blackboard newGenerator newVal
      where
        randomPair0 = (-1, boardGenerator blackboard)
        newGenerator = snd randomPair0
        newVal = False
    newBlackboard = (statement7 (statement6 (statement5 (statement4 (statement3 (statement2 (statement1 (statement0 dummy))))))))

