module BehaviorTreeEnvironment where
import SereneRandomizer
import System.Random
import SereneOperations
import BehaviorTreeBlackboard

data BTreeEnvironment = BTreeEnvironment {
  sereneEnvGenerator :: StdGen
  , envEnvVAR1 :: Integer
  , envEnvFROZENVAR3Index0 :: Integer
  , envEnvFROZENVAR3Index1 :: Integer
  , envEnvFROZENVAR3Index2 :: Integer
  }

fromBTreeEnvironmentToString :: BTreeBlackboard -> BTreeEnvironment -> String
fromBTreeEnvironmentToString blackboard environment = "Env = {" ++ "envEnvVAR1: " ++ show (envEnvVAR1 environment) ++ ", " ++ "envEnvFROZENVAR3: " ++ "[" ++ show (envEnvFROZENVAR3 0 environment) ++ ", " ++ show (envEnvFROZENVAR3 1 environment) ++ ", " ++ show (envEnvFROZENVAR3 2 environment)++ "]" ++ ", " ++ "envEnvDEFINE5: " ++ show (envEnvDEFINE5 blackboard environment) ++ "}"

-- START OF ENVIRONMENT FUNCTIONS

envEnvDEFINE5 :: BTreeBlackboard -> BTreeEnvironment -> Bool
envEnvDEFINE5 blackboard environment = (sereneXNOR ((envEnvFROZENVAR3 1 environment) /= (boardBlVAR0 1 blackboard)) True)

-- START OF GET FUNCTIONS FOR ARRAYS

envEnvFROZENVAR3 :: Integer -> BTreeEnvironment -> Integer
envEnvFROZENVAR3 0 = envEnvFROZENVAR3Index0
envEnvFROZENVAR3 1 = envEnvFROZENVAR3Index1
envEnvFROZENVAR3 2 = envEnvFROZENVAR3Index2
envEnvFROZENVAR3 _ = error "envEnvFROZENVAR3 illegal index value"

-- START OF TYPE CHECKING FUNCTIONS

checkValueEnvEnvVAR1 :: Integer -> Integer
checkValueEnvEnvVAR1 value
  | (-5) > value || value > (-2) = error "envEnvVAR1 illegal value"
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
      | (False /= True) = updateEnvEnvVAR1 environment (min (-2) (max (-5) ((sereneCOUNT ((envEnvVAR1 environment) >= 53) (sereneIMPLIES True (sereneXOR True True))) + (sereneCOUNT (sereneIMPLIES False (False == False)) (sereneIMPLIES (93 >= (envEnvVAR1 environment)) ((min 100 (max (-100) ((boardBlVAR2 blackboard) + ((envEnvFROZENVAR3 1 environment) + (-17))))) < (boardBlDEFINE4 blackboard)))))))
      | otherwise = updateEnvEnvVAR1 environment (min (-2) (max (-5) (-88)))

    tempEnvironment1 = tickUpdate1EnvVAR1 tempEnvironment0

    tickUpdate2EnvVAR1 :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate2EnvVAR1 environment
      | (False && (envEnvDEFINE5 blackboard environment)) = updateEnvEnvVAR1 environment (min (-2) (max (-5) (min 100 (max (-100) ((envEnvFROZENVAR3 2 environment) - (min 100 (max (-100) (- (envEnvFROZENVAR3 2 environment)))))))))
      | otherwise = updateEnvEnvVAR1 environment (min (-2) (max (-5) (min 100 (max (-100) ((min 100 (max (-100) (57 + ((envEnvVAR1 environment) + ((-37) + 75))))) - (envEnvVAR1 environment))))))

    tempEnvironment2 = tickUpdate2EnvVAR1 tempEnvironment1

    tickUpdate3EnvVAR1 :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate3EnvVAR1 environment
      | (envEnvDEFINE5 blackboard environment) = updateEnvEnvVAR1 environment (min (-2) (max (-5) (min 100 (max (-100) (- (envEnvFROZENVAR3 1 environment))))))
      | otherwise = updateEnvEnvVAR1 environment (min (-2) (max (-5) (min 100 (max (-100) ((boardBlVAR2 blackboard) + (envEnvVAR1 environment))))))

    tempEnvironment3 = tickUpdate3EnvVAR1 tempEnvironment2

    tickUpdate4EnvVAR1 :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate4EnvVAR1 environment = updateEnvEnvVAR1 environment (min (-2) (max (-5) (min 100 (max (-100) (45 + ((boardBlVAR0 1 blackboard) + (boardBlVAR2 blackboard)))))))

    tempEnvironment4 = tickUpdate4EnvVAR1 tempEnvironment3

    tickUpdate5EnvVAR1 :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate5EnvVAR1 environment
      | (sereneXNOR (envEnvDEFINE5 blackboard environment) ((-35) < (-64))) = updateEnvEnvVAR1 environment (min (-2) (max (-5) (min 100 (max (-100) (abs (min 100 (max (-100) (37 - (boardBlVAR0 0 blackboard)))))))))
      | otherwise = updateEnvEnvVAR1 environment (min (-2) (max (-5) (min 100 (max (-100) (abs ((sereneCOUNT (sereneXNOR False (envEnvDEFINE5 blackboard environment)) ((boardBlDEFINE4 blackboard) >= (-19))) + (sereneCOUNT False (sereneXOR (envEnvDEFINE5 blackboard environment) (envEnvDEFINE5 blackboard environment)))))))))

    tempEnvironment5 = tickUpdate5EnvVAR1 tempEnvironment4



