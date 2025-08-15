module BehaviorTreeEnvironment where
import BehaviorTreeBlackboard

data BTreeEnvironment = BTreeEnvironment {
  env_x :: Int
  , env_y :: Int  } deriving (Show)

update_env_x :: BTreeEnvironment -> Int -> BTreeEnvironment
update_env_x environment value
  | 0 > value || value > 10 = error "x illegal value"
  | otherwise = environment { env_x = value }

update_env_y :: BTreeEnvironment -> Int -> BTreeEnvironment
update_env_y environment value
  | 0 > value || value > 10 = error "y illegal value"
  | otherwise = environment { env_y = value }

check_termination :: BTreeEnvironment -> Blackboard -> Bool
check_termination environment blackboard = True

evaluateCodes :: BTreeEnvironment -> Blackboard -> [BTreeEnvironment -> BTreeEnvironment] -> BTreeEnvironment
evaluateCodes environment blackboard codes
  | null codes = environment
  | otherwise = evaluateCodes ((head codes) environment) blackboard (tail codes)


initialBTreeEnvironment = BTreeEnvironment 0 10
