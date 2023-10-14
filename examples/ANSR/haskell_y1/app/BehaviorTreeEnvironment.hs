module BehaviorTreeEnvironment where
import SereneRandomizer
import System.Random
import SereneOperations
import BehaviorTreeBlackboard

data BTreeEnvironment = BTreeEnvironment {
    envGenerator :: StdGen
  , envTarX :: Integer
  , envTarY :: Integer
  , envTimer :: Integer
  }

fromBTreeEnvironmentToString :: BTreeBlackboard -> BTreeEnvironment -> String
fromBTreeEnvironmentToString blackboard environment = "env = {" ++ "envTreeX: " ++ (show (envTreeX blackboard environment)) ++ ", " ++ "envTreeY: " ++ (show (envTreeY blackboard environment)) ++ ", " ++ "envTarX: " ++ (show (envTarX environment)) ++ ", " ++ "envTarY: " ++ (show (envTarY environment)) ++ ", " ++ "envTimer: " ++ (show (envTimer environment)) ++ "}"

-- START OF ENVIRONMENT FUNCTIONS

envTreeX :: BTreeBlackboard -> BTreeEnvironment -> (Integer, Integer)
envTreeX blackboard environment = newVal
  where
    newUpdate0 = 5
    defaultValue0 = 2
    defaultValue1 = 2
    defaultValue = (defaultValue0, defaultValue1)
    newVal = newArrayTreeX defaultValue [(1, newUpdate0)]
envTreeY :: BTreeBlackboard -> BTreeEnvironment -> (Integer, Integer)
envTreeY blackboard environment = newVal
  where
    newUpdate0 = 5
    defaultValue0 = 2
    defaultValue1 = 2
    defaultValue = (defaultValue0, defaultValue1)
    newVal = newArrayTreeY defaultValue [(1, newUpdate0)]

-- START OF INDEX FUNCTIONS FOR ARRAYS

indexIntoTreeX :: Integer -> (Integer, Integer) -> Integer
indexIntoTreeX 0 (value, _) = value
indexIntoTreeX 1 (_, value) = value
indexIntoTreeX _ _ = error "indexIntoTreeX illegal index value"
indexIntoTreeY :: Integer -> (Integer, Integer) -> Integer
indexIntoTreeY 0 (value, _) = value
indexIntoTreeY 1 (_, value) = value
indexIntoTreeY _ _ = error "indexIntoTreeY illegal index value"

-- START OF NEW ARRAY FUNCTIONS

newArrayTreeX :: (Integer, Integer) -> [(Integer, Integer)] -> (Integer, Integer)
newArrayTreeX values  []  = values
newArrayTreeX (value0, value1) indicesValues = updateValues indicesValues
    where
      updateValues :: [(Integer, Integer)] -> (Integer, Integer)
      updateValues [] = (value0, value1)
      updateValues ((0, currentValue) : nextIndicesValues) = (currentValue, updatedValue1)
        where
          (_, updatedValue1) = updateValues nextIndicesValues
      updateValues ((1, currentValue) : nextIndicesValues) = (updatedValue0, currentValue)
        where
          (updatedValue0, _) = updateValues nextIndicesValues
newArrayTreeY :: (Integer, Integer) -> [(Integer, Integer)] -> (Integer, Integer)
newArrayTreeY values  []  = values
newArrayTreeY (value0, value1) indicesValues = updateValues indicesValues
    where
      updateValues :: [(Integer, Integer)] -> (Integer, Integer)
      updateValues [] = (value0, value1)
      updateValues ((0, currentValue) : nextIndicesValues) = (currentValue, updatedValue1)
        where
          (_, updatedValue1) = updateValues nextIndicesValues
      updateValues ((1, currentValue) : nextIndicesValues) = (updatedValue0, currentValue)
        where
          (updatedValue0, _) = updateValues nextIndicesValues

-- START OF UPDATES

envUpdateTarX :: BTreeEnvironment -> StdGen -> Integer -> BTreeEnvironment
envUpdateTarX environment newGen newVal = environment { envGenerator = newGen, envTarX = newVal }
envUpdateTarY :: BTreeEnvironment -> StdGen -> Integer -> BTreeEnvironment
envUpdateTarY environment newGen newVal = environment { envGenerator = newGen, envTarY = newVal }
envUpdateTimer :: BTreeEnvironment -> StdGen -> Integer -> BTreeEnvironment
envUpdateTimer environment newGen newVal = environment { envGenerator = newGen, envTimer = newVal }

-- START OF TICK CONDITION

checkTickConditionTermination :: BTreeBlackboard -> BTreeEnvironment -> Bool
checkTickConditionTermination blackboard environment = (not (boardVictory blackboard))

-- START OF FUTURE CHANGES

