module BehaviorTreeBlackboard where
import SereneRandomizer
import System.Random
import SereneOperations

data BTreeBlackboard = BTreeBlackboard {
  sereneBoardGenerator :: StdGen
  , boardBlVAR0Index0 :: Integer
  , boardBlVAR0Index1 :: Integer
  , boardBlVAR2Index0 :: Integer
  , boardBlVAR2Index1 :: Integer
  , boardBlVAR2Index2 :: Integer
  }

fromBTreeBlackboardToString :: BTreeBlackboard -> String
fromBTreeBlackboardToString blackboard = "Board = {" ++ "boardBlVAR0: " ++ "[" ++ show (boardBlVAR0 0 blackboard) ++ ", " ++ show (boardBlVAR0 1 blackboard)++ "]" ++ ", " ++ "boardBlVAR0: " ++ "[" ++ show (boardBlVAR0 0 blackboard) ++ ", " ++ show (boardBlVAR0 1 blackboard)++ "]" ++ ", " ++ "boardBlVAR2: " ++ "[" ++ show (boardBlVAR2 0 blackboard) ++ ", " ++ show (boardBlVAR2 1 blackboard) ++ ", " ++ show (boardBlVAR2 2 blackboard)++ "]" ++ ", " ++ "boardBlVAR2: " ++ "[" ++ show (boardBlVAR2 0 blackboard) ++ ", " ++ show (boardBlVAR2 1 blackboard) ++ ", " ++ show (boardBlVAR2 2 blackboard)++ "]" ++ ", " ++ "boardBlVAR2: " ++ "[" ++ show (boardBlVAR2 0 blackboard) ++ ", " ++ show (boardBlVAR2 1 blackboard) ++ ", " ++ show (boardBlVAR2 2 blackboard)++ "]" ++ ", " ++ "boardBlDEFINE4: " ++ show (boardBlDEFINE4 blackboard) ++ ", " ++ "boardBlDEFINE7: " ++ "[" ++ show (boardBlDEFINE7 0 blackboard) ++ ", " ++ show (boardBlDEFINE7 1 blackboard) ++ ", " ++ show (boardBlDEFINE7 2 blackboard)++ "]" ++ "}"

-- START OF BLACKBOARD FUNCTIONS

boardBlDEFINE4 :: BTreeBlackboard -> Bool
boardBlDEFINE4 blackboard
  | ((False || True) || True) = (sereneXNOR False True)
  | False = False
  | otherwise = False
boardBlDEFINE7 :: Integer -> BTreeBlackboard -> Integer
boardBlDEFINE7 0 blackboard
  | ("yes" /= "yes") = (min 5 (max 2 (((boardBlVAR2 1 blackboard) + (((boardBlVAR0 0 blackboard) * ((boardBlVAR0 1 blackboard) * 57)) + ((86 + ((boardBlVAR0 0 blackboard) + (boardBlVAR0 1 blackboard))) + (86 - (boardBlVAR2 1 blackboard))))) - (min (boardBlVAR0 1 blackboard) (max (boardBlVAR0 0 blackboard) 90)))))
  | otherwise = (min 5 (max 2 52))
boardBlDEFINE7 1 blackboard = (min 5 (max 2 ((-78) * ((boardBlVAR0 0 blackboard) * ((-69) * 92)))))
boardBlDEFINE7 2 blackboard
  | ((min (-3) 53) >= (-68)) = (min 5 (max 2 39))
  | False = (min 5 (max 2 (min (- (min (boardBlVAR0 0 blackboard) (boardBlVAR2 1 blackboard))) 47)))
  | otherwise = (min 5 (max 2 ((- (boardBlVAR2 0 blackboard)) - ((boardBlVAR0 0 blackboard) - (boardBlVAR2 2 blackboard)))))
boardBlDEFINE7 _ _ = error "boardBlDEFINE7 illegal index value"

-- START OF LOCAL BLACKBOARD FUNCTIONS


-- START OF GET FUNCTIONS FOR LOCAL VARIABLES


-- START OF GET FUNCTIONS FOR ARRAYS

boardBlVAR0 :: Integer -> BTreeBlackboard -> Integer
boardBlVAR0 0 = boardBlVAR0Index0
boardBlVAR0 1 = boardBlVAR0Index1
boardBlVAR0 _ = error "boardBlVAR0 illegal index value"
boardBlVAR2 :: Integer -> BTreeBlackboard -> Integer
boardBlVAR2 0 = boardBlVAR2Index0
boardBlVAR2 1 = boardBlVAR2Index1
boardBlVAR2 2 = boardBlVAR2Index2
boardBlVAR2 _ = error "boardBlVAR2 illegal index value"

