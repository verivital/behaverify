module BehaviorTreeBlackboard where
import SereneRandomizer
import System.Random
import SereneOperations

data BTreeBlackboard = BTreeBlackboard {
  sereneBoardGenerator :: StdGen
  , boardFooIndex0 :: Int
  , boardFooIndex1 :: Int
  , boardFooIndex2 :: Int
  , boardIndexVar :: Int
  , localBoardBar5Index0 :: String
  , localBoardBar5Index1 :: String
  , localBoardBar5Index2 :: String
  , localBoardBar4Index0 :: String
  , localBoardBar4Index1 :: String
  , localBoardBar4Index2 :: String
  }

instance Show BTreeBlackboard where
  show (BTreeBlackboard _ boardFooIndex0 boardFooIndex1 boardFooIndex2 boardIndexVar localBoardBar5Index0 localBoardBar5Index1 localBoardBar5Index2 localBoardBar4Index0 localBoardBar4Index1 localBoardBar4Index2) = "Board = {" ++ "boardFooIndex0: " ++ show boardFooIndex0 ++ ", boardFooIndex1: " ++ show boardFooIndex1 ++ ", boardFooIndex2: " ++ show boardFooIndex2 ++ ", boardIndexVar: " ++ show boardIndexVar ++ ", localBoardBar5Index0: " ++ show localBoardBar5Index0 ++ ", localBoardBar5Index1: " ++ show localBoardBar5Index1 ++ ", localBoardBar5Index2: " ++ show localBoardBar5Index2 ++ ", localBoardBar4Index0: " ++ show localBoardBar4Index0 ++ ", localBoardBar4Index1: " ++ show localBoardBar4Index1 ++ ", localBoardBar4Index2: " ++ show localBoardBar4Index2 ++ "}"

-- START OF BLACKBOARD FUNCTIONS

boardTrom :: Int -> BTreeBlackboard -> Int
boardTrom 0 blackboard = ((boardFoo 0 blackboard) + ((boardFoo 1 blackboard) + (boardFoo 2 blackboard)))
boardTrom 1 blackboard = ((boardFoo 0 blackboard) * ((boardFoo 1 blackboard) * (boardFoo 2 blackboard)))
boardTrom _ _ = error "boardTrom illegal index value"

-- START OF LOCAL BLACKBOARD FUNCTIONS


-- START OF GET FUNCTIONS FOR LOCAL VARIABLES

localBoardBar :: Int -> Int -> BTreeBlackboard -> String
localBoardBar 4 = localBoardBar4
localBoardBar 5 = localBoardBar5
localBoardBar _ = error "bar illegal local reference"

-- START OF GET FUNCTIONS FOR ARRAYS

boardFoo :: Int -> BTreeBlackboard -> Int
boardFoo 0 = boardFooIndex0
boardFoo 1 = boardFooIndex1
boardFoo 2 = boardFooIndex2
boardFoo _ = error "boardFoo illegal index value"
localBoardBar4 :: Int -> BTreeBlackboard -> String
localBoardBar4 0 = localBoardBar4Index0
localBoardBar4 1 = localBoardBar4Index1
localBoardBar4 2 = localBoardBar4Index2
localBoardBar4 _ = error "localBoardBar4 illegal index value"
localBoardBar5 :: Int -> BTreeBlackboard -> String
localBoardBar5 0 = localBoardBar5Index0
localBoardBar5 1 = localBoardBar5Index1
localBoardBar5 2 = localBoardBar5Index2
localBoardBar5 _ = error "localBoardBar5 illegal index value"

-- START OF TYPE CHECKING FUNCTIONS

checkValueBoardFoo :: Int -> Int
checkValueBoardFoo value
  | 0 > value || value > 10 = error "boardFoo illegal value"
  | otherwise = value

checkValueBoardIndexVar :: Int -> Int
checkValueBoardIndexVar value
  | 0 > value || value > 2 = error "boardIndexVar illegal value"
  | otherwise = value

