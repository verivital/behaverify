module BehaviorTreeBlackboard where
import SereneRandomizer
import System.Random
import SereneOperations

data BTreeBlackboard = BTreeBlackboard {
  sereneBoardGenerator :: StdGen
  , boardBlVAR0 :: Bool
  , boardBlFROZENVAR6Index0 :: String
  , boardBlFROZENVAR6Index1 :: String
  , boardBlFROZENVAR6Index2 :: String
  , localBoardLocalVAR2Location0 :: String
  }

fromBTreeBlackboardToString :: BTreeBlackboard -> String
fromBTreeBlackboardToString blackboard = "Board = {" ++ "boardBlVAR0: " ++ show (boardBlVAR0 blackboard) ++ ", " ++ "boardBlFROZENVAR6: " ++ "[" ++ show (boardBlFROZENVAR6 0 blackboard) ++ ", " ++ show (boardBlFROZENVAR6 1 blackboard) ++ ", " ++ show (boardBlFROZENVAR6 2 blackboard)++ "]" ++ ", " ++ "boardBlFROZENVAR6: " ++ "[" ++ show (boardBlFROZENVAR6 0 blackboard) ++ ", " ++ show (boardBlFROZENVAR6 1 blackboard) ++ ", " ++ show (boardBlFROZENVAR6 2 blackboard)++ "]" ++ ", " ++ "boardBlFROZENVAR6: " ++ "[" ++ show (boardBlFROZENVAR6 0 blackboard) ++ ", " ++ show (boardBlFROZENVAR6 1 blackboard) ++ ", " ++ show (boardBlFROZENVAR6 2 blackboard)++ "]" ++ ", " ++ "localBoardLocalVAR2Location0: " ++ show (localBoardLocalVAR2 0blackboard) ++ ", " ++ "boardBlDEFINE8: " ++ show (boardBlDEFINE8 blackboard) ++ ", " ++ "localBoardLocalDEFINE7Location0: " ++ "[" ++ show (localBoardLocalDEFINE7 0 0 blackboard) ++ ", " ++ show (localBoardLocalDEFINE7 0 1 blackboard) ++ ", " ++ show (localBoardLocalDEFINE7 0 2 blackboard)++ "]" ++ ", " ++ "localBoardLocalDEFINE10Location0: " ++ show (localBoardLocalDEFINE10 0blackboard) ++ "}"

-- START OF BLACKBOARD FUNCTIONS

boardBlDEFINE8 :: BTreeBlackboard -> String
boardBlDEFINE8 blackboard = (boardBlFROZENVAR6 0 blackboard)

-- START OF LOCAL BLACKBOARD FUNCTIONS

localBoardLocalDEFINE10 :: Integer -> BTreeBlackboard -> Integer
localBoardLocalDEFINE10 0 blackboard
  | (False && True) = (min (-2) (max (-5) (min ((-3) - (-54)) (-5))))
  | (sereneIMPLIES (boardBlVAR0 blackboard) False) = (min (-2) (max (-5) ((-2) * ((-31) * (4 * 69)))))
  | otherwise = (min (-2) (max (-5) ((-2) + ((max 46 39) + (((sereneCOUNT ((boardBlVAR0 blackboard) && (boardBlVAR0 blackboard)) (sereneIMPLIES True False)) + (sereneCOUNT ((boardBlVAR0 blackboard) == (boardBlVAR0 blackboard)) (sereneXNOR True (boardBlVAR0 blackboard)))) + (abs 99))))))
  where nodeLocation = 0
