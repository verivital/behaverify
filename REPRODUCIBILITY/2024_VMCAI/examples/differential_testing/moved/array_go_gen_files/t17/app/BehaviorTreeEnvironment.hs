module BehaviorTreeEnvironment where
import SereneRandomizer
import System.Random
import SereneOperations
import BehaviorTreeBlackboard

data BTreeEnvironment = BTreeEnvironment {
  sereneEnvGenerator :: StdGen
  , envEnvVAR1Index0 :: String
  , envEnvVAR1Index1 :: String
  , envEnvVAR1Index2 :: String
  , envEnvVAR2Index0 :: String
  , envEnvVAR2Index1 :: String
  , envEnvVAR2Index2 :: String
  , envEnvVAR4 :: Bool
  }

fromBTreeEnvironmentToString :: BTreeBlackboard -> BTreeEnvironment -> String
fromBTreeEnvironmentToString blackboard environment = "Env = {" ++ "envEnvVAR1: " ++ "[" ++ show (envEnvVAR1 0 environment) ++ ", " ++ show (envEnvVAR1 1 environment) ++ ", " ++ show (envEnvVAR1 2 environment)++ "]" ++ ", " ++ "envEnvVAR2: " ++ "[" ++ show (envEnvVAR2 0 environment) ++ ", " ++ show (envEnvVAR2 1 environment) ++ ", " ++ show (envEnvVAR2 2 environment)++ "]" ++ ", " ++ "envEnvVAR4: " ++ show (envEnvVAR4 environment) ++ ", " ++ "envEnvDEFINE6: " ++ show (envEnvDEFINE6 blackboard environment) ++ "}"

-- START OF ENVIRONMENT FUNCTIONS

envEnvDEFINE6 :: BTreeBlackboard -> BTreeEnvironment -> Bool
envEnvDEFINE6 blackboard environment
  | (envEnvVAR4 environment) = True
  | otherwise = ((boardBlDEFINE5 blackboard) < (boardBlVAR0 2 blackboard))

-- START OF GET FUNCTIONS FOR ARRAYS

envEnvVAR1 :: Integer -> BTreeEnvironment -> String
envEnvVAR1 0 = envEnvVAR1Index0
envEnvVAR1 1 = envEnvVAR1Index1
envEnvVAR1 2 = envEnvVAR1Index2
envEnvVAR1 _ = error "envEnvVAR1 illegal index value"
envEnvVAR2 :: Integer -> BTreeEnvironment -> String
envEnvVAR2 0 = envEnvVAR2Index0
envEnvVAR2 1 = envEnvVAR2Index1
envEnvVAR2 2 = envEnvVAR2Index2
envEnvVAR2 _ = error "envEnvVAR2 illegal index value"

-- START OF TYPE CHECKING FUNCTIONS

checkValueEnvEnvVAR1 :: String -> String
checkValueEnvEnvVAR1 "yes" = "yes"
checkValueEnvEnvVAR1 "no" = "no"
checkValueEnvEnvVAR1 "both" = "both"
checkValueEnvEnvVAR1 _ = error "envEnvVAR1 illegal value"

checkValueEnvEnvVAR2 :: String -> String
checkValueEnvEnvVAR2 "yes" = "yes"
checkValueEnvEnvVAR2 "no" = "no"
checkValueEnvEnvVAR2 "both" = "both"
checkValueEnvEnvVAR2 _ = error "envEnvVAR2 illegal value"

checkValueEnvEnvVAR4 :: Bool -> Bool
checkValueEnvEnvVAR4 value = value


-- START OF SET FUNCTIONS

updateEnvGenerator :: BTreeEnvironment -> StdGen -> BTreeEnvironment
updateEnvGenerator environment newGen = environment { sereneEnvGenerator = newGen }
updateEnvEnvVAR1Index0 :: BTreeEnvironment -> String -> BTreeEnvironment
updateEnvEnvVAR1Index0 environment value = environment { envEnvVAR1Index0 = (checkValueEnvEnvVAR1 value)}
updateEnvEnvVAR1Index1 :: BTreeEnvironment -> String -> BTreeEnvironment
updateEnvEnvVAR1Index1 environment value = environment { envEnvVAR1Index1 = (checkValueEnvEnvVAR1 value)}
updateEnvEnvVAR1Index2 :: BTreeEnvironment -> String -> BTreeEnvironment
updateEnvEnvVAR1Index2 environment value = environment { envEnvVAR1Index2 = (checkValueEnvEnvVAR1 value)}
updateEnvEnvVAR2Index0 :: BTreeEnvironment -> String -> BTreeEnvironment
updateEnvEnvVAR2Index0 environment value = environment { envEnvVAR2Index0 = (checkValueEnvEnvVAR2 value)}
updateEnvEnvVAR2Index1 :: BTreeEnvironment -> String -> BTreeEnvironment
updateEnvEnvVAR2Index1 environment value = environment { envEnvVAR2Index1 = (checkValueEnvEnvVAR2 value)}
updateEnvEnvVAR2Index2 :: BTreeEnvironment -> String -> BTreeEnvironment
updateEnvEnvVAR2Index2 environment value = environment { envEnvVAR2Index2 = (checkValueEnvEnvVAR2 value)}
updateEnvEnvVAR4 :: BTreeEnvironment -> Bool -> BTreeEnvironment
updateEnvEnvVAR4 environment value = environment { envEnvVAR4 = (checkValueEnvEnvVAR4 value)}

