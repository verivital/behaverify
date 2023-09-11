module BehaviorTreeBlackboard where
import SereneRandomizer
import System.Random
import SereneOperations

data BTreeBlackboard = BTreeBlackboard {
  sereneBoardGenerator :: StdGen
  , boardBlVAR0Index0 :: String
  , boardBlVAR0Index1 :: String
  , boardBlVAR2 :: Bool
  , boardBlVAR3 :: Integer
  , boardBlFROZENVAR5Index0 :: Integer
  , boardBlFROZENVAR5Index1 :: Integer
  , boardBlFROZENVAR5Index2 :: Integer
  }

fromBTreeBlackboardToString :: BTreeBlackboard -> String
fromBTreeBlackboardToString blackboard = "Board = {" ++ "boardBlVAR0: " ++ "[" ++ show (boardBlVAR0 0 blackboard) ++ ", " ++ show (boardBlVAR0 1 blackboard)++ "]" ++ ", " ++ "boardBlVAR0: " ++ "[" ++ show (boardBlVAR0 0 blackboard) ++ ", " ++ show (boardBlVAR0 1 blackboard)++ "]" ++ ", " ++ "boardBlVAR2: " ++ show (boardBlVAR2 blackboard) ++ ", " ++ "boardBlVAR3: " ++ show (boardBlVAR3 blackboard) ++ ", " ++ "boardBlFROZENVAR5: " ++ "[" ++ show (boardBlFROZENVAR5 0 blackboard) ++ ", " ++ show (boardBlFROZENVAR5 1 blackboard) ++ ", " ++ show (boardBlFROZENVAR5 2 blackboard)++ "]" ++ ", " ++ "boardBlFROZENVAR5: " ++ "[" ++ show (boardBlFROZENVAR5 0 blackboard) ++ ", " ++ show (boardBlFROZENVAR5 1 blackboard) ++ ", " ++ show (boardBlFROZENVAR5 2 blackboard)++ "]" ++ ", " ++ "boardBlFROZENVAR5: " ++ "[" ++ show (boardBlFROZENVAR5 0 blackboard) ++ ", " ++ show (boardBlFROZENVAR5 1 blackboard) ++ ", " ++ show (boardBlFROZENVAR5 2 blackboard)++ "]" ++ ", " ++ "boardBlDEFINE8: " ++ "[" ++ show (boardBlDEFINE8 0 blackboard) ++ ", " ++ show (boardBlDEFINE8 1 blackboard)++ "]" ++ "}"

-- START OF BLACKBOARD FUNCTIONS

boardBlDEFINE8 :: Integer -> BTreeBlackboard -> Integer
boardBlDEFINE8 0 blackboard
  | (((-49) * ((max (boardBlVAR3 blackboard) (boardBlFROZENVAR5 1 blackboard)) * 100)) < 26) = (min 5 (max 2 ((sereneCOUNT (sereneIMPLIES True True) ((max (boardBlFROZENVAR5 0 blackboard) (boardBlVAR3 blackboard)) >= ((sereneCOUNT (sereneIMPLIES (True && (boardBlVAR2 blackboard)) ((-73) <= (-28))) (((boardBlFROZENVAR5 2 blackboard) - (boardBlFROZENVAR5 0 blackboard)) > 75)) + (sereneCOUNT False ((min (boardBlVAR3 blackboard) 57) > (-83)))))) + (sereneCOUNT ((- 70) <= (boardBlFROZENVAR5 0 blackboard)) ((((sereneCOUNT ((-33) == 69) ((boardBlVAR2 blackboard) == True)) + (sereneCOUNT ((boardBlFROZENVAR5 1 blackboard) <= 90) (sereneIMPLIES True (boardBlVAR2 blackboard)))) - (boardBlVAR3 blackboard)) < ((boardBlFROZENVAR5 1 blackboard) * (40 * 32)))))))
  | otherwise = (min 5 (max 2 (max ((-89) * ((boardBlFROZENVAR5 0 blackboard) * ((boardBlVAR3 blackboard) * (boardBlVAR3 blackboard)))) 53)))
boardBlDEFINE8 1 blackboard
  | (94 <= 92) = (min 5 (max 2 ((-96) * (boardBlVAR3 blackboard))))
  | ((76 > (-74)) && False) = (min 5 (max 2 ((sereneCOUNT ((boardBlFROZENVAR5 1 blackboard) >= 37) (sereneXNOR (boardBlVAR2 blackboard) False)) + (sereneCOUNT False ((boardBlFROZENVAR5 1 blackboard) <= (-43))))))
  | otherwise = (min 5 (max 2 (max (min (-45) 76) (sereneCOUNT ((-91) < (boardBlVAR3 blackboard)) ((boardBlVAR2 blackboard) == True)))))
