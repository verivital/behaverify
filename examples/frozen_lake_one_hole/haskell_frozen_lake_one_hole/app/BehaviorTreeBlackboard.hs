module BehaviorTreeBlackboard where
import SereneRandomizer
import System.Random
import SereneOperations

data BTreeBlackboard = BTreeBlackboard {
  sereneBoardGenerator :: StdGen
  , boardTilesIndex0 :: String
  , boardTilesIndex1 :: String
  , boardTilesIndex2 :: String
  , boardTilesIndex3 :: String
  , boardTilesIndex4 :: String
  , boardTilesIndex5 :: String
  , boardTilesIndex6 :: String
  , boardTilesIndex7 :: String
  , boardTilesIndex8 :: String
  , boardTilesIndex9 :: String
  , boardTilesIndex10 :: String
  , boardTilesIndex11 :: String
  , boardTilesIndex12 :: String
  , boardTilesIndex13 :: String
  , boardTilesIndex14 :: String
  , boardTilesIndex15 :: String
  , boardAction :: Int
  , boardSometimes :: Bool
  , boardStrategy :: String
  , boardSubgoal :: Int
  }

instance Show BTreeBlackboard where
  show (BTreeBlackboard _ boardTilesIndex0 boardTilesIndex1 boardTilesIndex2 boardTilesIndex3 boardTilesIndex4 boardTilesIndex5 boardTilesIndex6 boardTilesIndex7 boardTilesIndex8 boardTilesIndex9 boardTilesIndex10 boardTilesIndex11 boardTilesIndex12 boardTilesIndex13 boardTilesIndex14 boardTilesIndex15 boardAction boardSometimes boardStrategy boardSubgoal) = "Board = {" ++ "boardTilesIndex0: " ++ show boardTilesIndex0 ++ ", boardTilesIndex1: " ++ show boardTilesIndex1 ++ ", boardTilesIndex2: " ++ show boardTilesIndex2 ++ ", boardTilesIndex3: " ++ show boardTilesIndex3 ++ ", boardTilesIndex4: " ++ show boardTilesIndex4 ++ ", boardTilesIndex5: " ++ show boardTilesIndex5 ++ ", boardTilesIndex6: " ++ show boardTilesIndex6 ++ ", boardTilesIndex7: " ++ show boardTilesIndex7 ++ ", boardTilesIndex8: " ++ show boardTilesIndex8 ++ ", boardTilesIndex9: " ++ show boardTilesIndex9 ++ ", boardTilesIndex10: " ++ show boardTilesIndex10 ++ ", boardTilesIndex11: " ++ show boardTilesIndex11 ++ ", boardTilesIndex12: " ++ show boardTilesIndex12 ++ ", boardTilesIndex13: " ++ show boardTilesIndex13 ++ ", boardTilesIndex14: " ++ show boardTilesIndex14 ++ ", boardTilesIndex15: " ++ show boardTilesIndex15 ++ ", boardAction: " ++ show boardAction ++ ", boardSometimes: " ++ show boardSometimes ++ ", boardStrategy: " ++ show boardStrategy ++ ", boardSubgoal: " ++ show boardSubgoal ++ "}"

-- START OF BLACKBOARD FUNCTIONS

boardXSubgoal :: BTreeBlackboard -> Int
boardXSubgoal blackboard = (rem (boardSubgoal blackboard) 4)
boardYSubgoal :: BTreeBlackboard -> Int
boardYSubgoal blackboard = (quot ((boardSubgoal blackboard) - (boardXSubgoal blackboard)) 4)

-- START OF LOCAL BLACKBOARD FUNCTIONS


-- START OF GET FUNCTIONS FOR LOCAL VARIABLES


-- START OF GET FUNCTIONS FOR ARRAYS

boardTiles :: Int -> BTreeBlackboard -> String
boardTiles 0 = boardTilesIndex0
boardTiles 1 = boardTilesIndex1
boardTiles 2 = boardTilesIndex2
boardTiles 3 = boardTilesIndex3
boardTiles 4 = boardTilesIndex4
boardTiles 5 = boardTilesIndex5
boardTiles 6 = boardTilesIndex6
boardTiles 7 = boardTilesIndex7
boardTiles 8 = boardTilesIndex8
boardTiles 9 = boardTilesIndex9
boardTiles 10 = boardTilesIndex10
boardTiles 11 = boardTilesIndex11
boardTiles 12 = boardTilesIndex12
boardTiles 13 = boardTilesIndex13
boardTiles 14 = boardTilesIndex14
boardTiles 15 = boardTilesIndex15
boardTiles _ = error "boardTiles illegal index value"

-- START OF TYPE CHECKING FUNCTIONS

