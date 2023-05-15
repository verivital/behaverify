module Behavior_tree_blackboard where
import SereneRandomizer
import System.Random

data BTreeBlackboard = BTreeBlackboard {
  sereneBoardGenerator :: StdGen
  , boardZone :: String
  , boardSide :: Int
  , boardHave_flag :: Bool
  , boardNeed_side_reached :: Bool
  , localBoardTile_searched47 :: Bool
  }

instance Show BTreeBlackboard where
  show (BTreeBlackboard _ boardZone boardSide boardHave_flag boardNeed_side_reached localBoardTile_searched47) = "Board = {" ++ "boardZone: " ++ show boardZone ++ ", boardSide: " ++ show boardSide ++ ", boardHave_flag: " ++ show boardHave_flag ++ ", boardNeed_side_reached: " ++ show boardNeed_side_reached ++ ", localBoardTile_searched47: " ++ show localBoardTile_searched47 ++ "}"


localBoardTile_searched :: Int -> BTreeBlackboard -> Bool
localBoardTile_searched 47 = localBoardTile_searched47
localBoardTile_searched _ = error "tile_searched illegal local reference"


boardForward :: BTreeBlackboard -> Int
boardForward blackboard
  | (boardHave_flag blackboard) = (-1)
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

updateBoardHave_flag :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateBoardHave_flag blackboard value = blackboard { boardHave_flag = value }

updateBoardNeed_side_reached :: BTreeBlackboard -> Bool -> BTreeBlackboard
updateBoardNeed_side_reached blackboard value = blackboard { boardNeed_side_reached = value }

localUpdateBoardTile_searched :: Int -> BTreeBlackboard -> Bool -> BTreeBlackboard
localUpdateBoardTile_searched 47 blackboard value = blackboard { localBoardTile_searched47 = value }
localUpdateBoardTile_searched _ _ _ = error "tile_searched illegal local reference"



initialBlackboard :: Int -> BTreeBlackboard
initialBlackboard seed = BTreeBlackboard newSereneGenerator newValZone newValSide newValHave_flag newValNeed_side_reached localNewValTile_searched47
  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen5
    initValZone :: StdGen -> (String, StdGen)
    initValZone curGen = ("home", curGen)

    (newValZone, tempGen1) = initValZone tempGen0

    initValSide :: StdGen -> (Int, StdGen)
    initValSide curGen = (1, curGen)

    (newValSide, tempGen2) = initValSide tempGen1

    initValHave_flag :: StdGen -> (Bool, StdGen)
    initValHave_flag curGen = (False, curGen)

    (newValHave_flag, tempGen3) = initValHave_flag tempGen2

    initValNeed_side_reached :: StdGen -> (Bool, StdGen)
    initValNeed_side_reached curGen = (True, curGen)

    (newValNeed_side_reached, tempGen4) = initValNeed_side_reached tempGen3

    localInitValTile_searched47 :: StdGen -> (Bool, StdGen)
    localInitValTile_searched47 curGen = (False, curGen)
    (localNewValTile_searched47, tempGen5) = localInitValTile_searched47 tempGen4

