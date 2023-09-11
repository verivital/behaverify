module BehaviorTreeBlackboard where
import SereneRandomizer
import System.Random
import SereneOperations

data BTreeBlackboard = BTreeBlackboard {
  sereneBoardGenerator :: StdGen
  , boardBlVAR0Index0 :: Integer
  , boardBlVAR0Index1 :: Integer
  , boardBlVAR0Index2 :: Integer
  , boardBlVAR3 :: Bool
  , localBoardLocalFROZENVAR5Location0Index0 :: String
  , localBoardLocalFROZENVAR5Location0Index1 :: String
  , localBoardLocalVAR4Location0 :: Bool
  , localBoardLocalFROZENVAR6Location0 :: Bool
  }

fromBTreeBlackboardToString :: BTreeBlackboard -> String
fromBTreeBlackboardToString blackboard = "Board = {" ++ "boardBlVAR0: " ++ "[" ++ show (boardBlVAR0 0 blackboard) ++ ", " ++ show (boardBlVAR0 1 blackboard) ++ ", " ++ show (boardBlVAR0 2 blackboard)++ "]" ++ ", " ++ "boardBlVAR0: " ++ "[" ++ show (boardBlVAR0 0 blackboard) ++ ", " ++ show (boardBlVAR0 1 blackboard) ++ ", " ++ show (boardBlVAR0 2 blackboard)++ "]" ++ ", " ++ "boardBlVAR0: " ++ "[" ++ show (boardBlVAR0 0 blackboard) ++ ", " ++ show (boardBlVAR0 1 blackboard) ++ ", " ++ show (boardBlVAR0 2 blackboard)++ "]" ++ ", " ++ "boardBlVAR3: " ++ show (boardBlVAR3 blackboard) ++ ", " ++ "localBoardLocalFROZENVAR5Location0: " ++ "[" ++ show (localBoardLocalFROZENVAR5 0 0 blackboard) ++ ", " ++ show (localBoardLocalFROZENVAR5 0 1 blackboard)++ "]" ++ ", " ++ "localBoardLocalVAR4Location0: " ++ show (localBoardLocalVAR4 0blackboard) ++ ", " ++ "localBoardLocalFROZENVAR6Location0: " ++ show (localBoardLocalFROZENVAR6 0blackboard) ++ "}"

-- START OF BLACKBOARD FUNCTIONS


-- START OF LOCAL BLACKBOARD FUNCTIONS


-- START OF GET FUNCTIONS FOR LOCAL VARIABLES

localBoardLocalVAR4 :: Integer -> BTreeBlackboard -> Bool
localBoardLocalVAR4 0 = localBoardLocalVAR4Location0
localBoardLocalVAR4 _ = error "localVAR4 illegal local reference"
localBoardLocalFROZENVAR5 :: Integer -> Integer -> BTreeBlackboard -> String
localBoardLocalFROZENVAR5 0 = localBoardLocalFROZENVAR5Location0
localBoardLocalFROZENVAR5 _ = error "localFROZENVAR5 illegal local reference"
localBoardLocalFROZENVAR6 :: Integer -> BTreeBlackboard -> Bool
localBoardLocalFROZENVAR6 0 = localBoardLocalFROZENVAR6Location0
localBoardLocalFROZENVAR6 _ = error "localFROZENVAR6 illegal local reference"

-- START OF GET FUNCTIONS FOR ARRAYS

boardBlVAR0 :: Integer -> BTreeBlackboard -> Integer
boardBlVAR0 0 = boardBlVAR0Index0
boardBlVAR0 1 = boardBlVAR0Index1
boardBlVAR0 2 = boardBlVAR0Index2
boardBlVAR0 _ = error "boardBlVAR0 illegal index value"
localBoardLocalFROZENVAR5Location0 :: Integer -> BTreeBlackboard -> String
localBoardLocalFROZENVAR5Location0 0 = localBoardLocalFROZENVAR5Location0Index0
localBoardLocalFROZENVAR5Location0 1 = localBoardLocalFROZENVAR5Location0Index1
localBoardLocalFROZENVAR50 _ = error "localBoardLocalFROZENVAR50 illegal index value"

-- START OF TYPE CHECKING FUNCTIONS

checkValueBoardBlVAR0 :: Integer -> Integer
checkValueBoardBlVAR0 value
  | (-5) > value || value > (-2) = error "boardBlVAR0 illegal value"
  | otherwise = value

checkValueLocalBoardLocalVAR2 :: Integer -> Integer
checkValueLocalBoardLocalVAR2 value
  | (-5) > value || value > (-2) = error "localBoardLocalVAR2 illegal value"
  | otherwise = value

checkValueBoardBlVAR3 :: Bool -> Bool
checkValueBoardBlVAR3 value = value

checkValueLocalBoardLocalVAR4 :: Bool -> Bool
checkValueLocalBoardLocalVAR4 value = value


-- START OF SET FUNCTIONS

