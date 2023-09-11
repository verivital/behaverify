module BehaviorTreeEnvironment where
import SereneRandomizer
import System.Random
import SereneOperations
import BehaviorTreeBlackboard

data BTreeEnvironment = BTreeEnvironment {
  sereneEnvGenerator :: StdGen
  , envEnvVAR1Index0 :: Bool
  , envEnvVAR1Index1 :: Bool
  , envEnvVAR2 :: String
  , envEnvFROZENVAR3Index0 :: String
  , envEnvFROZENVAR3Index1 :: String
  , envEnvFROZENVAR3Index2 :: String
  , envEnvFROZENVAR4Index0 :: Integer
  , envEnvFROZENVAR4Index1 :: Integer
  , envEnvFROZENVAR4Index2 :: Integer
  }

fromBTreeEnvironmentToString :: BTreeBlackboard -> BTreeEnvironment -> String
fromBTreeEnvironmentToString blackboard environment = "Env = {" ++ "envEnvVAR1: " ++ "[" ++ show (envEnvVAR1 0 environment) ++ ", " ++ show (envEnvVAR1 1 environment)++ "]" ++ ", " ++ "envEnvVAR2: " ++ show (envEnvVAR2 environment) ++ ", " ++ "envEnvFROZENVAR3: " ++ "[" ++ show (envEnvFROZENVAR3 0 environment) ++ ", " ++ show (envEnvFROZENVAR3 1 environment) ++ ", " ++ show (envEnvFROZENVAR3 2 environment)++ "]" ++ ", " ++ "envEnvFROZENVAR4: " ++ "[" ++ show (envEnvFROZENVAR4 0 environment) ++ ", " ++ show (envEnvFROZENVAR4 1 environment) ++ ", " ++ show (envEnvFROZENVAR4 2 environment)++ "]" ++ "}"

-- START OF ENVIRONMENT FUNCTIONS


-- START OF GET FUNCTIONS FOR ARRAYS

envEnvVAR1 :: Integer -> BTreeEnvironment -> Bool
envEnvVAR1 0 = envEnvVAR1Index0
envEnvVAR1 1 = envEnvVAR1Index1
envEnvVAR1 _ = error "envEnvVAR1 illegal index value"
envEnvFROZENVAR3 :: Integer -> BTreeEnvironment -> String
envEnvFROZENVAR3 0 = envEnvFROZENVAR3Index0
envEnvFROZENVAR3 1 = envEnvFROZENVAR3Index1
envEnvFROZENVAR3 2 = envEnvFROZENVAR3Index2
envEnvFROZENVAR3 _ = error "envEnvFROZENVAR3 illegal index value"
envEnvFROZENVAR4 :: Integer -> BTreeEnvironment -> Integer
envEnvFROZENVAR4 0 = envEnvFROZENVAR4Index0
envEnvFROZENVAR4 1 = envEnvFROZENVAR4Index1
envEnvFROZENVAR4 2 = envEnvFROZENVAR4Index2
envEnvFROZENVAR4 _ = error "envEnvFROZENVAR4 illegal index value"

-- START OF TYPE CHECKING FUNCTIONS

checkValueEnvEnvVAR1 :: Bool -> Bool
checkValueEnvEnvVAR1 value = value

checkValueEnvEnvVAR2 :: String -> String
checkValueEnvEnvVAR2 "yes" = "yes"
checkValueEnvEnvVAR2 "no" = "no"
checkValueEnvEnvVAR2 "both" = "both"
checkValueEnvEnvVAR2 _ = error "envEnvVAR2 illegal value"


-- START OF SET FUNCTIONS

updateEnvGenerator :: BTreeEnvironment -> StdGen -> BTreeEnvironment
updateEnvGenerator environment newGen = environment { sereneEnvGenerator = newGen }
updateEnvEnvVAR1Index0 :: BTreeEnvironment -> Bool -> BTreeEnvironment
updateEnvEnvVAR1Index0 environment value = environment { envEnvVAR1Index0 = (checkValueEnvEnvVAR1 value)}
updateEnvEnvVAR1Index1 :: BTreeEnvironment -> Bool -> BTreeEnvironment
updateEnvEnvVAR1Index1 environment value = environment { envEnvVAR1Index1 = (checkValueEnvEnvVAR1 value)}
updateEnvEnvVAR2 :: BTreeEnvironment -> String -> BTreeEnvironment
updateEnvEnvVAR2 environment value = environment { envEnvVAR2 = (checkValueEnvEnvVAR2 value)}

