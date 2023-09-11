module BehaviorTreeBlackboard where
import SereneRandomizer
import System.Random
import SereneOperations

data BTreeBlackboard = BTreeBlackboard {
  sereneBoardGenerator :: StdGen
  , boardBlVAR0Index0 :: Integer
  , boardBlVAR0Index1 :: Integer
  , boardBlVAR0Index2 :: Integer
  , localBoardLocalVAR3Location4Index0 :: Bool
  , localBoardLocalVAR3Location4Index1 :: Bool
  , localBoardLocalVAR3Location6Index0 :: Bool
  , localBoardLocalVAR3Location6Index1 :: Bool
  }

fromBTreeBlackboardToString :: BTreeBlackboard -> String
fromBTreeBlackboardToString blackboard = "Board = {" ++ "boardBlVAR0: " ++ "[" ++ show (boardBlVAR0 0 blackboard) ++ ", " ++ show (boardBlVAR0 1 blackboard) ++ ", " ++ show (boardBlVAR0 2 blackboard)++ "]" ++ ", " ++ "boardBlVAR0: " ++ "[" ++ show (boardBlVAR0 0 blackboard) ++ ", " ++ show (boardBlVAR0 1 blackboard) ++ ", " ++ show (boardBlVAR0 2 blackboard)++ "]" ++ ", " ++ "boardBlVAR0: " ++ "[" ++ show (boardBlVAR0 0 blackboard) ++ ", " ++ show (boardBlVAR0 1 blackboard) ++ ", " ++ show (boardBlVAR0 2 blackboard)++ "]" ++ ", " ++ "localBoardLocalVAR3Location4: " ++ "[" ++ show (localBoardLocalVAR3 4 0 blackboard) ++ ", " ++ show (localBoardLocalVAR3 4 1 blackboard)++ "]" ++ ", " ++ "localBoardLocalVAR3Location6: " ++ "[" ++ show (localBoardLocalVAR3 6 0 blackboard) ++ ", " ++ show (localBoardLocalVAR3 6 1 blackboard)++ "]" ++ ", " ++ "boardBlDEFINE5: " ++ show (boardBlDEFINE5 blackboard) ++ "}"

-- START OF BLACKBOARD FUNCTIONS

boardBlDEFINE5 :: BTreeBlackboard -> Integer
boardBlDEFINE5 blackboard = (min (-2) (max (-5) (boardBlVAR0 2 blackboard)))

-- START OF LOCAL BLACKBOARD FUNCTIONS


-- START OF GET FUNCTIONS FOR LOCAL VARIABLES

localBoardLocalVAR3 :: Integer -> Integer -> BTreeBlackboard -> Bool
localBoardLocalVAR3 4 = localBoardLocalVAR3Location4
localBoardLocalVAR3 6 = localBoardLocalVAR3Location6
localBoardLocalVAR3 _ = error "localVAR3 illegal local reference"

-- START OF GET FUNCTIONS FOR ARRAYS

boardBlVAR0 :: Integer -> BTreeBlackboard -> Integer
boardBlVAR0 0 = boardBlVAR0Index0
boardBlVAR0 1 = boardBlVAR0Index1
boardBlVAR0 2 = boardBlVAR0Index2
boardBlVAR0 _ = error "boardBlVAR0 illegal index value"
localBoardLocalVAR3Location4 :: Integer -> BTreeBlackboard -> Bool
localBoardLocalVAR3Location4 0 = localBoardLocalVAR3Location4Index0
localBoardLocalVAR3Location4 1 = localBoardLocalVAR3Location4Index1
localBoardLocalVAR34 _ = error "localBoardLocalVAR34 illegal index value"
localBoardLocalVAR3Location6 :: Integer -> BTreeBlackboard -> Bool
localBoardLocalVAR3Location6 0 = localBoardLocalVAR3Location6Index0
localBoardLocalVAR3Location6 1 = localBoardLocalVAR3Location6Index1
localBoardLocalVAR36 _ = error "localBoardLocalVAR36 illegal index value"

-- START OF TYPE CHECKING FUNCTIONS

checkValueBoardBlVAR0 :: Integer -> Integer
checkValueBoardBlVAR0 value
  | (-5) > value || value > (-2) = error "boardBlVAR0 illegal value"
  | otherwise = value

