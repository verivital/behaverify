module BehaviorTreeBlackboard where
import SereneRandomizer
import System.Random
import SereneOperations

data BTreeBlackboard = BTreeBlackboard {
  sereneBoardGenerator :: StdGen
  , boardBlVAR0 :: Integer
  , boardBlVAR3Index0 :: String
  , boardBlVAR3Index1 :: String
  }

fromBTreeBlackboardToString :: BTreeBlackboard -> String
fromBTreeBlackboardToString blackboard = "Board = {" ++ "boardBlVAR0: " ++ show (boardBlVAR0 blackboard) ++ ", " ++ "boardBlVAR3: " ++ "[" ++ show (boardBlVAR3 0 blackboard) ++ ", " ++ show (boardBlVAR3 1 blackboard)++ "]" ++ ", " ++ "boardBlVAR3: " ++ "[" ++ show (boardBlVAR3 0 blackboard) ++ ", " ++ show (boardBlVAR3 1 blackboard)++ "]" ++ ", " ++ "boardBlDEFINE5: " ++ show (boardBlDEFINE5 blackboard) ++ ", " ++ "localBoardLocalDEFINE7Location1: " ++ show (localBoardLocalDEFINE7 1blackboard) ++ ", " ++ "localBoardLocalDEFINE6Location3: " ++ "[" ++ show (localBoardLocalDEFINE6 3 0 blackboard) ++ ", " ++ show (localBoardLocalDEFINE6 3 1 blackboard) ++ ", " ++ show (localBoardLocalDEFINE6 3 2 blackboard)++ "]" ++ "}"

-- START OF BLACKBOARD FUNCTIONS

boardBlDEFINE5 :: BTreeBlackboard -> String
boardBlDEFINE5 blackboard
  | False = "yes"
  | ((boardBlVAR0 blackboard) < (boardBlVAR0 blackboard)) = "both"
  | otherwise = (boardBlVAR3 0 blackboard)

-- START OF LOCAL BLACKBOARD FUNCTIONS

localBoardLocalDEFINE7 :: Integer -> BTreeBlackboard -> Integer
localBoardLocalDEFINE7 1 blackboard
  | True = (min 5 (max 2 ((sereneCOUNT ((19 < (boardBlVAR0 blackboard)) == (True && True)) (sereneXOR False ((boardBlVAR0 blackboard) /= 60))) + (sereneCOUNT False ((abs ((sereneCOUNT ((boardBlVAR3 0 blackboard) /= "both") (sereneXOR False False)) + (sereneCOUNT (True && False) (False && True)))) <= ((boardBlVAR0 blackboard) * ((-39) * (boardBlVAR0 blackboard))))))))
  | ((-59) < (min 72 (max (-23) (boardBlVAR0 blackboard)))) = (min 5 (max 2 24))
  | otherwise = (min 5 (max 2 ((sereneCOUNT ((-6) <= (boardBlVAR0 blackboard)) ((boardBlVAR0 blackboard) == (-36))) + (sereneCOUNT False (sereneXOR False ((boardBlVAR3 1 blackboard) == (boardBlVAR3 0 blackboard)))))))
  where nodeLocation = 1
localBoardLocalDEFINE7 _ _ = error "localDEFINE7 illegal local reference"
localBoardLocalDEFINE6 :: Integer -> Integer -> BTreeBlackboard -> Integer
localBoardLocalDEFINE6 3 = localBoardLocalDEFINE6Location3
localBoardLocalDEFINE6 _ = error "localBoardLocalDEFINE6 illegal local reference"
localBoardLocalDEFINE6Location3 :: Integer -> BTreeBlackboard -> Integer
localBoardLocalDEFINE6Location3 0 = localBoardLocalDEFINE6Location3Index0
localBoardLocalDEFINE6Location3 1 = localBoardLocalDEFINE6Location3Index1
localBoardLocalDEFINE6Location3 2 = localBoardLocalDEFINE6Location3Index2
localBoardLocalDEFINE6Location3 _ = error "localBoardLocalDEFINE63 illegal index"
localBoardLocalDEFINE6Location3Index0 blackboard = (min (-2) (max (-5) (min 40 (boardBlVAR0 blackboard))))
  where nodeLocation = 3
localBoardLocalDEFINE6Location3Index1 blackboard = (min (-2) (max (-5) (-17)))
  where nodeLocation = 3
localBoardLocalDEFINE6Location3Index2 blackboard = (min (-2) (max (-5) (min (max (-96) (boardBlVAR0 blackboard)) (max 78 (boardBlVAR0 blackboard)))))
  where nodeLocation = 3

-- START OF GET FUNCTIONS FOR LOCAL VARIABLES


-- START OF GET FUNCTIONS FOR ARRAYS

boardBlVAR3 :: Integer -> BTreeBlackboard -> String
boardBlVAR3 0 = boardBlVAR3Index0
boardBlVAR3 1 = boardBlVAR3Index1
boardBlVAR3 _ = error "boardBlVAR3 illegal index value"

