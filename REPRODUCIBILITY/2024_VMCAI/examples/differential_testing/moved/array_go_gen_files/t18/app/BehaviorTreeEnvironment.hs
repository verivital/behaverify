module BehaviorTreeEnvironment where
import SereneRandomizer
import System.Random
import SereneOperations
import BehaviorTreeBlackboard

data BTreeEnvironment = BTreeEnvironment {
  sereneEnvGenerator :: StdGen
  , envEnvVAR1Index0 :: String
  , envEnvVAR1Index1 :: String
  , envEnvVAR1Index2 :: String
  , envEnvVAR3 :: Integer
  }

fromBTreeEnvironmentToString :: BTreeBlackboard -> BTreeEnvironment -> String
fromBTreeEnvironmentToString blackboard environment = "Env = {" ++ "envEnvVAR1: " ++ "[" ++ show (envEnvVAR1 0 environment) ++ ", " ++ show (envEnvVAR1 1 environment) ++ ", " ++ show (envEnvVAR1 2 environment)++ "]" ++ ", " ++ "envEnvVAR3: " ++ show (envEnvVAR3 environment) ++ ", " ++ "envEnvDEFINE5: " ++ "[" ++ show (envEnvDEFINE5 0 blackboard environment) ++ ", " ++ show (envEnvDEFINE5 1 blackboard environment)++ "]" ++ ", " ++ "envEnvDEFINE6: " ++ "[" ++ show (envEnvDEFINE6 0 blackboard environment) ++ ", " ++ show (envEnvDEFINE6 1 blackboard environment) ++ ", " ++ show (envEnvDEFINE6 2 blackboard environment)++ "]" ++ "}"

-- START OF ENVIRONMENT FUNCTIONS

envEnvDEFINE5 :: Integer -> BTreeBlackboard -> BTreeEnvironment -> String
envEnvDEFINE5 0 blackboard environment
  | (69 > 33) = (envEnvVAR1 0 environment)
  | False = (envEnvVAR1 1 environment)
  | otherwise = "yes"
envEnvDEFINE5 1 blackboard environment = "no"
envEnvDEFINE5 _ _ _ = error "envEnvDEFINE5 illegal index value"
envEnvDEFINE6 :: Integer -> BTreeBlackboard -> BTreeEnvironment -> Integer
envEnvDEFINE6 0 blackboard environment = (min 5 (max 2 (max (- (-51)) (boardBlVAR2 1 blackboard))))
envEnvDEFINE6 1 blackboard environment
  | True = (min 5 (max 2 (envEnvVAR3 environment)))
  | otherwise = (min 5 (max 2 (min (- (-37)) (-70))))
envEnvDEFINE6 2 blackboard environment
  | ((boardBlDEFINE4 blackboard) || False) = (min 5 (max 2 (envEnvVAR3 environment)))
  | (((boardBlVAR0 1 blackboard) + ((-16) + 21)) <= (- (envEnvVAR3 environment))) = (min 5 (max 2 (34 + ((envEnvVAR3 environment) + (45 + 58)))))
  | otherwise = (min 5 (max 2 (boardBlVAR2 0 blackboard)))
envEnvDEFINE6 _ _ _ = error "envEnvDEFINE6 illegal index value"

-- START OF GET FUNCTIONS FOR ARRAYS

envEnvVAR1 :: Integer -> BTreeEnvironment -> String
envEnvVAR1 0 = envEnvVAR1Index0
envEnvVAR1 1 = envEnvVAR1Index1
envEnvVAR1 2 = envEnvVAR1Index2
envEnvVAR1 _ = error "envEnvVAR1 illegal index value"

-- START OF TYPE CHECKING FUNCTIONS

checkValueEnvEnvVAR1 :: String -> String
checkValueEnvEnvVAR1 "yes" = "yes"
checkValueEnvEnvVAR1 "no" = "no"
checkValueEnvEnvVAR1 "both" = "both"
checkValueEnvEnvVAR1 _ = error "envEnvVAR1 illegal value"

checkValueEnvEnvVAR3 :: Integer -> Integer
checkValueEnvEnvVAR3 value
  | 2 > value || value > 5 = error "envEnvVAR3 illegal value"
  | otherwise = value


-- START OF SET FUNCTIONS

updateEnvGenerator :: BTreeEnvironment -> StdGen -> BTreeEnvironment
updateEnvGenerator environment newGen = environment { sereneEnvGenerator = newGen }
updateEnvEnvVAR1Index0 :: BTreeEnvironment -> String -> BTreeEnvironment
updateEnvEnvVAR1Index0 environment value = environment { envEnvVAR1Index0 = (checkValueEnvEnvVAR1 value)}
updateEnvEnvVAR1Index1 :: BTreeEnvironment -> String -> BTreeEnvironment
updateEnvEnvVAR1Index1 environment value = environment { envEnvVAR1Index1 = (checkValueEnvEnvVAR1 value)}
updateEnvEnvVAR1Index2 :: BTreeEnvironment -> String -> BTreeEnvironment
updateEnvEnvVAR1Index2 environment value = environment { envEnvVAR1Index2 = (checkValueEnvEnvVAR1 value)}
updateEnvEnvVAR3 :: BTreeEnvironment -> Integer -> BTreeEnvironment
updateEnvEnvVAR3 environment value = environment { envEnvVAR3 = (checkValueEnvEnvVAR3 value)}

