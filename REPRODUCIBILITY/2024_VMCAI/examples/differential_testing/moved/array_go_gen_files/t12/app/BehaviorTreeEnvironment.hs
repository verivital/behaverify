module BehaviorTreeEnvironment where
import SereneRandomizer
import System.Random
import SereneOperations
import BehaviorTreeBlackboard

data BTreeEnvironment = BTreeEnvironment {
  sereneEnvGenerator :: StdGen
  , envEnvVAR1 :: Integer
  , envEnvVAR2 :: String
  }

fromBTreeEnvironmentToString :: BTreeBlackboard -> BTreeEnvironment -> String
fromBTreeEnvironmentToString blackboard environment = "Env = {" ++ "envEnvVAR1: " ++ show (envEnvVAR1 environment) ++ ", " ++ "envEnvVAR2: " ++ show (envEnvVAR2 environment) ++ ", " ++ "envEnvDEFINE5: " ++ "[" ++ show (envEnvDEFINE5 0 blackboard environment) ++ ", " ++ show (envEnvDEFINE5 1 blackboard environment)++ "]" ++ ", " ++ "envEnvDEFINE6: " ++ "[" ++ show (envEnvDEFINE6 0 blackboard environment) ++ ", " ++ show (envEnvDEFINE6 1 blackboard environment) ++ ", " ++ show (envEnvDEFINE6 2 blackboard environment)++ "]" ++ "}"

-- START OF ENVIRONMENT FUNCTIONS

envEnvDEFINE5 :: Integer -> BTreeBlackboard -> BTreeEnvironment -> Integer
envEnvDEFINE5 0 blackboard environment
  | ((89 > (boardBlDEFINE3 blackboard)) || (sereneIMPLIES ((envEnvVAR1 environment) >= (-31)) False)) = (min (-2) (max (-5) (boardBlDEFINE3 blackboard)))
  | otherwise = (min (-2) (max (-5) (- (-4))))
envEnvDEFINE5 1 blackboard environment = (min (-2) (max (-5) 19))
envEnvDEFINE5 _ _ _ = error "envEnvDEFINE5 illegal index value"
envEnvDEFINE6 :: Integer -> BTreeBlackboard -> BTreeEnvironment -> Bool
envEnvDEFINE6 0 blackboard environment = (86 <= 12)
envEnvDEFINE6 1 blackboard environment = (86 <= 12)
envEnvDEFINE6 2 blackboard environment = (86 <= 12)
envEnvDEFINE6 _ _ _ = error "envEnvDEFINE6 illegal index value"

-- START OF GET FUNCTIONS FOR ARRAYS


-- START OF TYPE CHECKING FUNCTIONS

checkValueEnvEnvVAR1 :: Integer -> Integer
checkValueEnvEnvVAR1 value
  | (-5) > value || value > (-2) = error "envEnvVAR1 illegal value"
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
    newEnvironment = tempEnvironment2
    tickUpdate1EnvVAR1 :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate1EnvVAR1 environment
      | (boardBlVAR0 blackboard) = updateEnvEnvVAR1 environment (min (-2) (max (-5) (envEnvDEFINE5 0 blackboard environment)))
      | otherwise = updateEnvEnvVAR1 environment (min (-2) (max (-5) (-97)))

    tempEnvironment1 = tickUpdate1EnvVAR1 tempEnvironment0

    tickUpdate2EnvVAR2 :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate2EnvVAR2 environment
      | (envEnvDEFINE6 0 blackboard environment) = updateEnvEnvVAR2 environment (envEnvVAR2 environment)
      | otherwise = updateEnvEnvVAR2 environment (envEnvVAR2 environment)

    tempEnvironment2 = tickUpdate2EnvVAR2 tempEnvironment1



-- START OF INITIAL ENVIRONMENT VALUE

initialEnvironment :: Integer -> BTreeBlackboard -> BTreeEnvironment
initialEnvironment seed blackboard = BTreeEnvironment newSereneGenerator newValEnvVAR1 newValEnvVAR2  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen2
    partialEnvironmentEnvVAR1 = BTreeEnvironment newSereneGenerator 0 " "
    initValEnvVAR1 :: StdGen -> (Integer, StdGen)
    initValEnvVAR1 curGen
      | ((-94) > (-39)) = ((min (-2) (max (-5) 2)), curGen)
      | otherwise = ((min (-2) (max (-5) (min (-71) (abs (-3))))), curGen)
      where
        environment = partialEnvironmentEnvVAR1

    (newValEnvVAR1, tempGen1) = initValEnvVAR1 tempGen0

    partialEnvironmentEnvVAR2 = BTreeEnvironment newSereneGenerator newValEnvVAR1 " "
    initValEnvVAR2 :: StdGen -> (String, StdGen)
    initValEnvVAR2 curGen = ("no", curGen)
      where
        environment = partialEnvironmentEnvVAR2

    (newValEnvVAR2, tempGen2) = initValEnvVAR2 tempGen1