checkValueLocalBoardLocalVAR3 :: Bool -> Bool
checkValueLocalBoardLocalVAR3 value = value


-- START OF SET FUNCTIONS

updateBoardGenerator :: BTreeBlackboard -> StdGen -> BTreeBlackboard
updateBoardGenerator blackboard newGen = blackboard { sereneBoardGenerator = newGen }
updateBoardBlVAR0Index0 :: BTreeBlackboard -> Integer -> BTreeBlackboard
updateBoardBlVAR0Index0 blackboard value = blackboard { boardBlVAR0Index0 = (checkValueBoardBlVAR0 value)}
updateBoardBlVAR0Index1 :: BTreeBlackboard -> Integer -> BTreeBlackboard
updateBoardBlVAR0Index1 blackboard value = blackboard { boardBlVAR0Index1 = (checkValueBoardBlVAR0 value)}
updateBoardBlVAR0Index2 :: BTreeBlackboard -> Integer -> BTreeBlackboard
updateBoardBlVAR0Index2 blackboard value = blackboard { boardBlVAR0Index2 = (checkValueBoardBlVAR0 value)}
updateLocalBoardLocalVAR3Location4Index0 :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateLocalBoardLocalVAR3Location4Index0 blackboard value = blackboard { localBoardLocalVAR3Location4Index0 = (checkValueLocalBoardLocalVAR3 value)}
updateLocalBoardLocalVAR3Location4Index1 :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateLocalBoardLocalVAR3Location4Index1 blackboard value = blackboard { localBoardLocalVAR3Location4Index1 = (checkValueLocalBoardLocalVAR3 value)}
updateLocalBoardLocalVAR3Location6Index0 :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateLocalBoardLocalVAR3Location6Index0 blackboard value = blackboard { localBoardLocalVAR3Location6Index0 = (checkValueLocalBoardLocalVAR3 value)}
updateLocalBoardLocalVAR3Location6Index1 :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateLocalBoardLocalVAR3Location6Index1 blackboard value = blackboard { localBoardLocalVAR3Location6Index1 = (checkValueLocalBoardLocalVAR3 value)}

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
updateLocalBoardLocalVAR3 :: Integer -> Integer -> BTreeBlackboard -> Bool -> BTreeBlackboard
updateLocalBoardLocalVAR3 4 = updateLocalBoardLocalVAR3Location4
updateLocalBoardLocalVAR3 6 = updateLocalBoardLocalVAR3Location6
updateLocalBoardLocalVAR3 _ = error "localBoardLocalVAR3 illegal local reference"
arrayUpdateLocalBoardLocalVAR3 :: Integer -> BTreeBlackboard -> [(Integer, Bool)] -> BTreeBlackboard
arrayUpdateLocalBoardLocalVAR3 4 = arrayUpdateLocalBoardLocalVAR3Location4
arrayUpdateLocalBoardLocalVAR3 6 = arrayUpdateLocalBoardLocalVAR3Location6
arrayUpdateLocalBoardLocalVAR3 _ = error "localBoardLocalVAR3 illegal local reference"
updateLocalBoardLocalVAR3Location4 :: Integer -> BTreeBlackboard -> Bool -> BTreeBlackboard
updateLocalBoardLocalVAR3Location4 0 = updateLocalBoardLocalVAR3Location4Index0
updateLocalBoardLocalVAR3Location4 1 = updateLocalBoardLocalVAR3Location4Index1
updateLocalBoardLocalVAR3Location4 _ = error "LocalBoardLocalVAR3Location4 illegal index value"
arrayUpdateLocalBoardLocalVAR3Location4 :: BTreeBlackboard -> [(Integer, Bool)] -> BTreeBlackboard
arrayUpdateLocalBoardLocalVAR3Location4 blackboard []  = blackboard
arrayUpdateLocalBoardLocalVAR3Location4 blackboard [(index, value)] = updateLocalBoardLocalVAR3Location4 index blackboard value
arrayUpdateLocalBoardLocalVAR3Location4 blackboard indicesValues = blackboard {
  localBoardLocalVAR3Location4Index0 = newLocalVAR3Location4Index0
  , localBoardLocalVAR3Location4Index1 = newLocalVAR3Location4Index1
  }
    where
      (newLocalVAR3Location4Index0, newLocalVAR3Location4Index1) = updateValues indicesValues
      updateValues :: [(Integer, Bool)] -> (Bool, Bool)
      updateValues [] = (localBoardLocalVAR3Location4Index0 blackboard, localBoardLocalVAR3Location4Index1 blackboard)
      updateValues ((0, currentValue) : nextIndicesValues) = (checkValueLocalBoardLocalVAR3 currentValue, updatedValue1)
        where
          (_, updatedValue1) = updateValues nextIndicesValues
      updateValues ((1, currentValue) : nextIndicesValues) = (updatedValue0, checkValueLocalBoardLocalVAR3 currentValue)
        where
          (updatedValue0, _) = updateValues nextIndicesValues
