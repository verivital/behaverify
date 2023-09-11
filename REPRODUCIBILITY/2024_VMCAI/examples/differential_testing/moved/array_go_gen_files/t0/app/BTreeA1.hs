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
      | not ((sereneXOR (sereneXNOR ((envEnvDEFINE5 0 conditionBlackboard conditionEnvironment) > (envEnvDEFINE5 1 conditionBlackboard conditionEnvironment)) (77 < (boardBlVAR0 1 conditionBlackboard))) (False && (envEnvDEFINE6 conditionBlackboard conditionEnvironment)))) = boardEnv
      | otherwise = privateBoardEnv
      where
        (conditionBlackboard, conditionEnvironment) = boardEnv
        privateTempBoardEnv0 = boardEnv
        privateBoardEnv = privateTempBoardEnv2
        privateTempBoardEnv1 = (arrayUpdateBoardBlVAR0 blackboard updates, environment)
          where
            (blackboard, environment) = privateTempBoardEnv0
            updates = [updatePair0]
            updatePair0 = ((min 1 (max 0 ((sereneCOUNT (sereneXOR True (False || (envEnvDEFINE7 blackboard environment))) ((envEnvDEFINE5 1 blackboard environment) /= 88)) + (sereneCOUNT False ("yes" == "yes"))))), updateValue0)
            updateValue0 = (min 5 (max 2 (boardBlVAR0 1 blackboard)))
              where
                (blackboard, environment) = privateTempBoardEnv0
        privateTempBoardEnv2 = (arrayUpdateBoardBlVAR0 blackboard updates, environment)
          where
            (blackboard, environment) = privateTempBoardEnv1
            updates = [updatePair0, updatePair1]
            updatePair0 = ((min 1 (max 0 (envEnvDEFINE5 0 blackboard environment))), updateValue0)
            updatePair1 = ((min 1 (max 0 (envEnvDEFINE5 0 blackboard environment))), updateValue1)
            updateValue0
              | (((-32) * ((boardBlVAR0 0 blackboard) * (14 * 0))) /= 14) = (min 5 (max 2 (- (boardBlVAR0 1 blackboard))))
              | otherwise = (min 5 (max 2 (max ((sereneCOUNT ((envEnvDEFINE5 0 blackboard environment) >= ((envEnvDEFINE5 1 blackboard environment) + (envEnvDEFINE5 1 blackboard environment))) (True == True)) + (sereneCOUNT False ((envEnvFROZENVAR3 0 environment) == "no"))) (min 8 (-67)))))
              where
                (blackboard, environment) = privateTempBoardEnv1
            updateValue1
              | True = (min 5 (max 2 (min ((envEnvDEFINE5 1 blackboard environment) + (76 + (envEnvDEFINE5 2 blackboard environment))) (83 * (29 * ((-36) * ((-84) * (-27))))))))
              | otherwise = (min 5 (max 2 ((-21) + ((envEnvDEFINE5 2 blackboard environment) + (67 + (-63))))))
              where
                (blackboard, environment) = privateTempBoardEnv1
    returnStatement :: (BTreeBlackboard, BTreeEnvironment) -> BTreeNodeStatus
    returnStatement boardEnv
      | ((sereneIMPLIES True True) == (False || (True || True))) = Running
      | (True == False) = Failure
      | (sereneXNOR True ((min 64 (boardBlVAR0 0 blackboard)) >= ((boardBlVAR0 0 blackboard) + (-23)))) = Running
      | otherwise = Failure
      where
        (blackboard, environment) = boardEnv
    boardEnvUpdate1 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    boardEnvUpdate1 boardEnv = (blackboard, arrayUpdateEnvEnvVAR1 environment updates)
      where
        (blackboard, environment) = boardEnv
        updates = [updatePair0, updatePair1]
        updatePair0 = ((min 2 (max 0 ((boardBlVAR0 1 blackboard) + (envEnvDEFINE5 1 blackboard environment)))), updateValue0)
        updatePair1 = ((min 2 (max 0 ((abs (envEnvDEFINE5 1 blackboard environment)) * (envEnvDEFINE5 1 blackboard environment)))), updateValue1)
        updateValue0
          | False = ("both" == "both")
          | otherwise = (False == (envEnvDEFINE7 blackboard environment))
          where
            (blackboard, environment) = boardEnv
        updateValue1
          | ((40 < (envEnvDEFINE5 2 blackboard environment)) == False) = (sereneXNOR ((envEnvDEFINE5 1 blackboard environment) > (envEnvDEFINE5 0 blackboard environment)) (sereneXOR (sereneXOR (envEnvDEFINE6 blackboard environment) (envEnvVAR1 2 environment)) True))
          | otherwise = (((envEnvDEFINE5 1 blackboard environment) * ((envEnvDEFINE5 1 blackboard environment) * ((boardBlVAR0 0 blackboard) * (envEnvDEFINE5 1 blackboard environment)))) <= (envEnvDEFINE5 0 blackboard environment))
          where
            (blackboard, environment) = boardEnv
    preStatusBoardEnv = boardEnvUpdate0 (oldBlackboard, oldEnvironment)
    returnStatus = returnStatement preStatusBoardEnv
    (newBlackboard, newEnvironment) = boardEnvUpdate1 preStatusBoardEnv
    newFutureChanges = futureChanges
