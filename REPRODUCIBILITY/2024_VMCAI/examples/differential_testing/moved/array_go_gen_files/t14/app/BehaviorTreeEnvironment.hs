module BehaviorTreeEnvironment where
import SereneRandomizer
import System.Random
import SereneOperations
import BehaviorTreeBlackboard

data BTreeEnvironment = BTreeEnvironment {
  sereneEnvGenerator :: StdGen
  , envEnvVAR1 :: Integer
  , envEnvVAR2Index0 :: String
  , envEnvVAR2Index1 :: String
  , envEnvFROZENVAR3Index0 :: Integer
  , envEnvFROZENVAR3Index1 :: Integer
  }

fromBTreeEnvironmentToString :: BTreeBlackboard -> BTreeEnvironment -> String
fromBTreeEnvironmentToString blackboard environment = "Env = {" ++ "envEnvVAR1: " ++ show (envEnvVAR1 environment) ++ ", " ++ "envEnvVAR2: " ++ "[" ++ show (envEnvVAR2 0 environment) ++ ", " ++ show (envEnvVAR2 1 environment)++ "]" ++ ", " ++ "envEnvFROZENVAR3: " ++ "[" ++ show (envEnvFROZENVAR3 0 environment) ++ ", " ++ show (envEnvFROZENVAR3 1 environment)++ "]" ++ "}"

-- START OF ENVIRONMENT FUNCTIONS


-- START OF GET FUNCTIONS FOR ARRAYS

envEnvVAR2 :: Integer -> BTreeEnvironment -> String
envEnvVAR2 0 = envEnvVAR2Index0
envEnvVAR2 1 = envEnvVAR2Index1
envEnvVAR2 _ = error "envEnvVAR2 illegal index value"
envEnvFROZENVAR3 :: Integer -> BTreeEnvironment -> Integer
envEnvFROZENVAR3 0 = envEnvFROZENVAR3Index0
envEnvFROZENVAR3 1 = envEnvFROZENVAR3Index1
envEnvFROZENVAR3 _ = error "envEnvFROZENVAR3 illegal index value"

-- START OF TYPE CHECKING FUNCTIONS

checkValueEnvEnvVAR1 :: Integer -> Integer
checkValueEnvEnvVAR1 value
  | 2 > value || value > 5 = error "envEnvVAR1 illegal value"
  | otherwise = value

checkValueEnvEnvVAR2 :: String -> String
checkValueEnvEnvVAR2 "yes" = "yes"
checkValueEnvEnvVAR2 "no" = "no"
checkValueEnvEnvVAR2 "both" = "both"
checkValueEnvEnvVAR2 _ = error "envEnvVAR2 illegal value"


-- START OF SET FUNCTIONS

updateEnvGenerator :: BTreeEnvironment -> StdGen -> BTreeEnvironment
updateEnvGenerator environment newGen = environment { sereneEnvGenerator = newGen }
updateEnvEnvVAR1 :: BTreeEnvironment -> Integer -> BTreeEnvironment
updateEnvEnvVAR1 environment value = environment { envEnvVAR1 = (checkValueEnvEnvVAR1 value)}
updateEnvEnvVAR2Index0 :: BTreeEnvironment -> String -> BTreeEnvironment
updateEnvEnvVAR2Index0 environment value = environment { envEnvVAR2Index0 = (checkValueEnvEnvVAR2 value)}
updateEnvEnvVAR2Index1 :: BTreeEnvironment -> String -> BTreeEnvironment
updateEnvEnvVAR2Index1 environment value = environment { envEnvVAR2Index1 = (checkValueEnvEnvVAR2 value)}

-- START OF SET FUNCTIONS FOR ARRAYS

