module Behavior_tree_environment where
import SereneRandomizer
import System.Random
import Behavior_tree_blackboard

data BTreeEnvironment = BTreeEnvironment {
  sereneEnvGenerator :: StdGen
  , envX :: Int
  , envY :: Int
  , envHole_1 :: Int
  , envHole_2 :: Int
  , envHole_3 :: Int
  , envHole_4 :: Int
  , envHole_5 :: Int
  , envHole_6 :: Int
  , envHole_7 :: Int
  , envHole_8 :: Int
  , envHole_9 :: Int
  , envFlag_x :: Int
  , envFlag_y :: Int
  , envTile_progress :: Int
  , envTile_tracker :: Int
  }

instance Show BTreeEnvironment where
  show (BTreeEnvironment _ envX envY envHole_1 envHole_2 envHole_3 envHole_4 envHole_5 envHole_6 envHole_7 envHole_8 envHole_9 envFlag_x envFlag_y envTile_progress envTile_tracker) = "Env = {" ++ "envX: " ++ show envX ++ ", envY: " ++ show envY ++ ", envHole_1: " ++ show envHole_1 ++ ", envHole_2: " ++ show envHole_2 ++ ", envHole_3: " ++ show envHole_3 ++ ", envHole_4: " ++ show envHole_4 ++ ", envHole_5: " ++ show envHole_5 ++ ", envHole_6: " ++ show envHole_6 ++ ", envHole_7: " ++ show envHole_7 ++ ", envHole_8: " ++ show envHole_8 ++ ", envHole_9: " ++ show envHole_9 ++ ", envFlag_x: " ++ show envFlag_x ++ ", envFlag_y: " ++ show envFlag_y ++ ", envTile_progress: " ++ show envTile_progress ++ ", envTile_tracker: " ++ show envTile_tracker ++ "}"


envActive_hole :: BTreeBlackboard -> BTreeEnvironment -> Int
envActive_hole blackboard environment
  | (((envX environment) + (min 0 (boardForward blackboard))) == 4) = (envHole_1 environment)
  | (((envX environment) + (min 0 (boardForward blackboard))) == (4 + 1)) = (envHole_2 environment)
  | (((envX environment) + (min 0 (boardForward blackboard))) == (4 + 2)) = (envHole_3 environment)
  | (((envX environment) + (min 0 (boardForward blackboard))) == (4 + 3)) = (envHole_4 environment)
  | (((envX environment) + (min 0 (boardForward blackboard))) == (4 + 4)) = (envHole_5 environment)
  | (((envX environment) + (min 0 (boardForward blackboard))) == (4 + 5)) = (envHole_6 environment)
  | (((envX environment) + (min 0 (boardForward blackboard))) == (4 + 6)) = (envHole_7 environment)
  | (((envX environment) + (min 0 (boardForward blackboard))) == (4 + 7)) = (envHole_8 environment)
  | (((envX environment) + (min 0 (boardForward blackboard))) == (4 + 8)) = (envHole_9 environment)
  | otherwise = (-1)
envFlag_returned :: BTreeBlackboard -> BTreeEnvironment -> Bool
envFlag_returned blackboard environment = ((boardHave_flag blackboard) && ((envX environment) <= 3))


updateEnvGenerator :: BTreeEnvironment -> StdGen -> BTreeEnvironment
updateEnvGenerator environment newGen = environment { sereneEnvGenerator = newGen }
updateEnvX :: BTreeEnvironment -> Int -> BTreeEnvironment
updateEnvX environment value
  | 0 > value || value > 18 = error "x illegal value"
  | otherwise = environment { envX = value }

updateEnvY :: BTreeEnvironment -> Int -> BTreeEnvironment
updateEnvY environment value
  | 0 > value || value > 2 = error "y illegal value"
  | otherwise = environment { envY = value }

updateEnvHole_1 :: BTreeEnvironment -> Int -> BTreeEnvironment
updateEnvHole_1 environment _ = environment

updateEnvHole_2 :: BTreeEnvironment -> Int -> BTreeEnvironment
updateEnvHole_2 environment _ = environment

