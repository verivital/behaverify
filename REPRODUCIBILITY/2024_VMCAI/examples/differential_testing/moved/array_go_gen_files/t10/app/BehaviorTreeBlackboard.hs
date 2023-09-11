module BehaviorTreeBlackboard where
import SereneRandomizer
import System.Random
import SereneOperations

data BTreeBlackboard = BTreeBlackboard {
  sereneBoardGenerator :: StdGen
  , boardBlVAR0Index0 :: String
  , boardBlVAR0Index1 :: String
  , boardBlVAR0Index2 :: String
  , boardBlVAR3 :: String
  , localBoardLocalVAR2Location3Index0 :: Integer
  , localBoardLocalVAR2Location3Index1 :: Integer
  , localBoardLocalVAR2Location3Index2 :: Integer
  }

fromBTreeBlackboardToString :: BTreeBlackboard -> String
fromBTreeBlackboardToString blackboard = "Board = {" ++ "boardBlVAR0: " ++ "[" ++ show (boardBlVAR0 0 blackboard) ++ ", " ++ show (boardBlVAR0 1 blackboard) ++ ", " ++ show (boardBlVAR0 2 blackboard)++ "]" ++ ", " ++ "boardBlVAR0: " ++ "[" ++ show (boardBlVAR0 0 blackboard) ++ ", " ++ show (boardBlVAR0 1 blackboard) ++ ", " ++ show (boardBlVAR0 2 blackboard)++ "]" ++ ", " ++ "boardBlVAR0: " ++ "[" ++ show (boardBlVAR0 0 blackboard) ++ ", " ++ show (boardBlVAR0 1 blackboard) ++ ", " ++ show (boardBlVAR0 2 blackboard)++ "]" ++ ", " ++ "boardBlVAR3: " ++ show (boardBlVAR3 blackboard) ++ ", " ++ "localBoardLocalVAR2Location3: " ++ "[" ++ show (localBoardLocalVAR2 3 0 blackboard) ++ ", " ++ show (localBoardLocalVAR2 3 1 blackboard) ++ ", " ++ show (localBoardLocalVAR2 3 2 blackboard)++ "]" ++ ", " ++ "boardBlDEFINE5: " ++ "[" ++ show (boardBlDEFINE5 0 blackboard) ++ ", " ++ show (boardBlDEFINE5 1 blackboard)++ "]" ++ ", " ++ "localBoardLocalDEFINE4Location3: " ++ show (localBoardLocalDEFINE4 3blackboard) ++ ", " ++ "localBoardLocalDEFINE6Location3: " ++ "[" ++ show (localBoardLocalDEFINE6 3 0 blackboard) ++ ", " ++ show (localBoardLocalDEFINE6 3 1 blackboard)++ "]" ++ "}"

-- START OF BLACKBOARD FUNCTIONS

boardBlDEFINE5 :: Integer -> BTreeBlackboard -> Integer
boardBlDEFINE5 0 blackboard
  | ((-73) /= (4 - 31)) = (min 5 (max 2 (abs (5 + (2 + (28 + (-18)))))))
  | False = (min 5 (max 2 ((-2) * 73)))
  | otherwise = (min 5 (max 2 (sereneCOUNT ((sereneXNOR True True) && ((-2) < 2)) (False || True))))
boardBlDEFINE5 1 blackboard = (min 5 (max 2 (((-6) - 85) * (min 5 3))))
boardBlDEFINE5 _ _ = error "boardBlDEFINE5 illegal index value"

-- START OF LOCAL BLACKBOARD FUNCTIONS

localBoardLocalDEFINE4 :: Integer -> BTreeBlackboard -> String
localBoardLocalDEFINE4 3 blackboard
  | (False || False) = "no"
  | ((-3) <= (-3)) = "both"
  | otherwise = "both"
  where nodeLocation = 3