updateEnvEnvVAR2 :: Integer -> BTreeEnvironment -> String -> BTreeEnvironment
updateEnvEnvVAR2 0 = updateEnvEnvVAR2Index0
updateEnvEnvVAR2 1 = updateEnvEnvVAR2Index1
updateEnvEnvVAR2 _ = error "EnvEnvVAR2 illegal index value"
arrayUpdateEnvEnvVAR2 :: BTreeEnvironment -> [(Integer, String)] -> BTreeEnvironment
arrayUpdateEnvEnvVAR2 environment []  = environment
arrayUpdateEnvEnvVAR2 environment [(index, value)] = updateEnvEnvVAR2 index environment value
arrayUpdateEnvEnvVAR2 environment indicesValues = environment {
  envEnvVAR2Index0 = newEnvVAR2Index0
  , envEnvVAR2Index1 = newEnvVAR2Index1
  }
    where
      (newEnvVAR2Index0, newEnvVAR2Index1) = updateValues indicesValues
      updateValues :: [(Integer, String)] -> (String, String)
      updateValues [] = (envEnvVAR2Index0 environment, envEnvVAR2Index1 environment)
      updateValues ((0, currentValue) : nextIndicesValues) = (checkValueEnvEnvVAR2 currentValue, updatedValue1)
        where
          (_, updatedValue1) = updateValues nextIndicesValues
      updateValues ((1, currentValue) : nextIndicesValues) = (updatedValue0, checkValueEnvEnvVAR2 currentValue)
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
    newEnvironment = tempEnvironment5
    tickUpdate1EnvVAR1 :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate1EnvVAR1 environment
      | ((envEnvVAR2 1 environment) == "no") = updateEnvEnvVAR1 environment (min 5 (max 2 (min (envEnvVAR1 environment) (boardBlDEFINE5 blackboard))))
      | otherwise = updateEnvEnvVAR1 environment (min 5 (max 2 (max (envEnvVAR1 environment) (envEnvFROZENVAR3 1 environment))))

    tempEnvironment1 = tickUpdate1EnvVAR1 tempEnvironment0

    tickUpdate2EnvVAR2 :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate2EnvVAR2 environment = arrayUpdateEnvEnvVAR2 environment updates
      where
        updates = [updatePair0]
        updatePair0 = ((min 1 (max 0 (-87))), updateValue0)
        updateValue0
          | ((sereneXNOR (boardBlVAR0 1 blackboard) False) == (((sereneCOUNT (False == True) (sereneXNOR False True)) + (sereneCOUNT False ((envEnvFROZENVAR3 1 environment) >= (envEnvVAR1 environment)))) >= (envEnvFROZENVAR3 0 environment))) = (envEnvVAR2 1 environment)
          | (boardBlVAR0 2 blackboard) = "no"
          | otherwise = (envEnvVAR2 0 environment)

    tempEnvironment2 = tickUpdate2EnvVAR2 tempEnvironment1

    tickUpdate3EnvVAR2 :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate3EnvVAR2 environment = arrayUpdateEnvEnvVAR2 environment updates
      where
        updates = [updatePair0]
        updatePair0 = ((min 1 (max 0 ((envEnvFROZENVAR3 1 environment) - 55))), updateValue0)
        updateValue0 = "no"

    tempEnvironment3 = tickUpdate3EnvVAR2 tempEnvironment2

    tickUpdate4EnvVAR1 :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate4EnvVAR1 environment = updateEnvEnvVAR1 environment (min 5 (max 2 (((envEnvVAR1 environment) - (envEnvVAR1 environment)) - (abs (abs (envEnvFROZENVAR3 1 environment))))))

    tempEnvironment4 = tickUpdate4EnvVAR1 tempEnvironment3

    tickUpdate5EnvVAR2 :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate5EnvVAR2 environment = arrayUpdateEnvEnvVAR2 environment updates
      where
        updates = [updatePair0, updatePair1]
        updatePair0 = ((min 1 (max 0 (max (envEnvFROZENVAR3 1 environment) (envEnvVAR1 environment)))), updateValue0)
        updatePair1 = ((min 1 (max 0 (abs (70 * 30)))), updateValue1)
        updateValue0
          | (sereneIMPLIES (boardBlVAR0 0 blackboard) (69 >= (abs (envEnvFROZENVAR3 1 environment)))) = (envEnvVAR2 0 environment)
          | (((-14) - (-17)) == ((envEnvFROZENVAR3 1 environment) + (boardBlDEFINE5 blackboard))) = (envEnvVAR2 1 environment)
          | otherwise = "both"
        updateValue1
          | ((envEnvVAR2 1 environment) /= "no") = "no"
          | True = (envEnvVAR2 0 environment)
          | otherwise = (envEnvVAR2 1 environment)

    tempEnvironment5 = tickUpdate5EnvVAR2 tempEnvironment4



