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
    boardEnvUpdate0 boardEnv = (arrayUpdateBoardBlVAR0 blackboard updates, environment)
      where
        (blackboard, environment) = boardEnv
        updates = [updatePair0]
        updatePair0 = ((min 2 (max 0 (abs (max (boardBlVAR0 2 blackboard) (localBoardLocalDEFINE8 nodeLocation blackboard))))), updateValue0)
        updateValue0 = (min (-2) (max (-5) ((sereneCOUNT (((boardBlVAR0 2 blackboard) + ((localBoardLocalDEFINE8 nodeLocation blackboard) + 41)) >= ((sereneCOUNT (sereneXOR True False) ((boardBlDEFINE7 0 blackboard) == True)) + (sereneCOUNT False ((boardBlDEFINE7 1 blackboard) == False)))) (sereneIMPLIES (True == False) (boardBlDEFINE7 0 blackboard))) + (sereneCOUNT (sereneXOR ((- (-26)) > (localBoardLocalFROZENVAR4 nodeLocation blackboard)) ((localBoardLocalDEFINE8 nodeLocation blackboard) >= 99)) ((localBoardLocalDEFINE8 nodeLocation blackboard) <= (((localBoardLocalDEFINE8 nodeLocation blackboard) * 39) - (-75)))))))
          where
            (blackboard, environment) = boardEnv
    boardEnvUpdate1 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    boardEnvUpdate1 boardEnv = (blackboard, updateEnvEnvVAR1 environment (False || False))
      where
        (blackboard, environment) = boardEnv
    returnStatement :: (BTreeBlackboard, BTreeEnvironment) -> BTreeNodeStatus
    returnStatement boardEnv
      | (sereneXNOR (boardBlDEFINE7 1 blackboard) (boardBlDEFINE5 1 blackboard)) = Running
      | otherwise = Failure
      where
        (blackboard, environment) = boardEnv
    futureChanges0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    futureChanges0 boardEnv = (blackboard, updateEnvEnvVAR2 environment ((envEnvVAR1 environment) && (envEnvFROZENVAR3 environment)))
      where
        (blackboard, environment) = boardEnv
    preStatusBoardEnv = boardEnvUpdate1 . boardEnvUpdate0 $ (oldBlackboard, oldEnvironment)
    returnStatus = returnStatement preStatusBoardEnv
    (newBlackboard, newEnvironment) =  preStatusBoardEnv
    newFutureChanges = futureChanges0 : futureChanges
