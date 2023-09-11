module BehaviorTreeBlackboard where
import SereneRandomizer
import System.Random
import SereneOperations

data BTreeBlackboard = BTreeBlackboard {
  sereneBoardGenerator :: StdGen
  , boardBlVAR0Index0 :: Integer
  , boardBlVAR0Index1 :: Integer
  , boardBlVAR2 :: Integer
  }

fromBTreeBlackboardToString :: BTreeBlackboard -> String
fromBTreeBlackboardToString blackboard = "Board = {" ++ "boardBlVAR0: " ++ "[" ++ show (boardBlVAR0 0 blackboard) ++ ", " ++ show (boardBlVAR0 1 blackboard)++ "]" ++ ", " ++ "boardBlVAR0: " ++ "[" ++ show (boardBlVAR0 0 blackboard) ++ ", " ++ show (boardBlVAR0 1 blackboard)++ "]" ++ ", " ++ "boardBlVAR2: " ++ show (boardBlVAR2 blackboard) ++ ", " ++ "boardBlDEFINE4: " ++ show (boardBlDEFINE4 blackboard) ++ "}"

-- START OF BLACKBOARD FUNCTIONS

boardBlDEFINE4 :: BTreeBlackboard -> Integer
boardBlDEFINE4 blackboard
  | True = (min 5 (max 2 (min 100 (max (-100) (- 99)))))
  | otherwise = (min 5 (max 2 (-36)))

-- START OF LOCAL BLACKBOARD FUNCTIONS


-- START OF GET FUNCTIONS FOR LOCAL VARIABLES


-- START OF GET FUNCTIONS FOR ARRAYS

boardBlVAR0 :: Integer -> BTreeBlackboard -> Integer
boardBlVAR0 0 = boardBlVAR0Index0
boardBlVAR0 1 = boardBlVAR0Index1
boardBlVAR0 _ = error "boardBlVAR0 illegal index value"

-- START OF TYPE CHECKING FUNCTIONS

checkValueBoardBlVAR0 :: Integer -> Integer
checkValueBoardBlVAR0 value
  | 2 > value || value > 5 = error "boardBlVAR0 illegal value"
  | otherwise = value

checkValueBoardBlVAR2 :: Integer -> Integer
checkValueBoardBlVAR2 value
  | (-5) > value || value > (-2) = error "boardBlVAR2 illegal value"
  | otherwise = value


-- START OF SET FUNCTIONS

updateBoardGenerator :: BTreeBlackboard -> StdGen -> BTreeBlackboard
updateBoardGenerator blackboard newGen = blackboard { sereneBoardGenerator = newGen }
updateBoardBlVAR0Index0 :: BTreeBlackboard -> Integer -> BTreeBlackboard
updateBoardBlVAR0Index0 blackboard value = blackboard { boardBlVAR0Index0 = (checkValueBoardBlVAR0 value)}
updateBoardBlVAR0Index1 :: BTreeBlackboard -> Integer -> BTreeBlackboard
updateBoardBlVAR0Index1 blackboard value = blackboard { boardBlVAR0Index1 = (checkValueBoardBlVAR0 value)}
updateBoardBlVAR2 :: BTreeBlackboard -> Integer -> BTreeBlackboard
updateBoardBlVAR2 blackboard value = blackboard { boardBlVAR2 = (checkValueBoardBlVAR2 value)}

-- START OF SET FUNCTIONS FOR ARRAYS

