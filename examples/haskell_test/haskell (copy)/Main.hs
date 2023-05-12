module Main where
import Test1
import Behavior_tree_core
import Behavior_tree_environment
import X_less_than_5_file
import Action1_file
import Action2_file


main :: IO ()
main =
  do {
    print each_env
  }
  where
    max_iteration = 100
    initial_environment = initialEnvironment
    tree_root = root_sel__node
    execution_chain :: Int -> MemoryTree -> MemoryTree -> Environment -> [Environment]
    execution_chain count memory partial environment
      | count >= max_iteration = environment:[]
      | False == (check_termination environment) = environment:[]
      | otherwise = environment : (execution_chain (count + 1) next_memory next_partial next_env)
      where
        (_, codes, temp_env, next_memory, next_partial) = evaluateTree tree_root memory partial environment
        next_env = evaluateCodes temp_env codes
    each_env = execution_chain 0 (allInvalid tree_root) (allInvalid tree_root) initial_environment