boardBlDEFINE8 _ _ = error "boardBlDEFINE8 illegal index value"

-- START OF LOCAL BLACKBOARD FUNCTIONS


-- START OF GET FUNCTIONS FOR LOCAL VARIABLES


-- START OF GET FUNCTIONS FOR ARRAYS

boardBlVAR0 :: Integer -> BTreeBlackboard -> String
boardBlVAR0 0 = boardBlVAR0Index0
boardBlVAR0 1 = boardBlVAR0Index1
boardBlVAR0 _ = error "boardBlVAR0 illegal index value"
boardBlFROZENVAR5 :: Integer -> BTreeBlackboard -> Integer
boardBlFROZENVAR5 0 = boardBlFROZENVAR5Index0
boardBlFROZENVAR5 1 = boardBlFROZENVAR5Index1
boardBlFROZENVAR5 2 = boardBlFROZENVAR5Index2
boardBlFROZENVAR5 _ = error "boardBlFROZENVAR5 illegal index value"

-- START OF TYPE CHECKING FUNCTIONS

checkValueBoardBlVAR0 :: String -> String
checkValueBoardBlVAR0 "yes" = "yes"
checkValueBoardBlVAR0 "no" = "no"
checkValueBoardBlVAR0 "both" = "both"
checkValueBoardBlVAR0 _ = error "boardBlVAR0 illegal value"

checkValueBoardBlVAR2 :: Bool -> Bool
checkValueBoardBlVAR2 value = value

checkValueBoardBlVAR3 :: Integer -> Integer
checkValueBoardBlVAR3 value
  | 2 > value || value > 5 = error "boardBlVAR3 illegal value"
  | otherwise = value


-- START OF SET FUNCTIONS

updateBoardGenerator :: BTreeBlackboard -> StdGen -> BTreeBlackboard
updateBoardGenerator blackboard newGen = blackboard { sereneBoardGenerator = newGen }
updateBoardBlVAR0Index0 :: BTreeBlackboard -> String -> BTreeBlackboard
updateBoardBlVAR0Index0 blackboard value = blackboard { boardBlVAR0Index0 = (checkValueBoardBlVAR0 value)}
updateBoardBlVAR0Index1 :: BTreeBlackboard -> String -> BTreeBlackboard
updateBoardBlVAR0Index1 blackboard value = blackboard { boardBlVAR0Index1 = (checkValueBoardBlVAR0 value)}
updateBoardBlVAR2 :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateBoardBlVAR2 blackboard value = blackboard { boardBlVAR2 = (checkValueBoardBlVAR2 value)}
updateBoardBlVAR3 :: BTreeBlackboard -> Integer -> BTreeBlackboard
updateBoardBlVAR3 blackboard value = blackboard { boardBlVAR3 = (checkValueBoardBlVAR3 value)}

-- START OF SET FUNCTIONS FOR ARRAYS

updateBoardBlVAR0 :: Integer -> BTreeBlackboard -> String -> BTreeBlackboard
updateBoardBlVAR0 0 = updateBoardBlVAR0Index0
updateBoardBlVAR0 1 = updateBoardBlVAR0Index1
updateBoardBlVAR0 _ = error "BoardBlVAR0 illegal index value"
arrayUpdateBoardBlVAR0 :: BTreeBlackboard -> [(Integer, String)] -> BTreeBlackboard
arrayUpdateBoardBlVAR0 blackboard []  = blackboard
arrayUpdateBoardBlVAR0 blackboard [(index, value)] = updateBoardBlVAR0 index blackboard value
arrayUpdateBoardBlVAR0 blackboard indicesValues = blackboard {
  boardBlVAR0Index0 = newBlVAR0Index0
  , boardBlVAR0Index1 = newBlVAR0Index1
  }
    where
      (newBlVAR0Index0, newBlVAR0Index1) = updateValues indicesValues
      updateValues :: [(Integer, String)] -> (String, String)
      updateValues [] = (boardBlVAR0Index0 blackboard, boardBlVAR0Index1 blackboard)
      updateValues ((0, currentValue) : nextIndicesValues) = (checkValueBoardBlVAR0 currentValue, updatedValue1)
        where
          (_, updatedValue1) = updateValues nextIndicesValues
      updateValues ((1, currentValue) : nextIndicesValues) = (updatedValue0, checkValueBoardBlVAR0 currentValue)
        where
          (updatedValue0, _) = updateValues nextIndicesValues

-- START OF INITIAL BLACKBOARD VALUE