-- START OF SET FUNCTIONS FOR ARRAYS

updateEnvEnvVAR1 :: Integer -> BTreeEnvironment -> Bool -> BTreeEnvironment
updateEnvEnvVAR1 0 = updateEnvEnvVAR1Index0
updateEnvEnvVAR1 1 = updateEnvEnvVAR1Index1
updateEnvEnvVAR1 _ = error "EnvEnvVAR1 illegal index value"
arrayUpdateEnvEnvVAR1 :: BTreeEnvironment -> [(Integer, Bool)] -> BTreeEnvironment
arrayUpdateEnvEnvVAR1 environment []  = environment
arrayUpdateEnvEnvVAR1 environment [(index, value)] = updateEnvEnvVAR1 index environment value
arrayUpdateEnvEnvVAR1 environment indicesValues = environment {
  envEnvVAR1Index0 = newEnvVAR1Index0
  , envEnvVAR1Index1 = newEnvVAR1Index1
  }
    where
      (newEnvVAR1Index0, newEnvVAR1Index1) = updateValues indicesValues
      updateValues :: [(Integer, Bool)] -> (Bool, Bool)
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
    newEnvironment = tempEnvironment0


-- START OF INITIAL ENVIRONMENT VALUE

initialEnvironment :: Integer -> BTreeBlackboard -> BTreeEnvironment
initialEnvironment seed blackboard = BTreeEnvironment newSereneGenerator newValEnvVAR1Index0 newValEnvVAR1Index1 newValEnvVAR2 newValEnvFROZENVAR3Index0 newValEnvFROZENVAR3Index1 newValEnvFROZENVAR3Index2 newValEnvFROZENVAR4Index0 newValEnvFROZENVAR4Index1 newValEnvFROZENVAR4Index2  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen9
    partialEnvironmentEnvVAR1Index0 = BTreeEnvironment newSereneGenerator True True " " " " " " " " 0 0 0
    initValEnvVAR1Index0 :: StdGen -> (Bool, StdGen)
    initValEnvVAR1Index0 curGen
      | ((True || False) == (False == True)) = ((sereneXOR ((boardBlVAR0 blackboard) == (-44)) (False == True)), curGen)
      | ((boardBlVAR0 blackboard) /= 24) = (((63 <= 60) == True), curGen)
      | otherwise = ((sereneXOR False (True /= (True && True))), curGen)
      where
        environment = partialEnvironmentEnvVAR1Index0

    (newValEnvVAR1Index0, tempGen1) = initValEnvVAR1Index0 tempGen0

    partialEnvironmentEnvVAR1Index1 = BTreeEnvironment newSereneGenerator newValEnvVAR1Index0 True " " " " " " " " 0 0 0
    initValEnvVAR1Index1 :: StdGen -> (Bool, StdGen)
    initValEnvVAR1Index1 curGen = (((-94) >= (-17)), curGen)
      where
        environment = partialEnvironmentEnvVAR1Index1

    (newValEnvVAR1Index1, tempGen2) = initValEnvVAR1Index1 tempGen1

    partialEnvironmentEnvVAR2 = BTreeEnvironment newSereneGenerator newValEnvVAR1Index0 newValEnvVAR1Index1 " " " " " " " " 0 0 0
    initValEnvVAR2 :: StdGen -> (String, StdGen)
    initValEnvVAR2 curGen = ("no", curGen)
      where
        environment = partialEnvironmentEnvVAR2

    (newValEnvVAR2, tempGen3) = initValEnvVAR2 tempGen2

    partialEnvironmentEnvFROZENVAR3Index0 = BTreeEnvironment newSereneGenerator newValEnvVAR1Index0 newValEnvVAR1Index1 newValEnvVAR2 " " " " " " 0 0 0
    initValEnvFROZENVAR3Index0 :: StdGen -> (String, StdGen)
    initValEnvFROZENVAR3Index0 curGen
      | (sereneXNOR False True) = (newValEnvVAR2, curGen)
      | otherwise = ("no", curGen)
      where
        environment = partialEnvironmentEnvFROZENVAR3Index0

    (newValEnvFROZENVAR3Index0, tempGen4) = initValEnvFROZENVAR3Index0 tempGen3

    partialEnvironmentEnvFROZENVAR3Index1 = BTreeEnvironment newSereneGenerator newValEnvVAR1Index0 newValEnvVAR1Index1 newValEnvVAR2 newValEnvFROZENVAR3Index0 " " " " 0 0 0
    initValEnvFROZENVAR3Index1 :: StdGen -> (String, StdGen)
    initValEnvFROZENVAR3Index1 curGen = (newValEnvVAR2, curGen)
      where
        environment = partialEnvironmentEnvFROZENVAR3Index1

    (newValEnvFROZENVAR3Index1, tempGen5) = initValEnvFROZENVAR3Index1 tempGen4

    partialEnvironmentEnvFROZENVAR3Index2 = BTreeEnvironment newSereneGenerator newValEnvVAR1Index0 newValEnvVAR1Index1 newValEnvVAR2 newValEnvFROZENVAR3Index0 newValEnvFROZENVAR3Index1 " " 0 0 0
    initValEnvFROZENVAR3Index2 :: StdGen -> (String, StdGen)
    initValEnvFROZENVAR3Index2 curGen
      | True = ("both", curGen)
      | (False && False) = ("no", curGen)
      | otherwise = ("no", curGen)
      where
        environment = partialEnvironmentEnvFROZENVAR3Index2

    (newValEnvFROZENVAR3Index2, tempGen6) = initValEnvFROZENVAR3Index2 tempGen5

    partialEnvironmentEnvFROZENVAR4Index0 = BTreeEnvironment newSereneGenerator newValEnvVAR1Index0 newValEnvVAR1Index1 newValEnvVAR2 newValEnvFROZENVAR3Index0 newValEnvFROZENVAR3Index1 newValEnvFROZENVAR3Index2 0 0 0
    initValEnvFROZENVAR4Index0 :: StdGen -> (Integer, StdGen)
    initValEnvFROZENVAR4Index0 curGen
      | ((- (boardBlVAR0 blackboard)) > (boardBlVAR0 blackboard)) = ((min (-2) (max (-5) (abs (boardBlVAR0 blackboard)))), curGen)
      | otherwise = ((min (-2) (max (-5) (min (boardBlVAR0 blackboard) (boardBlVAR0 blackboard)))), curGen)
      where
        environment = partialEnvironmentEnvFROZENVAR4Index0

    (newValEnvFROZENVAR4Index0, tempGen7) = initValEnvFROZENVAR4Index0 tempGen6

    partialEnvironmentEnvFROZENVAR4Index1 = BTreeEnvironment newSereneGenerator newValEnvVAR1Index0 newValEnvVAR1Index1 newValEnvVAR2 newValEnvFROZENVAR3Index0 newValEnvFROZENVAR3Index1 newValEnvFROZENVAR3Index2 newValEnvFROZENVAR4Index0 0 0
    initValEnvFROZENVAR4Index1 :: StdGen -> (Integer, StdGen)
    initValEnvFROZENVAR4Index1 curGen
      | ((- (boardBlVAR0 blackboard)) > (boardBlVAR0 blackboard)) = ((min (-2) (max (-5) (abs (boardBlVAR0 blackboard)))), curGen)
      | otherwise = ((min (-2) (max (-5) (min (boardBlVAR0 blackboard) (boardBlVAR0 blackboard)))), curGen)
      where
        environment = partialEnvironmentEnvFROZENVAR4Index1

    (newValEnvFROZENVAR4Index1, tempGen8) = initValEnvFROZENVAR4Index1 tempGen7

    partialEnvironmentEnvFROZENVAR4Index2 = BTreeEnvironment newSereneGenerator newValEnvVAR1Index0 newValEnvVAR1Index1 newValEnvVAR2 newValEnvFROZENVAR3Index0 newValEnvFROZENVAR3Index1 newValEnvFROZENVAR3Index2 newValEnvFROZENVAR4Index0 newValEnvFROZENVAR4Index1 0
    initValEnvFROZENVAR4Index2 :: StdGen -> (Integer, StdGen)
    initValEnvFROZENVAR4Index2 curGen
      | ((- (boardBlVAR0 blackboard)) > (boardBlVAR0 blackboard)) = ((min (-2) (max (-5) (abs (boardBlVAR0 blackboard)))), curGen)
      | otherwise = ((min (-2) (max (-5) (min (boardBlVAR0 blackboard) (boardBlVAR0 blackboard)))), curGen)
      where
        environment = partialEnvironmentEnvFROZENVAR4Index2

    (newValEnvFROZENVAR4Index2, tempGen9) = initValEnvFROZENVAR4Index2 tempGen8


