module BehaviorTreeBlackboard where
import SereneRandomizer
import System.Random
import SereneOperations

data BTreeBlackboard = BTreeBlackboard {
  sereneBoardGenerator :: StdGen
  , boardBlVAR0Index0 :: Integer
  , boardBlVAR0Index1 :: Integer
  , localBoardLocalVAR2Location0Index0 :: Bool
  , localBoardLocalVAR2Location0Index1 :: Bool
  }

fromBTreeBlackboardToString :: BTreeBlackboard -> String
fromBTreeBlackboardToString blackboard = "Board = {" ++ "boardBlVAR0: " ++ "[" ++ show (boardBlVAR0 0 blackboard) ++ ", " ++ show (boardBlVAR0 1 blackboard)++ "]" ++ ", " ++ "boardBlVAR0: " ++ "[" ++ show (boardBlVAR0 0 blackboard) ++ ", " ++ show (boardBlVAR0 1 blackboard)++ "]" ++ ", " ++ "localBoardLocalVAR2Location0: " ++ "[" ++ show (localBoardLocalVAR2 0 0 blackboard) ++ ", " ++ show (localBoardLocalVAR2 0 1 blackboard)++ "]" ++ ", " ++ "boardBlDEFINE5: " ++ show (boardBlDEFINE5 blackboard) ++ ", " ++ "localBoardLocalDEFINE4Location0: " ++ "[" ++ show (localBoardLocalDEFINE4 0 0 blackboard) ++ ", " ++ show (localBoardLocalDEFINE4 0 1 blackboard)++ "]" ++ "}"

-- START OF BLACKBOARD FUNCTIONS

boardBlDEFINE5 :: BTreeBlackboard -> Integer
boardBlDEFINE5 blackboard
  | False = (min 5 (max 2 (min (-78) (-20))))
  | (True == (False || False)) = (min 5 (max 2 (((sereneCOUNT ((boardBlVAR0 1 blackboard) > (-8)) (sereneXOR False True)) + (sereneCOUNT (True || True) (sereneXNOR False True))) + ((boardBlVAR0 1 blackboard) + (boardBlVAR0 0 blackboard)))))
  | otherwise = (min 5 (max 2 (max 81 (boardBlVAR0 0 blackboard))))

-- START OF LOCAL BLACKBOARD FUNCTIONS

localBoardLocalDEFINE4 :: Integer -> Integer -> BTreeBlackboard -> Integer
localBoardLocalDEFINE4 0 = localBoardLocalDEFINE4Location0
localBoardLocalDEFINE4 _ = error "localBoardLocalDEFINE4 illegal local reference"
localBoardLocalDEFINE4Location0 :: Integer -> BTreeBlackboard -> Integer
localBoardLocalDEFINE4Location0 0 = localBoardLocalDEFINE4Location0Index0
localBoardLocalDEFINE4Location0 1 = localBoardLocalDEFINE4Location0Index1
localBoardLocalDEFINE4Location0 _ = error "localBoardLocalDEFINE40 illegal index"
localBoardLocalDEFINE4Location0Index0 blackboard
  | (((boardBlVAR0 1 blackboard) /= (boardBlVAR0 1 blackboard)) == (((-32) > (boardBlVAR0 1 blackboard)) || False)) = (min 5 (max 2 (boardBlVAR0 1 blackboard)))
  | otherwise = (min 5 (max 2 (8 - (boardBlVAR0 0 blackboard))))
  where nodeLocation = 0
localBoardLocalDEFINE4Location0Index1 blackboard
  | ((boardBlVAR0 1 blackboard) < ((boardBlVAR0 1 blackboard) + (boardBlVAR0 0 blackboard))) = (min 5 (max 2 (50 - (boardBlVAR0 0 blackboard))))
  | ((boardBlVAR0 0 blackboard) > (abs (boardBlVAR0 1 blackboard))) = (min 5 (max 2 ((boardBlVAR0 0 blackboard) + (boardBlVAR0 0 blackboard))))
  | otherwise = (min 5 (max 2 (boardBlVAR0 0 blackboard)))
  where nodeLocation = 0

-- START OF GET FUNCTIONS FOR LOCAL VARIABLES

localBoardLocalVAR2 :: Integer -> Integer -> BTreeBlackboard -> Bool
localBoardLocalVAR2 0 = localBoardLocalVAR2Location0
localBoardLocalVAR2 _ = error "localVAR2 illegal local reference"

