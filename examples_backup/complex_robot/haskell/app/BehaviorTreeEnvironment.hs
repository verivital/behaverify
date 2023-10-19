module BehaviorTreeEnvironment where
import SereneRandomizer
import System.Random
import SereneOperations
import BehaviorTreeBlackboard

data BTreeEnvironment = BTreeEnvironment {
  sereneEnvGenerator :: StdGen
  , envX :: Integer
  , envY :: Integer
  , envHole1 :: Integer
  , envHole2 :: Integer
  , envHole3 :: Integer
  , envHole4 :: Integer
  , envHole5 :: Integer
  , envHole6 :: Integer
  , envHole7 :: Integer
  , envHole8 :: Integer
  , envHole9 :: Integer
  , envFlagX :: Integer
  , envFlagY :: Integer
  , envTileProgress :: Integer
  , envTileTracker :: Integer
  }

fromBTreeEnvironmentToString :: BTreeBlackboard -> BTreeEnvironment -> String
fromBTreeEnvironmentToString blackboard environment = "Env = {" ++ "envX: " ++ show (envX environment) ++ ", " ++ "envY: " ++ show (envY environment) ++ ", " ++ "envHole1: " ++ show (envHole1 environment) ++ ", " ++ "envHole2: " ++ show (envHole2 environment) ++ ", " ++ "envHole3: " ++ show (envHole3 environment) ++ ", " ++ "envHole4: " ++ show (envHole4 environment) ++ ", " ++ "envHole5: " ++ show (envHole5 environment) ++ ", " ++ "envHole6: " ++ show (envHole6 environment) ++ ", " ++ "envHole7: " ++ show (envHole7 environment) ++ ", " ++ "envHole8: " ++ show (envHole8 environment) ++ ", " ++ "envHole9: " ++ show (envHole9 environment) ++ ", " ++ "envFlagX: " ++ show (envFlagX environment) ++ ", " ++ "envFlagY: " ++ show (envFlagY environment) ++ ", " ++ "envTileProgress: " ++ show (envTileProgress environment) ++ ", " ++ "envTileTracker: " ++ show (envTileTracker environment) ++ ", " ++ "envActiveHole: " ++ show (envActiveHole blackboard environment) ++ ", " ++ "envFlagReturned: " ++ show (envFlagReturned blackboard environment) ++ "}"

-- START OF ENVIRONMENT FUNCTIONS

envActiveHole :: BTreeBlackboard -> BTreeEnvironment -> Integer
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

-- START OF GET FUNCTIONS FOR ARRAYS


-- START OF TYPE CHECKING FUNCTIONS

checkValueEnvX :: Integer -> Integer
checkValueEnvX value
  | 0 > value || value > 18 = error "envX illegal value"
  | otherwise = value

checkValueEnvY :: Integer -> Integer
checkValueEnvY value
  | 0 > value || value > 2 = error "envY illegal value"
  | otherwise = value

checkValueEnvFlagX :: Integer -> Integer
checkValueEnvFlagX value
  | 15 > value || value > 18 = error "envFlagX illegal value"
  | otherwise = value

checkValueEnvFlagY :: Integer -> Integer
checkValueEnvFlagY value
  | 0 > value || value > 2 = error "envFlagY illegal value"
  | otherwise = value

checkValueEnvTileProgress :: Integer -> Integer
checkValueEnvTileProgress value
  | 0 > value || value > 2 = error "envTileProgress illegal value"
  | otherwise = value

checkValueEnvTileTracker :: Integer -> Integer
checkValueEnvTileTracker value
  | 0 > value || value > 2 = error "envTileTracker illegal value"
  | otherwise = value


-- START OF SET FUNCTIONS

