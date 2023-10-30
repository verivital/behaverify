module BehaviorTreeBlackboard where
import SereneRandomizer
import System.Random
import SereneOperations

data BTreeBlackboard = BTreeBlackboard {
    boardGenerator :: StdGen
  , boardBlVAR0 :: String
  }

fromBTreeBlackboardToString :: BTreeBlackboard -> String
fromBTreeBlackboardToString blackboard = "board = {" ++ "boardBlVAR0: " ++ (show (boardBlVAR0 blackboard)) ++ "}"

-- START OF GET FUNCTIONS FOR LOCAL VARIABLES


-- START OF BLACKBOARD FUNCTIONS


-- START OF LOCAL BLACKBOARD FUNCTIONS


-- START OF INDEX FUNCTIONS FOR ARRAYS


-- START OF NEW ARRAY FUNCTIONS


-- START OF UPDATES

boardUpdate :: BTreeBlackboard -> StdGen -> BTreeBlackboard
boardUpdate blackboard newGen = blackboard { boardGenerator = newGen }
boardUpdateBlVAR0 :: BTreeBlackboard -> StdGen -> String -> BTreeBlackboard
boardUpdateBlVAR0 blackboard newGen newVal = blackboard { boardGenerator = newGen, boardBlVAR0 = newVal }

-- START OF INITIAL BLACKBOARD VALUE

initialBlackboard :: Integer -> BTreeBlackboard
initialBlackboard seed = newBlackboard
  where
    -- START OF UDPATE FROZENVAR (for internal use only)
    -- START OF CREATING
    firstGen = getGenerator seed
    dummy = BTreeBlackboard firstGen " "
    statement0 :: BTreeBlackboard -> BTreeBlackboard
    statement0 blackboard = boardUpdateBlVAR0 blackboard newGenerator newVal
      where
        randomPair0 = (-1, boardGenerator blackboard)
        newGenerator = snd randomPair0
        newVal
          | True = "both"
          | otherwise = "yes"
    newBlackboard = (statement0 dummy)

