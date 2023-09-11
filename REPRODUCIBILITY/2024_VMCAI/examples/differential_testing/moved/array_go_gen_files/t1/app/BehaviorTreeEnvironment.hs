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
  , envEnvVAR2Index2 :: Integer
  , envEnvVAR3 :: Integer
  , envEnvFROZENVAR4Index0 :: Integer
  , envEnvFROZENVAR4Index1 :: Integer
  }

fromBTreeEnvironmentToString :: BTreeBlackboard -> BTreeEnvironment -> String
fromBTreeEnvironmentToString blackboard environment = "Env = {" ++ "envEnvVAR1: " ++ "[" ++ show (envEnvVAR1 0 environment) ++ ", " ++ show (envEnvVAR1 1 environment) ++ ", " ++ show (envEnvVAR1 2 environment)++ "]" ++ ", " ++ "envEnvVAR2: " ++ "[" ++ show (envEnvVAR2 0 environment) ++ ", " ++ show (envEnvVAR2 1 environment) ++ ", " ++ show (envEnvVAR2 2 environment)++ "]" ++ ", " ++ "envEnvVAR3: " ++ show (envEnvVAR3 environment) ++ ", " ++ "envEnvFROZENVAR4: " ++ "[" ++ show (envEnvFROZENVAR4 0 environment) ++ ", " ++ show (envEnvFROZENVAR4 1 environment)++ "]" ++ "}"

-- START OF ENVIRONMENT FUNCTIONS


-- START OF GET FUNCTIONS FOR ARRAYS

envEnvVAR1 :: Integer -> BTreeEnvironment -> Integer
envEnvVAR1 0 = envEnvVAR1Index0
envEnvVAR1 1 = envEnvVAR1Index1
envEnvVAR1 2 = envEnvVAR1Index2
envEnvVAR1 _ = error "envEnvVAR1 illegal index value"
envEnvVAR2 :: Integer -> BTreeEnvironment -> Integer
envEnvVAR2 0 = envEnvVAR2Index0
envEnvVAR2 1 = envEnvVAR2Index1
envEnvVAR2 2 = envEnvVAR2Index2
envEnvVAR2 _ = error "envEnvVAR2 illegal index value"
envEnvFROZENVAR4 :: Integer -> BTreeEnvironment -> Integer
envEnvFROZENVAR4 0 = envEnvFROZENVAR4Index0
envEnvFROZENVAR4 1 = envEnvFROZENVAR4Index1
envEnvFROZENVAR4 _ = error "envEnvFROZENVAR4 illegal index value"

-- START OF TYPE CHECKING FUNCTIONS

checkValueEnvEnvVAR1 :: Integer -> Integer
checkValueEnvEnvVAR1 value
  | 2 > value || value > 5 = error "envEnvVAR1 illegal value"
  | otherwise = value

checkValueEnvEnvVAR2 :: Integer -> Integer
checkValueEnvEnvVAR2 value
  | (-5) > value || value > (-2) = error "envEnvVAR2 illegal value"
  | otherwise = value