updateLocalBoardLocalVAR3Location6 :: Integer -> BTreeBlackboard -> Bool -> BTreeBlackboard
updateLocalBoardLocalVAR3Location6 0 = updateLocalBoardLocalVAR3Location6Index0
updateLocalBoardLocalVAR3Location6 1 = updateLocalBoardLocalVAR3Location6Index1
updateLocalBoardLocalVAR3Location6 _ = error "LocalBoardLocalVAR3Location6 illegal index value"
arrayUpdateLocalBoardLocalVAR3Location6 :: BTreeBlackboard -> [(Integer, Bool)] -> BTreeBlackboard
arrayUpdateLocalBoardLocalVAR3Location6 blackboard []  = blackboard
arrayUpdateLocalBoardLocalVAR3Location6 blackboard [(index, value)] = updateLocalBoardLocalVAR3Location6 index blackboard value
arrayUpdateLocalBoardLocalVAR3Location6 blackboard indicesValues = blackboard {
  localBoardLocalVAR3Location6Index0 = newLocalVAR3Location6Index0
  , localBoardLocalVAR3Location6Index1 = newLocalVAR3Location6Index1
  }
    where
      (newLocalVAR3Location6Index0, newLocalVAR3Location6Index1) = updateValues indicesValues
      updateValues :: [(Integer, Bool)] -> (Bool, Bool)
      updateValues [] = (localBoardLocalVAR3Location6Index0 blackboard, localBoardLocalVAR3Location6Index1 blackboard)
      updateValues ((0, currentValue) : nextIndicesValues) = (checkValueLocalBoardLocalVAR3 currentValue, updatedValue1)
        where
          (_, updatedValue1) = updateValues nextIndicesValues
      updateValues ((1, currentValue) : nextIndicesValues) = (updatedValue0, checkValueLocalBoardLocalVAR3 currentValue)
        where
          (updatedValue0, _) = updateValues nextIndicesValues

-- START OF INITIAL BLACKBOARD VALUE

