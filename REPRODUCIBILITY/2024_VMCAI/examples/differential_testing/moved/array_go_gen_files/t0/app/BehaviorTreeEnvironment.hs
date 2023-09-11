module BehaviorTreeEnvironment where
import SereneRandomizer
import System.Random
import SereneOperations
import BehaviorTreeBlackboard

data BTreeEnvironment = BTreeEnvironment {
  sereneEnvGenerator :: StdGen
  , envEnvVAR1Index0 :: Bool
  , envEnvVAR1Index1 :: Bool
  , envEnvVAR1Index2 :: Bool
  , envEnvFROZENVAR3Index0 :: String
  , envEnvFROZENVAR3Index1 :: String
  , envEnvFROZENVAR3Index2 :: String
  }

fromBTreeEnvironmentToString :: BTreeBlackboard -> BTreeEnvironment -> String
fromBTreeEnvironmentToString blackboard environment = "Env = {" ++ "envEnvVAR1: " ++ "[" ++ show (envEnvVAR1 0 environment) ++ ", " ++ show (envEnvVAR1 1 environment) ++ ", " ++ show (envEnvVAR1 2 environment)++ "]" ++ ", " ++ "envEnvFROZENVAR3: " ++ "[" ++ show (envEnvFROZENVAR3 0 environment) ++ ", " ++ show (envEnvFROZENVAR3 1 environment) ++ ", " ++ show (envEnvFROZENVAR3 2 environment)++ "]" ++ ", " ++ "envEnvDEFINE5: " ++ "[" ++ show (envEnvDEFINE5 0 blackboard environment) ++ ", " ++ show (envEnvDEFINE5 1 blackboard environment) ++ ", " ++ show (envEnvDEFINE5 2 blackboard environment)++ "]" ++ ", " ++ "envEnvDEFINE6: " ++ show (envEnvDEFINE6 blackboard environment) ++ ", " ++ "envEnvDEFINE7: " ++ show (envEnvDEFINE7 blackboard environment) ++ "}"

-- START OF ENVIRONMENT FUNCTIONS

envEnvDEFINE6 :: BTreeBlackboard -> BTreeEnvironment -> Bool
envEnvDEFINE6 blackboard environment
  | (sereneXNOR (envEnvVAR1 2 environment) False) = (sereneXOR (sereneIMPLIES (envEnvVAR1 0 environment) False) (sereneXNOR (sereneXOR (envEnvVAR1 2 environment) (envEnvVAR1 0 environment)) True))
  | otherwise = ((boardBlVAR0 0 blackboard) <= 70)
envEnvDEFINE7 :: BTreeBlackboard -> BTreeEnvironment -> Bool
envEnvDEFINE7 blackboard environment
  | (False && (sereneIMPLIES (False == True) (envEnvDEFINE6 blackboard environment))) = (envEnvVAR1 1 environment)
  | otherwise = (envEnvDEFINE6 blackboard environment)
envEnvDEFINE5 :: Integer -> BTreeBlackboard -> BTreeEnvironment -> Integer
envEnvDEFINE5 0 blackboard environment
  | ((True || (envEnvVAR1 0 environment)) || True) = (min (-2) (max (-5) ((sereneCOUNT (sereneXNOR (True /= (envEnvVAR1 1 environment)) ("yes" /= "yes")) (False == ((boardBlVAR0 0 blackboard) < (boardBlVAR0 0 blackboard)))) + (sereneCOUNT ((- (-90)) >= (boardBlVAR0 0 blackboard)) ((envEnvFROZENVAR3 0 environment) == "no")))))
  | otherwise = (min (-2) (max (-5) ((boardBlVAR0 1 blackboard) - (boardBlVAR0 1 blackboard))))
envEnvDEFINE5 1 blackboard environment
  | (sereneXOR (envEnvVAR1 1 environment) ("yes" /= "no")) = (min (-2) (max (-5) (boardBlVAR0 0 blackboard)))
  | (sereneXNOR (envEnvVAR1 0 environment) (envEnvVAR1 1 environment)) = (min (-2) (max (-5) (abs (min 79 (-91)))))
  | otherwise = (min (-2) (max (-5) (max 37 (boardBlVAR0 0 blackboard))))