updateBoardBlVAR0 :: Integer -> BTreeBlackboard -> Integer -> BTreeBlackboard
updateBoardBlVAR0 0 = updateBoardBlVAR0Index0
updateBoardBlVAR0 1 = updateBoardBlVAR0Index1
updateBoardBlVAR0 _ = error "BoardBlVAR0 illegal index value"
arrayUpdateBoardBlVAR0 :: BTreeBlackboard -> [(Integer, Integer)] -> BTreeBlackboard
arrayUpdateBoardBlVAR0 blackboard []  = blackboard
arrayUpdateBoardBlVAR0 blackboard [(index, value)] = updateBoardBlVAR0 index blackboard value
arrayUpdateBoardBlVAR0 blackboard indicesValues = blackboard {
  boardBlVAR0Index0 = newBlVAR0Index0
  , boardBlVAR0Index1 = newBlVAR0Index1
  }
    where
      (newBlVAR0Index0, newBlVAR0Index1) = updateValues indicesValues
      updateValues :: [(Integer, Integer)] -> (Integer, Integer)
      updateValues [] = (boardBlVAR0Index0 blackboard, boardBlVAR0Index1 blackboard)
      updateValues ((0, currentValue) : nextIndicesValues) = (checkValueBoardBlVAR0 currentValue, updatedValue1)
        where
          (_, updatedValue1) = updateValues nextIndicesValues
      updateValues ((1, currentValue) : nextIndicesValues) = (updatedValue0, checkValueBoardBlVAR0 currentValue)
        where
          (updatedValue0, _) = updateValues nextIndicesValues

-- START OF INITIAL BLACKBOARD VALUE

initialBlackboard :: Integer -> BTreeBlackboard
initialBlackboard seed = BTreeBlackboard newSereneGenerator newValBlVAR0Index0 newValBlVAR0Index1 newValBlVAR2  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen3
    partialBlackboardBlVAR0Index0 = BTreeBlackboard newSereneGenerator 0 0 0
    initValBlVAR0Index0 :: StdGen -> (Integer, StdGen)
    initValBlVAR0Index0 curGen = ((min 5 (max 2 (min 100 (max (-100) ((min 100 (max (-100) (- (-12)))) * ((min 100 (max (-100) (- (min 100 (max (-100) (- 2)))))) * ((-3) * (min 100 (max (-100) (abs 4)))))))))), curGen)
      where
        blackboard = partialBlackboardBlVAR0Index0

    (newValBlVAR0Index0, tempGen1) = initValBlVAR0Index0 tempGen0

    partialBlackboardBlVAR0Index1 = BTreeBlackboard newSereneGenerator newValBlVAR0Index0 0 0
    initValBlVAR0Index1 :: StdGen -> (Integer, StdGen)
    initValBlVAR0Index1 curGen = ((min 5 (max 2 (min 100 (max (-100) ((min 100 (max (-100) (- (-12)))) * ((min 100 (max (-100) (- (min 100 (max (-100) (- 2)))))) * ((-3) * (min 100 (max (-100) (abs 4)))))))))), curGen)
      where
        blackboard = partialBlackboardBlVAR0Index1

    (newValBlVAR0Index1, tempGen2) = initValBlVAR0Index1 tempGen1

    partialBlackboardBlVAR2 = BTreeBlackboard newSereneGenerator newValBlVAR0Index0 newValBlVAR0Index1 0
    initValBlVAR2 :: StdGen -> (Integer, StdGen)
    initValBlVAR2 curGen
      | ((boardBlVAR0 0 blackboard) > (-29)) = ((min (-2) (max (-5) (min 100 (max (-100) (- (min 100 (max (-100) ((boardBlVAR0 1 blackboard) * ((min 100 (max (-100) (max (boardBlVAR0 1 blackboard) (boardBlVAR0 1 blackboard)))) * ((-24) * (boardBlVAR0 0 blackboard))))))))))), curGen)
      | otherwise = ((min (-2) (max (-5) (min 100 (max (-100) ((boardBlVAR0 0 blackboard) * ((min 100 (max (-100) ((boardBlVAR0 1 blackboard) * ((-86) * (-89))))) * ((boardBlVAR0 0 blackboard) * (boardBlVAR0 1 blackboard)))))))), curGen)
      where
        blackboard = partialBlackboardBlVAR2

    (newValBlVAR2, tempGen3) = initValBlVAR2 tempGen2


