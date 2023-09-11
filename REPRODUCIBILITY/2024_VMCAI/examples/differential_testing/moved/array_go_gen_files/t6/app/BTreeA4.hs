module BTreeA4 where
import BehaviorTreeCore
import BehaviorTreeBlackboard
import BehaviorTreeEnvironment
import SereneRandomizer
import SereneOperations



bTreeFunctionA4 :: [BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
bTreeFunctionA4 _ nodeLocation _ _ _ _ oldBlackboard oldEnvironment futureChanges = (returnStatus, [], [], newBlackboard, newEnvironment, newFutureChanges)
  where
    boardEnvUpdate0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    boardEnvUpdate0 boardEnv
      | not (False) = boardEnv
      | otherwise = privateBoardEnv
      where
        (conditionBlackboard, conditionEnvironment) = boardEnv
        privateTempBoardEnv0 = boardEnv
        privateBoardEnv = privateTempBoardEnv1
        privateTempBoardEnv1 = (arrayUpdateBoardBlVAR0 blackboard updates, environment)
          where
            (blackboard, environment) = privateTempBoardEnv0
            updates = [updatePair0]
            updatePair0 = ((min 2 (max 0 ((-78) + (boardBlVAR3 blackboard)))), updateValue0)
            updateValue0
              | ((envEnvVAR1 1 environment) > (-63)) = (boardBlDEFINE6 0 blackboard)
              | otherwise = (((boardBlVAR3 blackboard) <= (boardBlDEFINE5 blackboard)) /= (True == True))
              where
                (blackboard, environment) = privateTempBoardEnv0
    returnStatement :: (BTreeBlackboard, BTreeEnvironment) -> BTreeNodeStatus
    returnStatement boardEnv
      | (sereneXNOR ((boardBlVAR0 2 blackboard) || (boardBlDEFINE6 1 blackboard)) (51 < (boardBlDEFINE5 blackboard))) = Failure
      | (True == (boardBlVAR0 1 blackboard)) = Failure
      | otherwise = Running
      where
        (blackboard, environment) = boardEnv
    boardEnvUpdate1 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    boardEnvUpdate1 boardEnv
      | not (((77 - (-69)) /= (envEnvVAR1 0 conditionEnvironment))) = boardEnv
      | otherwise = privateBoardEnv
      where
        (conditionBlackboard, conditionEnvironment) = boardEnv
        privateTempBoardEnv0 = boardEnv
        privateBoardEnv = privateTempBoardEnv1
        privateTempBoardEnv1
          | (False || (boardBlDEFINE6 2 blackboard)) = (updateBoardBlVAR4 blackboard (min 5 (max 2 (min (- (boardBlDEFINE5 blackboard)) (max (-5) (boardBlDEFINE5 blackboard))))), environment)
          | True = (updateBoardBlVAR4 blackboard (min 5 (max 2 ((- (boardBlDEFINE5 blackboard)) * ((sereneCOUNT (sereneIMPLIES (boardBlVAR0 1 blackboard) (boardBlDEFINE6 1 blackboard)) ((boardBlDEFINE6 2 blackboard) /= (boardBlVAR0 2 blackboard))) + (sereneCOUNT (sereneXOR (boardBlDEFINE6 0 blackboard) (boardBlDEFINE6 1 blackboard)) (sereneXNOR False (boardBlDEFINE6 0 blackboard))))))), environment)
          | otherwise = (updateBoardBlVAR4 blackboard (min 5 (max 2 (max (- (-59)) (-78)))), environment)
          where
            (blackboard, environment) = privateTempBoardEnv0
    boardEnvUpdate2 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    boardEnvUpdate2 boardEnv
      | not ((True || (boardBlDEFINE6 1 conditionBlackboard))) = boardEnv
      | otherwise = privateBoardEnv
      where
        (conditionBlackboard, conditionEnvironment) = boardEnv
        privateTempBoardEnv0 = boardEnv
        privateBoardEnv = privateTempBoardEnv1
        privateTempBoardEnv1
          | (boardBlDEFINE6 2 blackboard) = (updateBoardBlVAR4 blackboard (min 5 (max 2 (abs (min (boardBlVAR4 blackboard) 32)))), environment)
          | otherwise = (updateBoardBlVAR4 blackboard (min 5 (max 2 ((sereneCOUNT (False || (boardBlVAR0 1 blackboard)) ((abs (envEnvVAR1 0 environment)) > (min (boardBlVAR3 blackboard) (-73)))) + (sereneCOUNT False ((boardBlVAR0 1 blackboard) || (sereneXNOR ((boardBlVAR0 0 blackboard) || (boardBlDEFINE6 0 blackboard)) False)))))), environment)
          where
            (blackboard, environment) = privateTempBoardEnv0
    futureChanges0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    futureChanges0 boardEnv = (blackboard, arrayUpdateEnvEnvVAR1 environment updates)
      where
        (blackboard, environment) = boardEnv
        updates = [updatePair0, updatePair1]
        updatePair0 = ((min 1 (max 0 82)), updateValue0)
        updatePair1 = ((min 1 (max 0 ((-51) + (-4)))), updateValue1)
        updateValue0
          | (boardBlVAR0 2 blackboard) = (min (-2) (max (-5) (boardBlVAR3 blackboard)))
          | otherwise = (min (-2) (max (-5) (min (abs (boardBlVAR3 blackboard)) (- 46))))
          where
            (blackboard, environment) = boardEnv
        updateValue1
          | (((envEnvVAR1 1 environment) - (boardBlVAR4 blackboard)) >= ((envEnvVAR1 1 environment) * (32 * (13 * (boardBlDEFINE5 blackboard))))) = (min (-2) (max (-5) (min (max ((sereneCOUNT ((boardBlDEFINE5 blackboard) > 50) (False || False)) + (sereneCOUNT False (94 <= (boardBlDEFINE5 blackboard)))) 75) ((sereneCOUNT ((- (boardBlVAR3 blackboard)) /= (-43)) ((max (boardBlDEFINE5 blackboard) (boardBlDEFINE5 blackboard)) < (- (boardBlVAR3 blackboard)))) + (sereneCOUNT ((False == False) == True) (False == (boardBlDEFINE6 2 blackboard)))))))
          | otherwise = (min (-2) (max (-5) 89))
          where
            (blackboard, environment) = boardEnv
    preStatusBoardEnv = boardEnvUpdate0 (oldBlackboard, oldEnvironment)
    returnStatus = returnStatement preStatusBoardEnv
    (newBlackboard, newEnvironment) = boardEnvUpdate2 . boardEnvUpdate1 $ preStatusBoardEnv
    newFutureChanges = futureChanges0 : futureChanges
