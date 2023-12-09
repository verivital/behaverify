module BehaviorTreeBlackboard where
import SereneRandomizer
import System.Random
import SereneOperations

data BTreeBlackboard = BTreeBlackboard {
    boardGenerator :: StdGen
  , boardCurX :: Integer
  , boardCurY :: Integer
  , boardDestX :: Integer
  , boardDestY :: Integer
  , boardXMode :: Bool
  , boardYDir :: Integer
  , boardVictory :: Bool
  }

fromBTreeBlackboardToString :: BTreeBlackboard -> String
fromBTreeBlackboardToString blackboard = "board = {" ++ "boardCurX: " ++ (show (boardCurX blackboard)) ++ ", " ++ "boardCurY: " ++ (show (boardCurY blackboard)) ++ ", " ++ "boardDestX: " ++ (show (boardDestX blackboard)) ++ ", " ++ "boardDestY: " ++ (show (boardDestY blackboard)) ++ ", " ++ "boardXMode: " ++ (show (boardXMode blackboard)) ++ ", " ++ "boardYDir: " ++ (show (boardYDir blackboard)) ++ ", " ++ "boardVictory: " ++ (show (boardVictory blackboard)) ++ "}"

-- START OF GET FUNCTIONS FOR LOCAL VARIABLES


-- START OF BLACKBOARD FUNCTIONS


-- START OF LOCAL BLACKBOARD FUNCTIONS


-- START OF INDEX FUNCTIONS FOR ARRAYS


-- START OF NEW ARRAY FUNCTIONS


-- START OF UPDATES

boardUpdate :: BTreeBlackboard -> StdGen -> BTreeBlackboard
boardUpdate blackboard newGen = blackboard { boardGenerator = newGen }
boardUpdateCurX :: BTreeBlackboard -> StdGen -> Integer -> BTreeBlackboard
boardUpdateCurX blackboard newGen newVal = blackboard { boardGenerator = newGen, boardCurX = newVal }
boardUpdateCurY :: BTreeBlackboard -> StdGen -> Integer -> BTreeBlackboard
boardUpdateCurY blackboard newGen newVal = blackboard { boardGenerator = newGen, boardCurY = newVal }
boardUpdateDestX :: BTreeBlackboard -> StdGen -> Integer -> BTreeBlackboard
boardUpdateDestX blackboard newGen newVal = blackboard { boardGenerator = newGen, boardDestX = newVal }
boardUpdateDestY :: BTreeBlackboard -> StdGen -> Integer -> BTreeBlackboard
boardUpdateDestY blackboard newGen newVal = blackboard { boardGenerator = newGen, boardDestY = newVal }
boardUpdateXMode :: BTreeBlackboard -> StdGen -> Bool -> BTreeBlackboard
boardUpdateXMode blackboard newGen newVal = blackboard { boardGenerator = newGen, boardXMode = newVal }
boardUpdateYDir :: BTreeBlackboard -> StdGen -> Integer -> BTreeBlackboard
boardUpdateYDir blackboard newGen newVal = blackboard { boardGenerator = newGen, boardYDir = newVal }
boardUpdateVictory :: BTreeBlackboard -> StdGen -> Bool -> BTreeBlackboard
boardUpdateVictory blackboard newGen newVal = blackboard { boardGenerator = newGen, boardVictory = newVal }

-- START OF INITIAL BLACKBOARD VALUE

initialBlackboard :: Integer -> BTreeBlackboard
initialBlackboard seed = newBlackboard
  where
    -- START OF UDPATE FROZENVAR (for internal use only)
    -- START OF CREATING
    firstGen = getGenerator seed
    dummy = BTreeBlackboard firstGen 0 0 0 0 True 0 True
    statement0 :: BTreeBlackboard -> BTreeBlackboard
    statement0 blackboard = boardUpdateCurX blackboard newGenerator newVal
      where
        randomPair0 = (-1, boardGenerator blackboard)
        newGenerator = snd randomPair0
        newVal = 0
    statement1 :: BTreeBlackboard -> BTreeBlackboard
    statement1 blackboard = boardUpdateCurY blackboard newGenerator newVal
      where
        randomPair0 = (-1, boardGenerator blackboard)
        newGenerator = snd randomPair0
        newVal = 0
    statement2 :: BTreeBlackboard -> BTreeBlackboard
    statement2 blackboard = boardUpdateDestX blackboard newGenerator newVal
      where
        randomPair0 = (-1, boardGenerator blackboard)
        newGenerator = snd randomPair0
        newVal = 0
    statement3 :: BTreeBlackboard -> BTreeBlackboard
    statement3 blackboard = boardUpdateDestY blackboard newGenerator newVal
      where
        randomPair0 = (-1, boardGenerator blackboard)
        newGenerator = snd randomPair0
        newVal = 0
    statement4 :: BTreeBlackboard -> BTreeBlackboard
    statement4 blackboard = boardUpdateXMode blackboard newGenerator newVal
      where
        randomPair0 = (-1, boardGenerator blackboard)
        newGenerator = snd randomPair0
        newVal = False
    statement5 :: BTreeBlackboard -> BTreeBlackboard
    statement5 blackboard = boardUpdateYDir blackboard newGenerator newVal
      where
        randomPair0 = (-1, boardGenerator blackboard)
        newGenerator = snd randomPair0
        newVal = 1
    statement6 :: BTreeBlackboard -> BTreeBlackboard
    statement6 blackboard = boardUpdateVictory blackboard newGenerator newVal
      where
        randomPair0 = (-1, boardGenerator blackboard)
        newGenerator = snd randomPair0
        newVal = False
    newBlackboard = (statement6 (statement5 (statement4 (statement3 (statement2 (statement1 (statement0 dummy)))))))

