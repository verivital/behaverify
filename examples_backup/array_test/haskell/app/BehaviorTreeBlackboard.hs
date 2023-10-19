module BehaviorTreeBlackboard where
import SereneRandomizer
import System.Random
import SereneOperations

data BTreeBlackboard = BTreeBlackboard {
  sereneBoardGenerator :: StdGen
  , boardFooIndex0 :: Integer
  , boardFooIndex1 :: Integer
  , boardFooIndex2 :: Integer
  , boardIndexVar :: Integer
  , localBoardBarLocation5Index0 :: String
  , localBoardBarLocation5Index1 :: String
  , localBoardBarLocation5Index2 :: String
  , localBoardBarLocation4Index0 :: String
  , localBoardBarLocation4Index1 :: String
  , localBoardBarLocation4Index2 :: String
  }

fromBTreeBlackboardToString :: BTreeBlackboard -> String
fromBTreeBlackboardToString blackboard = "Board = {" ++ "boardFoo: " ++ "[" ++ show (boardFoo 0 blackboard) ++ ", " ++ show (boardFoo 1 blackboard) ++ ", " ++ show (boardFoo 2 blackboard)++ "]" ++ ", " ++ "boardFoo: " ++ "[" ++ show (boardFoo 0 blackboard) ++ ", " ++ show (boardFoo 1 blackboard) ++ ", " ++ show (boardFoo 2 blackboard)++ "]" ++ ", " ++ "boardFoo: " ++ "[" ++ show (boardFoo 0 blackboard) ++ ", " ++ show (boardFoo 1 blackboard) ++ ", " ++ show (boardFoo 2 blackboard)++ "]" ++ ", " ++ "boardIndexVar: " ++ show (boardIndexVar blackboard) ++ ", " ++ "localBoardBarLocation5: " ++ "[" ++ show (localBoardBar 5 0 blackboard) ++ ", " ++ show (localBoardBar 5 1 blackboard) ++ ", " ++ show (localBoardBar 5 2 blackboard)++ "]" ++ ", " ++ "localBoardBarLocation4: " ++ "[" ++ show (localBoardBar 4 0 blackboard) ++ ", " ++ show (localBoardBar 4 1 blackboard) ++ ", " ++ show (localBoardBar 4 2 blackboard)++ "]" ++ ", " ++ "boardTrom: " ++ "[" ++ show (boardTrom 0 blackboard) ++ ", " ++ show (boardTrom 1 blackboard)++ "]" ++ "}"

-- START OF BLACKBOARD FUNCTIONS

boardTrom :: Integer -> BTreeBlackboard -> Integer
boardTrom 0 blackboard = ((boardFoo 0 blackboard) + ((boardFoo 1 blackboard) + (boardFoo 2 blackboard)))
boardTrom 1 blackboard = ((boardFoo 0 blackboard) * ((boardFoo 1 blackboard) * (boardFoo 2 blackboard)))
boardTrom _ _ = error "boardTrom illegal index value"

-- START OF LOCAL BLACKBOARD FUNCTIONS


-- START OF GET FUNCTIONS FOR LOCAL VARIABLES

localBoardBar :: Integer -> Integer -> BTreeBlackboard -> String
localBoardBar 4 = localBoardBarLocation4
localBoardBar 5 = localBoardBarLocation5
localBoardBar _ = error "bar illegal local reference"

-- START OF GET FUNCTIONS FOR ARRAYS

boardFoo :: Integer -> BTreeBlackboard -> Integer
boardFoo 0 = boardFooIndex0
boardFoo 1 = boardFooIndex1
boardFoo 2 = boardFooIndex2
boardFoo _ = error "boardFoo illegal index value"
localBoardBarLocation4 :: Integer -> BTreeBlackboard -> String
localBoardBarLocation4 0 = localBoardBarLocation4Index0
localBoardBarLocation4 1 = localBoardBarLocation4Index1
localBoardBarLocation4 2 = localBoardBarLocation4Index2
localBoardBar4 _ = error "localBoardBar4 illegal index value"
localBoardBarLocation5 :: Integer -> BTreeBlackboard -> String
localBoardBarLocation5 0 = localBoardBarLocation5Index0
localBoardBarLocation5 1 = localBoardBarLocation5Index1
localBoardBarLocation5 2 = localBoardBarLocation5Index2
localBoardBar5 _ = error "localBoardBar5 illegal index value"

