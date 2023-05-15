module Behavior_tree_environment where
import SereneRandomizer
import System.Random
import Behavior_tree_blackboard

data BTreeEnvironment = BTreeEnvironment {
  sereneEnvGenerator :: StdGen
  }

instance Show BTreeEnvironment where
  show (BTreeEnvironment _ ) = "Env = {" ++ "}"
updateEnvGenerator :: BTreeEnvironment -> StdGen -> BTreeEnvironment
updateEnvGenerator environment newGen = environment { sereneEnvGenerator = newGen }
checkTickConditionTermination :: BTreeBlackboard -> BTreeEnvironment -> Bool
checkTickConditionTermination blackboard environment = True

applyFutureChanges :: BTreeEnvironment -> [BTreeEnvironment -> BTreeEnvironment] -> BTreeEnvironment
applyFutureChanges environment futureChanges
  | null futureChanges = environment
  | otherwise = applyFutureChanges (head futureChanges environment) (tail futureChanges)


betweenTickUpdate :: BTreeEnvironment -> BTreeEnvironment
betweenTickUpdate environment = environment


initialEnvironment :: Int -> BTreeBlackboard -> BTreeEnvironment
initialEnvironment seed blackboard = BTreeEnvironment newSereneGenerator 
  where
    tempGen0 = getGenerator seed
    newSereneGenerator = tempGen0

