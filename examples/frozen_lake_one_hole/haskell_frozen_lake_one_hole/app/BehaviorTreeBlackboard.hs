module BehaviorTreeBlackboard where
import SereneRandomizer
import System.Random
import SereneOperations

data BTreeBlackboard = BTreeBlackboard {
  sereneBoardGenerator :: StdGen
  , boardAction :: Int
  , boardSometimes :: Bool
  , boardStrategy :: String
  , boardSubgoal :: Int
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
  }

instance Show BTreeBlackboard where
  show (BTreeBlackboard _ boardAction boardSometimes boardStrategy boardSubgoal boardTilesIndex0 boardTilesIndex1 boardTilesIndex2 boardTilesIndex3 boardTilesIndex4 boardTilesIndex5 boardTilesIndex6 boardTilesIndex7 boardTilesIndex8 boardTilesIndex9 boardTilesIndex10 boardTilesIndex11 boardTilesIndex12 boardTilesIndex13 boardTilesIndex14 boardTilesIndex15) = "Board = {" ++ "boardAction: " ++ show boardAction ++ ", boardSometimes: " ++ show boardSometimes ++ ", boardStrategy: " ++ show boardStrategy ++ ", boardSubgoal: " ++ show boardSubgoal ++ ", boardTilesIndex0: " ++ show boardTilesIndex0 ++ ", boardTilesIndex1: " ++ show boardTilesIndex1 ++ ", boardTilesIndex2: " ++ show boardTilesIndex2 ++ ", boardTilesIndex3: " ++ show boardTilesIndex3 ++ ", boardTilesIndex4: " ++ show boardTilesIndex4 ++ ", boardTilesIndex5: " ++ show boardTilesIndex5 ++ ", boardTilesIndex6: " ++ show boardTilesIndex6 ++ ", boardTilesIndex7: " ++ show boardTilesIndex7 ++ ", boardTilesIndex8: " ++ show boardTilesIndex8 ++ ", boardTilesIndex9: " ++ show boardTilesIndex9 ++ ", boardTilesIndex10: " ++ show boardTilesIndex10 ++ ", boardTilesIndex11: " ++ show boardTilesIndex11 ++ ", boardTilesIndex12: " ++ show boardTilesIndex12 ++ ", boardTilesIndex13: " ++ show boardTilesIndex13 ++ ", boardTilesIndex14: " ++ show boardTilesIndex14 ++ ", boardTilesIndex15: " ++ show boardTilesIndex15 ++ "}"


sereneIndexTiles :: Int -> BTreeBlackboard -> String
sereneIndexTiles l = boardTilesIndexl
sereneIndexTiles o = boardTilesIndexo
sereneIndexTiles c = boardTilesIndexc
sereneIndexTiles _ = boardTilesIndex_
sereneIndexTiles a = boardTilesIndexa
sereneIndexTiles r = boardTilesIndexr
sereneIndexTiles r = boardTilesIndexr
sereneIndexTiles a = boardTilesIndexa
sereneIndexTiles y = boardTilesIndexy
sereneIndexTiles _ = boardTilesIndex_
sereneIndexTiles s = boardTilesIndexs
sereneIndexTiles i = boardTilesIndexi
sereneIndexTiles z = boardTilesIndexz
sereneIndexTiles e = boardTilesIndexe
sereneIndexTiles_ = error "tiles illegal index value"




boardXSubgoal :: BTreeBlackboard -> Int
boardXSubgoal blackboard = ((boardSubgoal blackboard) % 4)
boardYSubgoal :: BTreeBlackboard -> Int
boardYSubgoal blackboard = (quot ((boardSubgoal blackboard) - (boardXSubgoal blackboard)) 4)


updateBoardGenerator :: BTreeBlackboard -> StdGen -> BTreeBlackboard
updateBoardGenerator blackboard newGen = blackboard { sereneBoardGenerator = newGen }
updateBoardTiles :: BTreeBlackboard -> String -> BTreeBlackboard
updateBoardTiles blackboard "unknown" = blackboard { boardTiles = "unknown" }
updateBoardTiles blackboard "safe" = blackboard { boardTiles = "safe" }
updateBoardTiles blackboard "hole" = blackboard { boardTiles = "hole" }
updateBoardTiles blackboard "goal" = blackboard { boardTiles = "goal" }
updateBoardTiles _ _ = error "tiles illegal value"