applyFutureChanges :: [(BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)] -> (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
applyFutureChanges [] = id
applyFutureChanges futureChanges = head futureChanges . applyFutureChanges (tail futureChanges)

-- START OF BETWEEN TICK CHANGES

betweenTickUpdate :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
betweenTickUpdate (blackboard, environment) = (newBlackboard, newEnvironment)
  where
    (newBlackboard, newEnvironment) = (statement2 (statement1 (statement0 (blackboard, environment))))
    statement0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    statement0 (blackboard, environment)  = (blackboard, envUpdateTarX environment newGenerator newVal)
      where
        randomPair0 = (-1, envGenerator environment)
        newGenerator = snd randomPair1
        newVal
          | ((envTimer environment) == 0) = randomNumberToResult1 (fst randomPair1)
          | otherwise = (envTarX environment)
          where
            randomNumberToResult1 :: Integer -> Integer
            randomNumberToResult1 0 = (envTarX environment)
            randomNumberToResult1 1 = (min 10 ((envTarX environment) + 1))
            randomNumberToResult1 2 = (max 0 ((envTarX environment) - 1))
            randomNumberToResult1 value = error ("randomNumberToResult1 illegal value: " ++ (show value))
        randomPair1 = getRandomInteger (snd randomPair0) 2
    statement1 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    statement1 (blackboard, environment)  = (blackboard, envUpdateTarY environment newGenerator newVal)
      where
        randomPair0 = (-1, envGenerator environment)
        newGenerator = snd randomPair1
        newVal
          | ((envTimer environment) == 0) = randomNumberToResult1 (fst randomPair1)
          | otherwise = (envTarY environment)
          where
            randomNumberToResult1 :: Integer -> Integer
            randomNumberToResult1 0 = (envTarY environment)
            randomNumberToResult1 1 = (min 10 ((envTarY environment) + 1))
            randomNumberToResult1 2 = (max 0 ((envTarY environment) - 1))
            randomNumberToResult1 value = error ("randomNumberToResult1 illegal value: " ++ (show value))
        randomPair1 = getRandomInteger (snd randomPair0) 2
    statement2 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    statement2 (blackboard, environment)  = (blackboard, envUpdateTimer environment newGenerator newVal)
      where
        randomPair0 = (-1, envGenerator environment)
        newGenerator = snd randomPair0
        newVal
          | ((envTimer environment) == 0) = 10
          | otherwise = (max 0 ((envTimer environment) - 1))

-- START OF INITIAL ENVIRONMENT VALUE

initialEnvironment :: Integer -> BTreeBlackboard -> BTreeEnvironment
initialEnvironment seed blackboard = newEnvironment
  where
    firstGen = getGenerator seed
    dummy = BTreeEnvironment firstGen 0 0 0
    statement0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    statement0 (blackboard, environment)  = (blackboard, envUpdateTarX environment newGenerator newVal)
      where
        randomPair0 = (-1, envGenerator environment)
        newGenerator = snd randomPair1
        newVal = randomNumberToResult1 (fst randomPair1)
          where
            randomNumberToResult1 :: Integer -> Integer
            randomNumberToResult1 0 = 0
            randomNumberToResult1 1 = 1
            randomNumberToResult1 2 = 2
            randomNumberToResult1 3 = 3
            randomNumberToResult1 4 = 4
            randomNumberToResult1 5 = 5
            randomNumberToResult1 6 = 6
            randomNumberToResult1 7 = 7
            randomNumberToResult1 8 = 8
            randomNumberToResult1 9 = 9
            randomNumberToResult1 10 = 10
            randomNumberToResult1 value = error ("randomNumberToResult1 illegal value: " ++ (show value))
        randomPair1 = getRandomInteger (snd randomPair0) 10
    statement1 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    statement1 (blackboard, environment)  = (blackboard, envUpdateTarY environment newGenerator newVal)
      where
        randomPair0 = (-1, envGenerator environment)
        newGenerator = snd randomPair1
        newVal = randomNumberToResult1 (fst randomPair1)
          where
            randomNumberToResult1 :: Integer -> Integer
            randomNumberToResult1 0 = 0
            randomNumberToResult1 1 = 1
            randomNumberToResult1 2 = 2
            randomNumberToResult1 3 = 3
            randomNumberToResult1 4 = 4
            randomNumberToResult1 5 = 5
            randomNumberToResult1 6 = 6
            randomNumberToResult1 7 = 7
            randomNumberToResult1 8 = 8
            randomNumberToResult1 9 = 9
            randomNumberToResult1 10 = 10
            randomNumberToResult1 value = error ("randomNumberToResult1 illegal value: " ++ (show value))
        randomPair1 = getRandomInteger (snd randomPair0) 10
    statement2 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    statement2 (blackboard, environment)  = (blackboard, envUpdateTimer environment newGenerator newVal)
      where
        randomPair0 = (-1, envGenerator environment)
        newGenerator = snd randomPair0
        newVal = 10
    (_, newEnvironment) = (statement2 (statement1 (statement0 (blackboard, dummy))))

