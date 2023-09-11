module BehaviorTreeBlackboard where
import SereneRandomizer
import System.Random
import SereneOperations

data BTreeBlackboard = BTreeBlackboard {
  sereneBoardGenerator :: StdGen
  , boardBlVAR0Index0 :: Bool
  , boardBlVAR0Index1 :: Bool
  , boardBlVAR0Index2 :: Bool
  , boardBlVAR3 :: Integer
  , boardBlVAR4 :: Integer
  }

fromBTreeBlackboardToString :: BTreeBlackboard -> String
fromBTreeBlackboardToString blackboard = "Board = {" ++ "boardBlVAR0: " ++ "[" ++ show (boardBlVAR0 0 blackboard) ++ ", " ++ show (boardBlVAR0 1 blackboard) ++ ", " ++ show (boardBlVAR0 2 blackboard)++ "]" ++ ", " ++ "boardBlVAR0: " ++ "[" ++ show (boardBlVAR0 0 blackboard) ++ ", " ++ show (boardBlVAR0 1 blackboard) ++ ", " ++ show (boardBlVAR0 2 blackboard)++ "]" ++ ", " ++ "boardBlVAR0: " ++ "[" ++ show (boardBlVAR0 0 blackboard) ++ ", " ++ show (boardBlVAR0 1 blackboard) ++ ", " ++ show (boardBlVAR0 2 blackboard)++ "]" ++ ", " ++ "boardBlVAR3: " ++ show (boardBlVAR3 blackboard) ++ ", " ++ "boardBlVAR4: " ++ show (boardBlVAR4 blackboard) ++ ", " ++ "boardBlDEFINE5: " ++ show (boardBlDEFINE5 blackboard) ++ ", " ++ "boardBlDEFINE6: " ++ "[" ++ show (boardBlDEFINE6 0 blackboard) ++ ", " ++ show (boardBlDEFINE6 1 blackboard) ++ ", " ++ show (boardBlDEFINE6 2 blackboard)++ "]" ++ ", " ++ "localBoardLocalDEFINE7Location2: " ++ show (localBoardLocalDEFINE7 2blackboard) ++ "}"

-- START OF BLACKBOARD FUNCTIONS

boardBlDEFINE5 :: BTreeBlackboard -> Integer
boardBlDEFINE5 blackboard
  | ((boardBlVAR4 blackboard) <= (sereneCOUNT (sereneXNOR (boardBlVAR0 1 blackboard) (boardBlVAR0 2 blackboard)) ((boardBlVAR4 blackboard) > 52))) = (min 5 (max 2 (min (boardBlVAR4 blackboard) (boardBlVAR4 blackboard))))
  | ((True /= (boardBlVAR0 2 blackboard)) /= True) = (min 5 (max 2 (abs (boardBlVAR4 blackboard))))
  | otherwise = (min 5 (max 2 (max (-19) (boardBlVAR4 blackboard))))
boardBlDEFINE6 :: Integer -> BTreeBlackboard -> Bool
boardBlDEFINE6 0 blackboard = ((-34) > (boardBlVAR3 blackboard))
boardBlDEFINE6 1 blackboard
  | (False /= False) = (True == (sereneXOR (boardBlVAR0 2 blackboard) False))
  | ((boardBlVAR0 1 blackboard) && False) = (((sereneCOUNT (False && (boardBlVAR0 0 blackboard)) (sereneIMPLIES True True)) < 97) || (43 <= (boardBlVAR4 blackboard)))
  | otherwise = True
boardBlDEFINE6 2 blackboard
  | True = (boardBlVAR0 0 blackboard)
  | (40 < (boardBlVAR3 blackboard)) = ((boardBlVAR0 0 blackboard) && ((boardBlDEFINE5 blackboard) >= ((-94) + ((boardBlVAR3 blackboard) + ((boardBlDEFINE5 blackboard) + 83)))))
  | otherwise = (boardBlVAR0 2 blackboard)
boardBlDEFINE6 _ _ = error "boardBlDEFINE6 illegal index value"

-- START OF LOCAL BLACKBOARD FUNCTIONS

