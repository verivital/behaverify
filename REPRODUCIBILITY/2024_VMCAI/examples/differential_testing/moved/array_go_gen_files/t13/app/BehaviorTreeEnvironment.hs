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
  , envEnvVAR4 :: Integer
  }

fromBTreeEnvironmentToString :: BTreeBlackboard -> BTreeEnvironment -> String
fromBTreeEnvironmentToString blackboard environment = "Env = {" ++ "envEnvVAR1: " ++ "[" ++ show (envEnvVAR1 0 environment) ++ ", " ++ show (envEnvVAR1 1 environment) ++ ", " ++ show (envEnvVAR1 2 environment)++ "]" ++ ", " ++ "envEnvVAR2: " ++ "[" ++ show (envEnvVAR2 0 environment) ++ ", " ++ show (envEnvVAR2 1 environment)++ "]" ++ ", " ++ "envEnvVAR4: " ++ show (envEnvVAR4 environment) ++ "}"

-- START OF ENVIRONMENT FUNCTIONS


-- START OF GET FUNCTIONS FOR ARRAYS

envEnvVAR1 :: Integer -> BTreeEnvironment -> String
envEnvVAR1 0 = envEnvVAR1Index0
envEnvVAR1 1 = envEnvVAR1Index1
envEnvVAR1 2 = envEnvVAR1Index2
envEnvVAR1 _ = error "envEnvVAR1 illegal index value"
envEnvVAR2 :: Integer -> BTreeEnvironment -> String
envEnvVAR2 0 = envEnvVAR2Index0
envEnvVAR2 1 = envEnvVAR2Index1
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

checkValueEnvEnvVAR4 :: Integer -> Integer
checkValueEnvEnvVAR4 value
  | 2 > value || value > 5 = error "envEnvVAR4 illegal value"
  | otherwise = value


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
updateEnvEnvVAR4 :: BTreeEnvironment -> Integer -> BTreeEnvironment
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
    tickUpdate1EnvVAR2 :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate1EnvVAR2 environment = arrayUpdateEnvEnvVAR2 environment updates
      where
        updates = [updatePair0]
        updatePair0 = ((min 1 (max 0 23)), updateValue0)
        updateValue0
          | (False && False) = (envEnvVAR2 0 environment)
          | (sereneXNOR False True) = "yes"
          | otherwise = "no"

    tempEnvironment1 = tickUpdate1EnvVAR2 tempEnvironment0

    tickUpdate2EnvVAR1 :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate2EnvVAR1 environment = arrayUpdateEnvEnvVAR1 environment updates
      where
        updates = [updatePair0]
        updatePair0 = ((min 2 (max 0 (abs (max (-98) 29)))), updateValue0)
        updateValue0
          | ((abs 69) >= (-42)) = (envEnvVAR2 0 environment)
          | ((54 >= (envEnvVAR4 environment)) && ((boardBlVAR0 blackboard) == (-20))) = (envEnvVAR2 0 environment)
          | otherwise = (boardBlDEFINE5 blackboard)

    tempEnvironment2 = tickUpdate2EnvVAR1 tempEnvironment1

    tickUpdate3EnvVAR1 :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate3EnvVAR1 environment = arrayUpdateEnvEnvVAR1 environment updates
      where
        updates = [updatePair0, updatePair1, updatePair2]
        updatePair0 = ((min 2 (max 0 (abs (-31)))), updateValue0)
        updatePair1 = ((min 2 (max 0 ((sereneCOUNT ((abs (envEnvVAR4 environment)) > ((-98) - (23 * (boardBlVAR0 blackboard)))) (((sereneCOUNT (False /= (40 < (envEnvVAR4 environment))) (sereneXOR False True)) + (sereneCOUNT (sereneXNOR (sereneIMPLIES True True) (sereneXNOR False False)) ((boardBlVAR0 blackboard) >= (-43)))) == (envEnvVAR4 environment))) + (sereneCOUNT ((True && True) && ((-43) <= (envEnvVAR4 environment))) (((envEnvVAR4 environment) + (91 + (boardBlVAR0 blackboard))) <= (max (-99) 36)))))), updateValue1)
        updatePair2 = ((min 2 (max 0 (-47))), updateValue2)
        updateValue0
          | True = (boardBlDEFINE5 blackboard)
          | otherwise = "no"
        updateValue1
          | (sereneIMPLIES True False) = "no"
          | otherwise = (boardBlDEFINE5 blackboard)
        updateValue2
          | (((sereneCOUNT ((envEnvVAR4 environment) /= (45 - 27)) (False /= True)) + (sereneCOUNT False ((sereneXOR True False) /= ((boardBlVAR0 blackboard) <= (envEnvVAR4 environment))))) > ((sereneCOUNT (sereneXOR True False) ((envEnvVAR2 1 environment) /= "no")) + (sereneCOUNT ((envEnvVAR4 environment) <= (boardBlVAR0 blackboard)) (True || True)))) = "yes"
          | otherwise = (boardBlVAR3 0 blackboard)

    tempEnvironment3 = tickUpdate3EnvVAR1 tempEnvironment2

    tickUpdate4EnvVAR4 :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate4EnvVAR4 environment = updateEnvEnvVAR4 environment (min 5 (max 2 ((min (-13) (-24)) + ((abs (-33)) + (boardBlVAR0 blackboard)))))

    tempEnvironment4 = tickUpdate4EnvVAR4 tempEnvironment3

    tickUpdate5EnvVAR4 :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate5EnvVAR4 environment = updateEnvEnvVAR4 environment (min 5 (max 2 (-99)))

    tempEnvironment5 = tickUpdate5EnvVAR4 tempEnvironment4