updateBoardAction :: BTreeBlackboard -> Int -> BTreeBlackboard
updateBoardAction blackboard (-2) = blackboard { boardAction = (-2) }
updateBoardAction blackboard (-1) = blackboard { boardAction = (-1) }
updateBoardAction blackboard 0 = blackboard { boardAction = 0 }
updateBoardAction blackboard 1 = blackboard { boardAction = 1 }
updateBoardAction blackboard 2 = blackboard { boardAction = 2 }
updateBoardAction blackboard 3 = blackboard { boardAction = 3 }
updateBoardAction _ _ = error "action illegal value"

updateBoardSometimes :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateBoardSometimes blackboard value = blackboard { boardSometimes = value }

updateBoardStrategy :: BTreeBlackboard -> String -> BTreeBlackboard
updateBoardStrategy blackboard "x_first" = blackboard { boardStrategy = "x_first" }
updateBoardStrategy blackboard "y_first" = blackboard { boardStrategy = "y_first" }
updateBoardStrategy _ _ = error "strategy illegal value"

updateBoardSubgoal :: BTreeBlackboard -> Int -> BTreeBlackboard
updateBoardSubgoal blackboard value
  | 0 > value || value > 15 = error "subgoal illegal value"
  | otherwise = blackboard { boardSubgoal = value }



