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
    boardEnvUpdate0 boardEnv = (arrayUpdateBoardBlVAR0 blackboard updates, environment)
      where
        (blackboard, environment) = boardEnv
        updates = [updatePair0, updatePair1]
        updatePair0 = ((min 2 (max 0 (sereneCOUNT (False /= (boardBlDEFINE7 0 blackboard)) ((- (boardBlVAR0 2 blackboard)) < 58)))), updateValue0)
        updatePair1 = ((min 2 (max 0 (min ((localBoardLocalDEFINE8 nodeLocation blackboard) * ((-12) * ((localBoardLocalDEFINE8 nodeLocation blackboard) * (boardBlVAR0 0 blackboard)))) (localBoardLocalDEFINE8 nodeLocation blackboard)))), updateValue1)
        updateValue0 = (min (-2) (max (-5) (-50)))
          where
            (blackboard, environment) = boardEnv
        updateValue1 = (min (-2) (max (-5) (abs 20)))
          where
            (blackboard, environment) = boardEnv
    returnStatement :: (BTreeBlackboard, BTreeEnvironment) -> BTreeNodeStatus
    returnStatement boardEnv
      | (sereneXNOR (boardBlDEFINE5 1 blackboard) ((boardBlDEFINE5 2 blackboard) == (boardBlDEFINE7 0 blackboard))) = Success
      | (boardBlDEFINE7 1 blackboard) = Running
      | (sereneXOR (sereneIMPLIES ((boardBlDEFINE5 2 blackboard) && False) True) ((sereneCOUNT (sereneIMPLIES False (boardBlDEFINE5 2 blackboard)) ((boardBlDEFINE7 0 blackboard) == True)) >= (-46))) = Success
      | otherwise = Running
      where
        (blackboard, environment) = boardEnv
    futureChanges0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    futureChanges0 boardEnv
      | (sereneXOR (((localBoardLocalDEFINE8 nodeLocation blackboard) * ((envEnvDEFINE6 1 blackboard environment) * 67)) == (- (envEnvDEFINE6 0 blackboard environment))) True) = (blackboard, updateEnvEnvVAR1 environment ((sereneXOR (envEnvVAR1 environment) True) == ((min (localBoardLocalDEFINE8 nodeLocation blackboard) (-83)) == ((sereneCOUNT ((boardBlDEFINE5 0 blackboard) == (envEnvFROZENVAR3 environment)) ((-51) > (-9))) + (sereneCOUNT (sereneXOR True True) (False == (envEnvVAR1 environment)))))))
      | (sereneXOR (boardBlDEFINE7 0 blackboard) (sereneIMPLIES False (envEnvVAR2 environment))) = (blackboard, updateEnvEnvVAR1 environment (sereneXNOR ((localBoardLocalDEFINE8 nodeLocation blackboard) <= (abs (localBoardLocalDEFINE8 nodeLocation blackboard))) (sereneIMPLIES False False)))
      | otherwise = (blackboard, updateEnvEnvVAR1 environment False)
      where
        (blackboard, environment) = boardEnv
    preStatusBoardEnv = boardEnvUpdate0 (oldBlackboard, oldEnvironment)
    returnStatus = returnStatement preStatusBoardEnv
    (newBlackboard, newEnvironment) =  preStatusBoardEnv
    newFutureChanges = futureChanges0 : futureChanges