checkValueLocalBoardBar :: String -> String
checkValueLocalBoardBar "increase" = "increase"
checkValueLocalBoardBar "decrease" = "decrease"
checkValueLocalBoardBar "nope" = "nope"
checkValueLocalBoardBar _ = error "localBoardBar illegal value"


-- START OF SET FUNCTIONS

updateBoardGenerator :: BTreeBlackboard -> StdGen -> BTreeBlackboard
updateBoardGenerator blackboard newGen = blackboard { sereneBoardGenerator = newGen }
updateBoardFooIndex0 :: BTreeBlackboard -> Int -> BTreeBlackboard
updateBoardFooIndex0 blackboard value = blackboard { boardFooIndex0 = (checkValueBoardFoo value)}
updateBoardFooIndex1 :: BTreeBlackboard -> Int -> BTreeBlackboard
updateBoardFooIndex1 blackboard value = blackboard { boardFooIndex1 = (checkValueBoardFoo value)}
updateBoardFooIndex2 :: BTreeBlackboard -> Int -> BTreeBlackboard
updateBoardFooIndex2 blackboard value = blackboard { boardFooIndex2 = (checkValueBoardFoo value)}
updateBoardIndexVar :: BTreeBlackboard -> Int -> BTreeBlackboard
updateBoardIndexVar blackboard value = blackboard { boardIndexVar = (checkValueBoardIndexVar value)}
updateLocalBoardBar5Index0 :: BTreeBlackboard -> String -> BTreeBlackboard
updateLocalBoardBar5Index0 blackboard value = blackboard { localBoardBar5Index0 = (checkValueLocalBoardBar value)}
updateLocalBoardBar5Index1 :: BTreeBlackboard -> String -> BTreeBlackboard
updateLocalBoardBar5Index1 blackboard value = blackboard { localBoardBar5Index1 = (checkValueLocalBoardBar value)}
updateLocalBoardBar5Index2 :: BTreeBlackboard -> String -> BTreeBlackboard
updateLocalBoardBar5Index2 blackboard value = blackboard { localBoardBar5Index2 = (checkValueLocalBoardBar value)}
updateLocalBoardBar4Index0 :: BTreeBlackboard -> String -> BTreeBlackboard
updateLocalBoardBar4Index0 blackboard value = blackboard { localBoardBar4Index0 = (checkValueLocalBoardBar value)}
updateLocalBoardBar4Index1 :: BTreeBlackboard -> String -> BTreeBlackboard
updateLocalBoardBar4Index1 blackboard value = blackboard { localBoardBar4Index1 = (checkValueLocalBoardBar value)}
updateLocalBoardBar4Index2 :: BTreeBlackboard -> String -> BTreeBlackboard
updateLocalBoardBar4Index2 blackboard value = blackboard { localBoardBar4Index2 = (checkValueLocalBoardBar value)}

-- START OF SET FUNCTIONS FOR ARRAYS

updateBoardFoo :: Int -> BTreeBlackboard -> Int -> BTreeBlackboard
updateBoardFoo 0 = updateBoardFooIndex0
updateBoardFoo 1 = updateBoardFooIndex1
updateBoardFoo 2 = updateBoardFooIndex2
updateBoardFoo _ = error "BoardFoo illegal index value"
arrayUpdateBoardFoo :: BTreeBlackboard -> [(Int, Int)] -> BTreeBlackboard
arrayUpdateBoardFoo blackboard []  = blackboard
arrayUpdateBoardFoo blackboard [(index, value)] = updateBoardFoo index blackboard value
arrayUpdateBoardFoo blackboard indicesValues = blackboard {
  boardFooIndex0 = newFooIndex0
  , boardFooIndex1 = newFooIndex1
  , boardFooIndex2 = newFooIndex2
  }
    where
      (newFooIndex0, newFooIndex1, newFooIndex2) = updateValues indicesValues
      updateValues :: [(Int, Int)] -> (Int, Int, Int)
      updateValues [] = (boardFooIndex0 blackboard, boardFooIndex1 blackboard, boardFooIndex2 blackboard)
      updateValues ((0, currentValue) : nextIndicesValues) = (checkValueBoardFoo currentValue, updatedValue1, updatedValue2)
        where
          (_, updatedValue1, updatedValue2) = updateValues nextIndicesValues
      updateValues ((1, currentValue) : nextIndicesValues) = (updatedValue0, checkValueBoardFoo currentValue, updatedValue2)
        where
          (updatedValue0, _, updatedValue2) = updateValues nextIndicesValues
      updateValues ((2, currentValue) : nextIndicesValues) = (updatedValue0, updatedValue1, checkValueBoardFoo currentValue)
        where
          (updatedValue0, updatedValue1, _) = updateValues nextIndicesValues