initialBlackboard :: Int -> BTreeBlackboard
initialBlackboard seed = BTreeBlackboard newSereneGenerator newValAction newValSometimes newValStrategy newValSubgoal newValTilesIndex0 newValTilesIndex1 newValTilesIndex2 newValTilesIndex3 newValTilesIndex4 newValTilesIndex5 newValTilesIndex6 newValTilesIndex7 newValTilesIndex8 newValTilesIndex9 newValTilesIndex10 newValTilesIndex11 newValTilesIndex12 newValTilesIndex13 newValTilesIndex14 newValTilesIndex15  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen20
    partialBlackboardAction = BTreeBlackboard newSereneGenerator 0 True " " 0 " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " "
    initValAction :: StdGen -> (Int, StdGen)
    initValAction curGen = ((-2), curGen)
      where
        blackboard = partialBlackboardAction

    (newValAction, tempGen1) = initValAction tempGen0

    partialBlackboardSometimes = BTreeBlackboard newSereneGenerator newValAction True " " 0 " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " "
    initValSometimes :: StdGen -> (Bool, StdGen)
    initValSometimes curGen = (False, curGen)
      where
        blackboard = partialBlackboardSometimes

    (newValSometimes, tempGen2) = initValSometimes tempGen1

    partialBlackboardStrategy = BTreeBlackboard newSereneGenerator newValAction newValSometimes " " 0 " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " "
    initValStrategy :: StdGen -> (String, StdGen)
    initValStrategy curGen = ("x_first", curGen)
      where
        blackboard = partialBlackboardStrategy

    (newValStrategy, tempGen3) = initValStrategy tempGen2

    partialBlackboardSubgoal = BTreeBlackboard newSereneGenerator newValAction newValSometimes newValStrategy 0 " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " "
    initValSubgoal :: StdGen -> (Int, StdGen)
    initValSubgoal curGen = (0, curGen)
      where
        blackboard = partialBlackboardSubgoal

    (newValSubgoal, tempGen4) = initValSubgoal tempGen3

    partialBlackboardTilesIndex0 = BTreeBlackboard newSereneGenerator newValAction newValSometimes newValStrategy newValSubgoal " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " "
    initValTilesIndex0 :: StdGen -> (String, StdGen)
    initValTilesIndex0 curGen = ("unknown", curGen)
      where
        blackboard = partialBlackboardTilesIndex0

    (newValTilesIndex0, tempGen5) = initValTilesIndex0 tempGen4

    partialBlackboardTilesIndex1 = BTreeBlackboard newSereneGenerator newValAction newValSometimes newValStrategy newValSubgoal newValTilesIndex0 " " " " " " " " " " " " " " " " " " " " " " " " " " " " " "
    initValTilesIndex1 :: StdGen -> (String, StdGen)
    initValTilesIndex1 curGen = ("unknown", curGen)
      where
        blackboard = partialBlackboardTilesIndex1

    (newValTilesIndex1, tempGen6) = initValTilesIndex1 tempGen5

    partialBlackboardTilesIndex2 = BTreeBlackboard newSereneGenerator newValAction newValSometimes newValStrategy newValSubgoal newValTilesIndex0 newValTilesIndex1 " " " " " " " " " " " " " " " " " " " " " " " " " " " "
    initValTilesIndex2 :: StdGen -> (String, StdGen)
    initValTilesIndex2 curGen = ("unknown", curGen)
      where
        blackboard = partialBlackboardTilesIndex2

    (newValTilesIndex2, tempGen7) = initValTilesIndex2 tempGen6

    partialBlackboardTilesIndex3 = BTreeBlackboard newSereneGenerator newValAction newValSometimes newValStrategy newValSubgoal newValTilesIndex0 newValTilesIndex1 newValTilesIndex2 " " " " " " " " " " " " " " " " " " " " " " " " " "
    initValTilesIndex3 :: StdGen -> (String, StdGen)
    initValTilesIndex3 curGen = ("unknown", curGen)
      where
        blackboard = partialBlackboardTilesIndex3

    (newValTilesIndex3, tempGen8) = initValTilesIndex3 tempGen7

    partialBlackboardTilesIndex4 = BTreeBlackboard newSereneGenerator newValAction newValSometimes newValStrategy newValSubgoal newValTilesIndex0 newValTilesIndex1 newValTilesIndex2 newValTilesIndex3 " " " " " " " " " " " " " " " " " " " " " " " "
    initValTilesIndex4 :: StdGen -> (String, StdGen)
    initValTilesIndex4 curGen = ("unknown", curGen)
      where
        blackboard = partialBlackboardTilesIndex4

    (newValTilesIndex4, tempGen9) = initValTilesIndex4 tempGen8

    partialBlackboardTilesIndex5 = BTreeBlackboard newSereneGenerator newValAction newValSometimes newValStrategy newValSubgoal newValTilesIndex0 newValTilesIndex1 newValTilesIndex2 newValTilesIndex3 newValTilesIndex4 " " " " " " " " " " " " " " " " " " " " " "
    initValTilesIndex5 :: StdGen -> (String, StdGen)
    initValTilesIndex5 curGen = ("unknown", curGen)
      where
        blackboard = partialBlackboardTilesIndex5

    (newValTilesIndex5, tempGen10) = initValTilesIndex5 tempGen9

    partialBlackboardTilesIndex6 = BTreeBlackboard newSereneGenerator newValAction newValSometimes newValStrategy newValSubgoal newValTilesIndex0 newValTilesIndex1 newValTilesIndex2 newValTilesIndex3 newValTilesIndex4 newValTilesIndex5 " " " " " " " " " " " " " " " " " " " "
    initValTilesIndex6 :: StdGen -> (String, StdGen)
    initValTilesIndex6 curGen = ("unknown", curGen)
      where
        blackboard = partialBlackboardTilesIndex6

    (newValTilesIndex6, tempGen11) = initValTilesIndex6 tempGen10

    partialBlackboardTilesIndex7 = BTreeBlackboard newSereneGenerator newValAction newValSometimes newValStrategy newValSubgoal newValTilesIndex0 newValTilesIndex1 newValTilesIndex2 newValTilesIndex3 newValTilesIndex4 newValTilesIndex5 newValTilesIndex6 " " " " " " " " " " " " " " " " " "
    initValTilesIndex7 :: StdGen -> (String, StdGen)
    initValTilesIndex7 curGen = ("unknown", curGen)
      where
        blackboard = partialBlackboardTilesIndex7

    (newValTilesIndex7, tempGen12) = initValTilesIndex7 tempGen11

    partialBlackboardTilesIndex8 = BTreeBlackboard newSereneGenerator newValAction newValSometimes newValStrategy newValSubgoal newValTilesIndex0 newValTilesIndex1 newValTilesIndex2 newValTilesIndex3 newValTilesIndex4 newValTilesIndex5 newValTilesIndex6 newValTilesIndex7 " " " " " " " " " " " " " " " "
    initValTilesIndex8 :: StdGen -> (String, StdGen)
    initValTilesIndex8 curGen = ("unknown", curGen)
      where
        blackboard = partialBlackboardTilesIndex8

    (newValTilesIndex8, tempGen13) = initValTilesIndex8 tempGen12

    partialBlackboardTilesIndex9 = BTreeBlackboard newSereneGenerator newValAction newValSometimes newValStrategy newValSubgoal newValTilesIndex0 newValTilesIndex1 newValTilesIndex2 newValTilesIndex3 newValTilesIndex4 newValTilesIndex5 newValTilesIndex6 newValTilesIndex7 newValTilesIndex8 " " " " " " " " " " " " " "
    initValTilesIndex9 :: StdGen -> (String, StdGen)
    initValTilesIndex9 curGen = ("unknown", curGen)
      where
        blackboard = partialBlackboardTilesIndex9

    (newValTilesIndex9, tempGen14) = initValTilesIndex9 tempGen13

    partialBlackboardTilesIndex10 = BTreeBlackboard newSereneGenerator newValAction newValSometimes newValStrategy newValSubgoal newValTilesIndex0 newValTilesIndex1 newValTilesIndex2 newValTilesIndex3 newValTilesIndex4 newValTilesIndex5 newValTilesIndex6 newValTilesIndex7 newValTilesIndex8 newValTilesIndex9 " " " " " " " " " " " "
    initValTilesIndex10 :: StdGen -> (String, StdGen)
    initValTilesIndex10 curGen = ("unknown", curGen)
      where
        blackboard = partialBlackboardTilesIndex10

    (newValTilesIndex10, tempGen15) = initValTilesIndex10 tempGen14

    partialBlackboardTilesIndex11 = BTreeBlackboard newSereneGenerator newValAction newValSometimes newValStrategy newValSubgoal newValTilesIndex0 newValTilesIndex1 newValTilesIndex2 newValTilesIndex3 newValTilesIndex4 newValTilesIndex5 newValTilesIndex6 newValTilesIndex7 newValTilesIndex8 newValTilesIndex9 newValTilesIndex10 " " " " " " " " " "
    initValTilesIndex11 :: StdGen -> (String, StdGen)
    initValTilesIndex11 curGen = ("unknown", curGen)
      where
        blackboard = partialBlackboardTilesIndex11

    (newValTilesIndex11, tempGen16) = initValTilesIndex11 tempGen15

    partialBlackboardTilesIndex12 = BTreeBlackboard newSereneGenerator newValAction newValSometimes newValStrategy newValSubgoal newValTilesIndex0 newValTilesIndex1 newValTilesIndex2 newValTilesIndex3 newValTilesIndex4 newValTilesIndex5 newValTilesIndex6 newValTilesIndex7 newValTilesIndex8 newValTilesIndex9 newValTilesIndex10 newValTilesIndex11 " " " " " " " "
    initValTilesIndex12 :: StdGen -> (String, StdGen)
    initValTilesIndex12 curGen = ("unknown", curGen)
      where
        blackboard = partialBlackboardTilesIndex12

    (newValTilesIndex12, tempGen17) = initValTilesIndex12 tempGen16

    partialBlackboardTilesIndex13 = BTreeBlackboard newSereneGenerator newValAction newValSometimes newValStrategy newValSubgoal newValTilesIndex0 newValTilesIndex1 newValTilesIndex2 newValTilesIndex3 newValTilesIndex4 newValTilesIndex5 newValTilesIndex6 newValTilesIndex7 newValTilesIndex8 newValTilesIndex9 newValTilesIndex10 newValTilesIndex11 newValTilesIndex12 " " " " " "
    initValTilesIndex13 :: StdGen -> (String, StdGen)
    initValTilesIndex13 curGen = ("unknown", curGen)
      where
        blackboard = partialBlackboardTilesIndex13

    (newValTilesIndex13, tempGen18) = initValTilesIndex13 tempGen17

    partialBlackboardTilesIndex14 = BTreeBlackboard newSereneGenerator newValAction newValSometimes newValStrategy newValSubgoal newValTilesIndex0 newValTilesIndex1 newValTilesIndex2 newValTilesIndex3 newValTilesIndex4 newValTilesIndex5 newValTilesIndex6 newValTilesIndex7 newValTilesIndex8 newValTilesIndex9 newValTilesIndex10 newValTilesIndex11 newValTilesIndex12 newValTilesIndex13 " " " "
    initValTilesIndex14 :: StdGen -> (String, StdGen)
    initValTilesIndex14 curGen = ("unknown", curGen)
      where
        blackboard = partialBlackboardTilesIndex14

    (newValTilesIndex14, tempGen19) = initValTilesIndex14 tempGen18

    partialBlackboardTilesIndex15 = BTreeBlackboard newSereneGenerator newValAction newValSometimes newValStrategy newValSubgoal newValTilesIndex0 newValTilesIndex1 newValTilesIndex2 newValTilesIndex3 newValTilesIndex4 newValTilesIndex5 newValTilesIndex6 newValTilesIndex7 newValTilesIndex8 newValTilesIndex9 newValTilesIndex10 newValTilesIndex11 newValTilesIndex12 newValTilesIndex13 newValTilesIndex14 " "
    initValTilesIndex15 :: StdGen -> (String, StdGen)
    initValTilesIndex15 curGen = ("unknown", curGen)
      where
        blackboard = partialBlackboardTilesIndex15

    (newValTilesIndex15, tempGen20) = initValTilesIndex15 tempGen19


