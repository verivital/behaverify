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
  }

fromBTreeEnvironmentToString :: BTreeBlackboard -> BTreeEnvironment -> String
fromBTreeEnvironmentToString blackboard environment = "Env = {" ++ "envEnvVAR1: " ++ "[" ++ show (envEnvVAR1 0 environment) ++ ", " ++ show (envEnvVAR1 1 environment) ++ ", " ++ show (envEnvVAR1 2 environment)++ "]" ++ ", " ++ "envEnvDEFINE5: " ++ "[" ++ show (envEnvDEFINE5 0 blackboard environment) ++ ", " ++ show (envEnvDEFINE5 1 blackboard environment) ++ ", " ++ show (envEnvDEFINE5 2 blackboard environment)++ "]" ++ "}"

-- START OF ENVIRONMENT FUNCTIONS

envEnvDEFINE5 :: Integer -> BTreeBlackboard -> BTreeEnvironment -> Bool
envEnvDEFINE5 0 blackboard environment
  | (sereneIMPLIES ((boardBlVAR2 blackboard) == True) True) = ((boardBlVAR2 blackboard) == (boardBlVAR2 blackboard))
  | (sereneXOR (boardBlVAR2 blackboard) (boardBlVAR2 blackboard)) = ((-2) <= (-3))
  | otherwise = ((boardBlVAR0 blackboard) /= (min (-95) (boardBlDEFINE4 blackboard)))
envEnvDEFINE5 1 blackboard environment
  | (10 > 99) = True
  | (boardBlVAR2 blackboard) = (sereneXNOR (boardBlVAR2 blackboard) True)
  | otherwise = ((0 - 42) >= (boardBlDEFINE4 blackboard))
envEnvDEFINE5 2 blackboard environment
  | (True && ((boardBlDEFINE4 blackboard) >= (boardBlVAR0 blackboard))) = ((80 + ((-27) + ((envEnvVAR1 0 environment) + (boardBlVAR0 blackboard)))) > (max 27 (-51)))
  | otherwise = ((boardBlVAR2 blackboard) == ((boardBlVAR0 blackboard) <= (boardBlDEFINE4 blackboard)))
envEnvDEFINE5 _ _ _ = error "envEnvDEFINE5 illegal index value"

-- START OF GET FUNCTIONS FOR ARRAYS

envEnvVAR1 :: Integer -> BTreeEnvironment -> Integer
envEnvVAR1 0 = envEnvVAR1Index0
envEnvVAR1 1 = envEnvVAR1Index1
envEnvVAR1 2 = envEnvVAR1Index2
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
updateEnvEnvVAR1Index2 :: BTreeEnvironment -> Integer -> BTreeEnvironment
updateEnvEnvVAR1Index2 environment value = environment { envEnvVAR1Index2 = (checkValueEnvEnvVAR1 value)}

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
        updates = [updatePair0, updatePair1]
        updatePair0 = ((min 2 (max 0 (envEnvVAR1 0 environment))), updateValue0)
        updatePair1 = ((min 2 (max 0 (- (-4)))), updateValue1)
        updateValue0
          | (sereneXOR (False == ((boardBlVAR2 blackboard) || (boardBlVAR2 blackboard))) ((boardBlVAR0 blackboard) < (envEnvVAR1 1 environment))) = (min 5 (max 2 ((sereneCOUNT (sereneXOR ((boardBlVAR2 blackboard) || (boardBlVAR2 blackboard)) (sereneXNOR True True)) ((True == False) == (True && (boardBlVAR2 blackboard)))) + (sereneCOUNT (((-19) >= 36) && (False || (envEnvDEFINE5 2 blackboard environment))) ((-73) < (abs (boardBlDEFINE4 blackboard)))))))
          | otherwise = (min 5 (max 2 (-28)))
        updateValue1
          | ((((boardBlVAR0 blackboard) - 35) * ((-76) * (((boardBlDEFINE4 blackboard) * ((boardBlDEFINE4 blackboard) * (93 * (boardBlVAR0 blackboard)))) * (-49)))) == (boardBlVAR0 blackboard)) = (min 5 (max 2 (-84)))
          | otherwise = (min 5 (max 2 (boardBlVAR0 blackboard)))

    tempEnvironment1 = tickUpdate1EnvVAR1 tempEnvironment0

    tickUpdate2EnvVAR1 :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate2EnvVAR1 environment = arrayUpdateEnvEnvVAR1 environment updates
      where
        updates = [updatePair0]
        updatePair0 = ((min 2 (max 0 13)), updateValue0)
        updateValue0
          | (False == False) = (min 5 (max 2 (min (-11) (abs 34))))
          | otherwise = (min 5 (max 2 (abs (sereneCOUNT (sereneIMPLIES True (envEnvDEFINE5 0 blackboard environment)) (False == True)))))

    tempEnvironment2 = tickUpdate2EnvVAR1 tempEnvironment1

    tickUpdate3EnvVAR1 :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate3EnvVAR1 environment = arrayUpdateEnvEnvVAR1 environment updates
      where
        updates = [updatePair0, updatePair1]
        updatePair0 = ((min 2 (max 0 (abs (min (- (-37)) (-71))))), updateValue0)
        updatePair1 = ((min 2 (max 0 ((64 + (-55)) * ((3 - (envEnvVAR1 1 environment)) * (((sereneCOUNT ((envEnvVAR1 1 environment) == 41) (False == True)) + (sereneCOUNT False (sereneXOR (envEnvDEFINE5 0 blackboard environment) (envEnvDEFINE5 0 blackboard environment)))) * (boardBlDEFINE4 blackboard)))))), updateValue1)
        updateValue0
          | True = (min 5 (max 2 (- (boardBlVAR0 blackboard))))
          | otherwise = (min 5 (max 2 (27 * ((39 * ((-77) * ((44 - 48) * (-11)))) * (envEnvVAR1 0 environment)))))
        updateValue1
          | True = (min 5 (max 2 (sereneCOUNT (sereneXOR True (sereneIMPLIES (envEnvDEFINE5 2 blackboard environment) False)) ((-80) > ((-25) - (-42))))))
          | otherwise = (min 5 (max 2 (min 15 (boardBlVAR0 blackboard))))

    tempEnvironment3 = tickUpdate3EnvVAR1 tempEnvironment2

    tickUpdate4EnvVAR1 :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate4EnvVAR1 environment = arrayUpdateEnvEnvVAR1 environment updates
      where
        updates = [updatePair0, updatePair1, updatePair2]
        updatePair0 = ((min 2 (max 0 (max (envEnvVAR1 1 environment) (-86)))), updateValue0)
        updatePair1 = ((min 2 (max 0 ((sereneCOUNT (True && (envEnvDEFINE5 0 blackboard environment)) ((boardBlDEFINE4 blackboard) < (-31))) + (sereneCOUNT False (sereneIMPLIES True True))))), updateValue1)
        updatePair2 = ((min 2 (max 0 18)), updateValue2)
        updateValue0
          | (boardBlVAR2 blackboard) = (min 5 (max 2 (boardBlDEFINE4 blackboard)))
          | otherwise = (min 5 (max 2 (boardBlVAR0 blackboard)))
        updateValue1
          | ((-5) >= (boardBlDEFINE4 blackboard)) = (min 5 (max 2 ((sereneCOUNT (((sereneCOUNT ((boardBlVAR2 blackboard) == False) (91 <= (-39))) + (sereneCOUNT (sereneXOR (envEnvDEFINE5 2 blackboard environment) (boardBlVAR2 blackboard)) (True == True))) > (49 + ((-29) + ((boardBlVAR0 blackboard) + (boardBlVAR0 blackboard))))) (((envEnvVAR1 1 environment) < 95) && False)) + (sereneCOUNT (((boardBlVAR2 blackboard) || (boardBlVAR2 blackboard)) /= True) ((max 76 (-72)) >= (-2))))))
          | otherwise = (min 5 (max 2 (abs (sereneCOUNT (63 < (boardBlDEFINE4 blackboard)) ((boardBlVAR2 blackboard) == True)))))
        updateValue2
          | ((boardBlVAR0 blackboard) == (- (-29))) = (min 5 (max 2 (- (min (envEnvVAR1 0 environment) 95))))
          | otherwise = (min 5 (max 2 (max (max 44 (boardBlDEFINE4 blackboard)) (66 * ((abs (boardBlDEFINE4 blackboard)) * ((-44) * (-94)))))))

    tempEnvironment4 = tickUpdate4EnvVAR1 tempEnvironment3



