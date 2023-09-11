module BehaviorTreeEnvironment where
import SereneRandomizer
import System.Random
import SereneOperations
import BehaviorTreeBlackboard

data BTreeEnvironment = BTreeEnvironment {
  sereneEnvGenerator :: StdGen
  , envEnvVAR1Index0 :: Integer
  , envEnvVAR1Index1 :: Integer
  }

fromBTreeEnvironmentToString :: BTreeBlackboard -> BTreeEnvironment -> String
fromBTreeEnvironmentToString blackboard environment = "Env = {" ++ "envEnvVAR1: " ++ "[" ++ show (envEnvVAR1 0 environment) ++ ", " ++ show (envEnvVAR1 1 environment)++ "]" ++ "}"

-- START OF ENVIRONMENT FUNCTIONS


-- START OF GET FUNCTIONS FOR ARRAYS

envEnvVAR1 :: Integer -> BTreeEnvironment -> Integer
envEnvVAR1 0 = envEnvVAR1Index0
envEnvVAR1 1 = envEnvVAR1Index1
envEnvVAR1 _ = error "envEnvVAR1 illegal index value"

-- START OF TYPE CHECKING FUNCTIONS

checkValueEnvEnvVAR1 :: Integer -> Integer
checkValueEnvEnvVAR1 value
  | 2 > value || value > 5 = error "envEnvVAR1 illegal value"
  | otherwise = value


-- START OF SET FUNCTIONS

updateEnvGenerator :: BTreeEnvironment -> StdGen -> BTreeEnvironment
updateEnvGenerator environment newGen = environment { sereneEnvGenerator = newGen }
updateEnvEnvVAR1Index0 :: BTreeEnvironment -> Integer -> BTreeEnvironment
updateEnvEnvVAR1Index0 environment value = environment { envEnvVAR1Index0 = (checkValueEnvEnvVAR1 value)}
updateEnvEnvVAR1Index1 :: BTreeEnvironment -> Integer -> BTreeEnvironment
updateEnvEnvVAR1Index1 environment value = environment { envEnvVAR1Index1 = (checkValueEnvEnvVAR1 value)}

-- START OF SET FUNCTIONS FOR ARRAYS

updateEnvEnvVAR1 :: Integer -> BTreeEnvironment -> Integer -> BTreeEnvironment
updateEnvEnvVAR1 0 = updateEnvEnvVAR1Index0
updateEnvEnvVAR1 1 = updateEnvEnvVAR1Index1
updateEnvEnvVAR1 _ = error "EnvEnvVAR1 illegal index value"
arrayUpdateEnvEnvVAR1 :: BTreeEnvironment -> [(Integer, Integer)] -> BTreeEnvironment
arrayUpdateEnvEnvVAR1 environment []  = environment
arrayUpdateEnvEnvVAR1 environment [(index, value)] = updateEnvEnvVAR1 index environment value
arrayUpdateEnvEnvVAR1 environment indicesValues = environment {
  envEnvVAR1Index0 = newEnvVAR1Index0
  , envEnvVAR1Index1 = newEnvVAR1Index1
  }
    where
      (newEnvVAR1Index0, newEnvVAR1Index1) = updateValues indicesValues
      updateValues :: [(Integer, Integer)] -> (Integer, Integer)
      updateValues [] = (envEnvVAR1Index0 environment, envEnvVAR1Index1 environment)
      updateValues ((0, currentValue) : nextIndicesValues) = (checkValueEnvEnvVAR1 currentValue, updatedValue1)
        where
          (_, updatedValue1) = updateValues nextIndicesValues
      updateValues ((1, currentValue) : nextIndicesValues) = (updatedValue0, checkValueEnvEnvVAR1 currentValue)
        where
          (updatedValue0, _) = updateValues nextIndicesValues

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
    tickUpdate1EnvVAR1 :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate1EnvVAR1 environment = arrayUpdateEnvEnvVAR1 environment updates
      where
        updates = [updatePair0, updatePair1]
        updatePair0 = ((min 1 (max 0 (max (boardBlDEFINE5 blackboard) (envEnvVAR1 0 environment)))), updateValue0)
        updatePair1 = ((min 1 (max 0 (-14))), updateValue1)
        updateValue0
          | ((envEnvVAR1 1 environment) /= (abs 95)) = (min 5 (max 2 (envEnvVAR1 0 environment)))
          | ((envEnvVAR1 0 environment) >= (-68)) = (min 5 (max 2 ((boardBlVAR0 0 blackboard) - (boardBlVAR0 1 blackboard))))
          | otherwise = (min 5 (max 2 (- 41)))
        updateValue1
          | True = (min 5 (max 2 ((sereneCOUNT (((boardBlDEFINE5 blackboard) + ((-47) + ((-100) + (boardBlDEFINE5 blackboard)))) <= 4) (sereneIMPLIES (sereneIMPLIES True False) (True || False))) + (sereneCOUNT ((max (envEnvVAR1 0 environment) (boardBlVAR0 1 blackboard)) /= 90) ((abs (-58)) /= (99 + ((-64) + ((boardBlVAR0 0 blackboard) + 79))))))))
          | ((envEnvVAR1 1 environment) > 26) = (min 5 (max 2 ((envEnvVAR1 1 environment) * ((-14) * ((-4) * (envEnvVAR1 0 environment))))))
          | otherwise = (min 5 (max 2 (boardBlVAR0 0 blackboard)))

    tempEnvironment1 = tickUpdate1EnvVAR1 tempEnvironment0

    tickUpdate2EnvVAR1 :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate2EnvVAR1 environment = arrayUpdateEnvEnvVAR1 environment updates
      where
        updates = [updatePair0]
        updatePair0 = ((min 1 (max 0 81)), updateValue0)
        updateValue0 = (min 5 (max 2 (max (boardBlDEFINE5 blackboard) (envEnvVAR1 0 environment))))

    tempEnvironment2 = tickUpdate2EnvVAR1 tempEnvironment1



