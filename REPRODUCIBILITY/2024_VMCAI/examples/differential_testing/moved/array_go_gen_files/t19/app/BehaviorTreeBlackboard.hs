module BehaviorTreeBlackboard where
import SereneRandomizer
import System.Random
import SereneOperations

data BTreeBlackboard = BTreeBlackboard {
  sereneBoardGenerator :: StdGen
  , boardBlVAR0 :: Integer
  }

fromBTreeBlackboardToString :: BTreeBlackboard -> String
fromBTreeBlackboardToString blackboard = "Board = {" ++ "boardBlVAR0: " ++ show (boardBlVAR0 blackboard) ++ ", " ++ "boardBlDEFINE6: " ++ "[" ++ show (boardBlDEFINE6 0 blackboard) ++ ", " ++ show (boardBlDEFINE6 1 blackboard)++ "]" ++ ", " ++ "localBoardLocalDEFINE5Location6: " ++ "[" ++ show (localBoardLocalDEFINE5 6 0 blackboard) ++ ", " ++ show (localBoardLocalDEFINE5 6 1 blackboard)++ "]" ++ ", " ++ "localBoardLocalDEFINE5Location8: " ++ "[" ++ show (localBoardLocalDEFINE5 8 0 blackboard) ++ ", " ++ show (localBoardLocalDEFINE5 8 1 blackboard)++ "]" ++ "}"

-- START OF BLACKBOARD FUNCTIONS

boardBlDEFINE6 :: Integer -> BTreeBlackboard -> String
boardBlDEFINE6 0 blackboard = "both"
boardBlDEFINE6 1 blackboard = "no"
boardBlDEFINE6 _ _ = error "boardBlDEFINE6 illegal index value"

-- START OF LOCAL BLACKBOARD FUNCTIONS

localBoardLocalDEFINE5 :: Integer -> Integer -> BTreeBlackboard -> Integer
localBoardLocalDEFINE5 6 = localBoardLocalDEFINE5Location6
localBoardLocalDEFINE5 8 = localBoardLocalDEFINE5Location8
localBoardLocalDEFINE5 _ = error "localBoardLocalDEFINE5 illegal local reference"
localBoardLocalDEFINE5Location6 :: Integer -> BTreeBlackboard -> Integer
localBoardLocalDEFINE5Location6 0 = localBoardLocalDEFINE5Location6Index0
localBoardLocalDEFINE5Location6 1 = localBoardLocalDEFINE5Location6Index1
localBoardLocalDEFINE5Location6 _ = error "localBoardLocalDEFINE56 illegal index"
localBoardLocalDEFINE5Location6Index0 blackboard
  | ((-48) > (-20)) = (min 5 (max 2 (-13)))
  | otherwise = (min 5 (max 2 (min ((min (-97) 68) - 39) (max (boardBlVAR0 blackboard) (boardBlVAR0 blackboard)))))
  where nodeLocation = 6
localBoardLocalDEFINE5Location6Index1 blackboard
  | ((-48) > (-20)) = (min 5 (max 2 (-13)))
  | otherwise = (min 5 (max 2 (min ((min (-97) 68) - 39) (max (boardBlVAR0 blackboard) (boardBlVAR0 blackboard)))))
  where nodeLocation = 6
localBoardLocalDEFINE5Location8 :: Integer -> BTreeBlackboard -> Integer
localBoardLocalDEFINE5Location8 0 = localBoardLocalDEFINE5Location8Index0
localBoardLocalDEFINE5Location8 1 = localBoardLocalDEFINE5Location8Index1
localBoardLocalDEFINE5Location8 _ = error "localBoardLocalDEFINE58 illegal index"
localBoardLocalDEFINE5Location8Index0 blackboard
  | ((-48) > (-20)) = (min 5 (max 2 (-13)))
  | otherwise = (min 5 (max 2 (min ((min (-97) 68) - 39) (max (boardBlVAR0 blackboard) (boardBlVAR0 blackboard)))))
  where nodeLocation = 8
localBoardLocalDEFINE5Location8Index1 blackboard
  | ((-48) > (-20)) = (min 5 (max 2 (-13)))
  | otherwise = (min 5 (max 2 (min ((min (-97) 68) - 39) (max (boardBlVAR0 blackboard) (boardBlVAR0 blackboard)))))
  where nodeLocation = 8

-- START OF GET FUNCTIONS FOR LOCAL VARIABLES


-- START OF GET FUNCTIONS FOR ARRAYS


-- START OF TYPE CHECKING FUNCTIONS

checkValueBoardBlVAR0 :: Integer -> Integer
checkValueBoardBlVAR0 value
  | 2 > value || value > 5 = error "boardBlVAR0 illegal value"
  | otherwise = value


-- START OF SET FUNCTIONS

updateBoardGenerator :: BTreeBlackboard -> StdGen -> BTreeBlackboard
updateBoardGenerator blackboard newGen = blackboard { sereneBoardGenerator = newGen }
updateBoardBlVAR0 :: BTreeBlackboard -> Integer -> BTreeBlackboard
updateBoardBlVAR0 blackboard value = blackboard { boardBlVAR0 = (checkValueBoardBlVAR0 value)}

-- START OF SET FUNCTIONS FOR ARRAYS


-- START OF INITIAL BLACKBOARD VALUE

initialBlackboard :: Integer -> BTreeBlackboard
initialBlackboard seed = BTreeBlackboard newSereneGenerator newValBlVAR0  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen1
    partialBlackboardBlVAR0 = BTreeBlackboard newSereneGenerator 0
    initValBlVAR0 :: StdGen -> (Integer, StdGen)
    initValBlVAR0 curGen = ((min 5 (max 2 4)), curGen)
      where
        blackboard = partialBlackboardBlVAR0

    (newValBlVAR0, tempGen1) = initValBlVAR0 tempGen0