-- START OF TYPE CHECKING FUNCTIONS

checkValueBoardBlVAR0 :: Integer -> Integer
checkValueBoardBlVAR0 value
  | (-5) > value || value > (-2) = error "boardBlVAR0 illegal value"
  | otherwise = value

checkValueBoardBlVAR2 :: Integer -> Integer
checkValueBoardBlVAR2 value
  | 2 > value || value > 5 = error "boardBlVAR2 illegal value"
  | otherwise = value


-- START OF SET FUNCTIONS

updateBoardGenerator :: BTreeBlackboard -> StdGen -> BTreeBlackboard
updateBoardGenerator blackboard newGen = blackboard { sereneBoardGenerator = newGen }
updateBoardBlVAR0Index0 :: BTreeBlackboard -> Integer -> BTreeBlackboard
updateBoardBlVAR0Index0 blackboard value = blackboard { boardBlVAR0Index0 = (checkValueBoardBlVAR0 value)}
updateBoardBlVAR0Index1 :: BTreeBlackboard -> Integer -> BTreeBlackboard
updateBoardBlVAR0Index1 blackboard value = blackboard { boardBlVAR0Index1 = (checkValueBoardBlVAR0 value)}
updateBoardBlVAR2Index0 :: BTreeBlackboard -> Integer -> BTreeBlackboard
updateBoardBlVAR2Index0 blackboard value = blackboard { boardBlVAR2Index0 = (checkValueBoardBlVAR2 value)}
updateBoardBlVAR2Index1 :: BTreeBlackboard -> Integer -> BTreeBlackboard
updateBoardBlVAR2Index1 blackboard value = blackboard { boardBlVAR2Index1 = (checkValueBoardBlVAR2 value)}
updateBoardBlVAR2Index2 :: BTreeBlackboard -> Integer -> BTreeBlackboard
updateBoardBlVAR2Index2 blackboard value = blackboard { boardBlVAR2Index2 = (checkValueBoardBlVAR2 value)}

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
updateBoardBlVAR2 :: Integer -> BTreeBlackboard -> Integer -> BTreeBlackboard
updateBoardBlVAR2 0 = updateBoardBlVAR2Index0
updateBoardBlVAR2 1 = updateBoardBlVAR2Index1
updateBoardBlVAR2 2 = updateBoardBlVAR2Index2
updateBoardBlVAR2 _ = error "BoardBlVAR2 illegal index value"
arrayUpdateBoardBlVAR2 :: BTreeBlackboard -> [(Integer, Integer)] -> BTreeBlackboard
arrayUpdateBoardBlVAR2 blackboard []  = blackboard
arrayUpdateBoardBlVAR2 blackboard [(index, value)] = updateBoardBlVAR2 index blackboard value
arrayUpdateBoardBlVAR2 blackboard indicesValues = blackboard {
  boardBlVAR2Index0 = newBlVAR2Index0
  , boardBlVAR2Index1 = newBlVAR2Index1
  , boardBlVAR2Index2 = newBlVAR2Index2
  }
    where
      (newBlVAR2Index0, newBlVAR2Index1, newBlVAR2Index2) = updateValues indicesValues
      updateValues :: [(Integer, Integer)] -> (Integer, Integer, Integer)
      updateValues [] = (boardBlVAR2Index0 blackboard, boardBlVAR2Index1 blackboard, boardBlVAR2Index2 blackboard)
      updateValues ((0, currentValue) : nextIndicesValues) = (checkValueBoardBlVAR2 currentValue, updatedValue1, updatedValue2)
        where
          (_, updatedValue1, updatedValue2) = updateValues nextIndicesValues
      updateValues ((1, currentValue) : nextIndicesValues) = (updatedValue0, checkValueBoardBlVAR2 currentValue, updatedValue2)
        where
          (updatedValue0, _, updatedValue2) = updateValues nextIndicesValues
      updateValues ((2, currentValue) : nextIndicesValues) = (updatedValue0, updatedValue1, checkValueBoardBlVAR2 currentValue)
        where
          (updatedValue0, updatedValue1, _) = updateValues nextIndicesValues

-- START OF INITIAL BLACKBOARD VALUE

