module Go_forward_file where
import Behavior_tree_core
import Behavior_tree_blackboard
import Behavior_tree_environment
import SereneRandomizer



go_forward :: [BTreeNode] -> TreeLocation -> BTreeNodeStatus -> [BTreeStatusTree] -> BTreeNodeStatus -> [BTreeStatusTree] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
go_forward nodeChildren nodeLocation memoryStatus memoryStorage partialStatus partialMemoryStorage blackboard environment futureChanges = (returnStatus, [], [], newBlackboard, newEnvironment, newFutureChanges)
  where
    returnStatement :: (BTreeBlackboard, BTreeEnvironment) -> BTreeNodeStatus
    returnStatement boardEnv = Running
      where
        (blackboard, environment) = boardEnv
    futureChanges0 :: BTreeBlackboard -> BTreeEnvironment -> (BTreeBlackboard, BTreeEnvironment)
    futureChanges0 boardEnv
      | ((((boardForward blackboard) + (envX environment)) >= 0) && (((boardForward blackboard) + (envX environment)) <= 18) && (|| ((envActive_hole blackboard environment) == -1) ((envActive_hole blackboard environment) == (envY environment)))) = (blackboard, updateEnvX environment ((envX environment) + (boardForward blackboard)))
      | otherwise = (blackboard, updateEnvX environment (envX environment))
      where
        (blackboard, environment) = boardEnv
    preStatusBoardEnv =  (blackboard, environment)
    returnStatus = returnStatement preStatusBoardEnv
    (newBlackboard, newEnvironment) =  preStatusBoardEnv
    newFutureChanges = futureChanges : futureChanges0
