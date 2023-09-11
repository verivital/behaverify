module BehaviorTreeEnvironment where
import SereneRandomizer
import System.Random
import SereneOperations
import BehaviorTreeBlackboard

data BTreeEnvironment = BTreeEnvironment {
  sereneEnvGenerator :: StdGen
  , envEnvVAR1Index0 :: Integer
  , envEnvVAR1Index1 :: Integer
  , envEnvVAR1Index2 :: Integer
  , envEnvVAR2Index0 :: Integer
  , envEnvVAR2Index1 :: Integer
  }

fromBTreeEnvironmentToString :: BTreeBlackboard -> BTreeEnvironment -> String
fromBTreeEnvironmentToString blackboard environment = "Env = {" ++ "envEnvVAR1: " ++ "[" ++ show (envEnvVAR1 0 environment) ++ ", " ++ show (envEnvVAR1 1 environment) ++ ", " ++ show (envEnvVAR1 2 environment)++ "]" ++ ", " ++ "envEnvVAR2: " ++ "[" ++ show (envEnvVAR2 0 environment) ++ ", " ++ show (envEnvVAR2 1 environment)++ "]" ++ ", " ++ "envEnvDEFINE7: " ++ "[" ++ show (envEnvDEFINE7 0 blackboard environment) ++ ", " ++ show (envEnvDEFINE7 1 blackboard environment) ++ ", " ++ show (envEnvDEFINE7 2 blackboard environment)++ "]" ++ "}"

-- START OF ENVIRONMENT FUNCTIONS

envEnvDEFINE7 :: Integer -> BTreeBlackboard -> BTreeEnvironment -> String
envEnvDEFINE7 0 blackboard environment
  | (sereneXNOR (boardBlVAR3 0 blackboard) False) = "yes"
  | otherwise = (boardBlVAR0 blackboard)
envEnvDEFINE7 1 blackboard environment
  | (sereneXNOR (boardBlVAR3 0 blackboard) False) = "yes"
  | otherwise = (boardBlVAR0 blackboard)
envEnvDEFINE7 2 blackboard environment
  | (sereneXNOR (boardBlVAR3 0 blackboard) False) = "yes"
  | otherwise = (boardBlVAR0 blackboard)
envEnvDEFINE7 _ _ _ = error "envEnvDEFINE7 illegal index value"

-- START OF GET FUNCTIONS FOR ARRAYS

envEnvVAR1 :: Integer -> BTreeEnvironment -> Integer
envEnvVAR1 0 = envEnvVAR1Index0
envEnvVAR1 1 = envEnvVAR1Index1
envEnvVAR1 2 = envEnvVAR1Index2
envEnvVAR1 _ = error "envEnvVAR1 illegal index value"
envEnvVAR2 :: Integer -> BTreeEnvironment -> Integer
envEnvVAR2 0 = envEnvVAR2Index0
envEnvVAR2 1 = envEnvVAR2Index1
envEnvVAR2 _ = error "envEnvVAR2 illegal index value"

-- START OF TYPE CHECKING FUNCTIONS

checkValueEnvEnvVAR1 :: Integer -> Integer
checkValueEnvEnvVAR1 value
  | 2 > value || value > 5 = error "envEnvVAR1 illegal value"
  | otherwise = value

checkValueEnvEnvVAR2 :: Integer -> Integer
checkValueEnvEnvVAR2 value
  | 2 > value || value > 5 = error "envEnvVAR2 illegal value"
  | otherwise = value


-- START OF SET FUNCTIONS

updateEnvGenerator :: BTreeEnvironment -> StdGen -> BTreeEnvironment
updateEnvGenerator environment newGen = environment { sereneEnvGenerator = newGen }
updateEnvEnvVAR1Index0 :: BTreeEnvironment -> Integer -> BTreeEnvironment
updateEnvEnvVAR1Index0 environment value = environment { envEnvVAR1Index0 = (checkValueEnvEnvVAR1 value)}
updateEnvEnvVAR1Index1 :: BTreeEnvironment -> Integer -> BTreeEnvironment
updateEnvEnvVAR1Index1 environment value = environment { envEnvVAR1Index1 = (checkValueEnvEnvVAR1 value)}
updateEnvEnvVAR1Index2 :: BTreeEnvironment -> Integer -> BTreeEnvironment
updateEnvEnvVAR1Index2 environment value = environment { envEnvVAR1Index2 = (checkValueEnvEnvVAR1 value)}
updateEnvEnvVAR2Index0 :: BTreeEnvironment -> Integer -> BTreeEnvironment
updateEnvEnvVAR2Index0 environment value = environment { envEnvVAR2Index0 = (checkValueEnvEnvVAR2 value)}
updateEnvEnvVAR2Index1 :: BTreeEnvironment -> Integer -> BTreeEnvironment
updateEnvEnvVAR2Index1 environment value = environment { envEnvVAR2Index1 = (checkValueEnvEnvVAR2 value)}