updateEnvGenerator :: BTreeEnvironment -> StdGen -> BTreeEnvironment
updateEnvGenerator environment newGen = environment { sereneEnvGenerator = newGen }
updateEnvX :: BTreeEnvironment -> Integer -> BTreeEnvironment
updateEnvX environment value = environment { envX = (checkValueEnvX value)}
updateEnvY :: BTreeEnvironment -> Integer -> BTreeEnvironment
updateEnvY environment value = environment { envY = (checkValueEnvY value)}
updateEnvFlagX :: BTreeEnvironment -> Integer -> BTreeEnvironment
updateEnvFlagX environment value = environment { envFlagX = (checkValueEnvFlagX value)}
updateEnvFlagY :: BTreeEnvironment -> Integer -> BTreeEnvironment
updateEnvFlagY environment value = environment { envFlagY = (checkValueEnvFlagY value)}
updateEnvTileProgress :: BTreeEnvironment -> Integer -> BTreeEnvironment
updateEnvTileProgress environment value = environment { envTileProgress = (checkValueEnvTileProgress value)}
updateEnvTileTracker :: BTreeEnvironment -> Integer -> BTreeEnvironment
updateEnvTileTracker environment value = environment { envTileTracker = (checkValueEnvTileTracker value)}

-- START OF SET FUNCTIONS FOR ARRAYS


-- START OF TICK CONDITION

checkTickConditionTermination :: BTreeBlackboard -> BTreeEnvironment -> Bool
checkTickConditionTermination blackboard environment = True

-- START OF FUTURE CHANGES