-- START OF TYPE CHECKING FUNCTIONS

checkValueBoardFoo :: Integer -> Integer
checkValueBoardFoo value
  | 0 > value || value > 10 = error "boardFoo illegal value"
  | otherwise = value

checkValueBoardIndexVar :: Integer -> Integer
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
updateBoardFooIndex0 :: BTreeBlackboard -> Integer -> BTreeBlackboard
updateBoardFooIndex0 blackboard value = blackboard { boardFooIndex0 = (checkValueBoardFoo value)}
updateBoardFooIndex1 :: BTreeBlackboard -> Integer -> BTreeBlackboard
updateBoardFooIndex1 blackboard value = blackboard { boardFooIndex1 = (checkValueBoardFoo value)}
updateBoardFooIndex2 :: BTreeBlackboard -> Integer -> BTreeBlackboard
updateBoardFooIndex2 blackboard value = blackboard { boardFooIndex2 = (checkValueBoardFoo value)}
updateBoardIndexVar :: BTreeBlackboard -> Integer -> BTreeBlackboard
updateBoardIndexVar blackboard value = blackboard { boardIndexVar = (checkValueBoardIndexVar value)}
updateLocalBoardBarLocation5Index0 :: BTreeBlackboard -> String -> BTreeBlackboard
updateLocalBoardBarLocation5Index0 blackboard value = blackboard { localBoardBarLocation5Index0 = (checkValueLocalBoardBar value)}
updateLocalBoardBarLocation5Index1 :: BTreeBlackboard -> String -> BTreeBlackboard
updateLocalBoardBarLocation5Index1 blackboard value = blackboard { localBoardBarLocation5Index1 = (checkValueLocalBoardBar value)}
updateLocalBoardBarLocation5Index2 :: BTreeBlackboard -> String -> BTreeBlackboard
updateLocalBoardBarLocation5Index2 blackboard value = blackboard { localBoardBarLocation5Index2 = (checkValueLocalBoardBar value)}
updateLocalBoardBarLocation4Index0 :: BTreeBlackboard -> String -> BTreeBlackboard
updateLocalBoardBarLocation4Index0 blackboard value = blackboard { localBoardBarLocation4Index0 = (checkValueLocalBoardBar value)}
updateLocalBoardBarLocation4Index1 :: BTreeBlackboard -> String -> BTreeBlackboard
updateLocalBoardBarLocation4Index1 blackboard value = blackboard { localBoardBarLocation4Index1 = (checkValueLocalBoardBar value)}
updateLocalBoardBarLocation4Index2 :: BTreeBlackboard -> String -> BTreeBlackboard
updateLocalBoardBarLocation4Index2 blackboard value = blackboard { localBoardBarLocation4Index2 = (checkValueLocalBoardBar value)}

-- START OF SET FUNCTIONS FOR ARRAYS

