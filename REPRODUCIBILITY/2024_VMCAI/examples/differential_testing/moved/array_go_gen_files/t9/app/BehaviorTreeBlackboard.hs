module BehaviorTreeBlackboard where
import SereneRandomizer
import System.Random
import SereneOperations

data BTreeBlackboard = BTreeBlackboard {
  sereneBoardGenerator :: StdGen
  , boardBlVAR0 :: String
  , boardBlVAR3Index0 :: Bool
  , boardBlVAR3Index1 :: Bool
  , boardBlFROZENVAR4Index0 :: Integer
  , boardBlFROZENVAR4Index1 :: Integer
  }

fromBTreeBlackboardToString :: BTreeBlackboard -> String
fromBTreeBlackboardToString blackboard = "Board = {" ++ "boardBlVAR0: " ++ show (boardBlVAR0 blackboard) ++ ", " ++ "boardBlVAR3: " ++ "[" ++ show (boardBlVAR3 0 blackboard) ++ ", " ++ show (boardBlVAR3 1 blackboard)++ "]" ++ ", " ++ "boardBlVAR3: " ++ "[" ++ show (boardBlVAR3 0 blackboard) ++ ", " ++ show (boardBlVAR3 1 blackboard)++ "]" ++ ", " ++ "boardBlFROZENVAR4: " ++ "[" ++ show (boardBlFROZENVAR4 0 blackboard) ++ ", " ++ show (boardBlFROZENVAR4 1 blackboard)++ "]" ++ ", " ++ "boardBlFROZENVAR4: " ++ "[" ++ show (boardBlFROZENVAR4 0 blackboard) ++ ", " ++ show (boardBlFROZENVAR4 1 blackboard)++ "]" ++ ", " ++ "boardBlDEFINE6: " ++ show (boardBlDEFINE6 blackboard) ++ ", " ++ "localBoardLocalDEFINE5Location3: " ++ "[" ++ show (localBoardLocalDEFINE5 3 0 blackboard) ++ ", " ++ show (localBoardLocalDEFINE5 3 1 blackboard) ++ ", " ++ show (localBoardLocalDEFINE5 3 2 blackboard)++ "]" ++ "}"

-- START OF BLACKBOARD FUNCTIONS

boardBlDEFINE6 :: BTreeBlackboard -> Integer
boardBlDEFINE6 blackboard
  | ((abs (boardBlFROZENVAR4 1 blackboard)) >= (6 - (- (boardBlFROZENVAR4 1 blackboard)))) = (min (-2) (max (-5) 72))
  | ((sereneXOR (True || True) True) && ((boardBlVAR0 blackboard) == (boardBlVAR0 blackboard))) = (min (-2) (max (-5) ((sereneCOUNT (sereneIMPLIES False (boardBlVAR3 0 blackboard)) ((boardBlVAR3 0 blackboard) && True)) + (sereneCOUNT False (True || (boardBlVAR3 1 blackboard))))))
  | otherwise = (min (-2) (max (-5) (- (max (boardBlFROZENVAR4 0 blackboard) (- 85)))))

-- START OF LOCAL BLACKBOARD FUNCTIONS

localBoardLocalDEFINE5 :: Integer -> Integer -> BTreeBlackboard -> String
localBoardLocalDEFINE5 3 = localBoardLocalDEFINE5Location3
localBoardLocalDEFINE5 _ = error "localBoardLocalDEFINE5 illegal local reference"
localBoardLocalDEFINE5Location3 :: Integer -> BTreeBlackboard -> String
localBoardLocalDEFINE5Location3 0 = localBoardLocalDEFINE5Location3Index0
localBoardLocalDEFINE5Location3 1 = localBoardLocalDEFINE5Location3Index1
localBoardLocalDEFINE5Location3 2 = localBoardLocalDEFINE5Location3Index2
localBoardLocalDEFINE5Location3 _ = error "localBoardLocalDEFINE53 illegal index"
localBoardLocalDEFINE5Location3Index0 blackboard = "yes"
  where nodeLocation = 3
localBoardLocalDEFINE5Location3Index1 blackboard = (boardBlVAR0 blackboard)
  where nodeLocation = 3
localBoardLocalDEFINE5Location3Index2 blackboard = (boardBlVAR0 blackboard)
  where nodeLocation = 3

-- START OF GET FUNCTIONS FOR LOCAL VARIABLES


-- START OF GET FUNCTIONS FOR ARRAYS

boardBlVAR3 :: Integer -> BTreeBlackboard -> Bool
boardBlVAR3 0 = boardBlVAR3Index0
boardBlVAR3 1 = boardBlVAR3Index1
boardBlVAR3 _ = error "boardBlVAR3 illegal index value"
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

checkValueBoardBlVAR3 :: Bool -> Bool
checkValueBoardBlVAR3 value = value


-- START OF SET FUNCTIONS

updateBoardGenerator :: BTreeBlackboard -> StdGen -> BTreeBlackboard
updateBoardGenerator blackboard newGen = blackboard { sereneBoardGenerator = newGen }
updateBoardBlVAR0 :: BTreeBlackboard -> String -> BTreeBlackboard
updateBoardBlVAR0 blackboard value = blackboard { boardBlVAR0 = (checkValueBoardBlVAR0 value)}
updateBoardBlVAR3Index0 :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateBoardBlVAR3Index0 blackboard value = blackboard { boardBlVAR3Index0 = (checkValueBoardBlVAR3 value)}
updateBoardBlVAR3Index1 :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateBoardBlVAR3Index1 blackboard value = blackboard { boardBlVAR3Index1 = (checkValueBoardBlVAR3 value)}

-- START OF SET FUNCTIONS FOR ARRAYS

