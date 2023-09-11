module BTreeA3 where
import BehaviorTreeCore
import BehaviorTreeBlackboard
import BehaviorTreeEnvironment
import SereneRandomizer
import SereneOperations



bTreeFunctionA3 :: [BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
bTreeFunctionA3 _ nodeLocation _ _ _ _ oldBlackboard oldEnvironment futureChanges = (returnStatus, [], [], newBlackboard, newEnvironment, newFutureChanges)
  where
    returnStatement :: (BTreeBlackboard, BTreeEnvironment) -> BTreeNodeStatus
    returnStatement boardEnv
      | True = Success
      | (sereneXNOR (sereneXNOR True (boardBlDEFINE5 1 blackboard)) ((boardBlDEFINE5 1 blackboard) == False)) = Running
      | (((localBoardLocalVAR2 nodeLocation blackboard) <= (localBoardLocalVAR2 nodeLocation blackboard)) == (sereneIMPLIES (boardBlDEFINE5 1 blackboard) True)) = Failure
      | otherwise = Success
      where
        (blackboard, environment) = boardEnv
    boardEnvUpdate0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    boardEnvUpdate0 boardEnv = (blackboard, arrayUpdateEnvEnvVAR1 environment updates)
      where
        (blackboard, environment) = boardEnv
        updates = [updatePair0]
        updatePair0 = ((min 2 (max 0 (-74))), updateValue0)
        updateValue0
          | True = (min (-2) (max (-5) (-91)))
          | True = (min (-2) (max (-5) (min 100 (max (-100) ((min 100 (max (-100) (abs (envEnvVAR1 1 environment)))) - (min 100 (max (-100) (abs 57))))))))
          | otherwise = (min (-2) (max (-5) (min 100 (max (-100) (min (-53) (min 100 (max (-100) ((localBoardLocalVAR2 nodeLocation blackboard) * ((-2) * ((envEnvVAR1 2 environment) * (envEnvVAR1 0 environment)))))))))))
          where
            (blackboard, environment) = boardEnv
    boardEnvUpdate1 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    boardEnvUpdate1 boardEnv = (blackboard, arrayUpdateEnvEnvVAR1 environment updates)
      where
        (blackboard, environment) = boardEnv
        updates = [updatePair0]
        updatePair0 = ((min 2 (max 0 (min 100 (max (-100) ((min 100 (max (-100) ((min 100 (max (-100) (max (-3) (envEnvDEFINE4 blackboard environment)))) + ((min 100 (max (-100) (max (localBoardLocalVAR2 nodeLocation blackboard) (envEnvVAR1 1 environment)))) + (min 100 (max (-100) (max (envEnvDEFINE4 blackboard environment) 40))))))) * (min 100 (max (-100) (- (min 100 (max (-100) (abs (-73)))))))))))), updateValue0)
        updateValue0
          | ((envEnvVAR1 0 environment) > (localBoardLocalVAR2 nodeLocation blackboard)) = (min (-2) (max (-5) (min 100 (max (-100) (- (envEnvDEFINE4 blackboard environment))))))
          | ((True && (boardBlDEFINE5 1 blackboard)) || ((envEnvDEFINE4 blackboard environment) == (-36))) = (min (-2) (max (-5) (min 100 (max (-100) (max 12 (-21))))))
          | otherwise = (min (-2) (max (-5) (min 100 (max (-100) (((sereneCOUNT (71 <= 80) ((-33) > (-99))) + (sereneCOUNT (sereneIMPLIES (boardBlDEFINE5 0 blackboard) True) ((boardBlDEFINE5 1 blackboard) && (boardBlDEFINE5 1 blackboard)))) * (min 100 (max (-100) ((envEnvDEFINE4 blackboard environment) * (-95)))))))))
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
        privateTempBoardEnv1 = (arrayUpdateBoardBlVAR0 blackboard updates, environment)
          where
            (blackboard, environment) = privateTempBoardEnv0
            updates = [updatePair0, updatePair1, updatePair2]
            updatePair0 = ((min 2 (max 0 (min 100 (max (-100) (abs (localBoardLocalVAR2 nodeLocation blackboard)))))), updateValue0)
            updatePair1 = ((min 2 (max 0 (min 100 (max (-100) (max (min 100 (max (-100) (abs (-39)))) (envEnvVAR1 0 environment)))))), updateValue1)
            updatePair2 = ((min 2 (max 0 ((sereneCOUNT (sereneXOR True False) (sereneXOR True (boardBlDEFINE5 1 blackboard))) + (sereneCOUNT ((boardBlDEFINE5 0 blackboard) == False) ((boardBlDEFINE5 0 blackboard) /= (boardBlDEFINE5 1 blackboard)))))), updateValue2)
            updateValue0 = "both"
              where
                (blackboard, environment) = privateTempBoardEnv0
            updateValue1 = (boardBlVAR0 2 blackboard)
              where
                (blackboard, environment) = privateTempBoardEnv0
            updateValue2 = (boardBlVAR0 1 blackboard)
              where
                (blackboard, environment) = privateTempBoardEnv0
    futureChanges0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    futureChanges0 boardEnv = (blackboard, arrayUpdateEnvEnvVAR1 environment updates)
      where
        (blackboard, environment) = boardEnv
        updates = [updatePair0, updatePair1, updatePair2]
        updatePair0 = ((min 2 (max 0 (min 100 (max (-100) ((min 100 (max (-100) ((localBoardLocalVAR2 nodeLocation blackboard) + (49 + ((envEnvVAR1 0 environment) + (envEnvVAR1 2 environment)))))) * ((min 100 (max (-100) (max (envEnvDEFINE4 blackboard environment) (envEnvDEFINE4 blackboard environment)))) * (96 * (-98)))))))), updateValue0)
        updatePair1 = ((min 2 (max 0 (min 100 (max (-100) (32 - 67))))), updateValue1)
        updatePair2 = ((min 2 (max 0 (min 100 (max (-100) ((localBoardLocalVAR2 nodeLocation blackboard) + (35 + (min 100 (max (-100) (- 21))))))))), updateValue2)
        updateValue0
          | False = (min (-2) (max (-5) ((sereneCOUNT (sereneXNOR (sereneXNOR (boardBlDEFINE5 0 blackboard) (boardBlDEFINE5 0 blackboard)) (sereneXOR False True)) (23 <= (min 100 (max (-100) (max 46 5))))) + (sereneCOUNT False ((envEnvVAR1 0 environment) > (sereneCOUNT ((envEnvDEFINE4 blackboard environment) <= (envEnvVAR1 2 environment)) ("no" /= "both")))))))
          | ("yes" /= (boardBlVAR0 1 blackboard)) = (min (-2) (max (-5) (min 100 (max (-100) ((envEnvVAR1 1 environment) * (envEnvDEFINE4 blackboard environment))))))
          | otherwise = (min (-2) (max (-5) (-18)))
          where
            (blackboard, environment) = boardEnv
        updateValue1
          | (sereneXNOR False ((envEnvVAR1 1 environment) > (envEnvDEFINE4 blackboard environment))) = (min (-2) (max (-5) (min 100 (max (-100) ((min 100 (max (-100) (max (sereneCOUNT ((localBoardLocalVAR2 nodeLocation blackboard) > 70) ((localBoardLocalVAR2 nodeLocation blackboard) >= (envEnvDEFINE4 blackboard environment))) (min 100 (max (-100) (- (localBoardLocalVAR2 nodeLocation blackboard))))))) * (min 100 (max (-100) (33 - (-5)))))))))
          | (sereneXOR ((min 100 (max (-100) (abs (envEnvDEFINE4 blackboard environment)))) == (envEnvDEFINE4 blackboard environment)) (boardBlDEFINE5 0 blackboard)) = (min (-2) (max (-5) (sereneCOUNT ((envEnvDEFINE4 blackboard environment) > (envEnvDEFINE4 blackboard environment)) ((localBoardLocalVAR2 nodeLocation blackboard) >= (envEnvVAR1 2 environment)))))
          | otherwise = (min (-2) (max (-5) 48))
          where
            (blackboard, environment) = boardEnv
        updateValue2
          | (sereneIMPLIES (boardBlDEFINE5 0 blackboard) (boardBlDEFINE5 1 blackboard)) = (min (-2) (max (-5) (min 100 (max (-100) ((-24) - (envEnvVAR1 1 environment))))))
          | (sereneIMPLIES (boardBlDEFINE5 1 blackboard) (boardBlDEFINE5 0 blackboard)) = (min (-2) (max (-5) (min 100 (max (-100) (94 + ((-43) + (45 + 19)))))))
          | otherwise = (min (-2) (max (-5) (min 100 (max (-100) (19 + ((-93) + (-3)))))))
          where
            (blackboard, environment) = boardEnv
    preStatusBoardEnv =  (oldBlackboard, oldEnvironment)
    returnStatus = returnStatement preStatusBoardEnv
    (newBlackboard, newEnvironment) = boardEnvUpdate2 . boardEnvUpdate1 . boardEnvUpdate0 $ preStatusBoardEnv
    newFutureChanges = futureChanges0 : futureChanges