-- START OF SET FUNCTIONS FOR ARRAYS

updateEnvEnvVAR1 :: Integer -> BTreeEnvironment -> Integer -> BTreeEnvironment
updateEnvEnvVAR1 0 = updateEnvEnvVAR1Index0
updateEnvEnvVAR1 1 = updateEnvEnvVAR1Index1
updateEnvEnvVAR1 2 = updateEnvEnvVAR1Index2
updateEnvEnvVAR1 _ = error "EnvEnvVAR1 illegal index value"
arrayUpdateEnvEnvVAR1 :: BTreeEnvironment -> [(Integer, Integer)] -> BTreeEnvironment
arrayUpdateEnvEnvVAR1 environment []  = environment
arrayUpdateEnvEnvVAR1 environment [(index, value)] = updateEnvEnvVAR1 index environment value
arrayUpdateEnvEnvVAR1 environment indicesValues = environment {
  envEnvVAR1Index0 = newEnvVAR1Index0
  , envEnvVAR1Index1 = newEnvVAR1Index1
  , envEnvVAR1Index2 = newEnvVAR1Index2
  }
    where
      (newEnvVAR1Index0, newEnvVAR1Index1, newEnvVAR1Index2) = updateValues indicesValues
      updateValues :: [(Integer, Integer)] -> (Integer, Integer, Integer)
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
updateEnvEnvVAR2 :: Integer -> BTreeEnvironment -> Integer -> BTreeEnvironment
updateEnvEnvVAR2 0 = updateEnvEnvVAR2Index0
updateEnvEnvVAR2 1 = updateEnvEnvVAR2Index1
updateEnvEnvVAR2 _ = error "EnvEnvVAR2 illegal index value"
arrayUpdateEnvEnvVAR2 :: BTreeEnvironment -> [(Integer, Integer)] -> BTreeEnvironment
arrayUpdateEnvEnvVAR2 environment []  = environment
arrayUpdateEnvEnvVAR2 environment [(index, value)] = updateEnvEnvVAR2 index environment value
arrayUpdateEnvEnvVAR2 environment indicesValues = environment {
  envEnvVAR2Index0 = newEnvVAR2Index0
  , envEnvVAR2Index1 = newEnvVAR2Index1
  }
    where
      (newEnvVAR2Index0, newEnvVAR2Index1) = updateValues indicesValues
      updateValues :: [(Integer, Integer)] -> (Integer, Integer)
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
    newEnvironment = tempEnvironment4
    tickUpdate1EnvVAR1 :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate1EnvVAR1 environment = arrayUpdateEnvEnvVAR1 environment updates
      where
        updates = [updatePair0, updatePair1, updatePair2]
        updatePair0 = ((min 2 (max 0 (76 - (max (envEnvVAR2 1 environment) (envEnvVAR1 0 environment))))), updateValue0)
        updatePair1 = ((min 2 (max 0 (min (max 80 (-4)) ((boardBlDEFINE6 blackboard) * (boardBlDEFINE6 blackboard))))), updateValue1)
        updatePair2 = ((min 2 (max 0 (envEnvVAR2 1 environment))), updateValue2)
        updateValue0 = (min 5 (max 2 (envEnvVAR2 1 environment)))
        updateValue1 = (min 5 (max 2 (abs (min 38 ((envEnvVAR2 1 environment) - (envEnvVAR2 0 environment))))))
        updateValue2 = (min 5 (max 2 (- 77)))

    tempEnvironment1 = tickUpdate1EnvVAR1 tempEnvironment0

    tickUpdate2EnvVAR1 :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate2EnvVAR1 environment = arrayUpdateEnvEnvVAR1 environment updates
      where
        updates = [updatePair0, updatePair1, updatePair2]
        updatePair0 = ((min 2 (max 0 ((min (boardBlFROZENVAR4 0 blackboard) 31) + 55))), updateValue0)
        updatePair1 = ((min 2 (max 0 ((((sereneCOUNT ((-90) < (boardBlDEFINE6 blackboard)) ("no" == (boardBlVAR0 blackboard))) + (sereneCOUNT ((boardBlVAR3 1 blackboard) || False) ((-48) <= (envEnvVAR1 2 environment)))) - (boardBlFROZENVAR4 0 blackboard)) + ((boardBlDEFINE6 blackboard) + (((-90) - 46) + (min (boardBlDEFINE6 blackboard) (envEnvVAR1 1 environment))))))), updateValue1)
        updatePair2 = ((min 2 (max 0 (max ((boardBlDEFINE6 blackboard) + ((envEnvVAR2 0 environment) + (-5))) (-51)))), updateValue2)
        updateValue0
          | ((boardBlVAR0 blackboard) /= (boardBlVAR0 blackboard)) = (min 5 (max 2 (max (-64) (-96))))
          | otherwise = (min 5 (max 2 (abs 74)))
        updateValue1
          | (((boardBlVAR3 0 blackboard) || False) == ((envEnvVAR1 0 environment) <= (envEnvVAR1 1 environment))) = (min 5 (max 2 (- (max (min (envEnvVAR2 0 environment) (envEnvVAR1 1 environment)) (max (-89) (boardBlFROZENVAR4 1 blackboard))))))
          | otherwise = (min 5 (max 2 ((-69) + (21 - 8))))
        updateValue2
          | (sereneXOR (False || (sereneIMPLIES False False)) (boardBlVAR3 1 blackboard)) = (min 5 (max 2 (- (max (boardBlDEFINE6 blackboard) (boardBlFROZENVAR4 0 blackboard)))))
          | otherwise = (min 5 (max 2 (- 50)))

    tempEnvironment2 = tickUpdate2EnvVAR1 tempEnvironment1

    tickUpdate3EnvVAR1 :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate3EnvVAR1 environment = arrayUpdateEnvEnvVAR1 environment updates
      where
        updates = [updatePair0, updatePair1]
        updatePair0 = ((min 2 (max 0 ((sereneCOUNT ((boardBlVAR3 0 blackboard) && True) ((boardBlVAR3 1 blackboard) == (boardBlVAR3 1 blackboard))) + (sereneCOUNT False ((envEnvVAR1 2 environment) <= (boardBlFROZENVAR4 0 blackboard)))))), updateValue0)
        updatePair1 = ((min 2 (max 0 ((65 * ((4 + ((boardBlDEFINE6 blackboard) + (boardBlDEFINE6 blackboard))) * ((envEnvVAR1 1 environment) * 54))) - ((-44) - (boardBlDEFINE6 blackboard))))), updateValue1)
        updateValue0 = (min 5 (max 2 ((envEnvVAR2 1 environment) - ((-78) - 35))))
        updateValue1 = (min 5 (max 2 ((abs (boardBlFROZENVAR4 0 blackboard)) + ((max 37 (envEnvVAR1 2 environment)) + (boardBlDEFINE6 blackboard)))))

    tempEnvironment3 = tickUpdate3EnvVAR1 tempEnvironment2

    tickUpdate4EnvVAR2 :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate4EnvVAR2 environment = arrayUpdateEnvEnvVAR2 environment updates
      where
        updates = [updatePair0]
        updatePair0 = ((min 1 (max 0 (boardBlDEFINE6 blackboard))), updateValue0)
        updateValue0
          | (sereneXOR (sereneIMPLIES (boardBlVAR3 0 blackboard) (boardBlVAR3 0 blackboard)) (boardBlVAR3 0 blackboard)) = (min 5 (max 2 (max (- (-74)) ((-96) + ((-77) + ((envEnvVAR2 0 environment) + (-13)))))))
          | ((boardBlVAR3 1 blackboard) && (boardBlVAR3 0 blackboard)) = (min 5 (max 2 (max 20 (boardBlDEFINE6 blackboard))))
          | otherwise = (min 5 (max 2 (abs (boardBlDEFINE6 blackboard))))

    tempEnvironment4 = tickUpdate4EnvVAR2 tempEnvironment3



