module Behavior_tree_environment where
data Environment = Environment {
  x :: Int
  , y :: Int  } deriving (Show)

update_env_x :: Environment -> Int -> Environment
update_env_x environment value
  | 0 > value || value > 10 = error "x illegal value"
  | otherwise = environment { x = value }

update_env_y :: Environment -> Int -> Environment
update_env_y environment value
  | 0 > value || value > 10 = error "y illegal value"
  | otherwise = environment { y = value }

check_termination :: Environment -> Bool
check_termination environment = True

evaluateCodes :: Environment -> [Environment -> Environment] -> Environment
evaluateCodes environment codes
  | null codes = environment
  | otherwise = evaluateCodes ((head codes) environment) (tail codes)


initialEnvironment = Environment 0 10