checkValueEnvEnvVAR3 :: Integer -> Integer
checkValueEnvEnvVAR3 value
  | 2 > value || value > 5 = error "envEnvVAR3 illegal value"
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
updateEnvEnvVAR2Index2 :: BTreeEnvironment -> Integer -> BTreeEnvironment
updateEnvEnvVAR2Index2 environment value = environment { envEnvVAR2Index2 = (checkValueEnvEnvVAR2 value)}
updateEnvEnvVAR3 :: BTreeEnvironment -> Integer -> BTreeEnvironment
updateEnvEnvVAR3 environment value = environment { envEnvVAR3 = (checkValueEnvEnvVAR3 value)}

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
updateEnvEnvVAR2 2 = updateEnvEnvVAR2Index2
updateEnvEnvVAR2 _ = error "EnvEnvVAR2 illegal index value"
arrayUpdateEnvEnvVAR2 :: BTreeEnvironment -> [(Integer, Integer)] -> BTreeEnvironment
arrayUpdateEnvEnvVAR2 environment []  = environment
arrayUpdateEnvEnvVAR2 environment [(index, value)] = updateEnvEnvVAR2 index environment value
arrayUpdateEnvEnvVAR2 environment indicesValues = environment {
  envEnvVAR2Index0 = newEnvVAR2Index0
  , envEnvVAR2Index1 = newEnvVAR2Index1
  , envEnvVAR2Index2 = newEnvVAR2Index2
  }
    where
      (newEnvVAR2Index0, newEnvVAR2Index1, newEnvVAR2Index2) = updateValues indicesValues
      updateValues :: [(Integer, Integer)] -> (Integer, Integer, Integer)
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
    newEnvironment = tempEnvironment4
    tickUpdate1EnvVAR3 :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate1EnvVAR3 environment
      | ((boardBlDEFINE7 blackboard) == (70 < (boardBlVAR0 0 blackboard))) = updateEnvEnvVAR3 environment (min 5 (max 2 ((boardBlVAR0 0 blackboard) - (envEnvVAR1 1 environment))))
      | otherwise = updateEnvEnvVAR3 environment (min 5 (max 2 (((envEnvFROZENVAR4 0 environment) * ((-16) * 61)) * ((envEnvFROZENVAR4 1 environment) * ((boardBlVAR0 1 blackboard) * (max 76 (-78)))))))

    tempEnvironment1 = tickUpdate1EnvVAR3 tempEnvironment0

    tickUpdate2EnvVAR2 :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate2EnvVAR2 environment = arrayUpdateEnvEnvVAR2 environment updates
      where
        updates = [updatePair0, updatePair1, updatePair2]
        updatePair0 = ((min 2 (max 0 ((max (envEnvFROZENVAR4 1 environment) 67) * ((max (abs (envEnvVAR1 0 environment)) 0) * ((envEnvVAR1 2 environment) + ((-12) + (envEnvVAR2 2 environment))))))), updateValue0)
        updatePair1 = ((min 2 (max 0 ((-58) - (-97)))), updateValue1)
        updatePair2 = ((min 2 (max 0 (-22))), updateValue2)
        updateValue0
          | (((boardBlDEFINE7 blackboard) && False) == True) = (min (-2) (max (-5) (-26)))
          | (boardBlDEFINE7 blackboard) = (min (-2) (max (-5) ((sereneCOUNT (sereneIMPLIES (sereneXOR (True == True) (sereneXOR False False)) False) ((-39) < (envEnvVAR1 1 environment))) + (sereneCOUNT (sereneXNOR (sereneXNOR (boardBlDEFINE7 blackboard) (boardBlDEFINE7 blackboard)) (sereneIMPLIES False True)) ((-61) >= (max (-82) (boardBlVAR0 0 blackboard)))))))
          | otherwise = (min (-2) (max (-5) (envEnvFROZENVAR4 0 environment)))
        updateValue1
          | ((sereneXNOR False True) && (boardBlDEFINE7 blackboard)) = (min (-2) (max (-5) (boardBlVAR0 1 blackboard)))
          | (True || (boardBlDEFINE7 blackboard)) = (min (-2) (max (-5) (abs (min (envEnvFROZENVAR4 1 environment) (-93)))))
          | otherwise = (min (-2) (max (-5) ((max ((sereneCOUNT (False == True) ((-54) <= (envEnvVAR2 0 environment))) + (sereneCOUNT False (sereneXOR True (boardBlDEFINE7 blackboard)))) ((envEnvVAR3 environment) * 6)) + ((-16) + ((- 26) + (max 77 (-24)))))))
        updateValue2
          | (sereneIMPLIES False (boardBlDEFINE7 blackboard)) = (min (-2) (max (-5) (- 73)))
          | (((-75) /= (envEnvVAR2 1 environment)) && (boardBlDEFINE7 blackboard)) = (min (-2) (max (-5) (max (max (envEnvVAR3 environment) (envEnvVAR3 environment)) (-19))))
          | otherwise = (min (-2) (max (-5) 38))

    tempEnvironment2 = tickUpdate2EnvVAR2 tempEnvironment1

    tickUpdate3EnvVAR1 :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate3EnvVAR1 environment = arrayUpdateEnvEnvVAR1 environment updates
      where
        updates = [updatePair0, updatePair1, updatePair2]
        updatePair0 = ((min 2 (max 0 ((sereneCOUNT (((envEnvVAR3 environment) - (-73)) == (97 * ((envEnvVAR1 0 environment) * (envEnvVAR3 environment)))) (((-36) /= (envEnvVAR2 0 environment)) && ((envEnvVAR3 environment) < 81))) + (sereneCOUNT (43 < (envEnvFROZENVAR4 0 environment)) (sereneXOR ((envEnvFROZENVAR4 1 environment) > (envEnvVAR2 1 environment)) True))))), updateValue0)
        updatePair1 = ((min 2 (max 0 ((abs 39) * (((-42) * ((boardBlVAR0 1 blackboard) * ((-37) * (-65)))) * (((sereneCOUNT ((boardBlDEFINE7 blackboard) || True) ((-59) <= (-65))) + (sereneCOUNT ((boardBlDEFINE7 blackboard) == False) ((-61) == 47))) * (95 * (10 * 69))))))), updateValue1)
        updatePair2 = ((min 2 (max 0 (abs (-38)))), updateValue2)
        updateValue0
          | ((boardBlDEFINE7 blackboard) || (boardBlDEFINE7 blackboard)) = (min 5 (max 2 ((min (envEnvVAR3 environment) (-1)) - (-27))))
          | ((boardBlDEFINE7 blackboard) == ((envEnvVAR1 1 environment) < (envEnvVAR1 2 environment))) = (min 5 (max 2 (-59)))
          | otherwise = (min 5 (max 2 ((boardBlVAR0 0 blackboard) * (((-99) * ((envEnvVAR3 environment) * 89)) * (abs 50)))))
        updateValue1
          | (sereneIMPLIES (boardBlDEFINE7 blackboard) True) = (min 5 (max 2 (sereneCOUNT (True || True) (True == (boardBlDEFINE7 blackboard)))))
          | ((envEnvVAR1 1 environment) >= (envEnvVAR2 0 environment)) = (min 5 (max 2 (max (-62) (-95))))
          | otherwise = (min 5 (max 2 (max (envEnvVAR3 environment) (envEnvVAR3 environment))))
        updateValue2
          | ((boardBlDEFINE7 blackboard) == (53 < 61)) = (min 5 (max 2 ((((-77) * (26 * ((envEnvVAR2 2 environment) * (boardBlVAR0 0 blackboard)))) - (-94)) - ((envEnvVAR2 1 environment) - (envEnvVAR1 1 environment)))))
          | False = (min 5 (max 2 ((abs (envEnvFROZENVAR4 0 environment)) - (sereneCOUNT ((envEnvVAR3 environment) > (-31)) (sereneXNOR False True)))))
          | otherwise = (min 5 (max 2 (envEnvFROZENVAR4 0 environment)))

    tempEnvironment3 = tickUpdate3EnvVAR1 tempEnvironment2

    tickUpdate4EnvVAR1 :: BTreeEnvironment -> BTreeEnvironment
    tickUpdate4EnvVAR1 environment = arrayUpdateEnvEnvVAR1 environment updates
      where
        updates = [updatePair0, updatePair1]
        updatePair0 = ((min 2 (max 0 ((sereneCOUNT ((boardBlDEFINE7 blackboard) || True) ((boardBlDEFINE7 blackboard) == False)) + (sereneCOUNT False ((envEnvFROZENVAR4 0 environment) <= 93))))), updateValue0)
        updatePair1 = ((min 2 (max 0 (42 * ((-100) * (-49))))), updateValue1)
        updateValue0 = (min 5 (max 2 (min ((sereneCOUNT ((boardBlVAR0 1 blackboard) <= (- (boardBlVAR0 1 blackboard))) (sereneIMPLIES (False || (boardBlDEFINE7 blackboard)) (True && (boardBlDEFINE7 blackboard)))) + (sereneCOUNT False (sereneXNOR (sereneXNOR True (boardBlDEFINE7 blackboard)) False))) (abs (abs (-1))))))
        updateValue1 = (min 5 (max 2 (abs (envEnvVAR3 environment))))

    tempEnvironment4 = tickUpdate4EnvVAR1 tempEnvironment3



