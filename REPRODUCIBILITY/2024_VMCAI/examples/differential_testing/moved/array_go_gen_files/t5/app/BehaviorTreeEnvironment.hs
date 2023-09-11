module BehaviorTreeEnvironment where
import SereneRandomizer
import System.Random
import SereneOperations
import BehaviorTreeBlackboard

data BTreeEnvironment = BTreeEnvironment {
  sereneEnvGenerator :: StdGen
  , envEnvVAR1 :: Integer
  , envEnvFROZENVAR5 :: Integer
  }

fromBTreeEnvironmentToString :: BTreeBlackboard -> BTreeEnvironment -> String
fromBTreeEnvironmentToString blackboard environment = "Env = {" ++ "envEnvVAR1: " ++ show (envEnvVAR1 environment) ++ ", " ++ "envEnvFROZENVAR5: " ++ show (envEnvFROZENVAR5 environment) ++ ", " ++ "envEnvDEFINE7: " ++ show (envEnvDEFINE7 blackboard environment) ++ "}"

-- START OF ENVIRONMENT FUNCTIONS

envEnvDEFINE7 :: BTreeBlackboard -> BTreeEnvironment -> String
envEnvDEFINE7 blackboard environment
  | (False == False) = "no"
  | otherwise = "both"

-- START OF GET FUNCTIONS FOR ARRAYS


-- START OF TYPE CHECKING FUNCTIONS

checkValueEnvEnvVAR1 :: Integer -> Integer
checkValueEnvEnvVAR1 value
  | 2 > value || value > 5 = error "envEnvVAR1 illegal value"
  | otherwise = value


-- START OF SET FUNCTIONS

updateEnvGenerator :: BTreeEnvironment -> StdGen -> BTreeEnvironment
updateEnvGenerator environment newGen = environment { sereneEnvGenerator = newGen }
updateEnvEnvVAR1 :: BTreeEnvironment -> Integer -> BTreeEnvironment
updateEnvEnvVAR1 environment value = environment { envEnvVAR1 = (checkValueEnvEnvVAR1 value)}

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
    newEnvironment = tempEnvironment0


-- START OF INITIAL ENVIRONMENT VALUE

initialEnvironment :: Integer -> BTreeBlackboard -> BTreeEnvironment
initialEnvironment seed blackboard = BTreeEnvironment newSereneGenerator newValEnvVAR1 newValEnvFROZENVAR5  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen2
    partialEnvironmentEnvVAR1 = BTreeEnvironment newSereneGenerator 0 0
    initValEnvVAR1 :: StdGen -> (Integer, StdGen)
    initValEnvVAR1 curGen
      | (4 < 5) = ((min 5 (max 2 (min 93 (max (-91) 27)))), curGen)
      | (sereneXOR False False) = ((min 5 (max 2 (sereneCOUNT ((((-2) - (-27)) + (((sereneCOUNT ((-14) <= 4) (True == False)) + (sereneCOUNT ((-4) /= 3) (sereneIMPLIES True False))) + (2 * (2 * (4 * (-22)))))) > ((-66) + ((-23) + ((-5) + (-88))))) (sereneIMPLIES ((boardBlVAR0 blackboard) /= "yes") (False == False))))), curGen)
      | otherwise = ((min 5 (max 2 ((-60) * ((-81) * 4)))), curGen)
      where
        environment = partialEnvironmentEnvVAR1

    (newValEnvVAR1, tempGen1) = initValEnvVAR1 tempGen0

    partialEnvironmentEnvFROZENVAR5 = BTreeEnvironment newSereneGenerator newValEnvVAR1 0
    initValEnvFROZENVAR5 :: StdGen -> (Integer, StdGen)
    initValEnvFROZENVAR5 curGen = ((min 5 (max 2 (newValEnvVAR1 - (-87)))), curGen)
      where
        environment = partialEnvironmentEnvFROZENVAR5

    (newValEnvFROZENVAR5, tempGen2) = initValEnvFROZENVAR5 tempGen1