localBoardLocalDEFINE7 :: Integer -> BTreeBlackboard -> Bool
localBoardLocalDEFINE7 2 blackboard = False
  where nodeLocation = 2
localBoardLocalDEFINE7 _ _ = error "localDEFINE7 illegal local reference"

-- START OF GET FUNCTIONS FOR LOCAL VARIABLES


-- START OF GET FUNCTIONS FOR ARRAYS

boardBlVAR0 :: Integer -> BTreeBlackboard -> Bool
boardBlVAR0 0 = boardBlVAR0Index0
boardBlVAR0 1 = boardBlVAR0Index1
boardBlVAR0 2 = boardBlVAR0Index2
boardBlVAR0 _ = error "boardBlVAR0 illegal index value"

-- START OF TYPE CHECKING FUNCTIONS

checkValueBoardBlVAR0 :: Bool -> Bool
checkValueBoardBlVAR0 value = value

checkValueLocalBoardLocalVAR2 :: Integer -> Integer
checkValueLocalBoardLocalVAR2 value
  | (-5) > value || value > (-2) = error "localBoardLocalVAR2 illegal value"
  | otherwise = value

checkValueBoardBlVAR3 :: Integer -> Integer
checkValueBoardBlVAR3 value
  | 2 > value || value > 5 = error "boardBlVAR3 illegal value"
  | otherwise = value

checkValueBoardBlVAR4 :: Integer -> Integer
checkValueBoardBlVAR4 value
  | 2 > value || value > 5 = error "boardBlVAR4 illegal value"
  | otherwise = value


-- START OF SET FUNCTIONS

updateBoardGenerator :: BTreeBlackboard -> StdGen -> BTreeBlackboard
updateBoardGenerator blackboard newGen = blackboard { sereneBoardGenerator = newGen }
updateBoardBlVAR0Index0 :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateBoardBlVAR0Index0 blackboard value = blackboard { boardBlVAR0Index0 = (checkValueBoardBlVAR0 value)}
updateBoardBlVAR0Index1 :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateBoardBlVAR0Index1 blackboard value = blackboard { boardBlVAR0Index1 = (checkValueBoardBlVAR0 value)}
updateBoardBlVAR0Index2 :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateBoardBlVAR0Index2 blackboard value = blackboard { boardBlVAR0Index2 = (checkValueBoardBlVAR0 value)}
updateBoardBlVAR3 :: BTreeBlackboard -> Integer -> BTreeBlackboard
updateBoardBlVAR3 blackboard value = blackboard { boardBlVAR3 = (checkValueBoardBlVAR3 value)}
updateBoardBlVAR4 :: BTreeBlackboard -> Integer -> BTreeBlackboard
updateBoardBlVAR4 blackboard value = blackboard { boardBlVAR4 = (checkValueBoardBlVAR4 value)}

-- START OF SET FUNCTIONS FOR ARRAYS

updateBoardBlVAR0 :: Integer -> BTreeBlackboard -> Bool -> BTreeBlackboard
updateBoardBlVAR0 0 = updateBoardBlVAR0Index0
updateBoardBlVAR0 1 = updateBoardBlVAR0Index1
updateBoardBlVAR0 2 = updateBoardBlVAR0Index2
updateBoardBlVAR0 _ = error "BoardBlVAR0 illegal index value"
arrayUpdateBoardBlVAR0 :: BTreeBlackboard -> [(Integer, Bool)] -> BTreeBlackboard
arrayUpdateBoardBlVAR0 blackboard []  = blackboard
arrayUpdateBoardBlVAR0 blackboard [(index, value)] = updateBoardBlVAR0 index blackboard value
arrayUpdateBoardBlVAR0 blackboard indicesValues = blackboard {
  boardBlVAR0Index0 = newBlVAR0Index0
  , boardBlVAR0Index1 = newBlVAR0Index1
  , boardBlVAR0Index2 = newBlVAR0Index2
  }
    where
      (newBlVAR0Index0, newBlVAR0Index1, newBlVAR0Index2) = updateValues indicesValues
      updateValues :: [(Integer, Bool)] -> (Bool, Bool, Bool)
      updateValues [] = (boardBlVAR0Index0 blackboard, boardBlVAR0Index1 blackboard, boardBlVAR0Index2 blackboard)
      updateValues ((0, currentValue) : nextIndicesValues) = (checkValueBoardBlVAR0 currentValue, updatedValue1, updatedValue2)
        where
          (_, updatedValue1, updatedValue2) = updateValues nextIndicesValues
      updateValues ((1, currentValue) : nextIndicesValues) = (updatedValue0, checkValueBoardBlVAR0 currentValue, updatedValue2)
        where
          (updatedValue0, _, updatedValue2) = updateValues nextIndicesValues
      updateValues ((2, currentValue) : nextIndicesValues) = (updatedValue0, updatedValue1, checkValueBoardBlVAR0 currentValue)
        where
          (updatedValue0, updatedValue1, _) = updateValues nextIndicesValues

