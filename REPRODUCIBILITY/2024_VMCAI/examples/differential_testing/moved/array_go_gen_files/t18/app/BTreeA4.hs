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
    boardEnvUpdate0 boardEnv = (arrayUpdateBoardBlVAR2 blackboard updates, environment)
      where
        (blackboard, environment) = boardEnv
        updates = [updatePair0]
        updatePair0 = ((min 2 (max 0 (boardBlDEFINE7 1 blackboard))), updateValue0)
        updateValue0
          | (sereneIMPLIES (boardBlDEFINE4 blackboard) True) = (min 5 (max 2 ((sereneCOUNT ((-93) > (max (-69) (boardBlVAR0 1 blackboard))) ((boardBlVAR2 2 blackboard) > (15 * ((-71) * (55 * (boardBlVAR2 1 blackboard)))))) + (sereneCOUNT ((- 4) < ((boardBlDEFINE7 2 blackboard) * ((-9) * (boardBlVAR2 1 blackboard)))) ((boardBlVAR0 1 blackboard) /= (-58))))))
          | otherwise = (min 5 (max 2 (abs ((-25) + ((boardBlVAR0 0 blackboard) + ((boardBlDEFINE7 0 blackboard) + 85))))))
          where
            (blackboard, environment) = boardEnv
    boardEnvUpdate1 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    boardEnvUpdate1 boardEnv = (arrayUpdateBoardBlVAR0 blackboard updates, environment)
      where
        (blackboard, environment) = boardEnv
        updates = [updatePair0]
        updatePair0 = ((min 1 (max 0 (abs (abs (-37))))), updateValue0)
        updateValue0
          | (sereneIMPLIES (boardBlDEFINE4 blackboard) (boardBlDEFINE4 blackboard)) = (min (-2) (max (-5) 42))
          | otherwise = (min (-2) (max (-5) (-42)))
          where
            (blackboard, environment) = boardEnv
    returnStatement :: (BTreeBlackboard, BTreeEnvironment) -> BTreeNodeStatus
    returnStatement boardEnv
      | (sereneIMPLIES ((boardBlVAR0 1 blackboard) < (boardBlVAR2 1 blackboard)) (boardBlDEFINE4 blackboard)) = Failure
      | ((boardBlDEFINE4 blackboard) && False) = Failure
      | otherwise = Failure
      where
        (blackboard, environment) = boardEnv
    preStatusBoardEnv = boardEnvUpdate1 . boardEnvUpdate0 $ (oldBlackboard, oldEnvironment)
    returnStatus = returnStatement preStatusBoardEnv
    (newBlackboard, newEnvironment) =  preStatusBoardEnv
    newFutureChanges = futureChanges