-- START OF SET FUNCTIONS FOR ARRAYS

updateEnvEnvVAR1 :: Integer -> BTreeEnvironment -> String -> BTreeEnvironment
updateEnvEnvVAR1 0 = updateEnvEnvVAR1Index0
updateEnvEnvVAR1 1 = updateEnvEnvVAR1Index1
updateEnvEnvVAR1 2 = updateEnvEnvVAR1Index2
updateEnvEnvVAR1 _ = error "EnvEnvVAR1 illegal index value"
arrayUpdateEnvEnvVAR1 :: BTreeEnvironment -> [(Integer, String)] -> BTreeEnvironment
arrayUpdateEnvEnvVAR1 environment []  = environment
arrayUpdateEnvEnvVAR1 environment [(index, value)] = updateEnvEnvVAR1 index environment value
arrayUpdateEnvEnvVAR1 environment indicesValues = environment {
  envEnvVAR1Index0 = newEnvVAR1Index0
  , envEnvVAR1Index1 = newEnvVAR1Index1
  , envEnvVAR1Index2 = newEnvVAR1Index2
  }
    where
      (newEnvVAR1Index0, newEnvVAR1Index1, newEnvVAR1Index2) = updateValues indicesValues
      updateValues :: [(Integer, String)] -> (String, String, String)
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
updateEnvEnvVAR2 :: Integer -> BTreeEnvironment -> String -> BTreeEnvironment
updateEnvEnvVAR2 0 = updateEnvEnvVAR2Index0
updateEnvEnvVAR2 1 = updateEnvEnvVAR2Index1
updateEnvEnvVAR2 2 = updateEnvEnvVAR2Index2
updateEnvEnvVAR2 _ = error "EnvEnvVAR2 illegal index value"
arrayUpdateEnvEnvVAR2 :: BTreeEnvironment -> [(Integer, String)] -> BTreeEnvironment
arrayUpdateEnvEnvVAR2 environment []  = environment
arrayUpdateEnvEnvVAR2 environment [(index, value)] = updateEnvEnvVAR2 index environment value
arrayUpdateEnvEnvVAR2 environment indicesValues = environment {
  envEnvVAR2Index0 = newEnvVAR2Index0
  , envEnvVAR2Index1 = newEnvVAR2Index1
  , envEnvVAR2Index2 = newEnvVAR2Index2
  }
    where
      (newEnvVAR2Index0, newEnvVAR2Index1, newEnvVAR2Index2) = updateValues indicesValues
      updateValues :: [(Integer, String)] -> (String, String, String)
      updateValues [] = (envEnvVAR2Index0 environment, envEnvVAR2Index1 environment, envEnvVAR2Index2 environment)
      updateValues ((0, currentValue) : nextIndicesValues) = (checkValueEnvEnvVAR2 currentValue, updatedValue1, updatedValue2)
        where
          (_, updatedValue1, updatedValue2) = updateValues nextIndicesValues
      updateValues ((1, currentValue) : nextIndicesValues) = (updatedValue0, checkValueEnvEnvVAR2 currentValue, updatedValue2)
        where
          (updatedValue0, _, updatedValue2) = updateValues nextIndicesValues
      updateValues ((2, currentValue) : nextIndicesValues) = (updatedValue0, updatedValue1, checkValueEnvEnvVAR2 currentValue)
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
    newEnvironment = tempEnvironment0


-- START OF INITIAL ENVIRONMENT VALUE

