module Action1_file where
import Behavior_tree_core
import Behavior_tree_blackboard
import Behavior_tree_environment


action1 :: [BTreeNode] -> TreeLocation -> BTreeNodeStatus -> [BTreeStatusTree] -> BTreeNodeStatus -> [BTreeStatusTree] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
action1 nodeChildren nodeLocation memoryStatus memoryStorage partialStatus partialMemoryStorage blackboard environment futureChanges = (returnStatus, [], [], newBlackboard, newEnvironment, newFutureChanges)
  where
    envUpdate0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    envUpdate0 boardEnv = (updateBoardX blackboard (min 10 ((boardX blackboard) + 5)), environment)
      where
        blackboard = fst boardEnv
        environment = snd boardEnv
    returnStatement :: (BTreeBlackboard, BTreeEnvironment) -> BTreeNodeStatus
    returnStatement boardEnv = Success
      where
        blackboard = fst boardEnv
        environment = snd boardEnv
    envUpdate1 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    envUpdate1 boardEnv = (updateBoardY blackboard (max 0 ((boardY blackboard) - 1)), environment)
      where
        blackboard = fst boardEnv
        environment = snd boardEnv
    preStatusBoardEnv = envUpdate0 (blackboard, environment)
    returnStatus = returnStatement preStatusBoardEnv
    postStatusBoardEnv = envUpdate1 preStatusBoardEnv
    newBlackboard = fst postStatusBoardEnv
    newEnvironment = snd postStatusBoardEnv
    newFutureChanges = futureChanges
