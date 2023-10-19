module BTreeSearchTile where
import BehaviorTreeCore
import BehaviorTreeBlackboard
import BehaviorTreeEnvironment
import SereneRandomizer
import SereneOperations



bTreeFunctionSearchTile :: [BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
bTreeFunctionSearchTile _ nodeLocation _ _ _ _ oldBlackboard oldEnvironment futureChanges = (returnStatus, [], [], newBlackboard, newEnvironment, newFutureChanges)
  where
    boardEnvUpdate0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    boardEnvUpdate0 boardEnv
      | not (True) = boardEnv
      | otherwise = privateBoardEnv
      where
        (conditionBlackboard, conditionEnvironment) = boardEnv
        privateTempBoardEnv0 = boardEnv
        privateBoardEnv = privateTempBoardEnv2
        privateTempBoardEnv1
          | ((envTileProgress environment) == 2) = (updateLocalBoardTileSearched nodeLocation blackboard True, environment)
          | otherwise = (updateBoardGenerator (updateLocalBoardTileSearched nodeLocation blackboard (privateRandom0 (fst (getRandomInteger (sereneBoardGenerator blackboard) 1)))) (snd (getRandomInteger (sereneBoardGenerator blackboard) 1)), environment)
          where
            (blackboard, environment) = privateTempBoardEnv0
            privateRandom0 :: Integer -> Bool
            privateRandom0 0 = True
            privateRandom0 _ = False
        privateTempBoardEnv2
          | (boardHaveFlag blackboard) = (updateBoardHaveFlag blackboard True, environment)
          | otherwise = (updateBoardHaveFlag blackboard ((localBoardTileSearched nodeLocation blackboard) && (((envX environment) == (envFlagX environment)) && ((envY environment) == (envFlagY environment)))), environment)
          where
            (blackboard, environment) = privateTempBoardEnv1
    returnStatement :: (BTreeBlackboard, BTreeEnvironment) -> BTreeNodeStatus
    returnStatement boardEnv
      | ((localBoardTileSearched nodeLocation blackboard) && (boardHaveFlag blackboard)) = Success
      | (localBoardTileSearched nodeLocation blackboard) = Failure
      | otherwise = Running
      where
        (blackboard, environment) = boardEnv
    futureChanges0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    futureChanges0 boardEnv
      | (localBoardTileSearched nodeLocation blackboard) = (blackboard, updateEnvTileProgress environment 2)
      | otherwise = (blackboard, updateEnvTileProgress environment (min 2 (1 + (envTileProgress environment))))
      where
        (blackboard, environment) = boardEnv
    preStatusBoardEnv = boardEnvUpdate0 (oldBlackboard, oldEnvironment)
    returnStatus = returnStatement preStatusBoardEnv
    (newBlackboard, newEnvironment) =  preStatusBoardEnv
    newFutureChanges = futureChanges0 : futureChanges
