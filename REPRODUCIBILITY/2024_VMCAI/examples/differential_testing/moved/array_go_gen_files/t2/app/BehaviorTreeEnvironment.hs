module BehaviorTreeEnvironment where
import SereneRandomizer
import System.Random
import SereneOperations
import BehaviorTreeBlackboard

data BTreeEnvironment = BTreeEnvironment {
  sereneEnvGenerator :: StdGen
  , envEnvVAR1 :: Bool
  }

fromBTreeEnvironmentToString :: BTreeBlackboard -> BTreeEnvironment -> String
fromBTreeEnvironmentToString blackboard environment = "Env = {" ++ "envEnvVAR1: " ++ show (envEnvVAR1 environment) ++ ", " ++ "envEnvDEFINE5: " ++ show (envEnvDEFINE5 blackboard environment) ++ ", " ++ "envEnvDEFINE6: " ++ show (envEnvDEFINE6 blackboard environment) ++ ", " ++ "envEnvDEFINE7: " ++ show (envEnvDEFINE7 blackboard environment) ++ ", " ++ "envEnvDEFINE8: " ++ "[" ++ show (envEnvDEFINE8 0 blackboard environment) ++ ", " ++ show (envEnvDEFINE8 1 blackboard environment)++ "]" ++ "}"

-- START OF ENVIRONMENT FUNCTIONS

envEnvDEFINE5 :: BTreeBlackboard -> BTreeEnvironment -> Integer
envEnvDEFINE5 blackboard environment = (min (-2) (max (-5) (-16)))
envEnvDEFINE6 :: BTreeBlackboard -> BTreeEnvironment -> String
envEnvDEFINE6 blackboard environment = (boardBlVAR2 blackboard)
envEnvDEFINE7 :: BTreeBlackboard -> BTreeEnvironment -> Integer
envEnvDEFINE7 blackboard environment
  | ((boardBlVAR2 blackboard) /= "yes") = (min 5 (max 2 (min 100 (max (-100) ((min 100 (max (-100) (abs (min 100 (max (-100) (min (envEnvDEFINE5 blackboard environment) 19)))))) - ((sereneCOUNT (sereneXOR (sereneXOR (envEnvVAR1 environment) (envEnvVAR1 environment)) True) ((min 100 (max (-100) ((envEnvDEFINE5 blackboard environment) - 94))) < (min 100 (max (-100) (min (boardBlVAR0 blackboard) (envEnvDEFINE5 blackboard environment)))))) + (sereneCOUNT ((True && (envEnvVAR1 environment)) && (sereneIMPLIES True False)) ((sereneXOR (envEnvVAR1 environment) False) && (envEnvVAR1 environment)))))))))
  | ((min 100 (max (-100) (- 0))) > (min 100 (max (-100) ((envEnvDEFINE5 blackboard environment) * ((envEnvDEFINE5 blackboard environment) * ((boardBlVAR0 blackboard) * (envEnvDEFINE5 blackboard environment))))))) = (min 5 (max 2 (sereneCOUNT (sereneIMPLIES (envEnvVAR1 environment) ((envEnvVAR1 environment) == True)) (sereneXOR (sereneXNOR ((envEnvVAR1 environment) && True) False) ((sereneXNOR (envEnvVAR1 environment) False) || ((boardBlVAR0 blackboard) < (envEnvDEFINE5 blackboard environment)))))))
  | otherwise = (min 5 (max 2 (min 100 (max (-100) (max (boardBlVAR0 blackboard) (envEnvDEFINE5 blackboard environment))))))
envEnvDEFINE8 :: Integer -> BTreeBlackboard -> BTreeEnvironment -> Integer
envEnvDEFINE8 0 blackboard environment = (min 5 (max 2 (envEnvDEFINE7 blackboard environment)))
envEnvDEFINE8 1 blackboard environment
  | ((sereneXNOR (envEnvVAR1 environment) (envEnvVAR1 environment)) && (sereneIMPLIES False True)) = (min 5 (max 2 (min 100 (max (-100) (- (-91))))))
  | otherwise = (min 5 (max 2 (min 100 (max (-100) (78 * ((-16) * 72))))))
envEnvDEFINE8 _ _ _ = error "envEnvDEFINE8 illegal index value"

-- START OF GET FUNCTIONS FOR ARRAYS


-- START OF TYPE CHECKING FUNCTIONS

checkValueEnvEnvVAR1 :: Bool -> Bool
checkValueEnvEnvVAR1 value = value


-- START OF SET FUNCTIONS

updateEnvGenerator :: BTreeEnvironment -> StdGen -> BTreeEnvironment
updateEnvGenerator environment newGen = environment { sereneEnvGenerator = newGen }
updateEnvEnvVAR1 :: BTreeEnvironment -> Bool -> BTreeEnvironment
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
    newEnvironment = tempEnvironment1
    tickUpdate1EnvVAR1 :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate1EnvVAR1 environment = updateEnvEnvVAR1 environment True

    tempEnvironment1 = tickUpdate1EnvVAR1 tempEnvironment0



-- START OF INITIAL ENVIRONMENT VALUE

initialEnvironment :: Integer -> BTreeBlackboard -> BTreeEnvironment
initialEnvironment seed blackboard = BTreeEnvironment newSereneGenerator newValEnvVAR1  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen1
    partialEnvironmentEnvVAR1 = BTreeEnvironment newSereneGenerator True
    initValEnvVAR1 :: StdGen -> (Bool, StdGen)
    initValEnvVAR1 curGen = (True, curGen)
      where
        environment = partialEnvironmentEnvVAR1

    (newValEnvVAR1, tempGen1) = initValEnvVAR1 tempGen0


