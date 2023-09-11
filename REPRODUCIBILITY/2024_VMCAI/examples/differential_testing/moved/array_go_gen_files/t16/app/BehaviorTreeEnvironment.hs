module BehaviorTreeEnvironment where
import SereneRandomizer
import System.Random
import SereneOperations
import BehaviorTreeBlackboard

data BTreeEnvironment = BTreeEnvironment {
  sereneEnvGenerator :: StdGen
  , envEnvVAR1 :: Bool
  , envEnvVAR2 :: String
  , envEnvFROZENVAR5 :: Integer
  , envEnvFROZENVAR6Index0 :: Bool
  , envEnvFROZENVAR6Index1 :: Bool
  }

fromBTreeEnvironmentToString :: BTreeBlackboard -> BTreeEnvironment -> String
fromBTreeEnvironmentToString blackboard environment = "Env = {" ++ "envEnvVAR1: " ++ show (envEnvVAR1 environment) ++ ", " ++ "envEnvVAR2: " ++ show (envEnvVAR2 environment) ++ ", " ++ "envEnvFROZENVAR5: " ++ show (envEnvFROZENVAR5 environment) ++ ", " ++ "envEnvFROZENVAR6: " ++ "[" ++ show (envEnvFROZENVAR6 0 environment) ++ ", " ++ show (envEnvFROZENVAR6 1 environment)++ "]" ++ "}"

-- START OF ENVIRONMENT FUNCTIONS


-- START OF GET FUNCTIONS FOR ARRAYS

envEnvFROZENVAR6 :: Integer -> BTreeEnvironment -> Bool
envEnvFROZENVAR6 0 = envEnvFROZENVAR6Index0
envEnvFROZENVAR6 1 = envEnvFROZENVAR6Index1
envEnvFROZENVAR6 _ = error "envEnvFROZENVAR6 illegal index value"

-- START OF TYPE CHECKING FUNCTIONS

checkValueEnvEnvVAR1 :: Bool -> Bool
checkValueEnvEnvVAR1 value = value

checkValueEnvEnvVAR2 :: String -> String
checkValueEnvEnvVAR2 "yes" = "yes"
checkValueEnvEnvVAR2 "no" = "no"
checkValueEnvEnvVAR2 "both" = "both"
checkValueEnvEnvVAR2 _ = error "envEnvVAR2 illegal value"


-- START OF SET FUNCTIONS

updateEnvGenerator :: BTreeEnvironment -> StdGen -> BTreeEnvironment
updateEnvGenerator environment newGen = environment { sereneEnvGenerator = newGen }
updateEnvEnvVAR1 :: BTreeEnvironment -> Bool -> BTreeEnvironment
updateEnvEnvVAR1 environment value = environment { envEnvVAR1 = (checkValueEnvEnvVAR1 value)}
updateEnvEnvVAR2 :: BTreeEnvironment -> String -> BTreeEnvironment
updateEnvEnvVAR2 environment value = environment { envEnvVAR2 = (checkValueEnvEnvVAR2 value)}

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
    newEnvironment = tempEnvironment5
    tickUpdate1EnvVAR1 :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate1EnvVAR1 environment
      | False = updateEnvEnvVAR1 environment (True == (envEnvVAR1 environment))
      | otherwise = updateEnvEnvVAR1 environment (64 < 36)

    tempEnvironment1 = tickUpdate1EnvVAR1 tempEnvironment0

    tickUpdate2EnvVAR2 :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate2EnvVAR2 environment = updateEnvEnvVAR2 environment (envEnvVAR2 environment)

    tempEnvironment2 = tickUpdate2EnvVAR2 tempEnvironment1

    tickUpdate3EnvVAR2 :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate3EnvVAR2 environment
      | ((max (boardBlVAR0 blackboard) (boardBlVAR3 blackboard)) == (abs (-31))) = updateEnvEnvVAR2 environment (envEnvVAR2 environment)
      | otherwise = updateEnvEnvVAR2 environment (envEnvVAR2 environment)

    tempEnvironment3 = tickUpdate3EnvVAR2 tempEnvironment2

    tickUpdate4EnvVAR1 :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate4EnvVAR1 environment = updateEnvEnvVAR1 environment (boardBlDEFINE7 2 blackboard)

    tempEnvironment4 = tickUpdate4EnvVAR1 tempEnvironment3

    tickUpdate5EnvVAR2 :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate5EnvVAR2 environment
      | (27 == (boardBlVAR3 blackboard)) = updateEnvEnvVAR2 environment (envEnvVAR2 environment)
      | otherwise = updateEnvEnvVAR2 environment (envEnvVAR2 environment)

    tempEnvironment5 = tickUpdate5EnvVAR2 tempEnvironment4