-- START OF INITIAL ENVIRONMENT VALUE

initialEnvironment :: Integer -> BTreeBlackboard -> BTreeEnvironment
initialEnvironment seed blackboard = BTreeEnvironment newSereneGenerator newValEnvVAR1 newValEnvVAR2Index0 newValEnvVAR2Index1 newValEnvFROZENVAR3Index0 newValEnvFROZENVAR3Index1  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen5
    partialEnvironmentEnvVAR1 = BTreeEnvironment newSereneGenerator 0 " " " " 0 0
    initValEnvVAR1 :: StdGen -> (Integer, StdGen)
    initValEnvVAR1 curGen = ((min 5 (max 2 (4 - (-2)))), curGen)
      where
        environment = partialEnvironmentEnvVAR1

    (newValEnvVAR1, tempGen1) = initValEnvVAR1 tempGen0

    partialEnvironmentEnvVAR2Index0 = BTreeEnvironment newSereneGenerator newValEnvVAR1 " " " " 0 0
    initValEnvVAR2Index0 :: StdGen -> (String, StdGen)
    initValEnvVAR2Index0 curGen
      | (sereneIMPLIES (boardBlVAR0 0 blackboard) (boardBlVAR0 1 blackboard)) = ("yes", curGen)
      | otherwise = ("both", curGen)
      where
        environment = partialEnvironmentEnvVAR2Index0

    (newValEnvVAR2Index0, tempGen2) = initValEnvVAR2Index0 tempGen1

    partialEnvironmentEnvVAR2Index1 = BTreeEnvironment newSereneGenerator newValEnvVAR1 newValEnvVAR2Index0 " " 0 0
    initValEnvVAR2Index1 :: StdGen -> (String, StdGen)
    initValEnvVAR2Index1 curGen
      | (sereneIMPLIES (boardBlVAR0 0 blackboard) (boardBlVAR0 1 blackboard)) = ("yes", curGen)
      | otherwise = ("both", curGen)
      where
        environment = partialEnvironmentEnvVAR2Index1

    (newValEnvVAR2Index1, tempGen3) = initValEnvVAR2Index1 tempGen2

    partialEnvironmentEnvFROZENVAR3Index0 = BTreeEnvironment newSereneGenerator newValEnvVAR1 newValEnvVAR2Index0 newValEnvVAR2Index1 0 0
    initValEnvFROZENVAR3Index0 :: StdGen -> (Integer, StdGen)
    initValEnvFROZENVAR3Index0 curGen = ((min 5 (max 2 ((sereneCOUNT (False || True) (sereneXOR (sereneXOR False ((boardBlVAR0 0 blackboard) || (boardBlVAR0 2 blackboard))) (newValEnvVAR1 < (abs (-52))))) + (sereneCOUNT ((boardBlVAR0 0 blackboard) || True) (sereneIMPLIES (sereneIMPLIES (boardBlVAR0 2 blackboard) (boardBlVAR0 1 blackboard)) ((max (-22) newValEnvVAR1) <= (- newValEnvVAR1))))))), curGen)
      where
        environment = partialEnvironmentEnvFROZENVAR3Index0

    (newValEnvFROZENVAR3Index0, tempGen4) = initValEnvFROZENVAR3Index0 tempGen3

    partialEnvironmentEnvFROZENVAR3Index1 = BTreeEnvironment newSereneGenerator newValEnvVAR1 newValEnvVAR2Index0 newValEnvVAR2Index1 newValEnvFROZENVAR3Index0 0
    initValEnvFROZENVAR3Index1 :: StdGen -> (Integer, StdGen)
    initValEnvFROZENVAR3Index1 curGen = ((min 5 (max 2 (max (max (max (-23) newValEnvVAR1) newValEnvVAR1) (abs (-63))))), curGen)
      where
        environment = partialEnvironmentEnvFROZENVAR3Index1

    (newValEnvFROZENVAR3Index1, tempGen5) = initValEnvFROZENVAR3Index1 tempGen4


