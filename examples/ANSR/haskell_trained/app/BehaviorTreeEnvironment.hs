module BehaviorTreeEnvironment where
import SereneRandomizer
import System.Random
import SereneOperations
import BehaviorTreeBlackboard

data BTreeEnvironment = BTreeEnvironment {
  sereneEnvGenerator :: StdGen
  , envTarX :: Integer
  , envTarY :: Integer
  , envTimer :: Integer
  }

fromBTreeEnvironmentToString :: BTreeBlackboard -> BTreeEnvironment -> String
fromBTreeEnvironmentToString blackboard environment = "Env = {" ++ "envTarX: " ++ show (envTarX environment) ++ ", " ++ "envTarY: " ++ show (envTarY environment) ++ ", " ++ "envTimer: " ++ show (envTimer environment) ++ ", " ++ "envTreeX: " ++ "[" ++ show (envTreeX 0 blackboard environment) ++ ", " ++ show (envTreeX 1 blackboard environment)++ "]" ++ ", " ++ "envTreeY: " ++ "[" ++ show (envTreeY 0 blackboard environment) ++ ", " ++ show (envTreeY 1 blackboard environment)++ "]" ++ "}"

-- START OF ENVIRONMENT FUNCTIONS

envTreeX :: Integer -> BTreeBlackboard -> BTreeEnvironment -> Integer
envTreeX 0 blackboard environment = 2
envTreeX 1 blackboard environment = 5
envTreeX _ _ _ = error "envTreeX illegal index value"
envTreeY :: Integer -> BTreeBlackboard -> BTreeEnvironment -> Integer
envTreeY 0 blackboard environment = 2
envTreeY 1 blackboard environment = 5
envTreeY _ _ _ = error "envTreeY illegal index value"

-- START OF GET FUNCTIONS FOR ARRAYS


-- START OF TYPE CHECKING FUNCTIONS

checkValueEnvTarX :: Integer -> Integer
checkValueEnvTarX value
  | 0 > value || value > 10 = error "envTarX illegal value"
  | otherwise = value

checkValueEnvTarY :: Integer -> Integer
checkValueEnvTarY value
  | 0 > value || value > 10 = error "envTarY illegal value"
  | otherwise = value

checkValueEnvTimer :: Integer -> Integer
checkValueEnvTimer value
  | 0 > value || value > 10 = error "envTimer illegal value"
  | otherwise = value


-- START OF SET FUNCTIONS

updateEnvGenerator :: BTreeEnvironment -> StdGen -> BTreeEnvironment
updateEnvGenerator environment newGen = environment { sereneEnvGenerator = newGen }
updateEnvTarX :: BTreeEnvironment -> Integer -> BTreeEnvironment
updateEnvTarX environment value = environment { envTarX = (checkValueEnvTarX value)}
updateEnvTarY :: BTreeEnvironment -> Integer -> BTreeEnvironment
updateEnvTarY environment value = environment { envTarY = (checkValueEnvTarY value)}
updateEnvTimer :: BTreeEnvironment -> Integer -> BTreeEnvironment
updateEnvTimer environment value = environment { envTimer = (checkValueEnvTimer value)}

-- START OF SET FUNCTIONS FOR ARRAYS


-- START OF TICK CONDITION

checkTickConditionTermination :: BTreeBlackboard -> BTreeEnvironment -> Bool
checkTickConditionTermination blackboard environment = (not (boardVictory blackboard))

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
    tickUpdate1TarX :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate1TarX environment
      | ((envTimer environment) == 0) = updateEnvGenerator (updateEnvTarX environment (privateRandom1 (fst (getRandomInteger (sereneEnvGenerator environment) 2)))) (snd (getRandomInteger (sereneEnvGenerator environment) 2))
      | otherwise = updateEnvTarX environment (envTarX environment)
      where
        privateRandom1 :: Integer -> Integer
        privateRandom1 0 = (envTarX environment)
        privateRandom1 1 = (min 10 ((envTarX environment) + 1))
        privateRandom1 _ = (max 0 ((envTarX environment) - 1))

    tempEnvironment1 = tickUpdate1TarX tempEnvironment0

    tickUpdate2TarY :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate2TarY environment
      | ((envTimer environment) == 0) = updateEnvGenerator (updateEnvTarY environment (privateRandom1 (fst (getRandomInteger (sereneEnvGenerator environment) 2)))) (snd (getRandomInteger (sereneEnvGenerator environment) 2))
      | otherwise = updateEnvTarY environment (envTarY environment)
      where
        privateRandom1 :: Integer -> Integer
        privateRandom1 0 = (envTarY environment)
        privateRandom1 1 = (min 10 ((envTarY environment) + 1))
        privateRandom1 _ = (max 0 ((envTarY environment) - 1))

    tempEnvironment2 = tickUpdate2TarY tempEnvironment1

    tickUpdate3Timer :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate3Timer environment
      | ((envTimer environment) == 0) = updateEnvTimer environment 10
      | otherwise = updateEnvTimer environment (max 0 ((envTimer environment) - 1))

    tempEnvironment3 = tickUpdate3Timer tempEnvironment2



-- START OF INITIAL ENVIRONMENT VALUE

initialEnvironment :: Integer -> BTreeBlackboard -> BTreeEnvironment
initialEnvironment seed blackboard = BTreeEnvironment newSereneGenerator newValTarX newValTarY newValTimer  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen3
    partialEnvironmentTarX = BTreeEnvironment newSereneGenerator 0 0 0
    initValTarX :: StdGen -> (Integer, StdGen)
    initValTarX curGen = (privateRandom0 (fst (getRandomInteger curGen 10)), snd (getRandomInteger curGen 10))
      where
        environment = partialEnvironmentTarX
        privateRandom0 :: Integer -> Integer
        privateRandom0 0 = 0
        privateRandom0 1 = 1
        privateRandom0 2 = 2
        privateRandom0 3 = 3
        privateRandom0 4 = 4
        privateRandom0 5 = 5
        privateRandom0 6 = 6
        privateRandom0 7 = 7
        privateRandom0 8 = 8
        privateRandom0 9 = 9
        privateRandom0 _ = 10

    (newValTarX, tempGen1) = initValTarX tempGen0

    partialEnvironmentTarY = BTreeEnvironment newSereneGenerator newValTarX 0 0
    initValTarY :: StdGen -> (Integer, StdGen)
    initValTarY curGen = (privateRandom0 (fst (getRandomInteger curGen 10)), snd (getRandomInteger curGen 10))
      where
        environment = partialEnvironmentTarY
        privateRandom0 :: Integer -> Integer
        privateRandom0 0 = 0
        privateRandom0 1 = 1
        privateRandom0 2 = 2
        privateRandom0 3 = 3
        privateRandom0 4 = 4
        privateRandom0 5 = 5
        privateRandom0 6 = 6
        privateRandom0 7 = 7
        privateRandom0 8 = 8
        privateRandom0 9 = 9
        privateRandom0 _ = 10

    (newValTarY, tempGen2) = initValTarY tempGen1

    partialEnvironmentTimer = BTreeEnvironment newSereneGenerator newValTarX newValTarY 0
    initValTimer :: StdGen -> (Integer, StdGen)
    initValTimer curGen = (10, curGen)
      where
        environment = partialEnvironmentTimer

    (newValTimer, tempGen3) = initValTimer tempGen2


