module BehaviorTreeEnvironment where
import SereneRandomizer
import System.Random
import BehaviorTreeBlackboard

data BTreeEnvironment = BTreeEnvironment {
  sereneEnvGenerator :: StdGen
  , envX :: Int
  , envY :: Int
  , envHole1 :: Int
  , envHole2 :: Int
  , envHole3 :: Int
  , envHole4 :: Int
  , envHole5 :: Int
  , envHole6 :: Int
  , envHole7 :: Int
  , envHole8 :: Int
  , envHole9 :: Int
  , envFlagX :: Int
  , envFlagY :: Int
  , envTileProgress :: Int
  , envTileTracker :: Int
  }

instance Show BTreeEnvironment where
  show (BTreeEnvironment _ envX envY envHole1 envHole2 envHole3 envHole4 envHole5 envHole6 envHole7 envHole8 envHole9 envFlagX envFlagY envTileProgress envTileTracker) = "Env = {" ++ "envX: " ++ show envX ++ ", envY: " ++ show envY ++ ", envHole1: " ++ show envHole1 ++ ", envHole2: " ++ show envHole2 ++ ", envHole3: " ++ show envHole3 ++ ", envHole4: " ++ show envHole4 ++ ", envHole5: " ++ show envHole5 ++ ", envHole6: " ++ show envHole6 ++ ", envHole7: " ++ show envHole7 ++ ", envHole8: " ++ show envHole8 ++ ", envHole9: " ++ show envHole9 ++ ", envFlagX: " ++ show envFlagX ++ ", envFlagY: " ++ show envFlagY ++ ", envTileProgress: " ++ show envTileProgress ++ ", envTileTracker: " ++ show envTileTracker ++ "}"


envActiveHole :: BTreeBlackboard -> BTreeEnvironment -> Int
envActiveHole blackboard environment
  | (((envX environment) + (min 0 (boardForward blackboard))) == 4) = (envHole1 environment)
  | (((envX environment) + (min 0 (boardForward blackboard))) == (4 + 1)) = (envHole2 environment)
  | (((envX environment) + (min 0 (boardForward blackboard))) == (4 + 2)) = (envHole3 environment)
  | (((envX environment) + (min 0 (boardForward blackboard))) == (4 + 3)) = (envHole4 environment)
  | (((envX environment) + (min 0 (boardForward blackboard))) == (4 + 4)) = (envHole5 environment)
  | (((envX environment) + (min 0 (boardForward blackboard))) == (4 + 5)) = (envHole6 environment)
  | (((envX environment) + (min 0 (boardForward blackboard))) == (4 + 6)) = (envHole7 environment)
  | (((envX environment) + (min 0 (boardForward blackboard))) == (4 + 7)) = (envHole8 environment)
  | (((envX environment) + (min 0 (boardForward blackboard))) == (4 + 8)) = (envHole9 environment)
  | otherwise = (-1)
envFlagReturned :: BTreeBlackboard -> BTreeEnvironment -> Bool
envFlagReturned blackboard environment = ((boardHaveFlag blackboard) && ((envX environment) <= 3))


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

updateEnvHole1 :: BTreeEnvironment -> Int -> BTreeEnvironment
updateEnvHole1 environment _ = environment

updateEnvHole2 :: BTreeEnvironment -> Int -> BTreeEnvironment
updateEnvHole2 environment _ = environment

updateEnvHole3 :: BTreeEnvironment -> Int -> BTreeEnvironment
updateEnvHole3 environment _ = environment

updateEnvHole4 :: BTreeEnvironment -> Int -> BTreeEnvironment
updateEnvHole4 environment _ = environment

updateEnvHole5 :: BTreeEnvironment -> Int -> BTreeEnvironment
updateEnvHole5 environment _ = environment

updateEnvHole6 :: BTreeEnvironment -> Int -> BTreeEnvironment
updateEnvHole6 environment _ = environment

updateEnvHole7 :: BTreeEnvironment -> Int -> BTreeEnvironment
updateEnvHole7 environment _ = environment

updateEnvHole8 :: BTreeEnvironment -> Int -> BTreeEnvironment
updateEnvHole8 environment _ = environment

updateEnvHole9 :: BTreeEnvironment -> Int -> BTreeEnvironment
updateEnvHole9 environment _ = environment

updateEnvFlagX :: BTreeEnvironment -> Int -> BTreeEnvironment
updateEnvFlagX environment value
  | 15 > value || value > 18 = error "flag_x illegal value"
  | otherwise = environment { envFlagX = value }

updateEnvFlagY :: BTreeEnvironment -> Int -> BTreeEnvironment
updateEnvFlagY environment value
  | 0 > value || value > 2 = error "flag_y illegal value"
  | otherwise = environment { envFlagY = value }

updateEnvTileProgress :: BTreeEnvironment -> Int -> BTreeEnvironment
updateEnvTileProgress environment value
  | 0 > value || value > 2 = error "tile_progress illegal value"
  | otherwise = environment { envTileProgress = value }

