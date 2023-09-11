module BehaviorTreeBlackboard where
import SereneRandomizer
import System.Random
import SereneOperations

data BTreeBlackboard = BTreeBlackboard {
  sereneBoardGenerator :: StdGen
  , boardBlVAR0Index0 :: Integer
  , boardBlVAR0Index1 :: Integer
  , boardBlVAR0Index2 :: Integer
  , localBoardLocalFROZENVAR4Location2 :: Integer
  , localBoardLocalFROZENVAR4Location4 :: Integer
  }

fromBTreeBlackboardToString :: BTreeBlackboard -> String
fromBTreeBlackboardToString blackboard = "Board = {" ++ "boardBlVAR0: " ++ "[" ++ show (boardBlVAR0 0 blackboard) ++ ", " ++ show (boardBlVAR0 1 blackboard) ++ ", " ++ show (boardBlVAR0 2 blackboard)++ "]" ++ ", " ++ "boardBlVAR0: " ++ "[" ++ show (boardBlVAR0 0 blackboard) ++ ", " ++ show (boardBlVAR0 1 blackboard) ++ ", " ++ show (boardBlVAR0 2 blackboard)++ "]" ++ ", " ++ "boardBlVAR0: " ++ "[" ++ show (boardBlVAR0 0 blackboard) ++ ", " ++ show (boardBlVAR0 1 blackboard) ++ ", " ++ show (boardBlVAR0 2 blackboard)++ "]" ++ ", " ++ "localBoardLocalFROZENVAR4Location2: " ++ show (localBoardLocalFROZENVAR4 2blackboard) ++ ", " ++ "localBoardLocalFROZENVAR4Location4: " ++ show (localBoardLocalFROZENVAR4 4blackboard) ++ ", " ++ "boardBlDEFINE5: " ++ "[" ++ show (boardBlDEFINE5 0 blackboard) ++ ", " ++ show (boardBlDEFINE5 1 blackboard) ++ ", " ++ show (boardBlDEFINE5 2 blackboard)++ "]" ++ ", " ++ "boardBlDEFINE7: " ++ "[" ++ show (boardBlDEFINE7 0 blackboard) ++ ", " ++ show (boardBlDEFINE7 1 blackboard)++ "]" ++ ", " ++ "localBoardLocalDEFINE8Location2: " ++ show (localBoardLocalDEFINE8 2blackboard) ++ ", " ++ "localBoardLocalDEFINE8Location3: " ++ show (localBoardLocalDEFINE8 3blackboard) ++ ", " ++ "localBoardLocalDEFINE8Location4: " ++ show (localBoardLocalDEFINE8 4blackboard) ++ ", " ++ "localBoardLocalDEFINE8Location5: " ++ show (localBoardLocalDEFINE8 5blackboard) ++ "}"

-- START OF BLACKBOARD FUNCTIONS

boardBlDEFINE5 :: Integer -> BTreeBlackboard -> Bool
boardBlDEFINE5 0 blackboard
  | (sereneIMPLIES False False) = True
  | False = False
  | otherwise = False
boardBlDEFINE5 1 blackboard
  | (sereneIMPLIES False False) = True
  | False = False
  | otherwise = False
boardBlDEFINE5 2 blackboard
  | (sereneIMPLIES False False) = True
  | False = False
  | otherwise = False
boardBlDEFINE5 _ _ = error "boardBlDEFINE5 illegal index value"
boardBlDEFINE7 :: Integer -> BTreeBlackboard -> Bool
boardBlDEFINE7 0 blackboard
  | (((-25) == (- 49)) == (False && (boardBlDEFINE5 1 blackboard))) = (sereneXNOR (boardBlDEFINE5 1 blackboard) (boardBlDEFINE5 2 blackboard))
  | ((50 >= (boardBlVAR0 1 blackboard)) == ((boardBlVAR0 0 blackboard) < (boardBlVAR0 1 blackboard))) = (sereneIMPLIES True ((-78) >= (boardBlVAR0 0 blackboard)))
  | otherwise = ((boardBlDEFINE5 2 blackboard) == ((boardBlDEFINE5 1 blackboard) || (boardBlDEFINE5 2 blackboard)))
boardBlDEFINE7 1 blackboard
  | (True == (boardBlDEFINE5 0 blackboard)) = ((boardBlVAR0 1 blackboard) >= (abs 27))
  | (((boardBlDEFINE5 2 blackboard) == True) && (((boardBlVAR0 2 blackboard) * (8 * ((boardBlVAR0 2 blackboard) * 5))) > (boardBlVAR0 2 blackboard))) = (11 <= (boardBlVAR0 1 blackboard))
  | otherwise = (boardBlDEFINE5 1 blackboard)
