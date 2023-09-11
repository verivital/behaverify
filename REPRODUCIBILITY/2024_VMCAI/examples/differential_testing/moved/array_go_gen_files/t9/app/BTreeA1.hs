module BTreeA1 where
import BehaviorTreeCore
import BehaviorTreeBlackboard
import BehaviorTreeEnvironment
import SereneRandomizer
import SereneOperations



bTreeFunctionA1 :: [BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
bTreeFunctionA1 _ nodeLocation _ _ _ _ oldBlackboard oldEnvironment futureChanges = (returnStatus, [], [], newBlackboard, newEnvironment, newFutureChanges)
  where
    boardEnvUpdate0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    boardEnvUpdate0 boardEnv = (blackboard, arrayUpdateEnvEnvVAR1 environment updates)
      where
        (blackboard, environment) = boardEnv
        updates = [updatePair0]
        updatePair0 = ((min 2 (max 0 60)), updateValue0)
        updateValue0
          | (True && True) = (min 5 (max 2 (- (envEnvVAR2 1 environment))))
          | otherwise = (min 5 (max 2 ((sereneCOUNT (sereneXNOR True (boardBlVAR3 0 blackboard)) ((boardBlVAR3 1 blackboard) && False)) + (sereneCOUNT (sereneXOR False False) (True == True)))))
          where
            (blackboard, environment) = boardEnv
    returnStatement :: (BTreeBlackboard, BTreeEnvironment) -> BTreeNodeStatus
    returnStatement boardEnv
      | (boardBlVAR3 0 blackboard) = Failure
      | otherwise = Success
      where
        (blackboard, environment) = boardEnv
    boardEnvUpdate1 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    boardEnvUpdate1 boardEnv
      | not (((localBoardLocalDEFINE5 nodeLocation 2 conditionBlackboard) == "no")) = boardEnv
      | otherwise = privateBoardEnv
      where
        (conditionBlackboard, conditionEnvironment) = boardEnv
        privateTempBoardEnv0 = boardEnv
        privateBoardEnv = privateTempBoardEnv1
        privateTempBoardEnv1 = (arrayUpdateBoardBlVAR3 blackboard updates, environment)
          where
            (blackboard, environment) = privateTempBoardEnv0
            updates = [updatePair0]
            updatePair0 = ((min 1 (max 0 (abs (-41)))), updateValue0)
            updateValue0 = ((- 90) < (max (-63) (envEnvVAR1 2 environment)))
              where
                (blackboard, environment) = privateTempBoardEnv0
    preStatusBoardEnv = boardEnvUpdate0 (oldBlackboard, oldEnvironment)
    returnStatus = returnStatement preStatusBoardEnv
    (newBlackboard, newEnvironment) = boardEnvUpdate1 preStatusBoardEnv
    newFutureChanges = futureChanges
