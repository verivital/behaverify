module BehaviorTreeEnvironment where
import SereneRandomizer
import System.Random
import SereneOperations
import BehaviorTreeBlackboard

data BTreeEnvironment = BTreeEnvironment {
  sereneEnvGenerator :: StdGen
  , envEnvVAR1 :: Bool
  , envEnvVAR2 :: Bool
  , envEnvFROZENVAR3 :: Bool
  }

fromBTreeEnvironmentToString :: BTreeBlackboard -> BTreeEnvironment -> String
fromBTreeEnvironmentToString blackboard environment = "Env = {" ++ "envEnvVAR1: " ++ show (envEnvVAR1 environment) ++ ", " ++ "envEnvVAR2: " ++ show (envEnvVAR2 environment) ++ ", " ++ "envEnvFROZENVAR3: " ++ show (envEnvFROZENVAR3 environment) ++ ", " ++ "envEnvDEFINE6: " ++ "[" ++ show (envEnvDEFINE6 0 blackboard environment) ++ ", " ++ show (envEnvDEFINE6 1 blackboard environment) ++ ", " ++ show (envEnvDEFINE6 2 blackboard environment)++ "]" ++ "}"

-- START OF ENVIRONMENT FUNCTIONS

envEnvDEFINE6 :: Integer -> BTreeBlackboard -> BTreeEnvironment -> Integer
envEnvDEFINE6 0 blackboard environment = (min 5 (max 2 (boardBlVAR0 2 blackboard)))
envEnvDEFINE6 1 blackboard environment = (min 5 (max 2 (boardBlVAR0 2 blackboard)))
envEnvDEFINE6 2 blackboard environment = (min 5 (max 2 (boardBlVAR0 2 blackboard)))
envEnvDEFINE6 _ _ _ = error "envEnvDEFINE6 illegal index value"

-- START OF GET FUNCTIONS FOR ARRAYS


-- START OF TYPE CHECKING FUNCTIONS

checkValueEnvEnvVAR1 :: Bool -> Bool
checkValueEnvEnvVAR1 value = value

checkValueEnvEnvVAR2 :: Bool -> Bool
checkValueEnvEnvVAR2 value = value


-- START OF SET FUNCTIONS

updateEnvGenerator :: BTreeEnvironment -> StdGen -> BTreeEnvironment
updateEnvGenerator environment newGen = environment { sereneEnvGenerator = newGen }
updateEnvEnvVAR1 :: BTreeEnvironment -> Bool -> BTreeEnvironment
updateEnvEnvVAR1 environment value = environment { envEnvVAR1 = (checkValueEnvEnvVAR1 value)}
updateEnvEnvVAR2 :: BTreeEnvironment -> Bool -> BTreeEnvironment
updateEnvEnvVAR2 environment value = environment { envEnvVAR2 = (checkValueEnvEnvVAR2 value)}

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
    newEnvironment = tempEnvironment0


-- START OF INITIAL ENVIRONMENT VALUE

initialEnvironment :: Integer -> BTreeBlackboard -> BTreeEnvironment
initialEnvironment seed blackboard = BTreeEnvironment newSereneGenerator newValEnvVAR1 newValEnvVAR2 newValEnvFROZENVAR3  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen3
    partialEnvironmentEnvVAR1 = BTreeEnvironment newSereneGenerator True True True
    initValEnvVAR1 :: StdGen -> (Bool, StdGen)
    initValEnvVAR1 curGen
      | False = (((boardBlVAR0 0 blackboard) == (min (-77) (boardBlVAR0 0 blackboard))), curGen)
      | otherwise = ((sereneXOR ((boardBlVAR0 1 blackboard) < (-4)) (sereneXNOR False True)), curGen)
      where
        environment = partialEnvironmentEnvVAR1

    (newValEnvVAR1, tempGen1) = initValEnvVAR1 tempGen0

    partialEnvironmentEnvVAR2 = BTreeEnvironment newSereneGenerator newValEnvVAR1 True True
    initValEnvVAR2 :: StdGen -> (Bool, StdGen)
    initValEnvVAR2 curGen = (((boardBlVAR0 0 blackboard) < ((boardBlVAR0 1 blackboard) - (boardBlVAR0 2 blackboard))), curGen)
      where
        environment = partialEnvironmentEnvVAR2

    (newValEnvVAR2, tempGen2) = initValEnvVAR2 tempGen1

    partialEnvironmentEnvFROZENVAR3 = BTreeEnvironment newSereneGenerator newValEnvVAR1 newValEnvVAR2 True
    initValEnvFROZENVAR3 :: StdGen -> (Bool, StdGen)
    initValEnvFROZENVAR3 curGen = ((newValEnvVAR2 && True), curGen)
      where
        environment = partialEnvironmentEnvFROZENVAR3

    (newValEnvFROZENVAR3, tempGen3) = initValEnvFROZENVAR3 tempGen2


