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
    boardEnvUpdate0 boardEnv = (arrayUpdateLocalBoardLocalVAR2 nodeLocation blackboard updates, environment)
      where
        (blackboard, environment) = boardEnv
        updates = [updatePair0]
        updatePair0 = ((min 1 (max 0 (localBoardLocalDEFINE4 nodeLocation 1 blackboard))), updateValue0)
        updateValue0
          | ((boardBlDEFINE5 blackboard) == 15) = (((boardBlVAR0 1 blackboard) - 67) /= (18 - (-4)))
          | otherwise = (99 < (min (boardBlVAR0 1 blackboard) (-29)))
          where
            (blackboard, environment) = boardEnv
    returnStatement :: (BTreeBlackboard, BTreeEnvironment) -> BTreeNodeStatus
    returnStatement boardEnv
      | ((boardBlDEFINE5 blackboard) < (boardBlDEFINE5 blackboard)) = Failure
      | otherwise = Running
      where
        (blackboard, environment) = boardEnv
    boardEnvUpdate1 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    boardEnvUpdate1 boardEnv = (blackboard, arrayUpdateEnvEnvVAR1 environment updates)
      where
        (blackboard, environment) = boardEnv
        updates = [updatePair0, updatePair1]
        updatePair0 = ((min 1 (max 0 (min (-22) (boardBlVAR0 0 blackboard)))), updateValue0)
        updatePair1 = ((min 1 (max 0 (min (min (-6) (-24)) (min 18 (boardBlVAR0 0 blackboard))))), updateValue1)
        updateValue0
          | False = (min 5 (max 2 (abs (abs ((-74) * ((-52) * (localBoardLocalDEFINE4 nodeLocation 0 blackboard)))))))
          | (localBoardLocalVAR2 nodeLocation 0 blackboard) = (min 5 (max 2 (- (localBoardLocalDEFINE4 nodeLocation 1 blackboard))))
          | otherwise = (min 5 (max 2 (envEnvVAR1 1 environment)))
          where
            (blackboard, environment) = boardEnv
        updateValue1
          | (localBoardLocalVAR2 nodeLocation 0 blackboard) = (min 5 (max 2 (min (localBoardLocalDEFINE4 nodeLocation 0 blackboard) (-56))))
          | True = (min 5 (max 2 ((((boardBlVAR0 1 blackboard) * (localBoardLocalDEFINE4 nodeLocation 0 blackboard)) * (localBoardLocalDEFINE4 nodeLocation 1 blackboard)) * ((- (localBoardLocalDEFINE4 nodeLocation 1 blackboard)) * ((min (-28) 56) * ((sereneCOUNT (41 < (envEnvVAR1 1 environment)) ((-85) < (-51))) * (localBoardLocalDEFINE4 nodeLocation 1 blackboard)))))))
          | otherwise = (min 5 (max 2 (8 - (-18))))
          where
            (blackboard, environment) = boardEnv
    boardEnvUpdate2 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    boardEnvUpdate2 boardEnv = (blackboard, arrayUpdateEnvEnvVAR1 environment updates)
      where
        (blackboard, environment) = boardEnv
        updates = [updatePair0]
        updatePair0 = ((min 1 (max 0 (-69))), updateValue0)
        updateValue0 = (min 5 (max 2 (-19)))
          where
            (blackboard, environment) = boardEnv
    futureChanges0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    futureChanges0 boardEnv = (blackboard, arrayUpdateEnvEnvVAR1 environment updates)
      where
        (blackboard, environment) = boardEnv
        updates = [updatePair0]
        updatePair0 = ((min 1 (max 0 ((min (-75) (-65)) + ((sereneCOUNT ((localBoardLocalVAR2 nodeLocation 0 blackboard) == False) (sereneIMPLIES (localBoardLocalVAR2 nodeLocation 0 blackboard) False)) + (sereneCOUNT (True == False) ((localBoardLocalDEFINE4 nodeLocation 0 blackboard) < 51)))))), updateValue0)
        updateValue0
          | ((localBoardLocalVAR2 nodeLocation 1 blackboard) == ((localBoardLocalDEFINE4 nodeLocation 1 blackboard) == (boardBlDEFINE5 blackboard))) = (min 5 (max 2 ((sereneCOUNT ((sereneXOR True True) /= True) ((localBoardLocalDEFINE4 nodeLocation 0 blackboard) <= (-57))) + (sereneCOUNT (((-9) - (boardBlVAR0 0 blackboard)) < (localBoardLocalDEFINE4 nodeLocation 0 blackboard)) ((-62) > (-94))))))
          | otherwise = (min 5 (max 2 ((abs 72) + ((31 + (boardBlVAR0 0 blackboard)) + (((localBoardLocalDEFINE4 nodeLocation 0 blackboard) * (envEnvVAR1 1 environment)) + (envEnvVAR1 0 environment))))))
          where
            (blackboard, environment) = boardEnv
    preStatusBoardEnv = boardEnvUpdate0 (oldBlackboard, oldEnvironment)
    returnStatus = returnStatement preStatusBoardEnv
    (newBlackboard, newEnvironment) = boardEnvUpdate2 . boardEnvUpdate1 $ preStatusBoardEnv
    newFutureChanges = futureChanges0 : futureChanges