localBoardLocalDEFINE4 _ _ = error "localDEFINE4 illegal local reference"
localBoardLocalDEFINE6 :: Integer -> Integer -> BTreeBlackboard -> Integer
localBoardLocalDEFINE6 3 = localBoardLocalDEFINE6Location3
localBoardLocalDEFINE6 _ = error "localBoardLocalDEFINE6 illegal local reference"
localBoardLocalDEFINE6Location3 :: Integer -> BTreeBlackboard -> Integer
localBoardLocalDEFINE6Location3 0 = localBoardLocalDEFINE6Location3Index0
localBoardLocalDEFINE6Location3 1 = localBoardLocalDEFINE6Location3Index1
localBoardLocalDEFINE6Location3 _ = error "localBoardLocalDEFINE63 illegal index"
localBoardLocalDEFINE6Location3Index0 blackboard
  | ((max (boardBlDEFINE5 1 blackboard) (-1)) > (- (boardBlDEFINE5 1 blackboard))) = (min (-2) (max (-5) (boardBlDEFINE5 0 blackboard)))
  | otherwise = (min (-2) (max (-5) 6))
  where nodeLocation = 3
localBoardLocalDEFINE6Location3Index1 blackboard
  | True = (min (-2) (max (-5) (((boardBlDEFINE5 0 blackboard) + 15) - (boardBlDEFINE5 1 blackboard))))
  | otherwise = (min (-2) (max (-5) (- ((boardBlDEFINE5 1 blackboard) * (boardBlDEFINE5 1 blackboard)))))
  where nodeLocation = 3

-- START OF GET FUNCTIONS FOR LOCAL VARIABLES

localBoardLocalVAR2 :: Integer -> Integer -> BTreeBlackboard -> Integer
localBoardLocalVAR2 3 = localBoardLocalVAR2Location3
localBoardLocalVAR2 _ = error "localVAR2 illegal local reference"

-- START OF GET FUNCTIONS FOR ARRAYS

boardBlVAR0 :: Integer -> BTreeBlackboard -> String
boardBlVAR0 0 = boardBlVAR0Index0
boardBlVAR0 1 = boardBlVAR0Index1
boardBlVAR0 2 = boardBlVAR0Index2
boardBlVAR0 _ = error "boardBlVAR0 illegal index value"
localBoardLocalVAR2Location3 :: Integer -> BTreeBlackboard -> Integer
localBoardLocalVAR2Location3 0 = localBoardLocalVAR2Location3Index0
localBoardLocalVAR2Location3 1 = localBoardLocalVAR2Location3Index1
localBoardLocalVAR2Location3 2 = localBoardLocalVAR2Location3Index2
localBoardLocalVAR23 _ = error "localBoardLocalVAR23 illegal index value"

-- START OF TYPE CHECKING FUNCTIONS

checkValueBoardBlVAR0 :: String -> String
checkValueBoardBlVAR0 "yes" = "yes"
checkValueBoardBlVAR0 "no" = "no"
checkValueBoardBlVAR0 "both" = "both"
checkValueBoardBlVAR0 _ = error "boardBlVAR0 illegal value"

checkValueLocalBoardLocalVAR2 :: Integer -> Integer
checkValueLocalBoardLocalVAR2 value
  | 2 > value || value > 5 = error "localBoardLocalVAR2 illegal value"
  | otherwise = value

checkValueBoardBlVAR3 :: String -> String
checkValueBoardBlVAR3 "yes" = "yes"
checkValueBoardBlVAR3 "no" = "no"
checkValueBoardBlVAR3 "both" = "both"
checkValueBoardBlVAR3 _ = error "boardBlVAR3 illegal value"


-- START OF SET FUNCTIONS

