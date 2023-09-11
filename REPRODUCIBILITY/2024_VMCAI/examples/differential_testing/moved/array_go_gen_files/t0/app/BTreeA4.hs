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
      | True = Running
      | (sereneXOR False False) = Failure
      | otherwise = Running
      where
        (blackboard, environment) = boardEnv
    boardEnvUpdate0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    boardEnvUpdate0 boardEnv
      | not (((min 100 (max (-100) (- 81))) /= (min 100 (max (-100) (abs (boardBlVAR2 conditionBlackboard)))))) = boardEnv
      | otherwise = privateBoardEnv
      where
        (conditionBlackboard, conditionEnvironment) = boardEnv
        privateTempBoardEnv0 = boardEnv
        privateBoardEnv = privateTempBoardEnv1
        privateTempBoardEnv1 = (arrayUpdateBoardBlVAR0 blackboard updates, environment)
          where
            (blackboard, environment) = privateTempBoardEnv0
            updates = [updatePair0, updatePair1]
            updatePair0 = ((min 1 (max 0 (min 100 (max (-100) ((envEnvFROZENVAR3 0 environment) * (3 * (-78))))))), updateValue0)
            updatePair1 = ((min 1 (max 0 (min 100 (max (-100) ((-5) - (sereneCOUNT (81 >= (boardBlVAR2 blackboard)) ((boardBlDEFINE4 blackboard) < (-43)))))))), updateValue1)
            updateValue0
              | (sereneXNOR ((boardBlVAR0 0 blackboard) < (-66)) (71 > (-2))) = (min 5 (max 2 (min 100 (max (-100) ((-25) - (min 100 (max (-100) (max (boardBlDEFINE4 blackboard) 32))))))))
              | otherwise = (min 5 (max 2 (min 100 (max (-100) (((sereneCOUNT (63 >= (envEnvVAR1 environment)) ((boardBlDEFINE4 blackboard) >= 36)) + (sereneCOUNT False ((envEnvDEFINE5 blackboard environment) && False))) + (71 + (envEnvVAR1 environment)))))))
              where
                (blackboard, environment) = privateTempBoardEnv0
            updateValue1
              | ((8 >= (-63)) || ((boardBlVAR0 0 blackboard) <= (-5))) = (min 5 (max 2 (min 100 (max (-100) (- (min 100 (max (-100) ((boardBlVAR0 1 blackboard) * (min 100 (max (-100) ((boardBlVAR2 blackboard) + (boardBlVAR0 0 blackboard))))))))))))
              | otherwise = (min 5 (max 2 (min 100 (max (-100) (51 * (98 * (boardBlDEFINE4 blackboard)))))))
              where
                (blackboard, environment) = privateTempBoardEnv0
    preStatusBoardEnv =  (oldBlackboard, oldEnvironment)
    returnStatus = returnStatement preStatusBoardEnv
    (newBlackboard, newEnvironment) = boardEnvUpdate0 preStatusBoardEnv
    newFutureChanges = futureChanges
