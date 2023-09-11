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
      | (sereneXOR False (False && (boardBlDEFINE5 0 blackboard))) = Success
      | otherwise = Success
      where
        (blackboard, environment) = boardEnv
    boardEnvUpdate0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    boardEnvUpdate0 boardEnv
      | not (((localBoardLocalVAR2 nodeLocation conditionBlackboard) > (-26))) = boardEnv
      | otherwise = privateBoardEnv
      where
        (conditionBlackboard, conditionEnvironment) = boardEnv
        privateTempBoardEnv0 = boardEnv
        privateBoardEnv = privateTempBoardEnv2
        privateTempBoardEnv1 = (updateLocalBoardLocalVAR2 nodeLocation blackboard (min 5 (max 2 (min 100 (max (-100) (- (min 100 (max (-100) ((envEnvDEFINE4 blackboard environment) * (envEnvVAR1 2 environment))))))))), environment)
          where
            (blackboard, environment) = privateTempBoardEnv0
        privateTempBoardEnv2 = (arrayUpdateBoardBlVAR0 blackboard updates, environment)
          where
            (blackboard, environment) = privateTempBoardEnv1
            updates = [updatePair0, updatePair1]
            updatePair0 = ((min 2 (max 0 (min 100 (max (-100) ((min 100 (max (-100) (66 * 69))) * (localBoardLocalVAR2 nodeLocation blackboard)))))), updateValue0)
            updatePair1 = ((min 2 (max 0 (min 100 (max (-100) (abs (min 100 (max (-100) (abs 45)))))))), updateValue1)
            updateValue0
              | ((envEnvVAR1 1 environment) /= (-52)) = (boardBlVAR0 0 blackboard)
              | otherwise = (boardBlVAR0 0 blackboard)
              where
                (blackboard, environment) = privateTempBoardEnv1
            updateValue1
              | ((True && (boardBlDEFINE5 1 blackboard)) == False) = (boardBlVAR0 0 blackboard)
              | otherwise = "no"
              where
                (blackboard, environment) = privateTempBoardEnv1
    boardEnvUpdate1 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    boardEnvUpdate1 boardEnv = (updateLocalBoardLocalVAR2 nodeLocation blackboard (min 5 (max 2 (min 100 (max (-100) (- ((sereneCOUNT (sereneIMPLIES (boardBlDEFINE5 0 blackboard) (boardBlDEFINE5 0 blackboard)) ((localBoardLocalVAR2 nodeLocation blackboard) > (-12))) + (sereneCOUNT False ((-21) == (localBoardLocalVAR2 nodeLocation blackboard))))))))), environment)
      where
        (blackboard, environment) = boardEnv
    boardEnvUpdate2 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    boardEnvUpdate2 boardEnv
      | not ((50 >= (min 100 (max (-100) (max 20 23))))) = boardEnv
      | otherwise = privateBoardEnv
      where
        (conditionBlackboard, conditionEnvironment) = boardEnv
        privateTempBoardEnv0 = boardEnv
        privateBoardEnv = privateTempBoardEnv1
        privateTempBoardEnv1
          | ((sereneXOR (boardBlDEFINE5 0 blackboard) (boardBlDEFINE5 1 blackboard)) || False) = (updateLocalBoardLocalVAR2 nodeLocation blackboard (min 5 (max 2 (min 100 (max (-100) (max (localBoardLocalDEFINE3 nodeLocation 0 blackboard) (-20)))))), environment)
          | (((envEnvDEFINE4 blackboard environment) > (envEnvDEFINE4 blackboard environment)) && (93 >= (localBoardLocalVAR2 nodeLocation blackboard))) = (updateLocalBoardLocalVAR2 nodeLocation blackboard (min 5 (max 2 (min 100 (max (-100) ((min 100 (max (-100) (max (envEnvVAR1 1 environment) (envEnvVAR1 0 environment)))) * ((-95) * ((min 100 (max (-100) ((localBoardLocalVAR2 nodeLocation blackboard) + ((localBoardLocalVAR2 nodeLocation blackboard) + (-28))))) * (min 100 (max (-100) (abs (-74))))))))))), environment)
          | otherwise = (updateLocalBoardLocalVAR2 nodeLocation blackboard (min 5 (max 2 (localBoardLocalDEFINE3 nodeLocation 0 blackboard))), environment)
          where
            (blackboard, environment) = privateTempBoardEnv0
    preStatusBoardEnv =  (oldBlackboard, oldEnvironment)
    returnStatus = returnStatement preStatusBoardEnv
    (newBlackboard, newEnvironment) = boardEnvUpdate2 . boardEnvUpdate1 . boardEnvUpdate0 $ preStatusBoardEnv
    newFutureChanges = futureChanges
