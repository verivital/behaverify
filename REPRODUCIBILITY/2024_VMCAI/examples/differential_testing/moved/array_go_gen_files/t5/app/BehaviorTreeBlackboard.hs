module BehaviorTreeBlackboard where
import SereneRandomizer
import System.Random
import SereneOperations

data BTreeBlackboard = BTreeBlackboard {
  sereneBoardGenerator :: StdGen
  , boardBlVAR0 :: String
  , boardBlFROZENVAR4Index0 :: Integer
  , boardBlFROZENVAR4Index1 :: Integer
  , localBoardLocalVAR2Location3 :: Integer
  , localBoardLocalVAR2Location2 :: Integer
  }

fromBTreeBlackboardToString :: BTreeBlackboard -> String
fromBTreeBlackboardToString blackboard = "Board = {" ++ "boardBlVAR0: " ++ show (boardBlVAR0 blackboard) ++ ", " ++ "boardBlFROZENVAR4: " ++ "[" ++ show (boardBlFROZENVAR4 0 blackboard) ++ ", " ++ show (boardBlFROZENVAR4 1 blackboard)++ "]" ++ ", " ++ "boardBlFROZENVAR4: " ++ "[" ++ show (boardBlFROZENVAR4 0 blackboard) ++ ", " ++ show (boardBlFROZENVAR4 1 blackboard)++ "]" ++ ", " ++ "localBoardLocalVAR2Location3: " ++ show (localBoardLocalVAR2 3blackboard) ++ ", " ++ "localBoardLocalVAR2Location2: " ++ show (localBoardLocalVAR2 2blackboard) ++ ", " ++ "boardBlDEFINE6: " ++ show (boardBlDEFINE6 blackboard) ++ "}"

-- START OF BLACKBOARD FUNCTIONS

boardBlDEFINE6 :: BTreeBlackboard -> Integer
boardBlDEFINE6 blackboard
  | (((-92) + (-26)) >= 96) = (min 5 (max 2 (- (-14))))
  | otherwise = (min 5 (max 2 (65 + ((boardBlFROZENVAR4 1 blackboard) + (0 + 92)))))

-- START OF LOCAL BLACKBOARD FUNCTIONS


-- START OF GET FUNCTIONS FOR LOCAL VARIABLES

localBoardLocalVAR2 :: Integer -> BTreeBlackboard -> Integer
localBoardLocalVAR2 2 = localBoardLocalVAR2Location2
localBoardLocalVAR2 3 = localBoardLocalVAR2Location3
localBoardLocalVAR2 _ = error "localVAR2 illegal local reference"

-- START OF GET FUNCTIONS FOR ARRAYS

boardBlFROZENVAR4 :: Integer -> BTreeBlackboard -> Integer
boardBlFROZENVAR4 0 = boardBlFROZENVAR4Index0
boardBlFROZENVAR4 1 = boardBlFROZENVAR4Index1
boardBlFROZENVAR4 _ = error "boardBlFROZENVAR4 illegal index value"

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

checkValueLocalBoardLocalVAR3 :: Integer -> Integer
checkValueLocalBoardLocalVAR3 value
  | 2 > value || value > 5 = error "localBoardLocalVAR3 illegal value"
  | otherwise = value


-- START OF SET FUNCTIONS

updateBoardGenerator :: BTreeBlackboard -> StdGen -> BTreeBlackboard
updateBoardGenerator blackboard newGen = blackboard { sereneBoardGenerator = newGen }
updateLocalBoardLocalVAR2 :: Integer -> BTreeBlackboard -> Integer -> BTreeBlackboard
updateLocalBoardLocalVAR2 2 = updateLocalBoardLocalVAR2Location2
updateLocalBoardLocalVAR2 3 = updateLocalBoardLocalVAR2Location3
updateLocalBoardLocalVAR2 _ = error "localBoardLocalVAR2 illegal local reference"
updateBoardBlVAR0 :: BTreeBlackboard -> String -> BTreeBlackboard
updateBoardBlVAR0 blackboard value = blackboard { boardBlVAR0 = (checkValueBoardBlVAR0 value)}
updateLocalBoardLocalVAR2Location3 :: BTreeBlackboard -> Integer -> BTreeBlackboard
updateLocalBoardLocalVAR2Location3 blackboard value = blackboard { localBoardLocalVAR2Location3 = (checkValueLocalBoardLocalVAR2 value)}
updateLocalBoardLocalVAR2Location2 :: BTreeBlackboard -> Integer -> BTreeBlackboard
updateLocalBoardLocalVAR2Location2 blackboard value = blackboard { localBoardLocalVAR2Location2 = (checkValueLocalBoardLocalVAR2 value)}