boardBlDEFINE7 _ _ = error "boardBlDEFINE7 illegal index value"

-- START OF LOCAL BLACKBOARD FUNCTIONS

localBoardLocalDEFINE8 :: Integer -> BTreeBlackboard -> Integer
localBoardLocalDEFINE8 2 blackboard
  | ((sereneXOR True (boardBlDEFINE7 0 blackboard)) || False) = (min 5 (max 2 (min (min (boardBlVAR0 1 blackboard) (boardBlVAR0 0 blackboard)) 72)))
  | otherwise = (min 5 (max 2 (abs (-72))))
  where nodeLocation = 2
localBoardLocalDEFINE8 3 blackboard
  | (False == True) = (min 5 (max 2 (abs (boardBlVAR0 1 blackboard))))
  | (boardBlDEFINE7 0 blackboard) = (min 5 (max 2 ((boardBlVAR0 1 blackboard) + ((boardBlVAR0 0 blackboard) + (55 + (-97))))))
  | otherwise = (min 5 (max 2 (min 8 ((sereneCOUNT (sereneIMPLIES False (boardBlDEFINE7 0 blackboard)) ((boardBlDEFINE5 0 blackboard) && True)) + (sereneCOUNT False ((boardBlDEFINE5 1 blackboard) || False))))))
  where nodeLocation = 3
localBoardLocalDEFINE8 4 blackboard
  | ((sereneXOR True (boardBlDEFINE7 0 blackboard)) || False) = (min 5 (max 2 (min (min (boardBlVAR0 1 blackboard) (boardBlVAR0 0 blackboard)) 72)))
  | otherwise = (min 5 (max 2 (abs (-72))))
  where nodeLocation = 4
localBoardLocalDEFINE8 5 blackboard
  | (sereneXNOR (boardBlDEFINE7 1 blackboard) True) = (min 5 (max 2 (abs (boardBlVAR0 2 blackboard))))
  | (sereneXNOR (False == (sereneXOR (boardBlDEFINE7 1 blackboard) (boardBlDEFINE7 0 blackboard))) (boardBlDEFINE7 1 blackboard)) = (min 5 (max 2 (max (-49) (abs (boardBlVAR0 2 blackboard)))))
  | otherwise = (min 5 (max 2 (min (boardBlVAR0 0 blackboard) (boardBlVAR0 1 blackboard))))
  where nodeLocation = 5
localBoardLocalDEFINE8 _ _ = error "localDEFINE8 illegal local reference"

-- START OF GET FUNCTIONS FOR LOCAL VARIABLES

localBoardLocalFROZENVAR4 :: Integer -> BTreeBlackboard -> Integer
localBoardLocalFROZENVAR4 2 = localBoardLocalFROZENVAR4Location2
localBoardLocalFROZENVAR4 4 = localBoardLocalFROZENVAR4Location4
localBoardLocalFROZENVAR4 _ = error "localFROZENVAR4 illegal local reference"

-- START OF GET FUNCTIONS FOR ARRAYS

boardBlVAR0 :: Integer -> BTreeBlackboard -> Integer
boardBlVAR0 0 = boardBlVAR0Index0
boardBlVAR0 1 = boardBlVAR0Index1
boardBlVAR0 2 = boardBlVAR0Index2
boardBlVAR0 _ = error "boardBlVAR0 illegal index value"

-- START OF TYPE CHECKING FUNCTIONS

checkValueBoardBlVAR0 :: Integer -> Integer
checkValueBoardBlVAR0 value
  | (-5) > value || value > (-2) = error "boardBlVAR0 illegal value"
  | otherwise = value


-- START OF SET FUNCTIONS