initialBlackboard :: Integer -> BTreeBlackboard
initialBlackboard seed = BTreeBlackboard newSereneGenerator newValBlVAR0Index0 newValBlVAR0Index1 newValBlVAR2Index0 newValBlVAR2Index1 newValBlVAR2Index2  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen5
    partialBlackboardBlVAR0Index0 = BTreeBlackboard newSereneGenerator 0 0 0 0 0
    initValBlVAR0Index0 :: StdGen -> (Integer, StdGen)
    initValBlVAR0Index0 curGen
      | (True == True) = ((min (-2) (max (-5) (abs 40))), curGen)
      | (sereneXOR True ((-74) /= (-2))) = ((min (-2) (max (-5) (-3))), curGen)
      | otherwise = ((min (-2) (max (-5) ((sereneCOUNT ((-59) < (-79)) (False == (sereneXNOR True True))) + (sereneCOUNT False (sereneXOR True False))))), curGen)
      where
        blackboard = partialBlackboardBlVAR0Index0

    (newValBlVAR0Index0, tempGen1) = initValBlVAR0Index0 tempGen0

    partialBlackboardBlVAR0Index1 = BTreeBlackboard newSereneGenerator newValBlVAR0Index0 0 0 0 0
    initValBlVAR0Index1 :: StdGen -> (Integer, StdGen)
    initValBlVAR0Index1 curGen
      | True = ((min (-2) (max (-5) (-66))), curGen)
      | (2 > (-77)) = ((min (-2) (max (-5) (-34))), curGen)
      | otherwise = ((min (-2) (max (-5) ((sereneCOUNT (False == False) (True && True)) + (sereneCOUNT False (True || False))))), curGen)
      where
        blackboard = partialBlackboardBlVAR0Index1

    (newValBlVAR0Index1, tempGen2) = initValBlVAR0Index1 tempGen1

    partialBlackboardBlVAR2Index0 = BTreeBlackboard newSereneGenerator newValBlVAR0Index0 newValBlVAR0Index1 0 0 0
    initValBlVAR2Index0 :: StdGen -> (Integer, StdGen)
    initValBlVAR2Index0 curGen
      | True = ((min 5 (max 2 ((max (boardBlVAR0 1 blackboard) 21) - ((boardBlVAR0 0 blackboard) + ((boardBlVAR0 1 blackboard) + (72 + 90)))))), curGen)
      | (sereneIMPLIES (sereneIMPLIES True ((boardBlVAR0 1 blackboard) == (boardBlVAR0 1 blackboard))) (sereneXNOR True True)) = ((min 5 (max 2 ((boardBlVAR0 0 blackboard) + 27))), curGen)
      | otherwise = ((min 5 (max 2 (abs ((sereneCOUNT ((boardBlVAR0 1 blackboard) == 72) (32 <= (boardBlVAR0 1 blackboard))) + (sereneCOUNT ("yes" == "no") (sereneXNOR (sereneIMPLIES False True) ("both" == "both"))))))), curGen)
      where
        blackboard = partialBlackboardBlVAR2Index0

    (newValBlVAR2Index0, tempGen3) = initValBlVAR2Index0 tempGen2

    partialBlackboardBlVAR2Index1 = BTreeBlackboard newSereneGenerator newValBlVAR0Index0 newValBlVAR0Index1 newValBlVAR2Index0 0 0
    initValBlVAR2Index1 :: StdGen -> (Integer, StdGen)
    initValBlVAR2Index1 curGen = ((min 5 (max 2 (boardBlVAR0 0 blackboard))), curGen)
      where
        blackboard = partialBlackboardBlVAR2Index1

    (newValBlVAR2Index1, tempGen4) = initValBlVAR2Index1 tempGen3

    partialBlackboardBlVAR2Index2 = BTreeBlackboard newSereneGenerator newValBlVAR0Index0 newValBlVAR0Index1 newValBlVAR2Index0 newValBlVAR2Index1 0
    initValBlVAR2Index2 :: StdGen -> (Integer, StdGen)
    initValBlVAR2Index2 curGen
      | (sereneXNOR True False) = ((min 5 (max 2 (boardBlVAR0 0 blackboard))), curGen)
      | otherwise = ((min 5 (max 2 ((min (boardBlVAR0 1 blackboard) 94) * ((-98) * (((sereneCOUNT ((boardBlVAR0 0 blackboard) > (boardBlVAR0 0 blackboard)) (False && False)) + (sereneCOUNT False ((boardBlVAR0 0 blackboard) >= (-57)))) * (boardBlVAR0 0 blackboard)))))), curGen)
      where
        blackboard = partialBlackboardBlVAR2Index2

    (newValBlVAR2Index2, tempGen5) = initValBlVAR2Index2 tempGen4