updateBoardFoo :: Integer -> BTreeBlackboard -> Integer -> BTreeBlackboard
updateBoardFoo 0 = updateBoardFooIndex0
updateBoardFoo 1 = updateBoardFooIndex1
updateBoardFoo 2 = updateBoardFooIndex2
updateBoardFoo _ = error "BoardFoo illegal index value"
arrayUpdateBoardFoo :: BTreeBlackboard -> [(Integer, Integer)] -> BTreeBlackboard
arrayUpdateBoardFoo blackboard []  = blackboard
arrayUpdateBoardFoo blackboard [(index, value)] = updateBoardFoo index blackboard value
arrayUpdateBoardFoo blackboard indicesValues = blackboard {
  boardFooIndex0 = newFooIndex0
  , boardFooIndex1 = newFooIndex1
  , boardFooIndex2 = newFooIndex2
  }
    where
      (newFooIndex0, newFooIndex1, newFooIndex2) = updateValues indicesValues
      updateValues :: [(Integer, Integer)] -> (Integer, Integer, Integer)
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
updateLocalBoardBar :: Integer -> Integer -> BTreeBlackboard -> String -> BTreeBlackboard
updateLocalBoardBar 4 = updateLocalBoardBarLocation4
updateLocalBoardBar 5 = updateLocalBoardBarLocation5
updateLocalBoardBar _ = error "localBoardBar illegal local reference"
arrayUpdateLocalBoardBar :: Integer -> BTreeBlackboard -> [(Integer, String)] -> BTreeBlackboard
arrayUpdateLocalBoardBar 4 = arrayUpdateLocalBoardBarLocation4
arrayUpdateLocalBoardBar 5 = arrayUpdateLocalBoardBarLocation5
arrayUpdateLocalBoardBar _ = error "localBoardBar illegal local reference"
updateLocalBoardBarLocation4 :: Integer -> BTreeBlackboard -> String -> BTreeBlackboard
updateLocalBoardBarLocation4 0 = updateLocalBoardBarLocation4Index0
updateLocalBoardBarLocation4 1 = updateLocalBoardBarLocation4Index1
updateLocalBoardBarLocation4 2 = updateLocalBoardBarLocation4Index2
updateLocalBoardBarLocation4 _ = error "LocalBoardBarLocation4 illegal index value"
arrayUpdateLocalBoardBarLocation4 :: BTreeBlackboard -> [(Integer, String)] -> BTreeBlackboard
arrayUpdateLocalBoardBarLocation4 blackboard []  = blackboard
arrayUpdateLocalBoardBarLocation4 blackboard [(index, value)] = updateLocalBoardBarLocation4 index blackboard value
arrayUpdateLocalBoardBarLocation4 blackboard indicesValues = blackboard {
  localBoardBarLocation4Index0 = newBarLocation4Index0
  , localBoardBarLocation4Index1 = newBarLocation4Index1
  , localBoardBarLocation4Index2 = newBarLocation4Index2
  }
    where
      (newBarLocation4Index0, newBarLocation4Index1, newBarLocation4Index2) = updateValues indicesValues
      updateValues :: [(Integer, String)] -> (String, String, String)
      updateValues [] = (localBoardBarLocation4Index0 blackboard, localBoardBarLocation4Index1 blackboard, localBoardBarLocation4Index2 blackboard)
      updateValues ((0, currentValue) : nextIndicesValues) = (checkValueLocalBoardBar currentValue, updatedValue1, updatedValue2)
        where
          (_, updatedValue1, updatedValue2) = updateValues nextIndicesValues
      updateValues ((1, currentValue) : nextIndicesValues) = (updatedValue0, checkValueLocalBoardBar currentValue, updatedValue2)
        where
          (updatedValue0, _, updatedValue2) = updateValues nextIndicesValues
      updateValues ((2, currentValue) : nextIndicesValues) = (updatedValue0, updatedValue1, checkValueLocalBoardBar currentValue)
        where
          (updatedValue0, updatedValue1, _) = updateValues nextIndicesValues
