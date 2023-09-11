module BehaviorTreeEnvironment where
import SereneRandomizer
import System.Random
import SereneOperations
import BehaviorTreeBlackboard

data BTreeEnvironment = BTreeEnvironment {
  sereneEnvGenerator :: StdGen
  , envEnvVAR1Index0 :: Integer
  , envEnvVAR1Index1 :: Integer
  , envEnvVAR1Index2 :: Integer
  }

fromBTreeEnvironmentToString :: BTreeBlackboard -> BTreeEnvironment -> String
fromBTreeEnvironmentToString blackboard environment = "Env = {" ++ "envEnvVAR1: " ++ "[" ++ show (envEnvVAR1 0 environment) ++ ", " ++ show (envEnvVAR1 1 environment) ++ ", " ++ show (envEnvVAR1 2 environment)++ "]" ++ ", " ++ "envEnvDEFINE4: " ++ show (envEnvDEFINE4 blackboard environment) ++ "}"

-- START OF ENVIRONMENT FUNCTIONS

envEnvDEFINE4 :: BTreeBlackboard -> BTreeEnvironment -> Integer
envEnvDEFINE4 blackboard environment
  | ("yes" == (boardBlVAR0 0 blackboard)) = (min (-2) (max (-5) (min 100 (max (-100) ((min 100 (max (-100) (min (envEnvVAR1 0 environment) 5))) * ((min 100 (max (-100) (max 4 (envEnvVAR1 2 environment)))) * (min 100 (max (-100) (max (min 100 (max (-100) ((envEnvVAR1 0 environment) - (-13)))) (sereneCOUNT (True == True) ((boardBlVAR0 0 blackboard) == "yes")))))))))))
  | (sereneIMPLIES True True) = (min (-2) (max (-5) (min 100 (max (-100) ((envEnvVAR1 2 environment) - (envEnvVAR1 2 environment))))))
  | otherwise = (min (-2) (max (-5) (envEnvVAR1 2 environment)))

-- START OF GET FUNCTIONS FOR ARRAYS

envEnvVAR1 :: Integer -> BTreeEnvironment -> Integer
envEnvVAR1 0 = envEnvVAR1Index0
envEnvVAR1 1 = envEnvVAR1Index1
envEnvVAR1 2 = envEnvVAR1Index2
envEnvVAR1 _ = error "envEnvVAR1 illegal index value"

-- START OF TYPE CHECKING FUNCTIONS

checkValueEnvEnvVAR1 :: Integer -> Integer
checkValueEnvEnvVAR1 value
  | (-5) > value || value > (-2) = error "envEnvVAR1 illegal value"
  | otherwise = value


-- START OF SET FUNCTIONS

updateEnvGenerator :: BTreeEnvironment -> StdGen -> BTreeEnvironment
updateEnvGenerator environment newGen = environment { sereneEnvGenerator = newGen }
updateEnvEnvVAR1Index0 :: BTreeEnvironment -> Integer -> BTreeEnvironment
updateEnvEnvVAR1Index0 environment value = environment { envEnvVAR1Index0 = (checkValueEnvEnvVAR1 value)}
updateEnvEnvVAR1Index1 :: BTreeEnvironment -> Integer -> BTreeEnvironment
updateEnvEnvVAR1Index1 environment value = environment { envEnvVAR1Index1 = (checkValueEnvEnvVAR1 value)}
updateEnvEnvVAR1Index2 :: BTreeEnvironment -> Integer -> BTreeEnvironment
updateEnvEnvVAR1Index2 environment value = environment { envEnvVAR1Index2 = (checkValueEnvEnvVAR1 value)}

-- START OF SET FUNCTIONS FOR ARRAYS

updateEnvEnvVAR1 :: Integer -> BTreeEnvironment -> Integer -> BTreeEnvironment
updateEnvEnvVAR1 0 = updateEnvEnvVAR1Index0
updateEnvEnvVAR1 1 = updateEnvEnvVAR1Index1
updateEnvEnvVAR1 2 = updateEnvEnvVAR1Index2
updateEnvEnvVAR1 _ = error "EnvEnvVAR1 illegal index value"
arrayUpdateEnvEnvVAR1 :: BTreeEnvironment -> [(Integer, Integer)] -> BTreeEnvironment
arrayUpdateEnvEnvVAR1 environment []  = environment
arrayUpdateEnvEnvVAR1 environment [(index, value)] = updateEnvEnvVAR1 index environment value
arrayUpdateEnvEnvVAR1 environment indicesValues = environment {
  envEnvVAR1Index0 = newEnvVAR1Index0
  , envEnvVAR1Index1 = newEnvVAR1Index1
  , envEnvVAR1Index2 = newEnvVAR1Index2
  }
    where
      (newEnvVAR1Index0, newEnvVAR1Index1, newEnvVAR1Index2) = updateValues indicesValues
      updateValues :: [(Integer, Integer)] -> (Integer, Integer, Integer)
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
    newEnvironment = tempEnvironment0


-- START OF INITIAL ENVIRONMENT VALUE

initialEnvironment :: Integer -> BTreeBlackboard -> BTreeEnvironment
initialEnvironment seed blackboard = BTreeEnvironment newSereneGenerator newValEnvVAR1Index0 newValEnvVAR1Index1 newValEnvVAR1Index2  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen3
    partialEnvironmentEnvVAR1Index0 = BTreeEnvironment newSereneGenerator 0 0 0
    initValEnvVAR1Index0 :: StdGen -> (Integer, StdGen)
    initValEnvVAR1Index0 curGen = ((min (-2) (max (-5) (min 100 (max (-100) ((-4) * ((min 100 (max (-100) (abs (-3)))) * ((min 100 (max (-100) (- 5))) * (min 100 (max (-100) (80 - (-3))))))))))), curGen)
      where
        environment = partialEnvironmentEnvVAR1Index0

    (newValEnvVAR1Index0, tempGen1) = initValEnvVAR1Index0 tempGen0

    partialEnvironmentEnvVAR1Index1 = BTreeEnvironment newSereneGenerator newValEnvVAR1Index0 0 0
    initValEnvVAR1Index1 :: StdGen -> (Integer, StdGen)
    initValEnvVAR1Index1 curGen = ((min (-2) (max (-5) (min 100 (max (-100) (min 94 2))))), curGen)
      where
        environment = partialEnvironmentEnvVAR1Index1

    (newValEnvVAR1Index1, tempGen2) = initValEnvVAR1Index1 tempGen1

    partialEnvironmentEnvVAR1Index2 = BTreeEnvironment newSereneGenerator newValEnvVAR1Index0 newValEnvVAR1Index1 0
    initValEnvVAR1Index2 :: StdGen -> (Integer, StdGen)
    initValEnvVAR1Index2 curGen
      | True = ((min (-2) (max (-5) (sereneCOUNT (True == True) (3 >= 4)))), curGen)
      | False = ((min (-2) (max (-5) 4)), curGen)
      | otherwise = ((min (-2) (max (-5) (min 100 (max (-100) (abs (-3)))))), curGen)
      where
        environment = partialEnvironmentEnvVAR1Index2

    (newValEnvVAR1Index2, tempGen3) = initValEnvVAR1Index2 tempGen2


