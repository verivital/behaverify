module BehaviorTreeEnvironment where
import SereneRandomizer
import System.Random
import SereneOperations
import BehaviorTreeBlackboard

data BTreeEnvironment = BTreeEnvironment {
  sereneEnvGenerator :: StdGen
  , envEnvVAR1Index0 :: String
  , envEnvVAR1Index1 :: String
  }

fromBTreeEnvironmentToString :: BTreeBlackboard -> BTreeEnvironment -> String
fromBTreeEnvironmentToString blackboard environment = "Env = {" ++ "envEnvVAR1: " ++ "[" ++ show (envEnvVAR1 0 environment) ++ ", " ++ show (envEnvVAR1 1 environment)++ "]" ++ ", " ++ "envEnvDEFINE7: " ++ show (envEnvDEFINE7 blackboard environment) ++ ", " ++ "envEnvDEFINE9: " ++ show (envEnvDEFINE9 blackboard environment) ++ "}"

-- START OF ENVIRONMENT FUNCTIONS

envEnvDEFINE7 :: BTreeBlackboard -> BTreeEnvironment -> Integer
envEnvDEFINE7 blackboard environment
  | ((boardBlVAR3 blackboard) && (93 <= (boardBlVAR0 1 blackboard))) = (min (-2) (max (-5) (-56)))
  | ((abs (-97)) <= 10) = (min (-2) (max (-5) (abs (sereneCOUNT (sereneXOR ((boardBlVAR3 blackboard) == False) ((-84) < (boardBlVAR0 0 blackboard))) ((boardBlVAR3 blackboard) && (sereneIMPLIES (boardBlVAR3 blackboard) (boardBlVAR3 blackboard)))))))
  | otherwise = (min (-2) (max (-5) (boardBlVAR0 0 blackboard)))
envEnvDEFINE9 :: BTreeBlackboard -> BTreeEnvironment -> Bool
envEnvDEFINE9 blackboard environment = ((boardBlVAR3 blackboard) || (False == (boardBlVAR3 blackboard)))

-- START OF GET FUNCTIONS FOR ARRAYS

envEnvVAR1 :: Integer -> BTreeEnvironment -> String
envEnvVAR1 0 = envEnvVAR1Index0
envEnvVAR1 1 = envEnvVAR1Index1
envEnvVAR1 _ = error "envEnvVAR1 illegal index value"

-- START OF TYPE CHECKING FUNCTIONS

checkValueEnvEnvVAR1 :: String -> String
checkValueEnvEnvVAR1 "yes" = "yes"
checkValueEnvEnvVAR1 "no" = "no"
checkValueEnvEnvVAR1 "both" = "both"
checkValueEnvEnvVAR1 _ = error "envEnvVAR1 illegal value"


-- START OF SET FUNCTIONS

updateEnvGenerator :: BTreeEnvironment -> StdGen -> BTreeEnvironment
updateEnvGenerator environment newGen = environment { sereneEnvGenerator = newGen }
updateEnvEnvVAR1Index0 :: BTreeEnvironment -> String -> BTreeEnvironment
updateEnvEnvVAR1Index0 environment value = environment { envEnvVAR1Index0 = (checkValueEnvEnvVAR1 value)}
updateEnvEnvVAR1Index1 :: BTreeEnvironment -> String -> BTreeEnvironment
updateEnvEnvVAR1Index1 environment value = environment { envEnvVAR1Index1 = (checkValueEnvEnvVAR1 value)}

-- START OF SET FUNCTIONS FOR ARRAYS