updateLocalBoardBarLocation5 :: Integer -> BTreeBlackboard -> String -> BTreeBlackboard
updateLocalBoardBarLocation5 0 = updateLocalBoardBarLocation5Index0
updateLocalBoardBarLocation5 1 = updateLocalBoardBarLocation5Index1
updateLocalBoardBarLocation5 2 = updateLocalBoardBarLocation5Index2
updateLocalBoardBarLocation5 _ = error "LocalBoardBarLocation5 illegal index value"
arrayUpdateLocalBoardBarLocation5 :: BTreeBlackboard -> [(Integer, String)] -> BTreeBlackboard
arrayUpdateLocalBoardBarLocation5 blackboard []  = blackboard
arrayUpdateLocalBoardBarLocation5 blackboard [(index, value)] = updateLocalBoardBarLocation5 index blackboard value
arrayUpdateLocalBoardBarLocation5 blackboard indicesValues = blackboard {
  localBoardBarLocation5Index0 = newBarLocation5Index0
  , localBoardBarLocation5Index1 = newBarLocation5Index1
  , localBoardBarLocation5Index2 = newBarLocation5Index2
  }
    where
      (newBarLocation5Index0, newBarLocation5Index1, newBarLocation5Index2) = updateValues indicesValues
      updateValues :: [(Integer, String)] -> (String, String, String)
      updateValues [] = (localBoardBarLocation5Index0 blackboard, localBoardBarLocation5Index1 blackboard, localBoardBarLocation5Index2 blackboard)
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