checkValueBoardTiles :: String -> String
checkValueBoardTiles "unknown" = "unknown"
checkValueBoardTiles "safe" = "safe"
checkValueBoardTiles "hole" = "hole"
checkValueBoardTiles "goal" = "goal"
checkValueBoardTiles _ = error "boardTiles illegal value"

checkValueBoardAction :: Int -> Int
checkValueBoardAction (-2) = (-2)
checkValueBoardAction (-1) = (-1)
checkValueBoardAction 0 = 0
checkValueBoardAction 1 = 1
checkValueBoardAction 2 = 2
checkValueBoardAction 3 = 3
checkValueBoardAction _ = error "boardAction illegal value"

checkValueBoardSometimes :: Bool -> Bool
checkValueBoardSometimes value = value

checkValueBoardStrategy :: String -> String
checkValueBoardStrategy "x_first" = "x_first"
checkValueBoardStrategy "y_first" = "y_first"
checkValueBoardStrategy _ = error "boardStrategy illegal value"

checkValueBoardSubgoal :: Int -> Int
checkValueBoardSubgoal value
  | 0 > value || value > 15 = error "boardSubgoal illegal value"
  | otherwise = value


-- START OF SET FUNCTIONS

updateBoardGenerator :: BTreeBlackboard -> StdGen -> BTreeBlackboard
updateBoardGenerator blackboard newGen = blackboard { sereneBoardGenerator = newGen }
updateBoardTilesIndex0 :: BTreeBlackboard -> String -> BTreeBlackboard
updateBoardTilesIndex0 blackboard value = blackboard { boardTilesIndex0 = (checkValueBoardTiles value)}
updateBoardTilesIndex1 :: BTreeBlackboard -> String -> BTreeBlackboard
updateBoardTilesIndex1 blackboard value = blackboard { boardTilesIndex1 = (checkValueBoardTiles value)}
updateBoardTilesIndex2 :: BTreeBlackboard -> String -> BTreeBlackboard
updateBoardTilesIndex2 blackboard value = blackboard { boardTilesIndex2 = (checkValueBoardTiles value)}
updateBoardTilesIndex3 :: BTreeBlackboard -> String -> BTreeBlackboard
updateBoardTilesIndex3 blackboard value = blackboard { boardTilesIndex3 = (checkValueBoardTiles value)}
updateBoardTilesIndex4 :: BTreeBlackboard -> String -> BTreeBlackboard
updateBoardTilesIndex4 blackboard value = blackboard { boardTilesIndex4 = (checkValueBoardTiles value)}
updateBoardTilesIndex5 :: BTreeBlackboard -> String -> BTreeBlackboard
updateBoardTilesIndex5 blackboard value = blackboard { boardTilesIndex5 = (checkValueBoardTiles value)}
updateBoardTilesIndex6 :: BTreeBlackboard -> String -> BTreeBlackboard
updateBoardTilesIndex6 blackboard value = blackboard { boardTilesIndex6 = (checkValueBoardTiles value)}
updateBoardTilesIndex7 :: BTreeBlackboard -> String -> BTreeBlackboard
updateBoardTilesIndex7 blackboard value = blackboard { boardTilesIndex7 = (checkValueBoardTiles value)}
updateBoardTilesIndex8 :: BTreeBlackboard -> String -> BTreeBlackboard
updateBoardTilesIndex8 blackboard value = blackboard { boardTilesIndex8 = (checkValueBoardTiles value)}
updateBoardTilesIndex9 :: BTreeBlackboard -> String -> BTreeBlackboard
updateBoardTilesIndex9 blackboard value = blackboard { boardTilesIndex9 = (checkValueBoardTiles value)}
updateBoardTilesIndex10 :: BTreeBlackboard -> String -> BTreeBlackboard
updateBoardTilesIndex10 blackboard value = blackboard { boardTilesIndex10 = (checkValueBoardTiles value)}
updateBoardTilesIndex11 :: BTreeBlackboard -> String -> BTreeBlackboard
updateBoardTilesIndex11 blackboard value = blackboard { boardTilesIndex11 = (checkValueBoardTiles value)}
updateBoardTilesIndex12 :: BTreeBlackboard -> String -> BTreeBlackboard
updateBoardTilesIndex12 blackboard value = blackboard { boardTilesIndex12 = (checkValueBoardTiles value)}
updateBoardTilesIndex13 :: BTreeBlackboard -> String -> BTreeBlackboard
updateBoardTilesIndex13 blackboard value = blackboard { boardTilesIndex13 = (checkValueBoardTiles value)}
updateBoardTilesIndex14 :: BTreeBlackboard -> String -> BTreeBlackboard
updateBoardTilesIndex14 blackboard value = blackboard { boardTilesIndex14 = (checkValueBoardTiles value)}
updateBoardTilesIndex15 :: BTreeBlackboard -> String -> BTreeBlackboard
updateBoardTilesIndex15 blackboard value = blackboard { boardTilesIndex15 = (checkValueBoardTiles value)}
updateBoardAction :: BTreeBlackboard -> Int -> BTreeBlackboard
updateBoardAction blackboard value = blackboard { boardAction = (checkValueBoardAction value)}
updateBoardSometimes :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateBoardSometimes blackboard value = blackboard { boardSometimes = (checkValueBoardSometimes value)}
updateBoardStrategy :: BTreeBlackboard -> String -> BTreeBlackboard
updateBoardStrategy blackboard value = blackboard { boardStrategy = (checkValueBoardStrategy value)}
updateBoardSubgoal :: BTreeBlackboard -> Int -> BTreeBlackboard
updateBoardSubgoal blackboard value = blackboard { boardSubgoal = (checkValueBoardSubgoal value)}

