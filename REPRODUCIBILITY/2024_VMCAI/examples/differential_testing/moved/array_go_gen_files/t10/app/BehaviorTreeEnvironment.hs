module BehaviorTreeEnvironment where
import SereneRandomizer
import System.Random
import SereneOperations
import BehaviorTreeBlackboard

data BTreeEnvironment = BTreeEnvironment {
  sereneEnvGenerator :: StdGen
  , envEnvVAR1 :: Integer
  }

fromBTreeEnvironmentToString :: BTreeBlackboard -> BTreeEnvironment -> String
fromBTreeEnvironmentToString blackboard environment = "Env = {" ++ "envEnvVAR1: " ++ show (envEnvVAR1 environment) ++ "}"

-- START OF ENVIRONMENT FUNCTIONS


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
    newEnvironment = tempEnvironment5
    tickUpdate1EnvVAR1 :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate1EnvVAR1 environment
      | (False || ((boardBlDEFINE5 0 blackboard) < (boardBlDEFINE5 0 blackboard))) = updateEnvEnvVAR1 environment (min 5 (max 2 (boardBlDEFINE5 1 blackboard)))
      | otherwise = updateEnvEnvVAR1 environment (min 5 (max 2 ((sereneCOUNT (sereneXOR False True) (True || False)) + (sereneCOUNT (False /= False) (True && False)))))

    tempEnvironment1 = tickUpdate1EnvVAR1 tempEnvironment0

    tickUpdate2EnvVAR1 :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate2EnvVAR1 environment
      | False = updateEnvEnvVAR1 environment (min 5 (max 2 ((-45) * ((-66) * (-14)))))
      | otherwise = updateEnvEnvVAR1 environment (min 5 (max 2 (max (min 50 ((sereneCOUNT (7 > 37) (sereneXNOR False True)) + (sereneCOUNT False (sereneXOR False True)))) (boardBlDEFINE5 0 blackboard))))

    tempEnvironment2 = tickUpdate2EnvVAR1 tempEnvironment1

    tickUpdate3EnvVAR1 :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate3EnvVAR1 environment
      | (sereneIMPLIES True True) = updateEnvEnvVAR1 environment (min 5 (max 2 ((boardBlDEFINE5 0 blackboard) + (((41 + (-36)) + ((boardBlDEFINE5 0 blackboard) + ((boardBlDEFINE5 0 blackboard) + (- (envEnvVAR1 environment))))) + ((((sereneCOUNT ((-10) >= (envEnvVAR1 environment)) ((envEnvVAR1 environment) < (envEnvVAR1 environment))) + (sereneCOUNT False (sereneIMPLIES False False))) + (boardBlDEFINE5 1 blackboard)) + 18)))))
      | otherwise = updateEnvEnvVAR1 environment (min 5 (max 2 (54 * (boardBlDEFINE5 1 blackboard))))

    tempEnvironment3 = tickUpdate3EnvVAR1 tempEnvironment2

    tickUpdate4EnvVAR1 :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate4EnvVAR1 environment
      | True = updateEnvEnvVAR1 environment (min 5 (max 2 (min 66 31)))
      | ((-81) <= (boardBlDEFINE5 1 blackboard)) = updateEnvEnvVAR1 environment (min 5 (max 2 (min (envEnvVAR1 environment) (boardBlDEFINE5 0 blackboard))))
      | otherwise = updateEnvEnvVAR1 environment (min 5 (max 2 (envEnvVAR1 environment)))

    tempEnvironment4 = tickUpdate4EnvVAR1 tempEnvironment3

    tickUpdate5EnvVAR1 :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate5EnvVAR1 environment = updateEnvEnvVAR1 environment (min 5 (max 2 (- ((boardBlDEFINE5 1 blackboard) * (86 * 53)))))

    tempEnvironment5 = tickUpdate5EnvVAR1 tempEnvironment4



-- START OF INITIAL ENVIRONMENT VALUE

initialEnvironment :: Integer -> BTreeBlackboard -> BTreeEnvironment
initialEnvironment seed blackboard = BTreeEnvironment newSereneGenerator newValEnvVAR1  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen1
    partialEnvironmentEnvVAR1 = BTreeEnvironment newSereneGenerator 0
    initValEnvVAR1 :: StdGen -> (Integer, StdGen)
    initValEnvVAR1 curGen
      | True = ((min 5 (max 2 ((sereneCOUNT (sereneIMPLIES (5 > 5) False) (4 <= (- (-87)))) + (sereneCOUNT (((max (-34) (-87)) - (max (-3) (-84))) < ((-4) + ((-2) + ((-5) + 3)))) (sereneXOR True (94 < (abs (-2)))))))), curGen)
      | otherwise = ((min 5 (max 2 (- (-3)))), curGen)
      where
        environment = partialEnvironmentEnvVAR1

    (newValEnvVAR1, tempGen1) = initValEnvVAR1 tempGen0


