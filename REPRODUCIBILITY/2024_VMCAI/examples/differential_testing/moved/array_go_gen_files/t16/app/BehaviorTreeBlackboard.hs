module BehaviorTreeBlackboard where
import SereneRandomizer
import System.Random
import SereneOperations

data BTreeBlackboard = BTreeBlackboard {
  sereneBoardGenerator :: StdGen
  , boardBlVAR0 :: Integer
  , boardBlVAR3 :: Integer
  , localBoardLocalVAR4Location1 :: Bool
  }

fromBTreeBlackboardToString :: BTreeBlackboard -> String
fromBTreeBlackboardToString blackboard = "Board = {" ++ "boardBlVAR0: " ++ show (boardBlVAR0 blackboard) ++ ", " ++ "boardBlVAR3: " ++ show (boardBlVAR3 blackboard) ++ ", " ++ "localBoardLocalVAR4Location1: " ++ show (localBoardLocalVAR4 1blackboard) ++ ", " ++ "boardBlDEFINE7: " ++ "[" ++ show (boardBlDEFINE7 0 blackboard) ++ ", " ++ show (boardBlDEFINE7 1 blackboard) ++ ", " ++ show (boardBlDEFINE7 2 blackboard)++ "]" ++ ", " ++ "localBoardLocalDEFINE8Location1: " ++ show (localBoardLocalDEFINE8 1blackboard) ++ ", " ++ "localBoardLocalDEFINE10Location1: " ++ show (localBoardLocalDEFINE10 1blackboard) ++ "}"

-- START OF BLACKBOARD FUNCTIONS

boardBlDEFINE7 :: Integer -> BTreeBlackboard -> Bool
boardBlDEFINE7 0 blackboard = True
boardBlDEFINE7 1 blackboard = True
boardBlDEFINE7 2 blackboard = True
boardBlDEFINE7 _ _ = error "boardBlDEFINE7 illegal index value"

-- START OF LOCAL BLACKBOARD FUNCTIONS

localBoardLocalDEFINE8 :: Integer -> BTreeBlackboard -> Integer
localBoardLocalDEFINE8 1 blackboard
  | False = (min 5 (max 2 (min (boardBlVAR0 blackboard) (boardBlVAR3 blackboard))))
  | (boardBlDEFINE7 1 blackboard) = (min 5 (max 2 (((- (boardBlVAR0 blackboard)) + ((boardBlVAR3 blackboard) * (boardBlVAR0 blackboard))) + ((-89) + (57 + (abs (boardBlVAR3 blackboard)))))))
  | otherwise = (min 5 (max 2 (min 15 79)))
  where nodeLocation = 1
localBoardLocalDEFINE8 _ _ = error "localDEFINE8 illegal local reference"
localBoardLocalDEFINE10 :: Integer -> BTreeBlackboard -> Bool
localBoardLocalDEFINE10 1 blackboard
  | (37 >= (abs (-23))) = (sereneXOR (boardBlDEFINE7 2 blackboard) False)
  | ("no" /= "both") = ((boardBlVAR0 blackboard) > (boardBlVAR0 blackboard))
  | otherwise = (False == ((boardBlDEFINE7 1 blackboard) == False))
  where nodeLocation = 1
localBoardLocalDEFINE10 _ _ = error "localDEFINE10 illegal local reference"

-- START OF GET FUNCTIONS FOR LOCAL VARIABLES

localBoardLocalVAR4 :: Integer -> BTreeBlackboard -> Bool
localBoardLocalVAR4 1 = localBoardLocalVAR4Location1
localBoardLocalVAR4 _ = error "localVAR4 illegal local reference"

-- START OF GET FUNCTIONS FOR ARRAYS


-- START OF TYPE CHECKING FUNCTIONS

checkValueBoardBlVAR0 :: Integer -> Integer
checkValueBoardBlVAR0 value
  | 2 > value || value > 5 = error "boardBlVAR0 illegal value"
  | otherwise = value

checkValueBoardBlVAR3 :: Integer -> Integer
checkValueBoardBlVAR3 value
  | 2 > value || value > 5 = error "boardBlVAR3 illegal value"
  | otherwise = value

checkValueLocalBoardLocalVAR4 :: Bool -> Bool
checkValueLocalBoardLocalVAR4 value = value


-- START OF SET FUNCTIONS

updateBoardGenerator :: BTreeBlackboard -> StdGen -> BTreeBlackboard
updateBoardGenerator blackboard newGen = blackboard { sereneBoardGenerator = newGen }
updateLocalBoardLocalVAR4 :: Integer -> BTreeBlackboard -> Bool -> BTreeBlackboard
updateLocalBoardLocalVAR4 1 = updateLocalBoardLocalVAR4Location1
updateLocalBoardLocalVAR4 _ = error "localBoardLocalVAR4 illegal local reference"
updateBoardBlVAR0 :: BTreeBlackboard -> Integer -> BTreeBlackboard
updateBoardBlVAR0 blackboard value = blackboard { boardBlVAR0 = (checkValueBoardBlVAR0 value)}
updateBoardBlVAR3 :: BTreeBlackboard -> Integer -> BTreeBlackboard
updateBoardBlVAR3 blackboard value = blackboard { boardBlVAR3 = (checkValueBoardBlVAR3 value)}
updateLocalBoardLocalVAR4Location1 :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateLocalBoardLocalVAR4Location1 blackboard value = blackboard { localBoardLocalVAR4Location1 = (checkValueLocalBoardLocalVAR4 value)}

-- START OF SET FUNCTIONS FOR ARRAYS


-- START OF INITIAL BLACKBOARD VALUE

initialBlackboard :: Integer -> BTreeBlackboard
initialBlackboard seed = BTreeBlackboard newSereneGenerator newValBlVAR0 newValBlVAR3 localNewValLocalVAR4Location1  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen3
    partialBlackboardBlVAR0 = BTreeBlackboard newSereneGenerator 0 0 True
    initValBlVAR0 :: StdGen -> (Integer, StdGen)
    initValBlVAR0 curGen
      | (False || False) = ((min 5 (max 2 (abs (abs 2)))), curGen)
      | True = ((min 5 (max 2 2)), curGen)
      | otherwise = ((min 5 (max 2 (min ((sereneCOUNT (False == (False || True)) ((True && False) == (False && True))) + (sereneCOUNT False ((min (-81) (-44)) <= (min (-5) (-64))))) (-99)))), curGen)
      where
        blackboard = partialBlackboardBlVAR0

    (newValBlVAR0, tempGen1) = initValBlVAR0 tempGen0

    partialBlackboardBlVAR3 = BTreeBlackboard newSereneGenerator newValBlVAR0 0 True
    initValBlVAR3 :: StdGen -> (Integer, StdGen)
    initValBlVAR3 curGen = ((min 5 (max 2 (abs (- (3 - (-70)))))), curGen)
      where
        blackboard = partialBlackboardBlVAR3

    (newValBlVAR3, tempGen2) = initValBlVAR3 tempGen1

    partialBlackboardLocalVAR4Location1 = BTreeBlackboard newSereneGenerator newValBlVAR0 newValBlVAR3 True
    localInitValLocalVAR4Location1 :: StdGen -> (Bool, StdGen)
    localInitValLocalVAR4Location1 curGen = ((newValBlVAR3 <= (newValBlVAR0 * (newValBlVAR0 * ((-88) * 59)))), curGen)
      where
        blackboard = partialBlackboardLocalVAR4Location1
        nodeLocation = 1

    (localNewValLocalVAR4Location1, tempGen3) = localInitValLocalVAR4Location1 tempGen2