initialBlackboard :: Integer -> BTreeBlackboard
initialBlackboard seed = BTreeBlackboard newSereneGenerator newValBlVAR0Index0 newValBlVAR0Index1 newValBlVAR2 newValBlVAR3 newValBlFROZENVAR5Index0 newValBlFROZENVAR5Index1 newValBlFROZENVAR5Index2  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen7
    partialBlackboardBlVAR0Index0 = BTreeBlackboard newSereneGenerator " " " " True 0 0 0 0
    initValBlVAR0Index0 :: StdGen -> (String, StdGen)
    initValBlVAR0Index0 curGen = ("no", curGen)
      where
        blackboard = partialBlackboardBlVAR0Index0

    (newValBlVAR0Index0, tempGen1) = initValBlVAR0Index0 tempGen0

    partialBlackboardBlVAR0Index1 = BTreeBlackboard newSereneGenerator newValBlVAR0Index0 " " True 0 0 0 0
    initValBlVAR0Index1 :: StdGen -> (String, StdGen)
    initValBlVAR0Index1 curGen
      | (3 > (abs (abs (-4)))) = ("both", curGen)
      | otherwise = ("both", curGen)
      where
        blackboard = partialBlackboardBlVAR0Index1

    (newValBlVAR0Index1, tempGen2) = initValBlVAR0Index1 tempGen1

    partialBlackboardBlVAR2 = BTreeBlackboard newSereneGenerator newValBlVAR0Index0 newValBlVAR0Index1 True 0 0 0 0
    initValBlVAR2 :: StdGen -> (Bool, StdGen)
    initValBlVAR2 curGen
      | False = ((sereneIMPLIES ((boardBlVAR0 1 blackboard) /= (boardBlVAR0 0 blackboard)) ("both" == (boardBlVAR0 1 blackboard))), curGen)
      | otherwise = (False, curGen)
      where
        blackboard = partialBlackboardBlVAR2

    (newValBlVAR2, tempGen3) = initValBlVAR2 tempGen2

    partialBlackboardBlVAR3 = BTreeBlackboard newSereneGenerator newValBlVAR0Index0 newValBlVAR0Index1 newValBlVAR2 0 0 0 0
    initValBlVAR3 :: StdGen -> (Integer, StdGen)
    initValBlVAR3 curGen
      | (((-3) < (-4)) || (39 /= 4)) = ((min 5 (max 2 12)), curGen)
      | otherwise = ((min 5 (max 2 (-5))), curGen)
      where
        blackboard = partialBlackboardBlVAR3

    (newValBlVAR3, tempGen4) = initValBlVAR3 tempGen3

    partialBlackboardBlFROZENVAR5Index0 = BTreeBlackboard newSereneGenerator newValBlVAR0Index0 newValBlVAR0Index1 newValBlVAR2 newValBlVAR3 0 0 0
    initValBlFROZENVAR5Index0 :: StdGen -> (Integer, StdGen)
    initValBlFROZENVAR5Index0 curGen = ((min (-2) (max (-5) (abs newValBlVAR3))), curGen)
      where
        blackboard = partialBlackboardBlFROZENVAR5Index0

    (newValBlFROZENVAR5Index0, tempGen5) = initValBlFROZENVAR5Index0 tempGen4

    partialBlackboardBlFROZENVAR5Index1 = BTreeBlackboard newSereneGenerator newValBlVAR0Index0 newValBlVAR0Index1 newValBlVAR2 newValBlVAR3 newValBlFROZENVAR5Index0 0 0
    initValBlFROZENVAR5Index1 :: StdGen -> (Integer, StdGen)
    initValBlFROZENVAR5Index1 curGen = ((min (-2) (max (-5) (-55))), curGen)
      where
        blackboard = partialBlackboardBlFROZENVAR5Index1

    (newValBlFROZENVAR5Index1, tempGen6) = initValBlFROZENVAR5Index1 tempGen5

    partialBlackboardBlFROZENVAR5Index2 = BTreeBlackboard newSereneGenerator newValBlVAR0Index0 newValBlVAR0Index1 newValBlVAR2 newValBlVAR3 newValBlFROZENVAR5Index0 newValBlFROZENVAR5Index1 0
    initValBlFROZENVAR5Index2 :: StdGen -> (Integer, StdGen)
    initValBlFROZENVAR5Index2 curGen = ((min (-2) (max (-5) (newValBlVAR3 * (13 * newValBlVAR3)))), curGen)
      where
        blackboard = partialBlackboardBlFROZENVAR5Index2

    (newValBlFROZENVAR5Index2, tempGen7) = initValBlFROZENVAR5Index2 tempGen6