-- START OF INITIAL ENVIRONMENT VALUE

initialEnvironment :: Integer -> BTreeBlackboard -> BTreeEnvironment
initialEnvironment seed blackboard = BTreeEnvironment newSereneGenerator newValEnvVAR1Index0 newValEnvVAR1Index1 newValEnvVAR1Index2  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen3
    partialEnvironmentEnvVAR1Index0 = BTreeEnvironment newSereneGenerator 0 0 0
    initValEnvVAR1Index0 :: StdGen -> (Integer, StdGen)
    initValEnvVAR1Index0 curGen
      | (sereneIMPLIES (True || False) ((boardBlVAR0 blackboard) == ((-98) - (boardBlVAR0 blackboard)))) = ((min 5 (max 2 (max (37 - (boardBlVAR0 blackboard)) (abs (boardBlVAR0 blackboard))))), curGen)
      | otherwise = ((min 5 (max 2 (boardBlVAR0 blackboard))), curGen)
      where
        environment = partialEnvironmentEnvVAR1Index0

    (newValEnvVAR1Index0, tempGen1) = initValEnvVAR1Index0 tempGen0

    partialEnvironmentEnvVAR1Index1 = BTreeEnvironment newSereneGenerator newValEnvVAR1Index0 0 0
    initValEnvVAR1Index1 :: StdGen -> (Integer, StdGen)
    initValEnvVAR1Index1 curGen
      | (sereneIMPLIES (True || False) ((boardBlVAR0 blackboard) == ((-98) - (boardBlVAR0 blackboard)))) = ((min 5 (max 2 (max (37 - (boardBlVAR0 blackboard)) (abs (boardBlVAR0 blackboard))))), curGen)
      | otherwise = ((min 5 (max 2 (boardBlVAR0 blackboard))), curGen)
      where
        environment = partialEnvironmentEnvVAR1Index1

    (newValEnvVAR1Index1, tempGen2) = initValEnvVAR1Index1 tempGen1

    partialEnvironmentEnvVAR1Index2 = BTreeEnvironment newSereneGenerator newValEnvVAR1Index0 newValEnvVAR1Index1 0
    initValEnvVAR1Index2 :: StdGen -> (Integer, StdGen)
    initValEnvVAR1Index2 curGen
      | (sereneIMPLIES (True || False) ((boardBlVAR0 blackboard) == ((-98) - (boardBlVAR0 blackboard)))) = ((min 5 (max 2 (max (37 - (boardBlVAR0 blackboard)) (abs (boardBlVAR0 blackboard))))), curGen)
      | otherwise = ((min 5 (max 2 (boardBlVAR0 blackboard))), curGen)
      where
        environment = partialEnvironmentEnvVAR1Index2

    (newValEnvVAR1Index2, tempGen3) = initValEnvVAR1Index2 tempGen2


