module BTreeA2 where
import BehaviorTreeCore
import BehaviorTreeBlackboard
import BehaviorTreeEnvironment
import SereneRandomizer
import SereneOperations



bTreeFunctionA2 :: [BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
bTreeFunctionA2 _ nodeLocation _ _ _ _ oldBlackboard oldEnvironment futureChanges = (returnStatus, [], [], newBlackboard, newEnvironment, newFutureChanges)
  where
    boardEnvUpdate0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    boardEnvUpdate0 boardEnv
      | not (((sereneXNOR False ((envEnvFROZENVAR3 conditionEnvironment) == (boardBlDEFINE7 0 conditionBlackboard))) == ((boardBlVAR0 0 conditionBlackboard) /= 14))) = boardEnv
      | otherwise = privateBoardEnv
      where
        (conditionBlackboard, conditionEnvironment) = boardEnv
        privateTempBoardEnv0 = boardEnv
        privateBoardEnv = privateTempBoardEnv1
        privateTempBoardEnv1 = (arrayUpdateBoardBlVAR0 blackboard updates, environment)
          where
            (blackboard, environment) = privateTempBoardEnv0
            updates = [updatePair0]
            updatePair0 = ((min 2 (max 0 (sereneCOUNT ((envEnvFROZENVAR3 environment) || (envEnvFROZENVAR3 environment)) ((localBoardLocalDEFINE8 nodeLocation blackboard) < (-90))))), updateValue0)
            updateValue0
              | (38 >= (boardBlVAR0 1 blackboard)) = (min (-2) (max (-5) (max (envEnvDEFINE6 1 blackboard environment) ((localBoardLocalDEFINE8 nodeLocation blackboard) * (-32)))))
              | ((-11) <= (boardBlVAR0 1 blackboard)) = (min (-2) (max (-5) ((sereneCOUNT (((envEnvDEFINE6 2 blackboard environment) <= ((localBoardLocalDEFINE8 nodeLocation blackboard) + (51 + ((envEnvDEFINE6 0 blackboard environment) + (envEnvDEFINE6 1 blackboard environment))))) && ((envEnvVAR1 environment) == (sereneXNOR True False))) ((abs (boardBlVAR0 1 blackboard)) /= ((boardBlVAR0 1 blackboard) - (-58)))) + (sereneCOUNT False ((False && False) || (28 == (38 * ((-99) * (localBoardLocalDEFINE8 nodeLocation blackboard)))))))))
              | otherwise = (min (-2) (max (-5) (max (boardBlVAR0 2 blackboard) (min (-93) (envEnvDEFINE6 1 blackboard environment)))))
              where
                (blackboard, environment) = privateTempBoardEnv0
    returnStatement :: (BTreeBlackboard, BTreeEnvironment) -> BTreeNodeStatus
    returnStatement boardEnv
      | ((abs 94) >= 18) = Success
      | ((abs (-67)) < (max (localBoardLocalDEFINE8 nodeLocation blackboard) 75)) = Failure
      | otherwise = Failure
      where
        (blackboard, environment) = boardEnv
    boardEnvUpdate1 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    boardEnvUpdate1 boardEnv = (arrayUpdateBoardBlVAR0 blackboard updates, environment)
      where
        (blackboard, environment) = boardEnv
        updates = [updatePair0, updatePair1, updatePair2]
        updatePair0 = ((min 2 (max 0 (min (abs 32) (-97)))), updateValue0)
        updatePair1 = ((min 2 (max 0 (-29))), updateValue1)
        updatePair2 = ((min 2 (max 0 (min (6 * (min 2 (localBoardLocalDEFINE8 nodeLocation blackboard))) (69 * (boardBlVAR0 2 blackboard))))), updateValue2)
        updateValue0 = (min (-2) (max (-5) (-14)))
          where
            (blackboard, environment) = boardEnv
        updateValue1 = (min (-2) (max (-5) (max (-2) (localBoardLocalDEFINE8 nodeLocation blackboard))))
          where
            (blackboard, environment) = boardEnv
        updateValue2 = (min (-2) (max (-5) ((boardBlVAR0 1 blackboard) + ((max 86 33) + ((max (localBoardLocalDEFINE8 nodeLocation blackboard) (-7)) + (max (boardBlVAR0 1 blackboard) (-33)))))))
          where
            (blackboard, environment) = boardEnv
    preStatusBoardEnv = boardEnvUpdate0 (oldBlackboard, oldEnvironment)
    returnStatus = returnStatement preStatusBoardEnv
    (newBlackboard, newEnvironment) = boardEnvUpdate1 preStatusBoardEnv
    newFutureChanges = futureChanges