initialBlackboard :: Integer -> BTreeBlackboard
initialBlackboard seed = BTreeBlackboard newSereneGenerator newValBlVAR0Index0 newValBlVAR0Index1 newValBlVAR0Index2 localNewValLocalVAR3Location4Index0 localNewValLocalVAR3Location4Index1 localNewValLocalVAR3Location6Index0 localNewValLocalVAR3Location6Index1  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen7
    partialBlackboardBlVAR0Index0 = BTreeBlackboard newSereneGenerator 0 0 0 True True True True
    initValBlVAR0Index0 :: StdGen -> (Integer, StdGen)
    initValBlVAR0Index0 curGen
      | ((sereneXOR False False) == (sereneIMPLIES False False)) = ((min (-2) (max (-5) (74 - (max (-80) (-2))))), curGen)
      | otherwise = ((min (-2) (max (-5) (max 2 (-22)))), curGen)
      where
        blackboard = partialBlackboardBlVAR0Index0

    (newValBlVAR0Index0, tempGen1) = initValBlVAR0Index0 tempGen0

    partialBlackboardBlVAR0Index1 = BTreeBlackboard newSereneGenerator newValBlVAR0Index0 0 0 True True True True
    initValBlVAR0Index1 :: StdGen -> (Integer, StdGen)
    initValBlVAR0Index1 curGen
      | True = ((min (-2) (max (-5) (- ((sereneCOUNT (False == True) (4 /= 5)) + (4 + (-66)))))), curGen)
      | (True && False) = ((min (-2) (max (-5) (abs (((sereneCOUNT (True && False) (sereneXNOR True True)) + (sereneCOUNT False (False == False))) - (- (-80)))))), curGen)
      | otherwise = ((min (-2) (max (-5) (- (23 * (75 * (-45)))))), curGen)
      where
        blackboard = partialBlackboardBlVAR0Index1

    (newValBlVAR0Index1, tempGen2) = initValBlVAR0Index1 tempGen1

    partialBlackboardBlVAR0Index2 = BTreeBlackboard newSereneGenerator newValBlVAR0Index0 newValBlVAR0Index1 0 True True True True
    initValBlVAR0Index2 :: StdGen -> (Integer, StdGen)
    initValBlVAR0Index2 curGen = ((min (-2) (max (-5) (-87))), curGen)
      where
        blackboard = partialBlackboardBlVAR0Index2

    (newValBlVAR0Index2, tempGen3) = initValBlVAR0Index2 tempGen2

    partialBlackboardLocalVAR3Location4Index0 = BTreeBlackboard newSereneGenerator newValBlVAR0Index0 newValBlVAR0Index1 newValBlVAR0Index2 True True True True
    localInitValLocalVAR3Location4Index0 :: StdGen -> (Bool, StdGen)
    localInitValLocalVAR3Location4Index0 curGen
      | (True == True) = (("both" /= "both"), curGen)
      | True = (((-26) < (-63)), curGen)
      | otherwise = (True, curGen)
      where
        blackboard = partialBlackboardLocalVAR3Location4Index0
        nodeLocation = 4

    (localNewValLocalVAR3Location4Index0, tempGen4) = localInitValLocalVAR3Location4Index0 tempGen3

    partialBlackboardLocalVAR3Location4Index1 = BTreeBlackboard newSereneGenerator newValBlVAR0Index0 newValBlVAR0Index1 newValBlVAR0Index2 localNewValLocalVAR3Location4Index0 True True True
    localInitValLocalVAR3Location4Index1 :: StdGen -> (Bool, StdGen)
    localInitValLocalVAR3Location4Index1 curGen
      | False = (True, curGen)
      | otherwise = (("yes" /= "no"), curGen)
      where
        blackboard = partialBlackboardLocalVAR3Location4Index1
        nodeLocation = 4

    (localNewValLocalVAR3Location4Index1, tempGen5) = localInitValLocalVAR3Location4Index1 tempGen4

    partialBlackboardLocalVAR3Location6Index0 = BTreeBlackboard newSereneGenerator newValBlVAR0Index0 newValBlVAR0Index1 newValBlVAR0Index2 localNewValLocalVAR3Location4Index0 localNewValLocalVAR3Location4Index1 True True
    localInitValLocalVAR3Location6Index0 :: StdGen -> (Bool, StdGen)
    localInitValLocalVAR3Location6Index0 curGen
      | (True == True) = (("both" /= "both"), curGen)
      | True = (((-26) < (-63)), curGen)
      | otherwise = (True, curGen)
      where
        blackboard = partialBlackboardLocalVAR3Location6Index0
        nodeLocation = 6

    (localNewValLocalVAR3Location6Index0, tempGen6) = localInitValLocalVAR3Location6Index0 tempGen5

    partialBlackboardLocalVAR3Location6Index1 = BTreeBlackboard newSereneGenerator newValBlVAR0Index0 newValBlVAR0Index1 newValBlVAR0Index2 localNewValLocalVAR3Location4Index0 localNewValLocalVAR3Location4Index1 localNewValLocalVAR3Location6Index0 True
    localInitValLocalVAR3Location6Index1 :: StdGen -> (Bool, StdGen)
    localInitValLocalVAR3Location6Index1 curGen
      | False = (True, curGen)
      | otherwise = (("yes" /= "no"), curGen)
      where
        blackboard = partialBlackboardLocalVAR3Location6Index1
        nodeLocation = 6

    (localNewValLocalVAR3Location6Index1, tempGen7) = localInitValLocalVAR3Location6Index1 tempGen6


