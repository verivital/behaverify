module BehaviorTreeBlackboard where
import SereneRandomizer
import System.Random
import SereneOperations

data BTreeBlackboard = BTreeBlackboard {
  sereneBoardGenerator :: StdGen
  , boardBlVAR0 :: Bool
  }

fromBTreeBlackboardToString :: BTreeBlackboard -> String
fromBTreeBlackboardToString blackboard = "Board = {" ++ "boardBlVAR0: " ++ show (boardBlVAR0 blackboard) ++ ", " ++ "boardBlDEFINE3: " ++ show (boardBlDEFINE3 blackboard) ++ ", " ++ "boardBlDEFINE4: " ++ show (boardBlDEFINE4 blackboard) ++ "}"

-- START OF BLACKBOARD FUNCTIONS

boardBlDEFINE3 :: BTreeBlackboard -> Integer
boardBlDEFINE3 blackboard
  | True = (min 5 (max 2 ((- (-26)) * ((- (-5)) * ((abs 91) * (84 * (-2)))))))
  | otherwise = (min 5 (max 2 (- 5)))
boardBlDEFINE4 :: BTreeBlackboard -> Integer
boardBlDEFINE4 blackboard
  | False = (min 5 (max 2 ((boardBlDEFINE3 blackboard) - (boardBlDEFINE3 blackboard))))
  | ("both" == "no") = (min 5 (max 2 ((- (boardBlDEFINE3 blackboard)) * 42)))
  | otherwise = (min 5 (max 2 ((boardBlDEFINE3 blackboard) * (((sereneCOUNT (sereneIMPLIES (False && False) False) (sereneIMPLIES (True == (boardBlVAR0 blackboard)) (boardBlVAR0 blackboard))) + (sereneCOUNT (100 > (boardBlDEFINE3 blackboard)) ((sereneXOR True (boardBlVAR0 blackboard)) || (sereneXOR (boardBlVAR0 blackboard) (boardBlVAR0 blackboard))))) * ((((boardBlDEFINE3 blackboard) - (boardBlDEFINE3 blackboard)) - (-20)) * ((boardBlDEFINE3 blackboard) - (boardBlDEFINE3 blackboard)))))))

-- START OF LOCAL BLACKBOARD FUNCTIONS


-- START OF GET FUNCTIONS FOR LOCAL VARIABLES


-- START OF GET FUNCTIONS FOR ARRAYS


-- START OF TYPE CHECKING FUNCTIONS

checkValueBoardBlVAR0 :: Bool -> Bool
checkValueBoardBlVAR0 value = value


-- START OF SET FUNCTIONS

updateBoardGenerator :: BTreeBlackboard -> StdGen -> BTreeBlackboard
updateBoardGenerator blackboard newGen = blackboard { sereneBoardGenerator = newGen }
updateBoardBlVAR0 :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateBoardBlVAR0 blackboard value = blackboard { boardBlVAR0 = (checkValueBoardBlVAR0 value)}

-- START OF SET FUNCTIONS FOR ARRAYS


-- START OF INITIAL BLACKBOARD VALUE

initialBlackboard :: Integer -> BTreeBlackboard
initialBlackboard seed = BTreeBlackboard newSereneGenerator newValBlVAR0  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen1
    partialBlackboardBlVAR0 = BTreeBlackboard newSereneGenerator True
    initValBlVAR0 :: StdGen -> (Bool, StdGen)
    initValBlVAR0 curGen
      | ((19 + ((-2) + (-2))) < 71) = (True, curGen)
      | (5 /= (-49)) = (((- 5) <= ((-10) + ((-4) + ((-56) + (-87))))), curGen)
      | otherwise = ((sereneXNOR True True), curGen)
      where
        blackboard = partialBlackboardBlVAR0

    (newValBlVAR0, tempGen1) = initValBlVAR0 tempGen0