updateBoardGenerator :: BTreeBlackboard -> StdGen -> BTreeBlackboard
updateBoardGenerator blackboard newGen = blackboard { sereneBoardGenerator = newGen }
updateBoardBlVAR0Index0 :: BTreeBlackboard -> String -> BTreeBlackboard
updateBoardBlVAR0Index0 blackboard value = blackboard { boardBlVAR0Index0 = (checkValueBoardBlVAR0 value)}
updateBoardBlVAR0Index1 :: BTreeBlackboard -> String -> BTreeBlackboard
updateBoardBlVAR0Index1 blackboard value = blackboard { boardBlVAR0Index1 = (checkValueBoardBlVAR0 value)}
updateBoardBlVAR0Index2 :: BTreeBlackboard -> String -> BTreeBlackboard
updateBoardBlVAR0Index2 blackboard value = blackboard { boardBlVAR0Index2 = (checkValueBoardBlVAR0 value)}
updateBoardBlVAR3 :: BTreeBlackboard -> String -> BTreeBlackboard
updateBoardBlVAR3 blackboard value = blackboard { boardBlVAR3 = (checkValueBoardBlVAR3 value)}
updateLocalBoardLocalVAR2Location3Index0 :: BTreeBlackboard -> Integer -> BTreeBlackboard
updateLocalBoardLocalVAR2Location3Index0 blackboard value = blackboard { localBoardLocalVAR2Location3Index0 = (checkValueLocalBoardLocalVAR2 value)}
updateLocalBoardLocalVAR2Location3Index1 :: BTreeBlackboard -> Integer -> BTreeBlackboard
updateLocalBoardLocalVAR2Location3Index1 blackboard value = blackboard { localBoardLocalVAR2Location3Index1 = (checkValueLocalBoardLocalVAR2 value)}
updateLocalBoardLocalVAR2Location3Index2 :: BTreeBlackboard -> Integer -> BTreeBlackboard
updateLocalBoardLocalVAR2Location3Index2 blackboard value = blackboard { localBoardLocalVAR2Location3Index2 = (checkValueLocalBoardLocalVAR2 value)}

-- START OF SET FUNCTIONS FOR ARRAYS

