module BehaviorTreeBlackboard where
import SereneRandomizer
import System.Random
import SereneOperations

data BTreeBlackboard = BTreeBlackboard {
  sereneBoardGenerator :: StdGen
  , boardValue :: Integer
  }

fromBTreeBlackboardToString :: BTreeBlackboard -> String
fromBTreeBlackboardToString blackboard = "Board = {" ++ "boardValue: " ++ show (boardValue blackboard) ++ "}"

-- START OF BLACKBOARD FUNCTIONS


-- START OF LOCAL BLACKBOARD FUNCTIONS


-- START OF GET FUNCTIONS FOR LOCAL VARIABLES


-- START OF GET FUNCTIONS FOR ARRAYS


-- START OF TYPE CHECKING FUNCTIONS

checkValueBoardValue :: Integer -> Integer
checkValueBoardValue value = value


-- START OF SET FUNCTIONS

updateBoardGenerator :: BTreeBlackboard -> StdGen -> BTreeBlackboard
updateBoardGenerator blackboard newGen = blackboard { sereneBoardGenerator = newGen }
updateBoardValue :: BTreeBlackboard -> Integer -> BTreeBlackboard
updateBoardValue blackboard value = blackboard { boardValue = (checkValueBoardValue value)}

-- START OF SET FUNCTIONS FOR ARRAYS


-- START OF INITIAL BLACKBOARD VALUE

initialBlackboard :: Integer -> BTreeBlackboard
initialBlackboard seed = BTreeBlackboard newSereneGenerator newValValue  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen1
    partialBlackboardValue = BTreeBlackboard newSereneGenerator 0
    initValValue :: StdGen -> (Integer, StdGen)
    initValValue curGen = (privateRandom0 (fst (getRandomInteger curGen 19)), snd (getRandomInteger curGen 19))
      where
        blackboard = partialBlackboardValue
        privateRandom0 :: Integer -> Integer
        privateRandom0 0 = 1
        privateRandom0 1 = 2
        privateRandom0 2 = 3
        privateRandom0 3 = 4
        privateRandom0 4 = 5
        privateRandom0 5 = 6
        privateRandom0 6 = 7
        privateRandom0 7 = 8
        privateRandom0 8 = 9
        privateRandom0 9 = 10
        privateRandom0 10 = 11
        privateRandom0 11 = 12
        privateRandom0 12 = 13
        privateRandom0 13 = 14
        privateRandom0 14 = 15
        privateRandom0 15 = 16
        privateRandom0 16 = 17
        privateRandom0 17 = 18
        privateRandom0 18 = 19
        privateRandom0 _ = 20

    (newValValue, tempGen1) = initValValue tempGen0


