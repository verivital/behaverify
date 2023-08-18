module BehaviorTreeEnvironment where
import SereneRandomizer
import System.Random
import BehaviorTreeBlackboard
import SereneOperations

data BTreeEnvironment = BTreeEnvironment {
  sereneEnvGenerator :: StdGen
  }

instance Show BTreeEnvironment where
  show (BTreeEnvironment _ ) = "Env = {" ++ "}"




updateEnvGenerator :: BTreeEnvironment -> StdGen -> BTreeEnvironment
updateEnvGenerator environment newGen = environment { sereneEnvGenerator = newGen }
checkTickConditionTermination :: BTreeBlackboard -> BTreeEnvironment -> Bool
checkTickConditionTermination blackboard environment = True

modifiedID :: BTreeBlackboard -> BTreeEnvironment -> BTreeEnvironment
modifiedID _ environment = environment
applyFutureChanges :: [(BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)] -> (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
applyFutureChanges [] = id
applyFutureChanges futureChanges = head futureChanges . applyFutureChanges (tail futureChanges)


betweenTickUpdate :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
betweenTickUpdate (blackboard, curEnvironment) = (blackboard, newEnvironment)
  where
    tempEnvironment0 = curEnvironment
    newEnvironment = tempEnvironment0



initialEnvironment :: Int -> BTreeBlackboard -> BTreeEnvironment
initialEnvironment seed blackboard = BTreeEnvironment newSereneGenerator 
  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen0

