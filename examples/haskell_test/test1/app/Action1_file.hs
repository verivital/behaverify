module Action1_file where
import Behavior_tree_core
import Behavior_tree_blackboard
import Behavior_tree_environment
import SereneRandomizer



action1 :: [BTreeNode] -> TreeLocation -> BTreeNodeStatus -> [BTreeStatusTree] -> BTreeNodeStatus -> [BTreeStatusTree] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
action1 nodeChildren nodeLocation memoryStatus memoryStorage partialStatus partialMemoryStorage blackboard environment futureChanges = (returnStatus, [], [], newBlackboard, newEnvironment, newFutureChanges)
  where
    envUpdate0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    envUpdate0 boardEnv
      | ((boardX blackboard) == 5) = (updateBoardGenerator (updateBoardX blackboard (localRandom0 (fst (getRandomInt (sereneBoardGenerator blackboard) 1)))) (snd (getRandomInt (sereneBoardGenerator blackboard) 1)), environment)
      | ((boardX blackboard) == 6) = (updateBoardGenerator (updateBoardX blackboard (localRandom1 (fst (getRandomInt (sereneBoardGenerator blackboard) 1)))) (snd (getRandomInt (sereneBoardGenerator blackboard) 1)), environment)
      | otherwise = (updateBoardX blackboard (min 10 ((boardX blackboard) + 3)), environment)
      where
        (blackboard, environment) = boardEnv
        localRandom0 :: Int -> Int
        localRandom0 0 = ((boardX blackboard) - 2)
        localRandom0 _ = ((boardX blackboard) + 2)
        localRandom1 :: Int -> Int
        localRandom1 0 = ((boardX blackboard) - 1)
        localRandom1 _ = ((boardX blackboard) + 1)
    returnStatement :: (BTreeBlackboard, BTreeEnvironment) -> BTreeNodeStatus
    returnStatement boardEnv = Success
      where
        (blackboard, environment) = boardEnv
    envUpdate1 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    envUpdate1 boardEnv = (updateBoardY blackboard (max 0 ((boardY blackboard) - 1)), environment)
      where
        (blackboard, environment) = boardEnv
    preStatusBoardEnv = envUpdate0 (blackboard, environment)
    returnStatus = returnStatement preStatusBoardEnv
    (newBlackboard, newEnvironment) = envUpdate1 preStatusBoardEnv
    newFutureChanges = futureChanges