updateBoardBlVAR3 :: Integer -> BTreeBlackboard -> Bool -> BTreeBlackboard
updateBoardBlVAR3 0 = updateBoardBlVAR3Index0
updateBoardBlVAR3 1 = updateBoardBlVAR3Index1
updateBoardBlVAR3 _ = error "BoardBlVAR3 illegal index value"
arrayUpdateBoardBlVAR3 :: BTreeBlackboard -> [(Integer, Bool)] -> BTreeBlackboard
arrayUpdateBoardBlVAR3 blackboard []  = blackboard
arrayUpdateBoardBlVAR3 blackboard [(index, value)] = updateBoardBlVAR3 index blackboard value
arrayUpdateBoardBlVAR3 blackboard indicesValues = blackboard {
  boardBlVAR3Index0 = newBlVAR3Index0
  , boardBlVAR3Index1 = newBlVAR3Index1
  }
    where
      (newBlVAR3Index0, newBlVAR3Index1) = updateValues indicesValues
      updateValues :: [(Integer, Bool)] -> (Bool, Bool)
      updateValues [] = (boardBlVAR3Index0 blackboard, boardBlVAR3Index1 blackboard)
      updateValues ((0, currentValue) : nextIndicesValues) = (checkValueBoardBlVAR3 currentValue, updatedValue1)
        where
          (_, updatedValue1) = updateValues nextIndicesValues
      updateValues ((1, currentValue) : nextIndicesValues) = (updatedValue0, checkValueBoardBlVAR3 currentValue)
        where
          (updatedValue0, _) = updateValues nextIndicesValues

-- START OF INITIAL BLACKBOARD VALUE

initialBlackboard :: Integer -> BTreeBlackboard
initialBlackboard seed = BTreeBlackboard newSereneGenerator newValBlVAR0 newValBlVAR3Index0 newValBlVAR3Index1 newValBlFROZENVAR4Index0 newValBlFROZENVAR4Index1  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen5
    partialBlackboardBlVAR0 = BTreeBlackboard newSereneGenerator " " True True 0 0
    initValBlVAR0 :: StdGen -> (String, StdGen)
    initValBlVAR0 curGen
      | False = ("yes", curGen)
      | (((-3) * ((-4) * (4 * (-5)))) < ((-77) - (-73))) = ("no", curGen)
      | otherwise = ("no", curGen)
      where
        blackboard = partialBlackboardBlVAR0

    (newValBlVAR0, tempGen1) = initValBlVAR0 tempGen0

    partialBlackboardBlVAR3Index0 = BTreeBlackboard newSereneGenerator newValBlVAR0 True True 0 0
    initValBlVAR3Index0 :: StdGen -> (Bool, StdGen)
    initValBlVAR3Index0 curGen
      | (False && True) = (False, curGen)
      | (((-18) * (4 * (3 * (-2)))) > ((-65) + (3 + (-13)))) = ((True == (90 >= (-5))), curGen)
      | otherwise = (True, curGen)
      where
        blackboard = partialBlackboardBlVAR3Index0

    (newValBlVAR3Index0, tempGen2) = initValBlVAR3Index0 tempGen1

    partialBlackboardBlVAR3Index1 = BTreeBlackboard newSereneGenerator newValBlVAR0 newValBlVAR3Index0 True 0 0
    initValBlVAR3Index1 :: StdGen -> (Bool, StdGen)
    initValBlVAR3Index1 curGen
      | (False && True) = (False, curGen)
      | (((-18) * (4 * (3 * (-2)))) > ((-65) + (3 + (-13)))) = ((True == (90 >= (-5))), curGen)
      | otherwise = (True, curGen)
      where
        blackboard = partialBlackboardBlVAR3Index1

    (newValBlVAR3Index1, tempGen3) = initValBlVAR3Index1 tempGen2

    partialBlackboardBlFROZENVAR4Index0 = BTreeBlackboard newSereneGenerator newValBlVAR0 newValBlVAR3Index0 newValBlVAR3Index1 0 0
    initValBlFROZENVAR4Index0 :: StdGen -> (Integer, StdGen)
    initValBlFROZENVAR4Index0 curGen
      | ((sereneCOUNT (True || (boardBlVAR3 0 blackboard)) (True && (boardBlVAR3 0 blackboard))) <= (-63)) = ((min 5 (max 2 (71 + ((-14) + ((-4) + 69))))), curGen)
      | (boardBlVAR3 1 blackboard) = ((min 5 (max 2 (max (-5) (-3)))), curGen)
      | otherwise = ((min 5 (max 2 95)), curGen)
      where
        blackboard = partialBlackboardBlFROZENVAR4Index0

    (newValBlFROZENVAR4Index0, tempGen4) = initValBlFROZENVAR4Index0 tempGen3

    partialBlackboardBlFROZENVAR4Index1 = BTreeBlackboard newSereneGenerator newValBlVAR0 newValBlVAR3Index0 newValBlVAR3Index1 newValBlFROZENVAR4Index0 0
    initValBlFROZENVAR4Index1 :: StdGen -> (Integer, StdGen)
    initValBlFROZENVAR4Index1 curGen
      | ((sereneCOUNT (True || (boardBlVAR3 0 blackboard)) (True && (boardBlVAR3 0 blackboard))) <= (-63)) = ((min 5 (max 2 (71 + ((-14) + ((-4) + 69))))), curGen)
      | (boardBlVAR3 1 blackboard) = ((min 5 (max 2 (max (-5) (-3)))), curGen)
      | otherwise = ((min 5 (max 2 95)), curGen)
      where
        blackboard = partialBlackboardBlFROZENVAR4Index1

    (newValBlFROZENVAR4Index1, tempGen5) = initValBlFROZENVAR4Index1 tempGen4


