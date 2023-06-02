module BehaviorTreeBlackboard where
import SereneRandomizer
import System.Random

data BTreeBlackboard = BTreeBlackboard {
  sereneBoardGenerator :: StdGen
  , boardZone :: String
  , boardSide :: Int
  , boardHaveFlag :: Bool
  , boardNeedSideReached :: Bool
  , localBoardTileSearched47 :: Bool
  }

instance Show BTreeBlackboard where
  show (BTreeBlackboard _ boardZone boardSide boardHaveFlag boardNeedSideReached localBoardTileSearched47) = "Board = {" ++ "boardZone: " ++ show boardZone ++ ", boardSide: " ++ show boardSide ++ ", boardHaveFlag: " ++ show boardHaveFlag ++ ", boardNeedSideReached: " ++ show boardNeedSideReached ++ ", localBoardTileSearched47: " ++ show localBoardTileSearched47 ++ "}"


localBoardTileSearched :: Int -> BTreeBlackboard -> Bool
localBoardTileSearched 47 = localBoardTileSearched47
localBoardTileSearched _ = error "tile_searched illegal local reference"


boardForward :: BTreeBlackboard -> Int
boardForward blackboard
  | (boardHaveFlag blackboard) = (-1)
  | otherwise = 1


updateBoardGenerator :: BTreeBlackboard -> StdGen -> BTreeBlackboard
updateBoardGenerator blackboard newGen = blackboard { sereneBoardGenerator = newGen }
updateBoardZone :: BTreeBlackboard -> String -> BTreeBlackboard
updateBoardZone blackboard "home" = blackboard { boardZone = "home" }
updateBoardZone blackboard "maze" = blackboard { boardZone = "maze" }
updateBoardZone blackboard "target" = blackboard { boardZone = "target" }
updateBoardZone _ _ = error "zone illegal value"

updateBoardSide :: BTreeBlackboard -> Int -> BTreeBlackboard
updateBoardSide blackboard (-1) = blackboard { boardSide = (-1) }
updateBoardSide blackboard 1 = blackboard { boardSide = 1 }
updateBoardSide _ _ = error "side illegal value"

updateBoardHaveFlag :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateBoardHaveFlag blackboard value = blackboard { boardHaveFlag = value }

updateBoardNeedSideReached :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateBoardNeedSideReached blackboard value = blackboard { boardNeedSideReached = value }

localUpdateBoardTileSearched :: Int -> BTreeBlackboard -> Bool -> BTreeBlackboard
localUpdateBoardTileSearched 47 blackboard value = blackboard { localBoardTileSearched47 = value }
localUpdateBoardTileSearched _ _ _ = error "tile_searched illegal local reference"



initialBlackboard :: Int -> BTreeBlackboard
initialBlackboard seed = BTreeBlackboard newSereneGenerator newValZone newValSide newValHaveFlag newValNeedSideReached localNewValTileSearched47
  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen5
    initValZone :: StdGen -> (String, StdGen)
    initValZone curGen = ("home", curGen)

    (newValZone, tempGen1) = initValZone tempGen0

    initValSide :: StdGen -> (Int, StdGen)
    initValSide curGen = (1, curGen)

    (newValSide, tempGen2) = initValSide tempGen1

    initValHaveFlag :: StdGen -> (Bool, StdGen)
    initValHaveFlag curGen = (False, curGen)

    (newValHaveFlag, tempGen3) = initValHaveFlag tempGen2

    initValNeedSideReached :: StdGen -> (Bool, StdGen)
    initValNeedSideReached curGen = (True, curGen)

    (newValNeedSideReached, tempGen4) = initValNeedSideReached tempGen3

    localInitValTileSearched47 :: StdGen -> (Bool, StdGen)
    localInitValTileSearched47 curGen = (False, curGen)
    (localNewValTileSearched47, tempGen5) = localInitValTileSearched47 tempGen4

