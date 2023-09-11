module BTreeA4 where
import BehaviorTreeCore
import BehaviorTreeBlackboard
import BehaviorTreeEnvironment
import SereneRandomizer
import SereneOperations



bTreeFunctionA4 :: [BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
bTreeFunctionA4 _ nodeLocation _ _ _ _ oldBlackboard oldEnvironment futureChanges = (returnStatus, [], [], newBlackboard, newEnvironment, newFutureChanges)
  where
    boardEnvUpdate0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    boardEnvUpdate0 boardEnv
      | not ((sereneIMPLIES ("yes" /= "both") False)) = boardEnv
      | otherwise = privateBoardEnv
      where
        (conditionBlackboard, conditionEnvironment) = boardEnv
        privateTempBoardEnv0 = boardEnv
        privateBoardEnv = privateTempBoardEnv2
        privateTempBoardEnv1 = (arrayUpdateBoardBlVAR3 blackboard updates, environment)
          where
            (blackboard, environment) = privateTempBoardEnv0
            updates = [updatePair0, updatePair1]
            updatePair0 = ((min 1 (max 0 (- (abs (-100))))), updateValue0)
            updatePair1 = ((min 1 (max 0 ((boardBlFROZENVAR4 0 blackboard) - 100))), updateValue1)
            updateValue0 = (sereneXOR (boardBlVAR3 0 blackboard) False)
              where
                (blackboard, environment) = privateTempBoardEnv0
            updateValue1 = ((boardBlDEFINE6 blackboard) > (boardBlDEFINE6 blackboard))
              where
                (blackboard, environment) = privateTempBoardEnv0
        privateTempBoardEnv2
          | ((boardBlVAR3 1 blackboard) && True) = (updateBoardBlVAR0 blackboard "no", environment)
          | otherwise = (updateBoardBlVAR0 blackboard "both", environment)
          where
            (blackboard, environment) = privateTempBoardEnv1
    returnStatement :: (BTreeBlackboard, BTreeEnvironment) -> BTreeNodeStatus
    returnStatement boardEnv
      | False = Failure
      | otherwise = Success
      where
        (blackboard, environment) = boardEnv
    boardEnvUpdate1 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    boardEnvUpdate1 boardEnv
      | not ((boardBlVAR3 1 conditionBlackboard)) = boardEnv
      | otherwise = privateBoardEnv
      where
        (conditionBlackboard, conditionEnvironment) = boardEnv
        privateTempBoardEnv0 = boardEnv
        privateBoardEnv = privateTempBoardEnv1
        privateTempBoardEnv1 = (updateBoardBlVAR0 blackboard "both", environment)
          where
            (blackboard, environment) = privateTempBoardEnv0
    preStatusBoardEnv = boardEnvUpdate0 (oldBlackboard, oldEnvironment)
    returnStatus = returnStatement preStatusBoardEnv
    (newBlackboard, newEnvironment) = boardEnvUpdate1 preStatusBoardEnv
    newFutureChanges = futureChanges
