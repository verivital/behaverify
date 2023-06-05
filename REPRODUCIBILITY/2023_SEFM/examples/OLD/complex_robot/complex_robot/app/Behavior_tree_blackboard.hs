module Behavior_tree_blackboard where
import SereneRandomizer
import System.Random

data BTreeBlackboard = BTreeBlackboard {
  sereneBoardGenerator :: StdGen
  , boardZone :: String
  , boardSide :: String
  , boardHave_flag :: Bool
  , localBoardTile_searched29 :: Bool
  }

instance Show BTreeBlackboard where
  show (BTreeBlackboard _ boardZone boardSide boardHave_flaglocalBoardTile_searched29) = "Board = {" ++ "boardZone: " ++ show boardZone ++ ", boardSide: " ++ show boardSide ++ ", boardHave_flag: " ++ show boardHave_flag ++ ", localBoardTile_searched29: " ++ show localBoardTile_searched29 ++ "}"


localBoardTile_searched :: Int -> BTreeBlackboard -> Bool
localBoardTile_searched 29 = localBoardTile_searched29
localBoardTile_searched _ _ = error "tile_searched illegal local reference"


boardForward :: BTreeBlackboard -> Int
boardForward blackboard
  | (boardHave_flag blackboard) = -1
  | otherwise = 1


updateBoardGenerator :: BTreeBlackboard -> StdGen -> BTreeBlackboard
updateBoardGenerator blackboard newGen = blackboard { sereneBoardGenerator = newGen }
updateBoardZone :: BTreeBlackboard -> String -> BTreeBlackboard
updateBoardZone blackboard "home" = blackboard { envZone = "home" }
updateBoardZone blackboard "maze" = blackboard { envZone = "maze" }
updateBoardZone blackboard "target" = blackboard { envZone = "target" }
updateBoardZone blackbaord value = error "zone illegal value"

updateBoardSide :: BTreeBlackboard -> String -> BTreeBlackboard
updateBoardSide blackboard "-1" = blackboard { envSide = "-1" }
updateBoardSide blackboard "1" = blackboard { envSide = "1" }
updateBoardSide blackbaord value = error "side illegal value"

updateBoardHave_flag :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateBoardHave_flag blackboard value = blackboard { boardHave_flag = value }

localUpdateBoardTile_searched :: Int -> BTreeBlackboard -> Bool -> BTreeBlackboard
localUpdateBoardTile_searched 29 blackboard value = blackboard { localBoardTile_searched29 = value }
localUpdateBoardTile_searched _ _ _ = error "tile_searched illegal local reference"



initialBlackboard :: Int -> BTreeBlackboard
initialBlackboard seed = BTreeBlackboard newSereneGenerator newValZone newValSide newValHave_flaglocalNewValTile_searched29
  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen4
    initValZone :: StdGen -> (String, StdGen)
    initValZone curGen = ('home', curGen)
    (newValZone, tempGen1) = initValZone tempGen0
    initValSide :: StdGen -> (String, StdGen)
    initValSide curGen = (1, curGen)
    (newValSide, tempGen2) = initValSide tempGen1
    initValHave_flag :: StdGen -> (Bool, StdGen)
    initValHave_flag curGen = (False, curGen)
    (newValHave_flag, tempGen3) = initValHave_flag tempGen2
    localInitValTile_searched29 :: StdGen -> (Bool, StdGen)
    localInitValTile_searched29 curGen = (False, curGen)
    (localNewValTile_searched29, tempGen4) = localInitValTile_searched29 tempGen3

