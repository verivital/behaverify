module BehaviorTreeBlackboard where
import SereneRandomizer
import System.Random
import SereneOperations

data BTreeBlackboard = BTreeBlackboard {
    boardGenerator :: StdGen
  }

fromBTreeBlackboardToString :: BTreeBlackboard -> String
fromBTreeBlackboardToString blackboard = "board = {" ++ "}"

-- START OF GET FUNCTIONS FOR LOCAL VARIABLES


-- START OF BLACKBOARD FUNCTIONS


-- START OF LOCAL BLACKBOARD FUNCTIONS


-- START OF INDEX FUNCTIONS FOR ARRAYS


-- START OF NEW ARRAY FUNCTIONS


-- START OF UPDATES


-- START OF INITIAL BLACKBOARD VALUE

initialBlackboard :: Integer -> BTreeBlackboard
initialBlackboard seed = newBlackboard
  where
    firstGen = getGenerator seed
    dummy = BTreeBlackboard firstGen 
    newBlackboard = dummy