-- START OF SET FUNCTIONS FOR ARRAYS

updateEnvEnvVAR1 :: Integer -> BTreeEnvironment -> String -> BTreeEnvironment
updateEnvEnvVAR1 0 = updateEnvEnvVAR1Index0
updateEnvEnvVAR1 1 = updateEnvEnvVAR1Index1
updateEnvEnvVAR1 2 = updateEnvEnvVAR1Index2
updateEnvEnvVAR1 _ = error "EnvEnvVAR1 illegal index value"
arrayUpdateEnvEnvVAR1 :: BTreeEnvironment -> [(Integer, String)] -> BTreeEnvironment
arrayUpdateEnvEnvVAR1 environment []  = environment
arrayUpdateEnvEnvVAR1 environment [(index, value)] = updateEnvEnvVAR1 index environment value
arrayUpdateEnvEnvVAR1 environment indicesValues = environment {
  envEnvVAR1Index0 = newEnvVAR1Index0
  , envEnvVAR1Index1 = newEnvVAR1Index1
  , envEnvVAR1Index2 = newEnvVAR1Index2
  }
    where
      (newEnvVAR1Index0, newEnvVAR1Index1, newEnvVAR1Index2) = updateValues indicesValues
      updateValues :: [(Integer, String)] -> (String, String, String)
      updateValues [] = (envEnvVAR1Index0 environment, envEnvVAR1Index1 environment, envEnvVAR1Index2 environment)
      updateValues ((0, currentValue) : nextIndicesValues) = (checkValueEnvEnvVAR1 currentValue, updatedValue1, updatedValue2)
        where
          (_, updatedValue1, updatedValue2) = updateValues nextIndicesValues
      updateValues ((1, currentValue) : nextIndicesValues) = (updatedValue0, checkValueEnvEnvVAR1 currentValue, updatedValue2)
        where
          (updatedValue0, _, updatedValue2) = updateValues nextIndicesValues
      updateValues ((2, currentValue) : nextIndicesValues) = (updatedValue0, updatedValue1, checkValueEnvEnvVAR1 currentValue)
        where
          (updatedValue0, updatedValue1, _) = updateValues nextIndicesValues

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
    tickUpdate1EnvVAR1 :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate1EnvVAR1 environment = arrayUpdateEnvEnvVAR1 environment updates
      where
        updates = [updatePair0, updatePair1, updatePair2]
        updatePair0 = ((min 2 (max 0 (min (boardBlVAR2 2 blackboard) (boardBlDEFINE7 1 blackboard)))), updateValue0)
        updatePair1 = ((min 2 (max 0 ((envEnvVAR3 environment) + ((min (boardBlVAR2 1 blackboard) (envEnvVAR3 environment)) + (sereneCOUNT ((boardBlDEFINE4 blackboard) || (boardBlDEFINE4 blackboard)) ((envEnvVAR1 0 environment) /= (envEnvVAR1 1 environment))))))), updateValue1)
        updatePair2 = ((min 2 (max 0 (- (-73)))), updateValue2)
        updateValue0
          | ("both" == (envEnvDEFINE5 0 blackboard environment)) = "yes"
          | ((boardBlVAR0 0 blackboard) >= ((envEnvDEFINE6 1 blackboard environment) + ((-12) + (((envEnvVAR3 environment) - (boardBlVAR2 1 blackboard)) + (- 39))))) = "both"
          | otherwise = (envEnvVAR1 2 environment)
        updateValue1
          | ((-2) > (((-82) - (envEnvDEFINE6 1 blackboard environment)) - (94 + (37 + ((-63) + (-99)))))) = (envEnvDEFINE5 0 blackboard environment)
          | ((boardBlDEFINE7 0 blackboard) >= (envEnvVAR3 environment)) = (envEnvVAR1 1 environment)
          | otherwise = "no"
        updateValue2
          | (((-39) > (boardBlVAR0 1 blackboard)) && ((boardBlDEFINE4 blackboard) || False)) = (envEnvVAR1 0 environment)
          | True = "no"
          | otherwise = (envEnvVAR1 1 environment)

    tempEnvironment1 = tickUpdate1EnvVAR1 tempEnvironment0

    tickUpdate2EnvVAR1 :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate2EnvVAR1 environment = arrayUpdateEnvEnvVAR1 environment updates
      where
        updates = [updatePair0, updatePair1]
        updatePair0 = ((min 2 (max 0 (max (envEnvDEFINE6 1 blackboard environment) (envEnvDEFINE6 1 blackboard environment)))), updateValue0)
        updatePair1 = ((min 2 (max 0 ((abs (-83)) + ((max 38 54) + ((boardBlVAR0 0 blackboard) + (17 + ((boardBlVAR2 0 blackboard) + 90))))))), updateValue1)
        updateValue0 = (envEnvDEFINE5 0 blackboard environment)
        updateValue1 = (envEnvDEFINE5 0 blackboard environment)

    tempEnvironment2 = tickUpdate2EnvVAR1 tempEnvironment1

    tickUpdate3EnvVAR1 :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate3EnvVAR1 environment = arrayUpdateEnvEnvVAR1 environment updates
      where
        updates = [updatePair0]
        updatePair0 = ((min 2 (max 0 (min 73 3))), updateValue0)
        updateValue0 = "both"

    tempEnvironment3 = tickUpdate3EnvVAR1 tempEnvironment2

    tickUpdate4EnvVAR1 :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate4EnvVAR1 environment = arrayUpdateEnvEnvVAR1 environment updates
      where
        updates = [updatePair0, updatePair1, updatePair2]
        updatePair0 = ((min 2 (max 0 (- (- (boardBlVAR2 0 blackboard))))), updateValue0)
        updatePair1 = ((min 2 (max 0 ((boardBlVAR0 1 blackboard) - 45))), updateValue1)
        updatePair2 = ((min 2 (max 0 (boardBlDEFINE7 0 blackboard))), updateValue2)
        updateValue0
          | ((envEnvVAR1 2 environment) /= (envEnvDEFINE5 1 blackboard environment)) = "both"
          | otherwise = (envEnvDEFINE5 0 blackboard environment)
        updateValue1
          | (sereneXOR ((envEnvVAR1 0 environment) /= "both") (boardBlDEFINE4 blackboard)) = (envEnvDEFINE5 1 blackboard environment)
          | otherwise = (envEnvDEFINE5 0 blackboard environment)
        updateValue2
          | ("yes" == "yes") = (envEnvVAR1 2 environment)
          | otherwise = (envEnvDEFINE5 1 blackboard environment)

    tempEnvironment4 = tickUpdate4EnvVAR1 tempEnvironment3