-- START OF GET FUNCTIONS FOR ARRAYS

boardBlVAR0 :: Integer -> BTreeBlackboard -> Integer
boardBlVAR0 0 = boardBlVAR0Index0
boardBlVAR0 1 = boardBlVAR0Index1
boardBlVAR0 _ = error "boardBlVAR0 illegal index value"
localBoardLocalVAR2Location0 :: Integer -> BTreeBlackboard -> Bool
localBoardLocalVAR2Location0 0 = localBoardLocalVAR2Location0Index0
localBoardLocalVAR2Location0 1 = localBoardLocalVAR2Location0Index1
localBoardLocalVAR20 _ = error "localBoardLocalVAR20 illegal index value"

-- START OF TYPE CHECKING FUNCTIONS

checkValueBoardBlVAR0 :: Integer -> Integer
checkValueBoardBlVAR0 value
  | (-5) > value || value > (-2) = error "boardBlVAR0 illegal value"
  | otherwise = value

checkValueLocalBoardLocalVAR2 :: Bool -> Bool
checkValueLocalBoardLocalVAR2 value = value

checkValueLocalBoardLocalVAR3 :: Bool -> Bool
checkValueLocalBoardLocalVAR3 value = value


-- START OF SET FUNCTIONS

updateBoardGenerator :: BTreeBlackboard -> StdGen -> BTreeBlackboard
updateBoardGenerator blackboard newGen = blackboard { sereneBoardGenerator = newGen }
updateBoardBlVAR0Index0 :: BTreeBlackboard -> Integer -> BTreeBlackboard
updateBoardBlVAR0Index0 blackboard value = blackboard { boardBlVAR0Index0 = (checkValueBoardBlVAR0 value)}
updateBoardBlVAR0Index1 :: BTreeBlackboard -> Integer -> BTreeBlackboard
updateBoardBlVAR0Index1 blackboard value = blackboard { boardBlVAR0Index1 = (checkValueBoardBlVAR0 value)}
updateLocalBoardLocalVAR2Location0Index0 :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateLocalBoardLocalVAR2Location0Index0 blackboard value = blackboard { localBoardLocalVAR2Location0Index0 = (checkValueLocalBoardLocalVAR2 value)}
updateLocalBoardLocalVAR2Location0Index1 :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateLocalBoardLocalVAR2Location0Index1 blackboard value = blackboard { localBoardLocalVAR2Location0Index1 = (checkValueLocalBoardLocalVAR2 value)}

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
updateLocalBoardLocalVAR2 :: Integer -> Integer -> BTreeBlackboard -> Bool -> BTreeBlackboard
updateLocalBoardLocalVAR2 0 = updateLocalBoardLocalVAR2Location0
updateLocalBoardLocalVAR2 _ = error "localBoardLocalVAR2 illegal local reference"
arrayUpdateLocalBoardLocalVAR2 :: Integer -> BTreeBlackboard -> [(Integer, Bool)] -> BTreeBlackboard
arrayUpdateLocalBoardLocalVAR2 0 = arrayUpdateLocalBoardLocalVAR2Location0
arrayUpdateLocalBoardLocalVAR2 _ = error "localBoardLocalVAR2 illegal local reference"
updateLocalBoardLocalVAR2Location0 :: Integer -> BTreeBlackboard -> Bool -> BTreeBlackboard
updateLocalBoardLocalVAR2Location0 0 = updateLocalBoardLocalVAR2Location0Index0
updateLocalBoardLocalVAR2Location0 1 = updateLocalBoardLocalVAR2Location0Index1
updateLocalBoardLocalVAR2Location0 _ = error "LocalBoardLocalVAR2Location0 illegal index value"
arrayUpdateLocalBoardLocalVAR2Location0 :: BTreeBlackboard -> [(Integer, Bool)] -> BTreeBlackboard
arrayUpdateLocalBoardLocalVAR2Location0 blackboard []  = blackboard
arrayUpdateLocalBoardLocalVAR2Location0 blackboard [(index, value)] = updateLocalBoardLocalVAR2Location0 index blackboard value
arrayUpdateLocalBoardLocalVAR2Location0 blackboard indicesValues = blackboard {
  localBoardLocalVAR2Location0Index0 = newLocalVAR2Location0Index0
  , localBoardLocalVAR2Location0Index1 = newLocalVAR2Location0Index1
  }
    where
      (newLocalVAR2Location0Index0, newLocalVAR2Location0Index1) = updateValues indicesValues
      updateValues :: [(Integer, Bool)] -> (Bool, Bool)
      updateValues [] = (localBoardLocalVAR2Location0Index0 blackboard, localBoardLocalVAR2Location0Index1 blackboard)
      updateValues ((0, currentValue) : nextIndicesValues) = (checkValueLocalBoardLocalVAR2 currentValue, updatedValue1)
        where
          (_, updatedValue1) = updateValues nextIndicesValues
      updateValues ((1, currentValue) : nextIndicesValues) = (updatedValue0, checkValueLocalBoardLocalVAR2 currentValue)
        where
          (updatedValue0, _) = updateValues nextIndicesValues

