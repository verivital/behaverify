module BehaviorTreeEnvironment where
import SereneRandomizer
import System.Random
import SereneOperations
import BehaviorTreeBlackboard

data BTreeEnvironment = BTreeEnvironment {
  sereneEnvGenerator :: StdGen
  , envTunnelState :: String
  , envEastCars :: Bool
  , envWestCars :: Bool
  , envWestLight :: Bool
  , envEastLight :: Bool
  }

fromBTreeEnvironmentToString :: BTreeBlackboard -> BTreeEnvironment -> String
fromBTreeEnvironmentToString blackboard environment = "Env = {" ++ "envTunnelState: " ++ show (envTunnelState environment) ++ ", " ++ "envEastCars: " ++ show (envEastCars environment) ++ ", " ++ "envWestCars: " ++ show (envWestCars environment) ++ ", " ++ "envWestLight: " ++ show (envWestLight environment) ++ ", " ++ "envEastLight: " ++ show (envEastLight environment) ++ ", " ++ "envWestAndEastCars: " ++ show (envWestAndEastCars blackboard environment) ++ "}"

-- START OF ENVIRONMENT FUNCTIONS

envWestAndEastCars :: BTreeBlackboard -> BTreeEnvironment -> Bool
envWestAndEastCars blackboard environment = ((envWestCars environment) && (envEastCars environment))

-- START OF GET FUNCTIONS FOR ARRAYS


-- START OF TYPE CHECKING FUNCTIONS

checkValueEnvTunnelState :: String -> String
checkValueEnvTunnelState "empty" = "empty"
checkValueEnvTunnelState "east_to_west" = "east_to_west"
checkValueEnvTunnelState "west_to_east" = "west_to_east"
checkValueEnvTunnelState _ = error "envTunnelState illegal value"

checkValueEnvEastCars :: Bool -> Bool
checkValueEnvEastCars value = value

checkValueEnvWestCars :: Bool -> Bool
checkValueEnvWestCars value = value

checkValueEnvWestLight :: Bool -> Bool
checkValueEnvWestLight value = value

checkValueEnvEastLight :: Bool -> Bool
checkValueEnvEastLight value = value


-- START OF SET FUNCTIONS

updateEnvGenerator :: BTreeEnvironment -> StdGen -> BTreeEnvironment
updateEnvGenerator environment newGen = environment { sereneEnvGenerator = newGen }
updateEnvTunnelState :: BTreeEnvironment -> String -> BTreeEnvironment
updateEnvTunnelState environment value = environment { envTunnelState = (checkValueEnvTunnelState value)}
updateEnvEastCars :: BTreeEnvironment -> Bool -> BTreeEnvironment
updateEnvEastCars environment value = environment { envEastCars = (checkValueEnvEastCars value)}
updateEnvWestCars :: BTreeEnvironment -> Bool -> BTreeEnvironment
updateEnvWestCars environment value = environment { envWestCars = (checkValueEnvWestCars value)}
updateEnvWestLight :: BTreeEnvironment -> Bool -> BTreeEnvironment
updateEnvWestLight environment value = environment { envWestLight = (checkValueEnvWestLight value)}
updateEnvEastLight :: BTreeEnvironment -> Bool -> BTreeEnvironment
updateEnvEastLight environment value = environment { envEastLight = (checkValueEnvEastLight value)}

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
    newEnvironment = tempEnvironment3
    tickUpdate1TunnelState :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate1TunnelState environment
      | (envWestLight environment) = updateEnvGenerator (updateEnvTunnelState environment (privateRandom1 (fst (getRandomInteger (sereneEnvGenerator environment) 1)))) (snd (getRandomInteger (sereneEnvGenerator environment) 1))
      | (envEastLight environment) = updateEnvGenerator (updateEnvTunnelState environment (privateRandom2 (fst (getRandomInteger (sereneEnvGenerator environment) 1)))) (snd (getRandomInteger (sereneEnvGenerator environment) 1))
      | otherwise = updateEnvGenerator (updateEnvTunnelState environment (privateRandom0 (fst (getRandomInteger (sereneEnvGenerator environment) 1)))) (snd (getRandomInteger (sereneEnvGenerator environment) 1))
      where
        privateRandom1 :: Integer -> String
        privateRandom1 0 = "empty"
        privateRandom1 _ = "west_to_east"
        privateRandom2 :: Integer -> String
        privateRandom2 0 = "empty"
        privateRandom2 _ = "east_to_west"
        privateRandom0 :: Integer -> String
        privateRandom0 0 = "empty"
        privateRandom0 _ = (envTunnelState environment)

    tempEnvironment1 = tickUpdate1TunnelState tempEnvironment0

    tickUpdate2WestCars :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate2WestCars environment
      | (envWestLight environment) = updateEnvGenerator (updateEnvWestCars environment (privateRandom1 (fst (getRandomInteger (sereneEnvGenerator environment) 1)))) (snd (getRandomInteger (sereneEnvGenerator environment) 1))
      | otherwise = updateEnvGenerator (updateEnvWestCars environment (privateRandom0 (fst (getRandomInteger (sereneEnvGenerator environment) 1)))) (snd (getRandomInteger (sereneEnvGenerator environment) 1))
      where
        privateRandom1 :: Integer -> Bool
        privateRandom1 0 = True
        privateRandom1 _ = False
        privateRandom0 :: Integer -> Bool
        privateRandom0 0 = True
        privateRandom0 _ = (envWestCars environment)

    tempEnvironment2 = tickUpdate2WestCars tempEnvironment1

    tickUpdate3EastCars :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate3EastCars environment
      | (envEastLight environment) = updateEnvGenerator (updateEnvEastCars environment (privateRandom1 (fst (getRandomInteger (sereneEnvGenerator environment) 1)))) (snd (getRandomInteger (sereneEnvGenerator environment) 1))
      | otherwise = updateEnvGenerator (updateEnvEastCars environment (privateRandom0 (fst (getRandomInteger (sereneEnvGenerator environment) 1)))) (snd (getRandomInteger (sereneEnvGenerator environment) 1))
      where
        privateRandom1 :: Integer -> Bool
        privateRandom1 0 = True
        privateRandom1 _ = False
        privateRandom0 :: Integer -> Bool
        privateRandom0 0 = True
        privateRandom0 _ = (envEastCars environment)

    tempEnvironment3 = tickUpdate3EastCars tempEnvironment2