initialEnvironment :: Integer -> BTreeBlackboard -> BTreeEnvironment
initialEnvironment seed blackboard = BTreeEnvironment newSereneGenerator newValEnvVAR1Index0 newValEnvVAR1Index1 newValEnvVAR1Index2 newValEnvVAR2Index0 newValEnvVAR2Index1 newValEnvVAR2Index2 newValEnvVAR4  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen7
    partialEnvironmentEnvVAR1Index0 = BTreeEnvironment newSereneGenerator " " " " " " " " " " " " True
    initValEnvVAR1Index0 :: StdGen -> (String, StdGen)
    initValEnvVAR1Index0 curGen
      | (((boardBlVAR0 1 blackboard) + (-7)) < (abs (-94))) = ("yes", curGen)
      | otherwise = ("yes", curGen)
      where
        environment = partialEnvironmentEnvVAR1Index0

    (newValEnvVAR1Index0, tempGen1) = initValEnvVAR1Index0 tempGen0

    partialEnvironmentEnvVAR1Index1 = BTreeEnvironment newSereneGenerator newValEnvVAR1Index0 " " " " " " " " " " True
    initValEnvVAR1Index1 :: StdGen -> (String, StdGen)
    initValEnvVAR1Index1 curGen
      | (True == True) = ("yes", curGen)
      | (sereneIMPLIES (True || True) ("no" == "both")) = ("yes", curGen)
      | otherwise = ("no", curGen)
      where
        environment = partialEnvironmentEnvVAR1Index1

    (newValEnvVAR1Index1, tempGen2) = initValEnvVAR1Index1 tempGen1

    partialEnvironmentEnvVAR1Index2 = BTreeEnvironment newSereneGenerator newValEnvVAR1Index0 newValEnvVAR1Index1 " " " " " " " " True
    initValEnvVAR1Index2 :: StdGen -> (String, StdGen)
    initValEnvVAR1Index2 curGen
      | (True /= False) = ("yes", curGen)
      | False = ("yes", curGen)
      | otherwise = ("no", curGen)
      where
        environment = partialEnvironmentEnvVAR1Index2

    (newValEnvVAR1Index2, tempGen3) = initValEnvVAR1Index2 tempGen2

    partialEnvironmentEnvVAR2Index0 = BTreeEnvironment newSereneGenerator newValEnvVAR1Index0 newValEnvVAR1Index1 newValEnvVAR1Index2 " " " " " " True
    initValEnvVAR2Index0 :: StdGen -> (String, StdGen)
    initValEnvVAR2Index0 curGen
      | (False || (True || True)) = ("no", curGen)
      | (sereneIMPLIES True False) = ((envEnvVAR1 0 environment), curGen)
      | otherwise = ("both", curGen)
      where
        environment = partialEnvironmentEnvVAR2Index0

    (newValEnvVAR2Index0, tempGen4) = initValEnvVAR2Index0 tempGen3

    partialEnvironmentEnvVAR2Index1 = BTreeEnvironment newSereneGenerator newValEnvVAR1Index0 newValEnvVAR1Index1 newValEnvVAR1Index2 newValEnvVAR2Index0 " " " " True
    initValEnvVAR2Index1 :: StdGen -> (String, StdGen)
    initValEnvVAR2Index1 curGen
      | ("both" /= "no") = ((envEnvVAR1 1 environment), curGen)
      | (92 < ((sereneCOUNT (False /= True) (True && True)) - ((sereneCOUNT (True || False) ((-54) >= 40)) + (sereneCOUNT (True /= True) ((boardBlVAR0 1 blackboard) >= (boardBlVAR0 1 blackboard)))))) = ((envEnvVAR1 2 environment), curGen)
      | otherwise = ("both", curGen)
      where
        environment = partialEnvironmentEnvVAR2Index1

    (newValEnvVAR2Index1, tempGen5) = initValEnvVAR2Index1 tempGen4

    partialEnvironmentEnvVAR2Index2 = BTreeEnvironment newSereneGenerator newValEnvVAR1Index0 newValEnvVAR1Index1 newValEnvVAR1Index2 newValEnvVAR2Index0 newValEnvVAR2Index1 " " True
    initValEnvVAR2Index2 :: StdGen -> (String, StdGen)
    initValEnvVAR2Index2 curGen
      | (sereneIMPLIES False ((boardBlVAR0 1 blackboard) < (boardBlVAR0 2 blackboard))) = ("both", curGen)
      | False = ((envEnvVAR1 0 environment), curGen)
      | otherwise = ((envEnvVAR1 1 environment), curGen)
      where
        environment = partialEnvironmentEnvVAR2Index2

    (newValEnvVAR2Index2, tempGen6) = initValEnvVAR2Index2 tempGen5

    partialEnvironmentEnvVAR4 = BTreeEnvironment newSereneGenerator newValEnvVAR1Index0 newValEnvVAR1Index1 newValEnvVAR1Index2 newValEnvVAR2Index0 newValEnvVAR2Index1 newValEnvVAR2Index2 True
    initValEnvVAR4 :: StdGen -> (Bool, StdGen)
    initValEnvVAR4 curGen
      | (((boardBlVAR0 2 blackboard) - (boardBlVAR0 0 blackboard)) /= (sereneCOUNT (sereneXOR False (sereneXOR False False)) (False || (False == False)))) = ((16 > (-20)), curGen)
      | (True && False) = ((sereneXNOR True True), curGen)
      | otherwise = ((sereneIMPLIES False (97 > (boardBlVAR0 0 blackboard))), curGen)
      where
        environment = partialEnvironmentEnvVAR4

    (newValEnvVAR4, tempGen7) = initValEnvVAR4 tempGen6


