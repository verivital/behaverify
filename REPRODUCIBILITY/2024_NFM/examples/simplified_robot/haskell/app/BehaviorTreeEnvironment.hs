module BehaviorTreeEnvironment where
import SereneRandomizer
import System.Random
import SereneOperations
import BehaviorTreeBlackboard

data BTreeEnvironment = BTreeEnvironment {
  sereneEnvGenerator :: StdGen
  , envXGoal :: Integer
  , envYGoal :: Integer
  , envXTrue :: Integer
  , envYTrue :: Integer
  , envRemainingGoals :: Integer
  }

fromBTreeEnvironmentToString :: BTreeBlackboard -> BTreeEnvironment -> String
fromBTreeEnvironmentToString blackboard environment = "Env = {" ++ "envXGoal: " ++ show (envXGoal environment) ++ ", " ++ "envYGoal: " ++ show (envYGoal environment) ++ ", " ++ "envXTrue: " ++ show (envXTrue environment) ++ ", " ++ "envYTrue: " ++ show (envYTrue environment) ++ ", " ++ "envRemainingGoals: " ++ show (envRemainingGoals environment) ++ "}"

-- START OF ENVIRONMENT FUNCTIONS


-- START OF GET FUNCTIONS FOR ARRAYS


-- START OF TYPE CHECKING FUNCTIONS

checkValueEnvXGoal :: Integer -> Integer
checkValueEnvXGoal value
  | 0 > value || value > 7 = error "envXGoal illegal value"
  | otherwise = value

checkValueEnvYGoal :: Integer -> Integer
checkValueEnvYGoal value
  | 0 > value || value > 7 = error "envYGoal illegal value"
  | otherwise = value

checkValueEnvXTrue :: Integer -> Integer
checkValueEnvXTrue value
  | 0 > value || value > 7 = error "envXTrue illegal value"
  | otherwise = value

checkValueEnvYTrue :: Integer -> Integer
checkValueEnvYTrue value
  | 0 > value || value > 7 = error "envYTrue illegal value"
  | otherwise = value

checkValueEnvRemainingGoals :: Integer -> Integer
checkValueEnvRemainingGoals value
  | 0 > value || value > 3 = error "envRemainingGoals illegal value"
  | otherwise = value


-- START OF SET FUNCTIONS

updateEnvGenerator :: BTreeEnvironment -> StdGen -> BTreeEnvironment
updateEnvGenerator environment newGen = environment { sereneEnvGenerator = newGen }
updateEnvXGoal :: BTreeEnvironment -> Integer -> BTreeEnvironment
updateEnvXGoal environment value = environment { envXGoal = (checkValueEnvXGoal value)}
updateEnvYGoal :: BTreeEnvironment -> Integer -> BTreeEnvironment
updateEnvYGoal environment value = environment { envYGoal = (checkValueEnvYGoal value)}
updateEnvXTrue :: BTreeEnvironment -> Integer -> BTreeEnvironment
updateEnvXTrue environment value = environment { envXTrue = (checkValueEnvXTrue value)}
updateEnvYTrue :: BTreeEnvironment -> Integer -> BTreeEnvironment
updateEnvYTrue environment value = environment { envYTrue = (checkValueEnvYTrue value)}
updateEnvRemainingGoals :: BTreeEnvironment -> Integer -> BTreeEnvironment
updateEnvRemainingGoals environment value = environment { envRemainingGoals = (checkValueEnvRemainingGoals value)}

-- START OF SET FUNCTIONS FOR ARRAYS


-- START OF TICK CONDITION

checkTickConditionTermination :: BTreeBlackboard -> BTreeEnvironment -> Bool
checkTickConditionTermination blackboard environment = ((envRemainingGoals environment) > 0)

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
    tickUpdate1RemainingGoals :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate1RemainingGoals environment
      | (((envXGoal environment) == (envXTrue environment)) && ((envYGoal environment) == (envYTrue environment))) = updateEnvRemainingGoals environment (max 0 ((envRemainingGoals environment) - 1))
      | otherwise = updateEnvRemainingGoals environment (envRemainingGoals environment)

    tempEnvironment1 = tickUpdate1RemainingGoals tempEnvironment0

    tickUpdate2XGoal :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate2XGoal environment
      | (0 == (envRemainingGoals environment)) = updateEnvXGoal environment (envXGoal environment)
      | (((envXGoal environment) == (envXTrue environment)) && ((envYGoal environment) == (envYTrue environment))) = updateEnvGenerator (updateEnvXGoal environment (privateRandom2 (fst (getRandomInteger (sereneEnvGenerator environment) 7)))) (snd (getRandomInteger (sereneEnvGenerator environment) 7))
      | otherwise = updateEnvXGoal environment (envXGoal environment)
      where
        privateRandom2 :: Integer -> Integer
        privateRandom2 0 = 0
        privateRandom2 1 = 1
        privateRandom2 2 = 2
        privateRandom2 3 = 3
        privateRandom2 4 = 4
        privateRandom2 5 = 5
        privateRandom2 6 = 6
        privateRandom2 _ = 7

    tempEnvironment2 = tickUpdate2XGoal tempEnvironment1

    tickUpdate3YGoal :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate3YGoal environment
      | (0 == (envRemainingGoals environment)) = updateEnvYGoal environment (envYGoal environment)
      | (((envXGoal environment) == (envXTrue environment)) && ((envYGoal environment) == (envYTrue environment))) = updateEnvGenerator (updateEnvYGoal environment (privateRandom2 (fst (getRandomInteger (sereneEnvGenerator environment) 7)))) (snd (getRandomInteger (sereneEnvGenerator environment) 7))
      | otherwise = updateEnvYGoal environment (envYGoal environment)
      where
        privateRandom2 :: Integer -> Integer
        privateRandom2 0 = 0
        privateRandom2 1 = 1
        privateRandom2 2 = 2
        privateRandom2 3 = 3
        privateRandom2 4 = 4
        privateRandom2 5 = 5
        privateRandom2 6 = 6
        privateRandom2 _ = 7

    tempEnvironment3 = tickUpdate3YGoal tempEnvironment2



