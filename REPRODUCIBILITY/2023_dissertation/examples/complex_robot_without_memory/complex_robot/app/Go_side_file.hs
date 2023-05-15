module Go_side_file where
import Behavior_tree_core
import Behavior_tree_blackboard
import Behavior_tree_environment
import SereneRandomizer



go_side :: [BTreeNode] -> TreeLocation -> BTreeNodeStatus -> [BTreeStatusTree] -> BTreeNodeStatus -> [BTreeStatusTree] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
go_side nodeChildren nodeLocation memoryStatus memoryStorage partialStatus partialMemoryStorage blackboard environment futureChanges = (returnStatus, [], [], newBlackboard, newEnvironment, newFutureChanges)
  where
    returnStatement :: (BTreeBlackboard, BTreeEnvironment) -> BTreeNodeStatus
    returnStatement boardEnv = Running
      where
        (blackboard, environment) = boardEnv
    futureChanges0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    futureChanges0 boardEnv
      | ((((boardSide blackboard) + (envY environment)) >= 0) && (((boardSide blackboard) + (envY environment)) <= 2)) = (blackboard, updateEnvY environment ((envY environment) + (boardSide blackboard)))
      | otherwise = (blackboard, updateEnvY environment (envY environment))
      where
        (blackboard, environment) = boardEnv
    preStatusBoardEnv =  (blackboard, environment)
    returnStatus = returnStatement preStatusBoardEnv
    (newBlackboard, newEnvironment) =  preStatusBoardEnv
    newFutureChanges = futureChanges0 : futureChanges
