module BehaviorTreeBlackboard where
import SereneRandomizer
import System.Random
import SereneOperations

data BTreeBlackboard = BTreeBlackboard {
  sereneBoardGenerator :: StdGen
  , boardBlVAR0Index0 :: String
  , boardBlVAR0Index1 :: String
  , boardBlVAR0Index2 :: String
  , localBoardLocalVAR2Location7 :: Integer
  , localBoardLocalVAR2Location1 :: Integer
  }

fromBTreeBlackboardToString :: BTreeBlackboard -> String
fromBTreeBlackboardToString blackboard = "Board = {" ++ "boardBlVAR0: " ++ "[" ++ show (boardBlVAR0 0 blackboard) ++ ", " ++ show (boardBlVAR0 1 blackboard) ++ ", " ++ show (boardBlVAR0 2 blackboard)++ "]" ++ ", " ++ "boardBlVAR0: " ++ "[" ++ show (boardBlVAR0 0 blackboard) ++ ", " ++ show (boardBlVAR0 1 blackboard) ++ ", " ++ show (boardBlVAR0 2 blackboard)++ "]" ++ ", " ++ "boardBlVAR0: " ++ "[" ++ show (boardBlVAR0 0 blackboard) ++ ", " ++ show (boardBlVAR0 1 blackboard) ++ ", " ++ show (boardBlVAR0 2 blackboard)++ "]" ++ ", " ++ "localBoardLocalVAR2Location7: " ++ show (localBoardLocalVAR2 7blackboard) ++ ", " ++ "localBoardLocalVAR2Location1: " ++ show (localBoardLocalVAR2 1blackboard) ++ ", " ++ "boardBlDEFINE5: " ++ "[" ++ show (boardBlDEFINE5 0 blackboard) ++ ", " ++ show (boardBlDEFINE5 1 blackboard)++ "]" ++ ", " ++ "localBoardLocalDEFINE3Location7: " ++ "[" ++ show (localBoardLocalDEFINE3 7 0 blackboard) ++ ", " ++ show (localBoardLocalDEFINE3 7 1 blackboard)++ "]" ++ "}"

-- START OF BLACKBOARD FUNCTIONS

boardBlDEFINE5 :: Integer -> BTreeBlackboard -> Bool
boardBlDEFINE5 0 blackboard = ((min 100 (max (-100) (min 2 (min 100 (max (-100) ((-9) + (24 + (-39)))))))) < (min 100 (max (-100) (abs 2))))
boardBlDEFINE5 1 blackboard = ((min 100 (max (-100) (min 2 (min 100 (max (-100) ((-9) + (24 + (-39)))))))) < (min 100 (max (-100) (abs 2))))
boardBlDEFINE5 _ _ = error "boardBlDEFINE5 illegal index value"

-- START OF LOCAL BLACKBOARD FUNCTIONS

localBoardLocalDEFINE3 :: Integer -> Integer -> BTreeBlackboard -> Integer
localBoardLocalDEFINE3 7 = localBoardLocalDEFINE3Location7
localBoardLocalDEFINE3 _ = error "localBoardLocalDEFINE3 illegal local reference"
localBoardLocalDEFINE3Location7 :: Integer -> BTreeBlackboard -> Integer
localBoardLocalDEFINE3Location7 0 = localBoardLocalDEFINE3Location7Index0
localBoardLocalDEFINE3Location7 1 = localBoardLocalDEFINE3Location7Index1
localBoardLocalDEFINE3Location7 _ = error "localBoardLocalDEFINE37 illegal index"
localBoardLocalDEFINE3Location7Index0 blackboard
  | ((-95) <= 2) = (min (-2) (max (-5) (min 100 (max (-100) (max (min 100 (max (-100) (- (min 100 (max (-100) (max (-13) 13)))))) (min 100 (max (-100) (min (min 100 (max (-100) (abs (-3)))) (-43)))))))))
  | otherwise = (min (-2) (max (-5) ((sereneCOUNT (sereneXNOR (sereneXOR (sereneXNOR True False) True) (2 >= (-3))) ((sereneXNOR False True) /= ((-2) <= 4))) + (sereneCOUNT False (sereneXOR True (True == (True || True)))))))
  where nodeLocation = 7
localBoardLocalDEFINE3Location7Index1 blackboard
  | (sereneXOR (False && False) False) = (min (-2) (max (-5) ((sereneCOUNT (sereneXOR ((min 100 (max (-100) (max 76 2))) >= (min 100 (max (-100) (min (-5) 2)))) (True == False)) (sereneXNOR (True || False) True)) + (sereneCOUNT ((min 100 (max (-100) (abs (-2)))) > 2) (sereneIMPLIES False (False && True))))))
  | (True || (41 >= 34)) = (min (-2) (max (-5) (-37)))
  | otherwise = (min (-2) (max (-5) (min 100 (max (-100) (3 - (-96))))))
  where nodeLocation = 7

-- START OF GET FUNCTIONS FOR LOCAL VARIABLES

localBoardLocalVAR2 :: Integer -> BTreeBlackboard -> Integer
localBoardLocalVAR2 1 = localBoardLocalVAR2Location1
localBoardLocalVAR2 7 = localBoardLocalVAR2Location7
localBoardLocalVAR2 _ = error "localVAR2 illegal local reference"

-- START OF GET FUNCTIONS FOR ARRAYS

boardBlVAR0 :: Integer -> BTreeBlackboard -> String
boardBlVAR0 0 = boardBlVAR0Index0
boardBlVAR0 1 = boardBlVAR0Index1
boardBlVAR0 2 = boardBlVAR0Index2
boardBlVAR0 _ = error "boardBlVAR0 illegal index value"

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


