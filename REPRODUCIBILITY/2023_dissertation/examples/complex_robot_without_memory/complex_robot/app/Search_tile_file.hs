module Search_tile_file where
import Behavior_tree_core
import Behavior_tree_blackboard
import Behavior_tree_environment
import SereneRandomizer



search_tile :: [BTreeNode] -> TreeLocation -> BTreeNodeStatus -> [BTreeStatusTree] -> BTreeNodeStatus -> [BTreeStatusTree] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
search_tile nodeChildren nodeLocation memoryStatus memoryStorage partialStatus partialMemoryStorage blackboard environment futureChanges = (returnStatus, [], [], newBlackboard, newEnvironment, newFutureChanges)
  where
    boardEnvUpdate0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    boardEnvUpdate0 boardEnv
      | True = privateBoardEnv
      | otherwise = boardEnv
      where
        privateBoardEnv
          | ((envTile_progress environment) == 2) = (localUpdateBoardTile_searched nodeLocation blackboard True, environment)
          | otherwise = (updateBoardGenerator (localUpdateBoardTile_searched nodeLocation blackboard (privateRandom0 (fst (getRandomInt (sereneBoardGenerator blackboard) 1)))) (snd (getRandomInt (sereneBoardGenerator blackboard) 1)), environment)
          where
            (blackboard, environment) = boardEnv
            privateRandom0 :: Int -> Bool
            privateRandom0 0 = True
            privateRandom0 _ = False
    boardEnvUpdate1 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    boardEnvUpdate1 boardEnv
      | True = privateBoardEnv
      | otherwise = boardEnv
      where
        privateBoardEnv
          | (boardHave_flag blackboard) = (updateBoardHave_flag blackboard True, environment)
          | otherwise = (updateBoardHave_flag blackboard ((localBoardTile_searched nodeLocation blackboard) && ((envX environment) == (envFlag_x environment)) && ((envY environment) == (envFlag_y environment))), environment)
          where
            (blackboard, environment) = boardEnv
    returnStatement :: (BTreeBlackboard, BTreeEnvironment) -> BTreeNodeStatus
    returnStatement boardEnv
      | ((localBoardTile_searched nodeLocation blackboard) && (boardHave_flag blackboard)) = Success
      | (localBoardTile_searched nodeLocation blackboard) = Failure
      | otherwise = Running
      where
        (blackboard, environment) = boardEnv
    futureChanges0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    futureChanges0 boardEnv
      | (localBoardTile_searched nodeLocation blackboard) = (blackboard, updateEnvTile_progress environment 2)
      | otherwise = (blackboard, updateEnvTile_progress environment (min 2 (1 + (envTile_progress environment))))
      where
        (blackboard, environment) = boardEnv
    preStatusBoardEnv = boardEnvUpdate1 . boardEnvUpdate0 $ (blackboard, environment)
    returnStatus = returnStatement preStatusBoardEnv
    (newBlackboard, newEnvironment) =  preStatusBoardEnv
    newFutureChanges = futureChanges0 : futureChanges