initialBlackboard :: Integer -> BTreeBlackboard
initialBlackboard seed = BTreeBlackboard newSereneGenerator newValFooIndex0 newValFooIndex1 newValFooIndex2 newValIndexVar localNewValBarLocation5Index0 localNewValBarLocation5Index1 localNewValBarLocation5Index2 localNewValBarLocation4Index0 localNewValBarLocation4Index1 localNewValBarLocation4Index2  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen10
    partialBlackboardFooIndex0 = BTreeBlackboard newSereneGenerator 0 0 0 0 " " " " " " " " " " " "
    initValFooIndex0 :: StdGen -> (Integer, StdGen)
    initValFooIndex0 curGen = (0, curGen)
      where
        blackboard = partialBlackboardFooIndex0

    (newValFooIndex0, tempGen1) = initValFooIndex0 tempGen0

    partialBlackboardFooIndex1 = BTreeBlackboard newSereneGenerator newValFooIndex0 0 0 0 " " " " " " " " " " " "
    initValFooIndex1 :: StdGen -> (Integer, StdGen)
    initValFooIndex1 curGen = (1, curGen)
      where
        blackboard = partialBlackboardFooIndex1

    (newValFooIndex1, tempGen2) = initValFooIndex1 tempGen1

    partialBlackboardFooIndex2 = BTreeBlackboard newSereneGenerator newValFooIndex0 newValFooIndex1 0 0 " " " " " " " " " " " "
    initValFooIndex2 :: StdGen -> (Integer, StdGen)
    initValFooIndex2 curGen = (2, curGen)
      where
        blackboard = partialBlackboardFooIndex2

    (newValFooIndex2, tempGen3) = initValFooIndex2 tempGen2

    partialBlackboardIndexVar = BTreeBlackboard newSereneGenerator newValFooIndex0 newValFooIndex1 newValFooIndex2 0 " " " " " " " " " " " "
    initValIndexVar :: StdGen -> (Integer, StdGen)
    initValIndexVar curGen = (privateRandom0 (fst (getRandomInteger curGen 2)), snd (getRandomInteger curGen 2))
      where
        blackboard = partialBlackboardIndexVar
        privateRandom0 :: Integer -> Integer
        privateRandom0 0 = 0
        privateRandom0 1 = 1
        privateRandom0 _ = 2

    (newValIndexVar, tempGen4) = initValIndexVar tempGen3

    partialBlackboardBarLocation5Index0 = BTreeBlackboard newSereneGenerator newValFooIndex0 newValFooIndex1 newValFooIndex2 newValIndexVar " " " " " " " " " " " "
    localInitValBarLocation5Index0 :: StdGen -> (String, StdGen)
    localInitValBarLocation5Index0 curGen = ("increase", curGen)
      where
        blackboard = partialBlackboardBarLocation5Index0
        nodeLocation = 5

    (localNewValBarLocation5Index0, tempGen5) = localInitValBarLocation5Index0 tempGen4

    partialBlackboardBarLocation5Index1 = BTreeBlackboard newSereneGenerator newValFooIndex0 newValFooIndex1 newValFooIndex2 newValIndexVar localNewValBarLocation5Index0 " " " " " " " " " "
    localInitValBarLocation5Index1 :: StdGen -> (String, StdGen)
    localInitValBarLocation5Index1 curGen = (privateRandom0 (fst (getRandomInteger curGen 1)), snd (getRandomInteger curGen 1))
      where
        blackboard = partialBlackboardBarLocation5Index1
        nodeLocation = 5
        privateRandom0 :: Integer -> String
        privateRandom0 0 = "increase"
        privateRandom0 _ = "decrease"

    (localNewValBarLocation5Index1, tempGen6) = localInitValBarLocation5Index1 tempGen5

    partialBlackboardBarLocation5Index2 = BTreeBlackboard newSereneGenerator newValFooIndex0 newValFooIndex1 newValFooIndex2 newValIndexVar localNewValBarLocation5Index0 localNewValBarLocation5Index1 " " " " " " " "
    localInitValBarLocation5Index2 :: StdGen -> (String, StdGen)
    localInitValBarLocation5Index2 curGen
      | False = (privateRandom0 (fst (getRandomInteger curGen 1)), snd (getRandomInteger curGen 1))
      | otherwise = ("nope", curGen)
      where
        blackboard = partialBlackboardBarLocation5Index2
        nodeLocation = 5
        privateRandom0 :: Integer -> String
        privateRandom0 0 = "increase"
        privateRandom0 _ = "decrease"

    (localNewValBarLocation5Index2, tempGen7) = localInitValBarLocation5Index2 tempGen6

    partialBlackboardBarLocation4Index0 = BTreeBlackboard newSereneGenerator newValFooIndex0 newValFooIndex1 newValFooIndex2 newValIndexVar localNewValBarLocation5Index0 localNewValBarLocation5Index1 localNewValBarLocation5Index2 " " " " " "
    localInitValBarLocation4Index0 :: StdGen -> (String, StdGen)
    localInitValBarLocation4Index0 curGen
      | (0 == 0) = ("increase", curGen)
      | (1 == 0) = ("decrease", curGen)
      | otherwise = ("nope", curGen)
      where
        blackboard = partialBlackboardBarLocation4Index0
        nodeLocation = 4

    (localNewValBarLocation4Index0, tempGen8) = localInitValBarLocation4Index0 tempGen7

    partialBlackboardBarLocation4Index1 = BTreeBlackboard newSereneGenerator newValFooIndex0 newValFooIndex1 newValFooIndex2 newValIndexVar localNewValBarLocation5Index0 localNewValBarLocation5Index1 localNewValBarLocation5Index2 localNewValBarLocation4Index0 " " " "
    localInitValBarLocation4Index1 :: StdGen -> (String, StdGen)
    localInitValBarLocation4Index1 curGen
      | (0 == 1) = ("increase", curGen)
      | (1 == 1) = ("decrease", curGen)
      | otherwise = ("nope", curGen)
      where
        blackboard = partialBlackboardBarLocation4Index1
        nodeLocation = 4

    (localNewValBarLocation4Index1, tempGen9) = localInitValBarLocation4Index1 tempGen8

    partialBlackboardBarLocation4Index2 = BTreeBlackboard newSereneGenerator newValFooIndex0 newValFooIndex1 newValFooIndex2 newValIndexVar localNewValBarLocation5Index0 localNewValBarLocation5Index1 localNewValBarLocation5Index2 localNewValBarLocation4Index0 localNewValBarLocation4Index1 " "
    localInitValBarLocation4Index2 :: StdGen -> (String, StdGen)
    localInitValBarLocation4Index2 curGen
      | (0 == 2) = ("increase", curGen)
      | (1 == 2) = ("decrease", curGen)
      | otherwise = ("nope", curGen)
      where
        blackboard = partialBlackboardBarLocation4Index2
        nodeLocation = 4

    (localNewValBarLocation4Index2, tempGen10) = localInitValBarLocation4Index2 tempGen9