-- START OF SET FUNCTIONS

updateBoardGenerator :: BTreeBlackboard -> StdGen -> BTreeBlackboard
updateBoardGenerator blackboard newGen = blackboard { sereneBoardGenerator = newGen }
updateLocalBoardLocalVAR2 :: Integer -> BTreeBlackboard -> Integer -> BTreeBlackboard
updateLocalBoardLocalVAR2 1 = updateLocalBoardLocalVAR2Location1
updateLocalBoardLocalVAR2 7 = updateLocalBoardLocalVAR2Location7
updateLocalBoardLocalVAR2 _ = error "localBoardLocalVAR2 illegal local reference"
updateBoardBlVAR0Index0 :: BTreeBlackboard -> String -> BTreeBlackboard
updateBoardBlVAR0Index0 blackboard value = blackboard { boardBlVAR0Index0 = (checkValueBoardBlVAR0 value)}
updateBoardBlVAR0Index1 :: BTreeBlackboard -> String -> BTreeBlackboard
updateBoardBlVAR0Index1 blackboard value = blackboard { boardBlVAR0Index1 = (checkValueBoardBlVAR0 value)}
updateBoardBlVAR0Index2 :: BTreeBlackboard -> String -> BTreeBlackboard
updateBoardBlVAR0Index2 blackboard value = blackboard { boardBlVAR0Index2 = (checkValueBoardBlVAR0 value)}
updateLocalBoardLocalVAR2Location7 :: BTreeBlackboard -> Integer -> BTreeBlackboard
updateLocalBoardLocalVAR2Location7 blackboard value = blackboard { localBoardLocalVAR2Location7 = (checkValueLocalBoardLocalVAR2 value)}
updateLocalBoardLocalVAR2Location1 :: BTreeBlackboard -> Integer -> BTreeBlackboard
updateLocalBoardLocalVAR2Location1 blackboard value = blackboard { localBoardLocalVAR2Location1 = (checkValueLocalBoardLocalVAR2 value)}

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

-- START OF INITIAL BLACKBOARD VALUE

initialBlackboard :: Integer -> BTreeBlackboard
initialBlackboard seed = BTreeBlackboard newSereneGenerator newValBlVAR0Index0 newValBlVAR0Index1 newValBlVAR0Index2 localNewValLocalVAR2Location7 localNewValLocalVAR2Location1  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen5
    partialBlackboardBlVAR0Index0 = BTreeBlackboard newSereneGenerator " " " " " " 0 0
    initValBlVAR0Index0 :: StdGen -> (String, StdGen)
    initValBlVAR0Index0 curGen
      | ((min 100 (max (-100) (max 2 (-15)))) > (min 100 (max (-100) (min 89 (-4))))) = ("no", curGen)
      | (2 == (-100)) = ("both", curGen)
      | otherwise = ("yes", curGen)
      where
        blackboard = partialBlackboardBlVAR0Index0

    (newValBlVAR0Index0, tempGen1) = initValBlVAR0Index0 tempGen0

    partialBlackboardBlVAR0Index1 = BTreeBlackboard newSereneGenerator newValBlVAR0Index0 " " " " 0 0
    initValBlVAR0Index1 :: StdGen -> (String, StdGen)
    initValBlVAR0Index1 curGen
      | False = ("no", curGen)
      | True = ("yes", curGen)
      | otherwise = ("no", curGen)
      where
        blackboard = partialBlackboardBlVAR0Index1

    (newValBlVAR0Index1, tempGen2) = initValBlVAR0Index1 tempGen1

    partialBlackboardBlVAR0Index2 = BTreeBlackboard newSereneGenerator newValBlVAR0Index0 newValBlVAR0Index1 " " 0 0
    initValBlVAR0Index2 :: StdGen -> (String, StdGen)
    initValBlVAR0Index2 curGen
      | (2 >= 2) = ("yes", curGen)
      | otherwise = ("yes", curGen)
      where
        blackboard = partialBlackboardBlVAR0Index2

    (newValBlVAR0Index2, tempGen3) = initValBlVAR0Index2 tempGen2

    partialBlackboardLocalVAR2Location7 = BTreeBlackboard newSereneGenerator newValBlVAR0Index0 newValBlVAR0Index1 newValBlVAR0Index2 0 0
    localInitValLocalVAR2Location7 :: StdGen -> (Integer, StdGen)
    localInitValLocalVAR2Location7 curGen = ((min 5 (max 2 (min 100 (max (-100) (- (min 100 (max (-100) (max 80 10)))))))), curGen)
      where
        blackboard = partialBlackboardLocalVAR2Location7
        nodeLocation = 7

    (localNewValLocalVAR2Location7, tempGen4) = localInitValLocalVAR2Location7 tempGen3

    partialBlackboardLocalVAR2Location1 = BTreeBlackboard newSereneGenerator newValBlVAR0Index0 newValBlVAR0Index1 newValBlVAR0Index2 localNewValLocalVAR2Location7 0
    localInitValLocalVAR2Location1 :: StdGen -> (Integer, StdGen)
    localInitValLocalVAR2Location1 curGen
      | ((boardBlDEFINE5 1 blackboard) && ((-5) < 76)) = ((min 5 (max 2 (min 100 (max (-100) ((min 100 (max (-100) (60 * ((-2) * (5 * (-74)))))) + ((min 100 (max (-100) (58 * 79))) + (2 + (min 100 (max (-100) (abs 3)))))))))), curGen)
      | otherwise = ((min 5 (max 2 22)), curGen)
      where
        blackboard = partialBlackboardLocalVAR2Location1
        nodeLocation = 1

    (localNewValLocalVAR2Location1, tempGen5) = localInitValLocalVAR2Location1 tempGen4