-- START OF SET FUNCTIONS FOR ARRAYS

updateBoardTiles :: Int -> BTreeBlackboard -> String -> BTreeBlackboard
updateBoardTiles 0 = updateBoardTilesIndex0
updateBoardTiles 1 = updateBoardTilesIndex1
updateBoardTiles 2 = updateBoardTilesIndex2
updateBoardTiles 3 = updateBoardTilesIndex3
updateBoardTiles 4 = updateBoardTilesIndex4
updateBoardTiles 5 = updateBoardTilesIndex5
updateBoardTiles 6 = updateBoardTilesIndex6
updateBoardTiles 7 = updateBoardTilesIndex7
updateBoardTiles 8 = updateBoardTilesIndex8
updateBoardTiles 9 = updateBoardTilesIndex9
updateBoardTiles 10 = updateBoardTilesIndex10
updateBoardTiles 11 = updateBoardTilesIndex11
updateBoardTiles 12 = updateBoardTilesIndex12
updateBoardTiles 13 = updateBoardTilesIndex13
updateBoardTiles 14 = updateBoardTilesIndex14
updateBoardTiles 15 = updateBoardTilesIndex15
updateBoardTiles _ = error "BoardTiles illegal index value"
arrayUpdateBoardTiles :: BTreeBlackboard -> [(Int, String)] -> BTreeBlackboard
arrayUpdateBoardTiles blackboard []  = blackboard
arrayUpdateBoardTiles blackboard [(index, value)] = updateBoardTiles index blackboard value
arrayUpdateBoardTiles blackboard indicesValues = blackboard {
  boardTilesIndex0 = newTilesIndex0
  , boardTilesIndex1 = newTilesIndex1
  , boardTilesIndex2 = newTilesIndex2
  , boardTilesIndex3 = newTilesIndex3
  , boardTilesIndex4 = newTilesIndex4
  , boardTilesIndex5 = newTilesIndex5
  , boardTilesIndex6 = newTilesIndex6
  , boardTilesIndex7 = newTilesIndex7
  , boardTilesIndex8 = newTilesIndex8
  , boardTilesIndex9 = newTilesIndex9
  , boardTilesIndex10 = newTilesIndex10
  , boardTilesIndex11 = newTilesIndex11
  , boardTilesIndex12 = newTilesIndex12
  , boardTilesIndex13 = newTilesIndex13
  , boardTilesIndex14 = newTilesIndex14
  , boardTilesIndex15 = newTilesIndex15
  }
    where
      (newTilesIndex0, newTilesIndex1, newTilesIndex2, newTilesIndex3, newTilesIndex4, newTilesIndex5, newTilesIndex6, newTilesIndex7, newTilesIndex8, newTilesIndex9, newTilesIndex10, newTilesIndex11, newTilesIndex12, newTilesIndex13, newTilesIndex14, newTilesIndex15) = updateValues indicesValues
      updateValues :: [(Int, String)] -> (String, String, String, String, String, String, String, String, String, String, String, String, String, String, String, String)
      updateValues [] = (boardTilesIndex0 blackboard, boardTilesIndex1 blackboard, boardTilesIndex2 blackboard, boardTilesIndex3 blackboard, boardTilesIndex4 blackboard, boardTilesIndex5 blackboard, boardTilesIndex6 blackboard, boardTilesIndex7 blackboard, boardTilesIndex8 blackboard, boardTilesIndex9 blackboard, boardTilesIndex10 blackboard, boardTilesIndex11 blackboard, boardTilesIndex12 blackboard, boardTilesIndex13 blackboard, boardTilesIndex14 blackboard, boardTilesIndex15 blackboard)
      updateValues ((0, currentValue) : nextIndicesValues) = (checkValueBoardTiles currentValue, updatedValue1, updatedValue2, updatedValue3, updatedValue4, updatedValue5, updatedValue6, updatedValue7, updatedValue8, updatedValue9, updatedValue10, updatedValue11, updatedValue12, updatedValue13, updatedValue14, updatedValue15)
        where
          (_, updatedValue1, updatedValue2, updatedValue3, updatedValue4, updatedValue5, updatedValue6, updatedValue7, updatedValue8, updatedValue9, updatedValue10, updatedValue11, updatedValue12, updatedValue13, updatedValue14, updatedValue15) = updateValues nextIndicesValues
      updateValues ((1, currentValue) : nextIndicesValues) = (updatedValue0, checkValueBoardTiles currentValue, updatedValue2, updatedValue3, updatedValue4, updatedValue5, updatedValue6, updatedValue7, updatedValue8, updatedValue9, updatedValue10, updatedValue11, updatedValue12, updatedValue13, updatedValue14, updatedValue15)
        where
          (updatedValue0, _, updatedValue2, updatedValue3, updatedValue4, updatedValue5, updatedValue6, updatedValue7, updatedValue8, updatedValue9, updatedValue10, updatedValue11, updatedValue12, updatedValue13, updatedValue14, updatedValue15) = updateValues nextIndicesValues
      updateValues ((2, currentValue) : nextIndicesValues) = (updatedValue0, updatedValue1, checkValueBoardTiles currentValue, updatedValue3, updatedValue4, updatedValue5, updatedValue6, updatedValue7, updatedValue8, updatedValue9, updatedValue10, updatedValue11, updatedValue12, updatedValue13, updatedValue14, updatedValue15)
        where
          (updatedValue0, updatedValue1, _, updatedValue3, updatedValue4, updatedValue5, updatedValue6, updatedValue7, updatedValue8, updatedValue9, updatedValue10, updatedValue11, updatedValue12, updatedValue13, updatedValue14, updatedValue15) = updateValues nextIndicesValues
      updateValues ((3, currentValue) : nextIndicesValues) = (updatedValue0, updatedValue1, updatedValue2, checkValueBoardTiles currentValue, updatedValue4, updatedValue5, updatedValue6, updatedValue7, updatedValue8, updatedValue9, updatedValue10, updatedValue11, updatedValue12, updatedValue13, updatedValue14, updatedValue15)
        where
          (updatedValue0, updatedValue1, updatedValue2, _, updatedValue4, updatedValue5, updatedValue6, updatedValue7, updatedValue8, updatedValue9, updatedValue10, updatedValue11, updatedValue12, updatedValue13, updatedValue14, updatedValue15) = updateValues nextIndicesValues
      updateValues ((4, currentValue) : nextIndicesValues) = (updatedValue0, updatedValue1, updatedValue2, updatedValue3, checkValueBoardTiles currentValue, updatedValue5, updatedValue6, updatedValue7, updatedValue8, updatedValue9, updatedValue10, updatedValue11, updatedValue12, updatedValue13, updatedValue14, updatedValue15)
        where
          (updatedValue0, updatedValue1, updatedValue2, updatedValue3, _, updatedValue5, updatedValue6, updatedValue7, updatedValue8, updatedValue9, updatedValue10, updatedValue11, updatedValue12, updatedValue13, updatedValue14, updatedValue15) = updateValues nextIndicesValues
      updateValues ((5, currentValue) : nextIndicesValues) = (updatedValue0, updatedValue1, updatedValue2, updatedValue3, updatedValue4, checkValueBoardTiles currentValue, updatedValue6, updatedValue7, updatedValue8, updatedValue9, updatedValue10, updatedValue11, updatedValue12, updatedValue13, updatedValue14, updatedValue15)
        where
          (updatedValue0, updatedValue1, updatedValue2, updatedValue3, updatedValue4, _, updatedValue6, updatedValue7, updatedValue8, updatedValue9, updatedValue10, updatedValue11, updatedValue12, updatedValue13, updatedValue14, updatedValue15) = updateValues nextIndicesValues
      updateValues ((6, currentValue) : nextIndicesValues) = (updatedValue0, updatedValue1, updatedValue2, updatedValue3, updatedValue4, updatedValue5, checkValueBoardTiles currentValue, updatedValue7, updatedValue8, updatedValue9, updatedValue10, updatedValue11, updatedValue12, updatedValue13, updatedValue14, updatedValue15)
        where
          (updatedValue0, updatedValue1, updatedValue2, updatedValue3, updatedValue4, updatedValue5, _, updatedValue7, updatedValue8, updatedValue9, updatedValue10, updatedValue11, updatedValue12, updatedValue13, updatedValue14, updatedValue15) = updateValues nextIndicesValues
      updateValues ((7, currentValue) : nextIndicesValues) = (updatedValue0, updatedValue1, updatedValue2, updatedValue3, updatedValue4, updatedValue5, updatedValue6, checkValueBoardTiles currentValue, updatedValue8, updatedValue9, updatedValue10, updatedValue11, updatedValue12, updatedValue13, updatedValue14, updatedValue15)
        where
          (updatedValue0, updatedValue1, updatedValue2, updatedValue3, updatedValue4, updatedValue5, updatedValue6, _, updatedValue8, updatedValue9, updatedValue10, updatedValue11, updatedValue12, updatedValue13, updatedValue14, updatedValue15) = updateValues nextIndicesValues
      updateValues ((8, currentValue) : nextIndicesValues) = (updatedValue0, updatedValue1, updatedValue2, updatedValue3, updatedValue4, updatedValue5, updatedValue6, updatedValue7, checkValueBoardTiles currentValue, updatedValue9, updatedValue10, updatedValue11, updatedValue12, updatedValue13, updatedValue14, updatedValue15)
        where
          (updatedValue0, updatedValue1, updatedValue2, updatedValue3, updatedValue4, updatedValue5, updatedValue6, updatedValue7, _, updatedValue9, updatedValue10, updatedValue11, updatedValue12, updatedValue13, updatedValue14, updatedValue15) = updateValues nextIndicesValues
      updateValues ((9, currentValue) : nextIndicesValues) = (updatedValue0, updatedValue1, updatedValue2, updatedValue3, updatedValue4, updatedValue5, updatedValue6, updatedValue7, updatedValue8, checkValueBoardTiles currentValue, updatedValue10, updatedValue11, updatedValue12, updatedValue13, updatedValue14, updatedValue15)
        where
          (updatedValue0, updatedValue1, updatedValue2, updatedValue3, updatedValue4, updatedValue5, updatedValue6, updatedValue7, updatedValue8, _, updatedValue10, updatedValue11, updatedValue12, updatedValue13, updatedValue14, updatedValue15) = updateValues nextIndicesValues
      updateValues ((10, currentValue) : nextIndicesValues) = (updatedValue0, updatedValue1, updatedValue2, updatedValue3, updatedValue4, updatedValue5, updatedValue6, updatedValue7, updatedValue8, updatedValue9, checkValueBoardTiles currentValue, updatedValue11, updatedValue12, updatedValue13, updatedValue14, updatedValue15)
        where
          (updatedValue0, updatedValue1, updatedValue2, updatedValue3, updatedValue4, updatedValue5, updatedValue6, updatedValue7, updatedValue8, updatedValue9, _, updatedValue11, updatedValue12, updatedValue13, updatedValue14, updatedValue15) = updateValues nextIndicesValues
      updateValues ((11, currentValue) : nextIndicesValues) = (updatedValue0, updatedValue1, updatedValue2, updatedValue3, updatedValue4, updatedValue5, updatedValue6, updatedValue7, updatedValue8, updatedValue9, updatedValue10, checkValueBoardTiles currentValue, updatedValue12, updatedValue13, updatedValue14, updatedValue15)
        where
          (updatedValue0, updatedValue1, updatedValue2, updatedValue3, updatedValue4, updatedValue5, updatedValue6, updatedValue7, updatedValue8, updatedValue9, updatedValue10, _, updatedValue12, updatedValue13, updatedValue14, updatedValue15) = updateValues nextIndicesValues
      updateValues ((12, currentValue) : nextIndicesValues) = (updatedValue0, updatedValue1, updatedValue2, updatedValue3, updatedValue4, updatedValue5, updatedValue6, updatedValue7, updatedValue8, updatedValue9, updatedValue10, updatedValue11, checkValueBoardTiles currentValue, updatedValue13, updatedValue14, updatedValue15)
        where
          (updatedValue0, updatedValue1, updatedValue2, updatedValue3, updatedValue4, updatedValue5, updatedValue6, updatedValue7, updatedValue8, updatedValue9, updatedValue10, updatedValue11, _, updatedValue13, updatedValue14, updatedValue15) = updateValues nextIndicesValues
      updateValues ((13, currentValue) : nextIndicesValues) = (updatedValue0, updatedValue1, updatedValue2, updatedValue3, updatedValue4, updatedValue5, updatedValue6, updatedValue7, updatedValue8, updatedValue9, updatedValue10, updatedValue11, updatedValue12, checkValueBoardTiles currentValue, updatedValue14, updatedValue15)
        where
          (updatedValue0, updatedValue1, updatedValue2, updatedValue3, updatedValue4, updatedValue5, updatedValue6, updatedValue7, updatedValue8, updatedValue9, updatedValue10, updatedValue11, updatedValue12, _, updatedValue14, updatedValue15) = updateValues nextIndicesValues
      updateValues ((14, currentValue) : nextIndicesValues) = (updatedValue0, updatedValue1, updatedValue2, updatedValue3, updatedValue4, updatedValue5, updatedValue6, updatedValue7, updatedValue8, updatedValue9, updatedValue10, updatedValue11, updatedValue12, updatedValue13, checkValueBoardTiles currentValue, updatedValue15)
        where
          (updatedValue0, updatedValue1, updatedValue2, updatedValue3, updatedValue4, updatedValue5, updatedValue6, updatedValue7, updatedValue8, updatedValue9, updatedValue10, updatedValue11, updatedValue12, updatedValue13, _, updatedValue15) = updateValues nextIndicesValues
      updateValues ((15, currentValue) : nextIndicesValues) = (updatedValue0, updatedValue1, updatedValue2, updatedValue3, updatedValue4, updatedValue5, updatedValue6, updatedValue7, updatedValue8, updatedValue9, updatedValue10, updatedValue11, updatedValue12, updatedValue13, updatedValue14, checkValueBoardTiles currentValue)
        where
          (updatedValue0, updatedValue1, updatedValue2, updatedValue3, updatedValue4, updatedValue5, updatedValue6, updatedValue7, updatedValue8, updatedValue9, updatedValue10, updatedValue11, updatedValue12, updatedValue13, updatedValue14, _) = updateValues nextIndicesValues