updateBoardBlVAR0 :: Integer -> BTreeBlackboard -> String -> BTreeBlackboard
updateBoardBlVAR0 0 = updateBoardBlVAR0Index0
updateBoardBlVAR0 1 = updateBoardBlVAR0Index1
updateBoardBlVAR0 2 = updateBoardBlVAR0Index2
updateBoardBlVAR0 _ = error "BoardBlVAR0 illegal index value"
arrayUpdateBoardBlVAR0 :: BTreeBlackboard -> [(Integer, String)] -> BTreeBlackboard
arrayUpdateBoardBlVAR0 blackboard []  = blackboard
arrayUpdateBoardBlVAR0 blackboard [(index, value)] = updateBoardBlVAR0 index blackboard value
arrayUpdateBoardBlVAR0 blackboard indicesValues = blackboard {
  boardBlVAR0Index0 = newBlVAR0Index0
  , boardBlVAR0Index1 = newBlVAR0Index1
  , boardBlVAR0Index2 = newBlVAR0Index2
  }
    where
      (newBlVAR0Index0, newBlVAR0Index1, newBlVAR0Index2) = updateValues indicesValues
      updateValues :: [(Integer, String)] -> (String, String, String)
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
updateLocalBoardLocalVAR2 :: Integer -> Integer -> BTreeBlackboard -> Integer -> BTreeBlackboard
updateLocalBoardLocalVAR2 3 = updateLocalBoardLocalVAR2Location3
updateLocalBoardLocalVAR2 _ = error "localBoardLocalVAR2 illegal local reference"
arrayUpdateLocalBoardLocalVAR2 :: Integer -> BTreeBlackboard -> [(Integer, Integer)] -> BTreeBlackboard
arrayUpdateLocalBoardLocalVAR2 3 = arrayUpdateLocalBoardLocalVAR2Location3
arrayUpdateLocalBoardLocalVAR2 _ = error "localBoardLocalVAR2 illegal local reference"
updateLocalBoardLocalVAR2Location3 :: Integer -> BTreeBlackboard -> Integer -> BTreeBlackboard
updateLocalBoardLocalVAR2Location3 0 = updateLocalBoardLocalVAR2Location3Index0
updateLocalBoardLocalVAR2Location3 1 = updateLocalBoardLocalVAR2Location3Index1
updateLocalBoardLocalVAR2Location3 2 = updateLocalBoardLocalVAR2Location3Index2
updateLocalBoardLocalVAR2Location3 _ = error "LocalBoardLocalVAR2Location3 illegal index value"
arrayUpdateLocalBoardLocalVAR2Location3 :: BTreeBlackboard -> [(Integer, Integer)] -> BTreeBlackboard
arrayUpdateLocalBoardLocalVAR2Location3 blackboard []  = blackboard
arrayUpdateLocalBoardLocalVAR2Location3 blackboard [(index, value)] = updateLocalBoardLocalVAR2Location3 index blackboard value
arrayUpdateLocalBoardLocalVAR2Location3 blackboard indicesValues = blackboard {
  localBoardLocalVAR2Location3Index0 = newLocalVAR2Location3Index0
  , localBoardLocalVAR2Location3Index1 = newLocalVAR2Location3Index1
  , localBoardLocalVAR2Location3Index2 = newLocalVAR2Location3Index2
  }
    where
      (newLocalVAR2Location3Index0, newLocalVAR2Location3Index1, newLocalVAR2Location3Index2) = updateValues indicesValues
      updateValues :: [(Integer, Integer)] -> (Integer, Integer, Integer)
      updateValues [] = (localBoardLocalVAR2Location3Index0 blackboard, localBoardLocalVAR2Location3Index1 blackboard, localBoardLocalVAR2Location3Index2 blackboard)
      updateValues ((0, currentValue) : nextIndicesValues) = (checkValueLocalBoardLocalVAR2 currentValue, updatedValue1, updatedValue2)
        where
          (_, updatedValue1, updatedValue2) = updateValues nextIndicesValues
      updateValues ((1, currentValue) : nextIndicesValues) = (updatedValue0, checkValueLocalBoardLocalVAR2 currentValue, updatedValue2)
        where
          (updatedValue0, _, updatedValue2) = updateValues nextIndicesValues
      updateValues ((2, currentValue) : nextIndicesValues) = (updatedValue0, updatedValue1, checkValueLocalBoardLocalVAR2 currentValue)
        where
          (updatedValue0, updatedValue1, _) = updateValues nextIndicesValues

-- START OF INITIAL BLACKBOARD VALUE