updateLocalBoardBar :: Int -> Int -> BTreeBlackboard -> String -> BTreeBlackboard
updateLocalBoardBar 4 = updateLocalBoardBar4
updateLocalBoardBar 5 = updateLocalBoardBar5
updateLocalBoardBar _ = error "localBoardBar illegal local reference"
arrayUpdateLocalBoardBar :: Int -> BTreeBlackboard -> [(Int, String)] -> BTreeBlackboard
arrayUpdateLocalBoardBar 4 = arrayUpdateLocalBoardBar4
arrayUpdateLocalBoardBar 5 = arrayUpdateLocalBoardBar5
arrayUpdateLocalBoardBar _ = error "localBoardBar illegal local reference"
updateLocalBoardBar4 :: Int -> BTreeBlackboard -> String -> BTreeBlackboard
updateLocalBoardBar4 0 = updateLocalBoardBar4Index0
updateLocalBoardBar4 1 = updateLocalBoardBar4Index1
updateLocalBoardBar4 2 = updateLocalBoardBar4Index2
updateLocalBoardBar4 _ = error "LocalBoardBar4 illegal index value"
arrayUpdateLocalBoardBar4 :: BTreeBlackboard -> [(Int, String)] -> BTreeBlackboard
arrayUpdateLocalBoardBar4 blackboard []  = blackboard
arrayUpdateLocalBoardBar4 blackboard [(index, value)] = updateLocalBoardBar4 index blackboard value
arrayUpdateLocalBoardBar4 blackboard indicesValues = blackboard {
  localBoardBar4Index0 = newBar4Index0
  , localBoardBar4Index1 = newBar4Index1
  , localBoardBar4Index2 = newBar4Index2
  }
    where
      (newBar4Index0, newBar4Index1, newBar4Index2) = updateValues indicesValues
      updateValues :: [(Int, String)] -> (String, String, String)
      updateValues [] = (localBoardBar4Index0 blackboard, localBoardBar4Index1 blackboard, localBoardBar4Index2 blackboard)
      updateValues ((0, currentValue) : nextIndicesValues) = (checkValueLocalBoardBar currentValue, updatedValue1, updatedValue2)
        where
          (_, updatedValue1, updatedValue2) = updateValues nextIndicesValues
      updateValues ((1, currentValue) : nextIndicesValues) = (updatedValue0, checkValueLocalBoardBar currentValue, updatedValue2)
        where
          (updatedValue0, _, updatedValue2) = updateValues nextIndicesValues
      updateValues ((2, currentValue) : nextIndicesValues) = (updatedValue0, updatedValue1, checkValueLocalBoardBar currentValue)
        where
          (updatedValue0, updatedValue1, _) = updateValues nextIndicesValues