updateBoardGenerator :: BTreeBlackboard -> StdGen -> BTreeBlackboard
updateBoardGenerator blackboard newGen = blackboard { sereneBoardGenerator = newGen }
updateLocalBoardLocalVAR4 :: Integer -> BTreeBlackboard -> Bool -> BTreeBlackboard
updateLocalBoardLocalVAR4 0 = updateLocalBoardLocalVAR4Location0
updateLocalBoardLocalVAR4 _ = error "localBoardLocalVAR4 illegal local reference"
updateBoardBlVAR0Index0 :: BTreeBlackboard -> Integer -> BTreeBlackboard
updateBoardBlVAR0Index0 blackboard value = blackboard { boardBlVAR0Index0 = (checkValueBoardBlVAR0 value)}
updateBoardBlVAR0Index1 :: BTreeBlackboard -> Integer -> BTreeBlackboard
updateBoardBlVAR0Index1 blackboard value = blackboard { boardBlVAR0Index1 = (checkValueBoardBlVAR0 value)}
updateBoardBlVAR0Index2 :: BTreeBlackboard -> Integer -> BTreeBlackboard
updateBoardBlVAR0Index2 blackboard value = blackboard { boardBlVAR0Index2 = (checkValueBoardBlVAR0 value)}
updateBoardBlVAR3 :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateBoardBlVAR3 blackboard value = blackboard { boardBlVAR3 = (checkValueBoardBlVAR3 value)}
updateLocalBoardLocalVAR4Location0 :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateLocalBoardLocalVAR4Location0 blackboard value = blackboard { localBoardLocalVAR4Location0 = (checkValueLocalBoardLocalVAR4 value)}

-- START OF SET FUNCTIONS FOR ARRAYS

