module Set_zone_file where
import Behavior_tree_core
import Behavior_tree_blackboard
import Behavior_tree_environment
import SereneRandomizer



set_zone :: [BTreeNode] -> TreeLocation -> BTreeNodeStatus -> [BTreeStatusTree] -> BTreeNodeStatus -> [BTreeStatusTree] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
set_zone nodeChildren nodeLocation memoryStatus memoryStorage partialStatus partialMemoryStorage blackboard environment futureChanges = (returnStatus, [], [], newBlackboard, newEnvironment, newFutureChanges)
  where
    boardEnvUpdate0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    boardEnvUpdate0 boardEnv
      | True = privateBoardEnv
      | otherwise = boardEnv
      where
        privateBoardEnv
          | ((envX environment) <= 3) = (updateBoardZone blackboard "home", environment)
          | ((envX environment) >= 15) = (updateBoardZone blackboard "target", environment)
          | otherwise = (updateBoardZone blackboard "maze", environment)
          where
            (blackboard, environment) = boardEnv
    returnStatement :: (BTreeBlackboard, BTreeEnvironment) -> BTreeNodeStatus
    returnStatement boardEnv = Success
      where
        (blackboard, environment) = boardEnv
    preStatusBoardEnv = boardEnvUpdate0 (blackboard, environment)
    returnStatus = returnStatement preStatusBoardEnv
    (newBlackboard, newEnvironment) =  preStatusBoardEnv
    newFutureChanges = futureChanges
