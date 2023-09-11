module BehaviorTreeBlackboard where
import SereneRandomizer
import System.Random
import SereneOperations

data BTreeBlackboard = BTreeBlackboard {
  sereneBoardGenerator :: StdGen
  , boardBlVAR0 :: Integer
  , boardBlFROZENVAR3 :: Integer
  }

fromBTreeBlackboardToString :: BTreeBlackboard -> String
fromBTreeBlackboardToString blackboard = "Board = {" ++ "boardBlVAR0: " ++ show (boardBlVAR0 blackboard) ++ ", " ++ "boardBlFROZENVAR3: " ++ show (boardBlFROZENVAR3 blackboard) ++ ", " ++ "boardBlDEFINE4: " ++ "[" ++ show (boardBlDEFINE4 0 blackboard) ++ ", " ++ show (boardBlDEFINE4 1 blackboard)++ "]" ++ "}"

-- START OF BLACKBOARD FUNCTIONS

boardBlDEFINE4 :: Integer -> BTreeBlackboard -> Integer
boardBlDEFINE4 0 blackboard = (min (-2) (max (-5) (sereneCOUNT (False == (28 /= (boardBlFROZENVAR3 blackboard))) ((boardBlVAR0 blackboard) < (min (min (boardBlVAR0 blackboard) (boardBlVAR0 blackboard)) (boardBlVAR0 blackboard))))))
boardBlDEFINE4 1 blackboard = (min (-2) (max (-5) (sereneCOUNT (False == (28 /= (boardBlFROZENVAR3 blackboard))) ((boardBlVAR0 blackboard) < (min (min (boardBlVAR0 blackboard) (boardBlVAR0 blackboard)) (boardBlVAR0 blackboard))))))
boardBlDEFINE4 _ _ = error "boardBlDEFINE4 illegal index value"

-- START OF LOCAL BLACKBOARD FUNCTIONS


-- START OF GET FUNCTIONS FOR LOCAL VARIABLES


-- START OF GET FUNCTIONS FOR ARRAYS


-- START OF TYPE CHECKING FUNCTIONS

checkValueBoardBlVAR0 :: Integer -> Integer
checkValueBoardBlVAR0 value
  | 2 > value || value > 5 = error "boardBlVAR0 illegal value"
  | otherwise = value

checkValueLocalBoardLocalVAR2 :: String -> String
checkValueLocalBoardLocalVAR2 "yes" = "yes"
checkValueLocalBoardLocalVAR2 "no" = "no"
checkValueLocalBoardLocalVAR2 "both" = "both"
checkValueLocalBoardLocalVAR2 _ = error "localBoardLocalVAR2 illegal value"


-- START OF SET FUNCTIONS

updateBoardGenerator :: BTreeBlackboard -> StdGen -> BTreeBlackboard
updateBoardGenerator blackboard newGen = blackboard { sereneBoardGenerator = newGen }
updateBoardBlVAR0 :: BTreeBlackboard -> Integer -> BTreeBlackboard
updateBoardBlVAR0 blackboard value = blackboard { boardBlVAR0 = (checkValueBoardBlVAR0 value)}

-- START OF SET FUNCTIONS FOR ARRAYS


-- START OF INITIAL BLACKBOARD VALUE

initialBlackboard :: Integer -> BTreeBlackboard
initialBlackboard seed = BTreeBlackboard newSereneGenerator newValBlVAR0 newValBlFROZENVAR3  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen2
    partialBlackboardBlVAR0 = BTreeBlackboard newSereneGenerator 0 0
    initValBlVAR0 :: StdGen -> (Integer, StdGen)
    initValBlVAR0 curGen = ((min 5 (max 2 11)), curGen)
      where
        blackboard = partialBlackboardBlVAR0

    (newValBlVAR0, tempGen1) = initValBlVAR0 tempGen0

    partialBlackboardBlFROZENVAR3 = BTreeBlackboard newSereneGenerator newValBlVAR0 0
    initValBlFROZENVAR3 :: StdGen -> (Integer, StdGen)
    initValBlFROZENVAR3 curGen
      | (sereneXNOR (sereneXNOR True True) (True == False)) = ((min (-2) (max (-5) (min (max newValBlVAR0 newValBlVAR0) (max 87 78)))), curGen)
      | (sereneXOR (sereneIMPLIES False ((-1) >= 5)) (sereneXOR (True == True) (sereneIMPLIES True True))) = ((min (-2) (max (-5) (sereneCOUNT ("both" /= "yes") (sereneIMPLIES (True || True) False)))), curGen)
      | otherwise = ((min (-2) (max (-5) 4)), curGen)
      where
        blackboard = partialBlackboardBlFROZENVAR3

    (newValBlFROZENVAR3, tempGen2) = initValBlFROZENVAR3 tempGen1