updateEnvTileTracker :: BTreeEnvironment -> Int -> BTreeEnvironment
updateEnvTileTracker environment value
  | 0 > value || value > 2 = error "tile_tracker illegal value"
  | otherwise = environment { envTileTracker = value }

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
initialEnvironment seed blackboard = BTreeEnvironment newSereneGenerator newValX newValY newValHole1 newValHole2 newValHole3 newValHole4 newValHole5 newValHole6 newValHole7 newValHole8 newValHole9 newValFlagX newValFlagY newValTileProgress newValTileTracker
  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen15
    initValX :: StdGen -> (Int, StdGen)
    initValX curGen = (0, curGen)

    (newValX, tempGen1) = initValX tempGen0

    initValY :: StdGen -> (Int, StdGen)
    initValY curGen = (0, curGen)

    (newValY, tempGen2) = initValY tempGen1

    initValHole1 :: StdGen -> (Int, StdGen)
    initValHole1 curGen = (privateRandom0 (fst (getRandomInt curGen 2)), snd (getRandomInt curGen 2))
      where
        privateRandom0 :: Int -> Int
        privateRandom0 0 = 0
        privateRandom0 1 = 1
        privateRandom0 _ = 2

    (newValHole1, tempGen3) = initValHole1 tempGen2

    initValHole2 :: StdGen -> (Int, StdGen)
    initValHole2 curGen = (privateRandom0 (fst (getRandomInt curGen 2)), snd (getRandomInt curGen 2))
      where
        privateRandom0 :: Int -> Int
        privateRandom0 0 = 0
        privateRandom0 1 = 1
        privateRandom0 _ = 2

    (newValHole2, tempGen4) = initValHole2 tempGen3

    initValHole3 :: StdGen -> (Int, StdGen)
    initValHole3 curGen = (privateRandom0 (fst (getRandomInt curGen 2)), snd (getRandomInt curGen 2))
      where
        privateRandom0 :: Int -> Int
        privateRandom0 0 = 0
        privateRandom0 1 = 1
        privateRandom0 _ = 2

    (newValHole3, tempGen5) = initValHole3 tempGen4

    initValHole4 :: StdGen -> (Int, StdGen)
    initValHole4 curGen = (privateRandom0 (fst (getRandomInt curGen 2)), snd (getRandomInt curGen 2))
      where
        privateRandom0 :: Int -> Int
        privateRandom0 0 = 0
        privateRandom0 1 = 1
        privateRandom0 _ = 2

    (newValHole4, tempGen6) = initValHole4 tempGen5

    initValHole5 :: StdGen -> (Int, StdGen)
    initValHole5 curGen = (privateRandom0 (fst (getRandomInt curGen 2)), snd (getRandomInt curGen 2))
      where
        privateRandom0 :: Int -> Int
        privateRandom0 0 = 0
        privateRandom0 1 = 1
        privateRandom0 _ = 2

    (newValHole5, tempGen7) = initValHole5 tempGen6

    initValHole6 :: StdGen -> (Int, StdGen)
    initValHole6 curGen = (privateRandom0 (fst (getRandomInt curGen 2)), snd (getRandomInt curGen 2))
      where
        privateRandom0 :: Int -> Int
        privateRandom0 0 = 0
        privateRandom0 1 = 1
        privateRandom0 _ = 2

    (newValHole6, tempGen8) = initValHole6 tempGen7

    initValHole7 :: StdGen -> (Int, StdGen)
    initValHole7 curGen = (privateRandom0 (fst (getRandomInt curGen 2)), snd (getRandomInt curGen 2))
      where
        privateRandom0 :: Int -> Int
        privateRandom0 0 = 0
        privateRandom0 1 = 1
        privateRandom0 _ = 2

    (newValHole7, tempGen9) = initValHole7 tempGen8

    initValHole8 :: StdGen -> (Int, StdGen)
    initValHole8 curGen = (privateRandom0 (fst (getRandomInt curGen 2)), snd (getRandomInt curGen 2))
      where
        privateRandom0 :: Int -> Int
        privateRandom0 0 = 0
        privateRandom0 1 = 1
        privateRandom0 _ = 2

    (newValHole8, tempGen10) = initValHole8 tempGen9

    initValHole9 :: StdGen -> (Int, StdGen)
    initValHole9 curGen = (privateRandom0 (fst (getRandomInt curGen 2)), snd (getRandomInt curGen 2))
      where
        privateRandom0 :: Int -> Int
        privateRandom0 0 = 0
        privateRandom0 1 = 1
        privateRandom0 _ = 2

    (newValHole9, tempGen11) = initValHole9 tempGen10

    initValFlagX :: StdGen -> (Int, StdGen)
    initValFlagX curGen = (privateRandom0 (fst (getRandomInt curGen 3)), snd (getRandomInt curGen 3))
      where
        privateRandom0 :: Int -> Int
        privateRandom0 0 = 15
        privateRandom0 1 = 16
        privateRandom0 2 = 17
        privateRandom0 _ = 18

    (newValFlagX, tempGen12) = initValFlagX tempGen11

    initValFlagY :: StdGen -> (Int, StdGen)
    initValFlagY curGen = (privateRandom0 (fst (getRandomInt curGen 2)), snd (getRandomInt curGen 2))
      where
        privateRandom0 :: Int -> Int
        privateRandom0 0 = 0
        privateRandom0 1 = 1
        privateRandom0 _ = 2

    (newValFlagY, tempGen13) = initValFlagY tempGen12

    initValTileProgress :: StdGen -> (Int, StdGen)
    initValTileProgress curGen = (0, curGen)

    (newValTileProgress, tempGen14) = initValTileProgress tempGen13

    initValTileTracker :: StdGen -> (Int, StdGen)
    initValTileTracker curGen = (0, curGen)

    (newValTileTracker, tempGen15) = initValTileTracker tempGen14


