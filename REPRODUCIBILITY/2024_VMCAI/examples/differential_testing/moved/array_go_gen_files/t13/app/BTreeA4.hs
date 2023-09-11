module BTreeA4 where
import BehaviorTreeCore
import BehaviorTreeBlackboard
import BehaviorTreeEnvironment
import SereneRandomizer
import SereneOperations



bTreeFunctionA4 :: [BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
bTreeFunctionA4 _ nodeLocation _ _ _ _ oldBlackboard oldEnvironment futureChanges = (returnStatus, [], [], newBlackboard, newEnvironment, newFutureChanges)
  where
    returnStatement :: (BTreeBlackboard, BTreeEnvironment) -> BTreeNodeStatus
    returnStatement boardEnv
      | ((max 93 (localBoardLocalDEFINE6 nodeLocation 0 blackboard)) <= (localBoardLocalDEFINE6 nodeLocation 2 blackboard)) = Failure
      | False = Running
      | (sereneXOR False False) = Failure
      | otherwise = Failure
      where
        (blackboard, environment) = boardEnv
    boardEnvUpdate0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    boardEnvUpdate0 boardEnv
      | not (((False && True) == ((envEnvVAR4 conditionEnvironment) /= (localBoardLocalDEFINE6 nodeLocation 2 conditionBlackboard)))) = boardEnv
      | otherwise = privateBoardEnv
      where
        (conditionBlackboard, conditionEnvironment) = boardEnv
        privateTempBoardEnv0 = boardEnv
        privateBoardEnv = privateTempBoardEnv1
        privateTempBoardEnv1
          | ((sereneXOR (False && False) False) == (True == False)) = (updateBoardBlVAR0 blackboard (min 5 (max 2 36)), environment)
          | (False == True) = (updateBoardBlVAR0 blackboard (min 5 (max 2 (envEnvVAR4 environment))), environment)
          | otherwise = (updateBoardBlVAR0 blackboard (min 5 (max 2 (- (max (-89) (localBoardLocalDEFINE6 nodeLocation 2 blackboard))))), environment)
          where
            (blackboard, environment) = privateTempBoardEnv0
    preStatusBoardEnv =  (oldBlackboard, oldEnvironment)
    returnStatus = returnStatement preStatusBoardEnv
    (newBlackboard, newEnvironment) = boardEnvUpdate0 preStatusBoardEnv
    newFutureChanges = futureChanges