-- START OF INITIAL ENVIRONMENT VALUE

initialEnvironment :: Integer -> BTreeBlackboard -> BTreeEnvironment
initialEnvironment seed blackboard = BTreeEnvironment newSereneGenerator newValEnvVAR1Index0 newValEnvVAR1Index1 newValEnvVAR1Index2 newValEnvVAR2Index0 newValEnvVAR2Index1 newValEnvVAR2Index2 newValEnvVAR3 newValEnvFROZENVAR4Index0 newValEnvFROZENVAR4Index1  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen9
    partialEnvironmentEnvVAR1Index0 = BTreeEnvironment newSereneGenerator 0 0 0 0 0 0 0 0 0
    initValEnvVAR1Index0 :: StdGen -> (Integer, StdGen)
    initValEnvVAR1Index0 curGen
      | ((57 - 1) >= (max (boardBlVAR0 1 blackboard) (boardBlVAR0 0 blackboard))) = ((min 5 (max 2 (abs (boardBlVAR0 1 blackboard)))), curGen)
      | ((sereneIMPLIES False True) && False) = ((min 5 (max 2 (abs (boardBlVAR0 1 blackboard)))), curGen)
      | otherwise = ((min 5 (max 2 11)), curGen)
      where
        environment = partialEnvironmentEnvVAR1Index0

    (newValEnvVAR1Index0, tempGen1) = initValEnvVAR1Index0 tempGen0

    partialEnvironmentEnvVAR1Index1 = BTreeEnvironment newSereneGenerator newValEnvVAR1Index0 0 0 0 0 0 0 0 0
    initValEnvVAR1Index1 :: StdGen -> (Integer, StdGen)
    initValEnvVAR1Index1 curGen = ((min 5 (max 2 (- ((sereneCOUNT (False == False) ((-80) > (-59))) + (sereneCOUNT False (sereneIMPLIES True False)))))), curGen)
      where
        environment = partialEnvironmentEnvVAR1Index1

    (newValEnvVAR1Index1, tempGen2) = initValEnvVAR1Index1 tempGen1

    partialEnvironmentEnvVAR1Index2 = BTreeEnvironment newSereneGenerator newValEnvVAR1Index0 newValEnvVAR1Index1 0 0 0 0 0 0 0
    initValEnvVAR1Index2 :: StdGen -> (Integer, StdGen)
    initValEnvVAR1Index2 curGen = ((min 5 (max 2 (abs (boardBlVAR0 0 blackboard)))), curGen)
      where
        environment = partialEnvironmentEnvVAR1Index2

    (newValEnvVAR1Index2, tempGen3) = initValEnvVAR1Index2 tempGen2

    partialEnvironmentEnvVAR2Index0 = BTreeEnvironment newSereneGenerator newValEnvVAR1Index0 newValEnvVAR1Index1 newValEnvVAR1Index2 0 0 0 0 0 0
    initValEnvVAR2Index0 :: StdGen -> (Integer, StdGen)
    initValEnvVAR2Index0 curGen = ((min (-2) (max (-5) (sereneCOUNT (False && (sereneXOR True True)) (30 > 63)))), curGen)
      where
        environment = partialEnvironmentEnvVAR2Index0

    (newValEnvVAR2Index0, tempGen4) = initValEnvVAR2Index0 tempGen3

    partialEnvironmentEnvVAR2Index1 = BTreeEnvironment newSereneGenerator newValEnvVAR1Index0 newValEnvVAR1Index1 newValEnvVAR1Index2 newValEnvVAR2Index0 0 0 0 0 0
    initValEnvVAR2Index1 :: StdGen -> (Integer, StdGen)
    initValEnvVAR2Index1 curGen
      | ((abs (envEnvVAR1 0 environment)) < ((-87) * ((-16) * ((envEnvVAR1 1 environment) * (-1))))) = ((min (-2) (max (-5) (((boardBlVAR0 0 blackboard) * ((-22) * 89)) - (-10)))), curGen)
      | (sereneXOR (((envEnvVAR1 0 environment) - 74) > 54) (36 <= (envEnvVAR1 1 environment))) = ((min (-2) (max (-5) (((min (envEnvVAR1 2 environment) (envEnvVAR1 2 environment)) * (boardBlVAR0 0 blackboard)) - ((-28) * (8 * ((envEnvVAR1 1 environment) * (envEnvVAR1 0 environment))))))), curGen)
      | otherwise = ((min (-2) (max (-5) (-61))), curGen)
      where
        environment = partialEnvironmentEnvVAR2Index1

    (newValEnvVAR2Index1, tempGen5) = initValEnvVAR2Index1 tempGen4

    partialEnvironmentEnvVAR2Index2 = BTreeEnvironment newSereneGenerator newValEnvVAR1Index0 newValEnvVAR1Index1 newValEnvVAR1Index2 newValEnvVAR2Index0 newValEnvVAR2Index1 0 0 0 0
    initValEnvVAR2Index2 :: StdGen -> (Integer, StdGen)
    initValEnvVAR2Index2 curGen
      | True = ((min (-2) (max (-5) (envEnvVAR1 1 environment))), curGen)
      | otherwise = ((min (-2) (max (-5) (max ((envEnvVAR1 1 environment) + 27) (-3)))), curGen)
      where
        environment = partialEnvironmentEnvVAR2Index2

    (newValEnvVAR2Index2, tempGen6) = initValEnvVAR2Index2 tempGen5

    partialEnvironmentEnvVAR3 = BTreeEnvironment newSereneGenerator newValEnvVAR1Index0 newValEnvVAR1Index1 newValEnvVAR1Index2 newValEnvVAR2Index0 newValEnvVAR2Index1 newValEnvVAR2Index2 0 0 0
    initValEnvVAR3 :: StdGen -> (Integer, StdGen)
    initValEnvVAR3 curGen = ((min 5 (max 2 (sereneCOUNT ((envEnvVAR2 0 environment) >= (-36)) (True == True)))), curGen)
      where
        environment = partialEnvironmentEnvVAR3

    (newValEnvVAR3, tempGen7) = initValEnvVAR3 tempGen6

    partialEnvironmentEnvFROZENVAR4Index0 = BTreeEnvironment newSereneGenerator newValEnvVAR1Index0 newValEnvVAR1Index1 newValEnvVAR1Index2 newValEnvVAR2Index0 newValEnvVAR2Index1 newValEnvVAR2Index2 newValEnvVAR3 0 0
    initValEnvFROZENVAR4Index0 :: StdGen -> (Integer, StdGen)
    initValEnvFROZENVAR4Index0 curGen = ((min 5 (max 2 (boardBlVAR0 1 blackboard))), curGen)
      where
        environment = partialEnvironmentEnvFROZENVAR4Index0

    (newValEnvFROZENVAR4Index0, tempGen8) = initValEnvFROZENVAR4Index0 tempGen7

    partialEnvironmentEnvFROZENVAR4Index1 = BTreeEnvironment newSereneGenerator newValEnvVAR1Index0 newValEnvVAR1Index1 newValEnvVAR1Index2 newValEnvVAR2Index0 newValEnvVAR2Index1 newValEnvVAR2Index2 newValEnvVAR3 newValEnvFROZENVAR4Index0 0
    initValEnvFROZENVAR4Index1 :: StdGen -> (Integer, StdGen)
    initValEnvFROZENVAR4Index1 curGen = ((min 5 (max 2 (boardBlVAR0 1 blackboard))), curGen)
      where
        environment = partialEnvironmentEnvFROZENVAR4Index1

    (newValEnvFROZENVAR4Index1, tempGen9) = initValEnvFROZENVAR4Index1 tempGen8