-- START OF TYPE CHECKING FUNCTIONS

checkValueBoardBlVAR0 :: Integer -> Integer
checkValueBoardBlVAR0 value
  | 2 > value || value > 5 = error "boardBlVAR0 illegal value"
  | otherwise = value

checkValueBoardBlVAR3 :: String -> String
checkValueBoardBlVAR3 "yes" = "yes"
checkValueBoardBlVAR3 "no" = "no"
checkValueBoardBlVAR3 "both" = "both"
checkValueBoardBlVAR3 _ = error "boardBlVAR3 illegal value"


-- START OF SET FUNCTIONS

updateBoardGenerator :: BTreeBlackboard -> StdGen -> BTreeBlackboard
updateBoardGenerator blackboard newGen = blackboard { sereneBoardGenerator = newGen }
updateBoardBlVAR0 :: BTreeBlackboard -> Integer -> BTreeBlackboard
updateBoardBlVAR0 blackboard value = blackboard { boardBlVAR0 = (checkValueBoardBlVAR0 value)}
updateBoardBlVAR3Index0 :: BTreeBlackboard -> String -> BTreeBlackboard
updateBoardBlVAR3Index0 blackboard value = blackboard { boardBlVAR3Index0 = (checkValueBoardBlVAR3 value)}
updateBoardBlVAR3Index1 :: BTreeBlackboard -> String -> BTreeBlackboard
updateBoardBlVAR3Index1 blackboard value = blackboard { boardBlVAR3Index1 = (checkValueBoardBlVAR3 value)}

-- START OF SET FUNCTIONS FOR ARRAYS

updateBoardBlVAR3 :: Integer -> BTreeBlackboard -> String -> BTreeBlackboard
updateBoardBlVAR3 0 = updateBoardBlVAR3Index0
updateBoardBlVAR3 1 = updateBoardBlVAR3Index1
updateBoardBlVAR3 _ = error "BoardBlVAR3 illegal index value"
arrayUpdateBoardBlVAR3 :: BTreeBlackboard -> [(Integer, String)] -> BTreeBlackboard
arrayUpdateBoardBlVAR3 blackboard []  = blackboard
arrayUpdateBoardBlVAR3 blackboard [(index, value)] = updateBoardBlVAR3 index blackboard value
arrayUpdateBoardBlVAR3 blackboard indicesValues = blackboard {
  boardBlVAR3Index0 = newBlVAR3Index0
  , boardBlVAR3Index1 = newBlVAR3Index1
  }
    where
      (newBlVAR3Index0, newBlVAR3Index1) = updateValues indicesValues
      updateValues :: [(Integer, String)] -> (String, String)
      updateValues [] = (boardBlVAR3Index0 blackboard, boardBlVAR3Index1 blackboard)
      updateValues ((0, currentValue) : nextIndicesValues) = (checkValueBoardBlVAR3 currentValue, updatedValue1)
        where
          (_, updatedValue1) = updateValues nextIndicesValues
      updateValues ((1, currentValue) : nextIndicesValues) = (updatedValue0, checkValueBoardBlVAR3 currentValue)
        where
          (updatedValue0, _) = updateValues nextIndicesValues

-- START OF INITIAL BLACKBOARD VALUE

initialBlackboard :: Integer -> BTreeBlackboard
initialBlackboard seed = BTreeBlackboard newSereneGenerator newValBlVAR0 newValBlVAR3Index0 newValBlVAR3Index1  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen3
    partialBlackboardBlVAR0 = BTreeBlackboard newSereneGenerator 0 " " " "
    initValBlVAR0 :: StdGen -> (Integer, StdGen)
    initValBlVAR0 curGen
      | (False || True) = ((min 5 (max 2 4)), curGen)
      | otherwise = ((min 5 (max 2 ((-44) * ((-2) * 89)))), curGen)
      where
        blackboard = partialBlackboardBlVAR0

    (newValBlVAR0, tempGen1) = initValBlVAR0 tempGen0

    partialBlackboardBlVAR3Index0 = BTreeBlackboard newSereneGenerator newValBlVAR0 " " " "
    initValBlVAR3Index0 :: StdGen -> (String, StdGen)
    initValBlVAR3Index0 curGen
      | ((abs (-92)) /= newValBlVAR0) = ("yes", curGen)
      | ("both" /= "yes") = ("both", curGen)
      | otherwise = ("yes", curGen)
      where
        blackboard = partialBlackboardBlVAR3Index0

    (newValBlVAR3Index0, tempGen2) = initValBlVAR3Index0 tempGen1

    partialBlackboardBlVAR3Index1 = BTreeBlackboard newSereneGenerator newValBlVAR0 newValBlVAR3Index0 " "
    initValBlVAR3Index1 :: StdGen -> (String, StdGen)
    initValBlVAR3Index1 curGen = ("no", curGen)
      where
        blackboard = partialBlackboardBlVAR3Index1

    (newValBlVAR3Index1, tempGen3) = initValBlVAR3Index1 tempGen2


