module BTreeA3 where
import BehaviorTreeCore
import BehaviorTreeBlackboard
import BehaviorTreeEnvironment
import SereneRandomizer
import SereneOperations



bTreeFunctionA3 :: [BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
bTreeFunctionA3 _ nodeLocation _ _ _ _ oldBlackboard oldEnvironment futureChanges = (returnStatus, [], [], newBlackboard, newEnvironment, newFutureChanges)
  where
    returnStatement :: (BTreeBlackboard, BTreeEnvironment) -> BTreeNodeStatus
    returnStatement boardEnv
      | ((-81) > ((-79) - (-48))) = Success
      | ((boardBlVAR0 blackboard) && False) = Success
      | (sereneIMPLIES ((localBoardLocalDEFINE7 nodeLocation 0 blackboard) > 4) (sereneXNOR True (boardBlVAR0 blackboard))) = Failure
      | otherwise = Success
      where
        (blackboard, environment) = boardEnv
    boardEnvUpdate0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    boardEnvUpdate0 boardEnv
      | not (((False == (boardBlVAR0 conditionBlackboard)) || (sereneXOR (boardBlVAR0 conditionBlackboard) True))) = boardEnv
      | otherwise = privateBoardEnv
      where
        (conditionBlackboard, conditionEnvironment) = boardEnv
        privateTempBoardEnv0 = boardEnv
        privateBoardEnv = privateTempBoardEnv2
        privateTempBoardEnv1 = (updateBoardBlVAR0 blackboard ((envEnvVAR1 2 environment) > 2), environment)
          where
            (blackboard, environment) = privateTempBoardEnv0
        privateTempBoardEnv2 = (updateBoardBlVAR0 blackboard True, environment)
          where
            (blackboard, environment) = privateTempBoardEnv1
    preStatusBoardEnv =  (oldBlackboard, oldEnvironment)
    returnStatus = returnStatement preStatusBoardEnv
    (newBlackboard, newEnvironment) = boardEnvUpdate0 preStatusBoardEnv
    newFutureChanges = futureChanges