-- START OF INITIAL ENVIRONMENT VALUE

initialEnvironment :: Integer -> BTreeBlackboard -> BTreeEnvironment
initialEnvironment seed blackboard = BTreeEnvironment newSereneGenerator newValEnvVAR1 newValEnvVAR2 newValEnvFROZENVAR5 newValEnvFROZENVAR6Index0 newValEnvFROZENVAR6Index1  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen5
    partialEnvironmentEnvVAR1 = BTreeEnvironment newSereneGenerator True " " 0 True True
    initValEnvVAR1 :: StdGen -> (Bool, StdGen)
    initValEnvVAR1 curGen
      | ((boardBlVAR0 blackboard) > (((-64) + ((-49) + ((boardBlVAR0 blackboard) + (-44)))) - ((-1) + 0))) = (False, curGen)
      | otherwise = (False, curGen)
      where
        environment = partialEnvironmentEnvVAR1

    (newValEnvVAR1, tempGen1) = initValEnvVAR1 tempGen0

    partialEnvironmentEnvVAR2 = BTreeEnvironment newSereneGenerator newValEnvVAR1 " " 0 True True
    initValEnvVAR2 :: StdGen -> (String, StdGen)
    initValEnvVAR2 curGen
      | ("yes" == "no") = ("both", curGen)
      | (88 < (-67)) = ("both", curGen)
      | otherwise = ("yes", curGen)
      where
        environment = partialEnvironmentEnvVAR2

    (newValEnvVAR2, tempGen2) = initValEnvVAR2 tempGen1

    partialEnvironmentEnvFROZENVAR5 = BTreeEnvironment newSereneGenerator newValEnvVAR1 newValEnvVAR2 0 True True
    initValEnvFROZENVAR5 :: StdGen -> (Integer, StdGen)
    initValEnvFROZENVAR5 curGen
      | (((boardBlVAR0 blackboard) + (92 + ((boardBlVAR0 blackboard) + (boardBlVAR0 blackboard)))) <= ((boardBlVAR0 blackboard) - 21)) = ((min 5 (max 2 (min (- (boardBlVAR3 blackboard)) (max 72 (-23))))), curGen)
      | otherwise = ((min 5 (max 2 ((-3) * (54 * ((boardBlVAR3 blackboard) * 20))))), curGen)
      where
        environment = partialEnvironmentEnvFROZENVAR5

    (newValEnvFROZENVAR5, tempGen3) = initValEnvFROZENVAR5 tempGen2

    partialEnvironmentEnvFROZENVAR6Index0 = BTreeEnvironment newSereneGenerator newValEnvVAR1 newValEnvVAR2 newValEnvFROZENVAR5 True True
    initValEnvFROZENVAR6Index0 :: StdGen -> (Bool, StdGen)
    initValEnvFROZENVAR6Index0 curGen
      | ("both" == "both") = ((8 >= (boardBlVAR0 blackboard)), curGen)
      | (True == newValEnvVAR1) = (False, curGen)
      | otherwise = (newValEnvVAR1, curGen)
      where
        environment = partialEnvironmentEnvFROZENVAR6Index0

    (newValEnvFROZENVAR6Index0, tempGen4) = initValEnvFROZENVAR6Index0 tempGen3

    partialEnvironmentEnvFROZENVAR6Index1 = BTreeEnvironment newSereneGenerator newValEnvVAR1 newValEnvVAR2 newValEnvFROZENVAR5 newValEnvFROZENVAR6Index0 True
    initValEnvFROZENVAR6Index1 :: StdGen -> (Bool, StdGen)
    initValEnvFROZENVAR6Index1 curGen
      | (sereneXNOR newValEnvVAR1 True) = (((boardBlVAR0 blackboard) > (boardBlVAR3 blackboard)), curGen)
      | (newValEnvVAR1 || newValEnvVAR1) = ((newValEnvVAR1 || newValEnvVAR1), curGen)
      | otherwise = (((boardBlVAR0 blackboard) < newValEnvFROZENVAR5), curGen)
      where
        environment = partialEnvironmentEnvFROZENVAR6Index1

    (newValEnvFROZENVAR6Index1, tempGen5) = initValEnvFROZENVAR6Index1 tempGen4