-- START OF INITIAL ENVIRONMENT VALUE

initialEnvironment :: Integer -> BTreeBlackboard -> BTreeEnvironment
initialEnvironment seed blackboard = BTreeEnvironment newSereneGenerator newValEnvVAR1 newValEnvFROZENVAR3Index0 newValEnvFROZENVAR3Index1 newValEnvFROZENVAR3Index2  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen4
    partialEnvironmentEnvVAR1 = BTreeEnvironment newSereneGenerator 0 0 0 0
    initValEnvVAR1 :: StdGen -> (Integer, StdGen)
    initValEnvVAR1 curGen
      | (False == True) = ((min (-2) (max (-5) 23)), curGen)
      | ((min 100 (max (-100) ((boardBlVAR0 0 blackboard) + (32 + ((boardBlVAR0 0 blackboard) + 22))))) == (min 100 (max (-100) ((boardBlVAR0 0 blackboard) - (min 100 (max (-100) (min (-80) (boardBlVAR0 0 blackboard)))))))) = ((min (-2) (max (-5) (min 100 (max (-100) (abs (min 100 (max (-100) (((sereneCOUNT (sereneIMPLIES True True) ((-64) > (boardBlVAR0 1 blackboard))) + (sereneCOUNT (sereneXOR True False) ((boardBlVAR0 0 blackboard) >= (-3)))) * ((min 100 (max (-100) (max (boardBlVAR0 0 blackboard) (boardBlVAR0 1 blackboard)))) * ((min 100 (max (-100) (abs (-43)))) * (min 100 (max (-100) (max 48 (boardBlVAR0 1 blackboard)))))))))))))), curGen)
      | otherwise = ((min (-2) (max (-5) (min 100 (max (-100) (- (min 100 (max (-100) ((boardBlVAR0 1 blackboard) + (((sereneCOUNT (sereneIMPLIES True True) (sereneXNOR True True)) + (sereneCOUNT False (sereneXNOR True False))) + ((min 100 (max (-100) ((-37) * ((boardBlVAR0 0 blackboard) * ((boardBlVAR0 0 blackboard) * 83))))) + 42)))))))))), curGen)
      where
        environment = partialEnvironmentEnvVAR1

    (newValEnvVAR1, tempGen1) = initValEnvVAR1 tempGen0

    partialEnvironmentEnvFROZENVAR3Index0 = BTreeEnvironment newSereneGenerator newValEnvVAR1 0 0 0
    initValEnvFROZENVAR3Index0 :: StdGen -> (Integer, StdGen)
    initValEnvFROZENVAR3Index0 curGen = ((min 5 (max 2 (min 100 (max (-100) (min (min 100 (max (-100) (55 * (-2)))) (min 100 (max (-100) (41 * newValEnvVAR1)))))))), curGen)
      where
        environment = partialEnvironmentEnvFROZENVAR3Index0

    (newValEnvFROZENVAR3Index0, tempGen2) = initValEnvFROZENVAR3Index0 tempGen1

    partialEnvironmentEnvFROZENVAR3Index1 = BTreeEnvironment newSereneGenerator newValEnvVAR1 newValEnvFROZENVAR3Index0 0 0
    initValEnvFROZENVAR3Index1 :: StdGen -> (Integer, StdGen)
    initValEnvFROZENVAR3Index1 curGen = ((min 5 (max 2 (min 100 (max (-100) (min (min 100 (max (-100) (55 * (-2)))) (min 100 (max (-100) (41 * newValEnvVAR1)))))))), curGen)
      where
        environment = partialEnvironmentEnvFROZENVAR3Index1

    (newValEnvFROZENVAR3Index1, tempGen3) = initValEnvFROZENVAR3Index1 tempGen2

    partialEnvironmentEnvFROZENVAR3Index2 = BTreeEnvironment newSereneGenerator newValEnvVAR1 newValEnvFROZENVAR3Index0 newValEnvFROZENVAR3Index1 0
    initValEnvFROZENVAR3Index2 :: StdGen -> (Integer, StdGen)
    initValEnvFROZENVAR3Index2 curGen = ((min 5 (max 2 (min 100 (max (-100) (min (min 100 (max (-100) (55 * (-2)))) (min 100 (max (-100) (41 * newValEnvVAR1)))))))), curGen)
      where
        environment = partialEnvironmentEnvFROZENVAR3Index2

    (newValEnvFROZENVAR3Index2, tempGen4) = initValEnvFROZENVAR3Index2 tempGen3


