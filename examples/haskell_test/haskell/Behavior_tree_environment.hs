module Behavior_tree_environment where
import Behavior_tree_blackboard
data BTreeEnvironment = BTreeEnvironment {
    } deriving (Show)

checkTickConditionTermination :: BTreeBlackboard -> BTreeEnvironment -> Bool
checkTickConditionTermination blackboard environment = True

applyFutureChanges :: BTreeEnvironment -> [BTreeEnvironment -> BTreeEnvironment] -> BTreeEnvironment
applyFutureChanges environment futureChanges
  | null futureChanges = environment
  | otherwise = applyFutureChanges (head futureChanges environment) (tail futureChanges)


betweenTickUpdate :: BTreeEnvironment -> BTreeEnvironment
betweenTickUpdate environment = environment


initialEnvironment = BTreeEnvironment 
