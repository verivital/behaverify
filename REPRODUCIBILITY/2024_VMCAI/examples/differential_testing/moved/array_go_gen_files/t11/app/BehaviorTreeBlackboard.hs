module BehaviorTreeBlackboard where
import SereneRandomizer
import System.Random
import SereneOperations

data BTreeBlackboard = BTreeBlackboard {
  sereneBoardGenerator :: StdGen
  , boardBlVAR0 :: Integer
  , boardBlVAR2 :: Bool
  }

fromBTreeBlackboardToString :: BTreeBlackboard -> String
fromBTreeBlackboardToString blackboard = "Board = {" ++ "boardBlVAR0: " ++ show (boardBlVAR0 blackboard) ++ ", " ++ "boardBlVAR2: " ++ show (boardBlVAR2 blackboard) ++ ", " ++ "boardBlDEFINE4: " ++ show (boardBlDEFINE4 blackboard) ++ ", " ++ "localBoardLocalDEFINE3Location1: " ++ "[" ++ show (localBoardLocalDEFINE3 1 0 blackboard) ++ ", " ++ show (localBoardLocalDEFINE3 1 1 blackboard)++ "]" ++ ", " ++ "localBoardLocalDEFINE3Location3: " ++ "[" ++ show (localBoardLocalDEFINE3 3 0 blackboard) ++ ", " ++ show (localBoardLocalDEFINE3 3 1 blackboard)++ "]" ++ "}"

-- START OF BLACKBOARD FUNCTIONS

boardBlDEFINE4 :: BTreeBlackboard -> Integer
boardBlDEFINE4 blackboard = (min (-2) (max (-5) ((sereneCOUNT ((-100) < (boardBlVAR0 blackboard)) ((boardBlVAR2 blackboard) == False)) + (sereneCOUNT ((boardBlVAR0 blackboard) > 15) ((boardBlVAR0 blackboard) /= (boardBlVAR0 blackboard))))))

-- START OF LOCAL BLACKBOARD FUNCTIONS

localBoardLocalDEFINE3 :: Integer -> Integer -> BTreeBlackboard -> Integer
localBoardLocalDEFINE3 1 = localBoardLocalDEFINE3Location1
localBoardLocalDEFINE3 3 = localBoardLocalDEFINE3Location3
localBoardLocalDEFINE3 _ = error "localBoardLocalDEFINE3 illegal local reference"
localBoardLocalDEFINE3Location1 :: Integer -> BTreeBlackboard -> Integer
localBoardLocalDEFINE3Location1 0 = localBoardLocalDEFINE3Location1Index0
localBoardLocalDEFINE3Location1 1 = localBoardLocalDEFINE3Location1Index1
localBoardLocalDEFINE3Location1 _ = error "localBoardLocalDEFINE31 illegal index"
localBoardLocalDEFINE3Location1Index0 blackboard
  | ((boardBlVAR0 blackboard) < (boardBlVAR0 blackboard)) = (min 5 (max 2 (max (boardBlVAR0 blackboard) (boardBlVAR0 blackboard))))
  | otherwise = (min 5 (max 2 ((-66) + ((-68) + ((abs (boardBlVAR0 blackboard)) + 17)))))
  where nodeLocation = 1
localBoardLocalDEFINE3Location1Index1 blackboard
  | ((boardBlVAR0 blackboard) < (boardBlVAR0 blackboard)) = (min 5 (max 2 (max (boardBlVAR0 blackboard) (boardBlVAR0 blackboard))))
  | otherwise = (min 5 (max 2 ((-66) + ((-68) + ((abs (boardBlVAR0 blackboard)) + 17)))))
  where nodeLocation = 1
localBoardLocalDEFINE3Location3 :: Integer -> BTreeBlackboard -> Integer
localBoardLocalDEFINE3Location3 0 = localBoardLocalDEFINE3Location3Index0
localBoardLocalDEFINE3Location3 1 = localBoardLocalDEFINE3Location3Index1
localBoardLocalDEFINE3Location3 _ = error "localBoardLocalDEFINE33 illegal index"
localBoardLocalDEFINE3Location3Index0 blackboard
  | ((boardBlVAR0 blackboard) < (boardBlVAR0 blackboard)) = (min 5 (max 2 (max (boardBlVAR0 blackboard) (boardBlVAR0 blackboard))))
  | otherwise = (min 5 (max 2 ((-66) + ((-68) + ((abs (boardBlVAR0 blackboard)) + 17)))))
  where nodeLocation = 3
localBoardLocalDEFINE3Location3Index1 blackboard
  | ((boardBlVAR0 blackboard) < (boardBlVAR0 blackboard)) = (min 5 (max 2 (max (boardBlVAR0 blackboard) (boardBlVAR0 blackboard))))
  | otherwise = (min 5 (max 2 ((-66) + ((-68) + ((abs (boardBlVAR0 blackboard)) + 17)))))
  where nodeLocation = 3

-- START OF GET FUNCTIONS FOR LOCAL VARIABLES


-- START OF GET FUNCTIONS FOR ARRAYS


-- START OF TYPE CHECKING FUNCTIONS

checkValueBoardBlVAR0 :: Integer -> Integer
checkValueBoardBlVAR0 value
  | (-5) > value || value > (-2) = error "boardBlVAR0 illegal value"
  | otherwise = value

checkValueBoardBlVAR2 :: Bool -> Bool
checkValueBoardBlVAR2 value = value


-- START OF SET FUNCTIONS

updateBoardGenerator :: BTreeBlackboard -> StdGen -> BTreeBlackboard
updateBoardGenerator blackboard newGen = blackboard { sereneBoardGenerator = newGen }
updateBoardBlVAR0 :: BTreeBlackboard -> Integer -> BTreeBlackboard
updateBoardBlVAR0 blackboard value = blackboard { boardBlVAR0 = (checkValueBoardBlVAR0 value)}
updateBoardBlVAR2 :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateBoardBlVAR2 blackboard value = blackboard { boardBlVAR2 = (checkValueBoardBlVAR2 value)}

-- START OF SET FUNCTIONS FOR ARRAYS


-- START OF INITIAL BLACKBOARD VALUE

initialBlackboard :: Integer -> BTreeBlackboard
initialBlackboard seed = BTreeBlackboard newSereneGenerator newValBlVAR0 newValBlVAR2  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen2
    partialBlackboardBlVAR0 = BTreeBlackboard newSereneGenerator 0 True
    initValBlVAR0 :: StdGen -> (Integer, StdGen)
    initValBlVAR0 curGen = ((min (-2) (max (-5) (abs ((-3) + (-97))))), curGen)
      where
        blackboard = partialBlackboardBlVAR0

    (newValBlVAR0, tempGen1) = initValBlVAR0 tempGen0

    partialBlackboardBlVAR2 = BTreeBlackboard newSereneGenerator newValBlVAR0 True
    initValBlVAR2 :: StdGen -> (Bool, StdGen)
    initValBlVAR2 curGen = ((sereneXNOR False False), curGen)
      where
        blackboard = partialBlackboardBlVAR2

    (newValBlVAR2, tempGen2) = initValBlVAR2 tempGen1