-- START OF INITIAL BLACKBOARD VALUE

initialBlackboard :: Integer -> BTreeBlackboard
initialBlackboard seed = BTreeBlackboard newSereneGenerator newValBlVAR0Index0 newValBlVAR0Index1 localNewValLocalVAR2Location0Index0 localNewValLocalVAR2Location0Index1  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen4
    partialBlackboardBlVAR0Index0 = BTreeBlackboard newSereneGenerator 0 0 True True
    initValBlVAR0Index0 :: StdGen -> (Integer, StdGen)
    initValBlVAR0Index0 curGen
      | ((3 * (4 * ((-2) * 27))) > (4 + (5 + (-2)))) = ((min (-2) (max (-5) 17)), curGen)
      | False = ((min (-2) (max (-5) (max (-5) 4))), curGen)
      | otherwise = ((min (-2) (max (-5) (min (- 90) (5 * (((-85) + ((-4) + ((-4) + (-27)))) * (abs 5)))))), curGen)
      where
        blackboard = partialBlackboardBlVAR0Index0

    (newValBlVAR0Index0, tempGen1) = initValBlVAR0Index0 tempGen0

    partialBlackboardBlVAR0Index1 = BTreeBlackboard newSereneGenerator newValBlVAR0Index0 0 True True
    initValBlVAR0Index1 :: StdGen -> (Integer, StdGen)
    initValBlVAR0Index1 curGen
      | ((3 * (4 * ((-2) * 27))) > (4 + (5 + (-2)))) = ((min (-2) (max (-5) 17)), curGen)
      | False = ((min (-2) (max (-5) (max (-5) 4))), curGen)
      | otherwise = ((min (-2) (max (-5) (min (- 90) (5 * (((-85) + ((-4) + ((-4) + (-27)))) * (abs 5)))))), curGen)
      where
        blackboard = partialBlackboardBlVAR0Index1

    (newValBlVAR0Index1, tempGen2) = initValBlVAR0Index1 tempGen1

    partialBlackboardLocalVAR2Location0Index0 = BTreeBlackboard newSereneGenerator newValBlVAR0Index0 newValBlVAR0Index1 True True
    localInitValLocalVAR2Location0Index0 :: StdGen -> (Bool, StdGen)
    localInitValLocalVAR2Location0Index0 curGen
      | (sereneIMPLIES False False) = (((boardBlDEFINE5 blackboard) > (boardBlVAR0 0 blackboard)), curGen)
      | (sereneIMPLIES (False == False) (False || True)) = (False, curGen)
      | otherwise = ((sereneXNOR ((-76) > 69) (False /= True)), curGen)
      where
        blackboard = partialBlackboardLocalVAR2Location0Index0
        nodeLocation = 0

    (localNewValLocalVAR2Location0Index0, tempGen3) = localInitValLocalVAR2Location0Index0 tempGen2

    partialBlackboardLocalVAR2Location0Index1 = BTreeBlackboard newSereneGenerator newValBlVAR0Index0 newValBlVAR0Index1 localNewValLocalVAR2Location0Index0 True
    localInitValLocalVAR2Location0Index1 :: StdGen -> (Bool, StdGen)
    localInitValLocalVAR2Location0Index1 curGen
      | (False && True) = ((sereneXOR False True), curGen)
      | (((boardBlDEFINE5 blackboard) > 78) && True) = (True, curGen)
      | otherwise = (((True && False) /= False), curGen)
      where
        blackboard = partialBlackboardLocalVAR2Location0Index1
        nodeLocation = 0

    (localNewValLocalVAR2Location0Index1, tempGen4) = localInitValLocalVAR2Location0Index1 tempGen3