updateLocalBoardBar5 :: Int -> BTreeBlackboard -> String -> BTreeBlackboard
updateLocalBoardBar5 0 = updateLocalBoardBar5Index0
updateLocalBoardBar5 1 = updateLocalBoardBar5Index1
updateLocalBoardBar5 2 = updateLocalBoardBar5Index2
updateLocalBoardBar5 _ = error "LocalBoardBar5 illegal index value"
arrayUpdateLocalBoardBar5 :: BTreeBlackboard -> [(Int, String)] -> BTreeBlackboard
arrayUpdateLocalBoardBar5 blackboard []  = blackboard
arrayUpdateLocalBoardBar5 blackboard [(index, value)] = updateLocalBoardBar5 index blackboard value
arrayUpdateLocalBoardBar5 blackboard indicesValues = blackboard {
  localBoardBar5Index0 = newBar5Index0
  , localBoardBar5Index1 = newBar5Index1
  , localBoardBar5Index2 = newBar5Index2
  }
    where
      (newBar5Index0, newBar5Index1, newBar5Index2) = updateValues indicesValues
      updateValues :: [(Int, String)] -> (String, String, String)
      updateValues [] = (localBoardBar5Index0 blackboard, localBoardBar5Index1 blackboard, localBoardBar5Index2 blackboard)
      updateValues ((0, currentValue) : nextIndicesValues) = (checkValueLocalBoardBar currentValue, updatedValue1, updatedValue2)
        where
          (_, updatedValue1, updatedValue2) = updateValues nextIndicesValues
      updateValues ((1, currentValue) : nextIndicesValues) = (updatedValue0, checkValueLocalBoardBar currentValue, updatedValue2)
        where
          (updatedValue0, _, updatedValue2) = updateValues nextIndicesValues
      updateValues ((2, currentValue) : nextIndicesValues) = (updatedValue0, updatedValue1, checkValueLocalBoardBar currentValue)
        where
          (updatedValue0, updatedValue1, _) = updateValues nextIndicesValues

-- START OF INITIAL BLACKBOARD VALUE