-- START OF SET FUNCTIONS FOR ARRAYS


-- START OF INITIAL BLACKBOARD VALUE

initialBlackboard :: Integer -> BTreeBlackboard
initialBlackboard seed = BTreeBlackboard newSereneGenerator newValBlVAR0 newValBlFROZENVAR4Index0 newValBlFROZENVAR4Index1 localNewValLocalVAR2Location3 localNewValLocalVAR2Location2  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen5
    partialBlackboardBlVAR0 = BTreeBlackboard newSereneGenerator " " 0 0 0 0
    initValBlVAR0 :: StdGen -> (String, StdGen)
    initValBlVAR0 curGen
      | ((2 + ((-13) + ((-18) + (-48)))) >= (-64)) = ("no", curGen)
      | otherwise = ("no", curGen)
      where
        blackboard = partialBlackboardBlVAR0

    (newValBlVAR0, tempGen1) = initValBlVAR0 tempGen0

    partialBlackboardBlFROZENVAR4Index0 = BTreeBlackboard newSereneGenerator newValBlVAR0 0 0 0 0
    initValBlFROZENVAR4Index0 :: StdGen -> (Integer, StdGen)
    initValBlFROZENVAR4Index0 curGen
      | False = ((min 5 (max 2 ((max (- 2) (-66)) * (5 - 3)))), curGen)
      | ((4 > (-59)) /= False) = ((min 5 (max 2 (min (- (abs 88)) (sereneCOUNT (77 <= 5) (False && True))))), curGen)
      | otherwise = ((min 5 (max 2 (abs 2))), curGen)
      where
        blackboard = partialBlackboardBlFROZENVAR4Index0

    (newValBlFROZENVAR4Index0, tempGen2) = initValBlFROZENVAR4Index0 tempGen1

    partialBlackboardBlFROZENVAR4Index1 = BTreeBlackboard newSereneGenerator newValBlVAR0 newValBlFROZENVAR4Index0 0 0 0
    initValBlFROZENVAR4Index1 :: StdGen -> (Integer, StdGen)
    initValBlFROZENVAR4Index1 curGen
      | (3 <= (-5)) = ((min 5 (max 2 ((sereneCOUNT (((abs 2) * (-22)) >= (75 - (sereneCOUNT ("yes" == newValBlVAR0) (32 <= 3)))) (sereneXNOR ((-5) <= (sereneCOUNT (True /= True) (False == False))) False)) + (sereneCOUNT False ((sereneXNOR True (4 >= (-40))) == True))))), curGen)
      | (((-4) /= 2) /= False) = ((min 5 (max 2 (- 2))), curGen)
      | otherwise = ((min 5 (max 2 ((2 + (5 + (4 + (-2)))) - (-2)))), curGen)
      where
        blackboard = partialBlackboardBlFROZENVAR4Index1

    (newValBlFROZENVAR4Index1, tempGen3) = initValBlFROZENVAR4Index1 tempGen2

    partialBlackboardLocalVAR2Location3 = BTreeBlackboard newSereneGenerator newValBlVAR0 newValBlFROZENVAR4Index0 newValBlFROZENVAR4Index1 0 0
    localInitValLocalVAR2Location3 :: StdGen -> (Integer, StdGen)
    localInitValLocalVAR2Location3 curGen = ((min 5 (max 2 (max 78 (-76)))), curGen)
      where
        blackboard = partialBlackboardLocalVAR2Location3
        nodeLocation = 3

    (localNewValLocalVAR2Location3, tempGen4) = localInitValLocalVAR2Location3 tempGen3

    partialBlackboardLocalVAR2Location2 = BTreeBlackboard newSereneGenerator newValBlVAR0 newValBlFROZENVAR4Index0 newValBlFROZENVAR4Index1 localNewValLocalVAR2Location3 0
    localInitValLocalVAR2Location2 :: StdGen -> (Integer, StdGen)
    localInitValLocalVAR2Location2 curGen = ((min 5 (max 2 (min (abs (boardBlDEFINE6 blackboard)) (boardBlFROZENVAR4 1 blackboard)))), curGen)
      where
        blackboard = partialBlackboardLocalVAR2Location2
        nodeLocation = 2

    (localNewValLocalVAR2Location2, tempGen5) = localInitValLocalVAR2Location2 tempGen4