initialBlackboard :: Integer -> BTreeBlackboard
initialBlackboard seed = BTreeBlackboard newSereneGenerator newValBlVAR0Index0 newValBlVAR0Index1 newValBlVAR0Index2 newValBlVAR3 localNewValLocalVAR2Location3Index0 localNewValLocalVAR2Location3Index1 localNewValLocalVAR2Location3Index2  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen7
    partialBlackboardBlVAR0Index0 = BTreeBlackboard newSereneGenerator " " " " " " " " 0 0 0
    initValBlVAR0Index0 :: StdGen -> (String, StdGen)
    initValBlVAR0Index0 curGen
      | (False == (sereneIMPLIES True True)) = ("both", curGen)
      | otherwise = ("yes", curGen)
      where
        blackboard = partialBlackboardBlVAR0Index0

    (newValBlVAR0Index0, tempGen1) = initValBlVAR0Index0 tempGen0

    partialBlackboardBlVAR0Index1 = BTreeBlackboard newSereneGenerator newValBlVAR0Index0 " " " " " " 0 0 0
    initValBlVAR0Index1 :: StdGen -> (String, StdGen)
    initValBlVAR0Index1 curGen
      | ((2 >= 87) && True) = ("both", curGen)
      | otherwise = ("both", curGen)
      where
        blackboard = partialBlackboardBlVAR0Index1

    (newValBlVAR0Index1, tempGen2) = initValBlVAR0Index1 tempGen1

    partialBlackboardBlVAR0Index2 = BTreeBlackboard newSereneGenerator newValBlVAR0Index0 newValBlVAR0Index1 " " " " 0 0 0
    initValBlVAR0Index2 :: StdGen -> (String, StdGen)
    initValBlVAR0Index2 curGen
      | True = ("yes", curGen)
      | otherwise = ("yes", curGen)
      where
        blackboard = partialBlackboardBlVAR0Index2

    (newValBlVAR0Index2, tempGen3) = initValBlVAR0Index2 tempGen2

    partialBlackboardBlVAR3 = BTreeBlackboard newSereneGenerator newValBlVAR0Index0 newValBlVAR0Index1 newValBlVAR0Index2 " " 0 0 0
    initValBlVAR3 :: StdGen -> (String, StdGen)
    initValBlVAR3 curGen
      | (((-4) + ((min 2 (-5)) + ((-3) + (38 + ((-98) + 4))))) <= (-5)) = ((boardBlVAR0 1 blackboard), curGen)
      | otherwise = ((boardBlVAR0 2 blackboard), curGen)
      where
        blackboard = partialBlackboardBlVAR3

    (newValBlVAR3, tempGen4) = initValBlVAR3 tempGen3

    partialBlackboardLocalVAR2Location3Index0 = BTreeBlackboard newSereneGenerator newValBlVAR0Index0 newValBlVAR0Index1 newValBlVAR0Index2 newValBlVAR3 0 0 0
    localInitValLocalVAR2Location3Index0 :: StdGen -> (Integer, StdGen)
    localInitValLocalVAR2Location3Index0 curGen = ((min 5 (max 2 (- (abs (boardBlDEFINE5 1 blackboard))))), curGen)
      where
        blackboard = partialBlackboardLocalVAR2Location3Index0
        nodeLocation = 3

    (localNewValLocalVAR2Location3Index0, tempGen5) = localInitValLocalVAR2Location3Index0 tempGen4

    partialBlackboardLocalVAR2Location3Index1 = BTreeBlackboard newSereneGenerator newValBlVAR0Index0 newValBlVAR0Index1 newValBlVAR0Index2 newValBlVAR3 localNewValLocalVAR2Location3Index0 0 0
    localInitValLocalVAR2Location3Index1 :: StdGen -> (Integer, StdGen)
    localInitValLocalVAR2Location3Index1 curGen = ((min 5 (max 2 (29 - ((8 * ((boardBlDEFINE5 0 blackboard) * ((-63) * (boardBlDEFINE5 0 blackboard)))) + ((min (-36) (boardBlDEFINE5 0 blackboard)) + ((boardBlDEFINE5 1 blackboard) - (boardBlDEFINE5 1 blackboard))))))), curGen)
      where
        blackboard = partialBlackboardLocalVAR2Location3Index1
        nodeLocation = 3

    (localNewValLocalVAR2Location3Index1, tempGen6) = localInitValLocalVAR2Location3Index1 tempGen5

    partialBlackboardLocalVAR2Location3Index2 = BTreeBlackboard newSereneGenerator newValBlVAR0Index0 newValBlVAR0Index1 newValBlVAR0Index2 newValBlVAR3 localNewValLocalVAR2Location3Index0 localNewValLocalVAR2Location3Index1 0
    localInitValLocalVAR2Location3Index2 :: StdGen -> (Integer, StdGen)
    localInitValLocalVAR2Location3Index2 curGen = ((min 5 (max 2 (abs ((-65) - (boardBlDEFINE5 1 blackboard))))), curGen)
      where
        blackboard = partialBlackboardLocalVAR2Location3Index2
        nodeLocation = 3

    (localNewValLocalVAR2Location3Index2, tempGen7) = localInitValLocalVAR2Location3Index2 tempGen6


