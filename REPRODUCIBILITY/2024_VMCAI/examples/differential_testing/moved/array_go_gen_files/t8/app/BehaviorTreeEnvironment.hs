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
  , envEnvVAR3 :: Integer
  }

fromBTreeEnvironmentToString :: BTreeBlackboard -> BTreeEnvironment -> String
fromBTreeEnvironmentToString blackboard environment = "Env = {" ++ "envEnvVAR1: " ++ "[" ++ show (envEnvVAR1 0 environment) ++ ", " ++ show (envEnvVAR1 1 environment) ++ ", " ++ show (envEnvVAR1 2 environment)++ "]" ++ ", " ++ "envEnvVAR3: " ++ show (envEnvVAR3 environment) ++ ", " ++ "envEnvDEFINE9: " ++ show (envEnvDEFINE9 blackboard environment) ++ "}"

-- START OF ENVIRONMENT FUNCTIONS

envEnvDEFINE9 :: BTreeBlackboard -> BTreeEnvironment -> Integer
envEnvDEFINE9 blackboard environment
  | ((boardBlFROZENVAR6 0 blackboard) /= "both") = (min 5 (max 2 (abs (min (envEnvVAR1 2 environment) (-18)))))
  | ((envEnvVAR3 environment) >= (envEnvVAR3 environment)) = (min 5 (max 2 (min (sereneCOUNT ("yes" == "yes") (90 < (envEnvVAR1 2 environment))) ((sereneCOUNT ((sereneXNOR (boardBlVAR0 blackboard) (boardBlVAR0 blackboard)) == (boardBlVAR0 blackboard)) (((envEnvVAR3 environment) - (-41)) > (-60))) + (sereneCOUNT (sereneXOR (boardBlVAR0 blackboard) (boardBlVAR0 blackboard)) (sereneXNOR True (boardBlVAR0 blackboard)))))))
  | otherwise = (min 5 (max 2 (abs (envEnvVAR1 1 environment))))

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

checkValueEnvEnvVAR3 :: Integer -> Integer
checkValueEnvEnvVAR3 value
  | (-5) > value || value > (-2) = error "envEnvVAR3 illegal value"
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
updateEnvEnvVAR3 :: BTreeEnvironment -> Integer -> BTreeEnvironment
updateEnvEnvVAR3 environment value = environment { envEnvVAR3 = (checkValueEnvEnvVAR3 value)}

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
    newEnvironment = tempEnvironment2
    tickUpdate1EnvVAR1 :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate1EnvVAR1 environment = arrayUpdateEnvEnvVAR1 environment updates
      where
        updates = [updatePair0, updatePair1]
        updatePair0 = ((min 2 (max 0 ((envEnvVAR1 2 environment) * ((abs (abs 18)) * (envEnvVAR3 environment))))), updateValue0)
        updatePair1 = ((min 2 (max 0 ((abs (envEnvDEFINE9 blackboard environment)) + (envEnvDEFINE9 blackboard environment)))), updateValue1)
        updateValue0
          | (((sereneCOUNT (True && True) ((envEnvDEFINE9 blackboard environment) < (envEnvVAR1 0 environment))) + (sereneCOUNT ((envEnvVAR3 environment) < 82) (True == (boardBlVAR0 blackboard)))) == (0 - (-47))) = (min (-2) (max (-5) (-52)))
          | (sereneXOR ((envEnvVAR1 2 environment) > (envEnvVAR1 1 environment)) False) = (min (-2) (max (-5) 1))
          | otherwise = (min (-2) (max (-5) (max (-18) 30)))
        updateValue1
          | (sereneIMPLIES True True) = (min (-2) (max (-5) (envEnvVAR3 environment)))
          | True = (min (-2) (max (-5) (((sereneCOUNT ((-52) < (envEnvDEFINE9 blackboard environment)) (True == False)) + (sereneCOUNT False ((envEnvDEFINE9 blackboard environment) <= (-89)))) - (abs 31))))
          | otherwise = (min (-2) (max (-5) (((sereneCOUNT ((boardBlVAR0 blackboard) == False) (False && False)) + (sereneCOUNT ((envEnvDEFINE9 blackboard environment) <= 34) (True == (boardBlVAR0 blackboard)))) * ((max (-96) (envEnvDEFINE9 blackboard environment)) * ((envEnvVAR3 environment) * (abs (sereneCOUNT (25 < 67) (sereneXNOR (boardBlVAR0 blackboard) (boardBlVAR0 blackboard)))))))))

    tempEnvironment1 = tickUpdate1EnvVAR1 tempEnvironment0

    tickUpdate2EnvVAR3 :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate2EnvVAR3 environment
      | ((-92) == (-28)) = updateEnvEnvVAR3 environment (min (-2) (max (-5) (max ((sereneCOUNT ((envEnvVAR3 environment) < 6) (sereneIMPLIES (boardBlVAR0 blackboard) True)) + (sereneCOUNT False ((envEnvDEFINE9 blackboard environment) <= (-95)))) 52)))
      | (sereneXOR (boardBlVAR0 blackboard) (boardBlVAR0 blackboard)) = updateEnvEnvVAR3 environment (min (-2) (max (-5) (abs (max (envEnvVAR3 environment) (-43)))))
      | otherwise = updateEnvEnvVAR3 environment (min (-2) (max (-5) (-33)))

    tempEnvironment2 = tickUpdate2EnvVAR3 tempEnvironment1