applyFutureChanges :: [(BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)] -> (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
applyFutureChanges [] = id
applyFutureChanges futureChanges = head futureChanges . applyFutureChanges (tail futureChanges)

-- START OF BETWEEN TICK CHANGES

betweenTickUpdate :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
betweenTickUpdate (blackboard, curEnvironment) = (blackboard, newEnvironment)
  where
    tempEnvironment0 = curEnvironment
    newEnvironment = tempEnvironment2
    tickUpdate1TileProgress :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate1TileProgress environment
      | ((envTileTracker environment) == (envTileProgress environment)) = updateEnvTileProgress environment 0
      | otherwise = updateEnvTileProgress environment (envTileProgress environment)

    tempEnvironment1 = tickUpdate1TileProgress tempEnvironment0

    tickUpdate2TileTracker :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate2TileTracker environment = updateEnvTileTracker environment (envTileProgress environment)

    tempEnvironment2 = tickUpdate2TileTracker tempEnvironment1



-- START OF INITIAL ENVIRONMENT VALUE

initialEnvironment :: Integer -> BTreeBlackboard -> BTreeEnvironment
initialEnvironment seed blackboard = BTreeEnvironment newSereneGenerator newValX newValY newValHole1 newValHole2 newValHole3 newValHole4 newValHole5 newValHole6 newValHole7 newValHole8 newValHole9 newValFlagX newValFlagY newValTileProgress newValTileTracker  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen15
    partialEnvironmentX = BTreeEnvironment newSereneGenerator 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    initValX :: StdGen -> (Integer, StdGen)
    initValX curGen = (0, curGen)
      where
        environment = partialEnvironmentX

    (newValX, tempGen1) = initValX tempGen0

    partialEnvironmentY = BTreeEnvironment newSereneGenerator newValX 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    initValY :: StdGen -> (Integer, StdGen)
    initValY curGen = (0, curGen)
      where
        environment = partialEnvironmentY

    (newValY, tempGen2) = initValY tempGen1

    partialEnvironmentHole1 = BTreeEnvironment newSereneGenerator newValX newValY 0 0 0 0 0 0 0 0 0 0 0 0 0
    initValHole1 :: StdGen -> (Integer, StdGen)
    initValHole1 curGen = (privateRandom0 (fst (getRandomInteger curGen 2)), snd (getRandomInteger curGen 2))
      where
        environment = partialEnvironmentHole1
        privateRandom0 :: Integer -> Integer
        privateRandom0 0 = 0
        privateRandom0 1 = 1
        privateRandom0 _ = 2

    (newValHole1, tempGen3) = initValHole1 tempGen2

    partialEnvironmentHole2 = BTreeEnvironment newSereneGenerator newValX newValY newValHole1 0 0 0 0 0 0 0 0 0 0 0 0
    initValHole2 :: StdGen -> (Integer, StdGen)
    initValHole2 curGen = (privateRandom0 (fst (getRandomInteger curGen 2)), snd (getRandomInteger curGen 2))
      where
        environment = partialEnvironmentHole2
        privateRandom0 :: Integer -> Integer
        privateRandom0 0 = 0
        privateRandom0 1 = 1
        privateRandom0 _ = 2

    (newValHole2, tempGen4) = initValHole2 tempGen3

    partialEnvironmentHole3 = BTreeEnvironment newSereneGenerator newValX newValY newValHole1 newValHole2 0 0 0 0 0 0 0 0 0 0 0
    initValHole3 :: StdGen -> (Integer, StdGen)
    initValHole3 curGen = (privateRandom0 (fst (getRandomInteger curGen 2)), snd (getRandomInteger curGen 2))
      where
        environment = partialEnvironmentHole3
        privateRandom0 :: Integer -> Integer
        privateRandom0 0 = 0
        privateRandom0 1 = 1
        privateRandom0 _ = 2

    (newValHole3, tempGen5) = initValHole3 tempGen4

    partialEnvironmentHole4 = BTreeEnvironment newSereneGenerator newValX newValY newValHole1 newValHole2 newValHole3 0 0 0 0 0 0 0 0 0 0
    initValHole4 :: StdGen -> (Integer, StdGen)
    initValHole4 curGen = (privateRandom0 (fst (getRandomInteger curGen 2)), snd (getRandomInteger curGen 2))
      where
        environment = partialEnvironmentHole4
        privateRandom0 :: Integer -> Integer
        privateRandom0 0 = 0
        privateRandom0 1 = 1
        privateRandom0 _ = 2

    (newValHole4, tempGen6) = initValHole4 tempGen5

    partialEnvironmentHole5 = BTreeEnvironment newSereneGenerator newValX newValY newValHole1 newValHole2 newValHole3 newValHole4 0 0 0 0 0 0 0 0 0
    initValHole5 :: StdGen -> (Integer, StdGen)
    initValHole5 curGen = (privateRandom0 (fst (getRandomInteger curGen 2)), snd (getRandomInteger curGen 2))
      where
        environment = partialEnvironmentHole5
        privateRandom0 :: Integer -> Integer
        privateRandom0 0 = 0
        privateRandom0 1 = 1
        privateRandom0 _ = 2

    (newValHole5, tempGen7) = initValHole5 tempGen6

    partialEnvironmentHole6 = BTreeEnvironment newSereneGenerator newValX newValY newValHole1 newValHole2 newValHole3 newValHole4 newValHole5 0 0 0 0 0 0 0 0
    initValHole6 :: StdGen -> (Integer, StdGen)
    initValHole6 curGen = (privateRandom0 (fst (getRandomInteger curGen 2)), snd (getRandomInteger curGen 2))
      where
        environment = partialEnvironmentHole6
        privateRandom0 :: Integer -> Integer
        privateRandom0 0 = 0
        privateRandom0 1 = 1
        privateRandom0 _ = 2

    (newValHole6, tempGen8) = initValHole6 tempGen7

    partialEnvironmentHole7 = BTreeEnvironment newSereneGenerator newValX newValY newValHole1 newValHole2 newValHole3 newValHole4 newValHole5 newValHole6 0 0 0 0 0 0 0
    initValHole7 :: StdGen -> (Integer, StdGen)
    initValHole7 curGen = (privateRandom0 (fst (getRandomInteger curGen 2)), snd (getRandomInteger curGen 2))
      where
        environment = partialEnvironmentHole7
        privateRandom0 :: Integer -> Integer
        privateRandom0 0 = 0
        privateRandom0 1 = 1
        privateRandom0 _ = 2

    (newValHole7, tempGen9) = initValHole7 tempGen8

    partialEnvironmentHole8 = BTreeEnvironment newSereneGenerator newValX newValY newValHole1 newValHole2 newValHole3 newValHole4 newValHole5 newValHole6 newValHole7 0 0 0 0 0 0
    initValHole8 :: StdGen -> (Integer, StdGen)
    initValHole8 curGen = (privateRandom0 (fst (getRandomInteger curGen 2)), snd (getRandomInteger curGen 2))
      where
        environment = partialEnvironmentHole8
        privateRandom0 :: Integer -> Integer
        privateRandom0 0 = 0
        privateRandom0 1 = 1
        privateRandom0 _ = 2

    (newValHole8, tempGen10) = initValHole8 tempGen9

    partialEnvironmentHole9 = BTreeEnvironment newSereneGenerator newValX newValY newValHole1 newValHole2 newValHole3 newValHole4 newValHole5 newValHole6 newValHole7 newValHole8 0 0 0 0 0
    initValHole9 :: StdGen -> (Integer, StdGen)
    initValHole9 curGen = (privateRandom0 (fst (getRandomInteger curGen 2)), snd (getRandomInteger curGen 2))
      where
        environment = partialEnvironmentHole9
        privateRandom0 :: Integer -> Integer
        privateRandom0 0 = 0
        privateRandom0 1 = 1
        privateRandom0 _ = 2

    (newValHole9, tempGen11) = initValHole9 tempGen10

    partialEnvironmentFlagX = BTreeEnvironment newSereneGenerator newValX newValY newValHole1 newValHole2 newValHole3 newValHole4 newValHole5 newValHole6 newValHole7 newValHole8 newValHole9 0 0 0 0
    initValFlagX :: StdGen -> (Integer, StdGen)
    initValFlagX curGen = (privateRandom0 (fst (getRandomInteger curGen 3)), snd (getRandomInteger curGen 3))
      where
        environment = partialEnvironmentFlagX
        privateRandom0 :: Integer -> Integer
        privateRandom0 0 = 15
        privateRandom0 1 = 16
        privateRandom0 2 = 17
        privateRandom0 _ = 18

    (newValFlagX, tempGen12) = initValFlagX tempGen11

    partialEnvironmentFlagY = BTreeEnvironment newSereneGenerator newValX newValY newValHole1 newValHole2 newValHole3 newValHole4 newValHole5 newValHole6 newValHole7 newValHole8 newValHole9 newValFlagX 0 0 0
    initValFlagY :: StdGen -> (Integer, StdGen)
    initValFlagY curGen = (privateRandom0 (fst (getRandomInteger curGen 2)), snd (getRandomInteger curGen 2))
      where
        environment = partialEnvironmentFlagY
        privateRandom0 :: Integer -> Integer
        privateRandom0 0 = 0
        privateRandom0 1 = 1
        privateRandom0 _ = 2

    (newValFlagY, tempGen13) = initValFlagY tempGen12

    partialEnvironmentTileProgress = BTreeEnvironment newSereneGenerator newValX newValY newValHole1 newValHole2 newValHole3 newValHole4 newValHole5 newValHole6 newValHole7 newValHole8 newValHole9 newValFlagX newValFlagY 0 0
    initValTileProgress :: StdGen -> (Integer, StdGen)
    initValTileProgress curGen = (0, curGen)
      where
        environment = partialEnvironmentTileProgress

    (newValTileProgress, tempGen14) = initValTileProgress tempGen13

    partialEnvironmentTileTracker = BTreeEnvironment newSereneGenerator newValX newValY newValHole1 newValHole2 newValHole3 newValHole4 newValHole5 newValHole6 newValHole7 newValHole8 newValHole9 newValFlagX newValFlagY newValTileProgress 0
    initValTileTracker :: StdGen -> (Integer, StdGen)
    initValTileTracker curGen = (0, curGen)
      where
        environment = partialEnvironmentTileTracker

    (newValTileTracker, tempGen15) = initValTileTracker tempGen14


