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
    boardEnvUpdate0 boardEnv
      | not ((sereneXOR True False)) = boardEnv
      | otherwise = privateBoardEnv
      where
        (conditionBlackboard, conditionEnvironment) = boardEnv
        privateTempBoardEnv0 = boardEnv
        privateBoardEnv = privateTempBoardEnv1
        privateTempBoardEnv1
          | True = (updateLocalBoardLocalVAR2 nodeLocation blackboard (min 5 (max 2 (max (boardBlFROZENVAR4 0 blackboard) (envEnvVAR1 environment)))), environment)
          | (sereneIMPLIES False ((envEnvDEFINE7 blackboard environment) /= "both")) = (updateLocalBoardLocalVAR2 nodeLocation blackboard (min 5 (max 2 (91 - (envEnvVAR1 environment)))), environment)
          | otherwise = (updateLocalBoardLocalVAR2 nodeLocation blackboard (min 5 (max 2 (abs (abs (-82))))), environment)
          where
            (blackboard, environment) = privateTempBoardEnv0
    returnStatement :: (BTreeBlackboard, BTreeEnvironment) -> BTreeNodeStatus
    returnStatement boardEnv = Failure
      where
        (blackboard, environment) = boardEnv
    boardEnvUpdate1 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    boardEnvUpdate1 boardEnv
      | not ((True && (sereneXOR True True))) = boardEnv
      | otherwise = privateBoardEnv
      where
        (conditionBlackboard, conditionEnvironment) = boardEnv
        privateTempBoardEnv0 = boardEnv
        privateBoardEnv = privateTempBoardEnv1
        privateTempBoardEnv1
          | (sereneXNOR True ((boardBlDEFINE6 blackboard) < (-62))) = (updateBoardBlVAR0 blackboard "no", environment)
          | otherwise = (updateBoardBlVAR0 blackboard "both", environment)
          where
            (blackboard, environment) = privateTempBoardEnv0
    futureChanges0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    futureChanges0 boardEnv
      | ((sereneXNOR True True) == (True == False)) = (blackboard, updateEnvEnvVAR1 environment (min 5 (max 2 (boardBlDEFINE6 blackboard))))
      | (37 >= (33 - (-24))) = (blackboard, updateEnvEnvVAR1 environment (min 5 (max 2 (envEnvVAR1 environment))))
      | otherwise = (blackboard, updateEnvEnvVAR1 environment (min 5 (max 2 (-28))))
      where
        (blackboard, environment) = boardEnv
    futureChanges1 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    futureChanges1 boardEnv
      | (sereneXOR ((sereneXNOR False True) == (True && False)) False) = (blackboard, updateEnvEnvVAR1 environment (min 5 (max 2 20)))
      | ((sereneIMPLIES False False) && (sereneXOR True False)) = (blackboard, updateEnvEnvVAR1 environment (min 5 (max 2 ((sereneCOUNT ((envEnvDEFINE7 blackboard environment) /= (envEnvDEFINE7 blackboard environment)) (81 <= (max (envEnvVAR1 environment) 60))) + (sereneCOUNT False (True && ((-25) < 78)))))))
      | otherwise = (blackboard, updateEnvEnvVAR1 environment (min 5 (max 2 ((-77) - (boardBlFROZENVAR4 1 blackboard)))))
      where
        (blackboard, environment) = boardEnv
    preStatusBoardEnv = boardEnvUpdate0 (oldBlackboard, oldEnvironment)
    returnStatus = returnStatement preStatusBoardEnv
    (newBlackboard, newEnvironment) = boardEnvUpdate1 preStatusBoardEnv
    newFutureChanges = futureChanges1 : futureChanges0 : futureChanges
