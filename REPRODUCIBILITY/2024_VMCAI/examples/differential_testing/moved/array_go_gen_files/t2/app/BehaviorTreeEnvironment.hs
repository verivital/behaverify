module BehaviorTreeEnvironment where
import SereneRandomizer
import System.Random
import SereneOperations
import BehaviorTreeBlackboard

data BTreeEnvironment = BTreeEnvironment {
  sereneEnvGenerator :: StdGen
  , envEnvVAR1Index0 :: Integer
  , envEnvVAR1Index1 :: Integer
  , envEnvFROZENVAR4 :: String
  }

fromBTreeEnvironmentToString :: BTreeBlackboard -> BTreeEnvironment -> String
fromBTreeEnvironmentToString blackboard environment = "Env = {" ++ "envEnvVAR1: " ++ "[" ++ show (envEnvVAR1 0 environment) ++ ", " ++ show (envEnvVAR1 1 environment)++ "]" ++ ", " ++ "envEnvFROZENVAR4: " ++ show (envEnvFROZENVAR4 environment) ++ ", " ++ "envEnvDEFINE9: " ++ "[" ++ show (envEnvDEFINE9 0 blackboard environment) ++ ", " ++ show (envEnvDEFINE9 1 blackboard environment) ++ ", " ++ show (envEnvDEFINE9 2 blackboard environment)++ "]" ++ "}"

-- START OF ENVIRONMENT FUNCTIONS

envEnvDEFINE9 :: Integer -> BTreeBlackboard -> BTreeEnvironment -> Bool
envEnvDEFINE9 0 blackboard environment = (boardBlVAR2 blackboard)
envEnvDEFINE9 1 blackboard environment = (boardBlVAR2 blackboard)
envEnvDEFINE9 2 blackboard environment = (boardBlVAR2 blackboard)
envEnvDEFINE9 _ _ _ = error "envEnvDEFINE9 illegal index value"

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
    newEnvironment = tempEnvironment3
    tickUpdate1EnvVAR1 :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate1EnvVAR1 environment = arrayUpdateEnvEnvVAR1 environment updates
      where
        updates = [updatePair0]
        updatePair0 = ((min 1 (max 0 96)), updateValue0)
        updateValue0
          | (True == (envEnvDEFINE9 0 blackboard environment)) = (min 5 (max 2 ((boardBlFROZENVAR5 1 blackboard) + ((max (-53) (envEnvVAR1 1 environment)) + (boardBlDEFINE8 1 blackboard)))))
          | otherwise = (min 5 (max 2 ((boardBlFROZENVAR5 2 blackboard) - (boardBlDEFINE8 0 blackboard))))

    tempEnvironment1 = tickUpdate1EnvVAR1 tempEnvironment0

    tickUpdate2EnvVAR1 :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate2EnvVAR1 environment = arrayUpdateEnvEnvVAR1 environment updates
      where
        updates = [updatePair0]
        updatePair0 = ((min 1 (max 0 (sereneCOUNT ((sereneIMPLIES False False) == (sereneIMPLIES (sereneIMPLIES False (boardBlVAR2 blackboard)) True)) (sereneXOR False ((envEnvVAR1 1 environment) >= (boardBlDEFINE8 1 blackboard)))))), updateValue0)
        updateValue0 = (min 5 (max 2 (-12)))

    tempEnvironment2 = tickUpdate2EnvVAR1 tempEnvironment1

    tickUpdate3EnvVAR1 :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate3EnvVAR1 environment = arrayUpdateEnvEnvVAR1 environment updates
      where
        updates = [updatePair0, updatePair1]
        updatePair0 = ((min 1 (max 0 (boardBlFROZENVAR5 1 blackboard))), updateValue0)
        updatePair1 = ((min 1 (max 0 (envEnvVAR1 0 environment))), updateValue1)
        updateValue0
          | ((envEnvVAR1 1 environment) <= (-77)) = (min 5 (max 2 ((sereneCOUNT ((-84) > 35) ((envEnvVAR1 0 environment) >= 47)) + (sereneCOUNT False ((-35) /= 6)))))
          | ((boardBlFROZENVAR5 1 blackboard) < 49) = (min 5 (max 2 (envEnvVAR1 0 environment)))
          | otherwise = (min 5 (max 2 (abs ((sereneCOUNT ((boardBlVAR3 blackboard) < 85) ((boardBlVAR0 0 blackboard) == "no")) + (sereneCOUNT False (sereneXNOR (envEnvDEFINE9 1 blackboard environment) False))))))
        updateValue1
          | (sereneXOR True (sereneIMPLIES False False)) = (min 5 (max 2 (- (- (-54)))))
          | (True == (boardBlVAR2 blackboard)) = (min 5 (max 2 (max (75 + ((-88) + 9)) (abs ((-24) - (boardBlFROZENVAR5 2 blackboard))))))
          | otherwise = (min 5 (max 2 (max (min 73 (boardBlDEFINE8 0 blackboard)) ((boardBlVAR3 blackboard) * ((-3) * (-50))))))

    tempEnvironment3 = tickUpdate3EnvVAR1 tempEnvironment2



-- START OF INITIAL ENVIRONMENT VALUE

initialEnvironment :: Integer -> BTreeBlackboard -> BTreeEnvironment
initialEnvironment seed blackboard = BTreeEnvironment newSereneGenerator newValEnvVAR1Index0 newValEnvVAR1Index1 newValEnvFROZENVAR4  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen3
    partialEnvironmentEnvVAR1Index0 = BTreeEnvironment newSereneGenerator 0 0 " "
    initValEnvVAR1Index0 :: StdGen -> (Integer, StdGen)
    initValEnvVAR1Index0 curGen = ((min 5 (max 2 ((sereneCOUNT ((-3) <= 79) (22 <= 74)) + (sereneCOUNT False (False == False))))), curGen)
      where
        environment = partialEnvironmentEnvVAR1Index0

    (newValEnvVAR1Index0, tempGen1) = initValEnvVAR1Index0 tempGen0

    partialEnvironmentEnvVAR1Index1 = BTreeEnvironment newSereneGenerator newValEnvVAR1Index0 0 " "
    initValEnvVAR1Index1 :: StdGen -> (Integer, StdGen)
    initValEnvVAR1Index1 curGen = ((min 5 (max 2 ((sereneCOUNT ((-3) <= 79) (22 <= 74)) + (sereneCOUNT False (False == False))))), curGen)
      where
        environment = partialEnvironmentEnvVAR1Index1

    (newValEnvVAR1Index1, tempGen2) = initValEnvVAR1Index1 tempGen1

    partialEnvironmentEnvFROZENVAR4 = BTreeEnvironment newSereneGenerator newValEnvVAR1Index0 newValEnvVAR1Index1 " "
    initValEnvFROZENVAR4 :: StdGen -> (String, StdGen)
    initValEnvFROZENVAR4 curGen = ((boardBlVAR0 1 blackboard), curGen)
      where
        environment = partialEnvironmentEnvFROZENVAR4

    (newValEnvFROZENVAR4, tempGen3) = initValEnvFROZENVAR4 tempGen2