envEnvDEFINE5 2 blackboard environment = (min (-2) (max (-5) (- (min 25 (boardBlVAR0 1 blackboard)))))
envEnvDEFINE5 _ _ _ = error "envEnvDEFINE5 illegal index value"

-- START OF GET FUNCTIONS FOR ARRAYS

envEnvVAR1 :: Integer -> BTreeEnvironment -> Bool
envEnvVAR1 0 = envEnvVAR1Index0
envEnvVAR1 1 = envEnvVAR1Index1
envEnvVAR1 2 = envEnvVAR1Index2
envEnvVAR1 _ = error "envEnvVAR1 illegal index value"
envEnvFROZENVAR3 :: Integer -> BTreeEnvironment -> String
envEnvFROZENVAR3 0 = envEnvFROZENVAR3Index0
envEnvFROZENVAR3 1 = envEnvFROZENVAR3Index1
envEnvFROZENVAR3 2 = envEnvFROZENVAR3Index2
envEnvFROZENVAR3 _ = error "envEnvFROZENVAR3 illegal index value"

-- START OF TYPE CHECKING FUNCTIONS

checkValueEnvEnvVAR1 :: Bool -> Bool
checkValueEnvEnvVAR1 value = value


-- START OF SET FUNCTIONS

updateEnvGenerator :: BTreeEnvironment -> StdGen -> BTreeEnvironment
updateEnvGenerator environment newGen = environment { sereneEnvGenerator = newGen }
updateEnvEnvVAR1Index0 :: BTreeEnvironment -> Bool -> BTreeEnvironment
updateEnvEnvVAR1Index0 environment value = environment { envEnvVAR1Index0 = (checkValueEnvEnvVAR1 value)}
updateEnvEnvVAR1Index1 :: BTreeEnvironment -> Bool -> BTreeEnvironment
updateEnvEnvVAR1Index1 environment value = environment { envEnvVAR1Index1 = (checkValueEnvEnvVAR1 value)}
updateEnvEnvVAR1Index2 :: BTreeEnvironment -> Bool -> BTreeEnvironment
updateEnvEnvVAR1Index2 environment value = environment { envEnvVAR1Index2 = (checkValueEnvEnvVAR1 value)}

-- START OF SET FUNCTIONS FOR ARRAYS

updateEnvEnvVAR1 :: Integer -> BTreeEnvironment -> Bool -> BTreeEnvironment
updateEnvEnvVAR1 0 = updateEnvEnvVAR1Index0
updateEnvEnvVAR1 1 = updateEnvEnvVAR1Index1
updateEnvEnvVAR1 2 = updateEnvEnvVAR1Index2
updateEnvEnvVAR1 _ = error "EnvEnvVAR1 illegal index value"
arrayUpdateEnvEnvVAR1 :: BTreeEnvironment -> [(Integer, Bool)] -> BTreeEnvironment
arrayUpdateEnvEnvVAR1 environment []  = environment
arrayUpdateEnvEnvVAR1 environment [(index, value)] = updateEnvEnvVAR1 index environment value
arrayUpdateEnvEnvVAR1 environment indicesValues = environment {
  envEnvVAR1Index0 = newEnvVAR1Index0
  , envEnvVAR1Index1 = newEnvVAR1Index1
  , envEnvVAR1Index2 = newEnvVAR1Index2
  }
    where
      (newEnvVAR1Index0, newEnvVAR1Index1, newEnvVAR1Index2) = updateValues indicesValues
      updateValues :: [(Integer, Bool)] -> (Bool, Bool, Bool)
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
    newEnvironment = tempEnvironment0


-- START OF INITIAL ENVIRONMENT VALUE