updateBoardBlVAR0 :: Integer -> BTreeBlackboard -> Integer -> BTreeBlackboard
updateBoardBlVAR0 0 = updateBoardBlVAR0Index0
updateBoardBlVAR0 1 = updateBoardBlVAR0Index1
updateBoardBlVAR0 2 = updateBoardBlVAR0Index2
updateBoardBlVAR0 _ = error "BoardBlVAR0 illegal index value"
arrayUpdateBoardBlVAR0 :: BTreeBlackboard -> [(Integer, Integer)] -> BTreeBlackboard
arrayUpdateBoardBlVAR0 blackboard []  = blackboard
arrayUpdateBoardBlVAR0 blackboard [(index, value)] = updateBoardBlVAR0 index blackboard value
arrayUpdateBoardBlVAR0 blackboard indicesValues = blackboard {
  boardBlVAR0Index0 = newBlVAR0Index0
  , boardBlVAR0Index1 = newBlVAR0Index1
  , boardBlVAR0Index2 = newBlVAR0Index2
  }
    where
      (newBlVAR0Index0, newBlVAR0Index1, newBlVAR0Index2) = updateValues indicesValues
      updateValues :: [(Integer, Integer)] -> (Integer, Integer, Integer)
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
initialBlackboard seed = BTreeBlackboard newSereneGenerator newValBlVAR0Index0 newValBlVAR0Index1 newValBlVAR0Index2 newValBlVAR3 localNewValLocalFROZENVAR5Location0Index0 localNewValLocalFROZENVAR5Location0Index1 localNewValLocalVAR4Location0 localNewValLocalFROZENVAR6Location0  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen8
    partialBlackboardBlVAR0Index0 = BTreeBlackboard newSereneGenerator 0 0 0 True " " " " True True
    initValBlVAR0Index0 :: StdGen -> (Integer, StdGen)
    initValBlVAR0Index0 curGen
      | (sereneIMPLIES (72 >= (-3)) True) = ((min (-2) (max (-5) (max (max (-69) 5) 3))), curGen)
      | (False /= True) = ((min (-2) (max (-5) (37 - (2 - (-77))))), curGen)
      | otherwise = ((min (-2) (max (-5) (- ((-2) - (-2))))), curGen)
      where
        blackboard = partialBlackboardBlVAR0Index0

    (newValBlVAR0Index0, tempGen1) = initValBlVAR0Index0 tempGen0

    partialBlackboardBlVAR0Index1 = BTreeBlackboard newSereneGenerator newValBlVAR0Index0 0 0 True " " " " True True
    initValBlVAR0Index1 :: StdGen -> (Integer, StdGen)
    initValBlVAR0Index1 curGen
      | (sereneIMPLIES (72 >= (-3)) True) = ((min (-2) (max (-5) (max (max (-69) 5) 3))), curGen)
      | (False /= True) = ((min (-2) (max (-5) (37 - (2 - (-77))))), curGen)
      | otherwise = ((min (-2) (max (-5) (- ((-2) - (-2))))), curGen)
      where
        blackboard = partialBlackboardBlVAR0Index1

    (newValBlVAR0Index1, tempGen2) = initValBlVAR0Index1 tempGen1

    partialBlackboardBlVAR0Index2 = BTreeBlackboard newSereneGenerator newValBlVAR0Index0 newValBlVAR0Index1 0 True " " " " True True
    initValBlVAR0Index2 :: StdGen -> (Integer, StdGen)
    initValBlVAR0Index2 curGen
      | (sereneIMPLIES (72 >= (-3)) True) = ((min (-2) (max (-5) (max (max (-69) 5) 3))), curGen)
      | (False /= True) = ((min (-2) (max (-5) (37 - (2 - (-77))))), curGen)
      | otherwise = ((min (-2) (max (-5) (- ((-2) - (-2))))), curGen)
      where
        blackboard = partialBlackboardBlVAR0Index2

    (newValBlVAR0Index2, tempGen3) = initValBlVAR0Index2 tempGen2

    partialBlackboardBlVAR3 = BTreeBlackboard newSereneGenerator newValBlVAR0Index0 newValBlVAR0Index1 newValBlVAR0Index2 True " " " " True True
    initValBlVAR3 :: StdGen -> (Bool, StdGen)
    initValBlVAR3 curGen
      | True = (((boardBlVAR0 0 blackboard) > 7), curGen)
      | otherwise = ((((sereneCOUNT (97 >= (boardBlVAR0 0 blackboard)) (sereneXNOR False True)) + (sereneCOUNT False (False && True))) >= (47 + (-40))), curGen)
      where
        blackboard = partialBlackboardBlVAR3

    (newValBlVAR3, tempGen4) = initValBlVAR3 tempGen3

    partialBlackboardLocalFROZENVAR5Location0Index0 = BTreeBlackboard newSereneGenerator newValBlVAR0Index0 newValBlVAR0Index1 newValBlVAR0Index2 newValBlVAR3 " " " " True True
    localInitValLocalFROZENVAR5Location0Index0 :: StdGen -> (String, StdGen)
    localInitValLocalFROZENVAR5Location0Index0 curGen = ("both", curGen)
      where
        blackboard = partialBlackboardLocalFROZENVAR5Location0Index0
        nodeLocation = 0

    (localNewValLocalFROZENVAR5Location0Index0, tempGen5) = localInitValLocalFROZENVAR5Location0Index0 tempGen4

    partialBlackboardLocalFROZENVAR5Location0Index1 = BTreeBlackboard newSereneGenerator newValBlVAR0Index0 newValBlVAR0Index1 newValBlVAR0Index2 newValBlVAR3 localNewValLocalFROZENVAR5Location0Index0 " " True True
    localInitValLocalFROZENVAR5Location0Index1 :: StdGen -> (String, StdGen)
    localInitValLocalFROZENVAR5Location0Index1 curGen = ("both", curGen)
      where
        blackboard = partialBlackboardLocalFROZENVAR5Location0Index1
        nodeLocation = 0

    (localNewValLocalFROZENVAR5Location0Index1, tempGen6) = localInitValLocalFROZENVAR5Location0Index1 tempGen5

    partialBlackboardLocalVAR4Location0 = BTreeBlackboard newSereneGenerator newValBlVAR0Index0 newValBlVAR0Index1 newValBlVAR0Index2 newValBlVAR3 localNewValLocalFROZENVAR5Location0Index0 localNewValLocalFROZENVAR5Location0Index1 True True
    localInitValLocalVAR4Location0 :: StdGen -> (Bool, StdGen)
    localInitValLocalVAR4Location0 curGen
      | (((-54) > (boardBlVAR0 0 blackboard)) || (sereneIMPLIES False False)) = (newValBlVAR3, curGen)
      | otherwise = (((boardBlVAR0 1 blackboard) > (boardBlVAR0 2 blackboard)), curGen)
      where
        blackboard = partialBlackboardLocalVAR4Location0
        nodeLocation = 0

    (localNewValLocalVAR4Location0, tempGen7) = localInitValLocalVAR4Location0 tempGen6

    partialBlackboardLocalFROZENVAR6Location0 = BTreeBlackboard newSereneGenerator newValBlVAR0Index0 newValBlVAR0Index1 newValBlVAR0Index2 newValBlVAR3 localNewValLocalFROZENVAR5Location0Index0 localNewValLocalFROZENVAR5Location0Index1 localNewValLocalVAR4Location0 True
    localInitValLocalFROZENVAR6Location0 :: StdGen -> (Bool, StdGen)
    localInitValLocalFROZENVAR6Location0 curGen
      | ((boardBlVAR0 2 blackboard) < (boardBlVAR0 1 blackboard)) = (("yes" /= "no"), curGen)
      | ((-18) >= (boardBlVAR0 0 blackboard)) = (False, curGen)
      | otherwise = ((((boardBlVAR0 0 blackboard) < 3) && (newValBlVAR3 == newValBlVAR3)), curGen)
      where
        blackboard = partialBlackboardLocalFROZENVAR6Location0
        nodeLocation = 0

    (localNewValLocalFROZENVAR6Location0, tempGen8) = localInitValLocalFROZENVAR6Location0 tempGen7


