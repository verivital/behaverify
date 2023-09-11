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
  , envLight :: String
  }

fromBTreeEnvironmentToString :: BTreeBlackboard -> BTreeEnvironment -> String
fromBTreeEnvironmentToString blackboard environment = "Env = {" ++ "envTunnelState: " ++ show (envTunnelState environment) ++ ", " ++ "envEastCars: " ++ show (envEastCars environment) ++ ", " ++ "envWestCars: " ++ show (envWestCars environment) ++ ", " ++ "envLight: " ++ show (envLight environment) ++ ", " ++ "envWestAndEastCars: " ++ show (envWestAndEastCars blackboard environment) ++ "}"

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

checkValueEnvLight :: String -> String
checkValueEnvLight "west_to_east" = "west_to_east"
checkValueEnvLight "east_to_west" = "east_to_west"
checkValueEnvLight "off" = "off"
checkValueEnvLight _ = error "envLight illegal value"


-- START OF SET FUNCTIONS

updateEnvGenerator :: BTreeEnvironment -> StdGen -> BTreeEnvironment
updateEnvGenerator environment newGen = environment { sereneEnvGenerator = newGen }
updateEnvTunnelState :: BTreeEnvironment -> String -> BTreeEnvironment
updateEnvTunnelState environment value = environment { envTunnelState = (checkValueEnvTunnelState value)}
updateEnvEastCars :: BTreeEnvironment -> Bool -> BTreeEnvironment
updateEnvEastCars environment value = environment { envEastCars = (checkValueEnvEastCars value)}
updateEnvWestCars :: BTreeEnvironment -> Bool -> BTreeEnvironment
updateEnvWestCars environment value = environment { envWestCars = (checkValueEnvWestCars value)}
updateEnvLight :: BTreeEnvironment -> String -> BTreeEnvironment
updateEnvLight environment value = environment { envLight = (checkValueEnvLight value)}

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
    newEnvironment = tempEnvironment4
    tickUpdate1Light :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate1Light environment
      | (boardSignal blackboard) = updateEnvLight environment (boardDirection blackboard)
      | otherwise = updateEnvLight environment "off"

    tempEnvironment1 = tickUpdate1Light tempEnvironment0

    tickUpdate2TunnelState :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate2TunnelState environment
      | ((envLight environment) == "off") = updateEnvGenerator (updateEnvTunnelState environment (privateRandom1 (fst (getRandomInteger (sereneEnvGenerator environment) 1)))) (snd (getRandomInteger (sereneEnvGenerator environment) 1))
      | otherwise = updateEnvGenerator (updateEnvTunnelState environment (privateRandom0 (fst (getRandomInteger (sereneEnvGenerator environment) 1)))) (snd (getRandomInteger (sereneEnvGenerator environment) 1))
      where
        privateRandom1 :: Integer -> String
        privateRandom1 0 = (envTunnelState environment)
        privateRandom1 _ = "empty"
        privateRandom0 :: Integer -> String
        privateRandom0 0 = (envLight environment)
        privateRandom0 _ = "empty"

    tempEnvironment2 = tickUpdate2TunnelState tempEnvironment1

    tickUpdate3WestCars :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate3WestCars environment
      | ((envLight environment) == "west_to_east") = updateEnvGenerator (updateEnvWestCars environment (privateRandom1 (fst (getRandomInteger (sereneEnvGenerator environment) 1)))) (snd (getRandomInteger (sereneEnvGenerator environment) 1))
      | otherwise = updateEnvGenerator (updateEnvWestCars environment (privateRandom0 (fst (getRandomInteger (sereneEnvGenerator environment) 1)))) (snd (getRandomInteger (sereneEnvGenerator environment) 1))
      where
        privateRandom1 :: Integer -> Bool
        privateRandom1 0 = True
        privateRandom1 _ = False
        privateRandom0 :: Integer -> Bool
        privateRandom0 0 = True
        privateRandom0 _ = (envWestCars environment)

    tempEnvironment3 = tickUpdate3WestCars tempEnvironment2

    tickUpdate4EastCars :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate4EastCars environment
      | ((envLight environment) == "east_to_west") = updateEnvGenerator (updateEnvEastCars environment (privateRandom1 (fst (getRandomInteger (sereneEnvGenerator environment) 1)))) (snd (getRandomInteger (sereneEnvGenerator environment) 1))
      | otherwise = updateEnvGenerator (updateEnvEastCars environment (privateRandom0 (fst (getRandomInteger (sereneEnvGenerator environment) 1)))) (snd (getRandomInteger (sereneEnvGenerator environment) 1))
      where
        privateRandom1 :: Integer -> Bool
        privateRandom1 0 = True
        privateRandom1 _ = False
        privateRandom0 :: Integer -> Bool
        privateRandom0 0 = True
        privateRandom0 _ = (envEastCars environment)

    tempEnvironment4 = tickUpdate4EastCars tempEnvironment3



-- START OF INITIAL ENVIRONMENT VALUE

initialEnvironment :: Integer -> BTreeBlackboard -> BTreeEnvironment
initialEnvironment seed blackboard = BTreeEnvironment newSereneGenerator newValTunnelState newValEastCars newValWestCars newValLight  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen4
    partialEnvironmentTunnelState = BTreeEnvironment newSereneGenerator " " True True " "
    initValTunnelState :: StdGen -> (String, StdGen)
    initValTunnelState curGen = ("empty", curGen)
      where
        environment = partialEnvironmentTunnelState

    (newValTunnelState, tempGen1) = initValTunnelState tempGen0

    partialEnvironmentEastCars = BTreeEnvironment newSereneGenerator newValTunnelState True True " "
    initValEastCars :: StdGen -> (Bool, StdGen)
    initValEastCars curGen = (privateRandom0 (fst (getRandomInteger curGen 1)), snd (getRandomInteger curGen 1))
      where
        environment = partialEnvironmentEastCars
        privateRandom0 :: Integer -> Bool
        privateRandom0 0 = True
        privateRandom0 _ = False

    (newValEastCars, tempGen2) = initValEastCars tempGen1

    partialEnvironmentWestCars = BTreeEnvironment newSereneGenerator newValTunnelState newValEastCars True " "
    initValWestCars :: StdGen -> (Bool, StdGen)
    initValWestCars curGen = (privateRandom0 (fst (getRandomInteger curGen 1)), snd (getRandomInteger curGen 1))
      where
        environment = partialEnvironmentWestCars
        privateRandom0 :: Integer -> Bool
        privateRandom0 0 = True
        privateRandom0 _ = False

    (newValWestCars, tempGen3) = initValWestCars tempGen2

    partialEnvironmentLight = BTreeEnvironment newSereneGenerator newValTunnelState newValEastCars newValWestCars " "
    initValLight :: StdGen -> (String, StdGen)
    initValLight curGen = ("off", curGen)
      where
        environment = partialEnvironmentLight

    (newValLight, tempGen4) = initValLight tempGen3


