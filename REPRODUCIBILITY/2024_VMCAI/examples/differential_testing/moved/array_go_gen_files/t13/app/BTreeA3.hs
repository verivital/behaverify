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
      | not (((envEnvVAR1 2 conditionEnvironment) /= "both")) = boardEnv
      | otherwise = privateBoardEnv
      where
        (conditionBlackboard, conditionEnvironment) = boardEnv
        privateTempBoardEnv0 = boardEnv
        privateBoardEnv = privateTempBoardEnv1
        privateTempBoardEnv1 = (arrayUpdateBoardBlVAR3 blackboard updates, environment)
          where
            (blackboard, environment) = privateTempBoardEnv0
            updates = [updatePair0, updatePair1]
            updatePair0 = ((min 1 (max 0 (- (76 * ((-36) * ((envEnvVAR4 environment) * (-22))))))), updateValue0)
            updatePair1 = ((min 1 (max 0 (max (localBoardLocalDEFINE7 nodeLocation blackboard) (envEnvVAR4 environment)))), updateValue1)
            updateValue0
              | ((max 29 (min (boardBlVAR0 blackboard) (-26))) < (sereneCOUNT (sereneXOR ((localBoardLocalDEFINE7 nodeLocation blackboard) <= (localBoardLocalDEFINE7 nodeLocation blackboard)) (False == True)) (False || False))) = "no"
              | otherwise = (envEnvVAR2 1 environment)
              where
                (blackboard, environment) = privateTempBoardEnv0
            updateValue1
              | (sereneXNOR (True /= True) ((-8) < 36)) = "both"
              | otherwise = (envEnvVAR1 2 environment)
              where
                (blackboard, environment) = privateTempBoardEnv0
    boardEnvUpdate1 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    boardEnvUpdate1 boardEnv
      | True = (updateBoardBlVAR0 blackboard (min 5 (max 2 (localBoardLocalDEFINE7 nodeLocation blackboard))), environment)
      | False = (updateBoardBlVAR0 blackboard (min 5 (max 2 (- 29))), environment)
      | otherwise = (updateBoardBlVAR0 blackboard (min 5 (max 2 (-61))), environment)
      where
        (blackboard, environment) = boardEnv
    boardEnvUpdate2 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    boardEnvUpdate2 boardEnv
      | not (True) = boardEnv
      | otherwise = privateBoardEnv
      where
        (conditionBlackboard, conditionEnvironment) = boardEnv
        privateTempBoardEnv0 = boardEnv
        privateBoardEnv = privateTempBoardEnv1
        privateTempBoardEnv1
          | (False && True) = (updateBoardBlVAR0 blackboard (min 5 (max 2 38)), environment)
          | otherwise = (updateBoardBlVAR0 blackboard (min 5 (max 2 (abs (localBoardLocalDEFINE7 nodeLocation blackboard)))), environment)
          where
            (blackboard, environment) = privateTempBoardEnv0
    returnStatement :: (BTreeBlackboard, BTreeEnvironment) -> BTreeNodeStatus
    returnStatement boardEnv
      | (False && True) = Failure
      | otherwise = Success
      where
        (blackboard, environment) = boardEnv
    boardEnvUpdate3 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    boardEnvUpdate3 boardEnv = (blackboard, arrayUpdateEnvEnvVAR2 environment updates)
      where
        (blackboard, environment) = boardEnv
        updates = [updatePair0, updatePair1]
        updatePair0 = ((min 1 (max 0 (max (32 - (boardBlVAR0 blackboard)) ((boardBlVAR0 blackboard) - 45)))), updateValue0)
        updatePair1 = ((min 1 (max 0 (min 66 (-91)))), updateValue1)
        updateValue0
          | ((True == True) && False) = (boardBlDEFINE5 blackboard)
          | ((localBoardLocalDEFINE7 nodeLocation blackboard) < (- (-28))) = "no"
          | otherwise = "both"
          where
            (blackboard, environment) = boardEnv
        updateValue1
          | (sereneIMPLIES True True) = "both"
          | ((-3) > (envEnvVAR4 environment)) = "both"
          | otherwise = "both"
          where
            (blackboard, environment) = boardEnv
    preStatusBoardEnv = boardEnvUpdate2 . boardEnvUpdate1 . boardEnvUpdate0 $ (oldBlackboard, oldEnvironment)
    returnStatus = returnStatement preStatusBoardEnv
    (newBlackboard, newEnvironment) = boardEnvUpdate3 preStatusBoardEnv
    newFutureChanges = futureChanges