initialBlackboard :: Int -> BTreeBlackboard
initialBlackboard seed = BTreeBlackboard newSereneGenerator newValFooIndex0 newValFooIndex1 newValFooIndex2 newValIndexVar localNewValBar5Index0 localNewValBar5Index1 localNewValBar5Index2 localNewValBar4Index0 localNewValBar4Index1 localNewValBar4Index2  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen10
    partialBlackboardFooIndex0 = BTreeBlackboard newSereneGenerator 0 0 0 0 " " " " " " " " " " " "
    initValFooIndex0 :: StdGen -> (Int, StdGen)
    initValFooIndex0 curGen = (0, curGen)
      where
        blackboard = partialBlackboardFooIndex0

    (newValFooIndex0, tempGen1) = initValFooIndex0 tempGen0

    partialBlackboardFooIndex1 = BTreeBlackboard newSereneGenerator newValFooIndex0 0 0 0 " " " " " " " " " " " "
    initValFooIndex1 :: StdGen -> (Int, StdGen)
    initValFooIndex1 curGen = (1, curGen)
      where
        blackboard = partialBlackboardFooIndex1

    (newValFooIndex1, tempGen2) = initValFooIndex1 tempGen1

    partialBlackboardFooIndex2 = BTreeBlackboard newSereneGenerator newValFooIndex0 newValFooIndex1 0 0 " " " " " " " " " " " "
    initValFooIndex2 :: StdGen -> (Int, StdGen)
    initValFooIndex2 curGen = (2, curGen)
      where
        blackboard = partialBlackboardFooIndex2

    (newValFooIndex2, tempGen3) = initValFooIndex2 tempGen2

    partialBlackboardIndexVar = BTreeBlackboard newSereneGenerator newValFooIndex0 newValFooIndex1 newValFooIndex2 0 " " " " " " " " " " " "
    initValIndexVar :: StdGen -> (Int, StdGen)
    initValIndexVar curGen = (privateRandom0 (fst (getRandomInt curGen 2)), snd (getRandomInt curGen 2))
      where
        blackboard = partialBlackboardIndexVar
        privateRandom0 :: Int -> Int
        privateRandom0 0 = 0
        privateRandom0 1 = 1
        privateRandom0 _ = 2

    (newValIndexVar, tempGen4) = initValIndexVar tempGen3

    partialBlackboardBar5Index0 = BTreeBlackboard newSereneGenerator newValFooIndex0 newValFooIndex1 newValFooIndex2 newValIndexVar " " " " " " " " " " " "
    localInitValBar5Index0 :: StdGen -> (String, StdGen)
    localInitValBar5Index0 curGen = ("increase", curGen)
      where
        blackboard = partialBlackboardBar5Index0
        nodeLocation = 5

    (localNewValBar5Index0, tempGen5) = localInitValBar5Index0 tempGen4

    partialBlackboardBar5Index1 = BTreeBlackboard newSereneGenerator newValFooIndex0 newValFooIndex1 newValFooIndex2 newValIndexVar localNewValBar5Index0 " " " " " " " " " "
    localInitValBar5Index1 :: StdGen -> (String, StdGen)
    localInitValBar5Index1 curGen = (privateRandom0 (fst (getRandomInt curGen 1)), snd (getRandomInt curGen 1))
      where
        blackboard = partialBlackboardBar5Index1
        nodeLocation = 5
        privateRandom0 :: Int -> String
        privateRandom0 0 = "increase"
        privateRandom0 _ = "decrease"

    (localNewValBar5Index1, tempGen6) = localInitValBar5Index1 tempGen5

    partialBlackboardBar5Index2 = BTreeBlackboard newSereneGenerator newValFooIndex0 newValFooIndex1 newValFooIndex2 newValIndexVar localNewValBar5Index0 localNewValBar5Index1 " " " " " " " "
    localInitValBar5Index2 :: StdGen -> (String, StdGen)
    localInitValBar5Index2 curGen
      | False = (privateRandom0 (fst (getRandomInt curGen 1)), snd (getRandomInt curGen 1))
      | otherwise = ("nope", curGen)
      where
        blackboard = partialBlackboardBar5Index2
        nodeLocation = 5
        privateRandom0 :: Int -> String
        privateRandom0 0 = "increase"
        privateRandom0 _ = "decrease"

    (localNewValBar5Index2, tempGen7) = localInitValBar5Index2 tempGen6

    partialBlackboardBar4Index0 = BTreeBlackboard newSereneGenerator newValFooIndex0 newValFooIndex1 newValFooIndex2 newValIndexVar localNewValBar5Index0 localNewValBar5Index1 localNewValBar5Index2 " " " " " "
    localInitValBar4Index0 :: StdGen -> (String, StdGen)
    localInitValBar4Index0 curGen
      | (0 == 0) = ("increase", curGen)
      | (1 == 0) = ("decrease", curGen)
      | otherwise = ("nope", curGen)
      where
        blackboard = partialBlackboardBar4Index0
        nodeLocation = 4

    (localNewValBar4Index0, tempGen8) = localInitValBar4Index0 tempGen7

    partialBlackboardBar4Index1 = BTreeBlackboard newSereneGenerator newValFooIndex0 newValFooIndex1 newValFooIndex2 newValIndexVar localNewValBar5Index0 localNewValBar5Index1 localNewValBar5Index2 localNewValBar4Index0 " " " "
    localInitValBar4Index1 :: StdGen -> (String, StdGen)
    localInitValBar4Index1 curGen
      | (0 == 1) = ("increase", curGen)
      | (1 == 1) = ("decrease", curGen)
      | otherwise = ("nope", curGen)
      where
        blackboard = partialBlackboardBar4Index1
        nodeLocation = 4

    (localNewValBar4Index1, tempGen9) = localInitValBar4Index1 tempGen8

    partialBlackboardBar4Index2 = BTreeBlackboard newSereneGenerator newValFooIndex0 newValFooIndex1 newValFooIndex2 newValIndexVar localNewValBar5Index0 localNewValBar5Index1 localNewValBar5Index2 localNewValBar4Index0 localNewValBar4Index1 " "
    localInitValBar4Index2 :: StdGen -> (String, StdGen)
    localInitValBar4Index2 curGen
      | (0 == 2) = ("increase", curGen)
      | (1 == 2) = ("decrease", curGen)
      | otherwise = ("nope", curGen)
      where
        blackboard = partialBlackboardBar4Index2
        nodeLocation = 4

    (localNewValBar4Index2, tempGen10) = localInitValBar4Index2 tempGen9