-- START OF INITIAL BLACKBOARD VALUE

initialBlackboard :: Int -> BTreeBlackboard
initialBlackboard seed = BTreeBlackboard newSereneGenerator newValTilesIndex0 newValTilesIndex1 newValTilesIndex2 newValTilesIndex3 newValTilesIndex4 newValTilesIndex5 newValTilesIndex6 newValTilesIndex7 newValTilesIndex8 newValTilesIndex9 newValTilesIndex10 newValTilesIndex11 newValTilesIndex12 newValTilesIndex13 newValTilesIndex14 newValTilesIndex15 newValAction newValSometimes newValStrategy newValSubgoal  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen20
    partialBlackboardTilesIndex0 = BTreeBlackboard newSereneGenerator " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " 0 True " " 0
    initValTilesIndex0 :: StdGen -> (String, StdGen)
    initValTilesIndex0 curGen = ("unknown", curGen)
      where
        blackboard = partialBlackboardTilesIndex0

    (newValTilesIndex0, tempGen1) = initValTilesIndex0 tempGen0

    partialBlackboardTilesIndex1 = BTreeBlackboard newSereneGenerator newValTilesIndex0 " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " 0 True " " 0
    initValTilesIndex1 :: StdGen -> (String, StdGen)
    initValTilesIndex1 curGen = ("unknown", curGen)
      where
        blackboard = partialBlackboardTilesIndex1

    (newValTilesIndex1, tempGen2) = initValTilesIndex1 tempGen1

    partialBlackboardTilesIndex2 = BTreeBlackboard newSereneGenerator newValTilesIndex0 newValTilesIndex1 " " " " " " " " " " " " " " " " " " " " " " " " " " " " 0 True " " 0
    initValTilesIndex2 :: StdGen -> (String, StdGen)
    initValTilesIndex2 curGen = ("unknown", curGen)
      where
        blackboard = partialBlackboardTilesIndex2

    (newValTilesIndex2, tempGen3) = initValTilesIndex2 tempGen2

    partialBlackboardTilesIndex3 = BTreeBlackboard newSereneGenerator newValTilesIndex0 newValTilesIndex1 newValTilesIndex2 " " " " " " " " " " " " " " " " " " " " " " " " " " 0 True " " 0
    initValTilesIndex3 :: StdGen -> (String, StdGen)
    initValTilesIndex3 curGen = ("unknown", curGen)
      where
        blackboard = partialBlackboardTilesIndex3

    (newValTilesIndex3, tempGen4) = initValTilesIndex3 tempGen3

    partialBlackboardTilesIndex4 = BTreeBlackboard newSereneGenerator newValTilesIndex0 newValTilesIndex1 newValTilesIndex2 newValTilesIndex3 " " " " " " " " " " " " " " " " " " " " " " " " 0 True " " 0
    initValTilesIndex4 :: StdGen -> (String, StdGen)
    initValTilesIndex4 curGen = ("unknown", curGen)
      where
        blackboard = partialBlackboardTilesIndex4

    (newValTilesIndex4, tempGen5) = initValTilesIndex4 tempGen4

    partialBlackboardTilesIndex5 = BTreeBlackboard newSereneGenerator newValTilesIndex0 newValTilesIndex1 newValTilesIndex2 newValTilesIndex3 newValTilesIndex4 " " " " " " " " " " " " " " " " " " " " " " 0 True " " 0
    initValTilesIndex5 :: StdGen -> (String, StdGen)
    initValTilesIndex5 curGen = ("unknown", curGen)
      where
        blackboard = partialBlackboardTilesIndex5

    (newValTilesIndex5, tempGen6) = initValTilesIndex5 tempGen5

    partialBlackboardTilesIndex6 = BTreeBlackboard newSereneGenerator newValTilesIndex0 newValTilesIndex1 newValTilesIndex2 newValTilesIndex3 newValTilesIndex4 newValTilesIndex5 " " " " " " " " " " " " " " " " " " " " 0 True " " 0
    initValTilesIndex6 :: StdGen -> (String, StdGen)
    initValTilesIndex6 curGen = ("unknown", curGen)
      where
        blackboard = partialBlackboardTilesIndex6

    (newValTilesIndex6, tempGen7) = initValTilesIndex6 tempGen6

    partialBlackboardTilesIndex7 = BTreeBlackboard newSereneGenerator newValTilesIndex0 newValTilesIndex1 newValTilesIndex2 newValTilesIndex3 newValTilesIndex4 newValTilesIndex5 newValTilesIndex6 " " " " " " " " " " " " " " " " " " 0 True " " 0
    initValTilesIndex7 :: StdGen -> (String, StdGen)
    initValTilesIndex7 curGen = ("unknown", curGen)
      where
        blackboard = partialBlackboardTilesIndex7

    (newValTilesIndex7, tempGen8) = initValTilesIndex7 tempGen7

    partialBlackboardTilesIndex8 = BTreeBlackboard newSereneGenerator newValTilesIndex0 newValTilesIndex1 newValTilesIndex2 newValTilesIndex3 newValTilesIndex4 newValTilesIndex5 newValTilesIndex6 newValTilesIndex7 " " " " " " " " " " " " " " " " 0 True " " 0
    initValTilesIndex8 :: StdGen -> (String, StdGen)
    initValTilesIndex8 curGen = ("unknown", curGen)
      where
        blackboard = partialBlackboardTilesIndex8

    (newValTilesIndex8, tempGen9) = initValTilesIndex8 tempGen8

    partialBlackboardTilesIndex9 = BTreeBlackboard newSereneGenerator newValTilesIndex0 newValTilesIndex1 newValTilesIndex2 newValTilesIndex3 newValTilesIndex4 newValTilesIndex5 newValTilesIndex6 newValTilesIndex7 newValTilesIndex8 " " " " " " " " " " " " " " 0 True " " 0
    initValTilesIndex9 :: StdGen -> (String, StdGen)
    initValTilesIndex9 curGen = ("unknown", curGen)
      where
        blackboard = partialBlackboardTilesIndex9

    (newValTilesIndex9, tempGen10) = initValTilesIndex9 tempGen9

    partialBlackboardTilesIndex10 = BTreeBlackboard newSereneGenerator newValTilesIndex0 newValTilesIndex1 newValTilesIndex2 newValTilesIndex3 newValTilesIndex4 newValTilesIndex5 newValTilesIndex6 newValTilesIndex7 newValTilesIndex8 newValTilesIndex9 " " " " " " " " " " " " 0 True " " 0
    initValTilesIndex10 :: StdGen -> (String, StdGen)
    initValTilesIndex10 curGen = ("unknown", curGen)
      where
        blackboard = partialBlackboardTilesIndex10

    (newValTilesIndex10, tempGen11) = initValTilesIndex10 tempGen10

    partialBlackboardTilesIndex11 = BTreeBlackboard newSereneGenerator newValTilesIndex0 newValTilesIndex1 newValTilesIndex2 newValTilesIndex3 newValTilesIndex4 newValTilesIndex5 newValTilesIndex6 newValTilesIndex7 newValTilesIndex8 newValTilesIndex9 newValTilesIndex10 " " " " " " " " " " 0 True " " 0
    initValTilesIndex11 :: StdGen -> (String, StdGen)
    initValTilesIndex11 curGen = ("unknown", curGen)
      where
        blackboard = partialBlackboardTilesIndex11

    (newValTilesIndex11, tempGen12) = initValTilesIndex11 tempGen11

    partialBlackboardTilesIndex12 = BTreeBlackboard newSereneGenerator newValTilesIndex0 newValTilesIndex1 newValTilesIndex2 newValTilesIndex3 newValTilesIndex4 newValTilesIndex5 newValTilesIndex6 newValTilesIndex7 newValTilesIndex8 newValTilesIndex9 newValTilesIndex10 newValTilesIndex11 " " " " " " " " 0 True " " 0
    initValTilesIndex12 :: StdGen -> (String, StdGen)
    initValTilesIndex12 curGen = ("unknown", curGen)
      where
        blackboard = partialBlackboardTilesIndex12

    (newValTilesIndex12, tempGen13) = initValTilesIndex12 tempGen12

    partialBlackboardTilesIndex13 = BTreeBlackboard newSereneGenerator newValTilesIndex0 newValTilesIndex1 newValTilesIndex2 newValTilesIndex3 newValTilesIndex4 newValTilesIndex5 newValTilesIndex6 newValTilesIndex7 newValTilesIndex8 newValTilesIndex9 newValTilesIndex10 newValTilesIndex11 newValTilesIndex12 " " " " " " 0 True " " 0
    initValTilesIndex13 :: StdGen -> (String, StdGen)
    initValTilesIndex13 curGen = ("unknown", curGen)
      where
        blackboard = partialBlackboardTilesIndex13

    (newValTilesIndex13, tempGen14) = initValTilesIndex13 tempGen13

    partialBlackboardTilesIndex14 = BTreeBlackboard newSereneGenerator newValTilesIndex0 newValTilesIndex1 newValTilesIndex2 newValTilesIndex3 newValTilesIndex4 newValTilesIndex5 newValTilesIndex6 newValTilesIndex7 newValTilesIndex8 newValTilesIndex9 newValTilesIndex10 newValTilesIndex11 newValTilesIndex12 newValTilesIndex13 " " " " 0 True " " 0
    initValTilesIndex14 :: StdGen -> (String, StdGen)
    initValTilesIndex14 curGen = ("unknown", curGen)
      where
        blackboard = partialBlackboardTilesIndex14

    (newValTilesIndex14, tempGen15) = initValTilesIndex14 tempGen14

    partialBlackboardTilesIndex15 = BTreeBlackboard newSereneGenerator newValTilesIndex0 newValTilesIndex1 newValTilesIndex2 newValTilesIndex3 newValTilesIndex4 newValTilesIndex5 newValTilesIndex6 newValTilesIndex7 newValTilesIndex8 newValTilesIndex9 newValTilesIndex10 newValTilesIndex11 newValTilesIndex12 newValTilesIndex13 newValTilesIndex14 " " 0 True " " 0
    initValTilesIndex15 :: StdGen -> (String, StdGen)
    initValTilesIndex15 curGen = ("unknown", curGen)
      where
        blackboard = partialBlackboardTilesIndex15

    (newValTilesIndex15, tempGen16) = initValTilesIndex15 tempGen15

    partialBlackboardAction = BTreeBlackboard newSereneGenerator newValTilesIndex0 newValTilesIndex1 newValTilesIndex2 newValTilesIndex3 newValTilesIndex4 newValTilesIndex5 newValTilesIndex6 newValTilesIndex7 newValTilesIndex8 newValTilesIndex9 newValTilesIndex10 newValTilesIndex11 newValTilesIndex12 newValTilesIndex13 newValTilesIndex14 newValTilesIndex15 0 True " " 0
    initValAction :: StdGen -> (Int, StdGen)
    initValAction curGen = ((-2), curGen)
      where
        blackboard = partialBlackboardAction

    (newValAction, tempGen17) = initValAction tempGen16

    partialBlackboardSometimes = BTreeBlackboard newSereneGenerator newValTilesIndex0 newValTilesIndex1 newValTilesIndex2 newValTilesIndex3 newValTilesIndex4 newValTilesIndex5 newValTilesIndex6 newValTilesIndex7 newValTilesIndex8 newValTilesIndex9 newValTilesIndex10 newValTilesIndex11 newValTilesIndex12 newValTilesIndex13 newValTilesIndex14 newValTilesIndex15 newValAction True " " 0
    initValSometimes :: StdGen -> (Bool, StdGen)
    initValSometimes curGen = (False, curGen)
      where
        blackboard = partialBlackboardSometimes

    (newValSometimes, tempGen18) = initValSometimes tempGen17

    partialBlackboardStrategy = BTreeBlackboard newSereneGenerator newValTilesIndex0 newValTilesIndex1 newValTilesIndex2 newValTilesIndex3 newValTilesIndex4 newValTilesIndex5 newValTilesIndex6 newValTilesIndex7 newValTilesIndex8 newValTilesIndex9 newValTilesIndex10 newValTilesIndex11 newValTilesIndex12 newValTilesIndex13 newValTilesIndex14 newValTilesIndex15 newValAction newValSometimes " " 0
    initValStrategy :: StdGen -> (String, StdGen)
    initValStrategy curGen = ("x_first", curGen)
      where
        blackboard = partialBlackboardStrategy

    (newValStrategy, tempGen19) = initValStrategy tempGen18

    partialBlackboardSubgoal = BTreeBlackboard newSereneGenerator newValTilesIndex0 newValTilesIndex1 newValTilesIndex2 newValTilesIndex3 newValTilesIndex4 newValTilesIndex5 newValTilesIndex6 newValTilesIndex7 newValTilesIndex8 newValTilesIndex9 newValTilesIndex10 newValTilesIndex11 newValTilesIndex12 newValTilesIndex13 newValTilesIndex14 newValTilesIndex15 newValAction newValSometimes newValStrategy 0
    initValSubgoal :: StdGen -> (Int, StdGen)
    initValSubgoal curGen = (0, curGen)
      where
        blackboard = partialBlackboardSubgoal

    (newValSubgoal, tempGen20) = initValSubgoal tempGen19