-- START OF INITIAL ENVIRONMENT VALUE

initialEnvironment :: Integer -> BTreeBlackboard -> BTreeEnvironment
initialEnvironment seed blackboard = BTreeEnvironment newSereneGenerator newValEnvVAR1Index0 newValEnvVAR1Index1  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen2
    partialEnvironmentEnvVAR1Index0 = BTreeEnvironment newSereneGenerator 0 0
    initValEnvVAR1Index0 :: StdGen -> (Integer, StdGen)
    initValEnvVAR1Index0 curGen
      | True = ((min 5 (max 2 (min (boardBlVAR0 0 blackboard) 72))), curGen)
      | False = ((min 5 (max 2 (min ((sereneCOUNT (False == True) (False && True)) + (sereneCOUNT (False == True) (False || True))) (max (max (-6) 50) ((sereneCOUNT ((-55) >= (boardBlVAR0 1 blackboard)) (False == False)) + (sereneCOUNT (True || False) ((boardBlVAR0 1 blackboard) > (boardBlVAR0 1 blackboard)))))))), curGen)
      | otherwise = ((min 5 (max 2 (min (min (boardBlVAR0 0 blackboard) (-89)) (-50)))), curGen)
      where
        environment = partialEnvironmentEnvVAR1Index0

    (newValEnvVAR1Index0, tempGen1) = initValEnvVAR1Index0 tempGen0

    partialEnvironmentEnvVAR1Index1 = BTreeEnvironment newSereneGenerator newValEnvVAR1Index0 0
    initValEnvVAR1Index1 :: StdGen -> (Integer, StdGen)
    initValEnvVAR1Index1 curGen
      | True = ((min 5 (max 2 (min (boardBlVAR0 0 blackboard) 72))), curGen)
      | False = ((min 5 (max 2 (min ((sereneCOUNT (False == True) (False && True)) + (sereneCOUNT (False == True) (False || True))) (max (max (-6) 50) ((sereneCOUNT ((-55) >= (boardBlVAR0 1 blackboard)) (False == False)) + (sereneCOUNT (True || False) ((boardBlVAR0 1 blackboard) > (boardBlVAR0 1 blackboard)))))))), curGen)
      | otherwise = ((min 5 (max 2 (min (min (boardBlVAR0 0 blackboard) (-89)) (-50)))), curGen)
      where
        environment = partialEnvironmentEnvVAR1Index1

    (newValEnvVAR1Index1, tempGen2) = initValEnvVAR1Index1 tempGen1


