module BTreeA1 where
import BehaviorTreeCore
import BehaviorTreeBlackboard
import BehaviorTreeEnvironment
import SereneRandomizer
import SereneOperations



bTreeFunctionA1 :: [BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
bTreeFunctionA1 _ nodeLocation _ _ _ _ oldBlackboard oldEnvironment futureChanges = (returnStatus, [], [], newBlackboard, newEnvironment, newFutureChanges)
  where
    returnStatement :: (BTreeBlackboard, BTreeEnvironment) -> BTreeNodeStatus
    returnStatement boardEnv
      | False = Failure
      | (sereneXOR (42 >= (localBoardLocalDEFINE5 nodeLocation 0 blackboard)) ((-100) <= (-7))) = Failure
      | otherwise = Running
      where
        (blackboard, environment) = boardEnv
    boardEnvUpdate0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    boardEnvUpdate0 boardEnv
      | not ((sereneIMPLIES (57 /= (localBoardLocalDEFINE5 nodeLocation 0 conditionBlackboard)) (False && (envEnvVAR1 1 conditionEnvironment)))) = boardEnv
      | otherwise = privateBoardEnv
      where
        (conditionBlackboard, conditionEnvironment) = boardEnv
        privateTempBoardEnv0 = boardEnv
        privateBoardEnv = privateTempBoardEnv3
        privateTempBoardEnv1
          | (True && (True == (envEnvVAR1 0 environment))) = (updateBoardBlVAR0 blackboard (min 5 (max 2 ((sereneCOUNT (sereneXOR True (False && True)) ((max 55 2) /= 38)) + (sereneCOUNT (((sereneCOUNT ((envEnvVAR1 0 environment) /= (envEnvVAR1 1 environment)) (64 <= (envEnvFROZENVAR4 2 environment))) > (-35)) == False) ((max (envEnvFROZENVAR4 0 environment) (boardBlVAR0 blackboard)) >= ((-84) - (max (localBoardLocalDEFINE5 nodeLocation 1 blackboard) (envEnvFROZENVAR4 2 environment)))))))), environment)
          | (True || True) = (updateBoardBlVAR0 blackboard (min 5 (max 2 (max 10 (90 - 95)))), environment)
          | otherwise = (updateBoardBlVAR0 blackboard (min 5 (max 2 ((sereneCOUNT (sereneIMPLIES True (sereneXOR (envEnvVAR1 0 environment) (envEnvVAR1 0 environment))) ((17 <= (-47)) || ((boardBlVAR0 blackboard) >= (boardBlVAR0 blackboard)))) + (sereneCOUNT ((44 + (55 + ((boardBlVAR0 blackboard) + (localBoardLocalDEFINE5 nodeLocation 1 blackboard)))) >= (max (- (-81)) 99)) (((localBoardLocalDEFINE5 nodeLocation 0 blackboard) * 55) > (-18)))))), environment)
          where
            (blackboard, environment) = privateTempBoardEnv0
        privateTempBoardEnv2
          | ((envEnvVAR2 environment) /= (envEnvFROZENVAR3 1 environment)) = (updateBoardBlVAR0 blackboard (min 5 (max 2 (- ((sereneCOUNT (False == (envEnvVAR1 1 environment)) (sereneXNOR False False)) + (sereneCOUNT ("no" == "yes") (sereneXOR (envEnvVAR1 1 environment) (envEnvVAR1 1 environment))))))), environment)
          | ((envEnvVAR1 0 environment) || (envEnvVAR1 1 environment)) = (updateBoardBlVAR0 blackboard (min 5 (max 2 (4 - (boardBlVAR0 blackboard)))), environment)
          | otherwise = (updateBoardBlVAR0 blackboard (min 5 (max 2 (-78))), environment)
          where
            (blackboard, environment) = privateTempBoardEnv1
        privateTempBoardEnv3
          | True = (updateBoardBlVAR0 blackboard (min 5 (max 2 (abs (max (-56) (localBoardLocalDEFINE5 nodeLocation 1 blackboard))))), environment)
          | otherwise = (updateBoardBlVAR0 blackboard (min 5 (max 2 (- ((localBoardLocalDEFINE5 nodeLocation 0 blackboard) - (localBoardLocalDEFINE5 nodeLocation 0 blackboard))))), environment)
          where
            (blackboard, environment) = privateTempBoardEnv2
    preStatusBoardEnv =  (oldBlackboard, oldEnvironment)
    returnStatus = returnStatement preStatusBoardEnv
    (newBlackboard, newEnvironment) = boardEnvUpdate0 preStatusBoardEnv
    newFutureChanges = futureChanges