-- START OF INITIAL BLACKBOARD VALUE

initialBlackboard :: Integer -> BTreeBlackboard
initialBlackboard seed = BTreeBlackboard newSereneGenerator newValBlVAR0Index0 newValBlVAR0Index1 newValBlVAR0Index2 newValBlVAR3 newValBlVAR4  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen5
    partialBlackboardBlVAR0Index0 = BTreeBlackboard newSereneGenerator True True True 0 0
    initValBlVAR0Index0 :: StdGen -> (Bool, StdGen)
    initValBlVAR0Index0 curGen
      | (sereneXNOR True True) = ((False && True), curGen)
      | otherwise = ((5 <= (abs (-27))), curGen)
      where
        blackboard = partialBlackboardBlVAR0Index0

    (newValBlVAR0Index0, tempGen1) = initValBlVAR0Index0 tempGen0

    partialBlackboardBlVAR0Index1 = BTreeBlackboard newSereneGenerator newValBlVAR0Index0 True True 0 0
    initValBlVAR0Index1 :: StdGen -> (Bool, StdGen)
    initValBlVAR0Index1 curGen = ((4 < ((sereneCOUNT (False || False) (sereneXNOR True False)) + (sereneCOUNT (4 > (-79)) (86 > 5)))), curGen)
      where
        blackboard = partialBlackboardBlVAR0Index1

    (newValBlVAR0Index1, tempGen2) = initValBlVAR0Index1 tempGen1

    partialBlackboardBlVAR0Index2 = BTreeBlackboard newSereneGenerator newValBlVAR0Index0 newValBlVAR0Index1 True 0 0
    initValBlVAR0Index2 :: StdGen -> (Bool, StdGen)
    initValBlVAR0Index2 curGen = (((-7) <= (-50)), curGen)
      where
        blackboard = partialBlackboardBlVAR0Index2

    (newValBlVAR0Index2, tempGen3) = initValBlVAR0Index2 tempGen2

    partialBlackboardBlVAR3 = BTreeBlackboard newSereneGenerator newValBlVAR0Index0 newValBlVAR0Index1 newValBlVAR0Index2 0 0
    initValBlVAR3 :: StdGen -> (Integer, StdGen)
    initValBlVAR3 curGen = ((min 5 (max 2 5)), curGen)
      where
        blackboard = partialBlackboardBlVAR3

    (newValBlVAR3, tempGen4) = initValBlVAR3 tempGen3

    partialBlackboardBlVAR4 = BTreeBlackboard newSereneGenerator newValBlVAR0Index0 newValBlVAR0Index1 newValBlVAR0Index2 newValBlVAR3 0
    initValBlVAR4 :: StdGen -> (Integer, StdGen)
    initValBlVAR4 curGen
      | ((newValBlVAR3 + (newValBlVAR3 + (42 + 22))) <= (min 74 newValBlVAR3)) = ((min 5 (max 2 newValBlVAR3)), curGen)
      | otherwise = ((min 5 (max 2 48)), curGen)
      where
        blackboard = partialBlackboardBlVAR4

    (newValBlVAR4, tempGen5) = initValBlVAR4 tempGen4