-- START OF INITIAL ENVIRONMENT VALUE

initialEnvironment :: Integer -> BTreeBlackboard -> BTreeEnvironment
initialEnvironment seed blackboard = BTreeEnvironment newSereneGenerator newValEnvVAR1Index0 newValEnvVAR1Index1 newValEnvVAR1Index2 newValEnvVAR3  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen4
    partialEnvironmentEnvVAR1Index0 = BTreeEnvironment newSereneGenerator 0 0 0 0
    initValEnvVAR1Index0 :: StdGen -> (Integer, StdGen)
    initValEnvVAR1Index0 curGen = ((min (-2) (max (-5) (-3))), curGen)
      where
        environment = partialEnvironmentEnvVAR1Index0

    (newValEnvVAR1Index0, tempGen1) = initValEnvVAR1Index0 tempGen0

    partialEnvironmentEnvVAR1Index1 = BTreeEnvironment newSereneGenerator newValEnvVAR1Index0 0 0 0
    initValEnvVAR1Index1 :: StdGen -> (Integer, StdGen)
    initValEnvVAR1Index1 curGen = ((min (-2) (max (-5) (-3))), curGen)
      where
        environment = partialEnvironmentEnvVAR1Index1

    (newValEnvVAR1Index1, tempGen2) = initValEnvVAR1Index1 tempGen1

    partialEnvironmentEnvVAR1Index2 = BTreeEnvironment newSereneGenerator newValEnvVAR1Index0 newValEnvVAR1Index1 0 0
    initValEnvVAR1Index2 :: StdGen -> (Integer, StdGen)
    initValEnvVAR1Index2 curGen = ((min (-2) (max (-5) (-3))), curGen)
      where
        environment = partialEnvironmentEnvVAR1Index2

    (newValEnvVAR1Index2, tempGen3) = initValEnvVAR1Index2 tempGen2

    partialEnvironmentEnvVAR3 = BTreeEnvironment newSereneGenerator newValEnvVAR1Index0 newValEnvVAR1Index1 newValEnvVAR1Index2 0
    initValEnvVAR3 :: StdGen -> (Integer, StdGen)
    initValEnvVAR3 curGen = ((min (-2) (max (-5) ((sereneCOUNT (sereneXNOR (boardBlVAR0 blackboard) (sereneXNOR False False)) ((boardBlVAR0 blackboard) && (87 >= (-82)))) + (sereneCOUNT False (58 > (-26)))))), curGen)
      where
        environment = partialEnvironmentEnvVAR3

    (newValEnvVAR3, tempGen4) = initValEnvVAR3 tempGen3


