module Action1_file where
import Behavior_tree_core
import Behavior_tree_environment


action1 :: [Node] -> NodeStatus -> [MemoryTree] -> NodeStatus -> [MemoryTree] -> Environment -> Codes -> NodeOutput
action1 children memoryStatus memoryTree partialStatus partialTree environment codes = (return_code, new_codes, new_environment, [], [])
  where
    env_update_0 ::  Environment -> Environment
    env_update_0 environment = update_env_x environment (min 10 (x environment + 5))
    return_statement :: Environment -> NodeStatus
    return_statement environment = Success
    env_update_1 ::  Environment -> Environment
    env_update_1 environment = update_env_y environment (max 0 (y environment - 1))
    pre_update_env = env_update_0 $ environment
    return_code = return_statement pre_update_env
    new_environment = env_update_1 $ pre_update_env
    new_codes =  codes