-- START OF INITIAL ENVIRONMENT VALUE

initialEnvironment :: Integer -> BTreeBlackboard -> BTreeEnvironment
initialEnvironment seed blackboard = BTreeEnvironment newSereneGenerator newValEnvVAR1Index0 newValEnvVAR1Index1 newValEnvVAR1Index2 newValEnvVAR2Index0 newValEnvVAR2Index1 newValEnvVAR4  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen6
    partialEnvironmentEnvVAR1Index0 = BTreeEnvironment newSereneGenerator " " " " " " " " " " 0
    initValEnvVAR1Index0 :: StdGen -> (String, StdGen)
    initValEnvVAR1Index0 curGen = ("both", curGen)
      where
        environment = partialEnvironmentEnvVAR1Index0

    (newValEnvVAR1Index0, tempGen1) = initValEnvVAR1Index0 tempGen0

    partialEnvironmentEnvVAR1Index1 = BTreeEnvironment newSereneGenerator newValEnvVAR1Index0 " " " " " " " " 0
    initValEnvVAR1Index1 :: StdGen -> (String, StdGen)
    initValEnvVAR1Index1 curGen
      | ((-93) >= (boardBlVAR0 blackboard)) = ("both", curGen)
      | (False && False) = ("both", curGen)
      | otherwise = ("no", curGen)
      where
        environment = partialEnvironmentEnvVAR1Index1

    (newValEnvVAR1Index1, tempGen2) = initValEnvVAR1Index1 tempGen1

    partialEnvironmentEnvVAR1Index2 = BTreeEnvironment newSereneGenerator newValEnvVAR1Index0 newValEnvVAR1Index1 " " " " " " 0
    initValEnvVAR1Index2 :: StdGen -> (String, StdGen)
    initValEnvVAR1Index2 curGen = ("no", curGen)
      where
        environment = partialEnvironmentEnvVAR1Index2

    (newValEnvVAR1Index2, tempGen3) = initValEnvVAR1Index2 tempGen2

    partialEnvironmentEnvVAR2Index0 = BTreeEnvironment newSereneGenerator newValEnvVAR1Index0 newValEnvVAR1Index1 newValEnvVAR1Index2 " " " " 0
    initValEnvVAR2Index0 :: StdGen -> (String, StdGen)
    initValEnvVAR2Index0 curGen = ("yes", curGen)
      where
        environment = partialEnvironmentEnvVAR2Index0

    (newValEnvVAR2Index0, tempGen4) = initValEnvVAR2Index0 tempGen3

    partialEnvironmentEnvVAR2Index1 = BTreeEnvironment newSereneGenerator newValEnvVAR1Index0 newValEnvVAR1Index1 newValEnvVAR1Index2 newValEnvVAR2Index0 " " 0
    initValEnvVAR2Index1 :: StdGen -> (String, StdGen)
    initValEnvVAR2Index1 curGen
      | True = ("no", curGen)
      | otherwise = ((envEnvVAR1 0 environment), curGen)
      where
        environment = partialEnvironmentEnvVAR2Index1

    (newValEnvVAR2Index1, tempGen5) = initValEnvVAR2Index1 tempGen4

    partialEnvironmentEnvVAR4 = BTreeEnvironment newSereneGenerator newValEnvVAR1Index0 newValEnvVAR1Index1 newValEnvVAR1Index2 newValEnvVAR2Index0 newValEnvVAR2Index1 0
    initValEnvVAR4 :: StdGen -> (Integer, StdGen)
    initValEnvVAR4 curGen = ((min 5 (max 2 (abs (- (boardBlVAR0 blackboard))))), curGen)
      where
        environment = partialEnvironmentEnvVAR4

    (newValEnvVAR4, tempGen6) = initValEnvVAR4 tempGen5