localBoardLocalDEFINE10 _ _ = error "localDEFINE10 illegal local reference"
localBoardLocalDEFINE7 :: Integer -> Integer -> BTreeBlackboard -> Integer
localBoardLocalDEFINE7 0 = localBoardLocalDEFINE7Location0
localBoardLocalDEFINE7 _ = error "localBoardLocalDEFINE7 illegal local reference"
localBoardLocalDEFINE7Location0 :: Integer -> BTreeBlackboard -> Integer
localBoardLocalDEFINE7Location0 0 = localBoardLocalDEFINE7Location0Index0
localBoardLocalDEFINE7Location0 1 = localBoardLocalDEFINE7Location0Index1
localBoardLocalDEFINE7Location0 2 = localBoardLocalDEFINE7Location0Index2
localBoardLocalDEFINE7Location0 _ = error "localBoardLocalDEFINE70 illegal index"
localBoardLocalDEFINE7Location0Index0 blackboard
  | ("yes" == "yes") = (min (-2) (max (-5) (-2)))
  | ((boardBlVAR0 blackboard) && ((-3) >= 83)) = (min (-2) (max (-5) ((sereneCOUNT (5 <= 3) (sereneXOR (boardBlVAR0 blackboard) False)) + (sereneCOUNT ((-5) > (-42)) (True || (boardBlVAR0 blackboard))))))
  | otherwise = (min (-2) (max (-5) (max 22 ((-4) - (-9)))))
  where nodeLocation = 0
localBoardLocalDEFINE7Location0Index1 blackboard
  | ("yes" == "yes") = (min (-2) (max (-5) (-2)))
  | ((boardBlVAR0 blackboard) && ((-3) >= 83)) = (min (-2) (max (-5) ((sereneCOUNT (5 <= 3) (sereneXOR (boardBlVAR0 blackboard) False)) + (sereneCOUNT ((-5) > (-42)) (True || (boardBlVAR0 blackboard))))))
  | otherwise = (min (-2) (max (-5) (max 22 ((-4) - (-9)))))
  where nodeLocation = 0
localBoardLocalDEFINE7Location0Index2 blackboard
  | ("yes" == "yes") = (min (-2) (max (-5) (-2)))
  | ((boardBlVAR0 blackboard) && ((-3) >= 83)) = (min (-2) (max (-5) ((sereneCOUNT (5 <= 3) (sereneXOR (boardBlVAR0 blackboard) False)) + (sereneCOUNT ((-5) > (-42)) (True || (boardBlVAR0 blackboard))))))
  | otherwise = (min (-2) (max (-5) (max 22 ((-4) - (-9)))))
  where nodeLocation = 0

-- START OF GET FUNCTIONS FOR LOCAL VARIABLES

localBoardLocalVAR2 :: Integer -> BTreeBlackboard -> String
localBoardLocalVAR2 0 = localBoardLocalVAR2Location0
localBoardLocalVAR2 _ = error "localVAR2 illegal local reference"

-- START OF GET FUNCTIONS FOR ARRAYS

boardBlFROZENVAR6 :: Integer -> BTreeBlackboard -> String
boardBlFROZENVAR6 0 = boardBlFROZENVAR6Index0
boardBlFROZENVAR6 1 = boardBlFROZENVAR6Index1
boardBlFROZENVAR6 2 = boardBlFROZENVAR6Index2
boardBlFROZENVAR6 _ = error "boardBlFROZENVAR6 illegal index value"

-- START OF TYPE CHECKING FUNCTIONS

checkValueBoardBlVAR0 :: Bool -> Bool
checkValueBoardBlVAR0 value = value

checkValueLocalBoardLocalVAR2 :: String -> String
checkValueLocalBoardLocalVAR2 "yes" = "yes"
checkValueLocalBoardLocalVAR2 "no" = "no"
checkValueLocalBoardLocalVAR2 "both" = "both"
checkValueLocalBoardLocalVAR2 _ = error "localBoardLocalVAR2 illegal value"

checkValueLocalBoardLocalVAR4 :: Bool -> Bool
checkValueLocalBoardLocalVAR4 value = value


-- START OF SET FUNCTIONS

updateBoardGenerator :: BTreeBlackboard -> StdGen -> BTreeBlackboard
updateBoardGenerator blackboard newGen = blackboard { sereneBoardGenerator = newGen }
updateLocalBoardLocalVAR2 :: Integer -> BTreeBlackboard -> String -> BTreeBlackboard
updateLocalBoardLocalVAR2 0 = updateLocalBoardLocalVAR2Location0
updateLocalBoardLocalVAR2 _ = error "localBoardLocalVAR2 illegal local reference"
updateBoardBlVAR0 :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateBoardBlVAR0 blackboard value = blackboard { boardBlVAR0 = (checkValueBoardBlVAR0 value)}
updateLocalBoardLocalVAR2Location0 :: BTreeBlackboard -> String -> BTreeBlackboard
updateLocalBoardLocalVAR2Location0 blackboard value = blackboard { localBoardLocalVAR2Location0 = (checkValueLocalBoardLocalVAR2 value)}