-- START OF INITIAL ENVIRONMENT VALUE

initialEnvironment :: Integer -> BTreeBlackboard -> BTreeEnvironment
initialEnvironment seed blackboard = BTreeEnvironment newSereneGenerator newValEnvVAR1Index0 newValEnvVAR1Index1 newValEnvVAR1Index2 newValEnvVAR2Index0 newValEnvVAR2Index1  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen5
    partialEnvironmentEnvVAR1Index0 = BTreeEnvironment newSereneGenerator 0 0 0 0 0
    initValEnvVAR1Index0 :: StdGen -> (Integer, StdGen)
    initValEnvVAR1Index0 curGen
      | False = ((min 5 (max 2 (sereneCOUNT (73 <= (-90)) ((-5) < 43)))), curGen)
      | ((True == True) == (sereneXOR False True)) = ((min 5 (max 2 (4 - (-61)))), curGen)
      | otherwise = ((min 5 (max 2 (- 60))), curGen)
      where
        environment = partialEnvironmentEnvVAR1Index0

    (newValEnvVAR1Index0, tempGen1) = initValEnvVAR1Index0 tempGen0

    partialEnvironmentEnvVAR1Index1 = BTreeEnvironment newSereneGenerator newValEnvVAR1Index0 0 0 0 0
    initValEnvVAR1Index1 :: StdGen -> (Integer, StdGen)
    initValEnvVAR1Index1 curGen
      | False = ((min 5 (max 2 (sereneCOUNT (73 <= (-90)) ((-5) < 43)))), curGen)
      | ((True == True) == (sereneXOR False True)) = ((min 5 (max 2 (4 - (-61)))), curGen)
      | otherwise = ((min 5 (max 2 (- 60))), curGen)
      where
        environment = partialEnvironmentEnvVAR1Index1

    (newValEnvVAR1Index1, tempGen2) = initValEnvVAR1Index1 tempGen1

    partialEnvironmentEnvVAR1Index2 = BTreeEnvironment newSereneGenerator newValEnvVAR1Index0 newValEnvVAR1Index1 0 0 0
    initValEnvVAR1Index2 :: StdGen -> (Integer, StdGen)
    initValEnvVAR1Index2 curGen
      | False = ((min 5 (max 2 (sereneCOUNT (73 <= (-90)) ((-5) < 43)))), curGen)
      | ((True == True) == (sereneXOR False True)) = ((min 5 (max 2 (4 - (-61)))), curGen)
      | otherwise = ((min 5 (max 2 (- 60))), curGen)
      where
        environment = partialEnvironmentEnvVAR1Index2

    (newValEnvVAR1Index2, tempGen3) = initValEnvVAR1Index2 tempGen2

    partialEnvironmentEnvVAR2Index0 = BTreeEnvironment newSereneGenerator newValEnvVAR1Index0 newValEnvVAR1Index1 newValEnvVAR1Index2 0 0
    initValEnvVAR2Index0 :: StdGen -> (Integer, StdGen)
    initValEnvVAR2Index0 curGen
      | ((sereneXOR False True) == (False || True)) = ((min 5 (max 2 (min (- (-53)) (-5)))), curGen)
      | otherwise = ((min 5 (max 2 (-7))), curGen)
      where
        environment = partialEnvironmentEnvVAR2Index0

    (newValEnvVAR2Index0, tempGen4) = initValEnvVAR2Index0 tempGen3

    partialEnvironmentEnvVAR2Index1 = BTreeEnvironment newSereneGenerator newValEnvVAR1Index0 newValEnvVAR1Index1 newValEnvVAR1Index2 newValEnvVAR2Index0 0
    initValEnvVAR2Index1 :: StdGen -> (Integer, StdGen)
    initValEnvVAR2Index1 curGen = ((min 5 (max 2 (envEnvVAR1 2 environment))), curGen)
      where
        environment = partialEnvironmentEnvVAR2Index1

    (newValEnvVAR2Index1, tempGen5) = initValEnvVAR2Index1 tempGen4