initialEnvironment :: Integer -> BTreeBlackboard -> BTreeEnvironment
initialEnvironment seed blackboard = BTreeEnvironment newSereneGenerator newValEnvVAR1Index0 newValEnvVAR1Index1 newValEnvVAR1Index2 newValEnvFROZENVAR3Index0 newValEnvFROZENVAR3Index1 newValEnvFROZENVAR3Index2  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen6
    partialEnvironmentEnvVAR1Index0 = BTreeEnvironment newSereneGenerator True True True " " " " " "
    initValEnvVAR1Index0 :: StdGen -> (Bool, StdGen)
    initValEnvVAR1Index0 curGen
      | (((boardBlVAR0 0 blackboard) * ((boardBlVAR0 1 blackboard) * ((boardBlVAR0 0 blackboard) * (boardBlVAR0 1 blackboard)))) > (39 + ((-62) + (boardBlVAR0 1 blackboard)))) = (False, curGen)
      | otherwise = (False, curGen)
      where
        environment = partialEnvironmentEnvVAR1Index0

    (newValEnvVAR1Index0, tempGen1) = initValEnvVAR1Index0 tempGen0

    partialEnvironmentEnvVAR1Index1 = BTreeEnvironment newSereneGenerator newValEnvVAR1Index0 True True " " " " " "
    initValEnvVAR1Index1 :: StdGen -> (Bool, StdGen)
    initValEnvVAR1Index1 curGen
      | (((boardBlVAR0 0 blackboard) * ((boardBlVAR0 1 blackboard) * ((boardBlVAR0 0 blackboard) * (boardBlVAR0 1 blackboard)))) > (39 + ((-62) + (boardBlVAR0 1 blackboard)))) = (False, curGen)
      | otherwise = (False, curGen)
      where
        environment = partialEnvironmentEnvVAR1Index1

    (newValEnvVAR1Index1, tempGen2) = initValEnvVAR1Index1 tempGen1

    partialEnvironmentEnvVAR1Index2 = BTreeEnvironment newSereneGenerator newValEnvVAR1Index0 newValEnvVAR1Index1 True " " " " " "
    initValEnvVAR1Index2 :: StdGen -> (Bool, StdGen)
    initValEnvVAR1Index2 curGen
      | (((boardBlVAR0 0 blackboard) * ((boardBlVAR0 1 blackboard) * ((boardBlVAR0 0 blackboard) * (boardBlVAR0 1 blackboard)))) > (39 + ((-62) + (boardBlVAR0 1 blackboard)))) = (False, curGen)
      | otherwise = (False, curGen)
      where
        environment = partialEnvironmentEnvVAR1Index2

    (newValEnvVAR1Index2, tempGen3) = initValEnvVAR1Index2 tempGen2

    partialEnvironmentEnvFROZENVAR3Index0 = BTreeEnvironment newSereneGenerator newValEnvVAR1Index0 newValEnvVAR1Index1 newValEnvVAR1Index2 " " " " " "
    initValEnvFROZENVAR3Index0 :: StdGen -> (String, StdGen)
    initValEnvFROZENVAR3Index0 curGen = ("both", curGen)
      where
        environment = partialEnvironmentEnvFROZENVAR3Index0

    (newValEnvFROZENVAR3Index0, tempGen4) = initValEnvFROZENVAR3Index0 tempGen3

    partialEnvironmentEnvFROZENVAR3Index1 = BTreeEnvironment newSereneGenerator newValEnvVAR1Index0 newValEnvVAR1Index1 newValEnvVAR1Index2 newValEnvFROZENVAR3Index0 " " " "
    initValEnvFROZENVAR3Index1 :: StdGen -> (String, StdGen)
    initValEnvFROZENVAR3Index1 curGen
      | True = ("both", curGen)
      | ((boardBlVAR0 0 blackboard) >= ((boardBlVAR0 0 blackboard) + ((boardBlVAR0 1 blackboard) + ((-88) + (boardBlVAR0 0 blackboard))))) = ("yes", curGen)
      | otherwise = ("both", curGen)
      where
        environment = partialEnvironmentEnvFROZENVAR3Index1

    (newValEnvFROZENVAR3Index1, tempGen5) = initValEnvFROZENVAR3Index1 tempGen4

    partialEnvironmentEnvFROZENVAR3Index2 = BTreeEnvironment newSereneGenerator newValEnvVAR1Index0 newValEnvVAR1Index1 newValEnvVAR1Index2 newValEnvFROZENVAR3Index0 newValEnvFROZENVAR3Index1 " "
    initValEnvFROZENVAR3Index2 :: StdGen -> (String, StdGen)
    initValEnvFROZENVAR3Index2 curGen
      | True = ("no", curGen)
      | otherwise = ("yes", curGen)
      where
        environment = partialEnvironmentEnvFROZENVAR3Index2

    (newValEnvFROZENVAR3Index2, tempGen6) = initValEnvFROZENVAR3Index2 tempGen5