-- START OF SET FUNCTIONS FOR ARRAYS


-- START OF INITIAL BLACKBOARD VALUE

initialBlackboard :: Integer -> BTreeBlackboard
initialBlackboard seed = BTreeBlackboard newSereneGenerator newValBlVAR0 newValBlFROZENVAR6Index0 newValBlFROZENVAR6Index1 newValBlFROZENVAR6Index2 localNewValLocalVAR2Location0  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen5
    partialBlackboardBlVAR0 = BTreeBlackboard newSereneGenerator True " " " " " " " "
    initValBlVAR0 :: StdGen -> (Bool, StdGen)
    initValBlVAR0 curGen
      | False = (((-3) < 2), curGen)
      | ((23 - 49) > 3) = (((True && True) || False), curGen)
      | otherwise = ((44 == (-2)), curGen)
      where
        blackboard = partialBlackboardBlVAR0

    (newValBlVAR0, tempGen1) = initValBlVAR0 tempGen0

    partialBlackboardBlFROZENVAR6Index0 = BTreeBlackboard newSereneGenerator newValBlVAR0 " " " " " " " "
    initValBlFROZENVAR6Index0 :: StdGen -> (String, StdGen)
    initValBlFROZENVAR6Index0 curGen
      | ((22 * (13 * 62)) <= ((abs 4) - (-84))) = ("yes", curGen)
      | otherwise = ("yes", curGen)
      where
        blackboard = partialBlackboardBlFROZENVAR6Index0

    (newValBlFROZENVAR6Index0, tempGen2) = initValBlFROZENVAR6Index0 tempGen1

    partialBlackboardBlFROZENVAR6Index1 = BTreeBlackboard newSereneGenerator newValBlVAR0 newValBlFROZENVAR6Index0 " " " " " "
    initValBlFROZENVAR6Index1 :: StdGen -> (String, StdGen)
    initValBlFROZENVAR6Index1 curGen = ("yes", curGen)
      where
        blackboard = partialBlackboardBlFROZENVAR6Index1

    (newValBlFROZENVAR6Index1, tempGen3) = initValBlFROZENVAR6Index1 tempGen2

    partialBlackboardBlFROZENVAR6Index2 = BTreeBlackboard newSereneGenerator newValBlVAR0 newValBlFROZENVAR6Index0 newValBlFROZENVAR6Index1 " " " "
    initValBlFROZENVAR6Index2 :: StdGen -> (String, StdGen)
    initValBlFROZENVAR6Index2 curGen
      | (("both" /= "both") /= (sereneIMPLIES (True && False) (False /= False))) = ("both", curGen)
      | (((5 + (66 + (3 + (-5)))) <= ((-5) + (5 + (18 + 32)))) && ((sereneXNOR newValBlVAR0 True) == ((-5) <= (-22)))) = ("yes", curGen)
      | otherwise = ("yes", curGen)
      where
        blackboard = partialBlackboardBlFROZENVAR6Index2

    (newValBlFROZENVAR6Index2, tempGen4) = initValBlFROZENVAR6Index2 tempGen3

    partialBlackboardLocalVAR2Location0 = BTreeBlackboard newSereneGenerator newValBlVAR0 newValBlFROZENVAR6Index0 newValBlFROZENVAR6Index1 newValBlFROZENVAR6Index2 " "
    localInitValLocalVAR2Location0 :: StdGen -> (String, StdGen)
    localInitValLocalVAR2Location0 curGen
      | (True == ((-46) <= 4)) = ("no", curGen)
      | otherwise = ("yes", curGen)
      where
        blackboard = partialBlackboardLocalVAR2Location0
        nodeLocation = 0

    (localNewValLocalVAR2Location0, tempGen5) = localInitValLocalVAR2Location0 tempGen4


