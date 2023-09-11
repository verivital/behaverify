module BehaviorTreeBlackboard where
import SereneRandomizer
import System.Random
import SereneOperations

data BTreeBlackboard = BTreeBlackboard {
  sereneBoardGenerator :: StdGen
  , boardBlVAR0 :: Integer
  , boardBlVAR2 :: String
  , boardBlVAR3Index0 :: String
  , boardBlVAR3Index1 :: String
  }

fromBTreeBlackboardToString :: BTreeBlackboard -> String
fromBTreeBlackboardToString blackboard = "Board = {" ++ "boardBlVAR0: " ++ show (boardBlVAR0 blackboard) ++ ", " ++ "boardBlVAR2: " ++ show (boardBlVAR2 blackboard) ++ ", " ++ "boardBlVAR3: " ++ "[" ++ show (boardBlVAR3 0 blackboard) ++ ", " ++ show (boardBlVAR3 1 blackboard)++ "]" ++ ", " ++ "boardBlVAR3: " ++ "[" ++ show (boardBlVAR3 0 blackboard) ++ ", " ++ show (boardBlVAR3 1 blackboard)++ "]" ++ "}"

-- START OF BLACKBOARD FUNCTIONS


-- START OF LOCAL BLACKBOARD FUNCTIONS


-- START OF GET FUNCTIONS FOR LOCAL VARIABLES


-- START OF GET FUNCTIONS FOR ARRAYS

boardBlVAR3 :: Integer -> BTreeBlackboard -> String
boardBlVAR3 0 = boardBlVAR3Index0
boardBlVAR3 1 = boardBlVAR3Index1
boardBlVAR3 _ = error "boardBlVAR3 illegal index value"

-- START OF TYPE CHECKING FUNCTIONS

checkValueBoardBlVAR0 :: Integer -> Integer
checkValueBoardBlVAR0 value
  | (-5) > value || value > (-2) = error "boardBlVAR0 illegal value"
  | otherwise = value

checkValueBoardBlVAR2 :: String -> String
checkValueBoardBlVAR2 "yes" = "yes"
checkValueBoardBlVAR2 "no" = "no"
checkValueBoardBlVAR2 "both" = "both"
checkValueBoardBlVAR2 _ = error "boardBlVAR2 illegal value"

checkValueBoardBlVAR3 :: String -> String
checkValueBoardBlVAR3 "yes" = "yes"
checkValueBoardBlVAR3 "no" = "no"
checkValueBoardBlVAR3 "both" = "both"
checkValueBoardBlVAR3 _ = error "boardBlVAR3 illegal value"

checkValueLocalBoardLocalVAR4 :: Bool -> Bool
checkValueLocalBoardLocalVAR4 value = value


-- START OF SET FUNCTIONS

updateBoardGenerator :: BTreeBlackboard -> StdGen -> BTreeBlackboard
updateBoardGenerator blackboard newGen = blackboard { sereneBoardGenerator = newGen }
updateBoardBlVAR0 :: BTreeBlackboard -> Integer -> BTreeBlackboard
updateBoardBlVAR0 blackboard value = blackboard { boardBlVAR0 = (checkValueBoardBlVAR0 value)}
updateBoardBlVAR2 :: BTreeBlackboard -> String -> BTreeBlackboard
updateBoardBlVAR2 blackboard value = blackboard { boardBlVAR2 = (checkValueBoardBlVAR2 value)}
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
initialBlackboard seed = BTreeBlackboard newSereneGenerator newValBlVAR0 newValBlVAR2 newValBlVAR3Index0 newValBlVAR3Index1  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen4
    partialBlackboardBlVAR0 = BTreeBlackboard newSereneGenerator 0 " " " " " "
    initValBlVAR0 :: StdGen -> (Integer, StdGen)
    initValBlVAR0 curGen
      | (sereneXNOR False ((14 <= (-3)) /= (31 >= 24))) = ((min (-2) (max (-5) 97)), curGen)
      | otherwise = ((min (-2) (max (-5) (min 100 (max (-100) (3 + (3 + (88 + (-14)))))))), curGen)
      where
        blackboard = partialBlackboardBlVAR0

    (newValBlVAR0, tempGen1) = initValBlVAR0 tempGen0

    partialBlackboardBlVAR2 = BTreeBlackboard newSereneGenerator newValBlVAR0 " " " " " "
    initValBlVAR2 :: StdGen -> (String, StdGen)
    initValBlVAR2 curGen
      | (False && ((min 100 (max (-100) (min 51 newValBlVAR0))) > newValBlVAR0)) = ("yes", curGen)
      | (newValBlVAR0 < newValBlVAR0) = ("no", curGen)
      | otherwise = ("no", curGen)
      where
        blackboard = partialBlackboardBlVAR2

    (newValBlVAR2, tempGen2) = initValBlVAR2 tempGen1

    partialBlackboardBlVAR3Index0 = BTreeBlackboard newSereneGenerator newValBlVAR0 newValBlVAR2 " " " "
    initValBlVAR3Index0 :: StdGen -> (String, StdGen)
    initValBlVAR3Index0 curGen = ("both", curGen)
      where
        blackboard = partialBlackboardBlVAR3Index0

    (newValBlVAR3Index0, tempGen3) = initValBlVAR3Index0 tempGen2

    partialBlackboardBlVAR3Index1 = BTreeBlackboard newSereneGenerator newValBlVAR0 newValBlVAR2 newValBlVAR3Index0 " "
    initValBlVAR3Index1 :: StdGen -> (String, StdGen)
    initValBlVAR3Index1 curGen = ("both", curGen)
      where
        blackboard = partialBlackboardBlVAR3Index1

    (newValBlVAR3Index1, tempGen4) = initValBlVAR3Index1 tempGen3