updateEnvEnvVAR1 :: Integer -> BTreeEnvironment -> String -> BTreeEnvironment
updateEnvEnvVAR1 0 = updateEnvEnvVAR1Index0
updateEnvEnvVAR1 1 = updateEnvEnvVAR1Index1
updateEnvEnvVAR1 _ = error "EnvEnvVAR1 illegal index value"
arrayUpdateEnvEnvVAR1 :: BTreeEnvironment -> [(Integer, String)] -> BTreeEnvironment
arrayUpdateEnvEnvVAR1 environment []  = environment
arrayUpdateEnvEnvVAR1 environment [(index, value)] = updateEnvEnvVAR1 index environment value
arrayUpdateEnvEnvVAR1 environment indicesValues = environment {
  envEnvVAR1Index0 = newEnvVAR1Index0
  , envEnvVAR1Index1 = newEnvVAR1Index1
  }
    where
      (newEnvVAR1Index0, newEnvVAR1Index1) = updateValues indicesValues
      updateValues :: [(Integer, String)] -> (String, String)
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
    newEnvironment = tempEnvironment4
    tickUpdate1EnvVAR1 :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate1EnvVAR1 environment = arrayUpdateEnvEnvVAR1 environment updates
      where
        updates = [updatePair0]
        updatePair0 = ((min 1 (max 0 (boardBlVAR0 2 blackboard))), updateValue0)
        updateValue0 = "no"

    tempEnvironment1 = tickUpdate1EnvVAR1 tempEnvironment0

    tickUpdate2EnvVAR1 :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate2EnvVAR1 environment = arrayUpdateEnvEnvVAR1 environment updates
      where
        updates = [updatePair0]
        updatePair0 = ((min 1 (max 0 ((max (envEnvDEFINE7 blackboard environment) (-22)) + ((envEnvDEFINE7 blackboard environment) + ((boardBlVAR0 2 blackboard) - 82))))), updateValue0)
        updateValue0
          | (sereneIMPLIES (envEnvDEFINE9 blackboard environment) True) = (envEnvVAR1 1 environment)
          | otherwise = (envEnvVAR1 0 environment)

    tempEnvironment2 = tickUpdate2EnvVAR1 tempEnvironment1

    tickUpdate3EnvVAR1 :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate3EnvVAR1 environment = arrayUpdateEnvEnvVAR1 environment updates
      where
        updates = [updatePair0, updatePair1]
        updatePair0 = ((min 1 (max 0 (boardBlVAR0 0 blackboard))), updateValue0)
        updatePair1 = ((min 1 (max 0 (max ((sereneCOUNT ((envEnvVAR1 0 environment) /= (envEnvVAR1 0 environment)) ((boardBlVAR0 0 blackboard) < (boardBlVAR0 2 blackboard))) + (sereneCOUNT ((envEnvDEFINE7 blackboard environment) >= (boardBlVAR0 1 blackboard)) ((boardBlVAR3 blackboard) && False))) (abs (envEnvDEFINE7 blackboard environment))))), updateValue1)
        updateValue0
          | ((-13) >= (envEnvDEFINE7 blackboard environment)) = "no"
          | otherwise = "no"
        updateValue1
          | ((abs (boardBlVAR0 2 blackboard)) > 80) = "no"
          | otherwise = "both"

    tempEnvironment3 = tickUpdate3EnvVAR1 tempEnvironment2

    tickUpdate4EnvVAR1 :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate4EnvVAR1 environment = arrayUpdateEnvEnvVAR1 environment updates
      where
        updates = [updatePair0, updatePair1]
        updatePair0 = ((min 1 (max 0 70)), updateValue0)
        updatePair1 = ((min 1 (max 0 (-90))), updateValue1)
        updateValue0
          | False = (envEnvVAR1 0 environment)
          | otherwise = "yes"
        updateValue1
          | ((boardBlVAR0 0 blackboard) < (-88)) = "no"
          | otherwise = "no"

    tempEnvironment4 = tickUpdate4EnvVAR1 tempEnvironment3



-- START OF INITIAL ENVIRONMENT VALUE

initialEnvironment :: Integer -> BTreeBlackboard -> BTreeEnvironment
initialEnvironment seed blackboard = BTreeEnvironment newSereneGenerator newValEnvVAR1Index0 newValEnvVAR1Index1  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen2
    partialEnvironmentEnvVAR1Index0 = BTreeEnvironment newSereneGenerator " " " "
    initValEnvVAR1Index0 :: StdGen -> (String, StdGen)
    initValEnvVAR1Index0 curGen
      | (False || False) = ("no", curGen)
      | ((abs (boardBlVAR0 0 blackboard)) > (boardBlVAR0 2 blackboard)) = ("yes", curGen)
      | otherwise = ("yes", curGen)
      where
        environment = partialEnvironmentEnvVAR1Index0

    (newValEnvVAR1Index0, tempGen1) = initValEnvVAR1Index0 tempGen0

    partialEnvironmentEnvVAR1Index1 = BTreeEnvironment newSereneGenerator newValEnvVAR1Index0 " "
    initValEnvVAR1Index1 :: StdGen -> (String, StdGen)
    initValEnvVAR1Index1 curGen = ("both", curGen)
      where
        environment = partialEnvironmentEnvVAR1Index1

    (newValEnvVAR1Index1, tempGen2) = initValEnvVAR1Index1 tempGen1