-- START OF INITIAL ENVIRONMENT VALUE

initialEnvironment :: Integer -> BTreeBlackboard -> BTreeEnvironment
initialEnvironment seed blackboard = BTreeEnvironment newSereneGenerator newValEnvVAR1Index0 newValEnvVAR1Index1 newValEnvVAR1Index2 newValEnvVAR3  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen4
    partialEnvironmentEnvVAR1Index0 = BTreeEnvironment newSereneGenerator " " " " " " 0
    initValEnvVAR1Index0 :: StdGen -> (String, StdGen)
    initValEnvVAR1Index0 curGen
      | (True /= (True || False)) = ("no", curGen)
      | (((boardBlVAR0 1 blackboard) + ((boardBlVAR0 0 blackboard) + 17)) >= 39) = ("both", curGen)
      | otherwise = ("yes", curGen)
      where
        environment = partialEnvironmentEnvVAR1Index0

    (newValEnvVAR1Index0, tempGen1) = initValEnvVAR1Index0 tempGen0

    partialEnvironmentEnvVAR1Index1 = BTreeEnvironment newSereneGenerator newValEnvVAR1Index0 " " " " 0
    initValEnvVAR1Index1 :: StdGen -> (String, StdGen)
    initValEnvVAR1Index1 curGen
      | (True /= (True || False)) = ("no", curGen)
      | (((boardBlVAR0 1 blackboard) + ((boardBlVAR0 0 blackboard) + 17)) >= 39) = ("both", curGen)
      | otherwise = ("yes", curGen)
      where
        environment = partialEnvironmentEnvVAR1Index1

    (newValEnvVAR1Index1, tempGen2) = initValEnvVAR1Index1 tempGen1

    partialEnvironmentEnvVAR1Index2 = BTreeEnvironment newSereneGenerator newValEnvVAR1Index0 newValEnvVAR1Index1 " " 0
    initValEnvVAR1Index2 :: StdGen -> (String, StdGen)
    initValEnvVAR1Index2 curGen
      | (True /= (True || False)) = ("no", curGen)
      | (((boardBlVAR0 1 blackboard) + ((boardBlVAR0 0 blackboard) + 17)) >= 39) = ("both", curGen)
      | otherwise = ("yes", curGen)
      where
        environment = partialEnvironmentEnvVAR1Index2

    (newValEnvVAR1Index2, tempGen3) = initValEnvVAR1Index2 tempGen2

    partialEnvironmentEnvVAR3 = BTreeEnvironment newSereneGenerator newValEnvVAR1Index0 newValEnvVAR1Index1 newValEnvVAR1Index2 0
    initValEnvVAR3 :: StdGen -> (Integer, StdGen)
    initValEnvVAR3 curGen
      | True = ((min 5 (max 2 (max ((boardBlVAR2 2 blackboard) + (boardBlVAR0 1 blackboard)) (min (-56) 88)))), curGen)
      | (((boardBlVAR2 0 blackboard) < (boardBlVAR0 1 blackboard)) == (sereneXNOR True False)) = ((min 5 (max 2 (- (boardBlVAR2 2 blackboard)))), curGen)
      | otherwise = ((min 5 (max 2 (- (abs (-20))))), curGen)
      where
        environment = partialEnvironmentEnvVAR3

    (newValEnvVAR3, tempGen4) = initValEnvVAR3 tempGen3


