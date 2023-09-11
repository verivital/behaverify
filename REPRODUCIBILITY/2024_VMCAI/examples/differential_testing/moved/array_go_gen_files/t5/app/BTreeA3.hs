module BTreeA3 where
import BehaviorTreeCore
import BehaviorTreeBlackboard
import BehaviorTreeEnvironment
import SereneRandomizer
import SereneOperations



bTreeFunctionA3 :: [BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
bTreeFunctionA3 _ nodeLocation _ _ _ _ oldBlackboard oldEnvironment futureChanges = (returnStatus, [], [], newBlackboard, newEnvironment, newFutureChanges)
  where
    boardEnvUpdate0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    boardEnvUpdate0 boardEnv
      | False = (blackboard, updateEnvEnvVAR1 environment (min 5 (max 2 (max (envEnvVAR1 environment) 74))))
      | (False && True) = (blackboard, updateEnvEnvVAR1 environment (min 5 (max 2 (((boardBlDEFINE6 blackboard) * ((envEnvVAR1 environment) * 90)) - (abs (-98))))))
      | otherwise = (blackboard, updateEnvEnvVAR1 environment (min 5 (max 2 4)))
      where
        (blackboard, environment) = boardEnv
    returnStatement :: (BTreeBlackboard, BTreeEnvironment) -> BTreeNodeStatus
    returnStatement boardEnv = Failure
      where
        (blackboard, environment) = boardEnv
    futureChanges0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    futureChanges0 boardEnv
      | ((min (-4) (boardBlDEFINE6 blackboard)) > (- 38)) = (blackboard, updateEnvEnvVAR1 environment (min 5 (max 2 ((- (boardBlFROZENVAR4 1 blackboard)) + ((abs 69) + ((boardBlDEFINE6 blackboard) + (27 * (max 18 78))))))))
      | otherwise = (blackboard, updateEnvEnvVAR1 environment (min 5 (max 2 (- (abs (boardBlFROZENVAR4 0 blackboard))))))
      where
        (blackboard, environment) = boardEnv
    preStatusBoardEnv = boardEnvUpdate0 (oldBlackboard, oldEnvironment)
    returnStatus = returnStatement preStatusBoardEnv
    (newBlackboard, newEnvironment) =  preStatusBoardEnv
    newFutureChanges = futureChanges0 : futureChanges