updateEnvHole_3 :: BTreeEnvironment -> Int -> BTreeEnvironment
updateEnvHole_3 environment _ = environment

updateEnvHole_4 :: BTreeEnvironment -> Int -> BTreeEnvironment
updateEnvHole_4 environment _ = environment

updateEnvHole_5 :: BTreeEnvironment -> Int -> BTreeEnvironment
updateEnvHole_5 environment _ = environment

updateEnvHole_6 :: BTreeEnvironment -> Int -> BTreeEnvironment
updateEnvHole_6 environment _ = environment

updateEnvHole_7 :: BTreeEnvironment -> Int -> BTreeEnvironment
updateEnvHole_7 environment _ = environment

updateEnvHole_8 :: BTreeEnvironment -> Int -> BTreeEnvironment
updateEnvHole_8 environment _ = environment

updateEnvHole_9 :: BTreeEnvironment -> Int -> BTreeEnvironment
updateEnvHole_9 environment _ = environment

updateEnvFlag_x :: BTreeEnvironment -> Int -> BTreeEnvironment
updateEnvFlag_x environment value
  | 15 > value || value > 18 = error "flag_x illegal value"
  | otherwise = environment { envFlag_x = value }

updateEnvFlag_y :: BTreeEnvironment -> Int -> BTreeEnvironment
updateEnvFlag_y environment value
  | 0 > value || value > 2 = error "flag_y illegal value"
  | otherwise = environment { envFlag_y = value }

updateEnvTile_progress :: BTreeEnvironment -> Int -> BTreeEnvironment
updateEnvTile_progress environment value
  | 0 > value || value > 2 = error "tile_progress illegal value"
  | otherwise = environment { envTile_progress = value }

updateEnvTile_tracker :: BTreeEnvironment -> Int -> BTreeEnvironment
updateEnvTile_tracker environment value
  | 0 > value || value > 2 = error "tile_tracker illegal value"
  | otherwise = environment { envTile_tracker = value }

checkTickConditionTermination :: BTreeBlackboard -> BTreeEnvironment -> Bool
checkTickConditionTermination blackboard environment = True