-- START OF INITIAL ENVIRONMENT VALUE

initialEnvironment :: Integer -> BTreeBlackboard -> BTreeEnvironment
initialEnvironment seed blackboard = BTreeEnvironment newSereneGenerator newValXGoal newValYGoal newValXTrue newValYTrue newValRemainingGoals  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen5
    partialEnvironmentXGoal = BTreeEnvironment newSereneGenerator 0 0 0 0 0
    initValXGoal :: StdGen -> (Integer, StdGen)
    initValXGoal curGen = (privateRandom0 (fst (getRandomInteger curGen 7)), snd (getRandomInteger curGen 7))
      where
        environment = partialEnvironmentXGoal
        privateRandom0 :: Integer -> Integer
        privateRandom0 0 = 0
        privateRandom0 1 = 1
        privateRandom0 2 = 2
        privateRandom0 3 = 3
        privateRandom0 4 = 4
        privateRandom0 5 = 5
        privateRandom0 6 = 6
        privateRandom0 _ = 7

    (newValXGoal, tempGen1) = initValXGoal tempGen0

    partialEnvironmentYGoal = BTreeEnvironment newSereneGenerator newValXGoal 0 0 0 0
    initValYGoal :: StdGen -> (Integer, StdGen)
    initValYGoal curGen = (privateRandom0 (fst (getRandomInteger curGen 7)), snd (getRandomInteger curGen 7))
      where
        environment = partialEnvironmentYGoal
        privateRandom0 :: Integer -> Integer
        privateRandom0 0 = 0
        privateRandom0 1 = 1
        privateRandom0 2 = 2
        privateRandom0 3 = 3
        privateRandom0 4 = 4
        privateRandom0 5 = 5
        privateRandom0 6 = 6
        privateRandom0 _ = 7

    (newValYGoal, tempGen2) = initValYGoal tempGen1

    partialEnvironmentXTrue = BTreeEnvironment newSereneGenerator newValXGoal newValYGoal 0 0 0
    initValXTrue :: StdGen -> (Integer, StdGen)
    initValXTrue curGen = (privateRandom0 (fst (getRandomInteger curGen 7)), snd (getRandomInteger curGen 7))
      where
        environment = partialEnvironmentXTrue
        privateRandom0 :: Integer -> Integer
        privateRandom0 0 = 0
        privateRandom0 1 = 1
        privateRandom0 2 = 2
        privateRandom0 3 = 3
        privateRandom0 4 = 4
        privateRandom0 5 = 5
        privateRandom0 6 = 6
        privateRandom0 _ = 7

    (newValXTrue, tempGen3) = initValXTrue tempGen2

    partialEnvironmentYTrue = BTreeEnvironment newSereneGenerator newValXGoal newValYGoal newValXTrue 0 0
    initValYTrue :: StdGen -> (Integer, StdGen)
    initValYTrue curGen = (privateRandom0 (fst (getRandomInteger curGen 7)), snd (getRandomInteger curGen 7))
      where
        environment = partialEnvironmentYTrue
        privateRandom0 :: Integer -> Integer
        privateRandom0 0 = 0
        privateRandom0 1 = 1
        privateRandom0 2 = 2
        privateRandom0 3 = 3
        privateRandom0 4 = 4
        privateRandom0 5 = 5
        privateRandom0 6 = 6
        privateRandom0 _ = 7

    (newValYTrue, tempGen4) = initValYTrue tempGen3

    partialEnvironmentRemainingGoals = BTreeEnvironment newSereneGenerator newValXGoal newValYGoal newValXTrue newValYTrue 0
    initValRemainingGoals :: StdGen -> (Integer, StdGen)
    initValRemainingGoals curGen = (privateRandom0 (fst (getRandomInteger curGen 2)), snd (getRandomInteger curGen 2))
      where
        environment = partialEnvironmentRemainingGoals
        privateRandom0 :: Integer -> Integer
        privateRandom0 0 = 1
        privateRandom0 1 = 2
        privateRandom0 _ = 3

    (newValRemainingGoals, tempGen5) = initValRemainingGoals tempGen4