-- START OF INITIAL ENVIRONMENT VALUE

initialEnvironment :: Integer -> BTreeBlackboard -> BTreeEnvironment
initialEnvironment seed blackboard = BTreeEnvironment newSereneGenerator newValTunnelState newValEastCars newValWestCars newValWestLight newValEastLight  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen5
    partialEnvironmentTunnelState = BTreeEnvironment newSereneGenerator " " True True True True
    initValTunnelState :: StdGen -> (String, StdGen)
    initValTunnelState curGen = ("empty", curGen)
      where
        environment = partialEnvironmentTunnelState

    (newValTunnelState, tempGen1) = initValTunnelState tempGen0

    partialEnvironmentEastCars = BTreeEnvironment newSereneGenerator newValTunnelState True True True True
    initValEastCars :: StdGen -> (Bool, StdGen)
    initValEastCars curGen = (privateRandom0 (fst (getRandomInteger curGen 1)), snd (getRandomInteger curGen 1))
      where
        environment = partialEnvironmentEastCars
        privateRandom0 :: Integer -> Bool
        privateRandom0 0 = True
        privateRandom0 _ = False

    (newValEastCars, tempGen2) = initValEastCars tempGen1

    partialEnvironmentWestCars = BTreeEnvironment newSereneGenerator newValTunnelState newValEastCars True True True
    initValWestCars :: StdGen -> (Bool, StdGen)
    initValWestCars curGen = (privateRandom0 (fst (getRandomInteger curGen 1)), snd (getRandomInteger curGen 1))
      where
        environment = partialEnvironmentWestCars
        privateRandom0 :: Integer -> Bool
        privateRandom0 0 = True
        privateRandom0 _ = False

    (newValWestCars, tempGen3) = initValWestCars tempGen2

    partialEnvironmentWestLight = BTreeEnvironment newSereneGenerator newValTunnelState newValEastCars newValWestCars True True
    initValWestLight :: StdGen -> (Bool, StdGen)
    initValWestLight curGen = (False, curGen)
      where
        environment = partialEnvironmentWestLight

    (newValWestLight, tempGen4) = initValWestLight tempGen3

    partialEnvironmentEastLight = BTreeEnvironment newSereneGenerator newValTunnelState newValEastCars newValWestCars newValWestLight True
    initValEastLight :: StdGen -> (Bool, StdGen)
    initValEastLight curGen = (False, curGen)
      where
        environment = partialEnvironmentEastLight

    (newValEastLight, tempGen5) = initValEastLight tempGen4