modifiedID :: BTreeBlackboard -> BTreeEnvironment -> BTreeEnvironment
modifiedID _ environment = environment
applyFutureChanges :: [(BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)] -> (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
applyFutureChanges [] = id
applyFutureChanges futureChanges = head futureChanges . applyFutureChanges (tail futureChanges)


betweenTickUpdate :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
betweenTickUpdate environment = environment


initialEnvironment :: Int -> BTreeBlackboard -> BTreeEnvironment
initialEnvironment seed blackboard = BTreeEnvironment newSereneGenerator newValX newValY newValHole_1 newValHole_2 newValHole_3 newValHole_4 newValHole_5 newValHole_6 newValHole_7 newValHole_8 newValHole_9 newValFlag_x newValFlag_y newValTile_progress newValTile_tracker
  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen15
    initValX :: StdGen -> (Int, StdGen)
    initValX curGen = (0, curGen)

    (newValX, tempGen1) = initValX tempGen0

    initValY :: StdGen -> (Int, StdGen)
    initValY curGen = (0, curGen)

    (newValY, tempGen2) = initValY tempGen1

    initValHole_1 :: StdGen -> (Int, StdGen)
    initValHole_1 curGen = (privateRandom0 (fst (getRandomInt curGen 2)), snd (getRandomInt curGen 2))
      where
        privateRandom0 :: Int -> Int
        privateRandom0 0 = 0
        privateRandom0 1 = 1
        privateRandom0 _ = 2

    (newValHole_1, tempGen3) = initValHole_1 tempGen2

    initValHole_2 :: StdGen -> (Int, StdGen)
    initValHole_2 curGen = (privateRandom0 (fst (getRandomInt curGen 2)), snd (getRandomInt curGen 2))
      where
        privateRandom0 :: Int -> Int
        privateRandom0 0 = 0
        privateRandom0 1 = 1
        privateRandom0 _ = 2

    (newValHole_2, tempGen4) = initValHole_2 tempGen3

    initValHole_3 :: StdGen -> (Int, StdGen)
    initValHole_3 curGen = (privateRandom0 (fst (getRandomInt curGen 2)), snd (getRandomInt curGen 2))
      where
        privateRandom0 :: Int -> Int
        privateRandom0 0 = 0
        privateRandom0 1 = 1
        privateRandom0 _ = 2

    (newValHole_3, tempGen5) = initValHole_3 tempGen4

    initValHole_4 :: StdGen -> (Int, StdGen)
    initValHole_4 curGen = (privateRandom0 (fst (getRandomInt curGen 2)), snd (getRandomInt curGen 2))
      where
        privateRandom0 :: Int -> Int
        privateRandom0 0 = 0
        privateRandom0 1 = 1
        privateRandom0 _ = 2

    (newValHole_4, tempGen6) = initValHole_4 tempGen5

    initValHole_5 :: StdGen -> (Int, StdGen)
    initValHole_5 curGen = (privateRandom0 (fst (getRandomInt curGen 2)), snd (getRandomInt curGen 2))
      where
        privateRandom0 :: Int -> Int
        privateRandom0 0 = 0
        privateRandom0 1 = 1
        privateRandom0 _ = 2

    (newValHole_5, tempGen7) = initValHole_5 tempGen6

    initValHole_6 :: StdGen -> (Int, StdGen)
    initValHole_6 curGen = (privateRandom0 (fst (getRandomInt curGen 2)), snd (getRandomInt curGen 2))
      where
        privateRandom0 :: Int -> Int
        privateRandom0 0 = 0
        privateRandom0 1 = 1
        privateRandom0 _ = 2

    (newValHole_6, tempGen8) = initValHole_6 tempGen7

    initValHole_7 :: StdGen -> (Int, StdGen)
    initValHole_7 curGen = (privateRandom0 (fst (getRandomInt curGen 2)), snd (getRandomInt curGen 2))
      where
        privateRandom0 :: Int -> Int
        privateRandom0 0 = 0
        privateRandom0 1 = 1
        privateRandom0 _ = 2

    (newValHole_7, tempGen9) = initValHole_7 tempGen8

    initValHole_8 :: StdGen -> (Int, StdGen)
    initValHole_8 curGen = (privateRandom0 (fst (getRandomInt curGen 2)), snd (getRandomInt curGen 2))
      where
        privateRandom0 :: Int -> Int
        privateRandom0 0 = 0
        privateRandom0 1 = 1
        privateRandom0 _ = 2

    (newValHole_8, tempGen10) = initValHole_8 tempGen9

    initValHole_9 :: StdGen -> (Int, StdGen)
    initValHole_9 curGen = (privateRandom0 (fst (getRandomInt curGen 2)), snd (getRandomInt curGen 2))
      where
        privateRandom0 :: Int -> Int
        privateRandom0 0 = 0
        privateRandom0 1 = 1
        privateRandom0 _ = 2

    (newValHole_9, tempGen11) = initValHole_9 tempGen10

    initValFlag_x :: StdGen -> (Int, StdGen)
    initValFlag_x curGen = (privateRandom0 (fst (getRandomInt curGen 3)), snd (getRandomInt curGen 3))
      where
        privateRandom0 :: Int -> Int
        privateRandom0 0 = 15
        privateRandom0 1 = 16
        privateRandom0 2 = 17
        privateRandom0 _ = 18

    (newValFlag_x, tempGen12) = initValFlag_x tempGen11

    initValFlag_y :: StdGen -> (Int, StdGen)
    initValFlag_y curGen = (privateRandom0 (fst (getRandomInt curGen 2)), snd (getRandomInt curGen 2))
      where
        privateRandom0 :: Int -> Int
        privateRandom0 0 = 0
        privateRandom0 1 = 1
        privateRandom0 _ = 2

    (newValFlag_y, tempGen13) = initValFlag_y tempGen12

    initValTile_progress :: StdGen -> (Int, StdGen)
    initValTile_progress curGen = (0, curGen)

    (newValTile_progress, tempGen14) = initValTile_progress tempGen13

    initValTile_tracker :: StdGen -> (Int, StdGen)
    initValTile_tracker curGen = (0, curGen)

    (newValTile_tracker, tempGen15) = initValTile_tracker tempGen14