updateBoardGenerator :: BTreeBlackboard -> StdGen -> BTreeBlackboard
updateBoardGenerator blackboard newGen = blackboard { sereneBoardGenerator = newGen }
updateBoardBlVAR0Index0 :: BTreeBlackboard -> Integer -> BTreeBlackboard
updateBoardBlVAR0Index0 blackboard value = blackboard { boardBlVAR0Index0 = (checkValueBoardBlVAR0 value)}
updateBoardBlVAR0Index1 :: BTreeBlackboard -> Integer -> BTreeBlackboard
updateBoardBlVAR0Index1 blackboard value = blackboard { boardBlVAR0Index1 = (checkValueBoardBlVAR0 value)}
updateBoardBlVAR0Index2 :: BTreeBlackboard -> Integer -> BTreeBlackboard
updateBoardBlVAR0Index2 blackboard value = blackboard { boardBlVAR0Index2 = (checkValueBoardBlVAR0 value)}

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
initialBlackboard seed = BTreeBlackboard newSereneGenerator newValBlVAR0Index0 newValBlVAR0Index1 newValBlVAR0Index2 localNewValLocalFROZENVAR4Location2 localNewValLocalFROZENVAR4Location4  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen5
    partialBlackboardBlVAR0Index0 = BTreeBlackboard newSereneGenerator 0 0 0 0 0
    initValBlVAR0Index0 :: StdGen -> (Integer, StdGen)
    initValBlVAR0Index0 curGen
      | (True == (((-5) * 4) > (max (-77) 5))) = ((min (-2) (max (-5) (abs (-5)))), curGen)
      | (True /= (sereneXNOR False True)) = ((min (-2) (max (-5) ((2 * ((-3) * (5 * (-43)))) - (-65)))), curGen)
      | otherwise = ((min (-2) (max (-5) (abs (sereneCOUNT (True && True) (False && True))))), curGen)
      where
        blackboard = partialBlackboardBlVAR0Index0

    (newValBlVAR0Index0, tempGen1) = initValBlVAR0Index0 tempGen0

    partialBlackboardBlVAR0Index1 = BTreeBlackboard newSereneGenerator newValBlVAR0Index0 0 0 0 0
    initValBlVAR0Index1 :: StdGen -> (Integer, StdGen)
    initValBlVAR0Index1 curGen
      | (True == (((-5) * 4) > (max (-77) 5))) = ((min (-2) (max (-5) (abs (-5)))), curGen)
      | (True /= (sereneXNOR False True)) = ((min (-2) (max (-5) ((2 * ((-3) * (5 * (-43)))) - (-65)))), curGen)
      | otherwise = ((min (-2) (max (-5) (abs (sereneCOUNT (True && True) (False && True))))), curGen)
      where
        blackboard = partialBlackboardBlVAR0Index1

    (newValBlVAR0Index1, tempGen2) = initValBlVAR0Index1 tempGen1

    partialBlackboardBlVAR0Index2 = BTreeBlackboard newSereneGenerator newValBlVAR0Index0 newValBlVAR0Index1 0 0 0
    initValBlVAR0Index2 :: StdGen -> (Integer, StdGen)
    initValBlVAR0Index2 curGen
      | (True == (((-5) * 4) > (max (-77) 5))) = ((min (-2) (max (-5) (abs (-5)))), curGen)
      | (True /= (sereneXNOR False True)) = ((min (-2) (max (-5) ((2 * ((-3) * (5 * (-43)))) - (-65)))), curGen)
      | otherwise = ((min (-2) (max (-5) (abs (sereneCOUNT (True && True) (False && True))))), curGen)
      where
        blackboard = partialBlackboardBlVAR0Index2

    (newValBlVAR0Index2, tempGen3) = initValBlVAR0Index2 tempGen2

    partialBlackboardLocalFROZENVAR4Location2 = BTreeBlackboard newSereneGenerator newValBlVAR0Index0 newValBlVAR0Index1 newValBlVAR0Index2 0 0
    localInitValLocalFROZENVAR4Location2 :: StdGen -> (Integer, StdGen)
    localInitValLocalFROZENVAR4Location2 curGen
      | ((boardBlDEFINE5 1 blackboard) || (False && (boardBlDEFINE7 0 blackboard))) = ((min 5 (max 2 (-12))), curGen)
      | (sereneXOR False False) = ((min 5 (max 2 ((-5) - (-59)))), curGen)
      | otherwise = ((min 5 (max 2 ((max (-91) (-93)) + ((boardBlVAR0 0 blackboard) + 8)))), curGen)
      where
        blackboard = partialBlackboardLocalFROZENVAR4Location2
        nodeLocation = 2

    (localNewValLocalFROZENVAR4Location2, tempGen4) = localInitValLocalFROZENVAR4Location2 tempGen3

    partialBlackboardLocalFROZENVAR4Location4 = BTreeBlackboard newSereneGenerator newValBlVAR0Index0 newValBlVAR0Index1 newValBlVAR0Index2 localNewValLocalFROZENVAR4Location2 0
    localInitValLocalFROZENVAR4Location4 :: StdGen -> (Integer, StdGen)
    localInitValLocalFROZENVAR4Location4 curGen
      | ((boardBlDEFINE5 1 blackboard) || (False && (boardBlDEFINE7 0 blackboard))) = ((min 5 (max 2 (-12))), curGen)
      | (sereneXOR False False) = ((min 5 (max 2 ((-5) - (-59)))), curGen)
      | otherwise = ((min 5 (max 2 ((max (-91) (-93)) + ((boardBlVAR0 0 blackboard) + 8)))), curGen)
      where
        blackboard = partialBlackboardLocalFROZENVAR4Location4
        nodeLocation = 4

    (localNewValLocalFROZENVAR4Location4, tempGen5) = localInitValLocalFROZENVAR4Location4 tempGen4


