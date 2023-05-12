module Action2_file where
import Behavior_tree_core
import Behavior_tree_blackboard
import Behavior_tree_environment


action2 :: [BTreeNode] -> TreeLocation -> BTreeNodeStatus -> [BTreeStatusTree] -> BTreeNodeStatus -> [BTreeStatusTree] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
action2 nodeChildren nodeLocation memoryStatus memoryStorage partialStatus partialMemoryStorage blackboard environment futureChanges = (returnStatus, [], [], newBlackboard, newEnvironment, newFutureChanges)
  where
    envUpdate0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    envUpdate0 boardEnv = (updateBoardX blackboard (min 10 ((boardX blackboard) * 2)), environment)
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
    envUpdate2 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    envUpdate2 boardEnv = (updateBoardX blackboard (max 0 ((boardX blackboard) - 1)), environment)
      where
        blackboard = fst boardEnv
        environment = snd boardEnv
    preStatusBoardEnv = envUpdate0 (blackboard, environment)
    returnStatus = returnStatement preStatusBoardEnv
    postStatusBoardEnv = envUpdate2 . envUpdate1 $ preStatusBoardEnv
    newBlackboard = fst postStatusBoardEnv
    newEnvironment = snd postStatusBoardEnv
    newFutureChanges = futureChanges
