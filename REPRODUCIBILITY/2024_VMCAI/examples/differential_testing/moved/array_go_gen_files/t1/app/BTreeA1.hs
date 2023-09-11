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
        updates = [updatePair0]
        updatePair0 = ((min 2 (max 0 (min 100 (max (-100) (max (-39) 5))))), updateValue0)
        updateValue0
          | ((boardBlVAR0 0 blackboard) == "both") = (boardBlVAR0 1 blackboard)
          | (86 <= 79) = (boardBlVAR0 0 blackboard)
          | otherwise = (boardBlVAR0 0 blackboard)
          where
            (blackboard, environment) = boardEnv
    boardEnvUpdate1 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    boardEnvUpdate1 boardEnv = (blackboard, arrayUpdateEnvEnvVAR1 environment updates)
      where
        (blackboard, environment) = boardEnv
        updates = [updatePair0]
        updatePair0 = ((min 2 (max 0 (min 100 (max (-100) (min (min 100 (max (-100) (min 66 94))) (min 100 (max (-100) (min (-38) (envEnvVAR1 1 environment))))))))), updateValue0)
        updateValue0
          | ((min 100 (max (-100) ((envEnvVAR1 1 environment) * ((min 100 (max (-100) (min (envEnvDEFINE4 blackboard environment) 91))) * (envEnvVAR1 0 environment))))) > (min 100 (max (-100) (abs 83)))) = (min (-2) (max (-5) (min 100 (max (-100) ((envEnvDEFINE4 blackboard environment) * (envEnvDEFINE4 blackboard environment))))))
          | otherwise = (min (-2) (max (-5) ((sereneCOUNT (sereneIMPLIES False (boardBlDEFINE5 1 blackboard)) ((boardBlDEFINE5 0 blackboard) || (boardBlDEFINE5 1 blackboard))) + (sereneCOUNT (sereneXNOR (boardBlDEFINE5 1 blackboard) False) (26 > (envEnvVAR1 2 environment))))))
          where
            (blackboard, environment) = boardEnv
    boardEnvUpdate2 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    boardEnvUpdate2 boardEnv = (arrayUpdateBoardBlVAR0 blackboard updates, environment)
      where
        (blackboard, environment) = boardEnv
        updates = [updatePair0, updatePair1]
        updatePair0 = ((min 2 (max 0 4)), updateValue0)
        updatePair1 = ((min 2 (max 0 (min 100 (max (-100) ((-4) + (4 + 4)))))), updateValue1)
        updateValue0
          | (True == True) = "both"
          | (sereneXOR False (((-95) <= (-33)) == (boardBlDEFINE5 1 blackboard))) = "both"
          | otherwise = (boardBlVAR0 0 blackboard)
          where
            (blackboard, environment) = boardEnv
        updateValue1
          | (boardBlDEFINE5 1 blackboard) = "yes"
          | ((min 100 (max (-100) ((-3) + (3 + (-4))))) /= 33) = (boardBlVAR0 2 blackboard)
          | otherwise = "yes"
          where
            (blackboard, environment) = boardEnv
    returnStatement :: (BTreeBlackboard, BTreeEnvironment) -> BTreeNodeStatus
    returnStatement boardEnv = Success
      where
        (blackboard, environment) = boardEnv
    boardEnvUpdate3 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    boardEnvUpdate3 boardEnv
      | not (((envEnvDEFINE4 conditionBlackboard conditionEnvironment) > (envEnvDEFINE4 conditionBlackboard conditionEnvironment))) = boardEnv
      | otherwise = privateBoardEnv
      where
        (conditionBlackboard, conditionEnvironment) = boardEnv
        privateTempBoardEnv0 = boardEnv
        privateBoardEnv = privateTempBoardEnv1
        privateTempBoardEnv1 = (arrayUpdateBoardBlVAR0 blackboard updates, environment)
          where
            (blackboard, environment) = privateTempBoardEnv0
            updates = [updatePair0, updatePair1]
            updatePair0 = ((min 2 (max 0 (min 100 (max (-100) ((envEnvVAR1 1 environment) + (envEnvDEFINE4 blackboard environment)))))), updateValue0)
            updatePair1 = ((min 2 (max 0 (min 100 (max (-100) (abs (min 100 (max (-100) (abs 12)))))))), updateValue1)
            updateValue0 = "both"
              where
                (blackboard, environment) = privateTempBoardEnv0
            updateValue1 = "yes"
              where
                (blackboard, environment) = privateTempBoardEnv0
    preStatusBoardEnv = boardEnvUpdate2 . boardEnvUpdate1 . boardEnvUpdate0 $ (oldBlackboard, oldEnvironment)
    returnStatus = returnStatement preStatusBoardEnv
    (newBlackboard, newEnvironment) = boardEnvUpdate3 preStatusBoardEnv
    newFutureChanges = futureChanges
